RX_IDLE = 0
RX_START = 1
RX_TRANSMIT = 2

class CON_V3_IR:
    def __init__(self, config, interconnect):       
        self._interconnect = interconnect
        self._interconnect.register_port_device(self)
        self._interconnect.register_clock_device(self)

        self._receiver_port = config["receiver"]["port"]
        self._receiver_mask = config["receiver"]["mask"]
        self._receiver_enbl_mask = config["receiver"]["enbl_mask"]

        self._transmitter_port = config["transmitter"]["port"]
        self._transmitter_mask = config["transmitter"]["mask"]
        
        self._PORT = config.get("port")

        self._tx_silence_cycles_counter = 0
        self._tx_impulse_cycles_counter = 0
        self._rx_impulse_cycles_counter = 0
        self._rx_silence_cycles_counter = 0

        self._tx_byte = 0
        self._tx_bit_count = 0

        self._rx_step = RX_IDLE
        self._rx_byte = 0
        self._rx_bit_count = 8

        self._prev_pin_state = 0
        self._tx_prev_pin_state = 0

        self._package_index = 0

        self._rx_bytes = []
        self._rx_test = [
                #[0xAC, 0x00, 0x03, 0xD6, 0x51, 0x53, 0x55, 0x57, 0x59, 0x00, 0x04, 0x88, 0x00, 0x00, 0x10, 0x00, 0x02, 0x10, 0x01, 0xDD],
                [0xAC, 0x00, 0x03, 0xD6, 0x51, 0x53, 0x55, 0x57, 0x59, 0x00, 0x04, 0x88, 0x00, 0x00, 0x10, 0x00, 0x52, 0x00, 0x00, 0x1C],
                [0xAC, 0x0A, 0x03, 0xD6, 0x00, 0x00, 0x00, 0x03, 0x92]
        ]

        self._tx_handler = None

        self._send_count = 0
        self._tx_count = 0
        self._interconnect.emit_port(self, self._receiver_port, self._receiver_mask, 0)

    def set_serial_tx_handler(self, tx_handler):
        self._tx_handler = tx_handler

    def clock(self, cycles):
        self._tx_silence_cycles_counter += cycles
        self._tr(cycles)

    def _tr(self, cycles):
        if (self._rx_step != RX_IDLE):
            #print(self._rx_silence_cycles_counter, self._rx_impulse_cycles_counter)
            self._rx_impulse_cycles_counter += cycles
            if (self._rx_impulse_cycles_counter >= 0):
                self._interconnect.emit_port(self, self._receiver_port, self._receiver_mask, 1)
                self._rx_silence_cycles_counter += cycles
            if (self._rx_silence_cycles_counter >= 0):
                self._interconnect.emit_port(self, self._receiver_port, self._receiver_mask, 0)
                if (self._rx_step == RX_START):
                    self._rx_impulse_cycles_counter = -38232
                    self._rx_silence_cycles_counter = -9908
                    self._rx_step = RX_TRANSMIT
                    #print("start")
                else:
                    #print("next bit %X" % (self._rx_byte & 0x01))
                    if (self._rx_bit_count > 7):
                        if (self._rx_bytes):
                            self._rx_byte = self._rx_bytes.pop(0)
                            self._rx_bit_count = 0
                            print("RX %X" % self._rx_byte)
                        else:
                            #self.send_bytes()
                            return

                    self._rx_impulse_cycles_counter = -1768
                    if (self._rx_byte & 0x01):
                        self._rx_silence_cycles_counter = -5508
                    else:
                        self._rx_silence_cycles_counter = -3088
                    self._rx_byte >>= 1
                    self._rx_bit_count += 1


    def send_bytes(self):
        self._interconnect.emit_port(self, self._receiver_port, self._receiver_mask, 0)
        if (self._package_index >= len(self._rx_test)):
            self._package_index = 0
        self._rx_bytes = self._rx_test[self._package_index].copy()
        self._package_index += 1
        self._rx_byte = self._rx_bytes.pop(0)
        self._rx_bit_count = 0
        self._rx_step = RX_START
        self._rx_silence_cycles_counter = -1067348# -1067348
        self._rx_impulse_cycles_counter = -4680
        print("next trans %X" % (self._rx_byte & 0x1))
        print("RX %X" % self._rx_byte)

    def port_handler(self, port, mask, value):
        if (port == self._transmitter_port):
            if (self._prev_pin_state != mask):
                self._prev_pin_state = mask
                if (mask & self._transmitter_mask):
                    if (self._tx_silence_cycles_counter < 300):
                        self._tx_impulse_cycles_counter += self._tx_silence_cycles_counter
                        self._tx_silence_cycles_counter = 0
                    else:
                        self._tx_bit_count += 1
                        if (self._tx_silence_cycles_counter < 4000):
                            #print("tx", self._cycles_counter, self._impulse_cycles_counter)
                            #"receive 0"
                            self._tx_byte >>= 1
                        elif (self._tx_silence_cycles_counter < 8000):
                            #print("tx", self._cycles_counter, self._impulse_cycles_counter)
                            self._tx_byte = (self._tx_byte >> 1) | 0x80
                        else:
                            self._tx_bit_count = 0

                        #print("tx", self._cycles_counter, self._impulse_cycles_counter)
                        if (self._tx_bit_count == 8):
                            self._tx_bit_count = 0
                            self._tx_count += 1
                            print("TX %X" % (self._tx_byte & 0xFF))
                            #self._ser.write(bytes([(self._tx_byte & 0xFF)]))

                        if (self._tx_impulse_cycles_counter > 4000 and self._tx_impulse_cycles_counter < 6000):
                            print("TX ens", self._tx_impulse_cycles_counter)
                            #self.send_bytes()
                            #self._tx_count = 0
                        self._tx_impulse_cycles_counter = 0
                        self._tx_silence_cycles_counter = 0
                        

                    
        if (port == self._receiver_port):
            if (self._tx_prev_pin_state != mask & self._receiver_enbl_mask):
                self._tx_prev_pin_state = mask & self._receiver_enbl_mask
                if (mask & self._receiver_enbl_mask == 0):
                    self.send_bytes()
                    pass
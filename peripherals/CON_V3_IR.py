RX_IDLE = 0
RX_TRANSMIT = 1
RX_STOP = 2

RX_BUFFER_SIZE = 0

BURST_AGC_CYCLES = 38232
SPACE_AGC_CYCLES = 9908

BURST_BIT_CYCLES = 1768
SPACE_BIT0_CYCLES = 3088
SPACE_BIT1_CYCLES = 5508
BURST_END_CYCLES = 4680
BURST_PULSE_CYCLES = 104

SPACE_BIT_THRESHOLD_CYCLES = (SPACE_BIT1_CYCLES + SPACE_BIT0_CYCLES) // 2
BURST_PULSE_THRESHOLD_CYCLES = BURST_PULSE_CYCLES + 5

class CON_V3_IR:
    def __init__(self, config, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_port_device(self)
        self._interconnect.register_clock_device(self)
        self._interconnect.register_serial_rx_device(self)

        self._receiver_port = config["receiver"]["port"]
        self._receiver_mask = config["receiver"]["mask"]
        self._receiver_enbl_mask = config["receiver"]["enbl_mask"]

        self._transmitter_port = config["transmitter"]["port"]
        self._transmitter_mask = config["transmitter"]["mask"]

        self._tx_burst_cycles_counter = 0
        self._tx_space_cycles_counter = 0
        self._rx_burst_cycles_counter = 0
        self._rx_space_cycles_counter = 0
        self._tx_byte = 0
        self._tx_bit_count = 0

        self._rx_step = RX_IDLE
        self._rx_byte_queue = []
        self._rx_byte = 0
        self._rx_bit_count = 0

        self._prev_pin_state = 0

        self._interconnect.emit_port(self, self._receiver_port, self._receiver_mask, 0)

    def clock(self, cycles):
        self._tx_space_cycles_counter += cycles

        if (self._rx_step != RX_IDLE):
            self._rx_burst_cycles_counter += cycles
            if (self._rx_burst_cycles_counter >= 0):
                self._interconnect.emit_port(self, self._receiver_port, self._receiver_mask, 1)
                self._rx_space_cycles_counter += cycles
                if (self._rx_step == RX_STOP):
                    self._rx_step = RX_IDLE
                elif (self._rx_space_cycles_counter >= 0):
                    self._interconnect.emit_port(self, self._receiver_port, self._receiver_mask, 0)
                    if (self._rx_bit_count == 8):
                        self._rx_bit_count = 0
                        if (self._rx_byte_queue):
                            self._rx_byte = self._rx_byte_queue.pop(0)
                        else:
                            self._rx_burst_cycles_counter = -BURST_END_CYCLES
                            self._rx_step = RX_STOP
                            return

                    self._rx_burst_cycles_counter = -BURST_BIT_CYCLES
                    if (self._rx_byte & 0x01):
                        self._rx_space_cycles_counter = -SPACE_BIT1_CYCLES
                    else:
                        self._rx_space_cycles_counter = -SPACE_BIT0_CYCLES
                    self._rx_byte >>= 1
                    self._rx_bit_count += 1

                    
    def serial_rx_handler(self, data):
        self._rx_byte_queue.extend(data)
        if (self._rx_step == RX_IDLE and len(self._rx_byte_queue) > RX_BUFFER_SIZE):
            self._interconnect.emit_port(self, self._receiver_port, self._receiver_mask, 0)
            self._rx_byte = self._rx_byte_queue.pop(0)
            self._rx_bit_count = 0
            self._rx_burst_cycles_counter = -BURST_AGC_CYCLES
            self._rx_space_cycles_counter = -SPACE_AGC_CYCLES
            self._rx_step = RX_TRANSMIT

    def port_handler(self, port, mask, value):
        if (port == self._transmitter_port):
            if (self._prev_pin_state != mask):
                self._prev_pin_state = mask
                if (mask & self._transmitter_mask):
                    if (self._tx_space_cycles_counter < BURST_PULSE_THRESHOLD_CYCLES):
                        self._tx_burst_cycles_counter += self._tx_space_cycles_counter
                    else:
                        if (self._tx_burst_cycles_counter < BURST_END_CYCLES):
                            self._tx_byte >>= 1
                            if (self._tx_space_cycles_counter > SPACE_BIT_THRESHOLD_CYCLES):
                                self._tx_byte |= 0x80

                            self._tx_bit_count += 1
                            if (self._tx_bit_count == 8):
                                self._interconnect.emit_serial_tx(bytes([self._tx_byte & 0xFF]))
                                self._tx_bit_count = 0
                        else:
                            self._tx_bit_count = 0

                        self._tx_burst_cycles_counter = 0
                        
                    self._tx_space_cycles_counter = 0
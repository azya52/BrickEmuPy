ROM_SIZE = 1024
PAGE_SIZE = 256
WRITE_PAGE_SIZE = 16

HW_ADDR_MASK = 0xF8

IDLE = 0
ADDR_BYTE = 1
WORD_ADDR = 2
WRITE_DATA = 3
READ_DATA = 4

class HT24LC08:
    def __init__(self, config, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_port_device(self)

        self._hw_addr = config.get("hw_address")
        self._port = config.get("port")
        self._SDA_mask = config.get("SDA")
        self._SCL_mask = config.get("SCL")
        self._mem_path = config.get("path")

        self._mem = bytearray(b'\x00' * ROM_SIZE)
        if self._mem_path:
            try:
                with open(self._mem_path, "rb") as f:
                    self._mem = bytearray(f.read(ROM_SIZE)).ljust(ROM_SIZE, b'\xFF')
            except FileNotFoundError:
                pass

        self._state = IDLE
        self._bit_count = 0
        self._curr_addr = 0
        self._scl = 1
        self._sda = 1
        self._ack_phase = False
        self._rx_byte = 0
        self._tx_byte = 0

    def __del__(self):
        if self._mem_path:
            try:
                with open(self._mem_path, "wb") as f:
                    f.write(self._mem)
            except Exception:
                pass

    def port_handler(self, port, mask, value):
        if (port == self._port):
            prev_scl = self._scl
            prev_sda = self._sda
            self._scl = mask & self._SCL_mask and value
            self._sda = mask & self._SDA_mask and value

            if (self._scl and (prev_scl != self._scl or prev_sda != self._sda)):
                
                if (prev_sda > self._sda): #START
                    self._state = ADDR_BYTE
                    self._bit_count = 0
                    self._ack_phase = False
                    self._interconnect.emit_port(self, self._port, self._SDA_mask, -1)

                elif (prev_sda < self._sda): #STOP
                    self._state = IDLE
                    self._ack_phase = False

                #SCL Rise
                
                elif self._ack_phase:
                    self._interconnect.emit_port(self, self._port, self._SDA_mask, 0)
                    self._ack_phase = False

                elif (self._state == READ_DATA):
                    if self._bit_count < 8:
                        if (self._tx_byte >> (7 - self._bit_count)) & 1:
                            self._interconnect.emit_port(self, self._port, self._SDA_mask, -1)
                        else:
                            self._interconnect.emit_port(self, self._port, self._SDA_mask, 0)                          
                        self._bit_count += 1
                    else:
                        self._curr_addr = (self._curr_addr + 1) % ROM_SIZE
                        self._tx_byte = self._mem[self._curr_addr]
                        self._bit_count = 0

                else:
                    self._rx_byte = (self._rx_byte << 1) | (self._sda > 0)
                    self._bit_count += 1
                    if (self._bit_count == 8):
                        rx_byte = self._rx_byte & 0xFF
                        self._bit_count = 0
                        
                        if self._state == ADDR_BYTE:
                            if ((rx_byte & HW_ADDR_MASK) == self._hw_addr):
                                self._ack_phase = True
                                self._curr_addr = ((rx_byte & ~HW_ADDR_MASK) >> 1) * PAGE_SIZE + (self._curr_addr % PAGE_SIZE)
                                if rx_byte & 1:
                                    self._state = READ_DATA
                                    self._tx_byte = self._mem[self._curr_addr]
                                else:
                                    self._state = WORD_ADDR
                            else:
                                self._state = IDLE

                        elif (self._state == WORD_ADDR):
                            self._ack_phase = True
                            self._curr_addr = self._curr_addr - (self._curr_addr % PAGE_SIZE) + rx_byte
                            self._state = WRITE_DATA

                        elif (self._state == WRITE_DATA):
                            self._ack_phase = True
                            curr_addr = self._curr_addr
                            self._mem[curr_addr] = rx_byte
                            self._curr_addr = curr_addr - (curr_addr % WRITE_PAGE_SIZE) + ((curr_addr + 1) % WRITE_PAGE_SIZE)
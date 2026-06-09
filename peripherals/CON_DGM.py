RX_IDLE = 0
RX_TRANSMIT = 1
RX_STOP = 2

PERIOD_SKIP = 2
MAX_PERIOD_COUNT = PERIOD_SKIP + 16

RX_WORD_SIZE = 2

LO_START_CYCLES = 67869
HI_START_CYCLES = 0

HI_AGC_CYCLES = 2135
LO_AGC_CYCLES = 1003

HI_BIT0_CYCLES = 1067
LO_BIT0_CYCLES = 3461

HI_BIT1_CYCLES = 2911
LO_BIT1_CYCLES = 1779

HI_END_CYCLES = 7000

class CON_DGM:
    def __init__(self, config, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_port_device(self)
        self._interconnect.register_clock_device(self)
        self._interconnect.register_serial_rx_device(self)

        self._port = config["port"]
        self._mask = config["mask"]

        self._tx_hi_cycles = 0
        self._tx_cycles_counter = 0
        self._tx_word = 0
        self._tx_period_count = 0

        self._rx_hi_cycles = 0
        self._rx_lo_cycles = 0
        self._rx_step = RX_IDLE
        self._rx_byte_queue = []
        self._rx_word = 0
        self._rx_period_count = 0

        self._prev_pin_state = 0xF

    def clock(self, cycles):
        self._tx_cycles_counter += cycles

        if (self._rx_step != RX_IDLE):
            self._rx_hi_cycles_counter += cycles
            if (self._rx_hi_cycles_counter >= 0):
                if (self._rx_step == RX_STOP):
                    self._interconnect.emit_port(self, self._port, self._mask, -1)
                    self._rx_step = RX_IDLE
                else:
                    self._interconnect.emit_port(self, self._port, self._mask, 0)
                    self._rx_lo_cycles_counter += cycles
                    if (self._rx_lo_cycles_counter >= 0):
                        self._interconnect.emit_port(self, self._port, self._mask, 1)
                        self._rx_period_count += 1
                        if (self._rx_period_count < PERIOD_SKIP):
                            self._rx_hi_cycles_counter = -HI_AGC_CYCLES
                            self._rx_lo_cycles_counter = -LO_AGC_CYCLES
                        elif (self._rx_period_count < MAX_PERIOD_COUNT):
                            if (self._rx_word & 0x8000):
                                self._rx_hi_cycles_counter = -HI_BIT1_CYCLES
                                self._rx_lo_cycles_counter = -LO_BIT1_CYCLES
                            else:
                                self._rx_hi_cycles_counter = -HI_BIT0_CYCLES
                                self._rx_lo_cycles_counter = -LO_BIT0_CYCLES
                            self._rx_word <<= 1
                        else:
                            self._rx_step = RX_STOP
                            self._rx_hi_cycles_counter = -HI_END_CYCLES

    def serial_rx_handler(self, data):
        self._rx_byte_queue.extend(data)
        if (len(self._rx_byte_queue) >= RX_WORD_SIZE):
            self._prev_rx_state = 1
            self._rx_word = self._rx_byte_queue.pop()
            self._rx_word |= self._rx_byte_queue.pop() << 8
            self._rx_period_count = 0
            self._rx_hi_cycles_counter = -HI_START_CYCLES
            self._rx_lo_cycles_counter = -LO_START_CYCLES
            self._rx_step = RX_TRANSMIT

    def port_handler(self, port, mask, value):
        if (port == self._port):
            if (self._prev_pin_state != mask):
                self._prev_pin_state = mask
                if (mask & self._mask):
                    self._tx_period_count += 1
                    if (self._tx_period_count > 2):
                        self._tx_word <<= 1
                        if (self._tx_hi_cycles > self._tx_cycles_counter):
                            self._tx_word |= 1
                        if self._tx_period_count == PERIOD_SKIP + 8 or self._tx_period_count == MAX_PERIOD_COUNT:
                            self._interconnect.emit_serial_tx(bytes([self._tx_word & 0xFF]))
                        if (self._tx_period_count == MAX_PERIOD_COUNT):
                            self._tx_period_count = 0
                else:
                    self._tx_hi_cycles = self._tx_cycles_counter
                self._tx_cycles_counter = 0
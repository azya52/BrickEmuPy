from .HT4BIT import HT4BIT

RAM_SIZE = 256
VRAM_SIZE = 128

EMPTY_VRAM = tuple([0] * VRAM_SIZE)
FUULL_VRAM = tuple([255] * VRAM_SIZE)

SUB_CLOCK = 32768

PC_RAM_BANK1 = 0x01
PC_LCD_ON = 0x02

class HTG12N0(HT4BIT):
    def __init__(self, mask, clock):
        super().__init__(mask, clock)

        self._PS_pullup_mask = mask['port_pullup']['PS']
        self._PM_pullup_mask = mask['port_pullup']['PM']

        self._PS_wakeup_mask = mask['port_wakeup']['PS']
        self._PM_wakeup_mask = mask['port_wakeup']['PM']

        self._rtc_div = clock / SUB_CLOCK * mask['rtc_clock_div']

        self._reset()

        self._execute = self._instructions_override({
            0b00110000: HTG12N0._out_pa_a,
            0b00110010: HTG12N0._in_a_pm,
            0b00110011: HTG12N0._in_a_ps,
            0b00110100: HTG12N0._out_pc_a,
            0b00110101: HTG12N0._out_pb_a
        })

    def _reset(self):
        super()._reset()
        
        self._RAM = [0] * RAM_SIZE
        self._VRAM = [0] * VRAM_SIZE 

        self._rtc_counter = 0
        
        self._PA = 0
        self._PB = 0
        self._PortC = 0

        self._PS = self._PS_pullup_mask
        self._PM = self._PM_pullup_mask

    def examine(self):
        return {
            "ACC": self._ACC,
            "PC": self._PC & 0x3FFF,
            "ST": self._STACK,
            "TC": self._TC,
            "CF": self._CF,
            "EF": self._EF,
            "TF": self._TF,
            "EI": self._EI,
            "HALT": self._HALT,
            "WR0": self._WR[0],
            "WR1": self._WR[1],
            "WR2": self._WR[2],
            "WR3": self._WR[3],
            "WR4": self._WR[4],
            "PM": self._PM,
            "PS": self._PS,
            "PA": self._PA,
            "PB": self._PB,
            "PRTC": self._PortC,
            "RAM": tuple(self._RAM),
            "GRAM": tuple(self._VRAM),
            **self._ROM.examine(),
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] & 0x3FFF
        if ("ST" in state):
            self._STACK = state["ST"] & 0xFFF
        if ("CF" in state):
            self._CF = state["CF"] & 0x1
        if ("EF" in state):
            self._EF = state["EF"] & 0x1
        if ("TF" in state):
            self._TF = state["TF"] & 0x1
        if ("EI" in state):
            self._EI = state["EI"] & 0x1
        if ("HALT" in state):
            self._HALT = state["HALT"] & 0x1
        if ("WR0" in state):
            self._WR[0] = state["WR0"] & 0xF
        if ("WR1" in state):
            self._WR[1] = state["WR1"] & 0xF
        if ("WR2" in state):
            self._WR[2] = state["WR2"] & 0xF
        if ("WR3" in state):
            self._WR[3] = state["WR3"] & 0xF
        if ("WR4" in state):
            self._WR[4] = state["WR4"] & 0xF
        if ("TC" in state):
            self._TC = state["TC"] & 0xFF
        if ("PA" in state):
            self._PA = state["PA"] & 0xF
        if ("PB" in state):
            self._PB = state["PB"] & 0xF
        if ("PRTC" in state):
            self._PortC = state["PRTC"] & 0xF
        if ("PM" in state):
            self._PM = state["PM"] & 0xF
        if ("PS" in state):
            self._PS = state["PS"] & 0xF
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xF
        if ("GRAM" in state):
            for i, value in state["VRAM"].items():
                self._VRAM[i] = value & 0xF
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
    
    def pin_set(self, port, pin, level):
        if (port == 'PM'):
            self._PM = ~(1 << pin) & self._PM | level << pin
            if ((self._PM_wakeup_mask & (1 << pin)) > 0):
                self._HALT = 0
        elif (port == 'PS'):
            self._PS = ~(1 << pin) & self._PS | level << pin
            if (self._PS_wakeup_mask & (1 << pin)):
                self._HALT = 0
        elif (port == 'RES'):
            self._reset()
            self._RESET = 1

    def pin_release(self, port, pin):
        if (port == 'PM'):
            self._PM &= ~(1 << pin)
            self._PM |= self._PM_pullup_mask & (1 << pin)
        elif (port == 'PS'):
            self._PS &= ~(1 << pin)
            self._PS |= self._PS_pullup_mask & (1 << pin)
        elif (port == 'RES'):
            self._RESET = 0
    
    def get_VRAM(self):
        if (not (self._PortC & PC_LCD_ON) | self._RESET):
            return EMPTY_VRAM
        return tuple(self._VRAM)

    def clock(self):
        exec_cycles = super().clock()

        self._rtc_counter -= exec_cycles
        while (self._rtc_counter <= 0):
            self._rtc_counter += self._rtc_div
            self._EF = 1
            self._HALT = 0

        return exec_cycles

    def _read_RAM(self, rp):
        index = (self._WR[rp + 1] << 4) | self._WR[rp]
        if (index >= 128):
            return self._VRAM[index - 128]
        if (self._PortC & PC_RAM_BANK1):
            return self._RAM[index + 128]
        return self._RAM[index]
         
    def _write_RAM(self, rp, value):
        index = (self._WR[rp + 1] << 4) | self._WR[rp]
        if (index >= 128):
            self._VRAM[index - 128] = value
        elif (self._PortC & PC_RAM_BANK1):
            self._RAM[index + 128] = value
        else:
            self._RAM[index] = value
    
    def _out_pa_a(self, opcode):
        self._PA = self._ACC
        self._PC += 1

        return 4

    def _out_pc_a(self, opcode):
        self._PortC = self._ACC
        self._PC += 1

        return 4

    def _out_pb_a(self, opcode):
        self._PB = self._ACC
        self._PC = ((self._PB & 0x3) << 12) | (self._PC & 0xFFF)
        self._PC += 1

        return 4

    def _in_a_pm(self, opcode):
        self._ACC = self._PM
        self._PC += 1

        return 4

    def _in_a_ps(self, opcode):
        self._ACC = self._PS
        self._PC += 1

        return 4
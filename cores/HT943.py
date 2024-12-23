from .HT4BIT import HT4BIT

RAM_SIZE = 256

EMPTY_VRAM = tuple([0] * 256)
FUULL_VRAM = tuple([255] * 256)

MCLOCK_DIV = 4

class HT943(HT4BIT):
    def __init__(self, mask, clock):
        super().__init__(mask, clock)

        self._PP_pullup_mask = mask['port_pullup']['PP']
        self._PS_pullup_mask = mask['port_pullup']['PS']
        self._PM_pullup_mask = mask['port_pullup']['PM']

        self._PP_wakeup_mask = mask['port_wakeup']['PP']
        self._PS_wakeup_mask = mask['port_wakeup']['PS']
        self._PM_wakeup_mask = mask['port_wakeup']['PM']

        self._reset()

        self._execute = self._instructions_override({
            0b00110000: HT943._out_pa_a,
            0b00110010: HT943._in_a_pm,
            0b00110011: HT943._in_a_ps,
            0b00110100: HT943._in_a_pp
        })

    def _reset(self):
        super()._reset()
        
        self._RAM = [0] * RAM_SIZE
        
        self._PA = 0
        self._PP = self._PP_pullup_mask
        self._PS = self._PS_pullup_mask
        self._PM = self._PM_pullup_mask

    def examine(self):
        return {
            "ACC": self._ACC,
            "PC": self._PC & 0xFFF,
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
            "PP": self._PP,
            "PM": self._PM,
            "PS": self._PS,
            "PA": self._PA,
            "RAM": tuple(self._RAM),
            **self._ROM.examine(),
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] & 0xFFF
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
        if ("PP" in state):
            self._PP = state["PP"] & 0xF
        if ("PM" in state):
            self._PM = state["PM"] & 0xF
        if ("PS" in state):
            self._PS = state["PS"] & 0xF
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xF
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
    
    def pin_set(self, port, pin, level):
        if (port == 'PP'):
            self._PP = ~(1 << pin) & self._PP | level << pin
            if (self._HALT and (self._PP_wakeup_mask & (1 << pin)) and (not level)):
                self._EF = 1
                self._HALT = 0
        elif (port == 'PM'):
            self._PM = ~(1 << pin) & self._PM | level << pin
            if (self._HALT and (self._PM_wakeup_mask & (1 << pin)) and (not level)):
                self._EF = 1
                self._HALT = 0
        elif (port == 'PS'):
            self._PS = ~(1 << pin) & self._PS | level << pin
            if (self._HALT and (self._PS_wakeup_mask & (1 << pin)) and (not level)):
                self._EF = 1
                self._HALT = 0
        elif (port == 'RES'):
            self._reset()
            self._RESET = 1

    def pin_release(self, port, pin):
        if (port == 'PP'):
            self._PP &= ~(1 << pin)
            self._PP |= self._PP_pullup_mask & (1 << pin)
        elif (port == 'PM'):
            self._PM &= ~(1 << pin)
            self._PM |= self._PM_pullup_mask & (1 << pin)
        elif (port == 'PS'):
            self._PS &= ~(1 << pin)
            self._PS |= self._PS_pullup_mask & (1 << pin)
        elif (port == 'RES'):
            self._RESET = 0
    
    def get_VRAM(self):
        if (self._HALT | self._RESET):
            return EMPTY_VRAM
        return tuple(self._RAM)
   
    def _out_pa_a(self, opcode):
        self._PA = self._ACC
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

    def _in_a_pp(self, opcode):
        self._ACC = self._PP
        self._PC += 1

        return 4
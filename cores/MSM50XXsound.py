SQUARENESS_FACTOR = 5
CHANNEL = 0

class MSM50XXsound():
    def __init__(self, mask, clock, interconnect):
        self._sound_freq_div = mask["sound_freq_div_tbl"]
        self._system_clock = clock
        self._interconnect = interconnect
        self._Freg = 0
        self._Freg4 = 2
        self._Mreg = 0
        self._melody_div1 = 0
        self._melody_div2 = 0
        self._state = 0

    def clock(self, exec_cycles):
        if (self._Freg):
            self._melody_div2 -= exec_cycles
            if (self._melody_div2 <= 0):
                self._melody_div2 += (self._system_clock // 16)
                self._state ^= 2
                self._melody_div1 -= self._melody_div2
                if (self._melody_div1 <= 0):
                    self._melody_div1 += (self._system_clock // 2)
                    self._state ^= 1
                if (self._Mreg == 0 and self._state & 0x2 == 0):
                    self._interconnect.emit_audio(CHANNEL, None)
                    self._Freg = 0
                elif (self._state & self._Mreg == self._Mreg and self._sound_freq_div[self._Freg]):
                    self._interconnect.emit_audio(CHANNEL, (self._system_clock / self._sound_freq_div[self._Freg], False, SQUARENESS_FACTOR, 0))
                else:
                    self._interconnect.emit_audio(CHANNEL, None)
        else:
            self._state = self._melody_div2 = self._melody_div1 = 0
            self._interconnect.emit_audio(CHANNEL, None)

    def set_sound(self, value):
        self._Freg = value & 0x3
        self._Mreg = value >> 2
        if (self._Freg == 2):
            self._Freg = self._Freg4
        
    def set_freq(self, value):
        self._Freg4 = value
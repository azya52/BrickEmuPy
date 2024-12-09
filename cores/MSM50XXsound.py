from .ToneGenerator import ToneGenerator

class MSM50XXsound():
    def __init__(self, clock):
        self._tone_generator = ToneGenerator()
        self._system_clock = clock
        self._current_cycle = 0
        self._Freg = 0
        self._Mreg = 0
        self._melody_div1 = 0
        self._melody_div2 = 0
        self._state = 0

    def clock(self, exec_cycles):
        self._current_cycle += exec_cycles
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
                    self._tone_generator.stop(self._current_cycle / self._system_clock)
                    self._Freg = 0
                if (self._state & self._Mreg == self._Mreg):
                    self._tone_generator.play((self._system_clock // 16) * self._Freg, False, 1/2, self._current_cycle / self._system_clock)
                else:
                    self._tone_generator.stop(self._current_cycle / self._system_clock)
        else:
            self._state = self._melody_div2 = self._melody_div1 = 0
            self._tone_generator.stop(self._current_cycle / self._system_clock)

    def set_freq(self, value):
        self._Freg = value & 0x3
        self._Mreg = value >> 2
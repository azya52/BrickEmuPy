MODE_DISABLE = 0
MODE_TONE = 1
MODE_RANDOM = 2
MODE_TONE_RANDOM = 3

SQUARENESS_FACTOR = 5

CHANNEL = 0
    
class EM73000sound():
    def __init__(self, clock, interconnect):
        self._interconnect = interconnect
        self._system_clock = clock
        self._basic_freq_div = 0
        self._freq_div = 0
        self._mode = 0

    def update(self):
        if (self._mode != MODE_DISABLE and (self._freq_div > 1)):
            freq = self._system_clock / self._basic_freq_div / self._freq_div / 2
            self._interconnect.emit_audio(CHANNEL, (freq, self._mode != MODE_TONE, SQUARENESS_FACTOR, 0))
        else:
            self._interconnect.emit_audio(CHANNEL, None)

    def set_basic_freq_div(self, basic_freq_div):
        self._basic_freq_div = basic_freq_div

    def set_freq_div(self, freq_div):
        self._freq_div = freq_div
        self.update()

    def set_mode(self, mode):
        self._mode = mode
        self.update()
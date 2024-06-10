from .ToneGenerator import ToneGenerator

MODE_DISABLE = 0
MODE_TONE = 1
MODE_RANDOM = 2
MODE_TONE_RANDOM = 3
    
class EM73000sound():
    def __init__(self, clock):
        self._system_clock = clock
        self._basic_freq_div = 0
        self._freq_div = 0
        self._mode = 0

        self._toneGenerator = ToneGenerator()

    def update(self):
        if (self._mode != MODE_DISABLE and (self._freq_div > 1)):
            freq = self._system_clock / self._basic_freq_div / self._freq_div / 2
            self._toneGenerator.addStart(freq, self._mode != MODE_TONE, 0.5)
        else:
            self._toneGenerator.stop()

    def stop(self):
        self._toneGenerator.close()
        del self._toneGenerator

    def set_basic_freq_div(self, basic_freq_div):
        self._basic_freq_div = basic_freq_div

    def set_freq_div(self, freq_div):
        self._freq_div = freq_div
        self.update()

    def set_mode(self, mode):
        self._mode = mode
        self.update()
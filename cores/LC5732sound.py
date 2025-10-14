from .ToneGenerator import ToneGenerator

SQUARENESS_FACTOR = 5

class LC5732sound():
    def __init__(self, mask, clock):
        self._system_clock = clock
        self._sound_freq_tbl = mask["sound_freq_tbl"]
        self._sound_duration_tbl = mask["sound_duration_tbl"]
        self._toneGenerator = ToneGenerator()

    def set_alm(self, alm, current_cycle):
        scal = alm & 0xF
        octave = (alm >> 4) & 0x3
        duration = (alm >> 6) & 0x3
        if (scal != 0xF and octave != 0x3):
            freq = self._sound_freq_tbl[octave][scal]
            duration = self._sound_duration_tbl[duration]
            self._toneGenerator.playFor(freq, False, duration, SQUARENESS_FACTOR, current_cycle / self._system_clock)
        else:
            self._toneGenerator.stop(current_cycle / self._system_clock)
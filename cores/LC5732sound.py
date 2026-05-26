SQUARENESS_FACTOR = 5
CHANNEL = 0

class LC5732sound():
    def __init__(self, mask, interconnect):
        self._sound_freq_tbl = mask["sound_freq_tbl"]
        self._interconnect = interconnect

    def set_alm(self, alm):
        scal = alm & 0xF
        octave = (alm >> 4) & 0x3
        if (scal != 0xF and octave != 0x3):
            freq = self._sound_freq_tbl[octave][scal]
            self._interconnect.emit_audio(CHANNEL, (freq, False, SQUARENESS_FACTOR, 0))
        else:
            self._interconnect.emit_audio(CHANNEL, None)
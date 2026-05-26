IO_SPEECH_CTRL_ENBL = 0x01

SUB_CLOCK = 32768

CHANNEL_TONEA = 0
CHANNEL_TONEB = 1
CHANNEL_NOISE = 2
CHANNEL_SPEECH = 3
   
class SPL0Xsound():
    def __init__(self, clock, sub_clock_div, interconnect):
        self._freq_factor = clock / sub_clock_div / SUB_CLOCK
        self._interconnect = interconnect

    def set_toneA(self, ctrl1, ctrl2):
        vol = (ctrl2 >> 6) / 3
        freq32 = (((ctrl2 & 0x3) << 8) | ctrl1) << 1
        if (vol > 0 and freq32 > 0):
            freq = self._freq_factor * freq32
            self._interconnect.emit_audio(CHANNEL_TONEA, (freq, False, vol, 0))
        else:
            self._interconnect.emit_audio(CHANNEL_TONEA, None)

    def set_toneB(self, ctrl1, ctrl2):
        vol = (ctrl2 >> 6) / 3
        freq32 = (((ctrl2 & 0x3) << 8) | ctrl1) << 1
        if (vol > 0 and freq32 > 0):
            freq = self._freq_factor * freq32
            self._interconnect.emit_audio(CHANNEL_TONEB, (freq, False, vol, 0))
        else:
            self._interconnect.emit_audio(CHANNEL_TONEB, None)

    def set_noise(self, ctrl1, ctrl2):
        vol = (ctrl2 >> 4) / 15
        freq32 = (16 - (ctrl1 & 0xF)) << 7
        if (vol > 0 and freq32 > 0):
            freq = self._freq_factor * freq32
            self._interconnect.emit_audio(CHANNEL_NOISE, (freq, True, vol, 0))
        else:
            self._interconnect.emit_audio(CHANNEL_NOISE, None)

    def set_speech(self, ctrl, data):
        amplitude = ((data & 0x3F) / 0x3F) * (1 - ((data >> 6) & 0x02)) #- 0.5
        if (data & 0x80):
            amplitude = 0
        if (data == 0 or not(ctrl & IO_SPEECH_CTRL_ENBL)):
            self._interconnect.emit_audio(CHANNEL_SPEECH, None)
        else:
            self._interconnect.emit_audio(CHANNEL_SPEECH, (0, False, amplitude, 0))
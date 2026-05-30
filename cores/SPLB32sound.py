IO_AUDIO_CTRL_PWM_ENBL = 0x80
IO_AUDIO_CTRL_TONE = 0x40
   
class SPLB32sound():
    def __init__(self, interconnect):
        self._interconnect = interconnect
        self._envelope = [0, 0]
        self._toggle_state = [1, 1]

    def set_data(self, channel, ctrl, data):
        if (ctrl & IO_AUDIO_CTRL_TONE):
            self._envelope[channel] = ((data & 0xFF) / 0xFF)
        else:
            if (data != 0):
                amplitude = ((data & 0xFF) / 128) - 1
                self._interconnect.emit_audio(channel, (0, False, amplitude, 0))
            else:  
                self._interconnect.emit_audio(channel, None)

    def toggle(self, channel):
        if (self._envelope[channel]):
            self._toggle_state[channel] *= -1
            self._interconnect.emit_audio(channel, (0, False, self._toggle_state[channel] * self._envelope[channel], 0))
        else:
            self._interconnect.emit_audio(channel, None)
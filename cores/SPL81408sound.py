IO_AUDIO_CTRL_ENBL = 0x80
IO_AUDIO_CTRL_TONE = 0x40

CHANNEL = 0
   
class SPL81408sound():
    def __init__(self, interconnect):
        self._interconnect = interconnect
        self._envelope = 0
        self._toggle_state = 1

    def set_data(self, ctrl, data):
        if (ctrl & IO_AUDIO_CTRL_ENBL):
            if (ctrl & IO_AUDIO_CTRL_TONE):
                self._envelope = ((data & 0xFF) / 0xFF)
            else:
                amplitude = ((data & 0xFF) / 128) - 1
                self._interconnect.emit_audio(CHANNEL, (0, False, amplitude, 0))
        else:
            self._interconnect.emit_audio(CHANNEL, None)

    def toggle(self):
        self._toggle_state *= -1
        self._interconnect.emit_audio(CHANNEL, (0, False, self._toggle_state * self._envelope, 0))
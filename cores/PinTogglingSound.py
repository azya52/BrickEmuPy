CHANNEL = 0

class PinTogglingSound:
    def __init__(self, interconnect):
        self._interconnect = interconnect
        self._toggle_state = 1

    def toggle(self, half_wave1, half_wave2):
        if (half_wave1 != half_wave2):
            self._toggle_state *= -1
            self._interconnect.emit_audio(CHANNEL, (0, False, self._toggle_state, 0))
            return
        else:
            self._interconnect.emit_audio(CHANNEL, None)
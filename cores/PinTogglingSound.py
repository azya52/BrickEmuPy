CHANNEL = 0

class PinTogglingSound:
    def __init__(self, interconnect):
        self._interconnect = interconnect

    def toggle(self, half_wave1, half_wave2):
        if (half_wave1 != half_wave2):
            self._interconnect.emit_audio(CHANNEL, (0, False, (half_wave1 > 0) + (half_wave2 > 0) * -1, 0))
        else:
            self._interconnect.emit_audio(CHANNEL, None)
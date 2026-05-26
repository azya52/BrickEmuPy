SQUARENESS_FACTOR = 5
CHANNEL = 0

class SPLB20sound():
    def __init__(self, clock, interconnect):
        self._system_clock = clock
        self._interconnect = interconnect
        self._tc_div = 1
        self._clock_div = 1
        self._enable = False

    def set_clock_div(self, clock_div):
        self._clock_div = clock_div
        self._tone()

    def set_tc_div(self, tc_div):
        self._tc_div = tc_div
        self._tone()

    def set_enable(self, enable):
        self._enable = enable
        self._tone()

    def _tone(self):
        if (self._tc_div > 0 and self._enable):
            freq = self._system_clock / self._clock_div / self._tc_div / 2
            self._interconnect.emit_audio(CHANNEL, (freq, False, SQUARENESS_FACTOR, 0))
        else:
            self._tone_on = False
            self._interconnect.emit_audio(CHANNEL, None)
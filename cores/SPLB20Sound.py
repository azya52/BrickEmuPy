from .ToneGenerator import ToneGenerator

SQUARENESS_FACTOR = 5

class SPLB20sound():
    def __init__(self, clock):
        self._system_clock = clock
        self._tc_div = 1
        self._clock_div = 1
        self._enable = False

        self._toneGenerator = ToneGenerator()

    def set_clock_div(self, clock_div, current_cycle):
        self._clock_div = clock_div
        self._tone(current_cycle)

    def set_tc_div(self, tc_div, current_cycle):
        self._tc_div = tc_div
        self._tone(current_cycle)

    def set_enable(self, enable, current_cycle):
        self._enable = enable
        self._tone(current_cycle)

    def _tone(self, current_cycle):
        if (self._tc_div > 0 and self._enable):
            freq = self._system_clock / self._clock_div / self._tc_div / 2
            self._toneGenerator.play(freq, False, SQUARENESS_FACTOR, current_cycle / self._system_clock)
        else:
            self._stop(current_cycle)
    
    def _stop(self, current_cycle):
        self._tone_on = False
        self._toneGenerator.stop(current_cycle / self._system_clock)
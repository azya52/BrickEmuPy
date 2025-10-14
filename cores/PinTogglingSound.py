from .ToneGenerator import ToneGenerator

class PinTogglingSound:

    def __init__(self, clock):
        self._clock = clock
        self._tone_generator = ToneGenerator()

    def toggle(self, half_wave1, half_wave2, current_cycle):
        if (half_wave1):
            self._tone_generator.play(0, False, 1, current_cycle / self._clock)
        elif (half_wave2):
            self._tone_generator.play(0, False, -1, current_cycle / self._clock)
        else:
            self._tone_generator.stop(current_cycle / self._clock)

    def stop(self):
        self._tone_generator.close()
        del self._tone_generator
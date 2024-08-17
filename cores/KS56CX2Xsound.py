from .ToneGenerator import ToneGenerator

class KS56CX2Xsound():
    def __init__(self, clock):
        self._clock = clock
        self._toneGenerator = ToneGenerator()

    def update(self, level, current_cycle):
        if (level):
            self._toneGenerator.play(1, False, -1, current_cycle / self._clock)
        else:
            self._toneGenerator.stop(current_cycle / self._clock)

    def stop(self):
        self._toneGenerator.close()
        del self._toneGenerator
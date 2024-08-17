from .ToneGenerator import ToneGenerator

class KS56CX2Xsound():
    def __init__(self):
        self._toneGenerator = ToneGenerator()

    def update(self, level):
        if (level):
            self._toneGenerator.addStart(1, False, -1)
        else:
            self._toneGenerator.stop()

    def stop(self):
        self._toneGenerator.close()
        del self._toneGenerator
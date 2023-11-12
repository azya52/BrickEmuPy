from PyQt6.QtMultimedia import QAudioFormat, QAudioSink

class Sound():
    def __init__(self):
        self._repeatCycle = 0
        self._channel = 0

    def stop(self):
        pass

    def setSoundChannel(self, channel):
        self._channel = channel

    def setOneCycle(self):
        self._repeatCycle = 0

    def setRepeatCycle(self):
        self._repeatCycle = 1

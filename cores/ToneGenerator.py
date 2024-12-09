import random

from PyQt6.QtCore import QIODeviceBase, QByteArray, QIODevice
from PyQt6.QtMultimedia import QAudioFormat, QAudioSink, QMediaDevices

BUFFER_SIZE = 4096
SOUND_LEVEL = (int) (32767 * 0.001)
SAMPLES_PART_SIZE = 4096
DATA_PART_SIZE = SAMPLES_PART_SIZE * 2

class AudioData(QIODevice):
    def __init__(self, sampleRate, bytesPerSample):
        super().__init__()
        self._toneStarts = []
        self._toneEnds = []
        self._currentByte = 0
        self._phase = 0
        self._sampleRate = sampleRate
        self._bytesPerSample = bytesPerSample
        self.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Unbuffered)
        
    def readData(self, maxlen):
        data = QByteArray()

        while maxlen:
            chunk = maxlen
            if (len(self._toneStarts) > 0):
                if (self._currentByte < self._toneStarts[0][0]):
                    chunk = min(maxlen, self._toneStarts[0][0] - self._currentByte)
                    data.append(chunk, b'\0')
                elif (len(self._toneEnds) == 0):
                    data.append(self.getSquareWaveData(chunk, self._toneStarts[0][1], self._toneStarts[0][2], self._toneStarts[0][3]))
                elif (self._currentByte < self._toneEnds[0]):
                    chunk = min(maxlen, self._toneEnds[0] - self._currentByte)
                    data.append(self.getSquareWaveData(chunk, self._toneStarts[0][1], self._toneStarts[0][2], self._toneStarts[0][3]))
                else:
                    self._toneStarts.pop(0)
                    self._toneEnds.pop(0)
                    continue
            else:
                return data.append(chunk, b'\0')

            self._currentByte += chunk
            maxlen -= chunk

        return data

    def getSquareWaveData(self, size, freq, noise, dutyRatio):
        phase = self._phase
        mul = freq / self._sampleRate
        squareWaveData = QByteArray()
        sample = prevSample = 0
        bytesPerSample = self._bytesPerSample
        size //= self._bytesPerSample
        for i in range(size):
            newSample = 1 - ((((i * mul + phase) % 1) > dutyRatio) << 1)
            if (newSample != prevSample):
                prevSample = newSample
                sample = (SOUND_LEVEL * newSample * random.choice([1, 1 - (noise << 1)])).to_bytes(bytesPerSample, 'big', signed=True)
            squareWaveData.append(sample)
        self._phase += size * mul
        return squareWaveData
    
    def bytesAvailable(self):
        return DATA_PART_SIZE
        
    def start(self, freq, noise, dutyRatio, goalTime):
        if (len(self._toneStarts) == 0):
            self._currentByte = round(self._sampleRate * goalTime) * self._bytesPerSample
        goalSample = DATA_PART_SIZE + round(self._sampleRate * goalTime) * self._bytesPerSample
        if (len(self._toneStarts) > len(self._toneEnds)):
            self._toneEnds.append(goalSample)
        if (freq > 0):
            self._toneStarts.append([goalSample, freq, noise, dutyRatio])

    def startFor(self, freq, noise, duration, dutyRatio, goalTime):
        if (len(self._toneStarts) == 0):
            self._currentByte = round(self._sampleRate * goalTime) * self._bytesPerSample
        goalSample = DATA_PART_SIZE + round(self._sampleRate * goalTime) * self._bytesPerSample
        if (len(self._toneStarts) > len(self._toneEnds)):
            self._toneEnds.append(goalSample)
        if (freq > 0):
            self._toneStarts.append([goalSample, freq, noise, dutyRatio])
            goalTime += duration
            goalSample = DATA_PART_SIZE + round(self._sampleRate * goalTime) * self._bytesPerSample
            self._toneEnds.append(goalSample)
        
    def stop(self, goalTime):
        if (len(self._toneStarts) > len(self._toneEnds)):
            goalSample = DATA_PART_SIZE + round(self._sampleRate * goalTime) * self._bytesPerSample
            self._toneEnds.append(goalSample)

class ToneGenerator(QAudioSink):
    def __init__(self):
        
        audioFormat = QAudioFormat()
        device = QMediaDevices.defaultAudioOutput()
        audioFormat.setSampleRate(device.maximumSampleRate())
        audioFormat.setChannelCount(1)
        audioFormat.setSampleFormat(QAudioFormat.SampleFormat.Int16)

        super().__init__(audioFormat)
        self.setBufferSize(BUFFER_SIZE)

        self._audioData = AudioData(audioFormat.sampleRate(), audioFormat.bytesPerSample())
        self.start(self._audioData)
        
    def play(self, freq, noise, dutyRatio, goalTime):
        self._audioData.start(freq, noise, dutyRatio, goalTime)

    def playFor(self, freq, noise, duration, dutyRatio, goalTime):
        self._audioData.startFor(freq, noise, duration, dutyRatio, goalTime)
        
    def stop(self, goalTime):
        self._audioData.stop(goalTime)
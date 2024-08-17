import time
import random

from PyQt6.QtCore import QIODeviceBase, QByteArray, QIODevice
from PyQt6.QtMultimedia import QAudioFormat, QAudioSink

SAMPLE_RATE = 44100
BUFFER_SIZE = 2048
SOUND_LEVEL = (int) (32767 * 0.1)
SAMPLES_PART_SIZE = 1000
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
        self._initTime = time.perf_counter()
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
                self._toneEnds.clear()
                self._initTime = time.perf_counter()
                self._currentByte = 0
                return data.append(chunk, b'\0')

            self._currentByte += chunk
            maxlen -= chunk

        return data

    def getSquareWaveData(self, size, freq, noise, dutyRatio):
        phase = self._phase
        mul = freq / self._sampleRate
        squareWaveData = QByteArray()
        prevSample = 0
        sample = 0
        for i in range(size // 2):
            newSample = SOUND_LEVEL if (((i * mul + phase) % 1) > dutyRatio) else 0
            if (newSample != prevSample):
                prevSample = newSample
                sample = -newSample if (noise and (random.random() > 0.5)) else newSample
            squareWaveData.append((sample & 0xFFFF).to_bytes(2, 'big'))
        self._phase += (size // 2) * mul
        return squareWaveData
    
    def bytesAvailable(self):
        return DATA_PART_SIZE
        
    def start(self, freq, noise, dutyRatio):
        goalTime = time.perf_counter() - self._initTime
        goalSample = DATA_PART_SIZE + int(self._sampleRate * goalTime) * self._bytesPerSample
        if (len(self._toneStarts) > len(self._toneEnds)):
            self._toneEnds.append(goalSample)
        if (freq > 0):
            self._toneStarts.append([goalSample, freq, noise, dutyRatio])

    def startFor(self, freq, noise, duration, dutyRatio):
        goalTime = time.perf_counter() - self._initTime
        goalSample = DATA_PART_SIZE + int(self._sampleRate * goalTime) * self._bytesPerSample
        if (len(self._toneStarts) > len(self._toneEnds)):
            self._toneEnds.append(goalSample)
        if (freq > 0):
            self._toneStarts.append([goalSample, freq, noise, dutyRatio])
            goalTime += duration
            goalSample = DATA_PART_SIZE + int(self._sampleRate * goalTime) * self._bytesPerSample
            self._toneEnds.append(goalSample)
        
    def stop(self):
        if (len(self._toneStarts) > len(self._toneEnds)):
            goalTime = time.perf_counter() - self._initTime
            goalSample = DATA_PART_SIZE + int(self._sampleRate * goalTime) * self._bytesPerSample
            self._toneEnds.append(goalSample)

class ToneGenerator(QAudioSink):
    def __init__(self):
        
        audioFormat = QAudioFormat()
        audioFormat.setSampleRate(SAMPLE_RATE)
        audioFormat.setChannelCount(1)
        audioFormat.setSampleFormat(QAudioFormat.SampleFormat.Int16)

        super().__init__(audioFormat)
        self.setBufferSize(BUFFER_SIZE)

        self._audioData = AudioData(audioFormat.sampleRate(), audioFormat.bytesPerSample())
        self.start(self._audioData)
        
    def addStart(self, freq, noise, dutyRatio):
        self._audioData.start(freq, noise, dutyRatio)

    def startFor(self, freq, noise, duration, dutyRatio):
        self._audioData.startFor(freq, noise, duration, dutyRatio)
        
    def stop(self):
        self._audioData.stop()

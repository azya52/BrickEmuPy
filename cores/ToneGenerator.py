import random, math

from PyQt6.QtCore import QIODeviceBase, QByteArray, QIODevice
from PyQt6.QtMultimedia import QAudioFormat, QAudioSink, QMediaDevices

BUFFER_SIZE = 4096
SOUND_LEVEL = (int) (32767 * 0.0005)
SAMPLES_PART_SIZE = 4096
SQUARENESS_FACTOR = 6
SAMPLE_RATE = 44100

class AudioData(QIODevice):
    def __init__(self, sampleRate, bytesPerSample, channelCount):
        super().__init__()
        self._toneStarts = []
        self._toneEnds = []
        self._currentByte = 0
        self._phase = 0
        self._sampleRate = sampleRate
        self._bytesPerSample = bytesPerSample
        self._channelCount = channelCount
        self.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Unbuffered)
        
    def readData(self, maxlen):
        data = QByteArray()

        while maxlen:
            chunk = maxlen
            if (len(self._toneStarts) > 0):
                if (self._currentByte < self._toneStarts[0][0]):
                    chunk = min(maxlen, self._toneStarts[0][0] - self._currentByte)
                    data.append(chunk, b'\0')
                    self._phase = 0
                elif (len(self._toneEnds) == 0):
                    data.append(self.getWaveData(chunk, self._toneStarts[0][1], self._toneStarts[0][2], self._toneStarts[0][3]))
                elif (self._currentByte < self._toneEnds[0]):
                    chunk = min(maxlen, self._toneEnds[0] - self._currentByte)
                    data.append(self.getWaveData(chunk, self._toneStarts[0][1], self._toneStarts[0][2], self._toneStarts[0][3]))
                else:
                    self._toneStarts.pop(0)
                    self._toneEnds.pop(0)
                    continue
            else:
                return data.append(chunk, b'\0')

            self._currentByte += chunk
            maxlen -= chunk

        return data

    def getWaveData(self, size, freq, noise, dutyRatio):
        phase = self._phase
        mul = math.pi * freq / self._sampleRate * 2
        waveData = QByteArray()
        channelCount = self._channelCount
        bytesPerSample = self._bytesPerSample
        size //= bytesPerSample * channelCount
        prevSample = rand = 1
        dutyRatio = dutyRatio * 2 - 1
        for i in range(size):
            newSample = max(-1, min(1, (math.sin(mul * i + phase) + dutyRatio) * SQUARENESS_FACTOR))
            if (noise and (newSample * prevSample < 0)):
                rand = random.choice([-1, 1])
                prevSample = newSample
            waveData.append(int(SOUND_LEVEL * newSample * rand).to_bytes(bytesPerSample, 'big', signed=True) * channelCount)
        self._phase += size * mul
        return waveData
   
    def bytesAvailable(self):
        return SAMPLES_PART_SIZE * self._channelCount * self._bytesPerSample
        
    def start(self, freq, noise, dutyRatio, goalTime):
        if (len(self._toneStarts) == 0):
            self._currentByte = round(self._sampleRate * goalTime) * self._bytesPerSample * self._channelCount
        goalSample = (SAMPLES_PART_SIZE + round(self._sampleRate * goalTime)) * self._bytesPerSample * self._channelCount
        if (len(self._toneStarts) > len(self._toneEnds)):
            self._toneEnds.append(goalSample)
        if (freq > 0):
            self._toneStarts.append([goalSample, freq, noise, dutyRatio])

    def startFor(self, freq, noise, duration, dutyRatio, goalTime):
        if (len(self._toneStarts) == 0):
            self._currentByte = round(self._sampleRate * goalTime) * self._bytesPerSample * self._channelCount
        goalSample = (SAMPLES_PART_SIZE + round(self._sampleRate * goalTime)) * self._bytesPerSample * self._channelCount
        self._toneEnds = []
        if (len(self._toneStarts) > len(self._toneEnds)):
            self._toneEnds.append(goalSample)
        if (freq > 0):
            self._toneStarts.append([goalSample, freq, noise, dutyRatio])
            goalTime += duration
            goalSample = (SAMPLES_PART_SIZE + round(self._sampleRate * goalTime)) * self._bytesPerSample * self._channelCount
            self._toneEnds.append(goalSample)
        
    def stop(self, goalTime):
        if (len(self._toneStarts) > len(self._toneEnds)):
            goalSample = (SAMPLES_PART_SIZE + round(self._sampleRate * goalTime)) * self._bytesPerSample * self._channelCount
            self._toneEnds.append(goalSample)

class ToneGenerator(QAudioSink):
    def __init__(self):
        
        device = QMediaDevices.defaultAudioOutput()
        audioFormat = device.preferredFormat()
        audioFormat.setSampleRate(SAMPLE_RATE)
        audioFormat.setSampleFormat(QAudioFormat.SampleFormat.Int16)

        super().__init__(audioFormat)
        self.setBufferSize(BUFFER_SIZE)

        self._audioData = AudioData(audioFormat.sampleRate(), audioFormat.bytesPerSample(), audioFormat.channelCount())
        self.start(self._audioData)
        
    def play(self, freq, noise, dutyRatio, goalTime):
        self._audioData.start(freq, noise, dutyRatio, goalTime)

    def playFor(self, freq, noise, duration, dutyRatio, goalTime):
        self._audioData.startFor(freq, noise, duration, dutyRatio, goalTime)
        
    def stop(self, goalTime):
        self._audioData.stop(goalTime)
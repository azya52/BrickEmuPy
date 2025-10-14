import random, math

from PyQt6.QtCore import QIODeviceBase, QByteArray, QIODevice
from PyQt6.QtMultimedia import QAudioFormat, QAudioSink, QMediaDevices

BUFFER_SIZE = 4096
SOUND_LEVEL = (int) (32767 * 0.15)
SAMPLES_PART_SIZE = 4096
SAMPLE_RATE = 44100

class AudioData(QIODevice):
    def __init__(self, sampleRate, bytesPerSample, channelCount):
        super().__init__()
        self._toneQueue = []
        self._currentByte = 0
        self._phase = 0
        self._sampleRate = sampleRate
        self._bytesPerSample = bytesPerSample
        self._channelCount = channelCount
        self._sampleSize = bytesPerSample * channelCount
        self.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Unbuffered)
        
    def readData(self, maxlen):
        data = QByteArray()
        while maxlen:
            if (len(self._toneQueue) > 0):
                if (self._currentByte < self._toneQueue[0][0]):
                    chunk = min(maxlen, self._toneQueue[0][0] - self._currentByte)
                    data.append(b'\0' * chunk)
                elif (len(self._toneQueue) == 1):
                    chunk = maxlen
                    data.append(self.getWaveData(chunk, self._toneQueue[0][1]))
                elif (self._currentByte < self._toneQueue[1][0]):
                    chunk = min(maxlen, self._toneQueue[1][0] - self._currentByte)
                    data.append(self.getWaveData(chunk, self._toneQueue[0][1]))
                else:
                    self._toneQueue.pop(0)
                    while (self._toneQueue and self._toneQueue[0][1] == None):
                        self._toneQueue.pop(0)
                    continue
            else:
                return data.append(b'\0' * maxlen)
                
            self._currentByte += chunk
            maxlen -= chunk

        return data

    def getWaveData(self, size, tone):
        freq, noise, amplitude = tone
        bps = self._bytesPerSample
        
        if (freq == 0):
            return QByteArray(int(amplitude * SOUND_LEVEL).to_bytes(bps, 'little', signed=True) * (size // bps)) 
        
        waveData = QByteArray()
        phase = self._phase
        channelCount = self._channelCount
        size //= bps * channelCount
        mul = math.pi * freq * 2 / self._sampleRate

        if (not noise):
            for i in range(size):
                waveData.append(int(max(-1, min(1, math.sin(mul * i + phase) * amplitude)) * SOUND_LEVEL)
                    .to_bytes(bps, 'little', signed=True) * channelCount)
        else:
            prevSample = rand = 1
            for i in range(size):
                newSample = int(max(-1, min(1, math.sin(mul * i + phase) * amplitude)) * SOUND_LEVEL)
                if (newSample * prevSample < 0):
                    rand = random.choice([-1, 1])
                    prevSample = newSample
                waveData.append((newSample * rand)
                    .to_bytes(bps, 'little', signed=True) * channelCount)

        self._phase += size * mul
        return waveData
   
    def bytesAvailable(self):
        return SAMPLES_PART_SIZE * self._channelCount * self._bytesPerSample
        
    def start(self, freq, noise, amplitude, goalTime):
        if (len(self._toneQueue) == 0):
            self._currentByte = round(self._sampleRate * goalTime) * self._sampleSize
        goalSample = (SAMPLES_PART_SIZE + round(self._sampleRate * goalTime)) * self._sampleSize
        self._toneQueue.append((goalSample, (freq, noise, amplitude)))

    def startFor(self, freq, noise, duration, amplitude, goalTime):
        if (len(self._toneQueue) == 0):
            self._currentByte = round(self._sampleRate * goalTime) * self._sampleSize
        goalSample = (SAMPLES_PART_SIZE + round(self._sampleRate * goalTime)) * self._sampleSize
        self._toneQueue.append((goalSample, (freq, noise, amplitude)))
        goalTime += duration
        goalSample = (SAMPLES_PART_SIZE + round(self._sampleRate * goalTime)) * self._sampleSize
        self._toneQueue.append((goalSample, None))
        
    def stop(self, goalTime):
        if (len(self._toneQueue) > 0):
            goalSample = (SAMPLES_PART_SIZE + round(self._sampleRate * goalTime)) * self._sampleSize
            self._toneQueue.append((goalSample, None))

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
        
    def play(self, freq, noise, amplitude, goalTime):
        self._audioData.start(freq, noise, amplitude, goalTime)

    def playFor(self, freq, noise, duration, amplitude, goalTime):
        self._audioData.startFor(freq, noise, duration, amplitude, goalTime)
        
    def stop(self, goalTime):
        self._audioData.stop(goalTime)
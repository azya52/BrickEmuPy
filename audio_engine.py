import random, math

from PyQt6.QtCore import QIODeviceBase, QByteArray, QIODevice
from PyQt6.QtMultimedia import QAudioFormat, QAudioSink, QMediaDevices

BUFFER_SIZE = 4096
SOUND_LEVEL = (int) (32767 * 0.1)
SAMPLE_RATE = 44100

class Channel:
    def __init__(self, sample_rate):
        self._tone_queue = []
        self._current_sample = 0
        self._phase = 0
        self._sample_rate = sample_rate
    
    def get_channel_data(self, size):
        data = []
        current_sample = self._current_sample
        remaining = size
        
        while remaining:
            if self._tone_queue:
                if current_sample < self._tone_queue[0][0]:
                    self._phase = 0
                    chunk = min(remaining, self._tone_queue[0][0] - current_sample)
                    data.extend([0.0] * chunk)
                elif len(self._tone_queue) == 1:
                    chunk = remaining
                    data.extend(self._get_wave_data(chunk, self._tone_queue[0][1]))
                elif current_sample < self._tone_queue[1][0]:
                    chunk = min(remaining, self._tone_queue[1][0] - current_sample)
                    data.extend(self._get_wave_data(chunk, self._tone_queue[0][1]))
                else:
                    self._tone_queue.pop(0)
                    while self._tone_queue and self._tone_queue[0][1] == None:
                        self._tone_queue.pop(0)
                    continue
            else:
                data.extend([0.0] * remaining)
                break
            
            current_sample += chunk
            remaining -= chunk
        
        self._current_sample = current_sample
        return data
    
    def _get_wave_data(self, size, tone):
        freq, noise, amplitude = tone

        if (freq == 0):
            return [amplitude] * size
        
        wave_data = [0] * size
        phase = self._phase
        mul = math.pi * freq * 2 / self._sample_rate

        if (not noise):
            for i in range(size):
                wave_data[i] = math.sin(phase) * amplitude
                phase += mul
        else:
            prev_sample = rand = 1
            for i in range(size):
                new_sample = math.sin(phase) * amplitude
                phase += mul
                if (new_sample * prev_sample < 0):
                    rand = random.choice([-1, 1])
                    prev_sample = new_sample
                wave_data[i] = new_sample * rand

        self._phase = phase % (2 * math.pi)
        return wave_data
    
    def start(self, freq, noise, amplitude, goalTime, sampleRate):
        if len(self._tone_queue) == 0:
            self._current_sample = round(sampleRate * goalTime)
        goalSample = BUFFER_SIZE + round(sampleRate * goalTime)
        self._tone_queue.append((goalSample, (freq, noise, amplitude)))
    
    def stop(self, goalTime, sampleRate):
        if len(self._tone_queue) > 0 and self._tone_queue[-1][1] != None:
            goalSample = BUFFER_SIZE + round(sampleRate * goalTime)
            self._tone_queue.append((goalSample, None))
    
    def reset(self):
        self._tone_queue = []
        self._current_sample = 0
        self._phase = 0


class AudioData(QIODevice):
    def __init__(self, sampleRate, bytesPerSample, channelCount):
        super().__init__()
        self._channels = {}
        self._sampleRate = sampleRate
        self._bytesPerSample = bytesPerSample
        self._channelCount = channelCount
        self.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Unbuffered)
        
    def readData(self, maxlen):
        bps = self._bytesPerSample
        channelCount = self._channelCount
        size = maxlen // (bps * channelCount)
        
        channel_data = []
        for ch in self._channels.values():
            channel_data.append(ch.get_channel_data(size))
        
        data = QByteArray()
        for i in range(size):
            mixed = 0
            for ch in channel_data:
                mixed += ch[i]
            mixed = max(-SOUND_LEVEL, min(SOUND_LEVEL, int(mixed)))
            data.append(mixed.to_bytes(bps, 'little', signed=True) * channelCount)
        
        return data

    def bytesAvailable(self):
        return BUFFER_SIZE
        
    def start(self, channel, freq, noise, amplitude, goalTime, duration):
        if channel not in self._channels:
            self._channels[channel] = Channel(self._sampleRate)

        self._channels[channel].start(freq, noise, amplitude * SOUND_LEVEL, goalTime, self._sampleRate)
        if duration > 0:
            stopTime = goalTime + duration
            self._channels[channel].stop(stopTime, self._sampleRate)

    def stop(self, channel, goalTime):
        if channel in self._channels:
            self._channels[channel].stop(goalTime, self._sampleRate)

    def reset(self):
        self._channels = {}


class AudioEngine:
    def __init__(self):
        device = QMediaDevices.defaultAudioOutput()
        audioFormat = device.preferredFormat()
        audioFormat.setSampleRate(SAMPLE_RATE)
        audioFormat.setSampleFormat(QAudioFormat.SampleFormat.Int16)

        self._audioSink = QAudioSink(audioFormat)
        self._audioSink.setBufferSize(BUFFER_SIZE)

        self._audioData = AudioData(audioFormat.sampleRate(), audioFormat.bytesPerSample(), audioFormat.channelCount())
        self._audioSink.start(self._audioData)
    
    def play(self, channel, freq, noise, amplitude, goalTime, duration):
        self._audioData.start(channel, freq, noise, amplitude, goalTime, duration)
    
    def stop(self, channel, goalTime):
        self._audioData.stop(channel, goalTime)
    
    def reset(self):
        self._audioData.reset()


audioEngine = None

def getAudioEngine():
    global audioEngine
    if audioEngine is None:
        audioEngine = AudioEngine()
    return audioEngine
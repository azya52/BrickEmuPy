import time
import random

from PyQt6.QtCore import QIODeviceBase, QByteArray, QIODevice
from PyQt6.QtMultimedia import QAudioFormat, QAudioSink

SOUND_LEVEL = (int) (32767 * 0.1)

SINGLE_SIZE_CHANNEL_SIZE = 32
SINGLE_SIZE_CHANNEL_COUNT = 12
SROM_SIZE = SINGLE_SIZE_CHANNEL_SIZE * 20

LFSR2DIV = (
    0, 2, 123, 3, 124, 75, 117, 4, 125, 101, 111, 76, 118, 42, 69, 5, 126, 66, 63, 102, 112, 86, 36, 77, 119,
    21, 95, 43, 70, 25, 105, 6, 127, 115, 99, 67, 64, 34, 19, 103, 113, 17, 15, 87, 37, 55, 89, 78, 120, 39,
    60, 22, 96, 52, 57, 44, 71, 91, 30, 26, 106, 47, 80, 7, 1, 122, 74, 116, 100, 110, 41, 68, 65, 62, 85, 35,
    20, 94, 24, 104, 114, 98, 33, 18, 16, 14, 54, 88, 38, 59, 51, 56, 90, 29, 46, 79, 121, 73, 109, 40, 61, 84,
    93, 23, 97, 32, 13, 53, 58, 50, 28, 45, 72, 108, 83, 92, 31, 12, 49, 27, 107, 82, 11, 48, 81, 10, 9, 8
)

class WaveGenerator(QIODevice):
    SAMPLES_PART_SIZE = 1000
    DATA_PART_SIZE = SAMPLES_PART_SIZE * 2

    def __init__(self, format):
        super().__init__()

        self.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Unbuffered)
        self._pos = 0
        self._toneStarts = []
        self._toneEnds = []
        self._bytesPerSample = format.bytesPerSample()
        self._sampleRate = format.sampleRate()
        self._initTime = time.perf_counter()
        self._phase = 0

    def readData(self, maxlen):
        data = QByteArray()

        while maxlen:
            chunk = maxlen
            if (len(self._toneStarts) > 0):
                if (self._pos < self._toneStarts[0][0]):
                    chunk = min(maxlen, self._toneStarts[0][0] - self._pos)
                    data.append(chunk, b'\0')
                elif (len(self._toneEnds) == 0):
                    data.append(self.getSquareWaveData(chunk, self._toneStarts[0][1], self._toneStarts[0][2]))
                elif (self._pos < self._toneEnds[0]):
                    chunk = min(maxlen, self._toneEnds[0] - self._pos)
                    data.append(self.getSquareWaveData(chunk, self._toneStarts[0][1], self._toneStarts[0][2]))
                else:
                    self._toneStarts.pop(0)
                    self._toneEnds.pop(0)
                    continue
            else:
                data.append(chunk, b'\0')

            self._pos += chunk
            maxlen -= chunk

        return data
    
    def getSquareWaveData(self, size, freq, noise):
        phase = self._phase
        mul = freq / self._sampleRate
        squareWaveData = QByteArray()
        prevSample = 0
        sample = 0
        for i in range(size // 2):
            newSample = SOUND_LEVEL if (((i * mul + phase) % 1) > 0.5) else -SOUND_LEVEL
            if (newSample != prevSample):
                prevSample = newSample
                sample = -newSample if (noise and (random.random() > 0.5)) else newSample
            squareWaveData.append((sample & 0xFFFF).to_bytes(2))
        self._phase += (size // 2) * mul
        return squareWaveData
        
    def start(self, freq, noise):
        goalTime = time.perf_counter() - self._initTime
        goalSample = self.DATA_PART_SIZE + int(self._sampleRate * goalTime) * self._bytesPerSample
        if (len(self._toneStarts) > len(self._toneEnds)):
            self._toneEnds.append(goalSample)
        if (freq > 0):
            self._toneStarts.append([goalSample, freq, noise])
        
    def stop(self):
        if (len(self._toneStarts) > len(self._toneEnds)):
            goalTime = time.perf_counter() - self._initTime
            goalSample = self.DATA_PART_SIZE + int(self._sampleRate * goalTime) * self._bytesPerSample
            self._toneEnds.append(goalSample)
    
    def bytesAvailable(self):
        return self.DATA_PART_SIZE
    
    
class Sound():
    def __init__(self, mask, clock):
        self._system_clock = clock
        self._clock_counter = 0
        self._note_counter = 0
        self._channel = 0
        self._repeat_cycle = False
        self._sound_on = False
        self._freq_div = mask["sound_freq_div"]
        self._speed_div = mask["sound_speed_div"]
        self._channel_effect = mask["sound_effect"]

        self._sROM = bytearray()
        if (mask["sound_rom_path"] != None):
            try:
                with open(mask["sound_rom_path"], "rb") as bin_f:
                    self._sROM = bytearray(bin_f.read())
            except FileNotFoundError as e:
                print(e.strerror, e.filename)
        self._sROM += bytearray([0] * (SROM_SIZE - len(self._sROM)))
        self._sROM = self._sROM[:SROM_SIZE]

        format = QAudioFormat()
        format.setSampleRate(44100)
        format.setChannelCount(1)
        format.setSampleFormat(QAudioFormat.SampleFormat.Int16)

        self._tone = QAudioSink(format)
        self._tone.setBufferSize(2048)
        self._toneGenerator = WaveGenerator(format)
        self._tone.start(self._toneGenerator)

    def clock(self):
        self._clock_counter -= 1
        if (self._sound_on and self._clock_counter <= 0):
            self._clock_counter = LFSR2DIV[self._speed_div[self._channel]] * self._freq_div * 4
            chanel_size = SINGLE_SIZE_CHANNEL_SIZE * ((self._channel >= SINGLE_SIZE_CHANNEL_COUNT) + 1)
            self._toneGenerator.start(self._get_freq(), self._channel_effect[self._channel])
            self._note_counter = (self._note_counter + 1) % chanel_size
            if ((self._note_counter == 0) and (not self._repeat_cycle)):
                self._sound_on = False
                self._toneGenerator.stop()

    def _get_freq(self):
        chanel_offset = self._channel * SINGLE_SIZE_CHANNEL_SIZE
        if (self._channel > SINGLE_SIZE_CHANNEL_COUNT):
            chanel_offset += (self._channel - SINGLE_SIZE_CHANNEL_COUNT) * SINGLE_SIZE_CHANNEL_SIZE
        note = self._sROM[chanel_offset + self._note_counter]
        
        if (note == 0):
            return 0
        
        return self._system_clock / self._freq_div / LFSR2DIV[note] * 2

    def stop(self):
        self._tone.stop()
        self._toneGenerator.close()

    def set_sound_off(self):
        self._sound_on = False
        self._toneGenerator.stop()

    def set_sound_channel(self, channel):
        self._sound_on = True
        self._note_counter = 0
        self._channel = channel

    def set_one_cycle(self):
        self._repeat_cycle = False

    def set_repeat_cycle(self):
        self._repeat_cycle = True

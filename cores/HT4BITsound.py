from .ToneGenerator import ToneGenerator

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
    
class HT4BITsound():
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
        self._cycle_counter = 0

        self._sROM = bytearray()
        if (mask["sound_rom_path"] != None):
            try:
                with open(mask["sound_rom_path"], "rb") as bin_f:
                    self._sROM = bytearray(bin_f.read())
            except FileNotFoundError as e:
                raise FileNotFoundError(e.errno, "Sound ROM file not found, please add the required sound ROM to this path", e.filename)
        self._sROM += bytearray([0] * (SROM_SIZE - len(self._sROM)))
        self._sROM = self._sROM[:SROM_SIZE]

        self._toneGenerator = ToneGenerator()

    def clock(self, exec_cycles):
        self._cycle_counter += exec_cycles
        if (self._sound_on):
            self._clock_counter -= exec_cycles
            if (self._clock_counter <= 0):
                self._clock_counter += LFSR2DIV[self._speed_div[self._channel]] * self._freq_div * 16
                chanel_size = SINGLE_SIZE_CHANNEL_SIZE * ((self._channel >= SINGLE_SIZE_CHANNEL_COUNT) + 1)
                self._toneGenerator.play(self._get_freq(), self._channel_effect[self._channel], 0.5, self._cycle_counter / self._system_clock)
                self._note_counter = (self._note_counter + 1) % chanel_size
                if ((self._note_counter == 0) and (not self._repeat_cycle)):
                    self._sound_on = False
                    self._toneGenerator.stop(self._cycle_counter / self._system_clock)

    def _get_freq(self):
        chanel_offset = self._channel * SINGLE_SIZE_CHANNEL_SIZE
        if (self._channel > SINGLE_SIZE_CHANNEL_COUNT):
            chanel_offset += (self._channel - SINGLE_SIZE_CHANNEL_COUNT) * SINGLE_SIZE_CHANNEL_SIZE
        note = self._sROM[chanel_offset + self._note_counter]
        
        if (note == 0):
            return 0
        
        return self._system_clock / self._freq_div / LFSR2DIV[note] * 2

    def stop(self):
        self._toneGenerator.close()
        del self._toneGenerator

    def set_sound_off(self):
        self._sound_on = False
        self._toneGenerator.stop(self._cycle_counter / self._system_clock)

    def set_sound_channel(self, channel):
        self._sound_on = True
        self._note_counter = 0
        self._channel = channel

    def set_one_cycle(self):
        self._repeat_cycle = False

    def set_repeat_cycle(self):
        self._repeat_cycle = True
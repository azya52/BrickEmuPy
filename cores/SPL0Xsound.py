from .ToneGenerator import ToneGenerator

IO_SPEECH_CTRL_ENBL = 0x01

SUB_CLOCK = 32768
   
class SPL0Xsound():
    def __init__(self, clock, sub_clock_div):
        self._freq_factor = clock / sub_clock_div / SUB_CLOCK
        self._clock = clock
        self._toneA_generator = ToneGenerator()
        self._toneB_generator = ToneGenerator()
        self._noise_generator = ToneGenerator()
        self._speech_generator = ToneGenerator()

    def set_toneA(self, ctrl1, ctrl2, cycle_counter):
        vol = (ctrl2 >> 6) / 3
        freq32 = (((ctrl2 & 0x3) << 8) | ctrl1) << 1
        if (vol > 0 and freq32 > 0):
            freq = self._freq_factor * freq32
            self._toneA_generator.play(freq, False, vol, cycle_counter / self._clock)
        else:
            self._toneA_generator.stop(cycle_counter / self._clock)

    def set_toneB(self, ctrl1, ctrl2, cycle_counter):
        vol = (ctrl2 >> 6) / 3
        freq32 = (((ctrl2 & 0x3) << 8) | ctrl1) << 1
        if (vol > 0 and freq32 > 0):
            freq = self._freq_factor * freq32
            self._toneB_generator.play(freq, False, vol, cycle_counter / self._clock)
        else:
            self._toneB_generator.stop(cycle_counter / self._clock)

    def set_noise(self, ctrl1, ctrl2, cycle_counter):
        vol = (ctrl2 >> 4) / 15
        freq32 = (16 - (ctrl1 & 0xF)) << 7
        if (vol > 0 and freq32 > 0):
            freq = self._freq_factor * freq32
            self._noise_generator.play(freq, True, vol, cycle_counter / self._clock)
        else:
            self._noise_generator.stop(cycle_counter / self._clock)

    def set_speech(self, ctrl, data, cycle_counter):
        amplitude = ((data & 0x3F) / 0x3F) * (1 - ((data >> 6) & 0x02))
        if (data == 0 or not(ctrl & IO_SPEECH_CTRL_ENBL)):
            self._speech_generator.stop(cycle_counter / self._clock)
        else:
            self._speech_generator.play(0, False, amplitude, cycle_counter / self._clock)
from .ToneGenerator import ToneGenerator

IO_AUDIO_CTRL_ENBL = 0x80
IO_AUDIO_CTRL_TONE = 0x40

SUB_CLOCK = 32768
   
class SPL81408sound():
    def __init__(self, clock):
        self._clock = clock
        self._speech_generator = ToneGenerator()
        self._envelope = 0
        self._toggle_state = 1

    def set_data(self, ctrl, data, cycle_counter):
        if (ctrl & IO_AUDIO_CTRL_ENBL):
            if (ctrl & IO_AUDIO_CTRL_TONE):
                #to-do
                self._envelope = ((data & 0xFF) / 0xFF)
            else:
                amplitude = ((data & 0xFF) / 128) - 1
                self._speech_generator.play(0, False, amplitude, cycle_counter / self._clock)
        else:
            self._speech_generator.stop(cycle_counter / self._clock)

    def toggle(self, cycle_counter):
        #to-do
        self._toggle_state *= -1
        self._speech_generator.play(0, False, self._toggle_state * self._envelope, cycle_counter / self._clock)
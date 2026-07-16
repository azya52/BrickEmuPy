   
SQUARENESS_FACTOR = 5

class STK55C324sound():
    def __init__(self, clock, interconnect):
        self._interconnect = interconnect
        self._main_clock = clock
        self._enable = [False, False]
        self._clock = [0, 0]
        self._freq = [0, 0]
        self._data = [0, 0]
        self._volume = [0, 0]

    def set_volume(self, channel, volume):
        self._volume[channel] = volume / 0xFF
        self._update_freq(channel)

    def set_clock(self, clock):
        prev_state = self._clock
        self._clock = [clock & 0x7, (clock >> 4) & 0x7]
        if (prev_state[0] != self._clock[0]):
            self._update_freq(0)
        if (prev_state[1] != self._clock[1]):
            self._update_freq(1)

    def set_data(self, channel, data):
        self._data[channel] = data
        self._update_freq(channel)
        
    def set_control(self, control):
        prev_state = self._enable
        self._enable = [(control & 0x1) > 0, (control & 0x4) > 0]
        if (prev_state[0] != self._enable[0]):
            self._update_freq(0)
        if (prev_state[1] != self._enable[1]):
            self._update_freq(1)

    def _update_freq(self, channel):
        if (self._enable[channel] and self._volume[channel] > 0 and self._data[channel] > 0):
            self._freq[channel] = (self._main_clock / (2 << self._clock[channel])) / self._data[channel] / 2
            self._interconnect.emit_audio(channel, (self._freq[channel], False, self._volume[channel] * SQUARENESS_FACTOR, 0))
        elif (not self._enable[channel] and self._volume[channel] > 0):
            self._interconnect.emit_audio(channel, (0, False, self._volume[channel], 0))
        else:
            self._interconnect.emit_audio(channel, None)
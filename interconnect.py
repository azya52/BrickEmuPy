class Interconnect:
    def __init__(self):
        self._port_devices = []
        self._input_devices = []
        self._clock_devices = []
        self._audio_forwarder_devices = []

    def register_port_device(self, dev):
        self._port_devices.append(dev)

    def emit_port(self, sender, port, mask, value):
        for dev in self._port_devices:
            if dev is not sender:
                dev.port_handler(port, mask, value)

    def register_input_device(self, dev):
        self._input_devices.append(dev)

    def emit_input(self, key, pressed):
        for dev in self._input_devices:
            dev.input_handler(key, pressed)

    def register_clock_device(self, dev):
        self._clock_devices.append(dev)

    def emit_clock(self, cycles):
        for dev in self._clock_devices:
            dev.clock(cycles)

    def register_audio_forwarder(self, dev):
        self._audio_forwarder_devices.append(dev)

    def emit_audio(self, channel, data):
        for dev in self._audio_forwarder_devices:
            dev.audio_handler(channel, data)
class Interconnect:
    def __init__(self, emulator):
        self._port_devices = []
        self._input_devices = []
        self._clock_devices = []
        self._serial_rx_devices = []
        self._emulator = emulator

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

    def emit_audio(self, channel, data):
        self._emulator.audio_handler(channel, data)

    def register_serial_rx_device(self, dev):
        self._serial_rx_devices.append(dev)

    def emit_serial_rx(self, data):
        for dev in self._serial_rx_devices:
            dev.serial_rx_handler(data)

    def emit_serial_tx(self, data):
        self._emulator.serial_tx_handler(data)
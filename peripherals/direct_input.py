class DirectInput:
    def __init__(self, config, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_input_device(self)
        self._config = config

    def input_handler(self, key, pressed):
        if (key in self._config):
            if (pressed):
                self._interconnect.emit_port(self, self._config[key]["port"], self._config[key]["mask"], self._config[key]["level"])
            else:
                self._interconnect.emit_port(self, self._config[key]["port"], self._config[key]["mask"], -1)
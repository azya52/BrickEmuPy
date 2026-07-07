class DirectConnection:
    def __init__(self, config, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_port_device(self)
        self._input_port = config["input"]["port"]
        self._input_mask = config["input"]["mask"]
        self._output_port = config["output"]["port"]
        self._output_mask = config["output"]["mask"]

    def port_handler(self, port, mask, value):
        if (port == self._output_port):
            self._interconnect.emit_port(self, self._input_port, self._input_mask, (mask & self._output_mask))
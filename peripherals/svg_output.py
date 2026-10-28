class SVGOutput:
    def __init__(self, config, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_port_device(self)
        self._config_by_port = {}
        for element, cfg in config.items():
            self._config_by_port.setdefault(cfg["port"], []).append((element, cfg["mask"], cfg.get("level", 1)))
        self._port_states = {}

    def port_handler(self, port, mask, value):
        configs = self._config_by_port.get(port)
        if (configs and value > 0):
            previous = self._port_states.get(port)
            if (previous != mask):
                self._port_states[port] = mask
                for element, cfg_mask, cfg_level in configs:
                    self._interconnect.emit_svg_element(element, (mask & cfg_mask > 0) == cfg_level)

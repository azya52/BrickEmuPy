class MatrixInput:
    def __init__(self, config, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_input_device(self)
        self._interconnect.register_port_device(self)
        self._config = config
        self._pressed_keys = []
        self._port_states = {}

    def port_handler(self, port, mask, value):
        if self._port_states.get(port) != mask:
            self._port_states[port] = mask
            self._update_matrix_inputs()

    def input_handler(self, key, pressed):
        if key in self._config:
            if pressed and key not in self._pressed_keys:
                self._pressed_keys.append(key)
            elif not pressed and key in self._pressed_keys:
                self._pressed_keys.remove(key)
            
            self._update_matrix_inputs()

    def _update_matrix_inputs(self):
        states = {}
        
        for btn_name in self._pressed_keys:
            cfg = self._config[btn_name]
            key = (cfg["port"], cfg["mask"])
            level_value = (self._port_states.get(cfg["level"]["port"], 0) & cfg["level"]["mask"]) != 0
            states[key] = states.get(key, False) or level_value
        
        for cfg in self._config.values():
            key = (cfg["port"], cfg["mask"])
            self._interconnect.emit_port(self, cfg["port"], cfg["mask"], states.get(key, -1))
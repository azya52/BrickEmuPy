class ROM():
    def __init__(self, romPath):
        self._ROM = bytearray()
        self.set_rom(romPath)

    def get_byte(self, addres):
        return self._ROM[addres % self._rom_size]
    
    def get_word(self, addres):
        return (self._ROM[addres % self._rom_size] << 8) | self._ROM[(addres + 1) % self._rom_size]

    def get_word_LSB(self, addres):
        return self._ROM[addres % self._rom_size] | (self._ROM[(addres + 1) % self._rom_size] << 8)

    def get_bytes(self, addres, count):
        size = self._rom_size
        rom = self._ROM
        result = 0
        for i in range(count):
            result |= rom[(addres + i) % size] << (8 * (count - i - 1))
        return result

    def write_byte(self, addres, value):
        if (addres < self._rom_size):
            self._ROM[addres] = value
    
    def write_word(self, addres, value):
        if (addres < self._rom_size - 1):
            self._ROM[addres] = (value >> 8) & 0xFF
            self._ROM[addres + 1] = value & 0xFF

    def size(self):
        return self._rom_size

    def get_mask(self):
        return (1 << self._rom_size.bit_length()) - 1
   
    def set_rom(self, path):
        if (path != None):
            try:
                with open(path, "rb") as bin_f:
                    self._ROM = bytearray(bin_f.read())
                    self._rom_size = len(self._ROM)
            except FileNotFoundError as e:
                raise FileNotFoundError(e.errno, "ROM file not found, please add the required ROM to this path", e.filename)

    def examine(self):
        return {
        }
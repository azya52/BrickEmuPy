class ROM():
    def __init__(self, romPath):
        self._ROM = bytearray()
        self.setRom(romPath)

    def getByte(self, addres):
        if (addres < self._rom_size):
            return self._ROM[addres]
        else:
            return 0
    
    def getWord(self, addres):
        if (addres < self._rom_size - 1):
            return (self._ROM[addres] << 8) | self._ROM[addres + 1]
        else:
            return 0

    def writeByte(self, addres, value):
        if (addres < self._rom_size):
            self._ROM[addres] = value
    
    def writeWord(self, addres, value):
        if (addres < self._rom_size - 1):
            self._ROM[addres] = (value >> 8) & 0xFF
            self._ROM[addres + 1] = value & 0xFF

    def size(self):
        return self._rom_size
   
    def setRom(self, path):
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
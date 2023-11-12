ROM_SIZE = 1024 * 4

class ROM():
    def __init__(self, romPath):
        self._ROM = bytearray()
        self.setRom(romPath)

    def getByte(self, addres):
        return self._ROM[addres & 0xFFF]
    
    def getWord(self, addres):
        return (self._ROM[addres & 0xFFF] << 8) | self._ROM[(addres + 1) & 0xFFF]

    def writeByte(self, addr, value):
        self._ROM[addr] = value
    
    def writeWord(self, addr, value):
        self._ROM[addr] = (value >> 8) & 0xFF
        self._ROM[addr + 1] = value & 0xFF

    def size(self):
        return len(self._ROM)
   
    def setRom(self, path):
        rom = bytearray()
        if (path != None):
            try:
                with open(path, "rb") as bin_f:
                    rom = bytearray(bin_f.read())
            except FileNotFoundError as e:
                print(e.strerror, e.filename)
        rom += bytearray([0] * (ROM_SIZE - len(rom)))
        self._ROM = rom[:ROM_SIZE]

    def examine(self):
        return {
        }
from .KS57dasm import KS57dasm

class KS57C21308dasm(KS57dasm):

    def __init__(self):
        super().__init__()

        self._clr_fmem_tbl = {
            0b10110010: "di",
            0b10011000: "di IEBT",
            0b10011010: "di IEW",
            0b10011011: "di IETPG",
            0b10011100: "di IET0",
            0b10011101: "di IEP0",
            0b10011110: "di IE0",
            0b10011111: "di IE2",
            0b10111000: "di IE4",
            0b10111011: "di IEKS",
            0b10111110: "di IE1"
        }

        self._set_fmem_tbl = {
            0b10110010: "ei",
            0b10100011: "idle",
            0b10110011: "stop",
            0b10011000: "ei IEBT",
            0b10011010: "ei IEW",
            0b10011011: "ei IETPG",
            0b10011100: "ei IET0",
            0b10011101: "ei IEP0",
            0b10011110: "ei IE0",
            0b10011111: "ei IE2",
            0b10111000: "ei IE4",
            0b10111011: "ei IEKS",
            0b10111110: "ei IE1"
        }

    def disassemble(self, rom):
        if (rom.size() > 0):
            listing = [None] * rom.size()
            vector = rom.getWord(0) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(2) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(4) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(6) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(8) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(10) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)

            listing = self._disassemble_pcea(listing, rom)

            for i in range(len(listing)):
                if (listing[i] is None):
                    byte = rom.getByte(i)
                    listing[i] = (1, byte, 'db ' + self._bytebase % byte)
                listing[i] = (self._opbase % listing[i][1], listing[i][2])
            
            return {"LISTING": tuple(listing)}
        else:
            return {}
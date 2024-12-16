from .HT4BITdasm import HT4BITdasm

class HTG12N0dasm(HT4BITdasm):

    def __init__(self):
        super().__init__()

        self._instructions = self._instructions_override({
            0b00110100: HTG12N0dasm._out_pc_a,
            0b00110101: HTG12N0dasm._out_pb_a
        })

    def _out_pc_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "out PC, A")

    def _out_pb_a(self, pc, opcode):
        npc = (pc + 1) & 0xFFF
        return (npc, 0x3000 | npc, 0x2000 | npc, 0x1000 | npc), (1, opcode >> 8, "out PB, A")
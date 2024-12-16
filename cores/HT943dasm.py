from .HT4BITdasm import HT4BITdasm

class HT943dasm(HT4BITdasm):

    def __init__(self):
        super().__init__()

        self._instructions = self._instructions_override({
            0b00110100: HT943dasm._in_a_pp
        })

    def _in_a_pp(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "in A, PP")
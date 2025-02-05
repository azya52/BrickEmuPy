IND_X = "($%0.2X, X)"
IND = "(%0.4X)"
ZP = "$%0.2X"
ZP_X = "$%0.2X, X"
IMM = "#$%0.2X"
BIT_A = "%0.1d, A"
BIT_ZP = "%0.1d, $%0.2X"
ABS = "$%0.4X"
ABS_X = "$%0.4X, X"
ADDR = "%0.4X"

ADDRESS_SPACE_SIZE = 0x10000

class SPLB20dasm():
    def __init__(self):
        self._instructions = (
            (SPLB20dasm._brk, 1),
            *([(SPLB20dasm._dummy, 1)] * 4),
            (SPLB20dasm._ora_zp, 2),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._php, 1),
            (SPLB20dasm._ora_imm, 2),
            *([(SPLB20dasm._dummy, 1)] * 6),
            (SPLB20dasm._bpl, 2),
            *([(SPLB20dasm._dummy, 1)] * 7),
            (SPLB20dasm._clc, 1),
            *([(SPLB20dasm._dummy, 1)] * 7),
            (SPLB20dasm._jsr_abs, 3),
            *([(SPLB20dasm._dummy, 1)] * 3),
            (SPLB20dasm._bit_zp, 2),
            (SPLB20dasm._and_zp, 2),
            (SPLB20dasm._rol_zp, 2),
            (SPLB20dasm._dummy, 1),
            (SPLB20dasm._plp, 1),
            (SPLB20dasm._and_imm, 2),
            (SPLB20dasm._rol_a, 1),
            (SPLB20dasm._dummy, 1),
            (SPLB20dasm._bit_abs, 3),
            *([(SPLB20dasm._dummy, 1)] * 3),
            (SPLB20dasm._bmi, 2),
            *([(SPLB20dasm._dummy, 1)] * 7),
            (SPLB20dasm._sec, 1),
            *([(SPLB20dasm._dummy, 1)] * 7),
            (SPLB20dasm._rti, 1),
            *([(SPLB20dasm._dummy, 1)] * 4),
            (SPLB20dasm._eor_zp, 2),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._pha, 1),
            (SPLB20dasm._eor_imm, 2),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._jmp_abs, 3),
            *([(SPLB20dasm._dummy, 1)] * 3),
            (SPLB20dasm._bvc, 2),
            *([(SPLB20dasm._dummy, 1)] * 4),
            (SPLB20dasm._eor_zp_x, 2),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._cli, 1),
            *([(SPLB20dasm._dummy, 1)] * 7),
            (SPLB20dasm._rts, 1),
            *([(SPLB20dasm._dummy, 1)] * 4),
            (SPLB20dasm._adc_zp, 2),
            (SPLB20dasm._ror_zp, 2),
            (SPLB20dasm._dummy, 1),
            (SPLB20dasm._pla, 1),
            (SPLB20dasm._adc_imm, 2),
            (SPLB20dasm._ror_a, 1),
            (SPLB20dasm._dummy, 1),
            (SPLB20dasm._jmp_ind, 3),
            *([(SPLB20dasm._dummy, 1)] * 3),
            (SPLB20dasm._bvs, 2),
            *([(SPLB20dasm._dummy, 1)] * 7),
            (SPLB20dasm._sei, 1),
            *([(SPLB20dasm._dummy, 1)] * 8),
            (SPLB20dasm._sta_ind_x, 2),
            *([(SPLB20dasm._dummy, 1)] * 3),
            (SPLB20dasm._sta_zp, 2),
            (SPLB20dasm._stx_zp, 2),
            *([(SPLB20dasm._dummy, 1)] * 3),
            (SPLB20dasm._txa, 1),
            *([(SPLB20dasm._dummy, 1)] * 3),
            (SPLB20dasm._stx_abs, 3),
            (SPLB20dasm._dummy, 1),
            (SPLB20dasm._bcc, 2),
            *([(SPLB20dasm._dummy, 1)] * 4),
            (SPLB20dasm._sta_zp_x, 2),
            *([(SPLB20dasm._dummy, 1)] * 4),
            (SPLB20dasm._txs, 1),
            *([(SPLB20dasm._dummy, 1)] * 6),
            (SPLB20dasm._lda_ind_x, 2),
            (SPLB20dasm._ldx_imm, 2),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._lda_zp, 2),
            (SPLB20dasm._ldx_zp, 2),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._lda_imm, 2),
            (SPLB20dasm._tax, 1),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._lda_abs, 3),
            (SPLB20dasm._ldx_abs, 3),
            (SPLB20dasm._dummy, 1),
            (SPLB20dasm._bcs, 2),
            *([(SPLB20dasm._dummy, 1)] * 4),
            (SPLB20dasm._lda_zp_x, 2),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._clv, 1),
            (SPLB20dasm._dummy, 1),
            (SPLB20dasm._tsx, 1),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._lda_abs_x, 3),
            *([(SPLB20dasm._dummy, 1)] * 7),
            (SPLB20dasm._cmp_zp, 2),
            (SPLB20dasm._dec_zp, 2),
            *([(SPLB20dasm._dummy, 1)] * 2),
            (SPLB20dasm._cmp_imm, 2),
            (SPLB20dasm._dex, 1),
            *([(SPLB20dasm._dummy, 1)] * 5),
            (SPLB20dasm._bne, 2),
            *([(SPLB20dasm._dummy, 1)] * 4),
            (SPLB20dasm._cmp_zp_x, 2),
            (SPLB20dasm._dec_zp_x, 2),
            *([(SPLB20dasm._dummy, 1)] * 9),
            (SPLB20dasm._cpx_imm, 2),
            *([(SPLB20dasm._dummy, 1)] * 3),
            (SPLB20dasm._cpx_zp, 2),
            (SPLB20dasm._sbc_zp, 2),
            (SPLB20dasm._inc_zp, 2),
            (SPLB20dasm._dummy, 1),
            (SPLB20dasm._inx, 1),
            (SPLB20dasm._sbc_imm, 2),
            (SPLB20dasm._nop, 1),
            *([(SPLB20dasm._dummy, 1)] * 5),
            (SPLB20dasm._beq, 2),
            *([(SPLB20dasm._dummy, 1)] * 7),
            (SPLB20dasm._sed, 1),
            *([(SPLB20dasm._dummy, 1)] * 7)
        )

    def disassemble(self, rom):
        if (rom.size() > 0 and rom.size() <= ADDRESS_SPACE_SIZE):
            self._rom_offset = ADDRESS_SPACE_SIZE - rom.size()
            listing = [None] * rom.size()
            for i in range(7):
                vector = rom.size() - 2 - i * 2
                if (vector > 0):
                    addr = (rom.getByte(vector) | (rom.getByte(vector + 1) << 8)) - self._rom_offset
                    if (addr != 0xFFFF):
                        listing = self._disassemble(addr, listing, rom)
            result = [()] * ADDRESS_SPACE_SIZE
            for i in range(len(listing)):
                if (listing[i] is None):
                    byte = rom.getByte(i)
                    listing[i] = (1, byte, 'db 0x%0.2X' % byte)
                result[i + self._rom_offset] = ("%0.2X" % listing[i][1], listing[i][2])
            return {"LISTING": tuple(result)}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        listing = self.disassemble(rom)["LISTING"]
        with open(file_path, 'w') as f:
            for i, line in enumerate(listing):
                if (line):
                    f.write(("%0.4X" % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(30) + "\n")
    
    def _disassemble(self, pc, listing, rom):
        while (pc >= 0 and pc < len(listing) and listing[pc] is None):
            opcode = rom.getByte(pc)
            instruction = self._instructions[opcode]
            instruction_size = instruction[1]
            if (instruction_size > 1):
                opcode = rom.getBytes(pc, instruction_size)
            next_pc, symbol = instruction[0](self, pc, opcode)
            listing[pc] = (instruction_size, opcode, symbol)
            while ((instruction_size > 1)  and ((pc + 1) < len(listing))):
                instruction_size -= 1
                pc += 1
                listing[pc] = (1, rom.getByte(pc), '')
            pc = next_pc[0]
            if (len(next_pc) > 1):
                listing = self._disassemble(next_pc[1], listing, rom)
        return listing

    def _brk(self, pc, opcode):
        return (pc + 1,), "brk"

    def _ora_zp(self, pc, opcode):
        return (pc + 2,), "ora " + ZP % (opcode & 0xFF)

    def _php(self, pc, opcode):
        return (pc + 1,), "php"

    def _ora_imm(self, pc, opcode):
        return (pc + 2,), "ora " + IMM % (opcode & 0xFF)

    def _bpl(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bpl " + ADDR % (self._rom_offset + addr)

    def _clc(self, pc, opcode):
        return (pc + 1,), "clc"

    def _jsr_abs(self, pc, opcode):
        addr = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3, addr - self._rom_offset), "jsr " + ADDR % addr

    def _bit_zp(self, pc, opcode):
        return (pc + 2,), "bit " + ZP % (opcode & 0xFF)

    def _and_zp(self, pc, opcode):
        return (pc + 2,), "and " + ZP % (opcode & 0xFF)

    def _rol_zp(self, pc, opcode):
        return (pc + 2,), "rol " + ZP % (opcode & 0xFF)

    def _plp(self, pc, opcode):
        return (pc + 1,), "plp"

    def _and_imm(self, pc, opcode):
        return (pc + 2,), "and " + IMM % (opcode & 0xFF)

    def _rol_a(self, pc, opcode):
        return (pc + 1,), "rol A"

    def _bit_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "bit " + ABS % abs

    def _bmi(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bmi " + ADDR % (self._rom_offset + addr)

    def _sec(self, pc, opcode):
        return (pc + 1,), "sec"

    def _rti(self, pc, opcode):
        return (pc,), "rti"

    def _eor_zp(self, pc, opcode):
        return (pc + 2,), "eor " + ZP % (opcode & 0xFF)

    def _pha(self, pc, opcode):
        return (pc + 1,), "pha"

    def _eor_imm(self, pc, opcode):
        return (pc + 2,), "eor " + IMM % (opcode & 0xFF)

    def _jmp_abs(self, pc, opcode):
        addr = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (addr - self._rom_offset,), "jmp " + ADDR % addr

    def _bvc(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bvc " + ADDR % (self._rom_offset + addr)

    def _eor_zp_x(self, pc, opcode):
        return (pc + 2,), "eor " + ZP_X % (opcode & 0xFF)

    def _cli(self, pc, opcode):
        return (pc + 1,), "cli"

    def _rts(self, pc, opcode):
        return (pc,), "rts"

    def _adc_zp(self, pc, opcode):
        return (pc + 2,), "adc " + ZP % (opcode & 0xFF)

    def _ror_zp(self, pc, opcode):
        return (pc + 2,), "ror " + ZP % (opcode & 0xFF)

    def _pla(self, pc, opcode):
        return (pc + 1,), "pla"

    def _adc_imm(self, pc, opcode):
        return (pc + 2,), "adc " + IMM % (opcode & 0xFF)

    def _ror_a(self, pc, opcode):
        return (pc + 1,), "ror A"

    def _jmp_ind(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "jmp " + IND % abs

    def _bvs(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bvs " + ADDR % (self._rom_offset + addr)

    def _sei(self, pc, opcode):
        return (pc + 1,), "sei"

    def _sta_ind_x(self, pc, opcode):
        return (pc + 2,), "sta " + IND_X % (opcode & 0xFF)

    def _sta_zp(self, pc, opcode):
        return (pc + 2,), "sta " + ZP % (opcode & 0xFF)

    def _stx_zp(self, pc, opcode):
        return (pc + 2,), "stx " + ZP % (opcode & 0xFF)

    def _txa(self, pc, opcode):
        return (pc + 1,), "txa"

    def _stx_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "stx " + ABS % abs 

    def _bcc(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bcc " + ADDR % (self._rom_offset + addr)

    def _sta_zp_x(self, pc, opcode):
        return (pc + 2,), "sta " + ZP_X % (opcode & 0xFF)

    def _txs(self, pc, opcode):
        return (pc + 1,), "txs"

    def _lda_ind_x(self, pc, opcode):
        return (pc + 2,), "lda " + IND_X % (opcode & 0xFF)

    def _ldx_imm(self, pc, opcode):
        return (pc + 2,), "ldx " + IMM % (opcode & 0xFF)

    def _lda_zp(self, pc, opcode):
        return (pc + 2,), "lda " + ZP % (opcode & 0xFF)

    def _ldx_zp(self, pc, opcode):
        return (pc + 2,), "ldx " + ZP % (opcode & 0xFF)

    def _lda_imm(self, pc, opcode):
        return (pc + 2,), "lda " + IMM % (opcode & 0xFF)

    def _tax(self, pc, opcode):
        return (pc + 1,), "tax"

    def _lda_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "lda " + ABS % abs 

    def _ldx_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ldx " + ABS % abs 

    def _bcs(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bcs " + ADDR % (self._rom_offset + addr)

    def _lda_zp_x(self, pc, opcode):
        return (pc + 2,), "lda " + ZP_X % (opcode & 0xFF)

    def _clv(self, pc, opcode):
        return (pc + 1,), "clv"

    def _tsx(self, pc, opcode):
        return (pc + 1,), "tsx"

    def _lda_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "lda " + ABS_X % abs

    def _cmp_zp(self, pc, opcode):
        return (pc + 2,), "cmp " + ZP % (opcode & 0xFF)

    def _dec_zp(self, pc, opcode):
        return (pc + 2,), "dec " + ZP % (opcode & 0xFF)

    def _cmp_imm(self, pc, opcode):
        return (pc + 2,), "cmp " + IMM % (opcode & 0xFF)

    def _dex(self, pc, opcode):
        return (pc + 1,), "dex"

    def _bne(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bne " + ADDR % (self._rom_offset + addr)

    def _cmp_zp_x(self, pc, opcode):
        return (pc + 2,), "cmp " + ZP_X % (opcode & 0xFF)

    def _dec_zp_x(self, pc, opcode):
        return (pc + 2,), "dec " + ZP_X % (opcode & 0xFF)

    def _cpx_imm(self, pc, opcode):
        return (pc + 2,), "cpx " + IMM % (opcode & 0xFF)

    def _cpx_zp(self, pc, opcode):
        return (pc + 2,), "cpx " + ZP % (opcode & 0xFF)

    def _sbc_zp(self, pc, opcode):
        return (pc + 2,), "sbc " + ZP % (opcode & 0xFF)

    def _inc_zp(self, pc, opcode):
        return (pc + 2,), "inc " + ZP % (opcode & 0xFF)

    def _inx(self, pc, opcode):
        return (pc + 1,), "inx"

    def _sbc_imm(self, pc, opcode):
        return (pc + 2,), "sbc " + IMM % (opcode & 0xFF)

    def _nop(self, pc, opcode):
        return (pc + 1,), "nop"

    def _beq(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "beq " + ADDR % (self._rom_offset + addr)

    def _sed(self, pc, opcode):
        return (pc + 1,), "sed"

    def _dummy(self, pc, opcode):
        return (pc + 1,), "illegal instruction"
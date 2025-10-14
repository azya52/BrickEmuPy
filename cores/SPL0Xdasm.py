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

ADDRESS_SPACE_SIZE = 0x2000

class SPL0Xdasm():
    def __init__(self):
        self._instructions = (
            (SPL0Xdasm._brk, 1),
            *([(SPL0Xdasm._dummy, 1)] * 4),
            (SPL0Xdasm._ora_zp, 2),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._php, 1),
            (SPL0Xdasm._ora_imm, 2),
            *([(SPL0Xdasm._dummy, 1)] * 6),
            (SPL0Xdasm._bpl, 2),
            *([(SPL0Xdasm._dummy, 1)] * 7),
            (SPL0Xdasm._clc, 1),
            *([(SPL0Xdasm._dummy, 1)] * 7),
            (SPL0Xdasm._jsr_abs, 3),
            *([(SPL0Xdasm._dummy, 1)] * 3),
            (SPL0Xdasm._bit_zp, 2),
            (SPL0Xdasm._and_zp, 2),
            (SPL0Xdasm._rol_zp, 2),
            (SPL0Xdasm._dummy, 1),
            (SPL0Xdasm._plp, 1),
            (SPL0Xdasm._and_imm, 2),
            (SPL0Xdasm._rol_a, 1),
            (SPL0Xdasm._dummy, 1),
            (SPL0Xdasm._bit_abs, 3),
            *([(SPL0Xdasm._dummy, 1)] * 3),
            (SPL0Xdasm._bmi, 2),
            *([(SPL0Xdasm._dummy, 1)] * 7),
            (SPL0Xdasm._sec, 1),
            *([(SPL0Xdasm._dummy, 1)] * 7),
            (SPL0Xdasm._rti, 1),
            *([(SPL0Xdasm._dummy, 1)] * 4),
            (SPL0Xdasm._eor_zp, 2),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._pha, 1),
            (SPL0Xdasm._eor_imm, 2),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._jmp_abs, 3),
            *([(SPL0Xdasm._dummy, 1)] * 3),
            (SPL0Xdasm._bvc, 2),
            *([(SPL0Xdasm._dummy, 1)] * 4),
            (SPL0Xdasm._eor_zp_x, 2),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._cli, 1),
            *([(SPL0Xdasm._dummy, 1)] * 7),
            (SPL0Xdasm._rts, 1),
            *([(SPL0Xdasm._dummy, 1)] * 4),
            (SPL0Xdasm._adc_zp, 2),
            (SPL0Xdasm._ror_zp, 2),
            (SPL0Xdasm._dummy, 1),
            (SPL0Xdasm._pla, 1),
            (SPL0Xdasm._adc_imm, 2),
            (SPL0Xdasm._ror_a, 1),
            (SPL0Xdasm._dummy, 1),
            (SPL0Xdasm._jmp_ind, 3),
            *([(SPL0Xdasm._dummy, 1)] * 3),
            (SPL0Xdasm._bvs, 2),
            *([(SPL0Xdasm._dummy, 1)] * 7),
            (SPL0Xdasm._sei, 1),
            *([(SPL0Xdasm._dummy, 1)] * 8),
            (SPL0Xdasm._sta_ind_x, 2),
            *([(SPL0Xdasm._dummy, 1)] * 3),
            (SPL0Xdasm._sta_zp, 2),
            (SPL0Xdasm._stx_zp, 2),
            *([(SPL0Xdasm._dummy, 1)] * 3),
            (SPL0Xdasm._txa, 1),
            *([(SPL0Xdasm._dummy, 1)] * 3),
            (SPL0Xdasm._stx_abs, 3),
            (SPL0Xdasm._dummy, 1),
            (SPL0Xdasm._bcc, 2),
            *([(SPL0Xdasm._dummy, 1)] * 4),
            (SPL0Xdasm._sta_zp_x, 2),
            *([(SPL0Xdasm._dummy, 1)] * 4),
            (SPL0Xdasm._txs, 1),
            *([(SPL0Xdasm._dummy, 1)] * 6),
            (SPL0Xdasm._lda_ind_x, 2),
            (SPL0Xdasm._ldx_imm, 2),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._lda_zp, 2),
            (SPL0Xdasm._ldx_zp, 2),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._lda_imm, 2),
            (SPL0Xdasm._tax, 1),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._lda_abs, 3),
            (SPL0Xdasm._ldx_abs, 3),
            (SPL0Xdasm._dummy, 1),
            (SPL0Xdasm._bcs, 2),
            *([(SPL0Xdasm._dummy, 1)] * 4),
            (SPL0Xdasm._lda_zp_x, 2),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._clv, 1),
            (SPL0Xdasm._dummy, 1),
            (SPL0Xdasm._tsx, 1),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._lda_abs_x, 3),
            *([(SPL0Xdasm._dummy, 1)] * 7),
            (SPL0Xdasm._cmp_zp, 2),
            (SPL0Xdasm._dec_zp, 2),
            *([(SPL0Xdasm._dummy, 1)] * 2),
            (SPL0Xdasm._cmp_imm, 2),
            (SPL0Xdasm._dex, 1),
            *([(SPL0Xdasm._dummy, 1)] * 5),
            (SPL0Xdasm._bne, 2),
            *([(SPL0Xdasm._dummy, 1)] * 4),
            (SPL0Xdasm._cmp_zp_x, 2),
            (SPL0Xdasm._dec_zp_x, 2),
            *([(SPL0Xdasm._dummy, 1)] * 9),
            (SPL0Xdasm._cpx_imm, 2),
            *([(SPL0Xdasm._dummy, 1)] * 3),
            (SPL0Xdasm._cpx_zp, 2),
            (SPL0Xdasm._sbc_zp, 2),
            (SPL0Xdasm._inc_zp, 2),
            (SPL0Xdasm._dummy, 1),
            (SPL0Xdasm._inx, 1),
            (SPL0Xdasm._sbc_imm, 2),
            (SPL0Xdasm._nop, 1),
            *([(SPL0Xdasm._dummy, 1)] * 5),
            (SPL0Xdasm._beq, 2),
            *([(SPL0Xdasm._dummy, 1)] * 7),
            (SPL0Xdasm._sed, 1),
            *([(SPL0Xdasm._dummy, 1)] * 7)
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            listing = [None] * rom.size()         
            for i in range(3):
                vector = ADDRESS_SPACE_SIZE - 2 - i * 2
                if (vector > 0):
                    addr = (rom.getByte(vector) | (rom.getByte(vector + 1) << 8))
                    if (addr != 0x0000):
                        listing = self._disassemble(addr, listing, rom, 0, 0)
            result = [()] * rom.size()
            for i in range(len(listing)):
                if (listing[i] is None):
                    byte = rom.getByte(i)
                    listing[i] = (1, byte, 'db 0x%0.2X' % byte)
                result[i] = ("%0.2X" % listing[i][1], listing[i][2])
            return {"LISTING": tuple(result)}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        listing = self.disassemble(rom)["LISTING"]
        with open(file_path, 'w') as f:
            for i, line in enumerate(listing):
                if (line):
                    f.write(("%0.4X" % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(30) + "\n")
    
    def _disassemble(self, pc, listing, rom, acc, bank):
        self._acc = acc
        self._bank = bank
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
            if (len(next_pc) > 1):
                if ((opcode & 0xFF0000) == 0x200000):
                    listing = self._disassemble(next_pc[1], listing, rom, acc, bank)
                else:
                    for pc in next_pc:
                        listing = self._disassemble(pc, listing, rom, acc, bank)
                    continue
            pc = next_pc[0]
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
        return (pc + 2, addr), "bpl " + ADDR % (addr)

    def _clc(self, pc, opcode):
        return (pc + 1,), "clc"

    def _jsr_abs(self, pc, opcode):
        addr = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3, addr), "jsr " + ADDR % addr

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
        return (pc + 2, addr), "bmi " + ADDR % (addr)

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
        if (addr >= 0x1000):
            addr += self._bank << 12
        return (addr,), "jmp " + ADDR % addr

    def _bvc(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bvc " + ADDR % (addr)

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
        return (pc + 2, addr), "bvs " + ADDR % (addr)

    def _sei(self, pc, opcode):
        return (pc + 1,), "sei"

    def _sta_ind_x(self, pc, opcode):
        return (pc + 2,), "sta " + IND_X % (opcode & 0xFF)

    def _sta_zp(self, pc, opcode):
        if ((opcode & 0xFF) == 0xD7):
            self._bank = self._acc
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
        return (pc + 2, addr), "bcc " + ADDR % (addr)

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
        self._acc = (opcode & 0xFF)
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
        return (pc + 2, addr), "bcs " + ADDR % (addr)

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
        return (pc + 2, addr), "bne " + ADDR % (addr)

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
        return (pc + 2, addr), "beq " + ADDR % (addr)

    def _sed(self, pc, opcode):
        return (pc + 1,), "sed"

    def _dummy(self, pc, opcode):
        return (pc + 1,), "illegal instruction"
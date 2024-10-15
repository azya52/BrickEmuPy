IND_X = "($%0.2X, X)"
IND_Y = "($%0.2X), Y"
IND = "(%0.4X)"
ZP_IND = "($%0.2X)"
ZP = "$%0.2X"
ZP_X = "$%0.2X, X"
ZP_Y = "$%0.2X, Y"
IMM = "#$%0.2X"
BIT_A = "%0.1d, A"
BIT_ZP = "%0.1d, $%0.2X"
ABS = "$%0.4X"
ABS_X = "$%0.4X, X"
ABS_Y = "$%0.4X, Y"
ADDR = "%0.4X"

ADDRESS_SPACE_SIZE = 0x10000

class M37520dasm():
    def __init__(self):
        self._instructions = (
            (M37520dasm._brk, 1),
            (M37520dasm._ora_ind_x, 2),
            (M37520dasm._jsr_zp_ind, 2),
            (M37520dasm._bbs_bit_a, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._ora_zp, 2),
            (M37520dasm._asl_zp, 2),
            (M37520dasm._bbs_bit_zp, 3),
            (M37520dasm._php, 1),
            (M37520dasm._ora_imm, 2),
            (M37520dasm._asl_a, 1),
            (M37520dasm._seb_bit_a, 1),
            (M37520dasm._dummy, 1),
            (M37520dasm._ora_abs, 3),
            (M37520dasm._asl_abs, 3),
            (M37520dasm._seb_bit_zp, 2),
            (M37520dasm._bpl, 2),
            (M37520dasm._ora_ind_y, 2),
            (M37520dasm._clt, 1),
            (M37520dasm._bbc_bit_a, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._ora_zp_x, 2),
            (M37520dasm._asl_zp_x, 2),
            (M37520dasm._bbc_bit_zp, 3),
            (M37520dasm._clc, 1),
            (M37520dasm._ora_abs_y, 3),
            (M37520dasm._dec_a, 1),
            (M37520dasm._clb_bit_a, 1),
            (M37520dasm._dummy, 1),
            (M37520dasm._ora_abs_x, 3),
            (M37520dasm._asl_abs_x, 3),
            (M37520dasm._clb_bit_zp, 2),
            (M37520dasm._jsr_abs, 3),
            (M37520dasm._and_ind_x, 2),
            (M37520dasm._jsr_sp, 2),
            (M37520dasm._bbs_bit_a, 2),
            (M37520dasm._bit_zp, 2),
            (M37520dasm._and_zp, 2),
            (M37520dasm._rol_zp, 2),
            (M37520dasm._bbs_bit_zp, 3),
            (M37520dasm._plp, 1),
            (M37520dasm._and_imm, 2),
            (M37520dasm._rol_a, 1),
            (M37520dasm._seb_bit_a, 1),
            (M37520dasm._bit_abs, 3),
            (M37520dasm._and_abs, 3),
            (M37520dasm._rol_abs, 3),
            (M37520dasm._seb_bit_zp, 2),
            (M37520dasm._bmi, 2),
            (M37520dasm._and_ind_y, 2),
            (M37520dasm._set, 1),
            (M37520dasm._bbc_bit_a, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._and_zp_x, 2),
            (M37520dasm._rol_zp_x, 2),
            (M37520dasm._bbc_bit_zp, 3),
            (M37520dasm._sec, 1),
            (M37520dasm._and_abs_y, 3),
            (M37520dasm._inc_a, 1),
            (M37520dasm._clb_bit_a, 1),
            (M37520dasm._ldm_zp, 3),
            (M37520dasm._and_abs_x, 3),
            (M37520dasm._rol_abs_x, 3),
            (M37520dasm._clb_bit_zp, 2),
            (M37520dasm._rti, 1),
            (M37520dasm._eor_ind_x, 2),
            (M37520dasm._stp, 1),
            (M37520dasm._bbs_bit_a, 2),
            (M37520dasm._com_zp, 2),
            (M37520dasm._eor_zp, 2),
            (M37520dasm._lsr_zp, 2),
            (M37520dasm._bbs_bit_zp, 3),
            (M37520dasm._pha, 1),
            (M37520dasm._eor_imm, 2),
            (M37520dasm._lsr_a, 1),
            (M37520dasm._seb_bit_a, 1),
            (M37520dasm._jmp_abs, 3),
            (M37520dasm._eor_abs, 3),
            (M37520dasm._lsr_abs, 3),
            (M37520dasm._seb_bit_zp, 2),
            (M37520dasm._bvc, 2),
            (M37520dasm._eor_ind_y, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._bbc_bit_a, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._eor_zp_x, 2),
            (M37520dasm._lsr_zp_x, 2),
            (M37520dasm._bbc_bit_zp, 3),
            (M37520dasm._cli, 1),
            (M37520dasm._eor_abs_y, 3),
            (M37520dasm._dummy, 1),
            (M37520dasm._clb_bit_a, 1),
            (M37520dasm._dummy, 1),
            (M37520dasm._eor_abs_x, 3),
            (M37520dasm._lsr_abs_x, 3),
            (M37520dasm._clb_bit_zp, 2),
            (M37520dasm._rts, 1),
            (M37520dasm._adc_ind_x, 2),
            (M37520dasm._mul_zp_x, 2),
            (M37520dasm._bbs_bit_a, 2),
            (M37520dasm._tst_zp, 2),
            (M37520dasm._adc_zp, 2),
            (M37520dasm._ror_zp, 2),
            (M37520dasm._bbs_bit_zp, 3),
            (M37520dasm._pla, 1),
            (M37520dasm._adc_imm, 2),
            (M37520dasm._ror_a, 1),
            (M37520dasm._seb_bit_a, 1),
            (M37520dasm._jmp_ind, 3),
            (M37520dasm._adc_abs, 3),
            (M37520dasm._ror_abs, 3),
            (M37520dasm._seb_bit_zp, 2),
            (M37520dasm._bvs, 2),
            (M37520dasm._adc_ind_y, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._bbc_bit_a, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._adc_zp_x, 2),
            (M37520dasm._ror_zp_x, 2),
            (M37520dasm._bbc_bit_zp, 3),
            (M37520dasm._sei, 1),
            (M37520dasm._adc_abs_y, 3),
            (M37520dasm._dummy, 1),
            (M37520dasm._clb_bit_a, 1),
            (M37520dasm._dummy, 1),
            (M37520dasm._adc_abs_x, 3),
            (M37520dasm._ror_abs_x, 3),
            (M37520dasm._clb_bit_zp, 2),
            (M37520dasm._bra, 2),
            (M37520dasm._sta_ind_x, 2),
            (M37520dasm._rrf_zp, 2),
            (M37520dasm._bbs_bit_a, 2),
            (M37520dasm._sty_zp, 2),
            (M37520dasm._sta_zp, 2),
            (M37520dasm._stx_zp, 2),
            (M37520dasm._bbs_bit_zp, 3),
            (M37520dasm._dey, 1),
            (M37520dasm._dummy, 1),
            (M37520dasm._txa, 1),
            (M37520dasm._seb_bit_a, 1),
            (M37520dasm._sty_abs, 3),
            (M37520dasm._sta_abs, 3),
            (M37520dasm._stx_abs, 3),
            (M37520dasm._seb_bit_zp, 2),
            (M37520dasm._bcc, 2),
            (M37520dasm._sta_ind_y, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._bbc_bit_a, 2),
            (M37520dasm._sty_zp_x, 2),
            (M37520dasm._sta_zp_x, 2),
            (M37520dasm._stx_zp_y, 2),
            (M37520dasm._bbc_bit_zp, 3),
            (M37520dasm._tya, 1),
            (M37520dasm._sta_abs_y, 3),
            (M37520dasm._txs, 1),
            (M37520dasm._clb_bit_a, 1),
            (M37520dasm._dummy, 1),
            (M37520dasm._sta_abs_x, 3),
            (M37520dasm._dummy, 1),
            (M37520dasm._clb_bit_zp, 2),
            (M37520dasm._ldy_imm, 2),
            (M37520dasm._lda_ind_x, 2),
            (M37520dasm._ldx_imm, 2),
            (M37520dasm._bbs_bit_a, 2),
            (M37520dasm._ldy_zp, 2),
            (M37520dasm._lda_zp, 2),
            (M37520dasm._ldx_zp, 2),
            (M37520dasm._bbs_bit_zp, 3),
            (M37520dasm._tay, 1),
            (M37520dasm._lda_imm, 2),
            (M37520dasm._tax, 1),
            (M37520dasm._seb_bit_a, 1),
            (M37520dasm._ldy_abs, 3),
            (M37520dasm._lda_abs, 3),
            (M37520dasm._ldx_abs, 3),
            (M37520dasm._seb_bit_zp, 2),
            (M37520dasm._bcs, 2),
            (M37520dasm._lda_ind_y, 2),
            (M37520dasm._jmp_zp_ind, 2),
            (M37520dasm._bbc_bit_a, 2),
            (M37520dasm._ldy_zp_x, 2),
            (M37520dasm._lda_zp_x, 2),
            (M37520dasm._ldx_zp_y, 2),
            (M37520dasm._bbc_bit_zp, 3),
            (M37520dasm._clv, 1),
            (M37520dasm._lda_abs_y, 3),
            (M37520dasm._tsx, 1),
            (M37520dasm._clb_bit_a, 1),
            (M37520dasm._ldy_abs_x, 3),
            (M37520dasm._lda_abs_x, 3),
            (M37520dasm._ldx_abs_y, 3),
            (M37520dasm._clb_bit_zp, 2),
            (M37520dasm._cpy_imm, 2),
            (M37520dasm._cmp_ind_x, 2),
            (M37520dasm._wit, 1),
            (M37520dasm._bbs_bit_a, 2),
            (M37520dasm._cpy_zp, 2),
            (M37520dasm._cmp_zp, 2),
            (M37520dasm._dec_zp, 2),
            (M37520dasm._bbs_bit_zp, 3),
            (M37520dasm._iny, 1),
            (M37520dasm._cmp_imm, 2),
            (M37520dasm._dex, 1),
            (M37520dasm._seb_bit_a, 1),
            (M37520dasm._cpy_abs, 3),
            (M37520dasm._cmp_abs, 3),
            (M37520dasm._dec_abs, 3),
            (M37520dasm._seb_bit_zp, 2),
            (M37520dasm._bne, 2),
            (M37520dasm._cmp_ind_y, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._bbc_bit_a, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._cmp_zp_x, 2),
            (M37520dasm._dec_zp_x, 2),
            (M37520dasm._bbc_bit_zp, 3),
            (M37520dasm._cld, 1),
            (M37520dasm._cmp_abs_y, 3),
            (M37520dasm._dummy, 1),
            (M37520dasm._clb_bit_a, 1),
            (M37520dasm._dummy, 1),
            (M37520dasm._cmp_abs_x, 3),
            (M37520dasm._dec_abs_x, 3),
            (M37520dasm._clb_bit_zp, 2),
            (M37520dasm._cpx_imm, 2),
            (M37520dasm._sbc_ind_x, 2),
            (M37520dasm._div_zp_x, 2),
            (M37520dasm._bbs_bit_a, 2),
            (M37520dasm._cpx_zp, 2),
            (M37520dasm._sbc_zp, 2),
            (M37520dasm._inc_zp, 2),
            (M37520dasm._bbs_bit_zp, 3),
            (M37520dasm._inx, 1),
            (M37520dasm._sbc_imm, 2),
            (M37520dasm._nop, 1),
            (M37520dasm._seb_bit_a, 1),
            (M37520dasm._cpx_abs, 3),
            (M37520dasm._sbc_abs, 3),
            (M37520dasm._inc_abs, 3),
            (M37520dasm._seb_bit_zp, 2),
            (M37520dasm._beq, 2),
            (M37520dasm._sbc_ind_y, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._bbc_bit_a, 2),
            (M37520dasm._dummy, 1),
            (M37520dasm._sbc_zp_x, 2),
            (M37520dasm._inc_zp_x, 2),
            (M37520dasm._bbc_bit_zp, 3),
            (M37520dasm._sed, 1),
            (M37520dasm._sbc_abs_y, 3),
            (M37520dasm._dummy, 1),
            (M37520dasm._clb_bit_a, 1),
            (M37520dasm._dummy, 1),
            (M37520dasm._sbc_abs_x, 3),
            (M37520dasm._inc_abs_x, 3),
            (M37520dasm._clb_bit_zp, 2)
        )

    def disassemble(self, rom):
        if (rom.size() > 0 and rom.size() <= ADDRESS_SPACE_SIZE):
            self._rom_offset = ADDRESS_SPACE_SIZE - rom.size()
            listing = [None] * rom.size()
            for i in range(16):
                vector = rom.size() - 2 - i * 2
                if (vector > 0):
                    addr = (rom.getByte(vector) | (rom.getByte(vector + 1) << 8)) - self._rom_offset
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
        while (pc > 0 and pc < len(listing) and listing[pc] is None):
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

    def _ora_ind_x(self, pc, opcode):
        return (pc + 2,), "ora " + IND_X % (opcode & 0xFF) 

    def _jsr_zp_ind(self, pc, opcode):
        return (pc + 2,), "jsr " + ZP_IND % (opcode & 0xFF)

    def _bbs_bit_a(self, pc, opcode):
        bit = (opcode >> 13) & 0x7
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bbs " + BIT_A % bit + ", " + ADDR % (self._rom_offset + addr)

    def _ora_zp(self, pc, opcode):
        return (pc + 2,), "ora " + ZP % (opcode & 0xFF)

    def _asl_zp(self, pc, opcode):
        return (pc + 2,), "asl " + ZP % (opcode & 0xFF)

    def _bbs_bit_zp(self, pc, opcode):
        bit = (opcode >> 21) & 0x7
        zp = (opcode >> 8) & 0xFF
        addr = pc + 3 + (opcode & 0xFF)
        return (pc + 3, addr), "bbs " + BIT_ZP % (bit, zp) + ", " + ADDR % (self._rom_offset + addr)

    def _php(self, pc, opcode):
        return (pc + 1,), "php"

    def _ora_imm(self, pc, opcode):
        return (pc + 2,), "ora " + IMM % (opcode & 0xFF)

    def _asl_a(self, pc, opcode):
        return (pc + 1,), "asl A"

    def _seb_bit_a(self, pc, opcode):
        bit = (opcode >> 5 & 0x7)
        return (pc + 1,), "seb " + BIT_A % bit 

    def _ora_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ora " + ABS % abs

    def _asl_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "asl " + ABS % abs

    def _seb_bit_zp(self, pc, opcode):
        bit = (opcode >> 13) & 0x7
        return (pc + 2,), "seb " + BIT_ZP % (bit, opcode & 0xFF)

    def _bpl(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bpl " + ADDR % (self._rom_offset + addr)

    def _ora_ind_y(self, pc, opcode):
        return (pc + 2,), "ora " + IND_Y % (opcode & 0xFF)

    def _clt(self, pc, opcode):
        return (pc + 1,), "clt"

    def _bbc_bit_a(self, pc, opcode):
        bit = (opcode >> 13) & 0x7
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bbc " + BIT_A % bit + ", " + ADDR % (self._rom_offset + addr)

    def _ora_zp_x(self, pc, opcode):
        return (pc + 2,), "ora " + ZP_X % (opcode & 0xFF)

    def _asl_zp_x(self, pc, opcode):
        return (pc + 2,), "asl " + ZP_X % (opcode & 0xFF)

    def _bbc_bit_zp(self, pc, opcode):
        bit = (opcode >> 21) & 0x7
        zp = (opcode >> 8) & 0xFF
        addr = pc + 3 + (opcode & 0xFF)
        return (pc + 3, addr), "bbc " + BIT_ZP % (bit, zp) + ", " + ADDR % (self._rom_offset + addr)

    def _clc(self, pc, opcode):
        return (pc + 1,), "clc"

    def _ora_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ora " + ABS_Y % abs

    def _dec_a(self, pc, opcode):
        return (pc + 1,), "dec A"

    def _clb_bit_a(self, pc, opcode):
        bit = (opcode >> 5 & 0x7)
        return (pc + 1,), "clb " + BIT_A % bit 

    def _ora_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ora " + ABS_X % abs 

    def _asl_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "asl" + ABS_X % abs

    def _clb_bit_zp(self, pc, opcode):
        bit = (opcode >> 13) & 0x7
        return (pc + 2,), "clb " + BIT_ZP % (bit, opcode & 0xFF)

    def _jsr_abs(self, pc, opcode):
        addr = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3, addr - self._rom_offset), "jsr " + ADDR % addr

    def _and_ind_x(self, pc, opcode):
        return (pc + 2,), "and " + IND_X % (opcode & 0xFF)

    def _jsr_sp(self, pc, opcode):
        addr = 0xFF00 | (opcode & 0xFF)
        return (pc + 2, addr), "jsr " + ADDR % (self._rom_offset + addr) 

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

    def _and_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "and " + ABS % abs

    def _rol_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "rol " + ABS % abs

    def _bmi(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bmi " + ADDR % (self._rom_offset + addr)

    def _and_ind_y(self, pc, opcode):
        return (pc + 2,), "and " + IND_Y % (opcode & 0xFF)

    def _set(self, pc, opcode):
        return (pc + 1,), "set"

    def _and_zp_x(self, pc, opcode):
        return (pc + 2,), "and " + ZP_X % (opcode & 0xFF)

    def _rol_zp_x(self, pc, opcode):
        return (pc + 2,), "rol " + ZP_X % (opcode & 0xFF)

    def _sec(self, pc, opcode):
        return (pc + 1,), "sec"

    def _and_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "and " + ABS_Y % abs 

    def _inc_a(self, pc, opcode):
        return (pc + 1,), "inc A"

    def _ldm_zp(self, pc, opcode):
        imm = (opcode >> 8) & 0xFF
        zp = opcode & 0xFF
        return (pc + 3,), "ldm " + IMM % imm + ", " + ZP % zp

    def _and_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "and " + ABS_X % abs 

    def _rol_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "rol " + ABS_X % abs 

    def _rti(self, pc, opcode):
        return (pc,), "rti"

    def _eor_ind_x(self, pc, opcode):
        return (pc + 2,), "eor " + IND_X % (opcode & 0xFF)

    def _stp(self, pc, opcode):
        return (pc + 1,), "stp"

    def _com_zp(self, pc, opcode):
        return (pc + 2,), "com " + ZP % (opcode & 0xFF)

    def _eor_zp(self, pc, opcode):
        return (pc + 2,), "eor " + ZP % (opcode & 0xFF)

    def _lsr_zp(self, pc, opcode):
        return (pc + 2,), "lsr " + ZP % (opcode & 0xFF)

    def _pha(self, pc, opcode):
        return (pc + 1,), "pha"

    def _eor_imm(self, pc, opcode):
        return (pc + 2,), "eor " + IMM % (opcode & 0xFF)

    def _lsr_a(self, pc, opcode):
        return (pc + 1,), "lsr A"

    def _jmp_abs(self, pc, opcode):
        addr = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (addr - self._rom_offset,), "jmp " + ADDR % addr

    def _eor_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "eor " + ABS % abs

    def _lsr_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "lsr " + ABS % abs

    def _bvc(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bvc " + ADDR % (self._rom_offset + addr)

    def _eor_ind_y(self, pc, opcode):
        return (pc + 2,), "eor " + IND_Y % (opcode & 0xFF)

    def _eor_zp_x(self, pc, opcode):
        return (pc + 2,), "eor " + ZP_X % (opcode & 0xFF)

    def _lsr_zp_x(self, pc, opcode):
        return (pc + 2,), "lsr " + ZP_X % (opcode & 0xFF)

    def _cli(self, pc, opcode):
        return (pc + 1,), "cli"

    def _eor_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "eor " + ABS_Y % abs

    def _eor_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "eor " + ABS_X % abs

    def _lsr_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "lsr " + ABS_X % abs

    def _rts(self, pc, opcode):
        return (pc,), "rts"

    def _adc_ind_x(self, pc, opcode):
        return (pc + 2,), "adc " + IND_X % (opcode & 0xFF)

    def _mul_zp_x(self, pc, opcode):
        return (pc + 2,), "mul " + ZP_X % (opcode & 0xFF)

    def _tst_zp(self, pc, opcode):
        return (pc + 2,), "tst " + ZP % (opcode & 0xFF)

    def _adc_zp(self, pc, opcode):
        return (pc + 2,), "adc " + ZP % (opcode & 0xFF)

    def _ror_zp(self, pc, opcode):
        return (pc + 2,), "ror " + ZP % (opcode & 0xFF)

    def _pla(self, pc, opcode):
        return (pc + 1,), "pla"

    def _adc_imm(self, pc, opcode):
        return (pc + 2,), "adc" + IMM % (opcode & 0xFF)

    def _ror_a(self, pc, opcode):
        return (pc + 1,), "ror A"

    def _jmp_ind(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "jmp " + IND % abs

    def _adc_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "adc " + ABS % abs 

    def _ror_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ror " + ABS % abs 

    def _bvs(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bvs " + ADDR % (self._rom_offset + addr)

    def _adc_ind_y(self, pc, opcode):
        return (pc + 2,), "adc " + IND_Y % (opcode & 0xFF)

    def _adc_zp_x(self, pc, opcode):
        return (pc + 2,), "adc " + ZP_X % (opcode & 0xFF)

    def _ror_zp_x(self, pc, opcode):
        return (pc + 2,), "ror " + ZP_X % (opcode & 0xFF)

    def _sei(self, pc, opcode):
        return (pc + 1,), "sei"

    def _adc_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "adc " + ABS_Y % abs 

    def _adc_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "adc " + ABS_X % abs 

    def _ror_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ror " + ABS_X % abs 

    def _bra(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (addr,), "bra " + ADDR % addr

    def _sta_ind_x(self, pc, opcode):
        return (pc + 2,), "sta " + IND_X % (opcode & 0xFF)

    def _rrf_zp(self, pc, opcode):
        return (pc + 2,), "rrf " + ZP % (opcode & 0xFF)

    def _sty_zp(self, pc, opcode):
        return (pc + 2,), "sty " + ZP % (opcode & 0xFF)

    def _sta_zp(self, pc, opcode):
        return (pc + 2,), "sta " + ZP % (opcode & 0xFF)

    def _stx_zp(self, pc, opcode):
        return (pc + 2,), "stx " + ZP % (opcode & 0xFF)

    def _dey(self, pc, opcode):
        return (pc + 1,), "dey"

    def _txa(self, pc, opcode):
        return (pc + 1,), "txa"

    def _sty_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sty " + ABS % abs 

    def _sta_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sta " + ABS % abs 

    def _stx_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "stx " + ABS % abs 

    def _bcc(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bcc " + ADDR % (self._rom_offset + addr)

    def _sta_ind_y(self, pc, opcode):
        return (pc + 2,), "sta " + IND_Y % (opcode & 0xFF)

    def _sty_zp_x(self, pc, opcode):
        return (pc + 2,), "sty " + ZP_X % (opcode & 0xFF)

    def _sta_zp_x(self, pc, opcode):
        return (pc + 2,), "sta " + ZP_X % (opcode & 0xFF)

    def _stx_zp_y(self, pc, opcode):
        return (pc + 2,), "stx " + ZP_Y % (opcode & 0xFF)

    def _tya(self, pc, opcode):
        return (pc + 1,), "tya"

    def _sta_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sta " + ABS_Y % abs

    def _txs(self, pc, opcode):
        return (pc + 1,), "txs"

    def _sta_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sta " + ABS_X % abs

    def _ldy_imm(self, pc, opcode):
        return (pc + 2,), "ldy " + IMM % (opcode & 0xFF)

    def _lda_ind_x(self, pc, opcode):
        return (pc + 2,), "lda " + IND_X % (opcode & 0xFF)

    def _ldx_imm(self, pc, opcode):
        return (pc + 2,), "ldx " + IMM % (opcode & 0xFF)

    def _ldy_zp(self, pc, opcode):
        return (pc + 2,), "ldy " + ZP % (opcode & 0xFF)

    def _lda_zp(self, pc, opcode):
        return (pc + 2,), "lda " + ZP % (opcode & 0xFF)

    def _ldx_zp(self, pc, opcode):
        return (pc + 2,), "ldx " + ZP % (opcode & 0xFF)

    def _tay(self, pc, opcode):
        return (pc + 1,), "tay"

    def _lda_imm(self, pc, opcode):
        return (pc + 2,), "lda " + IMM % (opcode & 0xFF)

    def _tax(self, pc, opcode):
        return (pc + 1,), "tax"

    def _ldy_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ldy " + ABS % abs 

    def _lda_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "lda " + ABS % abs 

    def _ldx_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ldx " + ABS % abs 

    def _bcs(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bcs " + ADDR % (self._rom_offset + addr)

    def _lda_ind_y(self, pc, opcode):
        return (pc + 2,), "lda " + IND_Y % (opcode & 0xFF)

    def _jmp_zp_ind(self, pc, opcode):
        return (pc + 2,), "jmp " + ZP_IND % (opcode & 0xFF)

    def _ldy_zp_x(self, pc, opcode):
        return (pc + 2,), "ldy " + ZP_X % (opcode & 0xFF)

    def _lda_zp_x(self, pc, opcode):
        return (pc + 2,), "lda " + ZP_X % (opcode & 0xFF)

    def _ldx_zp_y(self, pc, opcode):
        return (pc + 2,), "ldx " + ZP_Y % (opcode & 0xFF)

    def _clv(self, pc, opcode):
        return (pc + 1,), "clv"

    def _lda_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "lda " + ABS_Y % abs

    def _tsx(self, pc, opcode):
        return (pc + 1,), "tsx"

    def _ldy_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ldy " + ABS_X % abs

    def _lda_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "lda " + ABS_X % abs

    def _ldx_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ldx " + ABS_Y % abs

    def _cpy_imm(self, pc, opcode):
        return (pc + 2,), "cpy " + IMM % (opcode & 0xFF)

    def _cmp_ind_x(self, pc, opcode):
        return (pc + 2,), "cmp " + IND_X % (opcode & 0xFF)

    def _wit(self, pc, opcode):
        return (pc + 1,), "wit"

    def _cpy_zp(self, pc, opcode):
        return (pc + 2,), "cpy " + ZP % (opcode & 0xFF)

    def _cmp_zp(self, pc, opcode):
        return (pc + 2,), "cmp " + ZP % (opcode & 0xFF)

    def _dec_zp(self, pc, opcode):
        return (pc + 2,), "dec " + ZP % (opcode & 0xFF)

    def _iny(self, pc, opcode):
        return (pc + 1,), "iny"

    def _cmp_imm(self, pc, opcode):
        return (pc + 2,), "cmp " + IMM % (opcode & 0xFF)

    def _dex(self, pc, opcode):
        return (pc + 1,), "dex"

    def _cpy_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "cpy " + ABS % abs 

    def _cmp_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "cmp " + ABS % abs 

    def _dec_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "dec " + ABS % abs 

    def _bne(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "bne " + ADDR % (self._rom_offset + addr)

    def _cmp_ind_y(self, pc, opcode):
        return (pc + 2,), "cmp " + IND_Y % (opcode & 0xFF)

    def _cmp_zp_x(self, pc, opcode):
        return (pc + 2,), "cmp " + ZP_X % (opcode & 0xFF)

    def _dec_zp_x(self, pc, opcode):
        return (pc + 2,), "dec " + ZP_X % (opcode & 0xFF)

    def _cld(self, pc, opcode):
        return (pc + 1,), "cld"

    def _cmp_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "cmp " + ABS_Y % abs

    def _cmp_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "cmp " + ABS_X % abs

    def _dec_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "dec " + ABS_X % abs

    def _cpx_imm(self, pc, opcode):
        return (pc + 2,), "cpx " + IMM % (opcode & 0xFF)

    def _sbc_ind_x(self, pc, opcode):
        return (pc + 2,), "sbc " + IND_X % (opcode & 0xFF)

    def _div_zp_x(self, pc, opcode):
        return (pc + 2,), "div " + ZP_X % (opcode & 0xFF)

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

    def _cpx_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "cpx " + ABS % abs

    def _sbc_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sbc " + ABS % abs

    def _inc_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "inc " + ABS % abs

    def _beq(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (pc + 2, addr), "beq " + ADDR % (self._rom_offset + addr)

    def _sbc_ind_y(self, pc, opcode):
        return (pc + 2,), "sbc" + IND_Y % (opcode & 0xFF)

    def _sbc_zp_x(self, pc, opcode):
        return (pc + 2,), "sbc " + ZP_X % (opcode & 0xFF)

    def _inc_zp_x(self, pc, opcode):
        return (pc + 2,), "inc " + ZP_X % (opcode & 0xFF)

    def _sed(self, pc, opcode):
        return (pc + 1,), "sed"

    def _sbc_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sbc " + ABS_Y % abs

    def _sbc_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sbc " + ABS_X % abs

    def _inc_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "abs " + ABS_X % abs

    def _dummy(self, pc, opcode):
        return (pc + 1,), "db %0.2X" % opcode

#from rom import ROM
#rom = ROM("./assets/pp.bin")
#dasm = M37520dasm()
#dasm.disassemble2text(rom, "pp.asm")
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

class STK55C324dasm():
    def __init__(self, roots=None):
        self._instructions = (
            (STK55C324dasm._brk, 1),
            (STK55C324dasm._ora_ind_x, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._tsb_zp, 2),
            (STK55C324dasm._ora_zp, 2),
            (STK55C324dasm._asl_zp, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._php, 1),
            (STK55C324dasm._ora_imm, 2),
            (STK55C324dasm._asl_a, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._tsb_abs, 3),
            (STK55C324dasm._ora_abs, 3),
            (STK55C324dasm._asl_abs, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bpl, 2),
            (STK55C324dasm._ora_ind_y, 2),
            (STK55C324dasm._ora_zp_ind, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._trb_zp, 2),
            (STK55C324dasm._ora_zp_x, 2),
            (STK55C324dasm._asl_zp_x, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._clc, 1),
            (STK55C324dasm._ora_abs_y, 3),
            (STK55C324dasm._inc_a, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._trb_abs, 3),
            (STK55C324dasm._ora_abs_x, 3),
            (STK55C324dasm._asl_abs_x, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._jsr_abs, 3),
            (STK55C324dasm._and_ind_x, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._bit_zp, 2),
            (STK55C324dasm._and_zp, 2),
            (STK55C324dasm._rol_zp, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._plp, 1),
            (STK55C324dasm._and_imm, 2),
            (STK55C324dasm._rol_a, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bit_abs, 3),
            (STK55C324dasm._and_abs, 3),
            (STK55C324dasm._rol_abs, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bmi, 2),
            (STK55C324dasm._and_ind_y, 2),
            (STK55C324dasm._and_zp_ind, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bit_zp_x, 2),
            (STK55C324dasm._and_zp_x, 2),
            (STK55C324dasm._rol_zp_x, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._sec, 1),
            (STK55C324dasm._and_abs_y, 3),
            (STK55C324dasm._dec_a, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bit_abs_x, 3),
            (STK55C324dasm._and_abs_x, 3),
            (STK55C324dasm._rol_abs_x, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._rti, 1),
            (STK55C324dasm._eor_ind_x, 2),
            *([(STK55C324dasm._dummy, 1)] * 3),
            (STK55C324dasm._eor_zp, 2),
            (STK55C324dasm._lsr_zp, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._pha, 1),
            (STK55C324dasm._eor_imm, 2),
            (STK55C324dasm._lsr_a, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._jmp_abs, 3),
            (STK55C324dasm._eor_abs, 3),
            (STK55C324dasm._lsr_abs, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bvc, 2),
            (STK55C324dasm._eor_ind_y, 2),
            (STK55C324dasm._eor_zp_ind, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._eor_zp_x, 2),
            (STK55C324dasm._lsr_zp_x, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._cli, 1),
            (STK55C324dasm._eor_abs_y, 3),
            (STK55C324dasm._phy, 1),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._eor_abs_x, 3),
            (STK55C324dasm._lsr_abs_x, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._rts, 1),
            (STK55C324dasm._adc_ind_x, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._stz_zp, 2),
            (STK55C324dasm._adc_zp, 2),
            (STK55C324dasm._ror_zp, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._pla, 1),
            (STK55C324dasm._adc_imm, 2),
            (STK55C324dasm._ror_a, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._jmp_ind, 3),
            (STK55C324dasm._adc_abs, 3),
            (STK55C324dasm._ror_abs, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bvs, 2),
            (STK55C324dasm._adc_ind_y, 2),
            (STK55C324dasm._adc_zp_ind, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._stz_zp_x, 2),
            (STK55C324dasm._adc_zp_x, 2),
            (STK55C324dasm._ror_zp_x, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._sei, 1),
            (STK55C324dasm._adc_abs_y, 3),
            (STK55C324dasm._ply, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._jmp_abs_ind_x, 3),
            (STK55C324dasm._adc_abs_x, 3),
            (STK55C324dasm._ror_abs_x, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bra, 2),
            (STK55C324dasm._sta_ind_x, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._sty_zp, 2),
            (STK55C324dasm._sta_zp, 2),
            (STK55C324dasm._stx_zp, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._dey, 1),
            (STK55C324dasm._bit_imm, 1),
            (STK55C324dasm._txa, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._sty_abs, 3),
            (STK55C324dasm._sta_abs, 3),
            (STK55C324dasm._stx_abs, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bcc, 2),
            (STK55C324dasm._sta_ind_y, 2),
            (STK55C324dasm._sta_zp_ind, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._sty_zp_x, 2),
            (STK55C324dasm._sta_zp_x, 2),
            (STK55C324dasm._stx_zp_y, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._tya, 1),
            (STK55C324dasm._sta_abs_y, 3),
            (STK55C324dasm._txs, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._stz_abs, 3),
            (STK55C324dasm._sta_abs_x, 3),
            (STK55C324dasm._stz_abs_x, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._ldy_imm, 2),
            (STK55C324dasm._lda_ind_x, 2),
            (STK55C324dasm._ldx_imm, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._ldy_zp, 2),
            (STK55C324dasm._lda_zp, 2),
            (STK55C324dasm._ldx_zp, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._tay, 1),
            (STK55C324dasm._lda_imm, 2),
            (STK55C324dasm._tax, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._ldy_abs, 3),
            (STK55C324dasm._lda_abs, 3),
            (STK55C324dasm._ldx_abs, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bcs, 2),
            (STK55C324dasm._lda_ind_y, 2),
            (STK55C324dasm._lda_zp_ind, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._ldy_zp_x, 2),
            (STK55C324dasm._lda_zp_x, 2),
            (STK55C324dasm._ldx_zp_y, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._clv, 1),
            (STK55C324dasm._lda_abs_y, 3),
            (STK55C324dasm._tsx, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._ldy_abs_x, 3),
            (STK55C324dasm._lda_abs_x, 3),
            (STK55C324dasm._ldx_abs_y, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._cpy_imm, 2),
            (STK55C324dasm._cmp_ind_x, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._cpy_zp, 2),
            (STK55C324dasm._cmp_zp, 2),
            (STK55C324dasm._dec_zp, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._iny, 1),
            (STK55C324dasm._cmp_imm, 2),
            (STK55C324dasm._dex, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._cpy_abs, 3),
            (STK55C324dasm._cmp_abs, 3),
            (STK55C324dasm._dec_abs, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._bne, 2),
            (STK55C324dasm._cmp_ind_y, 2),
            (STK55C324dasm._cmp_zp_ind, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._cmp_zp_x, 2),
            (STK55C324dasm._dec_zp_x, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._cld, 1),
            (STK55C324dasm._cmp_abs_y, 3),
            (STK55C324dasm._phx, 1),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._cmp_abs_x, 3),
            (STK55C324dasm._dec_abs_x, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._cpx_imm, 2),
            (STK55C324dasm._sbc_ind_x, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._cpx_zp, 2),
            (STK55C324dasm._sbc_zp, 2),
            (STK55C324dasm._inc_zp, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._inx, 1),
            (STK55C324dasm._sbc_imm, 2),
            (STK55C324dasm._nop, 1),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._cpx_abs, 3),
            (STK55C324dasm._sbc_abs, 3),
            (STK55C324dasm._inc_abs, 3),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._beq, 2),
            (STK55C324dasm._sbc_ind_y, 2),
            (STK55C324dasm._sbc_zp_ind, 2),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._sbc_zp_x, 2),
            (STK55C324dasm._inc_zp_x, 2),
            (STK55C324dasm._dummy, 1),
            (STK55C324dasm._sed, 1),
            (STK55C324dasm._sbc_abs_y, 3),
            (STK55C324dasm._plx, 1),
            *([(STK55C324dasm._dummy, 1)] * 2),
            (STK55C324dasm._sbc_abs_x, 3),
            (STK55C324dasm._inc_abs_x, 3),
            (STK55C324dasm._dummy, 1)
        )

    def disassemble(self, rom):
        if (rom.size() > 0 and rom.size() <= ADDRESS_SPACE_SIZE):
            self._rom_offset = ADDRESS_SPACE_SIZE - rom.size()
            listing = [None] * rom.size()
            for i in range(16):
                vector = rom.size() - 2 - i * 2
                if (vector > 0):
                    addr = (rom.get_byte(vector) | (rom.get_byte(vector + 1) << 8)) - self._rom_offset
                    listing = self._disassemble(addr, listing, rom)
            result = [()] * ADDRESS_SPACE_SIZE
            for i in range(len(listing)):
                if (listing[i] is None):
                    byte = rom.get_byte(i)
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
            opcode = rom.get_byte(pc)
            instruction = self._instructions[opcode]
            instruction_size = instruction[1]
            if (instruction_size > 1):
                opcode = rom.get_bytes(pc, instruction_size)
            next_pc, symbol = instruction[0](self, pc, opcode)
            listing[pc] = (instruction_size, opcode, symbol)
            while ((instruction_size > 1)  and ((pc + 1) < len(listing))):
                instruction_size -= 1
                pc += 1
                listing[pc] = (1, rom.get_byte(pc), '')
            pc = next_pc[0]
            if (len(next_pc) > 1):
                listing = self._disassemble(next_pc[1], listing, rom)
        return listing

    def _brk(self, pc, opcode):
        return (pc + 1,), "brk"

    def _ora_ind_x(self, pc, opcode):
        return (pc + 2,), "ora " + IND_X % (opcode & 0xFF)

    def _tsb_zp(self, pc, opcode):
        return (pc + 2,), "tsb " + ZP % (opcode & 0xFF)

    def _ora_zp(self, pc, opcode):
        return (pc + 2,), "ora " + ZP % (opcode & 0xFF)

    def _asl_zp(self, pc, opcode):
        return (pc + 2,), "asl " + ZP % (opcode & 0xFF)

    def _php(self, pc, opcode):
        return (pc + 1,), "php"

    def _ora_imm(self, pc, opcode):
        return (pc + 2,), "ora " + IMM % (opcode & 0xFF)

    def _asl_a(self, pc, opcode):
        return (pc + 1,), "asl A"

    def _seb_bit_a(self, pc, opcode):
        bit = (opcode >> 5 & 0x7)
        return (pc + 1,), "seb " + BIT_A % bit 

    def _tsb_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "tsb " + ABS % abs

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

    def _ora_zp_ind(self, pc, opcode):
        return (pc + 2,), "ora " + ZP_IND % (opcode & 0xFF)

    def _clt(self, pc, opcode):
        return (pc + 1,), "clt"

    def _trb_zp(self, pc, opcode):
        return (pc + 2,), "trb " + ZP % (opcode & 0xFF)

    def _ora_zp_x(self, pc, opcode):
        return (pc + 2,), "ora " + ZP_X % (opcode & 0xFF)

    def _asl_zp_x(self, pc, opcode):
        return (pc + 2,), "asl " + ZP_X % (opcode & 0xFF)

    def _clc(self, pc, opcode):
        return (pc + 1,), "clc"

    def _ora_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ora " + ABS_Y % abs

    def _dec_a(self, pc, opcode):
        return (pc + 1,), "dec A"

    def _trb_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "trb " + ABS % abs

    def _ora_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ora " + ABS_X % abs 

    def _asl_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "asl" + ABS_X % abs

    def _jsr_abs(self, pc, opcode):
        addr = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3, addr - self._rom_offset), "jsr " + ADDR % addr

    def _and_ind_x(self, pc, opcode):
        return (pc + 2,), "and " + IND_X % (opcode & 0xFF)

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

    def _and_zp_ind(self, pc, opcode):
        return (pc + 2,), "and " + ZP_IND % (opcode & 0xFF)

    def _bit_zp_x(self, pc, opcode):
        return (pc + 2,), "bit " + ZP_X % (opcode & 0xFF)

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

    def _bit_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "bit " + ABS_X % abs 

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

    def _eor_zp_ind(self, pc, opcode):
        return (pc + 2,), "eor " + ZP_IND % (opcode & 0xFF)

    def _eor_zp_x(self, pc, opcode):
        return (pc + 2,), "eor " + ZP_X % (opcode & 0xFF)

    def _lsr_zp_x(self, pc, opcode):
        return (pc + 2,), "lsr " + ZP_X % (opcode & 0xFF)

    def _cli(self, pc, opcode):
        return (pc + 1,), "cli"

    def _phy(self, pc, opcode):
        return (pc + 1,), "phy"

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

    def _stz_zp(self, pc, opcode):
        return (pc + 2,), "stz " + ZP % (opcode & 0xFF)

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
        return (0,), "jmp " + IND % abs

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

    def _adc_zp_ind(self, pc, opcode):
        return (pc + 2,), "adc " + ZP_IND % (opcode & 0xFF)

    def _stz_zp_x(self, pc, opcode):
        return (pc + 2,), "stz " + ZP_X % (opcode & 0xFF)

    def _adc_zp_x(self, pc, opcode):
        return (pc + 2,), "adc " + ZP_X % (opcode & 0xFF)

    def _ror_zp_x(self, pc, opcode):
        return (pc + 2,), "ror " + ZP_X % (opcode & 0xFF)

    def _sei(self, pc, opcode):
        return (pc + 1,), "sei"

    def _adc_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "adc " + ABS_Y % abs 

    def _ply(self, pc, opcode):
        return (pc + 1,), "ply"

    def _jmp_abs_ind_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (0,), "jmp " + IND_X % abs

    def _adc_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "adc " + ABS_X % abs 

    def _ror_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "ror " + ABS_X % abs 

    def _bra(self, pc, opcode):
        addr = (pc + 2 + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return (addr,), "bra " + ADDR % (self._rom_offset + addr)

    def _sta_ind_x(self, pc, opcode):
        return (pc + 2,), "sta " + IND_X % (opcode & 0xFF)

    def _sty_zp(self, pc, opcode):
        return (pc + 2,), "sty " + ZP % (opcode & 0xFF)

    def _sta_zp(self, pc, opcode):
        return (pc + 2,), "sta " + ZP % (opcode & 0xFF)

    def _stx_zp(self, pc, opcode):
        return (pc + 2,), "stx " + ZP % (opcode & 0xFF)

    def _dey(self, pc, opcode):
        return (pc + 1,), "dey"

    def _bit_imm(self, pc, opcode):
        return (pc + 2,), "bit " + IMM % (opcode & 0xFF)

    def _txa(self, pc, opcode):
        return (pc + 1,), "txa"

    def _sty_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sty " + ABS % abs 

    def _sta_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sta " + ABS % abs 

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

    def _sta_zp_ind(self, pc, opcode):
        return (pc + 2,), "sta " + ZP_IND % (opcode & 0xFF)

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

    def _stz_abs(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "stz " + ABS % abs 

    def _sta_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sta " + ABS_X % abs

    def _stz_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "stz " + ABS_X % abs

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

    def _lda_zp_ind(self, pc, opcode):
        return (pc + 2,), "lda " + ZP_IND % (opcode & 0xFF)

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

    def _cmp_zp_ind(self, pc, opcode):
        return (pc + 2,), "cmp " + ZP_IND % (opcode & 0xFF)

    def _cmp_zp_x(self, pc, opcode):
        return (pc + 2,), "cmp " + ZP_X % (opcode & 0xFF)

    def _dec_zp_x(self, pc, opcode):
        return (pc + 2,), "dec " + ZP_X % (opcode & 0xFF)

    def _cld(self, pc, opcode):
        return (pc + 1,), "cld"

    def _cmp_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "cmp " + ABS_Y % abs

    def _phx(self, pc, opcode):
        return (pc + 1,), "phx"

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

    def _sbc_zp_ind(self, pc, opcode):
        return (pc + 2,), "sbc" + ZP_IND % (opcode & 0xFF)

    def _sbc_zp_x(self, pc, opcode):
        return (pc + 2,), "sbc " + ZP_X % (opcode & 0xFF)

    def _inc_zp_x(self, pc, opcode):
        return (pc + 2,), "inc " + ZP_X % (opcode & 0xFF)

    def _sed(self, pc, opcode):
        return (pc + 1,), "sed"

    def _sbc_abs_y(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sbc " + ABS_Y % abs

    def _plx(self, pc, opcode):
        return (pc + 1,), "plx"

    def _sbc_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "sbc " + ABS_X % abs

    def _inc_abs_x(self, pc, opcode):
        abs = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return (pc + 3,), "abs " + ABS_X % abs

    def _dummy(self, pc, opcode):
        return (pc + 1,), "illegal instruction"
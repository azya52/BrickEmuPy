PSETOP = 0b111001000000
PSETMASK = 0b111111100000

class E0C6200dasm():

    def __init__(self):
        self._base = '0x%X'
        self._nibbase = '0x%0.1X'
        self._bytebase = '0x%0.2X'
        self._wordbase = '0x%0.3X'
        self._addrbase = '%00.4X'
        self._opbase = '%0.3X'

        self._abmxmy_tbl = (
            "A",
            "B",
            "M(X)",
            "M(Y)"
        )

        self._instruction_tbl = (
            *([E0C6200dasm._jp_s] * 256),           #0 0 0 0  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200dasm._retd_l] * 256),         #0 0 0 1  l7 l6 l5 l4  l3 l2 l1 l0
            *([E0C6200dasm._jp_c_s] * 256),         #0 0 1 0  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200dasm._jp_nc_s] * 256),        #0 0 1 1  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200dasm._call_s] * 256),         #0 1 0 0  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200dasm._calz_s] * 256),         #0 1 0 1  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200dasm._jp_z_s] * 256),         #0 1 1 0  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200dasm._jp_nz_s] * 256),        #0 1 1 1  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200dasm._ld_y_y] * 256),         #1 0 0 0  y7 y6 y5 y4  y3 y2 y1 y0
            *([E0C6200dasm._lbpx_mx_l] * 256),      #1 0 0 1  l7 l6 l5 l4  l3 l2 l1 l0
            *([E0C6200dasm._adc_xh_i] * 16),        #1 0 1 0  0 0 0 0  i3 i2 i1 i0
            *([E0C6200dasm._adc_xl_i] * 16),        #1 0 1 0  0 0 0 1  i3 i2 i1 i0
            *([E0C6200dasm._adc_yh_i] * 16),        #1 0 1 0  0 0 1 0  i3 i2 i1 i0
            *([E0C6200dasm._adc_yl_i] * 16),        #1 0 1 0  0 0 1 1  i3 i2 i1 i0
            *([E0C6200dasm._cp_xh_i] * 16),         #1 0 1 0  0 1 0 0  i3 i2 i1 i0
            *([E0C6200dasm._cp_xl_i] * 16),         #1 0 1 0  0 1 0 1  i3 i2 i1 i0
            *([E0C6200dasm._cp_yh_i] * 16),         #1 0 1 0  0 1 1 0  i3 i2 i1 i0
            *([E0C6200dasm._cp_yl_i] * 16),         #1 0 1 0  0 1 1 1  i3 i2 i1 i0
            *([E0C6200dasm._add_r_q] * 16),         #1 0 1 0  1 0 0 0  r1 r0 q1 q0
            *([E0C6200dasm._adc_r_q] * 16),         #1 0 1 0  1 0 0 1  r1 r0 q1 q0
            *([E0C6200dasm._sub_r_q] * 16),         #1 0 1 0  1 0 1 0  r1 r0 q1 q0
            *([E0C6200dasm._sbc_r_q] * 16),         #1 0 1 0  1 0 1 1  r1 r0 q1 q0
            *([E0C6200dasm._and_r_q] * 16),         #1 0 1 0  1 1 0 0  r1 r0 q1 q0
            *([E0C6200dasm._or_r_q] * 16),          #1 0 1 0  1 1 0 1  r1 r0 q1 q0
            *([E0C6200dasm._xor_r_q] * 16),         #1 0 1 0  1 1 1 0  r1 r0 q1 q0
            *([E0C6200dasm._rlc_r] * 16),           #1 0 1 0  1 1 1 1  r1 r0 r1 r0
            *([E0C6200dasm._ld_x_x] * 256),         #1 0 1 1  x7 x6 x5 x4  x3 x2 x1 x0
            *([E0C6200dasm._add_r_i] * 64),         #1 1 0 0  0 0 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._adc_r_i] * 64),         #1 1 0 0  0 1 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._and_r_i] * 64),         #1 1 0 0  1 0 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._or_r_i] * 64),          #1 1 0 0  1 1 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._xor_r_i] * 64),         #1 1 0 1  0 0 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._sbc_r_i] * 64),         #1 1 0 1  0 1 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._fan_r_i] * 64),         #1 1 0 1  1 0 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._cp_r_i] * 64),          #1 1 0 1  1 1 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._ld_r_i] * 64),          #1 1 1 0  0 0 r1 r0  i3 i2 i1 i0
            *([E0C6200dasm._pset_p] * 32),          #1 1 1 0  0 1 0 p4  p3 p2 p1 p0
            *([E0C6200dasm._ldpx_mx_i] * 16),       #1 1 1 0  0 1 1 0  i3 i2 i1 i0
            *([E0C6200dasm._ldpy_my_i] * 16),       #1 1 1 0  0 1 1 1  i3 i2 i1 i0
            *([E0C6200dasm._ld_xp_r] * 4),          #1 1 1 0  1 0 0 0  0 0 r1 r0
            *([E0C6200dasm._ld_xh_r] * 4),          #1 1 1 0  1 0 0 0  0 1 r1 r0
            *([E0C6200dasm._ld_xl_r] * 4),          #1 1 1 0  1 0 0 0  1 0 r1 r0
            *([E0C6200dasm._rrc_r] * 4),            #1 1 1 0  1 0 0 0  1 1 r1 r0
            *([E0C6200dasm._ld_yp_r] * 4),          #1 1 1 0  1 0 0 1  0 0 r1 r0
            *([E0C6200dasm._ld_yh_r] * 4),          #1 1 1 0  1 0 0 1  0 1 r1 r0
            *([E0C6200dasm._ld_yl_r] * 4),          #1 1 1 0  1 0 0 1  1 0 r1 r0
            *([E0C6200dasm._dummy] * 4),
            *([E0C6200dasm._ld_r_xp] * 4),          #1 1 1 0  1 0 1 0  0 0 r1 r0
            *([E0C6200dasm._ld_r_xh] * 4),          #1 1 1 0  1 0 1 0  0 1 r1 r0
            *([E0C6200dasm._ld_r_xl] * 4),          #1 1 1 0  1 0 1 0  1 0 r1 r0
            *([E0C6200dasm._dummy] * 4),
            *([E0C6200dasm._ld_r_yp] * 4),          #1 1 1 0  1 0 1 1  0 0 r1 r0
            *([E0C6200dasm._ld_r_yh] * 4),          #1 1 1 0  1 0 1 1  0 1 r1 r0
            *([E0C6200dasm._ld_r_yl] * 4),          #1 1 1 0  1 0 1 1  1 0 r1 r0
            *([E0C6200dasm._dummy] * 4),
            *([E0C6200dasm._ld_r_q] * 16),          #1 1 1 0  1 1 0 0  r1 r0 q1 q0
            *([E0C6200dasm._dummy] * 16),
            *([E0C6200dasm._ldpx_r_q] * 16),        #1 1 1 0  1 1 1 0  r1 r0 q1 q0
            *([E0C6200dasm._ldpy_r_q] * 16),        #1 1 1 0  1 1 1 1  r1 r0 q1 q0
            *([E0C6200dasm._cp_r_q] * 16),          #1 1 1 1  0 0 0 0  r1 r0 q1 q0
            *([E0C6200dasm._fan_r_q] * 16),         #1 1 1 1  0 0 0 1  r1 r0 q1 q0
            *([E0C6200dasm._dummy] * 8),
            *([E0C6200dasm._acpx_mx_r] * 4),        #1 1 1 1  0 0 1 0  1 0 r1 r0
            *([E0C6200dasm._acpy_my_r] * 4),        #1 1 1 1  0 0 1 0  1 1 r1 r0
            *([E0C6200dasm._dummy] * 8),
            *([E0C6200dasm._scpx_mx_r] * 4),        #1 1 1 1  0 0 1 1  1 0 r1 r0
            *([E0C6200dasm._scpx_my_r] * 4),        #1 1 1 1  0 0 1 1  1 1 r1 r0
            *([E0C6200dasm._set_f_i] * 16),         #1 1 1 1  0 1 0 0  i3 i2 i1 i0
            *([E0C6200dasm._rst_f_i] * 16),         #1 1 1 1  0 1 0 1  i3 i2 i1 i0
            *([E0C6200dasm._inc_mn] * 16),          #1 1 1 1  0 1 1 0  n3 n2 n1 n0
            *([E0C6200dasm._dec_mn] * 16),          #1 1 1 1  0 1 1 1  n3 n2 n1 n0
            *([E0C6200dasm._ld_mn_a] * 16),         #1 1 1 1  1 0 0 0  n3 n2 n1 n0
            *([E0C6200dasm._ld_mn_b] * 16),         #1 1 1 1  1 0 0 1  n3 n2 n1 n0
            *([E0C6200dasm._ld_a_mn] * 16),         #1 1 1 1  1 0 1 0  n3 n2 n1 n0
            *([E0C6200dasm._ld_b_mn] * 16),         #1 1 1 1  1 0 1 1  n3 n2 n1 n0
            *([E0C6200dasm._push_r] * 4),           #1 1 1 1  1 1 0 0  0 0 r1 r0
            E0C6200dasm._push_xp,                   #1 1 1 1  1 1 0 0  0 1 0 0
            E0C6200dasm._push_xh,                   #1 1 1 1  1 1 0 0  0 1 0 1
            E0C6200dasm._push_xl,                   #1 1 1 1  1 1 0 0  0 1 1 0
            E0C6200dasm._push_yp,                   #1 1 1 1  1 1 0 0  0 1 1 1
            E0C6200dasm._push_yh,                   #1 1 1 1  1 1 0 0  1 0 0 0
            E0C6200dasm._push_yl,                   #1 1 1 1  1 1 0 0  1 0 0 1
            E0C6200dasm._push_f,                    #1 1 1 1  1 1 0 0  1 0 1 0
            E0C6200dasm._dec_sp,                    #1 1 1 1  1 1 0 0  1 0 1 1
            *([E0C6200dasm._dummy] * 4),
            *([E0C6200dasm._pop_r] * 4),            #1 1 1 1  1 1 0 1  0 0 r1 r0
            E0C6200dasm._pop_xp,                    #1 1 1 1  1 1 0 1  0 1 0 0
            E0C6200dasm._pop_xh,                    #1 1 1 1  1 1 0 1  0 1 0 1
            E0C6200dasm._pop_xl,                    #1 1 1 1  1 1 0 1  0 1 1 0
            E0C6200dasm._pop_yp,                    #1 1 1 1  1 1 0 1  0 1 1 1
            E0C6200dasm._pop_yh,                    #1 1 1 1  1 1 0 1  1 0 0 0
            E0C6200dasm._pop_yl,                    #1 1 1 1  1 1 0 1  1 0 0 1
            E0C6200dasm._pop_f,                     #1 1 1 1  1 1 0 1  1 0 1 0
            E0C6200dasm._inc_sp,                    #1 1 1 1  1 1 0 1  1 0 1 1
            *([E0C6200dasm._dummy] * 2),
            E0C6200dasm._rets,                      #1 1 1 1  1 1 0 1  1 1 1 0
            E0C6200dasm._ret,                       #1 1 1 1  1 1 0 1  1 1 1 1
            *([E0C6200dasm._ld_sph_r] * 4),         #1 1 1 1  1 1 1 0  0 0 r1 r0
            *([E0C6200dasm._ld_r_sph] * 4),         #1 1 1 1  1 1 1 0  0 1 r1 r0
            E0C6200dasm._jpba,                      #1 1 1 1  1 1 1 0  1 0 0 0
            *([E0C6200dasm._dummy] * 7),
            *([E0C6200dasm._ld_spl_r] * 4),         #1 1 1 1  1 1 1 1  0 0 r1 r0
            *([E0C6200dasm._ld_r_spl] * 4),         #1 1 1 1  1 1 1 1  0 1 r1 r0
            E0C6200dasm._halt,                      #1 1 1 1  1 1 1 1  1 0 0 0
            *([E0C6200dasm._dummy] * 2),
            E0C6200dasm._nop5,                      #1 1 1 1  1 1 1 1  1 0 1 1
            *([E0C6200dasm._dummy] * 3),
            E0C6200dasm._nop7                       #1 1 1 1  1 1 1 1  1 1 1 1
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            opcode = 0
            listing = [None] * (rom.size() // 2)
            for i in range(len(listing)):
                pc = i
                if (opcode & PSETMASK == PSETOP):
                    pc = opcode << 8 & 0x1F00
                opcode = rom.getWord(i * 2) & 0xFFF
                listing[i] = (self._opbase % opcode, self._instruction_tbl[opcode](self, pc, opcode))
            return {"LISTING": tuple(listing)}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        listing = self.disassemble(rom)["LISTING"]
        result = ""
        for i, line in enumerate(listing):
            result += (self._addrbase % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(30) + "\n"
        with open(file_path, 'w') as f:
            f.write(result)

    def _jp_s(self, pc, opcode):
        addr = (pc & 0x1F00) | (opcode & 0x0FF)
        return "jp " + self._addrbase % addr

    def _retd_l(self, pc, opcode):
        return "retd " + self._bytebase % (opcode & 0x0FF)

    def _jp_c_s(self, pc, opcode):
        addr = (pc & 0x1F00) | (opcode & 0x0FF)
        return "jp c, " + self._addrbase % addr

    def _jp_nc_s(self, pc, opcode):
        addr = (pc & 0x1F00) | (opcode & 0x0FF)
        return "jp nc, " + self._addrbase % addr

    def _call_s(self, pc, opcode):
        addr = (pc & 0x1F00) | (opcode & 0x0FF)
        return "call " + self._addrbase % addr

    def _calz_s(self, pc, opcode):
        addr = (pc & 0x1000) | (opcode & 0x0FF)
        return "callz " + self._addrbase % addr

    def _jp_z_s(self, pc, opcode):
        addr = (pc & 0x1F00) | (opcode & 0x0FF)
        return "jp z, " + self._addrbase % addr

    def _jp_nz_s(self, pc, opcode):
        addr = (pc & 0x1F00) | (opcode & 0x0FF)
        return "jp nz, " + self._addrbase % addr

    def _ld_y_y(self, pc, opcode):
        return "ld Y, " + self._bytebase % (opcode & 0x0FF)

    def _lbpx_mx_l(self, pc, opcode):
        return "lbpx M(X), " + self._bytebase % (opcode & 0x0FF)

    def _adc_xh_i(self, pc, opcode):
        return "adc XH, " + self._nibbase % (opcode & 0x00F)

    def _adc_xl_i(self, pc, opcode):
        return "adc XL, " + self._nibbase % (opcode & 0x00F)

    def _adc_yh_i(self, pc, opcode):
        return "adc YH, " + self._nibbase % (opcode & 0x00F)

    def _adc_yl_i(self, pc, opcode):
        return "adc YL, " + self._nibbase % (opcode & 0x00F)

    def _cp_xh_i(self, pc, opcode):
        return "cp XH, " + self._nibbase % (opcode & 0x00F)

    def _cp_xl_i(self, pc, opcode):
        return "cp XL, " + self._nibbase % (opcode & 0x00F)

    def _cp_yh_i(self, pc, opcode):
        return "cp YH, " + self._nibbase % (opcode & 0x00F)

    def _cp_yl_i(self, pc, opcode):
        return "adc YL, " + self._nibbase % (opcode & 0x00F)

    def _add_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "add " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[r]

    def _adc_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "adc " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[r]

    def _sub_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "sub " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[r]

    def _sbc_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "sbc " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[r]

    def _and_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "and " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[r]

    def _or_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "or " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[r]

    def _xor_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "xor " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[r]
   
    def _rlc_r(self, pc, opcode):
        r = opcode & 0x3
        return "rlc " + self._abmxmy_tbl[r]

    def _ld_x_x(self, pc, opcode):
        return "ld X, " + self._bytebase % (opcode & 0x0FF)

    def _add_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "add " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)

    def _adc_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "adc " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)

    def _and_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "and " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)

    def _or_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "or " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)
   
    def _xor_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "xor " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)

    def _sbc_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "sbc " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)

    def _fan_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "fan " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)

    def _cp_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "cp " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)

    def _ld_r_i(self, pc, opcode):
        r = opcode >> 4 & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", " + self._nibbase % (opcode & 0x00F)
 
    def _pset_p(self, pc, opcode):
        return "pset " + self._bytebase % (opcode & 0x01F)

    def _ldpx_mx_i(self, pc, opcode):
        return "ldpx M(X), " + self._nibbase % (opcode & 0x00F)

    def _ldpy_my_i(self, pc, opcode):
        return "ldpy M(Y), " + self._nibbase % (opcode & 0x00F)
  
    def _ld_xp_r(self, pc, opcode):
        r = opcode & 0x3
        return "ld XP, " + self._abmxmy_tbl[r]

    def _ld_xh_r(self, pc, opcode):
        r = opcode & 0x3
        return "ld XH, " + self._abmxmy_tbl[r]
 
    def _ld_xl_r(self, pc, opcode):
        r = opcode & 0x3
        return "ld XL, " + self._abmxmy_tbl[r]

    def _rrc_r(self, pc, opcode):
        r = opcode & 0x3
        return "rrc " + self._abmxmy_tbl[r]

    def _ld_yp_r(self, pc, opcode):
        r = opcode & 0x3
        return "ld YP, " + self._abmxmy_tbl[r]

    def _ld_yh_r(self, pc, opcode):
        r = opcode & 0x3
        return "ld YH, " + self._abmxmy_tbl[r]
 
    def _ld_yl_r(self, pc, opcode):
        r = opcode & 0x3
        return "ld YL, " + self._abmxmy_tbl[r]

    def _dummy(self, pc, opcode):
        return "dw " + self._wordbase % opcode

    def _ld_r_xp(self, pc, opcode):
        r = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", XP"

    def _ld_r_xh(self, pc, opcode):
        r = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", XH"

    def _ld_r_xl(self, pc, opcode):
        r = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", XL"
  
    def _ld_r_yp(self, pc, opcode):
        r = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", YP"

    def _ld_r_yh(self, pc, opcode):
        r = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", YH"
  
    def _ld_r_yl(self, pc, opcode):
        r = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", YL"

    def _ld_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[q]

    def _ldpx_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        if (r == q):
            return "inc X"
        return "ldpx " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[q]

    def _ldpy_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        if (r == q):
            return "inc Y"
        return "ldpy " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[q]

    def _cp_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "cp " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[q]
   
    def _fan_r_q(self, pc, opcode):
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        return "fan " + self._abmxmy_tbl[r] + ", " + self._abmxmy_tbl[q]
  
    def _acpx_mx_r(self, pc, opcode):
        r = opcode & 0x3
        return "acpx M(X), " + self._abmxmy_tbl[r]

    def _acpy_my_r(self, pc, opcode):
        r = opcode & 0x3
        return "acpy M(Y), " + self._abmxmy_tbl[r]
  
    def _scpx_mx_r(self, pc, opcode):
        r = opcode & 0x3
        return "scpx M(X), " + self._abmxmy_tbl[r]
 
    def _scpx_my_r(self, pc, opcode):
        r = opcode & 0x3
        return "scpx M(Y), " + self._abmxmy_tbl[r]

    def _set_f_i(self, pc, opcode):
        f = opcode & 0x00F
        if (f == 0x1):
            return "scf"
        elif (f == 0x2):
            return "szf"
        elif (f == 0x4):
            return "sdf"
        elif (f == 0x8):
            return "ei"
        return "set F, " + self._nibbase % f

    def _rst_f_i(self, pc, opcode):
        f = opcode & 0x00F
        if (f == 0xE):
            return "rcf"
        elif (f == 0xD):
            return "rzf"
        elif (f == 0xB):
            return "rdf"
        elif (f == 0x7):
            return "di"
        return "rst F, " + self._nibbase % f

    def _inc_mn(self, pc, opcode):
        n = opcode & 0x00F
        return "inc M(" + self._nibbase % n + ")"

    def _dec_mn(self, pc, opcode):
        n = opcode & 0x00F
        return "inc M(" + self._nibbase % n + ")"
   
    def _ld_mn_a(self, pc, opcode):
        n = opcode & 0x00F  
        return "ld M(" + self._nibbase % n + "), A"

    def _ld_mn_b(self, pc, opcode):
        n = opcode & 0x00F  
        return "ld M(" + self._nibbase % n + "), B"
   
    def _ld_a_mn(self, pc, opcode):
        n = opcode & 0x00F  
        return "ld A, M(" + self._nibbase % n + ")"

    def _ld_b_mn(self, pc, opcode):
        n = opcode & 0x00F  
        return "ld B, M(" + self._nibbase % n + ")"
    
    def _push_r(self, pc, opcode):
        r = opcode & 0x3
        return "push " + self._abmxmy_tbl[r]

    def _push_xp(self, pc, opcode):
        return "push XP"

    def _push_xh(self, pc, opcode):
        return "push XH"
 
    def _push_xl(self, pc, opcode):
        return "push XL"
    
    def _push_yp(self, pc, opcode):
        return "push YP"

    def _push_yh(self, pc, opcode):
        return "push YH"
 
    def _push_yl(self, pc, opcode):
        return "push YL"

    def _push_f(self, pc, opcode):
        return "push F"
  
    def _dec_sp(self, pc, opcode):
        return "dec SP"
  
    def _pop_r(self, pc, opcode):
        r = opcode & 0x3
        return "pop " + self._abmxmy_tbl[r]

    def _pop_xp(self, pc, opcode):
        return "pop XP"

    def _pop_xh(self, pc, opcode):
        return "pop XH"

    def _pop_xl(self, pc, opcode):
        return "pop XL"
 
    def _pop_yp(self, pc, opcode):
        return "pop YP"

    def _pop_yh(self, pc, opcode):
        return "pop YH"

    def _pop_yl(self, pc, opcode):
        return "pop YL"

    def _pop_f(self, pc, opcode):
        return "pop F"

    def _inc_sp(self, pc, opcode):
        return "inc SP"
   
    def _rets(self, pc, opcode):
        return "rets"

    def _ret(self, pc, opcode):
        return "ret"

    def _ld_sph_r(self, pc, opcode):
        r = opcode & 0x3
        return "ld SPH, " + self._abmxmy_tbl[r]

    def _ld_r_sph(self, pc, opcode):
        r = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", SPH"

    def _jpba(self, pc, opcode):
        return "jpba"

    def _ld_spl_r(self, pc, opcode):
        r = opcode & 0x3
        return "ld SPL, " + self._abmxmy_tbl[r]

    def _ld_r_spl(self, pc, opcode):
        r = opcode & 0x3
        return "ld " + self._abmxmy_tbl[r] + ", SPL"

    def _halt(self, pc, opcode):
        return "halt"
  
    def _nop5(self, pc, opcode):
        return "nop5"

    def _nop7(self, pc, opcode):
        return "nop7"
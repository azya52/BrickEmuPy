from .rom import ROM
from .PinTogglingSound import PinTogglingSound

SUB_CLOCK = 32768

ADDRESS_SPACE_SIZE = 0x10000

SFR_SIZE = 0x40
RAM_SIZE = 0x200
RAM_OFFSET = 0x40
LCDRAM_SIZE = 0xB0
LCDRAM_OFFSET_B0 = 0x40
LCDRAM_OFFSET_B3 = 0x340

VADDR_RESET = 4
VADDR_BRK = 34

IO_INTEDGE_INT0 = 0x01
IO_INTEDGE_INT1 = 0x02

IO_IREQ1_INT0 = 0x01
IO_IREQ1_INT1 = 0x02
IO_IREQ1_SIOR1 = 0x04
IO_IREQ1_SIOT1 = 0x08
IO_IREQ1_TX = 0x10 
IO_IREQ1_TY = 0x20 
IO_IREQ1_T2 = 0x40 
IO_IREQ1_T3 = 0x80 

IO_IREQ2_SIOR2 = 0x01
IO_IREQ2_SIOT2 = 0x02
IO_IREQ2_CNTR0 = 0x04
IO_IREQ2_CNTR1 = 0x08
IO_IREQ2_T1 = 0x10 
IO_IREQ2_KEYON = 0x20

IO_ICON1_INT0 = 0x01
IO_ICON1_INT1 = 0x02
IO_ICON1_SIOR1 = 0x04
IO_ICON1_SIOT1 = 0x08
IO_ICON1_TX = 0x10 
IO_ICON1_TY = 0x20 
IO_ICON1_T2 = 0x40 
IO_ICON1_T3 = 0x80 

IO_ICON2_SIOR2 = 0x01
IO_ICON2_SIOT2 = 0x02
IO_ICON2_CNTR0 = 0x04
IO_ICON2_CNTR1 = 0x08
IO_ICON2_T1 = 0x10 
IO_ICON2_KEYON = 0x20

IO_TXM_WCTRL = 0x01
IO_TXM_OPMODE = 0x30
IO_TXM_CNTR0 = 0x40
IO_TXM_STOP = 0x80

IO_TYM_OPMODE = 0x30
IO_TYM_CNTR1 = 0x40
IO_TYM_STOP = 0x80

IO_T123M_T2WCTRL = 0x04
IO_T123M_T2SRC = 0x08
IO_T123M_T3SRC = 0x10
IO_T123M_T1SRC = 0x20

IO_LM_DR = 0x03
IO_LM_PAGE0 = 0x04
IO_LM_ENABLE = 0x08
IO_LM_TYPEB = 0x10
IO_LM_CLKDIV = 0x60
IO_LM_CLKSRC = 0x80

IO_LC_LEVEL = 0x1F
IO_LC_ENABLE = 0x80

IO_CPUM_MODE = 0x03
IO_CPUM_SPAGE1 = 0x04
IO_CPUM_XCOHIGH = 0x08
IO_CPUM_XCENABLE = 0x10
IO_CPUM_MAINSTOP = 0x20
IO_CPUM_MAINDIV8 = 0x40
IO_CPUM_CLKLOW = 0x80

class M37520():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = PinTogglingSound(clock)

        self._rom_offset = ADDRESS_SPACE_SIZE - self._ROM.size()

        self._cycle_counter = 0

        self._pullup_ext = {
            **{"P0": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0},
            **mask['port_pullup']
        }

        self._port_input = {
            "P0": [0, 0],
            "P1": [0, 0],
            "P2": [0, 0],
            "P3": [0, 0],
            "P4": [0, 0]
        }
    
        self._instr_counter = 0
        self._timerX_counter = 0
        self._timerY_counter = 0
        self._timer1_counter = 0
        self._timer2_counter = 0
        self._timer3_counter = 0

        self._sub_clock_div = clock / SUB_CLOCK
        self._sub_timers_clock_div = self._sub_clock_div * 32

        self.reset()

        self._io_tbl = {
            0x00: (M37520._get_io_p0, M37520._set_io_p0),
            0x01: (M37520._get_io_p0d, M37520._set_io_p0d),
            0x02: (M37520._get_io_p1, M37520._set_io_p1),
            0x03: (M37520._get_io_p1d, M37520._set_io_p1d),
            0x04: (M37520._get_io_p2, M37520._set_io_p2),
            0x05: (M37520._get_io_p2d, M37520._set_io_p2d),
            0x06: (M37520._get_io_p3, M37520._set_io_p3),
            0x07: (M37520._get_io_p3d, M37520._set_io_p3d),
            0x08: (M37520._get_io_p4, M37520._set_io_p4),
            0x09: (M37520._get_io_p4d, M37520._set_io_p4d),

            0x0B: (M37520._get_io_pullp0, M37520._set_io_pullp0),
            0x0C: (M37520._get_io_pullp1, M37520._set_io_pullp1),
            0x0D: (M37520._get_io_pullp2, M37520._set_io_pullp2),
            0x0E: (M37520._get_io_pullp3, M37520._set_io_pullp3),
            0x0F: (M37520._get_io_pullp4, M37520._set_io_pullp4),

            0x20: (M37520._get_io_txl, M37520._set_io_txl),
            0x21: (M37520._get_io_txh, M37520._set_io_txh),
            0x22: (M37520._get_io_tyl, M37520._set_io_tyl),
            0x23: (M37520._get_io_tyh, M37520._set_io_tyh),
            0x24: (M37520._get_io_t1, M37520._set_io_t1),
            0x25: (M37520._get_io_t2, M37520._set_io_t2),
            0x26: (M37520._get_io_t3, M37520._set_io_t3),
            0x27: (M37520._get_io_txm, M37520._set_io_txm),
            0x28: (M37520._get_io_tym, M37520._set_io_tym),
            0x29: (M37520._get_io_t123m, M37520._set_io_t123m),

            0x35: (M37520._get_io_35, M37520._set_io_35),

            0x37: (M37520._get_io_lc, M37520._set_io_lc),

            0x39: (M37520._get_io_lm, M37520._set_io_lm),
            0x3A: (M37520._get_io_intedge, M37520._set_io_intedge),
            0x3B: (M37520._get_io_cpum, M37520._set_io_cpum),
            0x3C: (M37520._get_io_ireq1, M37520._set_io_ireq1),
            0x3D: (M37520._get_io_ireq2, M37520._set_io_ireq1),
            0x3E: (M37520._get_io_icon1, M37520._set_io_icon1),
            0x3F: (M37520._get_io_icon2, M37520._set_io_icon2)
        }

        self._execute = (
            (M37520._brk, 1),
            (M37520._ora_ind_x, 2),
            (M37520._jsr_zp_ind, 2),
            (M37520._bbs_bit_a, 2),
            (M37520._dummy, 1),
            (M37520._ora_zp, 2),
            (M37520._asl_zp, 2),
            (M37520._bbs_bit_zp, 3),
            (M37520._php, 1),
            (M37520._ora_imm, 2),
            (M37520._asl_a, 1),
            (M37520._seb_bit_a, 1),
            (M37520._dummy, 1),
            (M37520._ora_abs, 3),
            (M37520._asl_abs, 3),
            (M37520._seb_bit_zp, 2),
            (M37520._bpl, 2),
            (M37520._ora_ind_y, 2),
            (M37520._clt, 1),
            (M37520._bbc_bit_a, 2),
            (M37520._dummy, 1),
            (M37520._ora_zp_x, 2),
            (M37520._asl_zp_x, 2),
            (M37520._bbc_bit_zp, 3),
            (M37520._clc, 1),
            (M37520._ora_abs_y, 3),
            (M37520._dec_a, 1),
            (M37520._clb_bit_a, 1),
            (M37520._dummy, 1),
            (M37520._ora_abs_x, 3),
            (M37520._asl_abs_x, 3),
            (M37520._clb_bit_zp, 2),
            (M37520._jsr_abs, 3),
            (M37520._and_ind_x, 2),
            (M37520._jsr_sp, 2),
            (M37520._bbs_bit_a, 2),
            (M37520._bit_zp, 2),
            (M37520._and_zp, 2),
            (M37520._rol_zp, 2),
            (M37520._bbs_bit_zp, 3),
            (M37520._plp, 1),
            (M37520._and_imm, 2),
            (M37520._rol_a, 1),
            (M37520._seb_bit_a, 1),
            (M37520._bit_abs, 3),
            (M37520._and_abs, 3),
            (M37520._rol_abs, 3),
            (M37520._seb_bit_zp, 2),
            (M37520._bmi, 2),
            (M37520._and_ind_y, 2),
            (M37520._set, 1),
            (M37520._bbc_bit_a, 2),
            (M37520._dummy, 1),
            (M37520._and_zp_x, 2),
            (M37520._rol_zp_x, 2),
            (M37520._bbc_bit_zp, 3),
            (M37520._sec, 1),
            (M37520._and_abs_y, 3),
            (M37520._inc_a, 1),
            (M37520._clb_bit_a, 1),
            (M37520._ldm_zp, 3),
            (M37520._and_abs_x, 3),
            (M37520._rol_abs_x, 3),
            (M37520._clb_bit_zp, 2),
            (M37520._rti, 1),
            (M37520._eor_ind_x, 2),
            (M37520._stp, 1),
            (M37520._bbs_bit_a, 2),
            (M37520._com_zp, 2),
            (M37520._eor_zp, 2),
            (M37520._lsr_zp, 2),
            (M37520._bbs_bit_zp, 3),
            (M37520._pha, 1),
            (M37520._eor_imm, 2),
            (M37520._lsr_a, 1),
            (M37520._seb_bit_a, 1),
            (M37520._jmp_abs, 3),
            (M37520._eor_abs, 3),
            (M37520._lsr_abs, 3),
            (M37520._seb_bit_zp, 2),
            (M37520._bvc, 2),
            (M37520._eor_ind_y, 2),
            (M37520._dummy, 1),
            (M37520._bbc_bit_a, 2),
            (M37520._dummy, 1),
            (M37520._eor_zp_x, 2),
            (M37520._lsr_zp_x, 2),
            (M37520._bbc_bit_zp, 3),
            (M37520._cli, 1),
            (M37520._eor_abs_y, 3),
            (M37520._dummy, 1),
            (M37520._clb_bit_a, 1),
            (M37520._dummy, 1),
            (M37520._eor_abs_x, 3),
            (M37520._lsr_abs_x, 3),
            (M37520._clb_bit_zp, 2),
            (M37520._rts, 1),
            (M37520._adc_ind_x, 2),
            (M37520._mul_zp_x, 2),
            (M37520._bbs_bit_a, 2),
            (M37520._tst_zp, 2),
            (M37520._adc_zp, 2),
            (M37520._ror_zp, 2),
            (M37520._bbs_bit_zp, 3),
            (M37520._pla, 1),
            (M37520._adc_imm, 2),
            (M37520._ror_a, 1),
            (M37520._seb_bit_a, 1),
            (M37520._jmp_ind, 3),
            (M37520._adc_abs, 3),
            (M37520._ror_abs, 3),
            (M37520._seb_bit_zp, 2),
            (M37520._bvs, 2),
            (M37520._adc_ind_y, 2),
            (M37520._dummy, 1),
            (M37520._bbc_bit_a, 2),
            (M37520._dummy, 1),
            (M37520._adc_zp_x, 2),
            (M37520._ror_zp_x, 2),
            (M37520._bbc_bit_zp, 3),
            (M37520._sei, 1),
            (M37520._adc_abs_y, 3),
            (M37520._dummy, 1),
            (M37520._clb_bit_a, 1),
            (M37520._dummy, 1),
            (M37520._adc_abs_x, 3),
            (M37520._ror_abs_x, 3),
            (M37520._clb_bit_zp, 2),
            (M37520._bra, 2),
            (M37520._sta_ind_x, 2),
            (M37520._rrf_zp, 2),
            (M37520._bbs_bit_a, 2),
            (M37520._sty_zp, 2),
            (M37520._sta_zp, 2),
            (M37520._stx_zp, 2),
            (M37520._bbs_bit_zp, 3),
            (M37520._dey, 1),
            (M37520._dummy, 1),
            (M37520._txa, 1),
            (M37520._seb_bit_a, 1),
            (M37520._sty_abs, 3),
            (M37520._sta_abs, 3),
            (M37520._stx_abs, 3),
            (M37520._seb_bit_zp, 2),
            (M37520._bcc, 2),
            (M37520._sta_ind_y, 2),
            (M37520._dummy, 1),
            (M37520._bbc_bit_a, 2),
            (M37520._sty_zp_x, 2),
            (M37520._sta_zp_x, 2),
            (M37520._stx_zp_y, 2),
            (M37520._bbc_bit_zp, 3),
            (M37520._tya, 1),
            (M37520._sta_abs_y, 3),
            (M37520._txs, 1),
            (M37520._clb_bit_a, 1),
            (M37520._dummy, 1),
            (M37520._sta_abs_x, 3),
            (M37520._dummy, 1),
            (M37520._clb_bit_zp, 2),
            (M37520._ldy_imm, 2),
            (M37520._lda_ind_x, 2),
            (M37520._ldx_imm, 2),
            (M37520._bbs_bit_a, 2),
            (M37520._ldy_zp, 2),
            (M37520._lda_zp, 2),
            (M37520._ldx_zp, 2),
            (M37520._bbs_bit_zp, 3),
            (M37520._tay, 1),
            (M37520._lda_imm, 2),
            (M37520._tax, 1),
            (M37520._seb_bit_a, 1),
            (M37520._ldy_abs, 3),
            (M37520._lda_abs, 3),
            (M37520._ldx_abs, 3),
            (M37520._seb_bit_zp, 2),
            (M37520._bcs, 2),
            (M37520._lda_ind_y, 2),
            (M37520._jmp_zp_ind, 2),
            (M37520._bbc_bit_a, 2),
            (M37520._ldy_zp_x, 2),
            (M37520._lda_zp_x, 2),
            (M37520._ldx_zp_y, 2),
            (M37520._bbc_bit_zp, 3),
            (M37520._clv, 1),
            (M37520._lda_abs_y, 3),
            (M37520._tsx, 1),
            (M37520._clb_bit_a, 1),
            (M37520._ldy_abs_x, 3),
            (M37520._lda_abs_x, 3),
            (M37520._ldx_abs_y, 3),
            (M37520._clb_bit_zp, 2),
            (M37520._cpy_imm, 2),
            (M37520._cmp_ind_x, 2),
            (M37520._wit, 1),
            (M37520._bbs_bit_a, 2),
            (M37520._cpy_zp, 2),
            (M37520._cmp_zp, 2),
            (M37520._dec_zp, 2),
            (M37520._bbs_bit_zp, 3),
            (M37520._iny, 1),
            (M37520._cmp_imm, 2),
            (M37520._dex, 1),
            (M37520._seb_bit_a, 1),
            (M37520._cpy_abs, 3),
            (M37520._cmp_abs, 3),
            (M37520._dec_abs, 3),
            (M37520._seb_bit_zp, 2),
            (M37520._bne, 2),
            (M37520._cmp_ind_y, 2),
            (M37520._dummy, 1),
            (M37520._bbc_bit_a, 2),
            (M37520._dummy, 1),
            (M37520._cmp_zp_x, 2),
            (M37520._dec_zp_x, 2),
            (M37520._bbc_bit_zp, 3),
            (M37520._cld, 1),
            (M37520._cmp_abs_y, 3),
            (M37520._dummy, 1),
            (M37520._clb_bit_a, 1),
            (M37520._dummy, 1),
            (M37520._cmp_abs_x, 3),
            (M37520._dec_abs_x, 3),
            (M37520._clb_bit_zp, 2),
            (M37520._cpx_imm, 2),
            (M37520._sbc_ind_x, 2),
            (M37520._div_zp_x, 2),
            (M37520._bbs_bit_a, 2),
            (M37520._cpx_zp, 2),
            (M37520._sbc_zp, 2),
            (M37520._inc_zp, 2),
            (M37520._bbs_bit_zp, 3),
            (M37520._inx, 1),
            (M37520._sbc_imm, 2),
            (M37520._nop, 1),
            (M37520._seb_bit_a, 1),
            (M37520._cpx_abs, 3),
            (M37520._sbc_abs, 3),
            (M37520._inc_abs, 3),
            (M37520._seb_bit_zp, 2),
            (M37520._beq, 2),
            (M37520._sbc_ind_y, 2),
            (M37520._dummy, 1),
            (M37520._bbc_bit_a, 2),
            (M37520._dummy, 1),
            (M37520._sbc_zp_x, 2),
            (M37520._inc_zp_x, 2),
            (M37520._bbc_bit_zp, 3),
            (M37520._sed, 1),
            (M37520._sbc_abs_y, 3),
            (M37520._dummy, 1),
            (M37520._clb_bit_a, 1),
            (M37520._dummy, 1),
            (M37520._sbc_abs_x, 3),
            (M37520._inc_abs_x, 3),
            (M37520._clb_bit_zp, 2)
        )

    def examine(self):
        return {
            "PC": self._PC,
            "A": self._A,
            "X": self._X,
            "Y": self._Y,
            "SP": self._SPP | self._SP,
            "NF": self._NF,
            "VF": self._VF,
            "TF": self._TF,
            "BF": self._BF,
            "DF": self._DF,
            "IF": self._IF,
            "ZF": self._ZF,
            "CF": self._CF,
            "RAM": self._RAM,
            "LCDRAM": self._LCDRAM,
            "IORAM": [self._io_tbl[key][0](self) for key in self._io_tbl.keys()]
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] & 0xFFFF
        if ("A" in state):
            self._A = state["A"] & 0xFF
        if ("X" in state):
            self._X = state["X"] & 0xFF
        if ("Y" in state):
            self._Y = state["Y"] & 0xFF
        if ("SP" in state):
            self._SP = state["SP"] & 0xFF
        if ("NF" in state):
            self._NF = state["NF"]
        if ("VF" in state):
            self._VF = state["VF"]
        if ("TF" in state):
            self._TF = state["TF"]
        if ("BF" in state):
            self._BF = state["BF"]
        if ("DF" in state):
            self._DF = state["DF"]
        if ("IF" in state):
            self._IF = state["IF"]
        if ("ZF" in state):
            self._NF = state["ZF"]
        if ("CF" in state):
            self._NF = state["CF"]
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xFF
        if ("LCDRAM" in state):
            for i, value in state["LCDRAM"].items():
                self._LCDRAM[i] = value & 0xFF
        if ("IORAM" in state):
            for i, value in state["IORAM"].items():
                if i < len(self._io_tbl):
                    list(self._io_tbl.values())[i][1](self, value & 0xFF)

    def reset(self):
        self._PC = 0

        self._A = 0
        self._X = 0
        self._Y = 0
        
        self._set_ps(0x04)

        self._SP = 0
        self._SPP = 0x100

        self._nWAIT = 1
        self._nSTOP = 1

        self._RAM = [0] * RAM_SIZE
        self._LCDRAM = [0] * LCDRAM_SIZE

        self._LCDRAM_OFFSET = LCDRAM_OFFSET_B3

        self._PDIR = {
            "P0": 0,
            "P1": 0,
            "P2": 0,
            "P3": 0,
            "P4": 0
        }

        self._PULLUP = {
            "P0": 0,
            "P1": 0,
            "P2": 0,
            "P3": 0,
            "P4": 0
        }

        self._PLATCH = {
            "P0": 0,
            "P1": 0,
            "P2": 0,
            "P3": 0,
            "P4": 0
        }

        self._TX = self._TXLATCH = 0xFFFF
        self._TY = self._TYLATCH = 0xFFFF
        self._T1 = self._T1LATCH = 0xFF
        self._T2 = self._T2LATCH = 0x01
        self._T3 = self._T3LATCH = 0xFF

        self._TXM = 0
        self._TYM = 0
        self._T123M = 0

        self._LC = 0
        self._INTEDGE = 0
        self._IREQ1 = 0
        self._IREQ2 = 0
        self._ICON1 = 0
        self._ICON2 = 0

        self._set_io_lm(0x00)
        self._set_io_cpum(0x4C)

        self._go_vector(VADDR_RESET)
        
    def _go_vector(self, addr):
        vector_addr = (ADDRESS_SPACE_SIZE - addr) - self._rom_offset
        self._PC = self._ROM.getWordLSB(vector_addr) % ADDRESS_SPACE_SIZE

    def pc(self):
        return self._PC % ADDRESS_SPACE_SIZE
    
    def get_VRAM(self):
        if (self._LM & IO_LM_ENABLE):
            return tuple(self._LCDRAM)
        return ()

    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter

    def pin_set(self, port, pin, level):
        self._process_port_input(port, pin, level)

    def pin_release(self, port, pin):
        self._process_port_input(port, pin, -1)

    def _port_read(self, port):
        return (
            (self._PDIR[port] & self._PLATCH[port]) | 
            (~self._PDIR[port] & (~self._port_input[port][0] & 
            (self._port_input[port][1] | self._PULLUP[port] | self._pullup_ext[port])))
        )

    def _process_port_input(self, port, pin, level):
        if (port == 'RES'):
            if (level == 0):
                self.reset()
        else:
            prev_port = self._port_read(port)
            self._port_input[port][0] &= ~(1 << pin)
            self._port_input[port][1] &= ~(1 << pin)
            if (level >= 0):
                self._port_input[port][level] |= (1 << pin)
            if (prev_port != self._port_read(port)):
                if (port == "P2" and level == 0):
                    self._IREQ2 |= IO_IREQ2_KEYON
                elif (port == "P4"):
                    if (pin == 0 and bool(self._INTEDGE & IO_INTEDGE_INT0) == level):
                        self._IREQ1 |= IO_IREQ1_INT0
                    elif (pin == 1 and bool(self._INTEDGE & IO_INTEDGE_INT1) == level):
                        self._IREQ1 |= IO_IREQ1_INT1

    def _interrupt(self, addr):
        self._nWAIT = 1
        self._write_mem(self._SPP | self._SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SPP | self._SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SPP | self._SP, self._ps())
        self._SP = (self._SP - 1) & 0xFF
        self._IF = 1
        self._go_vector(addr)

    def _interrupt_process(self):
        if (self._IREQ1):
            for i in range(8):
                if (self._IREQ1 & self._ICON1 & (1 << i)):
                    self._IREQ1 &= ~(1 << i)
                    return self._interrupt(6 + (i << 1))
        if (self._IREQ2):
            for i in range(6):
                if (self._IREQ2 & self._ICON2 & (1 << i)):
                    self._IREQ2 &= ~(1 << i)
                    return self._interrupt(22 + (i << 1))

    def _timers_clock(self, exec_cycles):
        if (not self._TXM & IO_TXM_STOP):
            self._timerX_counter -= exec_cycles
            while (self._timerX_counter <= 0):
                self._timerX_counter += self._main_timers_clock_div
                self._TX -= 1
                if (self._TX < 0):
                    self._TX = self._TXLATCH
                    self._IREQ1 |= IO_IREQ1_TX

        if (not self._TYM & IO_TYM_STOP):
            self._timerY_counter -= exec_cycles
            while (self._timerY_counter <= 0):
                self._timerY_counter += self._main_timers_clock_div
                self._TY -= 1
                if (self._TY < 0):
                    self._TY = self._TYLATCH
                    self._IREQ1 |= IO_IREQ1_TY

        self._timer1_counter -= exec_cycles
        while (self._timer1_counter <= 0):
            if (self._T123M & IO_T123M_T1SRC):
                self._timer1_counter += self._sub_timers_clock_div
            else:
                self._timer1_counter += self._main_timers_clock_div
            self._T1 -= 1
            if (self._T1 < 0):
                self._T1 = self._T1LATCH
                self._IREQ2 |= IO_IREQ2_T1

        self._timer2_counter -= exec_cycles
        while (self._timer2_counter <= 0):
            if (self._T123M & IO_T123M_T2SRC):
                self._timer2_counter += self._main_timers_clock_div
            elif (self._T123M & IO_T123M_T1SRC):
                self._timer2_counter += self._sub_timers_clock_div * self._T1LATCH
            else:
                self._timer2_counter += self._main_timers_clock_div * self._T1LATCH
            self._T2 -= 1
            if (self._T2 < 0):
                self._T2 = self._T2LATCH
                self._IREQ1 |= IO_IREQ1_T2

        self._timer3_counter -= exec_cycles
        while (self._timer3_counter <= 0):
            if (self._T123M & IO_T123M_T3SRC):
                self._timer3_counter += self._sub_timers_clock_div
            elif (self._T123M & IO_T123M_T1SRC):
                self._timer3_counter += self._sub_timers_clock_div * self._T1LATCH
            else:
                self._timer3_counter += self._main_timers_clock_div * self._T1LATCH
            self._T3 -= 1
            if (self._T3 < 0):
                self._T3 = self._T3LATCH
                self._IREQ1 |= IO_IREQ1_T3

    def clock(self):
        exec_cycles = self._cpu_clock_div

        if (self._nSTOP):
            if (self._nWAIT):
                byte = self._ROM.getByte(self._PC - self._rom_offset)
                bytes_count = self._execute[byte][1]
                opcode = self._ROM.getBytes(self._PC - self._rom_offset, bytes_count)
                self._PC += bytes_count
                exec_cycles *= self._execute[byte][0](self, opcode)
                self._instr_counter += 1

            self._timers_clock(exec_cycles)

        if (not self._IF):
            self._interrupt_process()

        self._cycle_counter += exec_cycles
        return exec_cycles


    def _get_io_dummy(self):
        return 0
    
    def _set_io_dummy(self, value):
        pass

    def _get_io_p0(self):
        return self._port_read("P0")
    
    def _set_io_p0(self, value):
        self._PLATCH["P0"] = value

    def _get_io_p0d(self):
        return self._PDIR["P0"]
    
    def _set_io_p0d(self, value):
        self._PDIR["P0"] = value

    def _get_io_p1(self):
        return self._port_read("P1")

    def _set_io_p1(self, value):
        self._PLATCH["P1"] = value

    def _get_io_p1d(self):
        return self._PDIR["P1"]
    
    def _set_io_p1d(self, value):
        self._PDIR["P1"] = value

    def _get_io_p2(self):
        return self._port_read("P2")
    
    def _set_io_p2(self, value):
        self._PLATCH["P2"] = value

    def _get_io_p2d(self):
        return self._PDIR["P2"]
    
    def _set_io_p2d(self, value):
        self._PDIR["P2"] = value

    def _get_io_p3(self):
        return self._port_read("P3")
    
    def _set_io_p3(self, value):
        self._sound.toggle((value & 0x40 > 0), (value & 0x20 > 0), self._cycle_counter)
        self._PLATCH["P3"] = value

    def _get_io_p3d(self):
        return self._PDIR["P3"]
    
    def _set_io_p3d(self, value):
        self._PDIR["P3"] = value

    def _get_io_p4(self):
        return self._port_read("P4")
    
    def _set_io_p4(self, value):
        self._PLATCH["P4"] = value & 0xFE

    def _get_io_p4d(self):
        return self._PDIR["P4"]
    
    def _set_io_p4d(self, value):
        self._PDIR["P4"] = value & 0xFE

    def _get_io_pullp0(self):
        return self._PULLUP["P0"]
    
    def _set_io_pullp0(self, value):
        self._PULLUP["P0"] = value

    def _get_io_pullp1(self):
        return self._PULLUP["P1"]
    
    def _set_io_pullp1(self, value):
        self._PULLUP["P1"] = value

    def _get_io_pullp2(self):
        return self._PULLUP["P2"]
    
    def _set_io_pullp2(self, value):
        self._PULLUP["P2"] = value

    def _get_io_pullp3(self):
        return self._PULLUP["P3"]
    
    def _set_io_pullp3(self, value):
        self._PULLUP["P3"] = value

    def _get_io_pullp4(self):
        return self._PULLUP["P4"]
    
    def _set_io_pullp4(self, value):
        self._PULLUP["P4"] = value

    def _get_io_txl(self):
        return self._TX & 0xFF
    
    def _set_io_txl(self, value):
        self._TXLATCH = (self._TX & 0xFF00) | value
        if (not self._TXM & IO_TXM_WCTRL):
            self._TX = self._TXLATCH

    def _get_io_txh(self):
        return self._TX >> 8
    
    def _set_io_txh(self, value):
        self._TXLATCH = (self._TX & 0xFF) | (value << 8)
        if (not self._TXM & IO_TXM_WCTRL):
            self._TX = self._TXLATCH

    def _get_io_tyl(self):
        return self._TY & 0xFF
    
    def _set_io_tyl(self, value):
        self._TY = (self._TY & 0xFF00) | value
        self._TYLATCH = self._TY

    def _get_io_tyh(self):
        return self._TY >> 8
    
    def _set_io_tyh(self, value):
        self._TY = (self._TY & 0xFF) | (value << 8)
        self._TYLATCH = self._TY

    def _get_io_t1(self):
        return self._T1
    
    def _set_io_t1(self, value):
        self._T1 = value
        self._T1LATCH = value

    def _get_io_t2(self):
        return self._T2
    
    def _set_io_t2(self, value):
        if (not self._T123M & IO_T123M_T2WCTRL):
            self._T2 = value
        self._T2LATCH = value

    def _get_io_t3(self):
        return self._T3
    
    def _set_io_t3(self, value):
        self._T3 = value
        self._T3LATCH = value

    def _get_io_txm(self):
        return self._TXM
    
    def _set_io_txm(self, value):
        self._TXM = value

    def _get_io_tym(self):
        return self._TYM
    
    def _set_io_tym(self, value):
        self._TYM = value

    def _get_io_t123m(self):
        return self._T123M
    
    def _set_io_t123m(self, value):
        self._T123M = value

    def _get_io_35(self):
        return 0
    
    def _set_io_35(self, value):
        pass

    def _get_io_lc(self):
        return self._LC
    
    def _set_io_lc(self, value):
        self._LC = value

    def _get_io_lm(self):
        return self._LM
    
    def _set_io_lm(self, value):
        self._LM = value
        if (value & IO_LM_PAGE0):
            self._LCDRAM_OFFSET = LCDRAM_OFFSET_B0
        else:
            self._LCDRAM_OFFSET = LCDRAM_OFFSET_B3

    def _get_io_intedge(self):
        return self._INTEDGE
    
    def _set_io_intedge(self, value):
        self._INTEDGE = value

    def _get_io_cpum(self):
        return self._CPUM
    
    def _set_io_cpum(self, value):
        self._CPUM = value
        if (self._CPUM & IO_CPUM_CLKLOW):
            self._cpu_clock_div = self._sub_clock_div * 2
            self._main_timers_clock_div = self._sub_clock_div
        else:
            self._cpu_clock_div = 2
            self._main_timers_clock_div = 1
            if (self._CPUM & IO_CPUM_MAINDIV8):
                self._cpu_clock_div *= 4
        
        self._SPP = (self._CPUM & IO_CPUM_SPAGE1 > 0) << 8

    def _get_io_ireq1(self):
        return self._IREQ1

    def _set_io_ireq1(self, value):
        self._IREQ1 &= value

    def _get_io_ireq2(self):
        return self._IREQ2

    def _set_io_ireq2(self, value):
        self._IREQ2 &= value

    def _get_io_icon1(self):
        return self._ICON1
    
    def _set_io_icon1(self, value):
        self._ICON1 = value

    def _get_io_icon2(self):
        return self._ICON2
    
    def _set_io_icon2(self, value):
        self._ICON2 = value

    def _write_mem(self, addr, value):
        if ((addr >= self._LCDRAM_OFFSET) and (addr < LCDRAM_SIZE + self._LCDRAM_OFFSET)):
            self._LCDRAM[addr - self._LCDRAM_OFFSET] = value
        elif ((addr >= RAM_OFFSET) and (addr < RAM_SIZE + RAM_OFFSET)):
            self._RAM[addr - RAM_OFFSET] = value
        else:
            io = self._io_tbl.get(addr)
            if (io != None):
                io[1](self, value)

    def _read_mem(self, addr):
        if ((addr >= self._LCDRAM_OFFSET) and (addr < LCDRAM_SIZE + self._LCDRAM_OFFSET)):
            return self._LCDRAM[addr - self._LCDRAM_OFFSET]
        elif ((addr >= RAM_OFFSET) and (addr < RAM_SIZE + RAM_OFFSET)):
            return self._RAM[addr - RAM_OFFSET]
        elif (addr < SFR_SIZE):
            io = self._io_tbl.get(addr)
            if (io != None):
                return io[0](self)
        elif (addr >= self._rom_offset):
            return self._ROM.getByte(addr - self._rom_offset)
        return 0

    def _ps(self):
        return (
            (self._NF << 7) |
            (self._VF << 6) |
            (self._TF << 5) |
            (self._BF << 4) |
            (self._DF << 3) |
            (self._IF << 2) |
            (self._ZF << 1) |
            (self._CF)
        )

    def _set_ps(self, ps):
        self._NF = (ps >> 7)
        self._VF = (ps & 0x40 > 0)
        self._TF = (ps & 0x20 > 0)
        self._BF = (ps & 0x10 > 0)
        self._DF = (ps & 0x08 > 0)
        self._IF = (ps & 0x04 > 0)
        self._ZF = (ps & 0x02 > 0)
        self._CF = ps & 0x1

    def _adc(self, operand):
        if (self._TF):
            A = self._read_mem(self._X)
        else:
            A = self._A
        new_value = A + operand + self._CF

        if ((self._DF) and ((A & 0x0F) + (operand & 0x0F) + self._CF > 9)):
            new_value += 6

        self._VF = (~(A ^ operand) & (A ^ new_value)) >> 7
        self._NF = (new_value >> 7) & 0x1

        if ((self._DF) and (new_value > 0x99)):
            new_value += 0x60

        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 255

        if (self._TF):
            self._write_mem(self._X, new_value & 0xFF)
            return 3

        self._A = new_value & 0xFF
        return 0

    def _sbc(self, operand):
        if (self._TF):
            A = self._read_mem(self._X)
        else:
            A = self._A
        new_value = A - operand - (not self._CF)

        if (self._DF):
            if ((A & 0x0F) - (operand & 0x0F) - (not self._CF) < 0):
                new_value -= 6
            if (new_value < 0):
                new_value -= 0x60

        self._VF = ((A ^ operand) & (A ^ new_value)) >> 7
        self._NF = (new_value >> 7) & 0x1
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >= 0

        if (self._TF):
            self._write_mem(self._X, new_value & 0xFF)
            return 3

        self._A = new_value & 0xFF
        return 0

    def _ora(self, operand):
        if (self._TF):
            new_value = self._read_mem(self._X) | operand
            self._write_mem(self._X, new_value)
            self._NF = new_value >> 7
            self._ZF = not new_value
            return 3
        else:
            self._A |= operand
            self._NF = self._A >> 7
            self._ZF = not self._A
            return 0

    def _and(self, operand):
        if (self._TF):
            new_value = self._read_mem(self._X) & operand
            self._write_mem(self._X, new_value)
            self._NF = new_value >> 7
            self._ZF = not new_value
            return 3
        else:
            self._A &= operand
            self._NF = self._A >> 7
            self._ZF = not self._A
            return 0

    def _eor(self, operand):
        if (self._TF):
            new_value = self._read_mem(self._X) ^ operand
            self._write_mem(self._X, new_value)
            self._NF = new_value >> 7
            self._ZF = not new_value
            return 3
        else:
            self._A ^= operand
            self._NF = self._A >> 7
            self._ZF = not self._A
            return 0

    def _lda(self, operand):
        self._NF = operand >> 7
        self._ZF = not operand
        if (self._TF):
            self._write_mem(self._X, operand)
            return 2
        else:
            self._A = operand
            return 0

    def _cmp(self, operand):
        if (self._TF):
            test_value = self._read_mem(self._X) - operand
        else:
            test_value = self._A - operand
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return self._TF

    def _brk(self, opcode):
        self._BF = 1
        self._PC = (self._PC + 1) & 0xFFFF
        self._interrupt(VADDR_BRK)
        return 7

    def _ora_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        return 6 + self._ora(self._read_mem(addr))

    def _jsr_zp_ind(self, opcode):
        self._write_mem(self._SPP | self._SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SPP | self._SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._PC = self._read_mem(opcode & 0xFF)
        self._PC |= (self._read_mem((opcode + 1) & 0xFF) << 8)
        return 7

    def _bbs_bit_a(self, opcode):
        bit = (opcode >> 13) & 0x7 
        if (self._A & (0x1 << bit)):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 6
        return 4

    def _ora_zp(self, opcode):
        return 3 + self._ora(self._read_mem(opcode & 0xFF))

    def _asl_zp(self, opcode):
        new_value = self._read_mem(opcode & 0xFF) << 1
        self._write_mem(opcode & 0xFF, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 5

    def _bbs_bit_zp(self, opcode):
        bit = (opcode >> 21) & 0x7
        zp = (opcode >> 8) & 0xFF
        if (self._read_mem(zp) & (0x1 << bit)):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 7
        return 5

    def _php(self, opcode):
        self._write_mem(self._SPP | self._SP, self._ps())
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _ora_imm(self, opcode):
        return 2 + self._ora(opcode & 0xFF)

    def _asl_a(self, opcode):
        new_value = self._A << 1
        self._A = new_value & 0xFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 2

    def _seb_bit_a(self, opcode):
        bit = (opcode >> 5) & 0x7
        self._A = self._A | (0x1 << bit)
        return 2

    def _ora_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 4 + self._ora(self._read_mem(addr))

    def _asl_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        new_value = self._read_mem(addr) << 1
        self._write_mem(addr, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 6

    def _seb_bit_zp(self, opcode):
        bit = (opcode >> 13) & 0x7
        self._write_mem(opcode & 0xFF, self._read_mem(opcode & 0xFF) | (0x1 << bit))
        return 5

    def _bpl(self, opcode):
        if (not self._NF):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 4
        return 2

    def _ora_ind_y(self, opcode):
        addr = ((self._read_mem(opcode & 0xFF) | (self._read_mem((opcode + 1) & 0xFF) << 8)) + self._Y) & 0xFFFF
        return 6 + self._ora(self._read_mem(addr))

    def _clt(self, opcode):
        self._TF = 0
        return 2

    def _bbc_bit_a(self, opcode):
        bit = (opcode >> 13) & 0x7 
        if (not self._A & (0x1 << bit)):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 6
        return 4

    def _ora_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        return 3 + self._ora(self._read_mem(addr))

    def _asl_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        new_value = self._read_mem(addr) << 1
        self._write_mem(addr, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 6

    def _bbc_bit_zp(self, opcode):
        bit = (opcode >> 21) & 0x7
        zp = (opcode >> 8) & 0xFF
        if (not self._read_mem(zp) & (0x1 << bit)):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 7
        return 5

    def _clc(self, opcode):
        self._CF = 0
        return 2

    def _ora_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        return 5 + self._ora(self._read_mem(addr))

    def _dec_a(self, opcode):
        self._A = (self._A - 1) & 0xFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _clb_bit_a(self, opcode):
        bit = (opcode >> 5) & 0x7
        self._A &= ~(0x1 << bit)
        return 2

    def _ora_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        return 5 + self._ora(self._read_mem(addr))

    def _asl_abs_x(self, opcode): 
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        new_value = self._read_mem(addr) << 1
        self._write_mem(addr, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 7

    def _clb_bit_zp(self, opcode):
        bit = (opcode >> 13) & 0x7
        self._write_mem(opcode & 0xFF, self._read_mem(opcode & 0xFF) & ~(0x1 << bit))
        return 5

    def _jsr_abs(self, opcode):
        self._write_mem(self._SPP | self._SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SPP | self._SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._PC = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return 6

    def _and_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        return 6 + self._and(self._read_mem(addr))

    def _jsr_sp(self, opcode):
        self._write_mem(self._SPP | self._SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SPP | self._SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._PC = 0xFF00 | (opcode & 0xFF)
        return 5

    def _bit_zp(self, opcode):
        m = self._read_mem(opcode & 0xFF)
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 3

    def _and_zp(self, opcode):
        return 3 + self._and(self._read_mem(opcode & 0xFF))

    def _rol_zp(self, opcode):
        new_value = (self._read_mem(opcode & 0xFF) << 1) | self._CF
        self._write_mem(opcode & 0xFF, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 5

    def _plp(self, opcode):
        self._SP = (self._SP + 1) & 0xFF
        self._set_ps(self._read_mem(self._SPP | self._SP))
        return 4

    def _and_imm(self, opcode):
        return 2 + self._and(opcode)

    def _rol_a(self, opcode):
        new_value = (self._A << 1) | self._CF
        self._A = new_value & 0xFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 2

    def _bit_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        m = self._read_mem(addr)
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 4

    def _and_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 4 + self._and(self._read_mem(addr))

    def _rol_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        new_value = (self._read_mem(addr) << 1) | self._CF
        self._write_mem(addr, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 6

    def _bmi(self, opcode):
        if (self._NF):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 4
        return 2

    def _and_ind_y(self, opcode):
        addr = ((self._read_mem(opcode & 0xFF) | (self._read_mem((opcode + 1) & 0xFF) << 8)) + self._Y) & 0xFFFF
        return 6 + self._and(self._read_mem(addr))

    def _set(self, opcode):
        self._TF = 1
        return 2

    def _and_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        return 4 + self._and(self._read_mem(addr))

    def _rol_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        new_value = (self._read_mem(addr) << 1) | self._CF
        self._write_mem(addr, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 6

    def _sec(self, opcode):
        self._CF = 1
        return 2

    def _and_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        return 5 + self._and(self._read_mem(addr))

    def _inc_a(self, opcode):
        self._A = (self._A + 1) & 0xFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2


    def _ldm_zp(self, opcode):
        self._write_mem(opcode & 0xFF, (opcode >> 8) & 0xFF)
        return 4

    def _and_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        return 5 + self._and(self._read_mem(addr))

    def _rol_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        new_value = (self._read_mem(addr) << 1) | self._CF
        self._write_mem(addr, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 7

    def _rti(self, opcode):
        self._SP = (self._SP + 1) & 0xFF
        self._set_ps(self._read_mem(self._SPP | self._SP))
        self._SP = (self._SP + 1) & 0xFF
        self._PC = self._read_mem(self._SPP | self._SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SPP | self._SP) << 8
        return 6

    def _eor_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        return 6 + self._eor(self._read_mem(addr))

    def _stp(self, opcode):
        self._nSTOP = 0
        return 2

    def _com_zp(self, opcode):
        new_value = self._read_mem(opcode & 0xFF) ^ 0xFF
        self._write_mem(opcode & 0xFF, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _eor_zp(self, opcode):
        return 3 + self._eor(self._read_mem(opcode & 0xFF))

    def _lsr_zp(self, opcode):
        prev_value = self._read_mem(opcode & 0xFF)
        self._write_mem(opcode & 0xFF, prev_value >> 1)
        self._NF = 0
        self._ZF = prev_value <= 1
        self._CF = prev_value & 0x01
        return 5

    def _pha(self, opcode):
        self._write_mem(self._SPP | self._SP, self._A)
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _eor_imm(self, opcode):
        return 2 + self._eor(opcode & 0xFF)

    def _lsr_a(self, opcode):
        prev_value = self._A
        self._A >>= 1
        self._NF = 0
        self._ZF = prev_value <= 1
        self._CF = prev_value & 0x01
        return 2

    def _jmp_abs(self, opcode):
        self._PC = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 3

    def _eor_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 4 + self._eor(self._read_mem(addr))

    def _lsr_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        prev_value = self._read_mem(addr)
        self._write_mem(addr, prev_value >> 1)
        self._NF = 0
        self._ZF = prev_value <= 1
        self._CF = prev_value & 0x01
        return 6

    def _bvc(self, opcode):
        if (not self._VF):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 4
        return 2

    def _eor_ind_y(self, opcode):
        addr = ((self._read_mem(opcode & 0xFF) | (self._read_mem((opcode + 1) & 0xFF) << 8)) + self._Y) & 0xFFFF
        return 6 + self._eor(self._read_mem(addr))

    def _eor_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        return 4 + self._eor(self._read_mem(addr))

    def _lsr_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, prev_value >> 1)
        self._NF = 0
        self._ZF = prev_value <= 1
        self._CF = prev_value & 0x01
        return 6

    def _cli(self, opcode):
        self._IF = 0
        return 2

    def _eor_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        return 5 + self._eor(self._read_mem(addr))

    def _eor_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        return 5 + self._eor(self._read_mem(addr))

    def _lsr_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, prev_value >> 1)
        self._NF = 0
        self._ZF = prev_value <= 1
        self._CF = prev_value & 0x01
        return 7

    def _rts(self, opcode):
        self._SP = (self._SP + 1) & 0xFF
        self._PC = self._read_mem(self._SPP | self._SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SPP | self._SP) << 8
        return 6

    def _adc_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        return 6 + self._adc(self._read_mem(addr))

    def _mul_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        new_value = self._A * self._read_mem(addr)
        self._write_mem(self._SPP | self._SP, new_value >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._A = new_value & 0xFF
        return 15

    def _tst_zp(self, opcode):
        zp = self._read_mem(opcode & 0xFF)
        self._NF = zp >> 7
        self._ZF = not zp
        return 3

    def _adc_zp(self, opcode):
        return 3 + self._adc(self._read_mem(opcode & 0xFF))

    def _ror_zp(self, opcode):
        prev_value = self._read_mem(opcode & 0xFF)
        self._write_mem(opcode & 0xFF, (prev_value >> 1) | (self._CF << 7))
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 5

    def _pla(self, opcode):
        self._SP = (self._SP + 1) & 0xFF
        self._A = self._read_mem(self._SPP | self._SP)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _adc_imm(self, opcode):
        return 2 + self._adc(opcode & 0xFF)

    def _ror_a(self, opcode):
        prev_value = self._A
        self._A = (prev_value >> 1) | (self._CF << 7)
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 2

    def _jmp_ind(self, opcode):
        addr = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        self._PC = self._read_mem(addr)
        self._PC |= self._read_mem((addr + 1) & 0xFFFF) << 8
        return 5

    def _adc_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 4 + self._adc(self._read_mem(addr))

    def _ror_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        prev_value = self._read_mem(addr)
        self._write_mem(addr, (prev_value >> 1) | (self._CF << 7))
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 6

    def _bvs(self, opcode):
        if (self._VF):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 4
        return 2

    def _adc_ind_y(self, opcode):
        addr = ((self._read_mem(opcode & 0xFF) | (self._read_mem((opcode + 1) & 0xFF) << 8)) + self._Y) & 0xFFFF
        return 6 +self._adc(self._read_mem(addr))

    def _adc_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        return 4 + self._adc(self._read_mem(addr))

    def _ror_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, (prev_value >> 1) | (self._CF << 7))
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 6

    def _sei(self, opcode):
        self._IF = 1
        return 2

    def _adc_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        return 5 + self._adc(self._read_mem(addr))

    def _adc_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        return 5 + self._adc(self._read_mem(addr))

    def _ror_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, (prev_value >> 1) | (self._CF << 7))
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 7

    def _bra(self, opcode):
        self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
        return 4

    def _sta_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        self._write_mem(addr, self._A)
        return 7

    def _rrf_zp(self, opcode):
        value = self._read_mem(opcode & 0xFF)
        self._write_mem(opcode & 0xFF, ((value >> 4) | (value << 4)) & 0xFF)
        return 8

    def _sty_zp(self, opcode):
        self._write_mem(opcode & 0xFF, self._Y)
        return 4

    def _sta_zp(self, opcode):
        self._write_mem(opcode & 0xFF, self._A)
        return 4

    def _stx_zp(self, opcode):
        self._write_mem(opcode & 0xFF, self._X)
        return 4

    def _dey(self, opcode):
        self._Y = (self._Y - 1) & 0xFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 2

    def _txa(self, opcode):
        self._A = self._X
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _sty_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        self._write_mem(addr, self._Y)
        return 5

    def _sta_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        self._write_mem(addr, self._A)
        return 7

    def _stx_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        self._write_mem(addr, self._X)
        return 5

    def _bcc(self, opcode):
        if (not self._CF):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 4
        return 2

    def _sta_ind_y(self, opcode):
        addr = ((self._read_mem(opcode & 0xFF) | (self._read_mem((opcode + 1) & 0xFF) << 8)) + self._Y) & 0xFFFF
        self._write_mem(addr, self._A)
        return 7

    def _sty_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        self._write_mem(addr, self._Y)
        return 5

    def _sta_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        self._write_mem(addr, self._A)
        return 5

    def _stx_zp_y(self, opcode):
        addr = (opcode + self._Y) & 0xFF
        self._write_mem(addr, self._X)
        return 5

    def _tya(self, opcode):
        self._A = self._Y
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _sta_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        self._write_mem(addr, self._A)
        return 6

    def _txs(self, opcode):
        self._SP = self._X
        return 2

    def _sta_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        self._write_mem(addr, self._A)
        return 6

    def _ldy_imm(self, opcode):
        self._Y = opcode & 0xFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 2

    def _lda_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        return 6 + self._lda(self._read_mem(addr))

    def _ldx_imm(self, opcode):
        self._X = opcode & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _ldy_zp(self, opcode):
        self._Y = self._read_mem(opcode & 0xFF)
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 3

    def _lda_zp(self, opcode):
        return 3 + self._lda(self._read_mem(opcode & 0xFF))

    def _ldx_zp(self, opcode):
        self._X = self._read_mem(opcode & 0xFF)
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 3

    def _tay(self, opcode):
        self._Y = self._A
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 2

    def _lda_imm(self, opcode):
        return 2 + self._lda(opcode & 0xFF)

    def _tax(self, opcode):
        self._X = self._A
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _ldy_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        self._Y = self._read_mem(addr)
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 4

    def _lda_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 4 + self._lda(self._read_mem(addr))

    def _ldx_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        self._X = self._read_mem(addr)
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 4

    def _bcs(self, opcode):
        if (self._CF):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 4
        return 2

    def _lda_ind_y(self, opcode):
        addr = ((self._read_mem(opcode & 0xFF) | (self._read_mem((opcode + 1) & 0xFF) << 8)) + self._Y) & 0xFFFF
        return 6 + self._lda(self._read_mem(addr))

    def _jmp_zp_ind(self, opcode):
        self._PC = self._read_mem(opcode & 0xFF)
        self._PC |= self._read_mem((opcode + 1) & 0xFF) << 8
        return 4

    def _ldy_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        self._Y = self._read_mem(addr)
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 4

    def _lda_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        return 4 + self._lda(self._read_mem(addr))

    def _ldx_zp_y(self, opcode):
        addr = (opcode + self._Y) & 0xFF
        self._X = self._read_mem(addr)
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 4

    def _clv(self, opcode):
        self._VF = 0
        return 2

    def _lda_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        return 5 + self._lda(self._read_mem(addr))

    def _tsx(self, opcode):
        self._X = self._SP
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _ldy_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        self._Y = self._read_mem(addr)
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 5

    def _lda_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        return 5 + self._lda(self._read_mem(addr))

    def _ldx_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        self._X = self._read_mem(addr)
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 5

    def _cpy_imm(self, opcode):
        test_value = self._Y - (opcode & 0xFF) 
        self._NF = test_value >> 7
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _cmp_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        return 6 + self._cmp(self._read_mem(addr))

    def _wit(self, opcode):
        self._nWAIT = 0
        return 2

    def _cpy_zp(self, opcode):
        test_value = self._Y - self._read_mem(opcode & 0xFF)
        self._NF = test_value >> 7
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3

    def _cmp_zp(self, opcode):
        return 3 + self._cmp(self._read_mem(opcode & 0xFF))

    def _dec_zp(self, opcode):
        new_value = (self._read_mem(opcode & 0xFF) - 1) & 0xFF
        self._write_mem(opcode & 0xFF, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _iny(self, opcode):
        self._Y = (self._Y + 1) & 0xFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 2

    def _cmp_imm(self, opcode):
        return 2 + self._cmp(opcode & 0xFF)

    def _dex(self, opcode):
        self._X = (self._X - 1) & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _cpy_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        test_value = self._Y - self._read_mem(addr)
        self._NF = test_value >> 7
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4

    def _cmp_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 4 + self._cmp(self._read_mem(addr))

    def _dec_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        new_value = (self._read_mem(addr) - 1) & 0xFF
        self._write_mem(addr, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _bne(self, opcode):
        if (not self._ZF):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 4
        return 2

    def _cmp_ind_y(self, opcode):
        addr = ((self._read_mem(opcode & 0xFF) | (self._read_mem((opcode + 1) & 0xFF) << 8)) + self._Y) & 0xFFFF
        return 6 + self._cmp(self._read_mem(addr))

    def _cmp_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        return 4 + self._cmp(self._read_mem(addr))

    def _dec_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        new_value = (self._read_mem(addr) - 1) & 0xFF
        self._write_mem(addr, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _cld(self, opcode):
        self._DF = 0
        return 2

    def _cmp_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        return 5 + self._cmp(self._read_mem(addr))

    def _cmp_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        return 5 + self._cmp(self._read_mem(addr))

    def _dec_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        new_value = (self._read_mem(addr) - 1) & 0xFF
        self._write_mem(addr, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 7

    def _cpx_imm(self, opcode):
        test_value = self._X - (opcode & 0xFF)
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _sbc_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        return 6 + self._sbc(self._read_mem(addr))

    def _div_zp_x(self, opcode):
        dividend = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        if (self._A):
            self._write_mem(self._SPP | self._SP, dividend % self._A)
            self._SP = (self._SP - 1) & 0xFF
            self._A = dividend // self._A
        return 16

    def _cpx_zp(self, opcode):
        test_value = self._X - self._read_mem(opcode & 0xFF)
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3

    def _sbc_zp(self, opcode):
        return 3 + self._sbc(self._read_mem(opcode & 0xFF))

    def _inc_zp(self, opcode):
        new_value = (self._read_mem(opcode & 0xFF) + 1) & 0xFF
        self._write_mem(opcode & 0xFF, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _inx(self, opcode):
        self._X = (self._X + 1) & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _sbc_imm(self, opcode):
        return 2 + self._sbc(opcode & 0xFF)

    def _nop(self, opcode):
        return 2

    def _cpx_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        test_value = self._X - self._read_mem(addr)
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4

    def _sbc_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 4 + self._sbc(self._read_mem(addr))

    def _inc_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        new_value = (self._read_mem(addr) + 1) & 0xFF
        self._write_mem(addr, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _beq(self, opcode):
        if (self._ZF == 1):
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 4
        return 2

    def _sbc_ind_y(self, opcode):
        addr = ((self._read_mem(opcode & 0xFF) | (self._read_mem((opcode + 1) & 0xFF) << 8)) + self._Y) & 0xFFFF
        return 6 + self._sbc(self._read_mem(addr))

    def _sbc_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        return 4 + self._sbc(self._read_mem(addr))

    def _inc_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        new_value = (self._read_mem(addr) + 1) & 0xFF
        self._write_mem(addr, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _sed(self, opcode):
        self._DF = 1
        return 2

    def _sbc_abs_y(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._Y) & 0xFFFF
        return 5 + self._sbc(self._read_mem(addr))

    def _sbc_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        return 5 + self._sbc(self._read_mem(addr))

    def _inc_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        new_value = (self._read_mem(addr) + 1) & 0xFF
        self._write_mem(addr, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 7

    def _dummy(self, opcode):
        return 2
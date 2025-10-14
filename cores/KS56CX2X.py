from .rom import ROM
from .PinTogglingSound import PinTogglingSound

SUB_CLOCK = 32768

RAM_SIZE = 0x1000
VRAM_OFFSET = 0x100
VRAM_SIZE = 256
IORAM_OFFSET = 0xF80
IORAM_SIZE = 128

EMPTY_VRAM = tuple([0] * VRAM_SIZE)
FULL_VRAM = tuple([1] * VRAM_SIZE)

BASIC_TIMER_DIV = [1 << 12, 1 << 12, 1 << 9, 1 << 9, 1 << 7, 1 << 7, 1 << 5]
WATCH_TIMER_DIV = [1 << 14, 1 << 7]
TIMER_T0_DIV = [0, 0, 0, 0, 1 << 10, 1 << 8, 1 << 6, 1 << 4]
MAIN_CLOCK_DIV = [64, 16, 8, 4]
WATCH_TIMER_MAIN_CLOCK_DIV = 128

PCC_MODE_NORMAL = 0
PCC_MODE_HALT = 1
PCC_MODE_STOP = 2

RPE_XA = 0
RPE_XAE = 1
RPE_HL = 2
RPE_HLE = 3
RPE_DE = 4
RPE_DEE = 5
RPE_BC = 6
RPE_BCE = 7

REG_A = 0
REG_X = 1
REG_L = 2
REG_H = 3
REG_E = 4
REG_D = 5
REG_C = 6
REG_B = 7

VRQ_INTBT = 1
VRQ_INT4 = 1 
VRQ_INT0 = 2
VRQ_INT1 = 3
VRQ_INTCSI = 4
VRQ_INTT0 = 5

IOM_INTA_IRQBT = 0x1
IOM_INTA_IEBT = 0x2
IOM_INTA_IRQ4 = 0x4
IOM_INTA_IE4 = 0x8
IOM_INTC_IRQW = 0x1
IOM_INTC_IEW = 0x2
IOM_INTE_IRQT0 = 0x1
IOM_INTE_IET0 = 0x2
IOM_INTE_IRQT1 = 0x4
IOM_INTE_IET1 = 0x8
IOM_INTF_IRQCSI = 0x1
IOM_INTF_IECSI = 0x2
IOM_INTF_IRQT2 = 0x4
IOM_INTF_IET2 = 0x8
IOM_INTG_IRQ0 = 0x1
IOM_INTG_IE0 = 0x2
IOM_INTG_IRQ1 = 0x4
IOM_INTG_IE1 = 0x8
IOM_INTH_IRQ2 = 0x1
IOM_INTH_IE2 = 0x2

IOM_TM0h_CP = 0x7
IOM_TM0l_START = 0x8
IOM_TM0l_OPERATION = 0x4

PORT_MODE_INPUT = 0
PORT_MODE_OUTPUT = 1

M_SCC_SUB_CLOCK = 0x1
M_SCC_MAIN_CLOCK_STOP = 0x8
M_WMl_SUB_CLOCK = 0x1
M_WMl_WATCH_ENABLE = 0x4
M_WMl_WATCH_FAST_MODE = 0x2
M_TM0l_COUNT = 0x4
M_IM0_FALLING_EDGE = 0x1
M_IM0_ANY_EDGE = 0x2
M_IM0_IGNORED = 0x3
M_IM0_NOISE_ELIM_DISABLE = 0x4
M_IM2_KR2KR3 = 2
M_IM2_KR0TOKR3 = 3

class KS56CX2X():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = PinTogglingSound(clock)

        self._instr_counter = 0
        self._basic_timer_counter = 0
        self._T0_timer_counter = 0
        self._watch_timer_counter = 0

        self._timerWatch_counter = 0
        self._sub_clock_div = clock / SUB_CLOCK
        self._cpu_clock_div = MAIN_CLOCK_DIV[0]

        self._cycle_counter = 0
        
        self._reset()

        self._io_tbl = {
            0xF80: (KS56CX2X._get_io_spl, KS56CX2X._set_io_spl),
            0xF81: (KS56CX2X._get_io_sph, KS56CX2X._set_io_sph),
            0xF82: (KS56CX2X._get_io_rbs, KS56CX2X._set_io_dummy),
            0xF83: (KS56CX2X._get_io_mbs, KS56CX2X._set_io_dummy),
            0xF84: (KS56CX2X._get_io_sbs, KS56CX2X._set_io_sbs),
            0xF85: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_btm),
            0xF86: (KS56CX2X._get_io_btl, KS56CX2X._set_io_dummy),
            0xF87: (KS56CX2X._get_io_bth, KS56CX2X._set_io_dummy),
            0xF88: (KS56CX2X._get_io_tmod2hl, KS56CX2X._set_io_tmod2hl),
            0xF89: (KS56CX2X._get_io_tmod2hh, KS56CX2X._set_io_tmod2hh),
            0xF8B: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_wdtm),
            0xF8C: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF8D: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF8E: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF8F: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF90: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF91: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF92: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF93: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF94: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF95: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF96: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF97: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xF98: (KS56CX2X._get_io_wml, KS56CX2X._set_io_wml), #to-do
            0xF99: (KS56CX2X._get_io_wmh, KS56CX2X._set_io_wmh), #to-do

            0xFA0: (KS56CX2X._get_io_tm0l, KS56CX2X._set_io_tm0l),
            0xFA1: (KS56CX2X._get_io_tm0h, KS56CX2X._set_io_tm0h),
            0xFA2: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFA4: (KS56CX2X._get_io_t0l, KS56CX2X._set_io_dummy),
            0xFA5: (KS56CX2X._get_io_t0h, KS56CX2X._set_io_dummy),
            0xFA6: (KS56CX2X._get_io_tmod0l, KS56CX2X._set_io_tmod0l),
            0xFA7: (KS56CX2X._get_io_tmod0h, KS56CX2X._set_io_tmod0h),
            0xFA8: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFA9: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFAA: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFAC: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFAD: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFAE: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFAF: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do

            0xFB0: (KS56CX2X._get_io_pswl, KS56CX2X._set_io_pswl),
            0xFB1: (KS56CX2X._get_io_pswh, KS56CX2X._set_io_pswh),
            0xFB2: (KS56CX2X._get_io_ips, KS56CX2X._set_io_ips),
            0xFB3: (KS56CX2X._get_io_pcc, KS56CX2X._set_io_pcc),
            0xFB4: (KS56CX2X._get_io_im0, KS56CX2X._set_io_im0), #to-do
            0xFB5: (KS56CX2X._get_io_im1, KS56CX2X._set_io_im1), #to-do
            0xFB6: (KS56CX2X._get_io_im2, KS56CX2X._set_io_im2), #to-do
            0xFB7: (KS56CX2X._get_io_scc, KS56CX2X._set_io_scc), #to-do
            0xFB8: (KS56CX2X._get_io_inta, KS56CX2X._set_io_inta),
            0xFBA: (KS56CX2X._get_io_intc, KS56CX2X._set_io_intc),
            0xFBC: (KS56CX2X._get_io_inte, KS56CX2X._set_io_inte),
            0xFBD: (KS56CX2X._get_io_intf, KS56CX2X._set_io_intf),
            0xFBE: (KS56CX2X._get_io_intg, KS56CX2X._set_io_intg),
            0xFBF: (KS56CX2X._get_io_inth, KS56CX2X._set_io_inth),

            0xFC0: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFC1: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFC2: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFC3: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFCF: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do

            0xFD0: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFDC: (KS56CX2X._get_io_pogal, KS56CX2X._set_io_pogal),
            0xFDD: (KS56CX2X._get_io_pogah, KS56CX2X._set_io_pogah),
            0xFDE: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFDF: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do

            0xFE0: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFE1: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFE2: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFE3: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFE4: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFE5: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFE6: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFE7: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFE8: (KS56CX2X._get_io_pmgal, KS56CX2X._set_io_pmgal),
            0xFE9: (KS56CX2X._get_io_pmgah, KS56CX2X._set_io_pmgah),
            0xFEC: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFED: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFEE: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            0xFEF: (KS56CX2X._get_io_dummy, KS56CX2X._set_io_dummy), #to-do
            
            0xFF0: (KS56CX2X._get_io_port0, KS56CX2X._set_io_dummy),
            0xFF1: (KS56CX2X._get_io_port1, KS56CX2X._set_io_dummy),
            0xFF2: (KS56CX2X._get_io_port2, KS56CX2X._set_io_port2),
            0xFF3: (KS56CX2X._get_io_port3, KS56CX2X._set_io_port3),
            0xFF5: (KS56CX2X._get_io_port5, KS56CX2X._set_io_port5),
            0xFF6: (KS56CX2X._get_io_port6, KS56CX2X._set_io_port6),
            0xFF8: (KS56CX2X._get_io_port8, KS56CX2X._set_io_port8),
            0xFF9: (KS56CX2X._get_io_port9, KS56CX2X._set_io_port9),
        }

        self._execute = (
            *([(KS56CX2X._br_raddr, 1)] * 16),             #0000 A3 A2 A1 A0
            *([(KS56CX2X._geti_taddr, 1)] * 48),           #00 T5 T4 T3 T2 T1 T0
            *([(KS56CX2X._callf_faddr, 2)] * 8),           #01000 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
            (KS56CX2X._pop_rp, 1),                         #01001000
            (KS56CX2X._push_rp, 1),                        #01001001
            (KS56CX2X._pop_rp, 1),                         #01001010
            (KS56CX2X._push_rp, 1),                        #01001011
            (KS56CX2X._pop_rp, 1),                         #01001100
            (KS56CX2X._push_rp, 1),                        #01001101
            (KS56CX2X._pop_rp, 1),                         #01001110
            (KS56CX2X._push_rp, 1),                        #01001111
            *([(KS56CX2X._brcb_caddr, 2)] * 16),           #0101 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
            #KS56CX2X._nop,                                #01100000
            *([(KS56CX2X._adds_a_n4, 1)] * 16),            #0110 I3 I2 I1 I0
            *([(KS56CX2X._mov_a_n4, 1)] * 16),             #0111 I3 I2 I1 I0
            (KS56CX2X._ske_a_ahl, 1),                      #10000000
            (KS56CX2X._dummy, 1),
            (KS56CX2X._incs_mem, 2),                       #10000010 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._dummy, 1),
            (KS56CX2X._clr1_mem_bit, 2),                   #10000100 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._set1_mem_bit, 2),                   #10000101 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._skf_mem_bit, 2),                    #10000110 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._skt_mem_bit, 2),                    #10000111 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._dummy, 1),
            (KS56CX2X._mov_xa_n8, 2),                      #10001001 | I7 I6 I5 I4 I3 I2 I1 I0
            (KS56CX2X._incs_rp1, 1),                       #10001010
            (KS56CX2X._mov_hl_n8, 2),                      #10001011 | I7 I6 I5 I4 I3 I2 I1 I0
            (KS56CX2X._incs_rp1, 1),                       #10001100
            (KS56CX2X._mov_de_n8, 2),                      #10001101 | I7 I6 I5 I4 I3 I2 I1 I0
            (KS56CX2X._incs_rp1, 1),                       #10001110
            (KS56CX2X._mov_bc_n8, 2),                      #10001111 | I7 I6 I5 I4 I3 I2 I1 I0
            (KS56CX2X._and_a_ahl, 1),                      #10010000
            (KS56CX2X._dummy, 1),
            #KS56CX2X._out_portn_xa,                       #10010010 | 1111 N3 N2 N1 N0
            (KS56CX2X._mov_mem_xa, 2),                     #10010010 | D7 D6 D5 D4 D3 D2 D1 0
            #KS56CX2X._out_portn_a,                        #10010011 | 1111 N3 N2 N1 N0
            (KS56CX2X._mov_mem_A, 2),                      #10010011 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._clr1_mem_bit, 2),                   #10010100 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._set1_mem_bit, 2),                   #10010101 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._skf_mem_bit, 2),                    #10010110 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._skt_mem_bit, 2),                    #10010111 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._rorc_a, 1),                         #10011000
            (KS56CX2X._execute_10011001, 2),               #10011001
            (KS56CX2X._execute_10011010, 2),               #10011010
            (KS56CX2X._execute_10011011, 2),               #10011011
            (KS56CX2X._execute_10011100, 2),               #10011100
            (KS56CX2X._execute_10011101, 2),               #10011101
            (KS56CX2X._dummy, 1),
            (KS56CX2X._execute_10011111, 2),               #10011111
            (KS56CX2X._or_a_ahl, 1),                       #10100000
            (KS56CX2X._dummy, 1),
            #KS56CX2X._in_xa,portn,                        #10100010 | 1111 N3 N2 N1 N0
            (KS56CX2X._mov_xa_mem, 2),                     #10100010 | D7 D6 D5 D4 D3 D2 D1 0
            #KS56CX2X._in_a_portn,                         #10100011 | 1111 N3 N2 N1 N0
            (KS56CX2X._mov_a_mem, 2),                      #10100011 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._clr1_mem_bit, 2),                   #10100100 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._set1_mem_bit, 2),                   #10100101 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._skf_mem_bit, 2),                    #10100110 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._skt_mem_bit, 2),                    #10100111 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._subs_a_ahl, 1),                     #10101000
            (KS56CX2X._addc_a_ahl, 1),                     #10101001
            (KS56CX2X._execute_10101010, 2),               #10101010
            (KS56CX2X._execute_10101011, 3),               #10101011
            (KS56CX2X._execute_10101100, 2),               #10101100
            (KS56CX2X._dummy, 1),
            (KS56CX2X._execute_10101110, 2),               #10101110
            (KS56CX2X._dummy, 1),
            (KS56CX2X._xor_a_ahl, 1),                      #10110000
            (KS56CX2X._dummy, 1),
            (KS56CX2X._xch_xa_mem, 2),                     #10110010 | D7 D6 D5 D4 D3 D2 D1 0
            (KS56CX2X._xch_a_mem, 2),                      #10110011 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._clr1_mem_bit, 2),                   #10110100 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._set1_mem_bit, 2),                   #10110101 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._skf_mem_bit, 2),                    #10110110 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._skt_mem_bit, 2),                    #10110111 | D7 D6 D5 D4 D3 D2 D1 D0
            (KS56CX2X._subc_a_ahl, 1),                     #10111000
            (KS56CX2X._adds_xa_n8, 2),                     #10111001 | I7 I6 I5 I4 I3 I2 I1 I0
            (KS56CX2X._dummy, 1),
            (KS56CX2X._dummy, 1),
            (KS56CX2X._execute_10111100, 2),               #10111100
            (KS56CX2X._execute_10111101, 2),               #10111101
            (KS56CX2X._execute_10111110, 2),               #10111110
            (KS56CX2X._execute_10111111, 2),               #10111111
            *([(KS56CX2X._incs_reg, 1)] * 8),              #11000 R2 R1 R0
            *([(KS56CX2X._decs_reg, 1)] * 8),              #11001 R2 R1 R0
            (KS56CX2X._movt_xa_pcxa, 1),                   #11010000
            (KS56CX2X._movt_xa_bcxa, 1),                   #11010001
            (KS56CX2X._adds_a_ahl, 1),                     #11010010
            (KS56CX2X._dummy, 1),
            (KS56CX2X._movt_xa_pcde, 1),                   #11010100
            (KS56CX2X._movt_xa_bcde, 1),                   #11010101
            (KS56CX2X._not1_cy, 1),                        #11010110
            (KS56CX2X._skt_cy, 1),                         #11010111
            *([(KS56CX2X._xch_a_reg1, 1)] * 8),            #11011 R2 R1 R0
            (KS56CX2X._rets, 1),                           #11100000
            (KS56CX2X._mov_a_ahl, 1),                      #11100001
            (KS56CX2X._mov_a_ahli, 1),                     #11100010
            (KS56CX2X._mov_a_ahld, 1),                     #11100011
            (KS56CX2X._mov_a_ade, 1),                      #11100100
            (KS56CX2X._mov_a_adl, 1),                      #11100101
            (KS56CX2X._clr1_cy, 1),                        #11100110
            (KS56CX2X._set1_cy, 1),                        #11100111
            (KS56CX2X._mov_ahl_a, 1),                      #11101000
            (KS56CX2X._xch_a_ahl, 1),                      #11101001
            (KS56CX2X._xch_a_ahli, 1),                     #11101010
            (KS56CX2X._xch_a_ahld, 1),                     #11101011
            (KS56CX2X._xch_a_ade, 1),                      #11101100
            (KS56CX2X._xch_a_adl, 1),                      #11101101
            (KS56CX2X._ret, 1),                            #11101110
            (KS56CX2X._reti, 1),                           #11101111
            *([(KS56CX2X._br_mraddr, 1)] * 16)             #1111 S3 S2 S1 S0
        )

        self._execute_10011001 = (
            KS56CX2X._br_pcxa,                             #10011001 | 00000000
            KS56CX2X._br_bcxa,                             #10011001 | 00000001
            KS56CX2X._incs_ahl,                            #10011001 | 00000010
            KS56CX2X._dummy,
            KS56CX2X._br_pcde,                             #10011001 | 00000100
            KS56CX2X._br_bcde,                             #10011001 | 00000101
            KS56CX2X._pop_bs,                              #10011001 | 00000110
            KS56CX2X._push_bs,                             #10011001 | 00000111
            *([KS56CX2X._ske_a_reg] * 8),                  #10011001 | 00001 R2 R1 R0
            *([KS56CX2X._sel_mbn] * 16),                   #10011001 | 0001 N3 N2 N1 N0
            *([KS56CX2X._sel_rbn] * 4),                    #10011001 | 001000 N1 N0
            *([KS56CX2X._dummy] * 12),
            *([KS56CX2X._and_a_n4] * 16),                  #10011001 | 0011 I3 I2 I1 I0
            *([KS56CX2X._or_a_n4] * 16),                   #10011001 | 0100 I3 I2 I1 I0
            #KS56CX2X._not_a,                              #10011001 | 01011111
            *([KS56CX2X._xor_a_n4] * 16),                  #10011001 | 0101 I3 I2 I1 I0
            *([KS56CX2X._ske_ahl_n4] * 16),                #10011001 | 0110 I3 I2 I1 I0
            *([KS56CX2X._mov_reg1_A] * 8),                 #10011001 | 01110 R2 R1 R0
            *([KS56CX2X._mov_a_reg] * 8)                   #10011001 | 01111 R2 R1 R0
        )

        self._execute_10101011 = (
            KS56CX2X._br_addr,                             #10101011 | 00 A13 A12 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
            KS56CX2X._call_addr                            #10101011 | 01 A13 A12 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        )

        self._execute_10011010 = (
            KS56CX2X._ske_reg_n4,                          #10011010 | I3 I2 I1 I0 0 R2 R1 R0
            KS56CX2X._mov_reg1_n4                          #10011010 | I3 I2 I1 I0 1 R2 R1 R0
        )

        self._execute_10011011 = (
            KS56CX2X._mov1_hmembit_cy,                     #10011011 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._mov1_pmeml_cy,                       #10011011 | 0100 G3 G2 G1 G0
            KS56CX2X._mov1_fmembit_cy,                     #10011011 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._mov1_fmembit_cy                      #10011011 | 11 B1 B0 F3 F2 F1 F0
        )

        self._execute_10011100 = (
            KS56CX2X._clr1_hmembit,                        #10011100 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._clr1_pmeml,                          #10011100 | 0100 G3 G2 G1 G0
            #KS56CX2X._di,                                 #10011100 | 10110010
            #KS56CX2X._di_iexxx,                           #10011100 | 10 N5 1 1 N2 N1 N0
            KS56CX2X._clr1_fmembit,                        #10011100 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._clr1_fmembit                         #10011100 | 11 B1 B0 F3 F2 F1 F0
        )
        
        self._execute_10011101 = (
            KS56CX2X._set1_hmembit,                        #10011101 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._set1_pmeml,                          #10011101 | 0100 G3 G2 G1 G0
            #KS56CX2X._ei,                                 #10011101 | 10110010
            #KS56CX2X._ei_iexxx,                           #10011101 | 10 N5 1 1 N2 N1 N0
            #KS56CX2X._halt,                               #10011101 | 10100011
            #KS56CX2X._stop                                #10011101 | 10110011
            KS56CX2X._set1_fmembit,                        #10011101 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._set1_fmembit                         #10011101 | 11 B1 B0 F3 F2 F1 F0
        )

        self._execute_10011111 = (
            KS56CX2X._sktclr_hmembit,                      #10011111 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._sktclr_pmeml,                        #10011111 | 0100 G3 G2 G1 G0
            KS56CX2X._sktclr_fmembit,                      #10011111 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._sktclr_fmembit                       #10011111 | 11 B1 B0 F3 F2 F1 F0
        )

        self._execute_10101010 = (
            *([KS56CX2X._dummy] * 16),
            KS56CX2X._mov_ahl_xa,                           #10101010 | 00010000
            KS56CX2X._xch_xa_ahl,                           #10101010 | 00010001
            *([KS56CX2X._dummy] * 6),
            KS56CX2X._mov_xa_ahl,                           #10101010 | 00011000
            KS56CX2X._ske_xa_ahl,                           #10101010 | 00011001
            *([KS56CX2X._dummy] * 38),
            *([KS56CX2X._xch_xa_rpe] * 8),                 #10101010 | 01000 P2 P1 P0
            *([KS56CX2X._ske_xa_rpe] * 8),                 #10101010 | 01001 P2 P1 P0
            *([KS56CX2X._mov_rpe1_XA] * 8),                #10101010 | 01010 P2 P1 P0
            *([KS56CX2X._mov_xa_rpe] * 8),                 #10101010 | 01011 P2 P1 P0
            *([KS56CX2X._dummy] * 8),
            *([KS56CX2X._decs_rpe] * 8),                   #10101010 | 01101 P2 P1 P0
            *([KS56CX2X._dummy] * 32),
            *([KS56CX2X._and_rpe1_xa] * 8),                #10101010 | 10010 P2 P1 P0
            *([KS56CX2X._and_xa_rpe] * 8),                 #10101010 | 10011 P2 P1 P0
            *([KS56CX2X._or_rpe1_xa] * 8),                 #10101010 | 10100 P2 P1 P0
            *([KS56CX2X._or_xa_rpe] * 8),                  #10101010 | 10101 P2 P1 P0
            *([KS56CX2X._xor_rpe1_xa] * 8),                #10101010 | 10110 P2 P1 P0
            *([KS56CX2X._xor_xa_rpe] * 8),                 #10101010 | 10111 P2 P1 P0
            *([KS56CX2X._adds_rpe1_xa] * 8),               #10101010 | 11000 P2 P1 P0
            *([KS56CX2X._adds_xa_rpe] * 8),                #10101010 | 11001 P2 P1 P0
            *([KS56CX2X._addc_rpe1_xa] * 8),               #10101010 | 11010 P2 P1 P0
            *([KS56CX2X._addc_xa_rpe] * 8),                #10101010 | 11011 P2 P1 P0
            *([KS56CX2X._subs_rpe1_xa] * 8),               #10101010 | 11100 P2 P1 P0
            *([KS56CX2X._subs_xa_rpe] * 8),                #10101010 | 11101 P2 P1 P0
            *([KS56CX2X._subc_rpe1_xa] * 8),               #10101010 | 11110 P2 P1 P0
            *([KS56CX2X._subc_xa_rpe] * 8),                #10101010 | 11111 P2 P1 P0
        )

        self._execute_10101100 = (
            KS56CX2X._and1_cy_hmembit,                     #10101100 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._and1_cy_pmeml,                       #10101100 | 0100 G3 G2 G1 G0
            KS56CX2X._and1_cy_fmembit,                     #10101100 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._and1_cy_fmembit                      #10101100 | 11 B1 B0 F3 F2 F1 F0
        )

        self._execute_10101110 = (
            KS56CX2X._or1_cy_hmembit,                      #10101110 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._or1_cy_pmeml,                        #10101110 | 0100 G3 G2 G1 G0
            KS56CX2X._or1_cy_fmembit,                      #10101110 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._or1_cy_fmembit                       #10101110 | 11 B1 B0 F3 F2 F1 F0
        )

        self._execute_10111100 = (
            KS56CX2X._xor1_cy_hmembit,                     #10111100 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._xor1_cy_pmeml,                       #10111100 | 0100 G3 G2 G1 G0
            KS56CX2X._xor1_cy_fmembit,                     #10111100 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._xor1_cy_fmembit                      #10111100 | 11 B1 B0 F3 F2 F1 F0
        )

        self._execute_10111101 = (
            KS56CX2X._mov1_cy_hmembit,                     #10111101 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._mov1_cy_pmeml,                       #10111101 | 0100 G3 G2 G1 G0
            KS56CX2X._mov1_cy_fmembit,                     #10111101 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._mov1_cy_fmembit                      #10111101 | 11 B1 B0 F3 F2 F1 F0
        )

        self._execute_10111110 = (
            KS56CX2X._skf_hmembit,                         #10111110 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._skf_pmeml,                           #10111110 | 0100 G3 G2 G1 G0
            KS56CX2X._skf_fmembit,                         #10111110 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._skf_fmembit                          #10111110 | 11 B1 B0 F3 F2 F1 F0
        )

        self._execute_10111111 = (
            KS56CX2X._skt_hmembit,                         #10111111 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2X._skt_pmeml,                           #10111111 | 0100 G3 G2 G1 G0
            KS56CX2X._skt_fmembit,                         #10111111 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2X._skt_fmembit                          #10111111 | 11 B1 B0 F3 F2 F1 F0
        )

    def examine(self):
        return {
            "PC": self._PC,
            "XA": self._get_rp(RPE_XA),
            "HL": self._get_rp(RPE_HL),
            "DE": self._get_rp(RPE_DE),
            "BC": self._get_rp(RPE_BC),
            "XAE": self._get_rp(RPE_XAE),
            "HLE": self._get_rp(RPE_HLE),
            "DEE": self._get_rp(RPE_DEE),
            "BCE": self._get_rp(RPE_BCE),
            "SP": self._SP,
            "CY": self._CY,
            "RBE": self._RBE,
            "MBE": self._MBE,
            "IME": self._IME,
            "RBS": self._RBS,
            "MBS": self._MBS,
            "SBS": self._SBS,
            "RAM0": self._RAM[:256],
            "RAM1": self._RAM[256:512],
            "IORAM": [self._io_tbl[key][0](self) for key in self._io_tbl.keys()]
        }

    def edit_state(self, state):
        if ("XA" in state):
            self._set_rp(RPE_XA, state["XA"])
        if ("HL" in state):
            self._set_rp(RPE_HL, state["HL"])
        if ("DE" in state):
            self._set_rp(RPE_DE, state["DE"])
        if ("BC" in state):
            self._set_rp(RPE_BC, state["BC"])
        if ("XAE" in state):
            self._set_rp(RPE_XAE, state["XAE"])
        if ("HLE" in state):
            self._set_rp(RPE_HLE, state["HLE"])
        if ("DEE" in state):
            self._set_rp(RPE_DEE, state["DEE"])
        if ("BCE" in state):
            self._set_rp(RPE_BCE, state["BCE"])
        if ("CY" in state):
            self._CY = state["CY"]
        if ("RBE" in state):
            self._RBE = state["RBE"]
        if ("MBE" in state):
            self._MBE = state["MBE"]
        if ("IME" in state):
            self._IME = state["IME"]
        if ("RBS" in state):
            self._RBS = state["RBS"] & 0x3
        if ("MBS" in state):
            self._MBS = state["MBS"] & 0xF
        if ("SBS" in state):
            self._SBS = state["SBS"] & 0xF
        if ("PC" in state):
            self._PC = state["PC"] & self._ROM.getMask()
        if ("SP" in state):
            self._SP = state["SP"] & 0xFF
        if ("RAM0" in state):
            for i, value in state["RAM0"].items():
                self._RAM[i] = value & 0xF
        if ("RAM1" in state):
            for i, value in state["RAM1"].items():
                self._RAM[256 + i] = value & 0xF
        if ("IORAM" in state):
            for i, value in state["IORAM"].items():
                if i < len(self._io_tbl):
                        list(self._io_tbl.values())[i][1](self, value & 0xF)
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])

    def _init_registers(self):
        self._PC = 0
        self._CY = 0
        self._SP = 0
        
        self._MBE = 0
        self._MBS = 0
        self._RBE = 0
        self._RBS = 0
        self._SBS = 0
        self._TMOD2H = 0xFF
        self._WDTM = 0
        self._BT = 0
        self._BTM = 0
        self._IST = 0
        self._SK = 0
        self._SCC = 0

        self._WMl = 0
        self._WMh = 0

        self._TM0l = 0
        self._TM0h = 0
        self._T0 = 0
        self._TMOD0 = 0xFF

        self._IME = 0
        self._IPS = 0
        self._PCC_MODE = 0
        self._PCC_CLOCK = 0
        self._IM0 = 0
        self._IM1 = 0
        self._IM2 = 0
        self._INTA = 0
        self._INTC = 0
        self._INTE = 0
        self._INTF = 0
        self._INTG = 0
        self._INTH = 0

        self._PORT0 = [0, 0]
        self._PORT1 = [0, 0]
        self._PORT2 = [0, 0]
        self._PORT3 = [0, 0]
        self._PORT5 = [0, 0]
        self._PORT6 = [0, 0]
        self._PORT8 = [0, 0]
        self._PORT9 = [0, 0]

        self._PORT2_OUT_LATCH = 0
        self._PORT3_OUT_LATCH = 0
        self._PORT5_OUT_LATCH = 0
        self._PORT6_OUT_LATCH = 0
        self._PORT8_OUT_LATCH = 0
        self._PORT9_OUT_LATCH = 0

        self._POGA = 0
        self._POGB = 0

        self._PM3 = 0
        self._PM6 = 0

        self._RAM = [0] * RAM_SIZE

    def _reset(self):
        self._init_registers()
        self._go_vector(0)

    def reset(self):
        self._reset()

    def pc(self):
        return self._PC & 0x1FFF
    
    def get_VRAM(self):
        return tuple(self._RAM[VRAM_OFFSET:(VRAM_OFFSET + VRAM_SIZE)])

    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter

    def _get_io_dummy(self):
        return 0
    
    def _set_io_dummy(self, value):
        pass

    def _get_io_spl(self):
        return self._SP & 0x0F

    def _set_io_spl(self, value):
        self._SP = (self._SP & 0xF0) | (value & 0xF)

    def _get_io_sph(self):
        return self._SP >> 4

    def _set_io_sph(self, value):
        self._SP = (self._SP & 0x0F) | ((value & 0xF) << 4)

    def _get_io_rbs(self):
        return self._RBS

    def _get_io_mbs(self):
        return self._MBS

    def _get_io_sbs(self):
        return self._SBS

    def _set_io_sbs(self, value):
        self._SBS = value & 0xF

    def _set_io_btm(self, value):
        self._BTM = value & 0x7
        if (value & 0x8):
            self._INTA &= ~IOM_INTA_IRQBT
            self._BT = 0

    def _get_io_btl(self):
        return self._BT & 0xF

    def _get_io_bth(self):
        return self._BT >> 4

    def _get_io_tmod2hl(self):
        return self._TMOD2H & 0xF

    def _set_io_tmod2hl(self, value):
        self._TMOD2H = (self._TMOD2H & 0xF0) | (value & 0xF)

    def _get_io_tmod2hh(self):
        return self._TMOD2H >> 4

    def _set_io_tmod2hh(self, value):
        self._TMOD2H = (self._TMOD2H & 0x0F) | ((value & 0xF) << 4)

    def _get_io_wml(self):
        return self._WMl

    def _set_io_wml(self, value):
        self._WMl = value & 0xF
        self._watch_timer_enable = value & 0x4

    def _get_io_wmh(self):
        return self._WMh

    def _set_io_wmh(self, value):
        self._WMh = (value & 0xB)

    def _get_io_tm0l(self):
        return self._TM0l

    def _set_io_tm0l(self, value):
        self._TM0l = value & 0xC
        if (value & IOM_TM0l_START):
            self._INTE &= ~IOM_INTE_IRQT0
            self._T0 = 0

    def _get_io_tm0h(self):
        return self._TM0h

    def _set_io_tm0h(self, value):
        self._TM0h = value & 0x7

    def _get_io_t0l(self):
        return self._T0 & 0xF

    def _get_io_t0h(self):
        return self._T0 >> 4
        
    def _get_io_tmod0l(self):
        return self._TMOD0 & 0xF

    def _set_io_tmod0l(self, value):
        self._TMOD0 = (self._TMOD0 & 0xF0) | (value & 0xF)

    def _get_io_tmod0h(self):
        return self._TMOD0 >> 4

    def _set_io_tmod0h(self, value):
        self._TMOD0 = (self._TMOD0 & 0x0F) | ((value << 4) & 0xF0)

    def _set_io_wdtm(self, value):
        self._WDTM = (value >> 3) & 0x1

    def _get_io_pswl(self):
        return (self._IST << 2) | (self._MBE << 1) | self._RBE

    def _set_io_pswl(self, value):
        self._IST = (value >> 2) & 0x3
        self._MBE = (value >> 1) & 0x1
        self._RBE = value & 0x1

    def _get_io_pswh(self):
        return (self._CY << 3) | self._SK

    def _set_io_pswh(self, value):
        self._CY = (value >> 3) & 0x1
        self._SK = value & 0x7

    def _get_io_ips(self):
        return (self._IME << 3) | self._IPS

    def _set_io_ips(self, value):
        self._IME = (value >> 3) & 0x1
        self._IPS = value & 0x7

    def _get_io_pcc(self):
        return (self._PCC_MODE << 2) | self._PCC_CLOCK

    def _set_io_pcc(self, value):
        self._PCC_MODE = (value >> 2) & 0x3
        self._PCC_CLOCK = value & 0x3
        self.update_cpu_clock_div()

    def _get_io_im0(self):
        return self._IM0

    def _set_io_im0(self, value):
        self._IM0 = value & 0xF

    def _get_io_im1(self):
        return self._IM1

    def _set_io_im1(self, value):
        self._IM1 = value & 0x1

    def _get_io_im2(self):
        return self._IM2

    def _set_io_im2(self, value):
        self._IM2 = value & 0x3

    def _get_io_scc(self):
        return self._SCC

    def _set_io_scc(self, value):
        self._SCC = value & 0x9
        self.update_cpu_clock_div()

    def _get_io_inta(self):
        return self._INTA

    def _set_io_inta(self, value):
        self._INTA = value

    def _get_io_intc(self):
        return self._INTC

    def _set_io_intc(self, value):
        self._INTC = value

    def _get_io_inte(self):
        return self._INTE

    def _set_io_inte(self, value):
        self._INTE = value

    def _get_io_intf(self):
        return self._INTF

    def _set_io_intf(self, value):
        self._INTF = value

    def _get_io_intg(self):
        return self._INTG

    def _set_io_intg(self, value):
        self._INTG = value

    def _get_io_inth(self):
        return self._INTH

    def _set_io_inth(self, value):
        self._INTH = value

    def _get_io_pogal(self):
        return self._POGA & 0xF

    def _set_io_pogal(self, value):
        self._POGA = (self._POGA & 0xF0) | (value & 0x0F)

    def _get_io_pogah(self):
        return (self._POGA >> 4) & 0x0F

    def _set_io_pogah(self, value):
        self._POGA = (self._POGA & 0x0F) | ((value & 0x0F) << 4)

    def _get_io_pmgal(self):
        return self._PM3

    def _set_io_pmgal(self, value):
        self._PM3 = value & 0xF

    def _get_io_pmgah(self):
        return self._PM6

    def _set_io_pmgah(self, value):
        self._PM6 = value & 0xF

    def _get_io_port0(self):
        return ~self._PORT0[0] & (self._PORT0[1] | (((self._POGA & 0x1) > 0) * 15))

    def _get_io_port1(self):
        return ~self._PORT1[0] & (self._PORT1[1] | (((self._POGA & 0x2) > 0) * 15))

    def _get_io_port2(self):
        return ~self._PORT2[0] & (self._PORT2[1] | (((self._POGA & 0x4) > 0) * 15))

    def _set_io_port2(self, value):
        self._PORT2_OUT_LATCH = value

    def _get_io_port3(self):
        ext = ~self._PORT3[0] & (self._PORT3[1] | (((self._POGA & 0x8) > 0) * 15))
        return (ext & ~self._PM3) | (self._PORT3_OUT_LATCH & self._PM3)

    def _set_io_port3(self, value):
        self._PORT3_OUT_LATCH = value
        self._sound.toggle(value & 0x8, 0, self._cycle_counter)

    def _get_io_port5(self):
        return ~self._PORT5[0] & self._PORT5[1]

    def _set_io_port5(self, value):
        self._PORT5_OUT_LATCH = value

    def _get_io_port6(self):
        ext = ~self._PORT6[0] & (self._PORT6[1] | (((self._POGA & 0x32) > 0) * 15))
        return (ext & ~self._PM6) | (self._PORT6_OUT_LATCH & self._PM6)

    def _set_io_port6(self, value):
        self._PORT6_OUT_LATCH = value

    def _get_io_port8(self):
        return ~self._PORT8[0] & (self._PORT8[1] | (((self._POGB & 0x1) > 0) * 15))

    def _set_io_port8(self, value):
        self._PORT8_OUT_LATCH = value

    def _get_io_port9(self):
        return ~self._PORT9[0] & (self._PORT9[1] | (((self._POGB & 0x2) > 0) * 15))

    def _set_io_port9(self, value):
        self._PORT9_OUT_LATCH = value

    def pin_set(self, port, pin, level):
        self._process_port_int(port, pin, level)

    def pin_release(self, port, pin):
        self._process_port_int(port, pin, -1)

    def _process_port_int(self, port, pin, level):
        if (port == 'PORT1'):
            prev_port = self._get_io_port1()
            self._PORT1[0] &= ~(1 << pin)
            self._PORT1[1] &= ~(1 << pin)
            if (level >= 0):
                self._PORT1[level] |= (1 << pin)
            if (prev_port != self._get_io_port1()):
                if ((pin == 1) and (self._IM1 != ((self._get_io_port1() >> 1) & 0x1))):
                    self._INTG |= IOM_INTG_IRQ1
                if ((pin == 0) and (self._IM0 != M_IM0_IGNORED) and
                    (((self._IM0 & M_IM0_FALLING_EDGE) != level) or (self._IM0 & M_IM0_ANY_EDGE))):
                    self._INTG |= IOM_INTG_IRQ0
        elif (port == 'PORT6'):
            prev_port = self._get_io_port6()
            self._PORT6[0] &= ~(1 << pin)
            self._PORT6[1] &= ~(1 << pin)
            if (level >= 0):
                self._PORT6[level] |= (1 << pin)
            if ((level == 0 and prev_port != self._get_io_port6()) and
                ((self._PM6 & (1 << pin)) == PORT_MODE_INPUT) and
                (self._IM2 == M_IM2_KR0TOKR3 or (self._IM2 == M_IM2_KR2KR3 and (pin == 2 or pin == 3)))):
                self._INTH |= IOM_INTH_IRQ2

    def update_cpu_clock_div(self):
        if (self._SCC & M_SCC_SUB_CLOCK):
            self._cpu_clock_div = self._sub_clock_div
        else:
            self._cpu_clock_div = MAIN_CLOCK_DIV[self._PCC_CLOCK]
            
    def _process_basic_timer(self, exec_cycles):
        self._basic_timer_counter -= exec_cycles
        while (self._basic_timer_counter <= 0):
            self._basic_timer_counter += BASIC_TIMER_DIV[self._BTM]
            self._BT = (self._BT + 1) & 0xFF
            if (self._BT == 0 and self._WDTM == 0):
                self._INTA |= IOM_INTA_IRQBT

    def _process_t0_timer(self, exec_cycles):
        if ((TIMER_T0_DIV[self._TM0h] > 0) and (self._TM0l & M_TM0l_COUNT)):
            self._T0_timer_counter -= exec_cycles
            while (self._T0_timer_counter <= 0):
                self._T0_timer_counter += TIMER_T0_DIV[self._TM0h]
                self._T0 = (self._T0 + 1) & 0xFF
                if (self._T0 == self._TMOD0):
                    self._INTE |= IOM_INTE_IRQT0
                    self._T0 = 0

    def _process_watch_timer(self, exec_cycles):
        if (self._WMl & M_WMl_WATCH_ENABLE):
            self._watch_timer_counter -= exec_cycles
            while (self._watch_timer_counter <= 0):
                if (self._WMl & M_WMl_SUB_CLOCK):
                    self._watch_timer_counter += WATCH_TIMER_DIV[self._WMl & M_WMl_WATCH_FAST_MODE] * self._sub_clock_div
                else:
                    self._watch_timer_counter += WATCH_TIMER_DIV[self._WMl & M_WMl_WATCH_FAST_MODE] * WATCH_TIMER_MAIN_CLOCK_DIV
                self._INTC |= IOM_INTC_IRQW
        else:
            self._watch_timer_counter = 0

    def _go_vector(self, addr):
        vector = self._ROM.getWord(addr)
        self._MBE = (vector >> 15) & 0x1
        self._RBE = (vector >> 14) & 0x1
        self._PC = vector & self._ROM.getMask()

    def _interrupt(self, IRQn):
        vector_addr = IRQn << 1
        self._stack_push((self._CY << 3) | self._SK)
        self._stack_push((self._IST << 2) | (self._MBE << 1) | self._RBE)
        self._stack_push((self._PC >> 4) & 0xF)
        self._stack_push(self._PC & 0xF)
        self._stack_push((self._MBE << 3) | (self._RBE << 2) | ((self._PC >> 12) & 0x1))
        self._stack_push((self._PC >> 8) & 0xF)
        self._go_vector(vector_addr)
        self._IST += 1
        if (IRQn == VRQ_INTBT):
            if ((self._INTA & IOM_INTA_IEBT) == 0):
                self._INTA &= ~IOM_INTA_IRQ4
            elif ((self._INTA & IOM_INTA_IE4) == 0):
                self._INTA &= ~IOM_INTA_IRQBT
        elif (IRQn == VRQ_INTT0):
            self._INTE &= ~IOM_INTE_IRQT0
        elif (IRQn == VRQ_INT0):
            self._INTG &= ~IOM_INTG_IRQ0
        elif (IRQn == VRQ_INT1):
            self._INTG &= ~IOM_INTG_IRQ1

    def _get_interrupt_vector(self):
        IRQn = 0
        if ((self._INTE & IOM_INTE_IET0) and (self._INTE & IOM_INTE_IRQT0)):
            if (VRQ_INTT0 == self._IPS and self._IST <= 1):
                return VRQ_INTT0
            elif (self._IST == 0):
                IRQn = VRQ_INTT0
        if ((self._INTG & IOM_INTG_IE1) and (self._INTG & IOM_INTG_IRQ1)):
            if (VRQ_INT1 == self._IPS and self._IST <= 1):
                return VRQ_INT1
            elif (self._IST == 0):
                IRQn = VRQ_INT1
        if ((self._INTG & IOM_INTG_IE0) and (self._INTG & IOM_INTG_IRQ0)):
            if (VRQ_INT0 == self._IPS and self._IST <= 1):
                return VRQ_INT0
            elif (self._IST == 0):
                IRQn = VRQ_INT0
        if ((self._INTA & IOM_INTA_IE4) and (self._INTA & IOM_INTA_IRQ4)):
            if (VRQ_INT4 == self._IPS and self._IST <= 1):
                return VRQ_INT4
            elif (self._IST == 0):
                IRQn = VRQ_INT4
        if ((self._INTA & IOM_INTA_IEBT) and (self._INTA & IOM_INTA_IRQBT)):
            if (VRQ_INTBT == self._IPS and self._IST <= 1):
                return VRQ_INTBT
            elif (self._IST == 0):
                IRQn = VRQ_INTBT
        return IRQn

    def clock(self):
        exec_cycles = self._cpu_clock_div
            
        if (self._PCC_MODE == PCC_MODE_NORMAL):
            byte = self._ROM.getByte(self._PC)
            bytes_count = self._execute[byte][1]
            opcode = self._ROM.getBytes(self._PC, bytes_count)
            self._PC += bytes_count
            exec_cycles *= self._execute[byte][0](self, opcode)
            self._instr_counter += 1
            
        elif (((self._INTC & IOM_INTC_IRQW) and (self._INTC & IOM_INTC_IEW)) |
            ((self._INTH & IOM_INTH_IRQ2) and (self._INTH & IOM_INTH_IE2)) |
            ((self._INTG & IOM_INTG_IRQ0) and (self._INTG & IOM_INTG_IE0) and (self._IM0 & M_IM0_NOISE_ELIM_DISABLE)) |
            ((self._INTG & IOM_INTG_IRQ1) and (self._INTG & IOM_INTG_IE1)) |
            ((self._INTE & IOM_INTE_IET0) and (self._INTE & IOM_INTE_IRQT0)) |
            ((self._INTA & IOM_INTA_IEBT) and (self._INTA & IOM_INTA_IRQBT))):
            self._PCC_MODE = PCC_MODE_NORMAL

        if (self._PCC_MODE != PCC_MODE_STOP):
            self._process_watch_timer(exec_cycles)
            if (not(self._SCC & M_SCC_MAIN_CLOCK_STOP)):
                self._process_basic_timer(exec_cycles)
                self._process_t0_timer(exec_cycles)

        if (self._IME):
            IRQn = self._get_interrupt_vector()
            if (IRQn > 0):
                self._interrupt(IRQn)
        
        self._cycle_counter += exec_cycles
        return exec_cycles

    def _get_mem(self, addr):
        mb = 15
        if ((self._MBE != 0) or (addr < 0x80)):
            mb = self._MBE * self._MBS
        if (mb != 15):
            return self._RAM[(mb << 8) + addr]
        else:
            io = self._io_tbl.get((mb << 8) + addr)
            if (io != None):
                return io[0](self)
            return 0

    def _set_mem(self, addr, value):
        mb = 15
        if ((self._MBE != 0) or (addr < 0x80)):
            mb = self._MBE * self._MBS
        if (mb != 15):
            self._RAM[(mb << 8) + addr] = value
        else:
            io = self._io_tbl.get((mb << 8) + addr)
            if (io != None):
                io[1](self, value)

    def _get_ahl(self):
        mb = self._MBE * self._MBS
        if (mb != 15):
            return self._RAM[(mb << 8) + self._get_rp(RPE_HL)]
        else:
            io = self._io_tbl.get((mb << 8) + self._get_rp(RPE_HL))
            if (io != None):
                return io[0](self)
            return 0

    def _get_ahl_byte(self):
        mb = self._MBE * self._MBS
        addr = (mb << 8) + self._get_rp(RPE_HL)
        if (mb != 15):
            return (self._RAM[addr + 1] << 4) | self._RAM[addr]
        else:
            result = 0
            io = self._io_tbl.get(addr + 1)
            if (io != None):
                result = io[0](self) << 4
            io = self._io_tbl.get(addr)
            if (io != None):
                result |= io[0](self)
            return result

    def _set_ahl(self, value):
        mb = self._MBE * self._MBS
        if (mb != 15):
            self._RAM[(mb << 8) + self._get_rp(RPE_HL)] = value
        else:
            io = self._io_tbl.get((mb << 8) + self._get_rp(RPE_HL))
            if (io != None):
                io[1](self, value)

    def _set_ahl_byte(self, value):
        mb = self._MBE * self._MBS
        addr = (mb << 8) + self._get_rp(RPE_HL)
        if (mb != 15):
            self._RAM[addr] = value & 0xF
            self._RAM[addr + 1] = value >> 4
        else:
            io = self._io_tbl.get(addr)
            if (io != None):
                io[1](self, value & 0xF)
            io = self._io_tbl.get(addr + 1)
            if (io != None):
                io[1](self, value >> 4)

    def _get_hmem(self, opcode):
        addr = (self._get_reg(REG_H) << 4) | (opcode & 0xF)
        mb = self._MBE * self._MBS
        if (mb != 15):
            return self._RAM[(mb << 8) + addr]
        else:
            io = self._io_tbl.get((mb << 8) + addr)
            if (io != None):
                return io[0](self)
            return 0

    def _set_hmem(self, opcode, value):
        addr = (self._get_reg(REG_H) << 4) | (opcode & 0xF)
        mb = self._MBE * self._MBS
        if (mb != 15):
            self._RAM[(mb << 8) + addr] = value
        else:
            io = self._io_tbl.get((mb << 8) + addr)
            if (io != None):
                io[1](self, value)

    def _get_pmeml(self, opcode):
        addr = 0xFC0 | ((opcode & 0xF) << 2) | (self._get_reg(REG_L) >> 2)
        io = self._io_tbl.get(addr)
        if (io != None):
            return io[0](self)
        return 0

    def _set_pmeml(self, opcode, value):
        addr = 0xFC0 | ((opcode & 0xF) << 2) | (self._get_reg(REG_L) >> 2)
        io = self._io_tbl.get(addr)
        if (io != None):
            io[1](self, value)

    def _get_fmem(self, opcode):
        addr = 0xFB0 | (opcode & 0b01001111)
        io = self._io_tbl.get(addr)
        if (io != None):
            return io[0](self)
        return 0

    def _set_fmem(self, opcode, value):
        addr = 0xFB0 | (opcode & 0b01001111)
        io = self._io_tbl.get(addr)
        if (io != None):
            io[1](self, value)

    def _get_reg(self, reg):
        return self._RAM[self._RBE * self._RBS * 8 + reg]

    def _set_reg(self, reg, value):
        self._RAM[self._RBE * self._RBS * 8 + reg] = value

    def _get_rp(self, rp):
        rp_offset = (self._RBE * self._RBS * 8 + (rp & 0x6)) ^ ((rp & 0x1) << 3)
        return (self._RAM[rp_offset + 1] << 4) | self._RAM[rp_offset]

    def _set_rp(self, rp, value):
        rp_offset = (self._RBE * self._RBS * 8 + (rp & 0x6)) ^ ((rp & 0x1) << 3)
        self._RAM[rp_offset] = value & 0xF
        self._RAM[rp_offset + 1] = (value >> 4) & 0xF

    def _stack_push(self, value):
        self._SP = (self._SP - 1) & 0xFF
        sp = ((self._SBS & 0x1) << 8) + self._SP
        self._RAM[sp] = value

    def _stack_push_byte(self, value):
        self._SP = (self._SP - 1) & 0xFF
        sph = ((self._SBS & 0x1) << 8) + self._SP
        self._RAM[sph] = (value >> 4) & 0xF
        self._SP = (self._SP - 1) & 0xFF
        spl = ((self._SBS & 0x1) << 8) + self._SP
        self._RAM[spl] = value & 0xF

    def _stack_pop(self):
        sp = ((self._SBS & 0x1) << 8) + self._SP
        self._SP = (self._SP + 1) & 0xFF
        return self._RAM[sp]

    def _stack_pop_byte(self):
        spl = ((self._SBS & 0x1) << 8) + self._SP
        sph = ((self._SBS & 0x1) << 8) + ((self._SP + 1) & 0xFF)
        self._SP = (self._SP + 2) & 0xFF
        return (self._RAM[sph] << 4) | self._RAM[spl]

    def _skip_next(self):
        opcode = self._ROM.getByte(self._PC)
        byte_count = self._execute[opcode][1]
        self._PC += byte_count
        return 1 if (byte_count < 3) else 2

    def _execute_10101011(self, opcode):
        #10011011
        return self._execute_10101011[(opcode >> 14) & 0x1](self, opcode)

    def _execute_10011001(self, opcode):
        #10011001
        return self._execute_10011001[opcode & 0x7F](self, opcode)
        
    def _execute_10011010(self, opcode):
        #10011010
        return self._execute_10011010[(opcode >> 3) & 0x1](self, opcode)

    def _execute_10011011(self, opcode):
        #10011011
        return self._execute_10011011[(opcode >> 6) & 0x3](self, opcode)

    def _execute_10011100(self, opcode):
        #10011100
        return self._execute_10011100[(opcode >> 6) & 0x3](self, opcode)

    def _execute_10011101(self, opcode):
        #10011101
        return self._execute_10011101[(opcode >> 6) & 0x3](self, opcode)

    def _execute_10011111(self, opcode):
        #10011111
        return self._execute_10011111[(opcode >> 6) & 0x3](self, opcode)

    def _execute_10101010(self, opcode):
        #10101010
        return self._execute_10101010[opcode & 0xFF](self, opcode)

    def _execute_10101100(self, opcode):
        #10101100
        return self._execute_10101100[(opcode >> 6) & 0x3](self, opcode)

    def _execute_10101110(self, opcode):
        #10101110
        return self._execute_10101110[(opcode >> 6) & 0x3](self, opcode)
    
    def _execute_10111100(self, opcode):
        #10111100
        return self._execute_10111100[(opcode >> 6) & 0x3](self, opcode)

    def _execute_10111101(self, opcode):
        #10111101
        return self._execute_10111101[(opcode >> 6) & 0x3](self, opcode)

    def _execute_10111110(self, opcode):
        #10111110
        return self._execute_10111110[(opcode >> 6) & 0x3](self, opcode)

    def _execute_10111111(self, opcode):
        #10111111
        return self._execute_10111111[(opcode >> 6) & 0x3](self, opcode)

    def _br_raddr(self, opcode):
        #0000 A3 A2 A1 A0
        self._PC += opcode
        return 8

    def _br_mraddr(self, opcode):
        #1111 A3 A2 A1 A0
        self._PC -= (16 - (opcode & 0x0F))
        return 8

    def _geti_taddr(self, opcode):
        #00 T5 T4 T3 T2 T1 T0
        taddr = opcode << 1
        byte = self._ROM.getByte(taddr)
        bytes_count = self._execute[byte][1]
        execute_time = 1
        if (bytes_count == 1):
            if ((byte & 0xC0) == 0):
                self._PC = self._ROM.getWord(taddr) & self._ROM.getMask()
                return 3
            opcode = byte
            execute_time += self._execute[byte][0](self, opcode)
            byte = self._ROM.getByte(taddr + 1)
            execute_time += self._execute[byte][0](self, opcode)
        else:
            opcode = self._ROM.getBytes(taddr, bytes_count)
            execute_time += self._execute[byte][0](self, opcode)
        return execute_time

    def _callf_faddr(self, opcode):
        #01000 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        self._stack_push((self._PC >> 4) & 0x000F)
        self._stack_push(self._PC & 0x000F)
        self._stack_push((self._MBE << 3) | (self._RBE << 2) | (self._PC >> 12) & 0x0003)
        self._stack_push((self._PC >> 8) & 0x000F)
        self._PC = opcode & self._ROM.getMask()
        return 2

    def _pop_rp(self, opcode):
        #01001 P2 P1 0
        self._set_rp(opcode & 0x6, self._stack_pop_byte())
        return 1

    def _push_rp(self, opcode):
        #01001 P2 P1 1
        self._stack_push_byte(self._get_rp(opcode & 0x6))
        return 1

    def _brcb_caddr(self, opcode):
        #0101 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        self._PC = ((self._PC & 0xF000) | (opcode & 0xFFF)) & self._ROM.getMask()
        return 2

    def _adds_a_n4(self, opcode):
        #0110 I3 I2 I1 I0
        new_A = self._get_reg(REG_A) + (opcode & 0xF)
        self._set_reg(REG_A, new_A & 0xF)
        if (new_A > 15):
            return 1 + self._skip_next()
        return 1

    def _mov_a_n4(self, opcode):
        #0111 I3 I2 I1 I0
        self._set_reg(REG_A, opcode & 0xF)
        cycle_count = 1
        opcode = self._ROM.getByte(self._PC)
        while (((opcode >> 4) == 0b0111) or (opcode == 0b10001001)):
            cycle_count += 1
            self._PC += self._execute[opcode][1]
            opcode = self._ROM.getByte(self._PC)
        return cycle_count

    def _ske_a_ahl(self, opcode):
        #10000000
        if (self._get_reg(REG_A) == self._get_ahl()):
            return 1 + self._skip_next()
        return 1

    def _incs_mem(self, opcode):
        #10000010 | D7 D6 D5 D4 D3 D2 D1 D0
        d = opcode & 0x00FF
        new_mem = (self._get_mem(d) + 1) & 0xF
        self._set_mem(d, new_mem)
        if (new_mem == 0):
            return 2 + self._skip_next()
        return 2

    def _clr1_mem_bit(self, opcode):
        #10 B1 B0 0100 | D7 D6 D5 D4 D3 D2 D1 D0
        d = opcode & 0x00FF
        new_mem = self._get_mem(d) & ~(1 << ((opcode >> 12) & 0x3))
        self._set_mem(d, new_mem)
        return 2

    def _set1_mem_bit(self, opcode):
        #10 B1 B0 0101 | D7 D6 D5 D4 D3 D2 D1 D0
        d = opcode & 0x00FF
        new_mem = self._get_mem(d) | (1 << ((opcode >> 12) & 0x3))
        self._set_mem(d, new_mem)
        return 2

    def _skf_mem_bit(self, opcode):
        #10 B1 B0 0110 | D7 D6 D5 D4 D3 D2 D1 D0
        if (not(self._get_mem(opcode & 0xFF) & (1 << ((opcode >> 12) & 0x3)))):
            return 2 + self._skip_next()
        return 2

    def _skt_mem_bit(self, opcode):
        #10 B1 B0 0111 | D7 D6 D5 D4 D3 D2 D1 D0
        if (self._get_mem(opcode & 0xFF) & (1 << ((opcode >> 12) & 0x3))):
            return 2 + self._skip_next()
        return 2

    def _mov_xa_n8(self, opcode):
        #10001001 | I7 I6 I5 I4 I3 I2 I1 I0
        self._set_rp(RPE_XA, opcode & 0xFF)
        cycle_count = 2
        opcode = self._ROM.getByte(self._PC)
        while (((opcode >> 4) == 0b0111) or (opcode == 0b10001001)):
            cycle_count += 1
            self._PC += self._execute[opcode][1]
            opcode = self._ROM.getByte(self._PC)
        return cycle_count

    def _incs_rp1(self, opcode):
        #10001 P2 P1 0
        new_rp = (self._get_rp(opcode & 0x6) + 1) & 0xFF
        self._set_rp(opcode & 0x6, new_rp)
        if (new_rp == 0):
            return 1 + self._skip_next()
        return 1

    def _mov_hl_n8(self, opcode):
        #10001011 | I7 I6 I5 I4 I3 I2 I1 I0
        self._set_rp(RPE_HL, opcode & 0xFF)
        cycle_count = 2
        opcode = self._ROM.getByte(self._PC)
        while (opcode == 0b10001011):
            cycle_count += 1
            self._PC += self._execute[opcode][1]
            opcode = self._ROM.getByte(self._PC)
        return cycle_count

    def _mov_de_n8(self, opcode):
        #10001101 | I7 I6 I5 I4 I3 I2 I1 I0
        self._set_rp(RPE_DE, opcode & 0xFF)
        return 2

    def _mov_bc_n8(self, opcode):
        #10001111 | I7 I6 I5 I4 I3 I2 I1 I0
        self._set_rp(RPE_BC, opcode & 0xFF)
        return 2

    def _and_a_ahl(self, opcode):
        #10010000
        self._set_reg(REG_A, self._get_reg(REG_A) & self._get_ahl())
        return 1

    def _mov_mem_xa(self, opcode):
        #10010010 | D7 D6 D5 D4 D3 D2 D1 0
        d = opcode & 0xFF
        self._set_mem(d, self._get_reg(REG_A))
        self._set_mem(d + 1, self._get_reg(REG_X))
        return 2

    def _mov_mem_A(self, opcode):
        #10010011 | D7 D6 D5 D4 D3 D2 D1 D0
        d = opcode & 0xFF
        self._set_mem(d, self._get_reg(REG_A))
        return 2

    def _rorc_a(self, opcode):
        #10011000
        new_CY = self._get_reg(REG_A) & 0x1
        self._set_reg(REG_A, (self._get_reg(REG_A) >> 1) | (self._CY << 3))
        self._CY = new_CY
        return 1

    def _or_a_ahl(self, opcode):
        #10100000
        self._set_reg(REG_A, self._get_reg(REG_A) | self._get_ahl())
        return 1

    def _mov_xa_mem(self, opcode):
        #10100010 | D7 D6 D5 D4 D3 D2 D1 0
        d = opcode & 0xFE
        self._set_reg(REG_A, self._get_mem(d))
        self._set_reg(REG_X, self._get_mem(d + 1))
        return 2

    def _mov_a_mem(self, opcode):
        #10100011 | D7 D6 D5 D4 D3 D2 D1 D0
        d = opcode & 0xFF
        self._set_reg(REG_A, self._get_mem(d))
        return 2

    def _subs_a_ahl(self, opcode):
        #10101000
        new_A = self._get_reg(REG_A) - self._get_ahl()
        self._set_reg(REG_A, new_A & 0xF)
        if (new_A < 0):
            return 1 + self._skip_next()
        return 1

    def _addc_a_ahl(self, opcode):
        #10101001
        new_A = self._get_reg(REG_A) + self._get_ahl() + self._CY
        self._set_reg(REG_A, new_A & 0xF)
        self._CY = new_A > 15
        opcode = self._ROM.getByte(self._PC)
        if ((opcode >> 4) == 0b0110):
            if (self._CY):
                return 1 + self._skip_next()
            self._PC += 1
            self._set_reg(REG_A, (self._get_reg(REG_A) + (opcode & 0xF)) & 0xF)
            return 2
        return 1

    def _br_addr(self, opcode):
        #10101011 | 00 A13 A12 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        self._PC = opcode & self._ROM.getMask()
        return 1

    def _call_addr(self, opcode):
        #10101011 | 01 A13 A12 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        self._stack_push((self._PC >> 4) & 0x000F)
        self._stack_push(self._PC & 0x000F)
        self._stack_push((self._MBE << 3) | (self._RBE << 2) | (self._PC >> 12) & 0x0003)
        self._stack_push((self._PC >> 8) & 0x000F)
        self._PC = opcode & self._ROM.getMask()
        return 3

    def _xor_a_ahl(self, opcode):
        #10110000
        new_A = self._get_reg(REG_A) ^ self._get_ahl()
        self._set_reg(REG_A, new_A)
        return 1

    def _xch_xa_mem(self, opcode):
        #10110010 | D7 D6 D5 D4 D3 D2 D1 0
        d = opcode & 0xFE
        buf_A = self._get_reg(REG_A)
        buf_X = self._get_reg(REG_X)
        self._set_reg(REG_A, self._get_mem(d))
        self._set_reg(REG_X, self._get_mem(d + 1))
        self._set_mem(d, buf_A)
        self._set_mem(d + 1, buf_X)
        return 2

    def _xch_a_mem(self, opcode):
        #10110011 | D7 D6 D5 D4 D3 D2 D1 D0
        d = opcode & 0xFF
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_mem(d))
        self._set_mem(d, buf_A)
        return 2

    def _subc_a_ahl(self, opcode):
        #10111000
        new_A = self._get_reg(REG_A) - self._get_ahl() - self._CY
        self._set_reg(REG_A, new_A & 0xF)
        self._CY = new_A < 0
        opcode = self._ROM.getByte(self._PC)
        if ((opcode >> 4) == 0b0110):
            if (self._CY):
                self._PC += 1
                self._set_reg(REG_A, (self._get_reg(REG_A) + (opcode & 0xF)) & 0xF)
                return 2
            return 1 + self._skip_next()
        return 1

    def _adds_xa_n8(self, opcode):
        #10111001 | I7 I6 I5 I4 I3 I2 I1 I0
        new_XA = self._get_rp(RPE_XA) + (opcode & 0xFF)
        self._set_rp(RPE_XA, new_XA & 0xFF)
        if (new_XA > 255):
            return 2 + self._skip_next()
        return 2

    def _incs_reg(self, opcode):
        #11000 R2 R1 R0
        reg = opcode & 0x7
        new_value = (self._get_reg(reg) + 1) & 0xF
        self._set_reg(reg, new_value)
        if (new_value == 0):
            return 1 + self._skip_next()
        return 1

    def _decs_reg(self, opcode):
        #11001 R2 R1 R0
        reg = opcode & 0x7
        new_value = (self._get_reg(reg) - 1) & 0xF
        self._set_reg(reg, new_value)
        if (new_value == 0xF):
            return 1 + self._skip_next()
        return 1

    def _movt_xa_pcxa(self, opcode):
        #11010000
        addr = (self._PC & 0xFF00) | self._get_rp(RPE_XA)
        self._set_rp(RPE_XA, self._ROM.getByte(addr))
        return 3

    def _movt_xa_bcxa(self, opcode):
        #11010001
        addr = (self._get_rp(RPE_BC) << 8) | self._get_rp(RPE_XA)
        self._set_rp(RPE_XA, self._ROM.getByte(addr))
        return 3

    def _adds_a_ahl(self, opcode):
        #11010010
        new_A = self._get_reg(REG_A) + self._get_ahl()
        self._set_reg(REG_A, new_A & 0xF)
        if (new_A > 15):
            return 1 + self._skip_next()
        return 1

    def _movt_xa_pcde(self, opcode):
        #11010100
        addr = (self._PC & 0xFF00) | self._get_rp(RPE_DE)
        self._set_rp(RPE_XA, self._ROM.getByte(addr))
        return 3

    def _movt_xa_bcde(self, opcode):
        #11010101
        addr = (self._get_rp(RPE_BC) << 8) | self._get_rp(RPE_DE)
        self._set_rp(RPE_XA, self._ROM.getByte(addr))
        return 3

    def _not1_cy(self, opcode):
        #11010110
        self._CY = not self._CY
        return 1

    def _skt_cy(self, opcode):
        #11010111
        if (self._CY):
            return 1 + self._skip_next()
        return 1

    def _xch_a_reg1(self, opcode):
        #11011 R2 R1 R0
        reg = opcode & 0x7
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_reg(reg))
        self._set_reg(reg, buf_A)
        return 1

    def _rets(self, opcode):
        #11100000
        self._PC = self._stack_pop() << 8
        stack_value = self._stack_pop()
        self._PC |= stack_value << 12 & 0x1000
        self._MBE = stack_value >> 3
        self._RBE = (stack_value >> 2) & 0x1
        self._PC |= self._stack_pop()
        self._PC |= self._stack_pop() << 4
        self._PC &= self._ROM.getMask()
        return 3 + self._skip_next()

    def _mov_a_ahl(self, opcode):
        #11100001
        self._set_reg(REG_A, self._get_ahl())
        return 1

    def _mov_a_ahli(self, opcode):
        #11100010
        self._set_reg(REG_A, self._get_ahl())
        new_L = (self._get_reg(REG_L) + 1) & 0xF
        self._set_reg(REG_L, new_L)
        if (new_L == 0):
            return 2 + self._skip_next()
        return 1

    def _mov_a_ahld(self, opcode):
        #11100011
        self._set_reg(REG_A, self._get_ahl())
        new_L = (self._get_reg(REG_L) - 1) & 0xF
        self._set_reg(REG_L, new_L)
        if (new_L == 0xF):
            return 2 + self._skip_next()
        return 1

    def _mov_a_ade(self, opcode):
        #11100100
        self._set_reg(REG_A, self._RAM[self._get_rp(RPE_DE)])
        return 1

    def _mov_a_adl(self, opcode):
        #11100101
        dl = (self._get_reg(REG_D) << 4) | self._get_reg(REG_L)
        self._set_reg(REG_A, self._RAM[dl])
        return 1

    def _clr1_cy(self, opcode):
        #11100110
        self._CY = 0
        return 1

    def _set1_cy(self, opcode):
        #11100111
        self._CY = 1
        return 1

    def _mov_ahl_a(self, opcode):
        #11101000
        self._set_ahl(self._get_reg(REG_A))
        return 1

    def _xch_a_ahl(self, opcode):
        #11101001
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_ahl())
        self._set_ahl(buf_A)
        return 1

    def _xch_a_ahli(self, opcode):
        #11101010
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_ahl())
        self._set_ahl(buf_A)
        new_L = (self._get_reg(REG_L) + 1) & 0xF
        self._set_reg(REG_L, new_L)
        if (new_L == 0):
            return 2 + self._skip_next()
        return 1

    def _xch_a_ahld(self, opcode):
        #11101011
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_ahl())
        self._set_ahl(buf_A)
        new_L = (self._get_reg(REG_L) - 1) & 0xF
        self._set_reg(REG_L, new_L)
        if (new_L == 0xF):
            return 2 + self._skip_next()
        return 1

    def _xch_a_ade(self, opcode):
        #11101100
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._RAM[self._get_rp(RPE_DE)])
        self._RAM[self._get_rp(RPE_DE)] = buf_A
        return 1

    def _xch_a_adl(self, opcode):
        #11101101
        buf_A = self._get_reg(REG_A)
        dl = (self._get_reg(REG_D) << 4) | self._get_reg(REG_L)
        self._set_reg(REG_A, self._RAM[dl])
        self._RAM[dl] = buf_A
        return 1

    def _ret(self, opcode):
        #11101110
        self._PC = self._stack_pop() << 8
        stack_value = self._stack_pop()
        self._PC |= stack_value << 12 & 0x1000
        self._MBE = stack_value >> 3
        self._RBE = (stack_value >> 2) & 0x1
        self._PC |= self._stack_pop()
        self._PC |= self._stack_pop() << 4
        self._PC &= self._ROM.getMask()
        return 3

    def _reti(self, opcode):
        #11101111
        self._PC = self._stack_pop() << 8
        stack_value = self._stack_pop()
        self._PC |= stack_value << 12 & 0x1000
        self._MBE = stack_value >> 3
        self._RBE = (stack_value >> 2) & 0x1
        self._PC |= self._stack_pop()
        self._PC |= self._stack_pop() << 4
        stack_value = self._stack_pop()
        self._IST = stack_value >> 2
        self._MBE = (stack_value >> 1) & 0x1
        self._RBE = stack_value & 0x1
        stack_value = self._stack_pop()
        self._CY = (stack_value >> 3) & 0x1
        self._SK = stack_value & 0x7
        self._PC &= self._ROM.getMask()
        return 3

    def _br_pcxa(self, opcode):
        #10011001 | 00000000
        self._PC = ((self._PC & 0xFF00) | (self._get_reg(REG_X) << 4) | self._get_reg(REG_A)) & self._ROM.getMask()
        return 3

    def _br_bcxa(self, opcode):
        #10011001 | 00000001
        self._PC = ((self._get_reg(REG_B) << 12) | (self._get_reg(REG_C) << 8) | (self._get_reg(REG_X) << 4) | self._get_reg(REG_A)) & self._ROM.getMask()
        return 3

    def _incs_ahl(self, opcode):
        #10011001 | 00000010
        new_ahl = (self._get_ahl() + 1) & 0xF
        self._set_ahl(new_ahl)
        if (new_ahl == 0):
            return 2 + self._skip_next()
        return 2

    def _br_pcde(self, opcode):
        #10011001 | 00000100
        self._PC = ((self._PC & 0xFF00) | (self._get_reg(REG_D) << 4) | self._get_reg(REG_E)) & self._ROM.getMask()
        return 3

    def _br_bcde(self, opcode):
        #10011001 | 00000101
        self._PC = ((self._get_reg(REG_B) << 12) | (self._get_reg(REG_C) << 8) | (self._get_reg(REG_D) << 4) | self._get_reg(REG_E)) & self._ROM.getMask()
        return 3

    def _pop_bs(self, opcode):
        #10011001 | 00000110
        self._RBS = self._stack_pop()
        self._MBS = self._stack_pop()
        return 2

    def _push_bs(self, opcode):
        #10011001 | 00000111
        self._stack_push(self._MBS)
        self._stack_push(self._RBS)
        return 2

    def _ske_a_reg(self, opcode):
        #10011001 | 00001 R2 R1 R0
        if (self._get_reg(REG_A) == self._get_reg(opcode & 0x7)):
            return 2 + self._skip_next()
        return 2

    def _sel_mbn(self, opcode):
        #10011001 | 0001 N3 N2 N1 N0
        self._MBS = opcode & 0xF
        return 2

    def _sel_rbn(self, opcode):
        #10011001 | 001000 N1 N0
        self._RBS = opcode & 0x3
        return 2

    def _and_a_n4(self, opcode):
        #10011001 | 0011 I3 I2 I1 I0
        self._set_reg(REG_A, self._get_reg(REG_A) & opcode)
        return 2

    def _or_a_n4(self, opcode):
        #10011001 | 0100 I3 I2 I1 I0§
        self._set_reg(REG_A, (self._get_reg(REG_A) | opcode) & 0xF)
        return 2

    def _xor_a_n4(self, opcode):
        #10011001 | 0101 I3 I2 I1 I0
        self._set_reg(REG_A, (self._get_reg(REG_A) ^ opcode) & 0xF)
        return 2

    def _ske_ahl_n4(self, opcode):
        #10011001 | 0110 I3 I2 I1 I0
        if (self._get_ahl() == (opcode & 0xF)):
            return 2 + self._skip_next()
        return 2

    def _mov_reg1_A(self, opcode):
        #10011001 | 01110 R2 R1 R0
        self._set_reg(opcode & 0x7, self._get_reg(REG_A))
        return 2

    def _mov_a_reg(self, opcode):
        #10011001 | 01111 R2 R1 R0
        self._set_reg(REG_A, self._get_reg(opcode & 0x7))
        return 2

    def _ske_reg_n4(self, opcode):
        #10011010 | I3 I2 I1 I0 0 R2 R1 R0
        if (self._get_reg(opcode & 0x7) == ((opcode >> 4) & 0xF)):
            return 2 + self._skip_next()
        return 2

    def _mov_reg1_n4(self, opcode):
        #10011010 | I3 I2 I1 I0 1 R2 R1 R0
        self._set_reg(opcode & 0x7, (opcode >> 4) & 0xF)
        return 2

    def _mov1_hmembit_cy(self, opcode):
        #10011011 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        if (self._CY):
            self._set_hmem(opcode, self._get_hmem(opcode) | (1 << b))
        else:
            self._set_hmem(opcode, self._get_hmem(opcode) & ~(1 << b))
        return 2

    def _mov1_pmeml_cy(self, opcode):
        #10011011 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        if (self._CY):
            self._set_pmeml(opcode, self._get_pmeml(opcode) | (1 << b))
        else:
            self._set_pmeml(opcode, self._get_pmeml(opcode) & ~(1 << b))
        return 2

    def _mov1_fmembit_cy(self, opcode):
        #10011011 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        if (self._CY):
            self._set_fmem(opcode, self._get_fmem(opcode) | (1 << b))
        else:
            self._set_fmem(opcode, self._get_fmem(opcode) & ~(1 << b))
        return 2

    def _clr1_hmembit(self, opcode):
        #10011100 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        self._set_hmem(opcode, self._get_hmem(opcode) & ~(1 << b))
        return 2

    def _clr1_pmeml(self, opcode):
        #10011100 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        self._set_pmeml(opcode, self._get_pmeml(opcode) & ~(1 << b))
        return 2

    def _clr1_fmembit(self, opcode):
        #10011100 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        self._set_fmem(opcode, self._get_fmem(opcode) & ~(1 << b))
        return 2

    def _set1_hmembit(self, opcode):
        #10011101 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        self._set_hmem(opcode, self._get_hmem(opcode) | (1 << b))
        return 2

    def _set1_pmeml(self, opcode):
        #10011101 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        self._set_pmeml(opcode, self._get_pmeml(opcode) | (1 << b))
        return 2

    def _set1_fmembit(self, opcode):
        #10011101 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        self._set_fmem(opcode, self._get_fmem(opcode) | (1 << b))
        return 2

    def _sktclr_hmembit(self, opcode):
        #10011111 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        mem = self._get_hmem(opcode) 
        if (mem & (1 << b)):
            self._set_hmem(opcode, mem & ~(1 << b))
            return 2 + self._skip_next()
        return 2

    def _sktclr_pmeml(self, opcode):
        #10011111 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        mem = self._set_pmeml(opcode) 
        if (mem & (1 << b)):
            self._set_pmeml(opcode, mem & ~(1 << b))
            return 2 + self._skip_next()
        return 2

    def _sktclr_fmembit(self, opcode):
        #10011111 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        mem = self._get_fmem(opcode) 
        if (mem & (1 << b)):
            self._set_fmem(opcode, mem & ~(1 << b))
            return 2 + self._skip_next()
        return 2

    def _mov_ahl_xa(self, opcode):
        #10101010 | 00010000
        self._set_ahl_byte(self._get_rp(RPE_XA))
        return 2

    def _xch_xa_ahl(self, opcode):
        #10101010 | 00010001
        xa = self._get_rp(RPE_XA)
        self._set_rp(RPE_XA, self._get_ahl_byte())
        self._set_ahl_byte(xa)
        return 2

    def _mov_xa_ahl(self, opcode):
        #10101010 | 00011000
        self._set_rp(RPE_XA, self._get_ahl_byte())
        return 2

    def _ske_xa_ahl(self, opcode):
        #10101010 | 00011001
        if (self._get_rp(RPE_XA) == self._get_ahl_byte()):
            return 2 + self._skip_next()
        return 2

    def _xch_xa_rpe(self, opcode):
        #10101010 | 01000 P2 P1 P0
        xa = self._get_rp(RPE_XA)
        self._set_rp(RPE_XA, self._get_rp(opcode & 0x7))
        self._set_rp(opcode & 0x7, xa)
        return 2

    def _ske_xa_rpe(self, opcode):
        #10101010 | 01001 P2 P1 P0
        if (self._get_rp(RPE_XA) == self._get_rp(opcode & 0x7)):
            return 2 + self._skip_next()
        return 2

    def _mov_rpe1_XA(self, opcode):
        #10101010 | 01010 P2 P1 P0
        self._set_rp(opcode & 0x7, self._get_rp(RPE_XA))
        return 2

    def _mov_xa_rpe(self, opcode):
        #10101010 | 01011 P2 P1 P0
        self._set_rp(RPE_XA, self._get_rp(opcode & 0x7))
        return 2

    def _decs_rpe(self, opcode):
        #10101010 | 01101 P2 P1 P0
        new_value = (self._get_rp(opcode & 0x7) - 1) & 0xFF
        self._set_rp(opcode & 0x7, new_value)
        if (new_value == 0xFF):
            return 2 + self._skip_next()
        return 2

    def _and_rpe1_xa(self, opcode):
        #10101010 | 10010 P2 P1 P0
        self._set_rp(opcode & 0x7, self._get_rp(opcode & 0x7) & self._get_rp(RPE_XA))
        return 2

    def _and_xa_rpe(self, opcode):
        #10101010 | 10011 P2 P1 P0
        self._set_rp(RPE_XA, self._get_rp(opcode & 0x7) & self._get_rp(RPE_XA))
        return 2

    def _or_rpe1_xa(self, opcode):
        #10101010 | 10100 P2 P1 P0
        self._set_rp(opcode & 0x7, self._get_rp(opcode & 0x7) | self._get_rp(RPE_XA))
        return 2

    def _or_xa_rpe(self, opcode):
        #10101010 | 10101 P2 P1 P0
        self._set_rp(RPE_XA, self._get_rp(opcode & 0x7) | self._get_rp(RPE_XA))
        return 2

    def _xor_rpe1_xa(self, opcode):
        #10101010 | 10110 P2 P1 P0
        self._set_rp(opcode & 0x7, self._get_rp(opcode & 0x7) ^ self._get_rp(RPE_XA))
        return 2

    def _xor_xa_rpe(self, opcode):
        #10101010 | 10111 P2 P1 P0
        self._set_rp(RPE_XA, self._get_rp(opcode & 0x7) ^ self._get_rp(RPE_XA))
        return 2

    def _adds_rpe1_xa(self, opcode):
        #10101010 | 11000 P2 P1 P0
        new_value = self._get_rp(opcode & 0x7) + self._get_rp(RPE_XA)
        self._set_rp(opcode & 0x7, new_value & 0xFF)
        if (new_value > 255):
            return 2 + self._skip_next()
        return 2

    def _adds_xa_rpe(self, opcode):
        #10101010 | 11001 P2 P1 P0
        new_value = self._get_rp(opcode & 0x7) + self._get_rp(RPE_XA)
        self._set_rp(RPE_XA, new_value & 0xFF)
        if (new_value > 255):
            return 2 + self._skip_next()
        return 2

    def _addc_rpe1_xa(self, opcode):
        #10101010 | 11010 P2 P1 P0
        new_value = self._get_rp(opcode & 0x7) + self._get_rp(RPE_XA) + self._CY
        self._set_rp(opcode & 0x7, new_value & 0xFF)
        self._CY = new_value > 255
        return 2

    def _addc_xa_rpe(self, opcode):
        #10101010 | 11011 P2 P1 P0
        new_value = self._get_rp(opcode & 0x7) + self._get_rp(RPE_XA) + self._CY
        self._set_rp(RPE_XA, new_value & 0xFF)
        self._CY = new_value > 255
        return 2

    def _subs_rpe1_xa(self, opcode):
        #10101010 | 11100 P2 P1 P0
        new_value = self._get_rp(opcode & 0x7) - self._get_rp(RPE_XA)
        self._set_rp(opcode & 0x7, new_value & 0xFF)
        if (new_value < 0):
            return 2 + self._skip_next()
        return 2

    def _subs_xa_rpe(self, opcode):
        #10101010 | 11101 P2 P1 P0
        new_value = self._get_rp(RPE_XA) - self._get_rp(opcode & 0x7)
        self._set_rp(RPE_XA, new_value & 0xFF)
        if (new_value < 0):
            return 2 + self._skip_next()
        return 2

    def _subc_rpe1_xa(self, opcode):
        #10101010 | 11110 P2 P1 P0
        new_value = self._get_rp(opcode & 0x7) - self._get_rp(RPE_XA) - self._CY
        self._set_rp(opcode & 0x7, new_value & 0xFF)
        self._CY = new_value < 0
        return 2

    def _subc_xa_rpe(self, opcode):
        #10101010 | 11111 P2 P1 P0
        new_value = self._get_rp(RPE_XA) - self._get_rp(opcode & 0x7) - self._CY
        self._set_rp(RPE_XA, new_value & 0xFF)
        self._CY = new_value < 0
        return 2

    def _and1_cy_hmembit(self, opcode):
        #10101100 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        self._CY &= (self._get_hmem(opcode) >> b) & 0x1
        return 2

    def _and1_cy_pmeml(self, opcode):
        #10101100 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        self._CY &= (self._get_pmeml(opcode) >> b) & 0x1
        return 2

    def _and1_cy_fmembit(self, opcode):
        #10101100 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        self._CY &= (self._get_fmem(opcode) >> b) & 0x1
        return 2

    def _or1_cy_hmembit(self, opcode):
        #10101110 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        self._CY |= (self._get_hmem(opcode) >> b) & 0x1
        return 2

    def _or1_cy_pmeml(self, opcode):
        #10101110 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        self._CY |= (self._get_pmeml(opcode) >> b) & 0x1
        return 2

    def _or1_cy_fmembit(self, opcode):
        #10101110 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        self._CY |= (self._get_fmem(opcode) >> b) & 0x1
        return 2

    def _xor1_cy_hmembit(self, opcode):
        #10111100 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        self._CY ^= (self._get_hmem(opcode) >> b) & 0x1
        return 2

    def _xor1_cy_pmeml(self, opcode):
        #10111100 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        self._CY ^= (self._get_pmeml(opcode) >> b) & 0x1
        return 2

    def _xor1_cy_fmembit(self, opcode):
        #10111100 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        self._CY ^= (self._get_fmem(opcode) >> b) & 0x1
        return 2

    def _mov1_cy_hmembit(self, opcode):
        #10111101 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        self._CY = (self._get_hmem(opcode) >> b) & 0x1
        return 2

    def _mov1_cy_pmeml(self, opcode):
        #10111101 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        self._CY = (self._get_pmeml(opcode) >> b) & 0x1
        return 2

    def _mov1_cy_fmembit(self, opcode):
        #10111101 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        self._CY = (self._get_fmem(opcode) >> b) & 0x1
        return 2

    def _skf_hmembit(self, opcode):
        #10111110 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        if (not((self._get_hmem(opcode) >> b) & 0x1)):
            return 2 + self._skip_next()
        return 2

    def _skf_pmeml(self, opcode):
        #10111110 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        if (not((self._get_pmeml(opcode) >> b) & 0x1)):
            return 2 + self._skip_next()
        return 2

    def _skf_fmembit(self, opcode):
        #10111110 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        if (not((self._get_fmem(opcode) >> b) & 0x1)):
            return 2 + self._skip_next()
        return 2

    def _skt_hmembit(self, opcode):
        #10111111 | 00 B1 B0 D3 D2 D1 D0
        b = (opcode >> 4) & 0x3
        if ((self._get_hmem(opcode) >> b) & 0x1):
            return 2 + self._skip_next()
        return 2

    def _skt_pmeml(self, opcode):
        #10111111 | 0100 G3 G2 G1 G0
        b = self._get_reg(REG_L) & 0x3
        if ((self._get_pmeml(opcode) >> b) & 0x1):
            return 2 + self._skip_next()
        return 2

    def _skt_fmembit(self, opcode):
        #10111111 | 1 X B1 B0 F3 F2 F1 F0
        b = (opcode >> 4) & 0x3
        if ((self._get_fmem(opcode) >> b) & 0x1):
            return 2 + self._skip_next()
        return 2

    def _dummy(self, opcode):
        return 0
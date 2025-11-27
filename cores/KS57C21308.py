from .rom import ROM
from .PinTogglingSound import PinTogglingSound

#Based on KS57C21408/S3C7E8 datasheet
#pinout
# 01 - 02   SEG58 - SEG59
# 03 - 07   COM4 - COM8
# 08 - 09   GND
# 10 - 13   P6.0 - P6.3
# 14 - 15   P2.0 - P2.1
# 16 - 19   P5.0 - P5.3
# 20 - 22   P4.0 - P4.2
# 23 - 26   P0.3 - P0.0
# 27        P1.1
# 28 - 29   -
# 30        P1.0
# 31        RESET
# 32        Xout
# 33        Xin
# 34        TEST
# 35        XTin
# 36        XTout
# 37 - 38   VCC
# 39 - 42   COM0 - COM3
# 43 - 100  SEG0 - SEG57

SUB_CLOCK = 32768

RAM_SIZE = 0x1F00
VRAM_OFFSET = 0x1400
VRAM_SIZE = 256
IORAM_OFFSET = 0xF80
IORAM_SIZE = 128

BASIC_TIMER_DIV = [1 << 12, 1 << 12, 1 << 12, 1 << 9, 1 << 9, 1 << 7, 1 << 7, 1 << 5]
WATCH_TIMER_DIV = [1 << 14, 1 << 7]
TIMER_T0_DIV = [0, 0, 0, 0, 1 << 10, 1 << 6, 1 << 4, 1]
MAIN_CLOCK_DIV = [64, 64, 8, 4]
WATCH_TIMER_MAIN_CLOCK_DIV = 128

PCC_MODE_NORMAL = 0
PCC_MODE_HALT = 1
PCC_MODE_STOP = 2

RP_EA = 0
RP_HL = 2
RP_WX = 4
RP_YZ = 6

REG_A = 0
REG_E = 1
REG_L = 2
REG_H = 3
REG_X = 4
REG_W = 5
REG_Z = 6
REG_Y = 7

VRQ_INTBT = 1
VRQ_INT4 = 1 
VRQ_INT0 = 2
VRQ_INT1 = 3
VRQ_INTP0 = 4
VRQ_INTT0 = 5

IO_WMODl_SUB_CLOCK = 0x1
IO_WMODl_WATCH_ENABLE = 0x4
IO_WMODl_WATCH_FAST_MODE = 0x2

IO_INTB_IRQBT = 0x1
IO_INTB_IEBT = 0x2
IO_INTB_IRQ4 = 0x4
IO_INTB_IE4 = 0x8
IO_INTW_IRQW = 0x1
IO_INTW_IEW = 0x2
IO_INTT0_IRQT0 = 0x1
IO_INTT0_IET0 = 0x2
IO_INTP0_IRQP0 = 0x1
IO_INTP0_IEP0 = 0x2
IO_INT01_IRQ0 = 0x1
IO_INT01_IE0 = 0x2
IO_INT01_IRQ1 = 0x4
IO_INT01_IE1 = 0x8
IO_INT2_IRQ2 = 0x1
IO_INT2_IE2 = 0x2

IO_TMOD0h_CP = 0x7
IO_TMOD0l_CLEAR = 0x8
IO_TMOD0l_ENABLE = 0x4

IO_TOE0_TOE0 = 0x4
IO_PUMOD0_PUR1 = 0x1 #?
IO_PUMOD0_PUR2 = 0x2 #?
IO_PUMOD0_PUR4 = 0x4 #?
IO_PUMOD0_PUR5 = 0x8 #?
IO_PUMOD0_PUR6 = 0x8 #?
IO_LMOD1_P0PULLUP = 0x1

IO_PMG1L_PM2 = 0xC
IO_PMG1H_PM4 = 0xF
IO_PMG2_PM4 = 0x1
IO_PMG2_PM5 = 0x2
IO_PMG2_PM7 = 0x8

IO_SCMOD_DISABLE_FX = 0x8
IO_SCMOD_SELECT_FXT = 0x1

PORT_MODE_INPUT = 0
PORT_MODE_OUTPUT = 1

PORT4_TC0_OUT_PIN = 0x2

IO_IM0_FALLING_EDGE = 0x1
IO_IM0_ANY_EDGE = 0x2
IO_IM0_IGNORED = 0x3
IO_IM1_FALLING_EDGE = 0x1
IO_IM1_ANY_EDGE = 0x2
IO_IM1_IGNORED = 0x3
IO_IM0_NOISE_ELIM_DISABLE = 0x4
IO_IM2_KR2KR3 = 2
IO_IM2_KR0TOKR3 = 3

class KS57C21308():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = PinTogglingSound(clock)

        self._instr_counter = 0
        self._cycle_counter = 0
        self._basic_timer_counter = 0
        self._T0_timer_counter = 0
        self._watch_timer_counter = 0

        self._sub_clock_div = clock / SUB_CLOCK
        self._cpu_clock_div = MAIN_CLOCK_DIV[0]

        self._debug_page = 0
        
        self._reset()

        self._io_tbl = {
            0xF80: (KS57C21308._get_io_spl, KS57C21308._set_io_spl),
            0xF81: (KS57C21308._get_io_sph, KS57C21308._set_io_sph),

            0xF85: (KS57C21308._get_io_dummy, KS57C21308._set_io_bmod),
            0xF86: (KS57C21308._get_io_bcntl, KS57C21308._set_io_dummy),
            0xF87: (KS57C21308._get_io_bcnth, KS57C21308._set_io_dummy),
            0xF88: (KS57C21308._get_io_dummy, KS57C21308._set_io_wmodl),
            0xF89: (KS57C21308._get_io_dummy, KS57C21308._set_io_wmodh),

            0xF8C: (KS57C21308._get_io_dummy, KS57C21308._set_io_lmod0),
            0xF8D: (KS57C21308._get_io_dummy, KS57C21308._set_io_lmod1),

            0xF90: (KS57C21308._get_io_dummy, KS57C21308._set_io_tmod0l),
            0xF91: (KS57C21308._get_io_dummy, KS57C21308._set_io_tmod0h),
            0xF92: (KS57C21308._get_io_toe0, KS57C21308._set_io_toe0),

            0xF94: (KS57C21308._get_io_tcnt0l, KS57C21308._set_io_dummy),
            0xF95: (KS57C21308._get_io_tcnt0h, KS57C21308._set_io_dummy),
            0xF96: (KS57C21308._get_io_dummy, KS57C21308._set_io_tref0l),
            0xF97: (KS57C21308._get_io_dummy, KS57C21308._set_io_tref0h),

            0xFA0: (KS57C21308._get_io_dummy, KS57C21308._set_io_pasrl),
            0xFA1: (KS57C21308._get_io_dummy, KS57C21308._set_io_pasrh),
            0xFA2: (KS57C21308._get_io_dummy, KS57C21308._set_io_dummy),
            0xFA3: (KS57C21308._get_io_dummy, KS57C21308._set_io_dummy),
            0xFA4: (KS57C21308._get_io_dummy, KS57C21308._set_io_dummy),
            0xFA5: (KS57C21308._get_io_dummy, KS57C21308._set_io_dummy),

            0xFB0: (KS57C21308._get_io_pswl, KS57C21308._set_io_pswl),
            0xFB1: (KS57C21308._get_io_dummy, KS57C21308._set_io_pswh),
            0xFB2: (KS57C21308._get_io_dummy, KS57C21308._set_io_ipr),
            0xFB3: (KS57C21308._get_io_pcon, KS57C21308._set_io_pcon),
            0xFB4: (KS57C21308._get_io_im0, KS57C21308._set_io_im0),
            0xFB5: (KS57C21308._get_io_im1, KS57C21308._set_io_im1),
            0xFB6: (KS57C21308._get_io_im2, KS57C21308._set_io_im2),
            0xFB7: (KS57C21308._get_io_dummy, KS57C21308._set_io_scmod),
            0xFB8: (KS57C21308._get_io_intb, KS57C21308._set_io_intb),
            0xFBA: (KS57C21308._get_io_intw, KS57C21308._set_io_intw),
            0xFBC: (KS57C21308._get_io_intt0, KS57C21308._set_io_intt0),
            0xFBD: (KS57C21308._get_io_intp0, KS57C21308._set_io_intp0),
            0xFBE: (KS57C21308._get_io_int01, KS57C21308._set_io_int01),
            0xFBF: (KS57C21308._get_io_int2, KS57C21308._set_io_int2),

            0xFC0: (KS57C21308._get_io_bsc0, KS57C21308._set_io_bsc0),
            0xFC1: (KS57C21308._get_io_bsc1, KS57C21308._set_io_bsc1),
            0xFC2: (KS57C21308._get_io_bsc2, KS57C21308._set_io_bsc2),
            0xFC3: (KS57C21308._get_io_bsc3, KS57C21308._set_io_bsc3),

            0xFD0: (KS57C21308._get_io_dummy, KS57C21308._set_io_clmod),
            0xFDA: (KS57C21308._get_io_dummy, KS57C21308._set_io_dummy),
            0xFDB: (KS57C21308._get_io_dummy, KS57C21308._set_io_dummy),
            0xFDC: (KS57C21308._get_io_dummy, KS57C21308._set_io_pumodl),
            0xFDD: (KS57C21308._get_io_dummy, KS57C21308._set_io_pumodh),

            0xFE8: (KS57C21308._get_io_dummy, KS57C21308._set_io_pmg1l),
            0xFE9: (KS57C21308._get_io_dummy, KS57C21308._set_io_pmg1h),
            0xFEA: (KS57C21308._get_io_dummy, KS57C21308._set_io_pmg2),

            0xFF0: (KS57C21308._get_io_port0, KS57C21308._set_io_dummy),
            0xFF1: (KS57C21308._get_io_port1, KS57C21308._set_io_dummy),
            0xFF2: (KS57C21308._get_io_port2, KS57C21308._set_io_port2),
            0xFF4: (KS57C21308._get_io_port4, KS57C21308._set_io_port4),
            0xFF5: (KS57C21308._get_io_port5, KS57C21308._set_io_port5),
            0xFF6: (KS57C21308._get_io_port6, KS57C21308._set_io_port6),
        }

        self._execute = (
            *([(KS57C21308._br_mraddr, 1)] * 16),         #0000AAAA
            *([(KS57C21308._br_raddr, 1)] * 16),          #0001AAAA
            *([(KS57C21308._ref, 1)] * 8),                #00100XXX
            (KS57C21308._pop_rp, 1),                      #00101000
            (KS57C21308._push_rp, 1),                     #00101001
            (KS57C21308._pop_rp, 1),                      #00101010
            (KS57C21308._push_rp, 1),                     #00101011
            (KS57C21308._pop_rp, 1),                      #00101100
            (KS57C21308._push_rp, 1),                     #00101101
            (KS57C21308._pop_rp, 1),                      #00101110
            (KS57C21308._push_rp, 1),                     #00101111
            *([(KS57C21308._ref, 1)] * 8),                #00110XXX
            (KS57C21308._cpse_a_ahl, 1),                  #00111000 
            (KS57C21308._and_a_ahl, 1),                   #00111001
            (KS57C21308._or_a_ahl, 1),                    #00111010
            (KS57C21308._xor_a_ahl, 1),                   #00111011
            (KS57C21308._sbc_a_ahl, 1),                   #00111100
            (KS57C21308._sbs_a_ahl, 1),                   #00111101
            (KS57C21308._adc_a_ahl, 1),                   #00111110
            (KS57C21308._ads_a_ahl, 1),                   #00111111
            *([(KS57C21308._ref, 1)] * 8),                #01000XXX
            *([(KS57C21308._decs_r, 1)] * 8),             #01001RRR
            *([(KS57C21308._ref, 1)] * 8),                #01010XXX
            *([(KS57C21308._incs_r, 1)] * 8),             #01011RRR
            *([(KS57C21308._ref, 1)] * 8),                #01100XXX
            *([(KS57C21308._xch_a_ra, 1)] * 8),           #01101RRR
            *([(KS57C21308._ref, 1)] * 8),                #01110XXX
            (KS57C21308._dummy, 1),                       #01111000
            (KS57C21308._xch_a_da, 2),                    #01111001 AAAAAAAA
            (KS57C21308._xch_a_ahli, 1),                  #01111010
            (KS57C21308._xch_a_ahld, 1),                  #01111011
            (KS57C21308._dummy, 1),                       #01111100
            (KS57C21308._xch_a_ahl, 1),                   #01111101
            (KS57C21308._xch_a_awx, 1),                   #01111110
            (KS57C21308._xch_a_awl, 1),                   #01111111
            (KS57C21308._dummy, 1),                       #10000000
            (KS57C21308._ld_ea_imm, 2),                   #10000001 DDDDDDDD
            (KS57C21308._incs_rrb, 1),                    #10000RR0
            (KS57C21308._ld_hl_imm, 2),                   #10000011 DDDDDDDD
            (KS57C21308._incs_rrb, 1),                    #10000RR0
            (KS57C21308._ld_wx_imm, 2),                   #10000101 DDDDDDDD
            (KS57C21308._incs_rrb, 1),                    #10000RR0
            (KS57C21308._ld_yz_imm, 2),                   #10000111 DDDDDDDD
            (KS57C21308._rrc_a, 1),                       #10001000
            (KS57C21308._ld_da_a, 2),                     #10001001 AAAAAAAA
            (KS57C21308._ldi_a_ahl, 1),                   #10001010
            (KS57C21308._ldd_a_ahl, 1),                   #10001011
            (KS57C21308._ld_a_da, 2),                     #10001100 AAAAAAAA
            (KS57C21308._ld_a_ahl, 1),                    #10001101
            (KS57C21308._ld_a_awx, 1),                    #10001110
            (KS57C21308._ld_a_awl, 1),                    #10001111
            *([(KS57C21308._jps_addr12, 2)] * 16),        #1001AAAA AAAAAAAA
            *([(KS57C21308._ads_a_im, 1)] * 16),          #1010DDDD
            *([(KS57C21308._ld_a_im, 1)] * 16),           #1011DDDD
            (KS57C21308._bitr_da_bit, 2),                 #11000000 AAAAAAAA
            (KS57C21308._bits_da_bit, 2),                 #11000001 AAAAAAAA
            (KS57C21308._btsf_da_bit, 2),                 #11000010 AAAAAAAA
            (KS57C21308._btst_da_bit, 2),                 #11000011 AAAAAAAA
            (KS57C21308._ld_ahl_a, 1),                    #11000100
            (KS57C21308._ret, 1),                         #11000101
            (KS57C21308._dummy, 1),                       #11000110
            (KS57C21308._dummy, 1),                       #11000111
            (KS57C21308._ldc_ea_aea, 1),                  #11001000
            (KS57C21308._ads_ea_imm, 2),                  #11001001 DDDDDDDD
            (KS57C21308._incs_da, 2),                     #11001010 AAAAAAAA
            (KS57C21308._dummy, 1),                       #11001011
            (KS57C21308._ldc_ea_awx, 1),                  #11001100
            (KS57C21308._ld_da_ea, 2),                    #11001101 AAAAAAAA
            (KS57C21308._ld_ea_da, 2),                    #11001110 AAAAAAAA
            (KS57C21308._xch_ea_da, 2),                   #11001111 AAAAAAAA
            (KS57C21308._bitr_da_bit, 2),                 #11010000 AAAAAAAA
            (KS57C21308._bits_da_bit, 2),                 #11010001 AAAAAAAA
            (KS57C21308._btsf_da_bit, 2),                 #11010010 AAAAAAAA
            (KS57C21308._btst_da_bit, 2),                 #11010011 AAAAAAAA
            (KS57C21308._dummy, 1),                       #11010100
            (KS57C21308._iret, 1),                        #11010101
            (KS57C21308._ccf, 1),                         #11010110
            (KS57C21308._btst_cy, 1),                     #11010111
            (KS57C21308._dummy, 1),                       #11011000
            (KS57C21308._execute_11011001, 2),            #11011001
            (KS57C21308._dummy, 1),                       #11011010
            (KS57C21308._execute_11011011, 3),            #11011011
            (KS57C21308._execute_11011100, 2),            #11011100
            (KS57C21308._execute_11011101, 2),            #11011101
            (KS57C21308._dummy, 1),                       #11011110
            (KS57C21308._dummy, 1),                       #11011111
            (KS57C21308._bitr_da_bit, 2),                 #11100000 AAAAAAAA
            (KS57C21308._bits_da_bit, 2),                 #11100001 AAAAAAAA
            (KS57C21308._btsf_da_bit, 2),                 #11100010 AAAAAAAA
            (KS57C21308._btst_da_bit, 2),                 #11100011 AAAAAAAA
            (KS57C21308._dummy, 1),                       #11100100
            (KS57C21308._sret, 1),                        #11100101
            (KS57C21308._bitr_cy, 1),                     #11100110
            (KS57C21308._bits_cy, 1),                     #11100111
            *([(KS57C21308._calls_addr11, 2)] * 8),       #11101AAA AAAAAAAA
            (KS57C21308._bitr_da_bit, 2),                 #11110000 AAAAAAAA
            (KS57C21308._bits_da_bit, 2),                 #11110001 AAAAAAAA
            (KS57C21308._btsf_da_bit, 2),                 #11110010 AAAAAAAA
            (KS57C21308._btst_da_bit, 2),                 #11110011 AAAAAAAA
            (KS57C21308._execute_11110100, 2),            #11110100
            (KS57C21308._execute_11110101, 2),            #11110101
            (KS57C21308._execute_11110110, 2),            #11110110
            (KS57C21308._execute_11110111, 2),            #11110111
            (KS57C21308._execute_11111000, 2),            #11111000
            (KS57C21308._execute_11111001, 2),            #11111001
            (KS57C21308._dummy, 1),                       #11111010
            (KS57C21308._dummy, 1),                       #11111011
            (KS57C21308._execute_11111100, 2),            #11111100
            (KS57C21308._execute_11111101, 2),            #11111101
            (KS57C21308._execute_11111110, 2),            #11111110
            (KS57C21308._execute_11111111, 2)             #11111111
        )

        self._execute_11011001_tbl = (
            KS57C21308._cpse_r_im,                        #11011001 DDDD0RRR
            KS57C21308._ld_ra_im                          #11011001 DDDD1RRR
        )

        self._execute_11011011_tbl = (
            KS57C21308._jp_addr14,                        #11011011 00AAAAAA AAAAAAAA
            KS57C21308._call_addr14                       #11011011 01AAAAAA AAAAAAAA
        )
        
        self._execute_11011100_tbl = (
            KS57C21308._ld_ahl_ea,                        #11011100 00000000
            KS57C21308._xch_ea_ahl,                       #11011100 00000001
            *([KS57C21308._dummy] * 6),
            KS57C21308._ld_ea_ahl,                        #11011100 00001000
            KS57C21308._cpse_ea_ahl,                      #11011100 00001001
            *([KS57C21308._dummy] * 6),
            *([KS57C21308._and_rrb_ea] * 8),              #11011100 00010RR0
            *([KS57C21308._and_ea_rr] * 8),               #11011100 00011RR0
            *([KS57C21308._or_rrb_ea] * 8),               #11011100 00100RR0
            *([KS57C21308._or_ea_rr] * 8),                #11011100 00101RR0
            *([KS57C21308._xor_rrb_ea] * 8),              #11011100 00110RR0
            *([KS57C21308._xor_ea_rr] * 8),               #11011100 00111RR0
            *([KS57C21308._dummy] * 64),                  #11011100 01XXXXXX
            *([KS57C21308._dummy] * 16),                  #11011100 1000XXXX
            *([KS57C21308._ads_rrb_ea] * 8),              #11011100 10010RR0
            *([KS57C21308._ads_ea_rr] * 8),               #11011100 10011RR0
            *([KS57C21308._adc_rrb_ea] * 8),              #11011100 10100RR0
            *([KS57C21308._adc_ea_rr] * 8),               #11011100 10101RR0
            *([KS57C21308._sbs_rrb_ea] * 8),              #11011100 10110RR0
            *([KS57C21308._sbs_ea_rr] * 8),               #11011100 10111RR0
            *([KS57C21308._sbc_rrb_ea] * 8),              #11011100 11000RR0
            *([KS57C21308._sbc_ea_rr] * 8),               #11011100 11001RR0
            *([KS57C21308._dummy] * 8),                   #11011100 11010XXX
            *([KS57C21308._decs_rr] * 8),                 #11011100 11011RR0
            *([KS57C21308._xch_ea_rrb] * 8),              #11011100 11100RR0
            *([KS57C21308._cpse_ea_rr] * 8),              #11011100 11101RR0
            *([KS57C21308._ld_rrb_ea] * 8),               #11011100 11110RR0
            *([KS57C21308._ld_ea_rrb] * 8),               #11011100 11111RR0
        )
        
        self._execute_11011101_tbl = (
            *([KS57C21308._ld_ra_a] * 8),                 #11011101 00000RRR
            *([KS57C21308._ld_a_r] * 8),                  #11011101 00001RRR
            *([KS57C21308._and_a_im] * 16),               #11011101 0001DDDD
            *([KS57C21308._or_a_im] * 16),                #11011101 0010DDDD
            *([KS57C21308._xor_a_im] * 16),               #11011101 0011DDDD
            *([KS57C21308._smb_n] * 16),                  #11011101 0100NNNN
            *([KS57C21308._srb_n] * 4),                   #11011101 010100NN
            *([KS57C21308._dummy] * 4),                   #11011101 010101XX
            *([KS57C21308._dummy] * 8),                   #11011101 01011XXX
            KS57C21308._jr_aea,                           #11011101 01100000
            KS57C21308._dummy,                            #11011101 01100001
            KS57C21308._incs_ahl,                         #11011101 01100010
            KS57C21308._dummy,                            #11011101 01100011
            KS57C21308._jr_awx,                           #11011101 01100100
            KS57C21308._dummy,                            #11011101 01100101
            KS57C21308._pop_sb,                           #11011101 01100110
            KS57C21308._push_sb,                          #11011101 01100111
            *([KS57C21308._cpse_a_r] * 8),                #11011101 01101RRR
            *([KS57C21308._cpse_ahl_im] * 16),            #11011101 0111DDDD
            *([KS57C21308._dummy] * 128),                 #11011101 1XXXXXXX
        )
        
        self._execute_11110101_tbl = (
            KS57C21308._band_cy_ahda_bit,                 #11110101 00BBAAAA
            KS57C21308._band_cy_memb_al,                  #11110101 0100AAAA
            KS57C21308._band_cy_mema_bit,                 #11110101 10BBAAAA
            KS57C21308._band_cy_mema_bit                  #11110101 11BBAAAA
        )
        
        self._execute_11110110_tbl = (
            KS57C21308._bor_cy_ahda_bit,                  #11110110 00BBAAAA
            KS57C21308._bor_cy_memb_al,                   #11110110 0100AAAA
            KS57C21308._bor_cy_mema_bit,                  #11110110 10BBAAAA
            KS57C21308._bor_cy_mema_bit                   #11110110 11BBAAAA
        )

        self._execute_11110111_tbl = (
            KS57C21308._bxor_cy_ahda_bit,                 #11110111 00BBAAAA
            KS57C21308._bxor_cy_memb_al,                  #11110111 0100AAAA
            KS57C21308._bxor_cy_mema_bit,                 #11110111 10BBAAAA
            KS57C21308._bxor_cy_mema_bit                  #11110111 11BBAAAA
        )
        
        self._execute_11110100_tbl = (
            KS57C21308._ldb_cy_ahda_bit,                  #11110100 00BBAAAA
            KS57C21308._ldb_cy_memb_al,                   #11110100 0100AAAA
            KS57C21308._ldb_cy_mema_bit,                  #11110100 10BBAAAA
            KS57C21308._ldb_cy_mema_bit                   #11110100 11BBAAAA
        )
        
        self._execute_11111000_tbl = (
            KS57C21308._btsf_ahda_bit,                    #11111000 00BBAAAA
            KS57C21308._btsf_memb_al,                     #11111000 0100AAAA
            KS57C21308._btsf_mema_bit,                    #11111000 10BBAAAA
            KS57C21308._btsf_mema_bit                     #11111000 11BBAAAA
        )

        self._execute_11111001_tbl = (
            KS57C21308._btst_ahda_bit,                    #11111001 00BBAAAA
            KS57C21308._btst_memb_al,                     #11111001 0100AAAA
            KS57C21308._btst_mema_bit,                    #11111001 10BBAAAA
            KS57C21308._btst_mema_bit                     #11111001 11BBAAAA
        )
                
        self._execute_11111100_tbl = (
            KS57C21308._ldb_ahda_bit_cy,                  #11111100 00BBAAAA
            KS57C21308._ldb_memb_al_cy,                   #11111100 0100AAAA
            KS57C21308._ldb_mema_bit_cy,                  #11111100 10BBAAAA
            KS57C21308._ldb_mema_bit_cy                   #11111100 11BBAAAA
        )
        
        self._execute_11111110_tbl = (
            KS57C21308._bitr_ahda_bit,                    #11111110 00BBAAAA
            KS57C21308._bitr_memb_al,                     #11111110 0100AAAA
            KS57C21308._bitr_mema_bit,                    #11111110 10BBAAAA
            KS57C21308._bitr_mema_bit                     #11111110 11BBAAAA
        )
        
        self._execute_11111111_tbl = (
            KS57C21308._bits_ahda_bit,                    #11111111 00BBAAAA
            KS57C21308._bits_memb_al,                     #11111111 0100AAAA
            KS57C21308._bits_mema_bit,                    #11111111 10BBAAAA
            KS57C21308._bits_mema_bit                     #11111111 11BBAAAA
        )

        self._execute_11111101_tbl = (
            KS57C21308._btstz_ahda_bit,                   #11111101 00BBAAAA
            KS57C21308._btstz_memb_al,                    #11111101 0100AAAA
            KS57C21308._btstz_mema_bit,                   #11111101 10BBAAAA
            KS57C21308._btstz_mema_bit                    #11111101 11BBAAAA
        )

    def examine(self):
        return {
            "PC": self._PC,
            "EA": self._get_rp(RP_EA),
            "HL": self._get_rp(RP_HL),
            "WX": self._get_rp(RP_WX),
            "YZ": self._get_rp(RP_YZ),
            "SP": self._SP,
            "CY": self._CY,
            "RBE": self._ERB,
            "MBE": self._EMB,
            "IME": self._IME,
            "RBS": self._SRB,
            "MBS": self._SMB,
            "PASR": self._PASR,
            "RAM": self._RAM[self._debug_page * 256: (self._debug_page + 1) * 256],
            "GRAM": self._RAM[VRAM_OFFSET:(VRAM_OFFSET + VRAM_SIZE)],
            "IORAM": [self._io_tbl[key][0](self) for key in self._io_tbl.keys()]
        }

    def edit_state(self, state):
        if ("EA" in state):
            self._set_rp(RP_EA, state["EA"])
        if ("HL" in state):
            self._set_rp(RP_HL, state["HL"])
        if ("WX" in state):
            self._set_rp(RP_WX, state["WX"])
        if ("YZ" in state):
            self._set_rp(RP_YZ, state["YZ"])
        if ("CY" in state):
            self._CY = state["CY"]
        if ("RBE" in state):
            self._ERB = state["RBE"]
        if ("MBE" in state):
            self._EMB = state["MBE"]
        if ("IME" in state):
            self._IME = state["IME"]
        if ("RBS" in state):
            self._SRB = state["RBS"] & 0x3
        if ("MBS" in state):
            self._SMB = state["MBS"] & 0xF
        if ("PASR" in state):
            self._PASR = state["PASR"] & 0xF
        if ("PC" in state):
            self._PC = state["PC"] & self._ROM.getMask()
        if ("SP" in state):
            self._SP = state["SP"] & 0xFF
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[self._debug_page * 256 + i] = value & 0xF
        if ("GRAM" in state):
            for i, value in state["GRAM"].items():
                self._RAM[VRAM_OFFSET + i] = value & 0xF
        if ("PAGE" in state):
            self._debug_page = state["PAGE"]
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
        
        self._EMB = 0
        self._SMB = 0
        self._ERB = 0
        self._SRB = 0
        self._BCNT = 0
        self._BMOD = 0
        self._IST = 0
        self._SK = 0
        self._SCMOD = 0

        self._PASR = 0

        self._WMODl = 0
        self._WMODh = 0

        self._TMOD0l = 0
        self._TMOD0h = 0
        self._TOE0 = 0
        self._LMOD0 = 0
        self._LMOD1 = 0
        self._TCNT0 = 0
        self._TREF0 = 0xFF

        self._BSC0 = 0
        self._BSC1 = 0
        self._BSC2 = 0
        self._BSC3 = 0

        self._IME = 0
        self._IPR = 0
        self._PCON_MODE = 0
        self._PCON_CLOCK = 0
        self._SCMOD = 0
        self._IM0 = 0
        self._IM1 = 0
        self._IM2 = 0
        self._INTB = 0
        self._INTW = 0
        self._INTT0 = 0
        self._INTP0 = 0
        self._INT01 = 0
        self._INT2 = 0

        self._PORT0 = [0, 0]
        self._PORT1 = [0, 0]
        self._PORT2 = [0, 0]
        self._PORT4 = [0, 0]
        self._PORT5 = [0, 0]
        self._PORT6 = [0, 0]

        self._PORT2_OUT_LATCH = 0
        self._PORT4_OUT_LATCH = 0
        self._PORT5_OUT_LATCH = 0
        self._PORT6_OUT_LATCH = 0
        self._PORT4_TC0_OUT = 0
        
        self._PUMOD0 = 0
        self._POGB = 0

        self._PM2 = 0
        self._PM4 = 0
        self._PM5 = 0
        self._PM6 = 0
        
        self._RAM = [0] * RAM_SIZE

    def _reset(self):
        self._sound.toggle(0, 0, 0)
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

    def _set_io_bsc0(self, value):
        self._BSC0 = (value & 0xF)

    def _set_io_bsc1(self, value):
        self._BSC1 = (value & 0xF)

    def _set_io_bsc2(self, value):
        self._BSC2 = (value & 0xF)
            
    def _set_io_bsc3(self, value):
        self._BSC3 = (value & 0xF)

    def _get_io_bsc0(self):
        return self._BSC0

    def _get_io_bsc1(self):
        return self._BSC1

    def _get_io_bsc2(self):
        return self._BSC2
            
    def _get_io_bsc3(self):
        return self._BSC3

    def _get_io_spl(self):
        return self._SP & 0x0F

    def _set_io_spl(self, value):
        self._SP = (self._SP & 0xF0) | (value & 0xE)

    def _get_io_sph(self):
        return self._SP >> 4

    def _set_io_sph(self, value):
        self._SP = (self._SP & 0x0F) | ((value & 0xF) << 4)

    def _set_io_bmod(self, value):
        self._BMOD = value & 0x7
        if (value & 0x8):
            self._INTB &= ~IO_INTB_IRQBT
            self._BCNT = 0

    def _get_io_bcntl(self):
        return self._BCNT & 0xF

    def _get_io_bcnth(self):
        return self._BCNT >> 4

    def _get_io_tmod2hl(self):
        return self._TMOD2H & 0xF

    def _set_io_tmod2hl(self, value):
        self._TMOD2H = (self._TMOD2H & 0xF0) | (value & 0xF)

    def _get_io_tmod2hh(self):
        return self._TMOD2H >> 4

    def _set_io_tmod2hh(self, value):
        self._TMOD2H = (self._TMOD2H & 0x0F) | ((value & 0xF) << 4)

    def _set_io_wmodl(self, value):
        self._WMODl = value & 0xF

    def _set_io_wmodh(self, value):
        self._WMODh = (value & 0xB)

    def _get_io_pasrl(self):
        return self._PASR & 0xF

    def _set_io_pasrl(self, value):
        self._PASR = (self._PASR & 0xF0) | (value & 0x0F)

    def _get_io_pasrh(self):
        return (self._PASR >> 4) & 0x1

    def _set_io_pasrh(self, value):
        self._PASR = ((value & 0x1) << 4) | (self._PASR & 0x0F)

    def _get_io_tcnt0l(self):
        return self._TCNT0 & 0xF

    def _get_io_tcnt0h(self):
        return self._TCNT0 >> 4

    def _set_io_tmod0h(self, value):
        self._TMOD0h = value & IO_TMOD0h_CP

    def _get_io_toe0(self):
        return self._TOE0

    def _set_io_toe0(self, value):
        self._TOE0 = value & IO_TOE0_TOE0

    def _set_io_lmod0(self, value):
        self._LMOD0 = value

    def _set_io_lmod1(self, value):
        self._LMOD1 = value

    def _set_io_tmod0l(self, value):
        if (value & IO_TMOD0l_CLEAR):
            self._INTT0 &= ~IO_INTT0_IRQT0
            self._TCNT0 = 0
        self._TMOD0l = value & (IO_TMOD0l_ENABLE | IO_TMOD0l_CLEAR)

    def _set_io_tref0l(self, value):
        self._TREF0 = (self._TREF0 & 0xF0) | (value & 0xF)

    def _set_io_tref0h(self, value):
        self._TREF0 = (self._TREF0 & 0x0F) | ((value << 4) & 0xF0)

    def _get_io_pswl(self):
        return (self._IST << 2) | (self._EMB << 1) | self._ERB

    def _set_io_pswl(self, value):
        self._IST = (value >> 2) & 0x3
        self._EMB = (value >> 1) & 0x1
        self._ERB = value & 0x1

    def _get_io_pswh(self):
        return (self._CY << 3) | self._SK

    def _set_io_pswh(self, value):
        self._CY = (value >> 3) & 0x1
        self._SK = value & 0x7

    def _get_io_ipr(self):
        return (self._IME << 3) | self._IPR

    def _set_io_ipr(self, value):
        self._IME = (value >> 3) & 0x1
        self._IPR = value & 0x7

    def _get_io_pcon(self):
        return (self._PCON_MODE << 2) | self._PCON_CLOCK

    def _set_io_pcon(self, value):
        self._PCON_MODE = (value >> 2) & 0x3
        self._PCON_CLOCK = value & 0x3
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

    def _set_io_scmod(self, value):
        self._SCMOD = value & 0x9
        self.update_cpu_clock_div()

    def _get_io_intb(self):
        return self._INTB

    def _set_io_intb(self, value):
        self._INTB = value

    def _get_io_intw(self):
        return self._INTW

    def _set_io_intw(self, value):
        self._INTW = value

    def _get_io_intt0(self):
        return self._INTT0

    def _set_io_intt0(self, value):
        self._INTT0 = value

    def _get_io_intp0(self):
        return self._INTP0

    def _set_io_intp0(self, value):
        self._INTP0 = value

    def _get_io_int01(self):
        return self._INT01

    def _set_io_int01(self, value):
        self._INT01 = value

    def _get_io_int2(self):
        return self._INT2

    def _set_io_int2(self, value):
        self._INT2 = value

    def _get_io_pumodl(self):
        return self._PUMOD0 & 0xF

    def _set_io_clmod(self, value):
        pass

    def _set_io_pumodl(self, value):
        print("pumodl %X" % self._PC)
        self._PUMOD0 = (self._PUMOD0 & 0xF0) | (value & 0x0F)

    def _get_io_pumodh(self):
        return (self._PUMOD0 >> 4) & 0x0F

    def _set_io_pumodh(self, value):
        print("pumodh", value)
        self._PUMOD0 = (self._PUMOD0 & 0x0F) | ((value & 0x0F) << 4)

    def _set_io_pmg1l(self, value):
        self._PM2 = (value & IO_PMG1L_PM2) >> 2

    def _set_io_pmg1h(self, value):
        self._PM6 = value & 0xF

    def _set_io_pmg2(self, value):
        self._PMG2 = value & 0xF
        if (value & IO_PMG2_PM4):
            self._PM4 = 0xF
        if (value & IO_PMG2_PM5):
            self._PM5 = 0xF

    def _get_io_port0(self):
        return ~self._PORT0[0] & (self._PORT0[1] | (((self._LMOD1 & IO_LMOD1_P0PULLUP) > 0) * 15))

    def _get_io_port1(self):
        return ~self._PORT1[0] & (self._PORT1[1] | (((self._PUMOD0 & IO_PUMOD0_PUR1) > 0) * 15))

    def _get_io_port2(self):
        ext = ~self._PORT2[0] & (self._PORT2[1] | (((self._PUMOD0 & IO_PUMOD0_PUR2) > 0) * 15))
        return (ext & ~self._PM2) | (self._PORT2_OUT_LATCH & self._PM2)

    def _set_io_port2(self, value):
        self._PORT2_OUT_LATCH = value

    def _get_io_port4(self):
        ext = ~self._PORT4[0] & (self._PORT4[1] | (((self._PUMOD0 & IO_PUMOD0_PUR4) > 0) * 15))
        return (ext & ~self._PM4) | ((self._PORT4_OUT_LATCH | self._PORT4_TC0_OUT) & self._PM4)

    def _set_io_port4(self, value):
        self._PORT4_OUT_LATCH = value

    def _get_io_port5(self):
        ext = ~self._PORT5[0] & (self._PORT5[1] | (((self._PUMOD0 & IO_PUMOD0_PUR5) > 0) * 15))
        return (ext & ~self._PM5) | (self._PORT5_OUT_LATCH & self._PM5)

    def _set_io_port5(self, value):
        self._PORT5_OUT_LATCH = value

    def _get_io_port6(self):
        ext = ~self._PORT6[0] & (self._PORT6[1] | (((self._PUMOD0 & IO_PUMOD0_PUR6) > 0) * 15))
        return (ext & ~self._PM6) | (self._PORT6_OUT_LATCH & self._PM6)

    def _set_io_port6(self, value):
        self._PORT6_OUT_LATCH = value

    def pin_set(self, port, pin, level):
        self._process_port_int(port, pin, level)

    def pin_release(self, port, pin):
        self._process_port_int(port, pin, -1)

    def _process_port_int(self, port, pin, level):
        if (port == 'PORT0'):
            prev_port = self._get_io_port0()
            self._PORT0[0] &= ~(1 << pin)
            self._PORT0[1] &= ~(1 << pin)
            if (level >= 0):
                self._PORT0[level] |= (1 << pin)
            if (prev_port != self._get_io_port0() and level == 0):
                self._INTP0 |= IO_INTP0_IRQP0
        if (port == 'PORT1'):
            prev_port = self._get_io_port1()
            self._PORT1[0] &= ~(1 << pin)
            self._PORT1[1] &= ~(1 << pin)
            if (level >= 0):
                self._PORT1[level] |= (1 << pin)
            if (prev_port != self._get_io_port1()):
                if ((pin == 1) and (self._IM1 != IO_IM1_IGNORED) and
                    (((self._IM1 & IO_IM1_FALLING_EDGE) != level) or (self._IM1 & IO_IM1_ANY_EDGE))):
                    self._INT01 |= IO_INT01_IRQ1
                if ((pin == 0) and (self._IM0 != IO_IM0_IGNORED) and
                    (((self._IM0 & IO_IM0_FALLING_EDGE) != level) or (self._IM0 & IO_IM0_ANY_EDGE))):
                    self._INT01 |= IO_INT01_IRQ0
        elif (port == 'PORT6'):
            prev_port = self._get_io_port6()
            self._PORT6[0] &= ~(1 << pin)
            self._PORT6[1] &= ~(1 << pin)
            if (level >= 0):
                self._PORT6[level] |= (1 << pin)
            if ((level == 0 and prev_port != self._get_io_port6()) and
                ((self._PM6 & (1 << pin)) == PORT_MODE_INPUT) and
                (self._IM2 == IO_IM2_KR0TOKR3 or (self._IM2 == IO_IM2_KR2KR3 and (pin == 2 or pin == 3)))):
                self._INT2 |= IO_INT2_IRQ2

    def update_cpu_clock_div(self):
        if (self._SCMOD & IO_SCMOD_SELECT_FXT):
            self._cpu_clock_div = self._sub_clock_div * 4
        else:
            self._cpu_clock_div = MAIN_CLOCK_DIV[self._PCON_CLOCK]
            
    def _process_basic_timer(self, exec_cycles):
        self._basic_timer_counter -= exec_cycles
        while (self._basic_timer_counter <= 0):
            self._basic_timer_counter += BASIC_TIMER_DIV[self._BMOD]
            self._BCNT = (self._BCNT + 1) & 0xFF
            if (self._BCNT == 0):
                self._INTB |= IO_INTB_IRQBT

    def _process_t0_timer(self, exec_cycles):
        if ((TIMER_T0_DIV[self._TMOD0h] > 0) and (self._TMOD0l & IO_TMOD0l_ENABLE)):
            self._T0_timer_counter -= exec_cycles
            while (self._T0_timer_counter <= 0):
                self._T0_timer_counter += TIMER_T0_DIV[self._TMOD0h]
                self._TCNT0 = (self._TCNT0 + 1) & 0xFF
                if (self._TCNT0 == self._TREF0):
                    self._INTT0 |= IO_INTT0_IRQT0
                    self._TCNT0 = 0
                    self._PORT4_TC0_OUT = ((self._TOE0 > 0) * 0xF) & (self._PORT4_TC0_OUT ^ PORT4_TC0_OUT_PIN)
                    self._sound.toggle(self._PORT4_TC0_OUT, ~self._PORT4_TC0_OUT, self._cycle_counter)

    def _process_watch_timer(self, exec_cycles):
        if (self._WMODl & IO_WMODl_WATCH_ENABLE):
            self._watch_timer_counter -= exec_cycles
            while (self._watch_timer_counter <= 0):
                if (self._WMODl & IO_WMODl_SUB_CLOCK):
                    self._watch_timer_counter += WATCH_TIMER_DIV[self._WMODl & IO_WMODl_WATCH_FAST_MODE] * self._sub_clock_div
                else:
                    self._watch_timer_counter += WATCH_TIMER_DIV[self._WMODl & IO_WMODl_WATCH_FAST_MODE] * WATCH_TIMER_MAIN_CLOCK_DIV
                self._INTW |= IO_INTW_IRQW
        else:
            self._watch_timer_counter = 0

    def _go_vector(self, addr):
        vector = self._ROM.getWord(addr)
        self._EMB = (vector >> 15) & 0x1
        self._ERB = (vector >> 14) & 0x1
        self._PC = vector & self._ROM.getMask()

    def _interrupt(self, IRQn):
        vector_addr = IRQn << 1
        self._stack_push((self._CY << 3) | self._SK)
        self._stack_push((self._IST << 2) | (self._EMB << 1) | self._ERB)
        self._stack_push((self._PC >> 4) & 0xF)
        self._stack_push(self._PC & 0xF)
        self._stack_push((self._EMB << 3) | (self._ERB << 2) | ((self._PC >> 12) & 0x1))
        self._stack_push((self._PC >> 8) & 0xF)
        self._go_vector(vector_addr)
        self._IST += 1
        if (IRQn == VRQ_INTBT):
            if ((self._INTB & IO_INTB_IEBT) == 0):
                self._INTB &= ~IO_INTB_IRQ4
            elif ((self._INTB & IO_INTB_IE4) == 0):
                self._INTB &= ~IO_INTB_IRQBT
        elif (IRQn == VRQ_INTT0):
            self._INTT0 &= ~IO_INTT0_IRQT0
        elif (IRQn == VRQ_INTP0):
            self._INTP0 &= ~IO_INTP0_IRQP0
        elif (IRQn == VRQ_INT0):
            self._INT01 &= ~IO_INT01_IRQ0
        elif (IRQn == VRQ_INT1):
            self._INT01 &= ~IO_INT01_IRQ1

    def _get_interrupt_vector(self):
        IRQn = 0
        if ((self._INTT0 & IO_INTT0_IET0) and (self._INTT0 & IO_INTT0_IRQT0)):
            if (VRQ_INTT0 == self._IPR and self._IST <= 1):
                return VRQ_INTT0
            elif (self._IST == 0):
                IRQn = VRQ_INTT0
        if ((self._INTP0 & IO_INTP0_IEP0) and (self._INTP0 & IO_INTP0_IRQP0)):
            if (VRQ_INTP0 == self._IPR and self._IST <= 1):
                return VRQ_INTP0
            elif (self._IST == 0):
                IRQn = VRQ_INTP0
        if ((self._INT01 & IO_INT01_IE1) and (self._INT01 & IO_INT01_IRQ1)):
            if (VRQ_INT1 == self._IPR and self._IST <= 1):
                return VRQ_INT1
            elif (self._IST == 0):
                IRQn = VRQ_INT1
        if ((self._INT01 & IO_INT01_IE0) and (self._INT01 & IO_INT01_IRQ0)):
            if (VRQ_INT0 == self._IPR and self._IST <= 1):
                return VRQ_INT0
            elif (self._IST == 0):
                IRQn = VRQ_INT0
        if ((self._INTB & IO_INTB_IE4) and (self._INTB & IO_INTB_IRQ4)):
            if (VRQ_INT4 == self._IPR and self._IST <= 1):
                return VRQ_INT4
            elif (self._IST == 0):
                IRQn = VRQ_INT4
        if ((self._INTB & IO_INTB_IEBT) and (self._INTB & IO_INTB_IRQBT)):
            if (VRQ_INTBT == self._IPR and self._IST <= 1):
                return VRQ_INTBT
            elif (self._IST == 0):
                IRQn = VRQ_INTBT
        return IRQn
    

    def clock(self):
        exec_cycles = self._cpu_clock_div
            
        if (self._PCON_MODE == PCC_MODE_NORMAL):
            byte = self._ROM.getByte(self._PC)
            bytes_count = self._execute[byte][1]
            opcode = self._ROM.getBytes(self._PC, bytes_count)
            self._PC += bytes_count
            exec_cycles *= self._execute[byte][0](self, opcode)
            self._instr_counter += 1
            
        elif (((self._INTW & IO_INTW_IRQW) and (self._INTW & IO_INTW_IEW)) |
            ((self._INT2 & IO_INT2_IRQ2) and (self._INT2 & IO_INT2_IE2)) |
            ((self._INT01 & IO_INT01_IRQ0) and (self._INT01 & IO_INT01_IE0) and (self._IM0 & IO_IM0_NOISE_ELIM_DISABLE)) |
            ((self._INT01 & IO_INT01_IRQ1) and (self._INT01 & IO_INT01_IE1)) |
            ((self._INTT0 & IO_INTT0_IRQT0) and (self._INTT0 & IO_INTT0_IET0)) |
            ((self._INTB & IO_INTB_IRQ4) and (self._INTB & IO_INTB_IE4)) |
            ((self._INTB & IO_INTB_IRQBT) and (self._INTB & IO_INTB_IEBT))):
            self._PCON_MODE = PCC_MODE_NORMAL

        self._process_watch_timer(exec_cycles)
        if (not(self._SCMOD & IO_SCMOD_DISABLE_FX)):
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
        if ((self._EMB != 0) or (addr < 0x80)):
            mb = self._EMB * self._SMB
        if (mb == 0):
            return self._RAM[addr]
        elif (mb == 1):
            return self._RAM[((self._PASR + 1) << 8) + addr]
        else:
            io = self._io_tbl.get(0xF00 + addr)
            if (io != None):
                return io[0](self)
            return 0

    def _get_mem_byte(self, addr):
        mb = 15
        if ((self._EMB != 0) or (addr < 0x80)):
            mb = self._EMB * self._SMB
        if (mb == 0):
            addr = addr & 0xFE
            return (self._RAM[addr + 1] << 4) | self._RAM[addr]
        elif (mb == 1):
            addr = ((self._PASR + 1) << 8) + addr
            if (self._PASR == 0x13):
                return self._RAM[addr]
            return (self._RAM[addr | 0x001] << 4) | self._RAM[addr & 0xFFE]
        else:
            addr = 0xF00 + (addr & 0xFE)
            result = 0
            io = self._io_tbl.get(addr + 1)
            if (io != None):
                result = io[0](self) << 4
            io = self._io_tbl.get(addr)
            if (io != None):
                result |= io[0](self)
            return result
            
    def _set_mem(self, addr, value):
        mb = 15
        if ((self._EMB != 0) or (addr < 0x80)):
            mb = self._EMB * self._SMB
        if (mb == 0):
            self._RAM[addr] = value
        elif (mb == 1):
            self._RAM[((self._PASR + 1) << 8) + addr] = value
        else:
            io = self._io_tbl.get(0xF00 + addr)
            if (io != None):
                io[1](self, value)

    def _set_mem_byte(self, addr, value):
        mb = 15
        if ((self._EMB != 0) or (addr < 0x80)):
            mb = self._EMB * self._SMB
        if (mb == 0):
            addr &= 0xFE
            self._RAM[addr] = value & 0xF
            self._RAM[addr + 1] = (value >> 4) & 0xF
        elif (mb == 1):
            addr = ((self._PASR + 1) << 8) + addr
            if (self._PASR == 0x13):
                self._RAM[addr] = value & 0x1F
            else:
                self._RAM[addr & 0xFFE] = value & 0xF
                self._RAM[addr | 1] = (value >> 4) & 0xF
        else:
            addr = 0xF00 + (addr & 0xFE)
            io = self._io_tbl.get(addr)
            if (io != None):
                io[1](self, value & 0xF)
            io = self._io_tbl.get(addr + 1)
            if (io != None):
                io[1](self, value >> 4)

    def _get_ahl(self):
        mb = self._EMB * self._SMB
        if (mb == 0):
            return self._RAM[self._get_rp(RP_HL)]
        elif (mb == 1):
            return self._RAM[((self._PASR + 1) << 8) + self._get_rp(RP_HL)]
        else:
            io = self._io_tbl.get(0xF00 + self._get_rp(RP_HL))
            if (io != None):
                return io[0](self)
            return 0

    def _set_ahl(self, value):
        mb = self._EMB * self._SMB
        if (mb == 0):
            self._RAM[self._get_rp(RP_HL)] = value
        elif (mb == 1):
            self._RAM[((self._PASR + 1) << 8) + self._get_rp(RP_HL)] = value
        else:
            io = self._io_tbl.get(0xF00 + self._get_rp(RP_HL))
            if (io != None):
                io[1](self, value)

    def _get_ahl_byte(self):
        mb = self._EMB * self._SMB
        if (mb == 0):
            addr = self._get_rp(RP_HL) & 0xFE
            return (self._RAM[addr + 1] << 4) | self._RAM[addr]
        elif (mb == 1):
            addr = ((self._PASR + 1) << 8) + self._get_rp(RP_HL)
            if (self._PASR == 0x13):
                return self._RAM[addr]
            return (self._RAM[addr | 0x001] << 4) | self._RAM[addr & 0xFFE]
        else:
            addr = 0xF00 + (self._get_rp(RP_HL) & 0xFE)
            result = 0
            io = self._io_tbl.get(addr + 1)
            if (io != None):
                result = io[0](self) << 4
            io = self._io_tbl.get(addr)
            if (io != None):
                result |= io[0](self)
            return result

    def _set_ahl_byte(self, value):
        mb = self._EMB * self._SMB
        if (mb == 0):
            addr = self._get_rp(RP_HL) & 0xFE
            self._RAM[addr] = value & 0xF
            self._RAM[addr + 1] = value >> 4
        elif (mb == 1):
            addr = ((self._PASR + 1) << 8) + self._get_rp(RP_HL)
            if (self._PASR == 0x13):
                self._RAM[addr] = value & 0x1F
            else:
                self._RAM[addr & 0xFFE] = value & 0xF
                self._RAM[addr | 0x001] = (value >> 4) & 0xF
        else:
            addr = 0xF00 + (self._get_rp(RP_HL) & 0xFE)
            io = self._io_tbl.get(addr)
            if (io != None):
                io[1](self, value & 0xF)
            io = self._io_tbl.get(addr + 1)
            if (io != None):
                io[1](self, value >> 4)

    def _get_hmem(self, opcode):
        addr = (self._get_reg(REG_H) << 4) | (opcode & 0xF)
        mb = self._EMB * self._SMB
        if (mb == 0):
            return self._RAM[addr]
        elif (mb == 1):
            return self._RAM[((self._PASR + 1) << 8) + addr]
        else:
            io = self._io_tbl.get(0xF00 + addr)
            if (io != None):
                return io[0](self)
            return 0

    def _set_hmem(self, opcode, value):
        addr = (self._get_reg(REG_H) << 4) | (opcode & 0xF)
        mb = self._EMB * self._SMB
        if (mb == 0):
            self._RAM[addr] = value
        elif (mb == 1):
            self._RAM[((self._PASR + 1) << 8) + addr] = value
        else:
            io = self._io_tbl.get(0xF00 + addr)
            if (io != None):
                io[1](self, value)

    def _get_memb_al(self, opcode):
        addr = 0xFC0 + ((opcode & 0xF) << 2) | (self._get_reg(REG_L) >> 2)
        io = self._io_tbl.get(addr)
        if (io != None):
            return io[0](self)
        return 0

    def _set_memb_al(self, opcode, value):
        addr = 0xFC0 + ((opcode & 0xF) << 2) | (self._get_reg(REG_L) >> 2)
        io = self._io_tbl.get(addr)
        if (io != None):
            io[1](self, value)

    def _get_mema(self, opcode):
        addr = 0xFB0 + (opcode & 0b01001111)
        io = self._io_tbl.get(addr)
        if (io != None):
            return io[0](self)
        return 0

    def _set_mema(self, opcode, value):
        addr = 0xFB0 + (opcode & 0b01001111)
        io = self._io_tbl.get(addr)
        if (io != None):
            io[1](self, value)

    def _get_reg(self, reg):
        return self._RAM[self._ERB * self._SRB * 8 + reg]

    def _set_reg(self, reg, value):
        self._RAM[self._ERB * self._SRB * 8 + reg] = value

    def _get_rp(self, rp):
        rp_offset = (self._ERB * self._SRB * 8 + (rp & 0x6)) ^ ((rp & 0x1) << 3)
        return (self._RAM[rp_offset + 1] << 4) | self._RAM[rp_offset]

    def _set_rp(self, rp, value):
        rp_offset = (self._ERB * self._SRB * 8 + (rp & 0x6)) ^ ((rp & 0x1) << 3)
        self._RAM[rp_offset] = value & 0xF
        self._RAM[rp_offset + 1] = (value >> 4) & 0xF

    def _stack_push(self, value):
        self._SP = (self._SP - 1) & 0xFF
        sp = self._SP
        self._RAM[sp] = value

    def _stack_push_byte(self, value):
        self._SP = (self._SP - 1) & 0xFF
        sph = self._SP
        self._RAM[sph] = (value >> 4) & 0xF
        self._SP = (self._SP - 1) & 0xFF
        spl = self._SP
        self._RAM[spl] = value & 0xF

    def _stack_pop(self):
        sp = self._SP
        self._SP = (self._SP + 1) & 0xFF
        return self._RAM[sp]

    def _stack_pop_byte(self):
        spl = self._SP
        sph = (self._SP + 1) & 0xFF
        self._SP = (self._SP + 2) & 0xFF
        return (self._RAM[sph] << 4) | self._RAM[spl]

    def _skip_next(self):
        opcode = self._ROM.getByte(self._PC)
        byte_count = self._execute[opcode][1]
        self._PC += byte_count
        return 1 if (byte_count < 3) else 2

    def _execute_11011011(self, opcode):
        return self._execute_11011011_tbl[(opcode >> 14) & 0x1](self, opcode)

    def _execute_11011101(self, opcode):
        return self._execute_11011101_tbl[opcode & 0x7F](self, opcode)
        
    def _execute_11011001(self, opcode):
        return self._execute_11011001_tbl[(opcode >> 3) & 0x1](self, opcode)

    def _execute_11111100(self, opcode):
        return self._execute_11111100_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _execute_11111110(self, opcode):
        return self._execute_11111110_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _execute_11111111(self, opcode):
        return self._execute_11111111_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _execute_11111101(self, opcode):
        return self._execute_11111101_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _execute_11011100(self, opcode):
        return self._execute_11011100_tbl[opcode & 0xFF](self, opcode)

    def _execute_11110101(self, opcode):
        return self._execute_11110101_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _execute_11110110(self, opcode):
        return self._execute_11110110_tbl[(opcode >> 6) & 0x3](self, opcode)
    
    def _execute_11110111(self, opcode):
        return self._execute_11110111_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _execute_11110100(self, opcode):
        return self._execute_11110100_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _execute_11111000(self, opcode):
        return self._execute_11111000_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _execute_11111001(self, opcode):
        return self._execute_11111001_tbl[(opcode >> 6) & 0x3](self, opcode)

    def _br_raddr(self, opcode):
        #0001AAAA
        self._PC += (opcode & 0x0F)
        return 8

    def _br_mraddr(self, opcode):
        #0000AAAA
        self._PC -= (16 - (opcode & 0x0F))
        return 8

    def _ref(self, opcode):
        #TTTTTTTT
        taddr = (opcode & 0xF0) | ((opcode << 1) & 0x0E)
        byte = self._ROM.getByte(taddr)
        if ((byte & 0xC0) == 0x00):
            self._PC = self._ROM.getWord(taddr) & self._ROM.getMask()
            return 3
        if ((byte & 0xC0) == 0x40):
            self._stack_push(0)
            self._stack_push((self._EMB << 1) | self._ERB)
            self._stack_push((self._PC >> 4) & 0x000F)
            self._stack_push(self._PC & 0x000F)
            self._stack_push((self._PC >> 12) & 0x0003)
            self._stack_push((self._PC >> 8) & 0x000F)
            self._PC = self._ROM.getWord(taddr) & self._ROM.getMask()
            return 3
        bytes_count = self._execute[byte][1]
        execute_time = 1
        if (bytes_count == 1):
            opcode = byte
            execute_time += self._execute[byte][0](self, opcode)
            byte = self._ROM.getByte(taddr + 1)
            execute_time += self._execute[byte][0](self, opcode)
        else:
            opcode = self._ROM.getBytes(taddr, bytes_count)
            execute_time += self._execute[byte][0](self, opcode)
        return execute_time

    def _calls_addr11(self, opcode):
        #11101AAA AAAAAAAA
        self._stack_push(0)
        self._stack_push((self._EMB << 1) | self._ERB)
        self._stack_push((self._PC >> 4) & 0x000F)
        self._stack_push(self._PC & 0x000F)
        self._stack_push((self._PC >> 12) & 0x0003)
        self._stack_push((self._PC >> 8) & 0x000F)
        self._PC = opcode & 0x7FF
        return 2

    def _pop_rp(self, opcode):
        #00101PP0
        self._set_rp(opcode & 0x6, self._stack_pop_byte())
        return 1

    def _push_rp(self, opcode):
        #00101PP1
        self._stack_push_byte(self._get_rp(opcode & 0x6))
        return 1

    def _jps_addr12(self, opcode):
        #1001AAAA AAAAAAAA
        self._PC = ((self._PC & 0xF000) | (opcode & 0xFFF)) & self._ROM.getMask()
        return 2

    def _ads_a_im(self, opcode):
        #1010DDDD
        new_A = self._get_reg(REG_A) + (opcode & 0xF)
        self._set_reg(REG_A, new_A & 0xF)
        if (new_A > 15):
            return 1 + self._skip_next()
        return 1

    def _ld_a_im(self, opcode):
        #1011DDDD
        self._set_reg(REG_A, opcode & 0xF)
        cycle_count = 1
        opcode = self._ROM.getByte(self._PC)
        while (((opcode >> 4) == 0b1011) or (opcode == 0b10000001)):
            cycle_count += 1
            self._PC += self._execute[opcode][1]
            opcode = self._ROM.getByte(self._PC)
        return cycle_count

    def _cpse_a_ahl(self, opcode):
        #00111000
        if (self._get_reg(REG_A) == self._get_ahl()):
            return 1 + self._skip_next()
        return 1

    def _incs_da(self, opcode):
        #11001010 AAAAAAAA
        d = opcode & 0x00FF
        new_da = (self._get_mem(d) + 1) & 0xF
        self._set_mem(d, new_da)
        if (new_da == 0):
            return 2 + self._skip_next()
        return 2

    def _bitr_da_bit(self, opcode):
        #11BB0000 AAAAAAAA
        a = opcode & 0x00FF
        new_da = self._get_mem(a) & ~(1 << ((opcode >> 12) & 0x3))
        self._set_mem(a, new_da)
        return 2

    def _bits_da_bit(self, opcode):
        #11BB0001 AAAAAAAA
        d = opcode & 0x00FF
        new_da = self._get_mem(d) | (1 << ((opcode >> 12) & 0x3))
        self._set_mem(d, new_da)
        return 2

    def _btsf_da_bit(self, opcode):
        #11BB0010 AAAAAAAA
        if (not(self._get_mem(opcode & 0xFF) & (1 << ((opcode >> 12) & 0x3)))):
            return 2 + self._skip_next()
        return 2

    def _btst_da_bit(self, opcode):
        #11BB0011 AAAAAAAA
        if (self._get_mem(opcode & 0xFF) & (1 << ((opcode >> 12) & 0x3))):
            return 2 + self._skip_next()
        return 2

    def _ld_ea_imm(self, opcode):
        #10000001 DDDDDDDD
        self._set_rp(RP_EA, opcode & 0xFF)
        cycle_count = 2
        opcode = self._ROM.getByte(self._PC)
        while (((opcode >> 4) == 0b1011) or (opcode == 0b10000001)):
            cycle_count += 1
            self._PC += self._execute[opcode][1]
            opcode = self._ROM.getByte(self._PC)
        return cycle_count

    def _incs_rrb(self, opcode):
        #10000RR0
        new_rp = (self._get_rp(opcode & 0x6) + 1) & 0xFF
        self._set_rp(opcode & 0x6, new_rp)
        if (new_rp == 0):
            return 1 + self._skip_next()
        return 1

    def _ld_hl_imm(self, opcode):
        #10000011 DDDDDDDD
        self._set_rp(RP_HL, opcode & 0xFF)
        cycle_count = 2
        opcode = self._ROM.getByte(self._PC)
        while (opcode == 0b10000011):
            cycle_count += 1
            self._PC += self._execute[opcode][1]
            opcode = self._ROM.getByte(self._PC)
        return cycle_count

    def _ld_wx_imm(self, opcode):
        #10000101 DDDDDDDD
        self._set_rp(RP_WX, opcode & 0xFF)
        return 2

    def _ld_yz_imm(self, opcode):
        #110000111 DDDDDDDD
        self._set_rp(RP_YZ, opcode & 0xFF)
        return 2

    def _and_a_ahl(self, opcode):
        #00111001
        self._set_reg(REG_A, self._get_reg(REG_A) & self._get_ahl())
        return 1

    def _ld_da_ea(self, opcode):
        #11001101 AAAAAAAA
        d = opcode & 0xFE
        self._set_mem_byte(opcode & 0xFF, self._get_rp(RP_EA))
        return 2

    def _ld_da_a(self, opcode):
        #10001001 AAAAAAAA
        d = opcode & 0xFF
        self._set_mem(d, self._get_reg(REG_A))
        return 2

    def _rrc_a(self, opcode):
        #10001000
        new_CY = self._get_reg(REG_A) & 0x1
        self._set_reg(REG_A, (self._get_reg(REG_A) >> 1) | (self._CY << 3))
        self._CY = new_CY
        return 1

    def _or_a_ahl(self, opcode):
        #00111010
        self._set_reg(REG_A, self._get_reg(REG_A) | self._get_ahl())
        return 1

    def _ld_ea_da(self, opcode):
        #11001110 AAAAAAAA
        d = opcode & 0xFE
        self._set_rp(RP_EA, self._get_mem_byte(d))
        return 2

    def _ld_a_da(self, opcode):
        #10001100 AAAAAAAA
        d = opcode & 0xFF
        self._set_reg(REG_A, self._get_mem(d))
        return 2

    def _sbs_a_ahl(self, opcode):
        #00111101
        new_A = self._get_reg(REG_A) - self._get_ahl()
        self._set_reg(REG_A, new_A & 0xF)
        if (new_A < 0):
            return 1 + self._skip_next()
        return 1

    def _adc_a_ahl(self, opcode):
        #00111110
        new_A = self._get_reg(REG_A) + self._get_ahl() + self._CY
        self._set_reg(REG_A, new_A & 0xF)
        self._CY = new_A > 15
        opcode = self._ROM.getByte(self._PC)
        if ((opcode >> 4) == 0b1010):
            if (self._CY):
                return 1 + self._skip_next()
            self._PC += 1
            self._set_reg(REG_A, (self._get_reg(REG_A) + (opcode & 0xF)) & 0xF)
            return 2
        return 1

    def _jp_addr14(self, opcode):
        #11011011 00AAAAAA AAAAAAAA
        self._PC = opcode & self._ROM.getMask()
        return 1

    def _call_addr14(self, opcode):
        #11011011 01AAAAAA AAAAAAAA
        self._stack_push(0)
        self._stack_push((self._EMB << 1) | self._ERB)
        self._stack_push((self._PC >> 4) & 0x000F)
        self._stack_push(self._PC & 0x000F)
        self._stack_push((self._PC >> 12) & 0x0003)
        self._stack_push((self._PC >> 8) & 0x000F)
        self._PC = opcode & self._ROM.getMask()
        return 3

    def _xor_a_ahl(self, opcode):
        #00111011
        new_A = self._get_reg(REG_A) ^ self._get_ahl()
        self._set_reg(REG_A, new_A)
        return 1

    def _xch_ea_da(self, opcode):
        #11001111 AAAAAAAA
        d = opcode & 0xFF
        buf_ea = self._get_rp(RP_EA)
        self._set_rp(RP_EA, self._get_mem_byte(d))
        self._set_mem_byte(d, buf_ea)
        return 2

    def _xch_a_da(self, opcode):
        #01111001 AAAAAAAA
        a = opcode & 0xFF
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_mem(a))
        self._set_mem(a, buf_A)
        return 2

    def _sbc_a_ahl(self, opcode):
        #00111100
        new_A = self._get_reg(REG_A) - self._get_ahl() - self._CY
        self._set_reg(REG_A, new_A & 0xF)
        self._CY = new_A < 0
        opcode = self._ROM.getByte(self._PC)
        if ((opcode >> 4) == 0b1010):
            if (self._CY):
                self._PC += 1
                self._set_reg(REG_A, (self._get_reg(REG_A) + (opcode & 0xF)) & 0xF)
                return 2
            return 1 + self._skip_next()
        return 1

    def _ads_ea_imm(self, opcode):
        #11001001 DDDDDDDD
        new_EA = self._get_rp(RP_EA) + (opcode & 0xFF)
        self._set_rp(RP_EA, new_EA & 0xFF)
        if (new_EA > 255):
            return 2 + self._skip_next()
        return 2

    def _incs_r(self, opcode):
        #01011RRR
        reg = opcode & 0x7
        new_value = (self._get_reg(reg) + 1) & 0xF
        self._set_reg(reg, new_value)
        if (new_value == 0):
            return 1 + self._skip_next()
        return 1

    def _decs_r(self, opcode):
        #01001RRR
        reg = opcode & 0x7
        new_value = (self._get_reg(reg) - 1) & 0xF
        self._set_reg(reg, new_value)
        if (new_value == 0xF):
            return 1 + self._skip_next()
        return 1

    def _ldc_ea_aea(self, opcode):
        #11001000
        addr = (self._PC & 0xFF00) | self._get_rp(RP_EA)
        self._set_rp(RP_EA, self._ROM.getByte(addr))
        return 3

    def _ads_a_ahl(self, opcode):
        #00111111
        new_A = self._get_reg(REG_A) + self._get_ahl()
        self._set_reg(REG_A, new_A & 0xF)
        if (new_A > 15):
            return 1 + self._skip_next()
        return 1

    def _ldc_ea_awx(self, opcode):
        #11001100
        addr = (self._PC & 0xFF00) | self._get_rp(RP_WX)
        self._set_rp(RP_EA, self._ROM.getByte(addr))
        return 3

    def _ccf(self, opcode):
        #11010110
        self._CY = not self._CY
        return 1

    def _btst_cy(self, opcode):
        #11010111
        if (self._CY):
            return 1 + self._skip_next()
        return 1

    def _xch_a_ra(self, opcode):
        #01101RRR
        reg = opcode & 0x7
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_reg(reg))
        self._set_reg(reg, buf_A)
        return 1

    def _sret(self, opcode):
        #11100101
        self._PC = self._stack_pop() << 8
        self._PC |= self._stack_pop() << 12 & 0x1000
        self._PC |= self._stack_pop()
        self._PC |= self._stack_pop() << 4
        stack_value = self._stack_pop()
        self._EMB = (stack_value >> 1) & 0x1
        self._ERB = stack_value & 0x1
        self._stack_pop()
        self._PC &= self._ROM.getMask()
        return 3 + self._skip_next()

    def _ld_a_ahl(self, opcode):
        #10001101
        self._set_reg(REG_A, self._get_ahl())
        return 1

    def _ldi_a_ahl(self, opcode):
        #10001010
        self._set_reg(REG_A, self._get_ahl())
        new_L = (self._get_reg(REG_L) + 1) & 0xF
        self._set_reg(REG_L, new_L)
        if (new_L == 0):
            return 2 + self._skip_next()
        return 1

    def _ldd_a_ahl(self, opcode):
        #10001011
        self._set_reg(REG_A, self._get_ahl())
        new_L = (self._get_reg(REG_L) - 1) & 0xF
        self._set_reg(REG_L, new_L)
        if (new_L == 0xF):
            return 2 + self._skip_next()
        return 1

    def _ld_a_awx(self, opcode):
        #10001110
        self._set_reg(REG_A, self._RAM[self._get_rp(RP_WX)])
        return 1

    def _ld_a_awl(self, opcode):
        #10001111
        wl = (self._get_reg(REG_W) << 4) | self._get_reg(REG_L)
        self._set_reg(REG_A, self._RAM[wl])
        return 1

    def _bitr_cy(self, opcode):
        #11100110
        self._CY = 0
        return 1

    def _bits_cy(self, opcode):
        #11100111
        self._CY = 1
        return 1

    def _ld_ahl_a(self, opcode):
        #11000100
        self._set_ahl(self._get_reg(REG_A))
        return 1

    def _xch_a_ahl(self, opcode):
        #01111101
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_ahl())
        self._set_ahl(buf_A)
        return 1

    def _xch_a_ahli(self, opcode):
        #01111010
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_ahl())
        self._set_ahl(buf_A)
        new_L = (self._get_reg(REG_L) + 1) & 0xF
        self._set_reg(REG_L, new_L)
        if (new_L == 0):
            return 2 + self._skip_next()
        return 1

    def _xch_a_ahld(self, opcode):
        #01111011
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._get_ahl())
        self._set_ahl(buf_A)
        new_L = (self._get_reg(REG_L) - 1) & 0xF
        self._set_reg(REG_L, new_L)
        if (new_L == 0xF):
            return 2 + self._skip_next()
        return 1

    def _xch_a_awx(self, opcode):
        #01111110
        buf_A = self._get_reg(REG_A)
        self._set_reg(REG_A, self._RAM[self._get_rp(RP_WX)])
        self._RAM[self._get_rp(RP_WX)] = buf_A
        return 1

    def _xch_a_awl(self, opcode):
        #01111111
        buf_A = self._get_reg(REG_A)
        wl = (self._get_reg(REG_W) << 4) | self._get_reg(REG_L)
        self._set_reg(REG_A, self._RAM[wl])
        self._RAM[wl] = buf_A
        return 1

    def _ret(self, opcode):
        #11000101    
        self._PC = self._stack_pop() << 8
        self._PC |= self._stack_pop() << 12 & 0x1000
        self._PC |= self._stack_pop()
        self._PC |= self._stack_pop() << 4
        stack_value = self._stack_pop()
        self._EMB = (stack_value >> 1) & 0x1
        self._ERB = stack_value & 0x1
        self._stack_pop()
        self._PC &= self._ROM.getMask()
        return 3

    def _iret(self, opcode):
        #11010101
        self._PC = self._stack_pop() << 8
        stack_value = self._stack_pop()
        self._PC |= stack_value << 12 & 0x1000
        self._EMB = stack_value >> 3
        self._ERB = (stack_value >> 2) & 0x1
        self._PC |= self._stack_pop()
        self._PC |= self._stack_pop() << 4
        stack_value = self._stack_pop()
        self._IST = stack_value >> 2
        self._EMB = (stack_value >> 1) & 0x1
        self._ERB = stack_value & 0x1
        stack_value = self._stack_pop()
        self._CY = (stack_value >> 3) & 0x1
        self._SK = stack_value & 0x7
        self._PC &= self._ROM.getMask()
        return 3

    def _jr_aea(self, opcode):
        #11011101 01100000
        self._PC = ((self._PC & 0xFF00) | (self._get_reg(REG_E) << 4) | self._get_reg(REG_A)) & self._ROM.getMask()
        return 3

    def _incs_ahl(self, opcode):
        #11011101 01100010
        new_ahl = (self._get_ahl() + 1) & 0xF
        self._set_ahl(new_ahl)
        if (new_ahl == 0):
            return 2 + self._skip_next()
        return 2

    def _jr_awx(self, opcode):
        #11011101 01100100
        self._PC = ((self._PC & 0xFF00) | (self._get_reg(REG_W) << 4) | self._get_reg(REG_X)) & self._ROM.getMask()
        return 3

    def _br_yzde(self, opcode):
        #10011001 | 00000101
        self._PC = ((self._get_reg(REG_Y) << 12) | (self._get_reg(REG_Z) << 8) | (self._get_reg(REG_W) << 4) | self._get_reg(REG_X)) & self._ROM.getMask()
        return 3

    def _pop_sb(self, opcode):
        #11011101 01100110
        self._SRB = self._stack_pop()
        self._SMB = self._stack_pop()
        return 2

    def _push_sb(self, opcode):
        #11011101 01100111
        self._stack_push(self._SMB)
        self._stack_push(self._SRB)
        return 2

    def _cpse_a_r(self, opcode):
        #11011101 01101RRR
        if (self._get_reg(REG_A) == self._get_reg(opcode & 0x7)):
            return 2 + self._skip_next()
        return 2

    def _smb_n(self, opcode):
        #11011101 0100NNNN
        self._SMB = opcode & 0xF
        return 2

    def _srb_n(self, opcode):
        #11011101 010100NN
        self._SRB = opcode & 0x3
        return 2

    def _and_a_im(self, opcode):
        #11011101 0001DDDD
        self._set_reg(REG_A, self._get_reg(REG_A) & opcode)
        return 2

    def _or_a_im(self, opcode):
        #11011101 0010DDDD
        self._set_reg(REG_A, (self._get_reg(REG_A) | opcode) & 0xF)
        return 2

    def _xor_a_im(self, opcode):
        #11011101 0011DDDD
        self._set_reg(REG_A, (self._get_reg(REG_A) ^ opcode) & 0xF)
        return 2

    def _cpse_ahl_im(self, opcode):
        #11011101 0111DDDD
        if (self._get_ahl() == (opcode & 0xF)):
            return 2 + self._skip_next()
        return 2

    def _ld_ra_a(self, opcode):
        #11011101 00000RRR
        self._set_reg(opcode & 0x7, self._get_reg(REG_A))
        return 2

    def _ld_a_r(self, opcode):
        #11011101 00001RRR
        self._set_reg(REG_A, self._get_reg(opcode & 0x7))
        return 2

    def _cpse_r_im(self, opcode):
        #11011001 DDDD0RRR
        if (self._get_reg(opcode & 0x7) == ((opcode >> 4) & 0xF)):
            return 2 + self._skip_next()
        return 2

    def _ld_ra_im(self, opcode):
        #11011001 DDDD1RRR
        self._set_reg(opcode & 0x7, (opcode >> 4) & 0xF)
        return 2

    def _ldb_ahda_bit_cy(self, opcode):
        #11111100 00BBAAAA
        b = (opcode >> 4) & 0x3
        if (self._CY):
            self._set_hmem(opcode, self._get_hmem(opcode) | (1 << b))
        else:
            self._set_hmem(opcode, self._get_hmem(opcode) & ~(1 << b))
        return 2

    def _ldb_memb_al_cy(self, opcode):
        #11111100 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        if (self._CY):
            self._set_memb_al(opcode, self._get_memb_al(opcode) | (1 << b))
        else:
            self._set_memb_al(opcode, self._get_memb_al(opcode) & ~(1 << b))
        return 2

    def _ldb_mema_bit_cy(self, opcode):
        #11111100 1XBBAAAA
        b = (opcode >> 4) & 0x3
        if (self._CY):
            self._set_mema(opcode, self._get_mema(opcode) | (1 << b))
        else:
            self._set_mema(opcode, self._get_mema(opcode) & ~(1 << b))
        return 2

    def _bitr_ahda_bit(self, opcode):
        #11111110 00BBAAAA
        b = (opcode >> 4) & 0x3
        self._set_hmem(opcode, self._get_hmem(opcode) & ~(1 << b))
        return 2

    def _bitr_memb_al(self, opcode):
        #11111110 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        self._set_memb_al(opcode, self._get_memb_al(opcode) & ~(1 << b))
        return 2

    def _bitr_mema_bit(self, opcode):
        #11111110 1XBBAAAA
        b = (opcode >> 4) & 0x3
        self._set_mema(opcode, self._get_mema(opcode) & ~(1 << b))
        return 2

    def _bits_ahda_bit(self, opcode):
        #11111111 00BBAAAA
        b = (opcode >> 4) & 0x3
        self._set_hmem(opcode, self._get_hmem(opcode) | (1 << b))
        return 2

    def _bits_memb_al(self, opcode):
        #11111111 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        self._set_memb_al(opcode, self._get_memb_al(opcode) | (1 << b))
        return 2

    def _bits_mema_bit(self, opcode):
        #11111111 1XBBAAAA
        b = (opcode >> 4) & 0x3
        self._set_mema(opcode, self._get_mema(opcode) | (1 << b))
        return 2

    def _btstz_ahda_bit(self, opcode):
        #11111101 00BBAAAA
        b = (opcode >> 4) & 0x3
        mem = self._get_hmem(opcode) 
        if (mem & (1 << b)):
            self._set_hmem(opcode, mem & ~(1 << b))
            return 2 + self._skip_next()
        return 2

    def _btstz_memb_al(self, opcode):
        #11111101 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        mem = self._set_memb_al(opcode) 
        if (mem & (1 << b)):
            self._set_memb_al(opcode, mem & ~(1 << b))
            return 2 + self._skip_next()
        return 2

    def _btstz_mema_bit(self, opcode):
        #11111101 1XBBAAAA
        b = (opcode >> 4) & 0x3
        mem = self._get_mema(opcode) 
        if (mem & (1 << b)):
            self._set_mema(opcode, mem & ~(1 << b))
            return 2 + self._skip_next()
        return 2

    def _ld_ahl_ea(self, opcode):
        #11011100 00000000
        self._set_ahl_byte(self._get_rp(RP_EA))
        return 2

    def _xch_ea_ahl(self, opcode):
        #11011100 00000001
        xa = self._get_rp(RP_EA)
        self._set_rp(RP_EA, self._get_ahl_byte())
        self._set_ahl_byte(xa)
        return 2

    def _ld_ea_ahl(self, opcode):
        #11011100 00001000
        self._set_rp(RP_EA, self._get_ahl_byte())
        return 2

    def _cpse_ea_ahl(self, opcode):
        #11011100 00001001
        if (self._get_rp(RP_EA) == self._get_ahl_byte()):
            return 2 + self._skip_next()
        return 2

    def _xch_ea_rrb(self, opcode):
        #11011100 11100RR0
        xa = self._get_rp(RP_EA)
        self._set_rp(RP_EA, self._get_rp(opcode & 0x6))
        self._set_rp(opcode & 0x6, xa)
        return 2

    def _cpse_ea_rr(self, opcode):
        #11011100 11101RR0
        if (self._get_rp(RP_EA) == self._get_rp(opcode & 0x6)):
            return 2 + self._skip_next()
        return 2

    def _ld_rrb_ea(self, opcode):
        #11011100 11110RR0
        self._set_rp(opcode & 0x6, self._get_rp(RP_EA))
        return 2

    def _ld_ea_rrb(self, opcode):
        #11011100 11111RR0
        self._set_rp(RP_EA, self._get_rp(opcode & 0x6))
        return 2

    def _decs_rr(self, opcode):
        #11011100 11011RR0
        new_value = (self._get_rp(opcode & 0x6) - 1) & 0xFF
        self._set_rp(opcode & 0x6, new_value)
        if (new_value == 0xFF):
            return 2 + self._skip_next()
        return 2

    def _and_rrb_ea(self, opcode):
        #11011100 00010RR0
        self._set_rp(opcode & 0x6, self._get_rp(opcode & 0x6) & self._get_rp(RP_EA))
        return 2

    def _and_ea_rr(self, opcode):
        #11011100 00011RR0
        self._set_rp(RP_EA, self._get_rp(opcode & 0x6) & self._get_rp(RP_EA))
        return 2

    def _or_rrb_ea(self, opcode):
        #11011100 00100RR0
        self._set_rp(opcode & 0x6, self._get_rp(opcode & 0x6) | self._get_rp(RP_EA))
        return 2

    def _or_ea_rr(self, opcode):
        #11011100 00101RR0
        self._set_rp(RP_EA, self._get_rp(opcode & 0x6) | self._get_rp(RP_EA))
        return 2

    def _xor_rrb_ea(self, opcode):
        #11011100 00110RR0
        self._set_rp(opcode & 0x6, self._get_rp(opcode & 0x6) ^ self._get_rp(RP_EA))
        return 2

    def _xor_ea_rr(self, opcode):
        #11011100 00111RR0
        self._set_rp(RP_EA, self._get_rp(opcode & 0x6) ^ self._get_rp(RP_EA))
        return 2

    def _ads_rrb_ea(self, opcode):
        #11011100 10010RR0
        new_value = self._get_rp(opcode & 0x6) + self._get_rp(RP_EA)
        self._set_rp(opcode & 0x6, new_value & 0xFF)
        if (new_value > 255):
            return 2 + self._skip_next()
        return 2

    def _ads_ea_rr(self, opcode):
        #11011100 10011RR0
        new_value = self._get_rp(opcode & 0x6) + self._get_rp(RP_EA)
        self._set_rp(RP_EA, new_value & 0xFF)
        if (new_value > 255):
            return 2 + self._skip_next()
        return 2

    def _adc_rrb_ea(self, opcode):
        #11011100 10100RR0
        new_value = self._get_rp(opcode & 0x6) + self._get_rp(RP_EA) + self._CY
        self._set_rp(opcode & 0x6, new_value & 0xFF)
        self._CY = new_value > 255
        return 2

    def _adc_ea_rr(self, opcode):
        #11011100 10101RR0
        new_value = self._get_rp(opcode & 0x6) + self._get_rp(RP_EA) + self._CY
        self._set_rp(RP_EA, new_value & 0xFF)
        self._CY = new_value > 255
        return 2

    def _sbs_rrb_ea(self, opcode):
        #11011100 10110RR0
        new_value = self._get_rp(opcode & 0x6) - self._get_rp(RP_EA)
        self._set_rp(opcode & 0x6, new_value & 0xFF)
        if (new_value < 0):
            return 2 + self._skip_next()
        return 2

    def _sbs_ea_rr(self, opcode):
        #11011100 10111RR0
        new_value = self._get_rp(RP_EA) - self._get_rp(opcode & 0x6)
        self._set_rp(RP_EA, new_value & 0xFF)
        if (new_value < 0):
            return 2 + self._skip_next()
        return 2

    def _sbc_rrb_ea(self, opcode):
        #11011100 11000RR0
        new_value = self._get_rp(opcode & 0x6) - self._get_rp(RP_EA) - self._CY
        self._set_rp(opcode & 0x6, new_value & 0xFF)
        self._CY = new_value < 0
        return 2

    def _sbc_ea_rr(self, opcode):
        #11011100 11001RR0
        new_value = self._get_rp(RP_EA) - self._get_rp(opcode & 0x6) - self._CY
        self._set_rp(RP_EA, new_value & 0xFF)
        self._CY = new_value < 0
        return 2

    def _band_cy_ahda_bit(self, opcode):
        #11110101 00BBAAAA
        b = (opcode >> 4) & 0x3
        self._CY &= (self._get_hmem(opcode) >> b) & 0x1
        return 2

    def _band_cy_memb_al(self, opcode):
        #11110101 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        self._CY &= (self._get_memb_al(opcode) >> b) & 0x1
        return 2

    def _band_cy_mema_bit(self, opcode):
        #11110101 1XBBAAAA
        b = (opcode >> 4) & 0x3
        self._CY &= (self._get_mema(opcode) >> b) & 0x1
        return 2

    def _bor_cy_ahda_bit(self, opcode):
        #11110110 00BBAAAA
        b = (opcode >> 4) & 0x3
        self._CY |= (self._get_hmem(opcode) >> b) & 0x1
        return 2

    def _bor_cy_memb_al(self, opcode):
        #11110110 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        self._CY |= (self._get_memb_al(opcode) >> b) & 0x1
        return 2

    def _bor_cy_mema_bit(self, opcode):
        #11110110 1XBBAAAA
        b = (opcode >> 4) & 0x3
        self._CY |= (self._get_mema(opcode) >> b) & 0x1
        return 2

    def _bxor_cy_ahda_bit(self, opcode):
        #11110111 00BBAAAA
        b = (opcode >> 4) & 0x3
        self._CY ^= (self._get_hmem(opcode) >> b) & 0x1
        return 2

    def _bxor_cy_memb_al(self, opcode):
        #11110111 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        self._CY ^= (self._get_memb_al(opcode) >> b) & 0x1
        return 2

    def _bxor_cy_mema_bit(self, opcode):
        #11110111 1XBBAAAA
        b = (opcode >> 4) & 0x3
        self._CY ^= (self._get_mema(opcode) >> b) & 0x1
        return 2

    def _ldb_cy_ahda_bit(self, opcode):
        #11110100 00BBAAAA
        b = (opcode >> 4) & 0x3
        self._CY = (self._get_hmem(opcode) >> b) & 0x1
        return 2

    def _ldb_cy_memb_al(self, opcode):
        #11110100 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        self._CY = (self._get_memb_al(opcode) >> b) & 0x1
        return 2

    def _ldb_cy_mema_bit(self, opcode):
        #11110100 1XBBAAAA
        b = (opcode >> 4) & 0x3
        self._CY = (self._get_mema(opcode) >> b) & 0x1
        return 2

    def _btsf_ahda_bit(self, opcode):
        #11111000 00BBAAAA
        b = (opcode >> 4) & 0x3
        if (not((self._get_hmem(opcode) >> b) & 0x1)):
            return 2 + self._skip_next()
        return 2

    def _btsf_memb_al(self, opcode):
        #11111000 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        if (not((self._get_memb_al(opcode) >> b) & 0x1)):
            return 2 + self._skip_next()
        return 2

    def _btsf_mema_bit(self, opcode):
        #11111000 1XBBAAAA
        b = (opcode >> 4) & 0x3
        if (not((self._get_mema(opcode) >> b) & 0x1)):
            return 2 + self._skip_next()
        return 2

    def _btst_ahda_bit(self, opcode):
        #11111001 00BBAAAA
        b = (opcode >> 4) & 0x3
        if ((self._get_hmem(opcode) >> b) & 0x1):
            return 2 + self._skip_next()
        return 2

    def _btst_memb_al(self, opcode):
        #11111001 0100AAAA
        b = self._get_reg(REG_L) & 0x3
        if ((self._get_memb_al(opcode) >> b) & 0x1):
            return 2 + self._skip_next()
        return 2

    def _btst_mema_bit(self, opcode):
        #11111001 1XBBAAAA
        b = (opcode >> 4) & 0x3
        if ((self._get_mema(opcode) >> b) & 0x1):
            return 2 + self._skip_next()
        return 2

    def _dummy(self, opcode):
        print("undefined opcode")
        return 0
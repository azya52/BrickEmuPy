from .rom import ROM
from .E0C6200sound import E0C6200sound

OSC1_CLOCK = 32768

TIMER_CLOCK_DIV = OSC1_CLOCK / 256
STOPWATCH_CLOCK_DIV = OSC1_CLOCK / 100
PTIMER_CLOCK_DIV = [0, 0, OSC1_CLOCK / 256, OSC1_CLOCK / 512, OSC1_CLOCK / 1024, OSC1_CLOCK / 2048, OSC1_CLOCK / 4096, OSC1_CLOCK / 8192]

RAM_SIZE = 0x300
VRAM_SIZE = 0x0A0
VRAM_PART1_OFFSET = 0xE00
VRAM_PART2_OFFSET = 0xE80
VRAM_PART_SIZE = 0x050
IORAM_OFFSET = 0xF00
IORAM_SIZE = 0x07F

EMPTY_VRAM = tuple([0] * VRAM_SIZE)
FULL_VRAM = tuple([1] * VRAM_SIZE)

IO_IT1 = 8
IO_IT2 = 4
IO_IT8 = 2
IO_IT32 = 1
IO_ISW0 = 2
IO_ISW1 = 1
IO_IPT = 1
IO_ISIO = 1
IO_IK0 = 1
IO_IK1 = 1
IO_EIT1 = 8
IO_EIT2 = 4
IO_EIT8 = 2
IO_EIT32 = 1
IO_EISW1 = 2
IO_EISW0 = 1
IO_EIPT = 1
IO_EISIO = 1
IO_EIK03 = 8
IO_EIK02 = 4
IO_EIK01 = 2
IO_EIK00 = 1
IO_EIK13 = 8
IO_EIK12 = 4
IO_EIK11 = 2
IO_EIK10 = 1
IO_TM3 = 8
IO_TM2 = 4
IO_TM1 = 2
IO_TM0 = 1
IO_TM7 = 8
IO_TM6 = 4
IO_TM5 = 2
IO_TM4 = 1
IO_SWL3 = 8
IO_SWL2 = 4
IO_SWL1 = 2
IO_SWL0 = 1
IO_SWH3 = 8
IO_SWH2 = 4
IO_SWH1 = 2
IO_SWH0 = 1
IO_PT3 = 8
IO_PT2 = 4
IO_PT1 = 2
IO_PT0 = 1
IO_PT7 = 8
IO_PT6 = 4
IO_PT5 = 2
IO_PT4 = 1
IO_RD3 = 8
IO_RD2 = 4
IO_RD1 = 2
IO_RD0 = 1
IO_RD7 = 8
IO_RD6 = 4
IO_RD5 = 2
IO_RD4 = 1
IO_SD3 = 8
IO_SD2 = 4
IO_SD1 = 2
IO_SD0 = 1
IO_SD7 = 8
IO_SD6 = 4
IO_SD5 = 2
IO_SD4 = 1
IO_K03 = 8
IO_K02 = 4
IO_K01 = 2
IO_K00 = 1
IO_DFK03 = 8
IO_DFK02 = 4
IO_DFK01 = 2
IO_DFK00 = 1
IO_K13 = 8
IO_K12 = 4
IO_K11 = 2
IO_K10 = 1
IO_R03 = 8
IO_R02 = 4
IO_R01 = 2
IO_R00 = 1
IO_R13 = 8
IO_R12 = 4
IO_R11 = 2
IO_R10 = 1
IO_R23 = 8
IO_R22 = 4
IO_R21 = 2
IO_R20 = 1
IO_R33 = 8
IO_R32 = 4
IO_R31 = 2
IO_R30 = 1
IO_R43 = 8
IO_R42 = 4
IO_R41 = 2
IO_R40 = 1
IO_P03 = 8
IO_P02 = 4
IO_P01 = 2
IO_P00 = 1
IO_P13 = 8
IO_P12 = 4
IO_P11 = 2
IO_P10 = 1
IO_P23 = 8
IO_P22 = 4
IO_P21 = 2
IO_P20 = 1
IO_P33 = 8
IO_P32 = 4
IO_P31 = 2
IO_P30 = 1
IO_CLKCHG = 8
IO_OSCC = 4
IO_VSC1 = 2
IO_VSC0 = 1
IO_ALOFF = 8
IO_ALON = 4
IO_LDUTY = 2
IO_HLMOD = 1
IO_LC3 = 8
IO_LC2 = 4
IO_LC1 = 2
IO_LC0 = 1
IO_SVDDT = 8
IO_SVDON = 4
IO_SVC1 = 2
IO_SVC0 = 1
IO_SHOTPW = 8
IO_BZFQ = 7
IO_BZFQ2 = 4
IO_BZFQ1 = 2
IO_BZFQ0 = 1
IO_BZSHOT = 8
IO_ENVRST = 4
IO_ENVRT = 2
IO_ENVON = 1
IO_TMRST = 2
IO_WDRST = 1
IO_SWRST = 2
IO_SWRUN = 1
IO_PTRST = 2
IO_PTRUN = 1
IO_PTCOUT = 8
IO_PTC = 7 
IO_PTC2 = 4
IO_PTC1 = 2
IO_PTC0 = 1
IO_SCTRG = 8
IO_SEN = 4
IO_SCS1 = 2
IO_SCS0 = 1
IO_HZR3 = 8
IO_HZR2 = 4
IO_HZR1 = 2
IO_HZR0 = 1
IO_IOC3 = 8
IO_IOC2 = 4
IO_IOC1 = 2
IO_IOC0 = 1
IO_PUP3 = 8
IO_PUP2 = 4
IO_PUP1 = 2
IO_PUP0 = 1


class E0C6200():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = E0C6200sound(OSC1_CLOCK)

        self._port_pullup = mask['port_pullup']

        self._p3_dedicated = mask['p3_dedicated']
        
        self._init_registers()

        self._OSC1_clock_div = clock / OSC1_CLOCK

        self._OSC1_counter = 0
        self._timer_counter = 0
        self._ptimer_counter = 0
        self._stopwatch_counter = 0
        self._execution_counter = 0
        self._instr_counter = 0

        self._if_delay = False

        self._RESET = 0

        self._io_tbl = {
            0xF00: (E0C6200._get_io_it, E0C6200._set_io_dummy),
            0xF01: (E0C6200._get_io_isw, E0C6200._set_io_dummy),
            0xF02: (E0C6200._get_io_ipt, E0C6200._set_io_dummy),
            0xF03: (E0C6200._get_io_isio, E0C6200._set_io_dummy),
            0xF04: (E0C6200._get_io_ik0, E0C6200._set_io_dummy),
            0xF05: (E0C6200._get_io_ik1, E0C6200._set_io_dummy),
            0xF10: (E0C6200._get_io_eit, E0C6200._set_io_eit),
            0xF11: (E0C6200._get_io_eisw, E0C6200._set_io_eisw),
            0xF12: (E0C6200._get_io_eipt, E0C6200._set_io_eipt),
            0xF13: (E0C6200._get_io_eisio, E0C6200._set_io_eisio),
            0xF14: (E0C6200._get_io_eik0, E0C6200._set_io_eik0),
            0xF15: (E0C6200._get_io_eik1, E0C6200._set_io_eik1),
            0xF20: (E0C6200._get_io_tm30, E0C6200._set_io_dummy),
            0xF21: (E0C6200._get_io_tm74, E0C6200._set_io_dummy),
            0xF22: (E0C6200._get_io_swl, E0C6200._set_io_dummy),
            0xF23: (E0C6200._get_io_swh, E0C6200._set_io_dummy),
            0xF24: (E0C6200._get_io_pt30, E0C6200._set_io_dummy),
            0xF25: (E0C6200._get_io_pt74, E0C6200._set_io_dummy),
            0xF26: (E0C6200._get_io_rd30, E0C6200._set_io_rd30),
            0xF27: (E0C6200._get_io_rd74, E0C6200._set_io_rd74),
            0xF30: (E0C6200._get_io_sd30, E0C6200._set_io_sd30),
            0xF31: (E0C6200._get_io_sd74, E0C6200._set_io_sd74),
            0xF40: (E0C6200._get_io_k0, E0C6200._set_io_dummy),
            0xF41: (E0C6200._get_io_dfk0, E0C6200._set_io_dummy),
            0xF42: (E0C6200._get_io_k1, E0C6200._set_io_dummy),
            0xF50: (E0C6200._get_io_r0, E0C6200._set_io_r0),
            0xF51: (E0C6200._get_io_r1, E0C6200._set_io_r1),
            0xF52: (E0C6200._get_io_r2, E0C6200._set_io_r2),
            0xF53: (E0C6200._get_io_r3, E0C6200._set_io_r3),
            0xF54: (E0C6200._get_io_r4, E0C6200._set_io_r4),

            0xF60: (E0C6200._get_io_p0, E0C6200._set_io_p0),
            0xF61: (E0C6200._get_io_p1, E0C6200._set_io_p1),
            0xF62: (E0C6200._get_io_p2, E0C6200._set_io_p2),
            0xF63: (E0C6200._get_io_p3, E0C6200._set_io_p3),

            0xF70: (E0C6200._get_io_ctrl_osc, E0C6200._set_io_ctrl_osc), #to-do
            0xF71: (E0C6200._get_io_ctrl_lcd, E0C6200._set_io_ctrl_lcd),
            0xF72: (E0C6200._get_io_lc, E0C6200._set_io_lc),
            0xF73: (E0C6200._get_io_ctrl_svd, E0C6200._set_io_dummy), #to-do
            0xF74: (E0C6200._get_io_ctrl_bz1, E0C6200._set_io_ctrl_bz1), #to-do
            0xF75: (E0C6200._get_io_ctrl_bz2, E0C6200._set_io_ctrl_bz2), #to-do
            0xF76: (E0C6200._get_io_dummy, E0C6200._set_io_ctrl_tm),
            0xF77: (E0C6200._get_io_ctrl_sw, E0C6200._set_io_ctrl_sw),
            0xF78: (E0C6200._get_io_ctrl_pt, E0C6200._set_io_ctrl_pt),
            0xF79: (E0C6200._get_io_ptc, E0C6200._set_io_ptc),
            0xF7A: (E0C6200._get_io_dummy, E0C6200._set_io_dummy), #to-do
            0xF7B: (E0C6200._get_io_dummy, E0C6200._set_io_dummy), #to-do
            0xF7D: (E0C6200._get_io_ioc, E0C6200._set_io_ioc),
            0xF7E: (E0C6200._get_io_pup, E0C6200._set_io_pup),
        }

        self._get_abmxmy_tbl = (
            E0C6200.get_A,
            E0C6200.get_B,
            E0C6200.get_MX,
            E0C6200.get_MY
        )

        self._set_abmxmy_tbl = (
            E0C6200.set_A,
            E0C6200.set_B,
            E0C6200.set_MX,
            E0C6200.set_MY
        )

        self._execute = (
            *([E0C6200._jp_s] * 256),           #0 0 0 0  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200._retd_l] * 256),         #0 0 0 1  l7 l6 l5 l4  l3 l2 l1 l0
            *([E0C6200._jp_c_s] * 256),         #0 0 1 0  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200._jp_nc_s] * 256),        #0 0 1 1  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200._call_s] * 256),         #0 1 0 0  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200._calz_s] * 256),         #0 1 0 1  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200._jp_z_s] * 256),         #0 1 1 0  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200._jp_nz_s] * 256),        #0 1 1 1  s7 s6 s5 s4  s3 s2 s1 s0
            *([E0C6200._ld_y_y] * 256),         #1 0 0 0  y7 y6 y5 y4  y3 y2 y1 y0
            *([E0C6200._lbpx_mx_l] * 256),      #1 0 0 1  l7 l6 l5 l4  l3 l2 l1 l0
            *([E0C6200._adc_xh_i] * 16),        #1 0 1 0  0 0 0 0  i3 i2 i1 i0
            *([E0C6200._adc_xl_i] * 16),        #1 0 1 0  0 0 0 1  i3 i2 i1 i0
            *([E0C6200._adc_yh_i] * 16),        #1 0 1 0  0 0 1 0  i3 i2 i1 i0
            *([E0C6200._adc_yl_i] * 16),        #1 0 1 0  0 0 1 1  i3 i2 i1 i0
            *([E0C6200._cp_xh_i] * 16),         #1 0 1 0  0 1 0 0  i3 i2 i1 i0
            *([E0C6200._cp_xl_i] * 16),         #1 0 1 0  0 1 0 1  i3 i2 i1 i0
            *([E0C6200._cp_yh_i] * 16),         #1 0 1 0  0 1 1 0  i3 i2 i1 i0
            *([E0C6200._cp_yl_i] * 16),         #1 0 1 0  0 1 1 1  i3 i2 i1 i0
            *([E0C6200._add_r_q] * 16),         #1 0 1 0  1 0 0 0  r1 r0 q1 q0
            *([E0C6200._adc_r_q] * 16),         #1 0 1 0  1 0 0 1  r1 r0 q1 q0
            *([E0C6200._sub_r_q] * 16),         #1 0 1 0  1 0 1 0  r1 r0 q1 q0
            *([E0C6200._sbc_r_q] * 16),         #1 0 1 0  1 0 1 1  r1 r0 q1 q0
            *([E0C6200._and_r_q] * 16),         #1 0 1 0  1 1 0 0  r1 r0 q1 q0
            *([E0C6200._or_r_q] * 16),          #1 0 1 0  1 1 0 1  r1 r0 q1 q0
            *([E0C6200._xor_r_q] * 16),         #1 0 1 0  1 1 1 0  r1 r0 q1 q0
            *([E0C6200._rlc_r] * 16),           #1 0 1 0  1 1 1 1  r1 r0 r1 r0
            *([E0C6200._ld_x_x] * 256),         #1 0 1 1  x7 x6 x5 x4  x3 x2 x1 x0
            *([E0C6200._add_r_i] * 64),         #1 1 0 0  0 0 r1 r0  i3 i2 i1 i0
            *([E0C6200._adc_r_i] * 64),         #1 1 0 0  0 1 r1 r0  i3 i2 i1 i0
            *([E0C6200._and_r_i] * 64),         #1 1 0 0  1 0 r1 r0  i3 i2 i1 i0
            *([E0C6200._or_r_i] * 64),          #1 1 0 0  1 1 r1 r0  i3 i2 i1 i0
            *([E0C6200._xor_r_i] * 64),         #1 1 0 1  0 0 r1 r0  i3 i2 i1 i0
            *([E0C6200._sbc_r_i] * 64),         #1 1 0 1  0 1 r1 r0  i3 i2 i1 i0
            *([E0C6200._fan_r_i] * 64),         #1 1 0 1  1 0 r1 r0  i3 i2 i1 i0
            *([E0C6200._cp_r_i] * 64),          #1 1 0 1  1 1 r1 r0  i3 i2 i1 i0
            *([E0C6200._ld_r_i] * 64),          #1 1 1 0  0 0 r1 r0  i3 i2 i1 i0
            *([E0C6200._pset_p] * 32),          #1 1 1 0  0 1 0 p4  p3 p2 p1 p0
            *([E0C6200._ldpx_mx_i] * 16),       #1 1 1 0  0 1 1 0  i3 i2 i1 i0
            *([E0C6200._ldpy_my_i] * 16),       #1 1 1 0  0 1 1 1  i3 i2 i1 i0
            *([E0C6200._ld_xp_r] * 4),          #1 1 1 0  1 0 0 0  0 0 r1 r0
            *([E0C6200._ld_xh_r] * 4),          #1 1 1 0  1 0 0 0  0 1 r1 r0
            *([E0C6200._ld_xl_r] * 4),          #1 1 1 0  1 0 0 0  1 0 r1 r0
            *([E0C6200._rrc_r] * 4),            #1 1 1 0  1 0 0 0  1 1 r1 r0
            *([E0C6200._ld_yp_r] * 4),          #1 1 1 0  1 0 0 1  0 0 r1 r0
            *([E0C6200._ld_yh_r] * 4),          #1 1 1 0  1 0 0 1  0 1 r1 r0
            *([E0C6200._ld_yl_r] * 4),          #1 1 1 0  1 0 0 1  1 0 r1 r0
            *([E0C6200._dummy] * 4),
            *([E0C6200._ld_r_xp] * 4),          #1 1 1 0  1 0 1 0  0 0 r1 r0
            *([E0C6200._ld_r_xh] * 4),          #1 1 1 0  1 0 1 0  0 1 r1 r0
            *([E0C6200._ld_r_xl] * 4),          #1 1 1 0  1 0 1 0  1 0 r1 r0
            *([E0C6200._dummy] * 4),
            *([E0C6200._ld_r_yp] * 4),          #1 1 1 0  1 0 1 1  0 0 r1 r0
            *([E0C6200._ld_r_yh] * 4),          #1 1 1 0  1 0 1 1  0 1 r1 r0
            *([E0C6200._ld_r_yl] * 4),          #1 1 1 0  1 0 1 1  1 0 r1 r0
            *([E0C6200._dummy] * 4),
            *([E0C6200._ld_r_q] * 16),          #1 1 1 0  1 1 0 0  r1 r0 q1 q0
            *([E0C6200._dummy] * 16),
            *([E0C6200._ldpx_r_q] * 16),        #1 1 1 0  1 1 1 0  r1 r0 q1 q0
            *([E0C6200._ldpy_r_q] * 16),        #1 1 1 0  1 1 1 1  r1 r0 q1 q0
            *([E0C6200._cp_r_q] * 16),          #1 1 1 1  0 0 0 0  r1 r0 q1 q0
            *([E0C6200._fan_r_q] * 16),         #1 1 1 1  0 0 0 1  r1 r0 q1 q0
            *([E0C6200._dummy] * 8),
            *([E0C6200._acpx_mx_r] * 4),        #1 1 1 1  0 0 1 0  1 0 r1 r0
            *([E0C6200._acpy_my_r] * 4),        #1 1 1 1  0 0 1 0  1 1 r1 r0
            *([E0C6200._dummy] * 8),
            *([E0C6200._scpx_mx_r] * 4),        #1 1 1 1  0 0 1 1  1 0 r1 r0
            *([E0C6200._scpy_my_r] * 4),        #1 1 1 1  0 0 1 1  1 1 r1 r0
            *([E0C6200._set_f_i] * 16),         #1 1 1 1  0 1 0 0  i3 i2 i1 i0
            *([E0C6200._rst_f_i] * 16),         #1 1 1 1  0 1 0 1  i3 i2 i1 i0
            *([E0C6200._inc_mn] * 16),          #1 1 1 1  0 1 1 0  n3 n2 n1 n0
            *([E0C6200._dec_mn] * 16),          #1 1 1 1  0 1 1 1  n3 n2 n1 n0
            *([E0C6200._ld_mn_a] * 16),         #1 1 1 1  1 0 0 0  n3 n2 n1 n0
            *([E0C6200._ld_mn_b] * 16),         #1 1 1 1  1 0 0 1  n3 n2 n1 n0
            *([E0C6200._ld_a_mn] * 16),         #1 1 1 1  1 0 1 0  n3 n2 n1 n0
            *([E0C6200._ld_b_mn] * 16),         #1 1 1 1  1 0 1 1  n3 n2 n1 n0
            *([E0C6200._push_r] * 4),           #1 1 1 1  1 1 0 0  0 0 r1 r0
            E0C6200._push_xp,                   #1 1 1 1  1 1 0 0  0 1 0 0
            E0C6200._push_xh,                   #1 1 1 1  1 1 0 0  0 1 0 1
            E0C6200._push_xl,                   #1 1 1 1  1 1 0 0  0 1 1 0
            E0C6200._push_yp,                   #1 1 1 1  1 1 0 0  0 1 1 1
            E0C6200._push_yh,                   #1 1 1 1  1 1 0 0  1 0 0 0
            E0C6200._push_yl,                   #1 1 1 1  1 1 0 0  1 0 0 1
            E0C6200._push_f,                    #1 1 1 1  1 1 0 0  1 0 1 0
            E0C6200._dec_sp,                    #1 1 1 1  1 1 0 0  1 0 1 1
            *([E0C6200._dummy] * 4),
            *([E0C6200._pop_r] * 4),            #1 1 1 1  1 1 0 1  0 0 r1 r0
            E0C6200._pop_xp,                    #1 1 1 1  1 1 0 1  0 1 0 0
            E0C6200._pop_xh,                    #1 1 1 1  1 1 0 1  0 1 0 1
            E0C6200._pop_xl,                    #1 1 1 1  1 1 0 1  0 1 1 0
            E0C6200._pop_yp,                    #1 1 1 1  1 1 0 1  0 1 1 1
            E0C6200._pop_yh,                    #1 1 1 1  1 1 0 1  1 0 0 0
            E0C6200._pop_yl,                    #1 1 1 1  1 1 0 1  1 0 0 1
            E0C6200._pop_f,                     #1 1 1 1  1 1 0 1  1 0 1 0
            E0C6200._inc_sp,                    #1 1 1 1  1 1 0 1  1 0 1 1
            *([E0C6200._dummy] * 2),
            E0C6200._rets,                      #1 1 1 1  1 1 0 1  1 1 1 0
            E0C6200._ret,                       #1 1 1 1  1 1 0 1  1 1 1 1
            *([E0C6200._ld_sph_r] * 4),         #1 1 1 1  1 1 1 0  0 0 r1 r0
            *([E0C6200._ld_r_sph] * 4),         #1 1 1 1  1 1 1 0  0 1 r1 r0
            E0C6200._jpba,                      #1 1 1 1  1 1 1 0  1 0 0 0
            *([E0C6200._dummy] * 7),
            *([E0C6200._ld_spl_r] * 4),         #1 1 1 1  1 1 1 1  0 0 r1 r0
            *([E0C6200._ld_r_spl] * 4),         #1 1 1 1  1 1 1 1  0 1 r1 r0
            E0C6200._halt,                      #1 1 1 1  1 1 1 1  1 0 0 0
            *([E0C6200._dummy] * 2),
            E0C6200._nop5,                      #1 1 1 1  1 1 1 1  1 0 1 1
            *([E0C6200._dummy] * 3),
            E0C6200._nop7                       #1 1 1 1  1 1 1 1  1 1 1 1
        )

    def examine(self):
        return {
            "PC": self._PC,
            "NPC": self._NPC & 0x1F00,
            "A": self._A,
            "B": self._B,
            "IX": self._IX,
            "IY": self._IY,
            "SP": self._SP,
            "CF": self._CF,
            "ZF": self._ZF,
            "DF": self._DF,
            "IF": self._IF,
            "HALT": self._HALT,
            "RAM0": self._RAM[:256],
            "RAM1": self._RAM[256:512],
            "RAM2": self._RAM[512:640],
            "VRAM": self._VRAM,
            "IORAM": (
                self._IT,
                self._ISW,
                self._IPT,
                self._ISIO,
                self._IK0,
                self._IK1,
                self._EIT,
                self._EISW,
                self._EIPT,
                self._EISIO,
                self._EIK0,
                self._EIK1,
                self._TM & 0xF,
                self._TM >> 4,
                self._SWL,
                self._SWH,
                self._PT & 0xF,
                self._PT >> 4,
                self._RD & 0xF,
                self._RD >> 4,
                self._SD & 0xF,
                self._SD >> 4,
                self._K0,
                self._DFK0,
                self._K1,
                self._R0,
                self._R1,
                self._R2,
                self._R3,
                self._R4,
                self._P0,
                self._P1,
                self._P2,
                self._P3,
                self._CTRL_OSC,
                self._CTRL_LCD,
                self._LC,
                self._CTRL_SVD,
                self._CTRL_BZ1,
                self._CTRL_BZ2,
                0,
                self._CTRL_SW,
                self._CTRL_PT,
                self._PTC,
                self._SC,
                self._HZR,
                self._IOC,
                self._PUP
            )
        }

    def edit_state(self, state):
        if ("CF" in state):
            self._CF = state["CF"]
        if ("ZF" in state):
            self._ZF = state["ZF"]
        if ("DF" in state):
            self._DF = state["DF"]
        if ("IF" in state):
            self._IF = state["IF"]
        if ("HALT" in state):
            self._HALT = state["HALT"]
        if ("PC" in state):
            self._PC = state["PC"] & 0x1FFF
        if ("NPC" in state):
            self._NPC = state["NPC"] & 0x1F00
        if ("SP" in state):
            self._SP = state["SP"] & 0xFF
        if ("A" in state):
            self._A = state["A"] & 0xF
        if ("B" in state):
            self._B = state["B"] & 0xF
        if ("IX" in state):
            self._IX = state["IX"] & 0xFF
        if ("IY" in state):
            self._IY = state["IY"] & 0xFF
        if ("RAM0" in state):
            for i, value in state["RAM0"].items():
                self._RAM[i] = value & 0xF
        if ("RAM1" in state):
            for i, value in state["RAM1"].items():
                self._RAM[256 + i] = value & 0xF
        if ("RAM2" in state):
            for i, value in state["RAM2"].items():
                self._RAM[512 + i] = value & 0xF
        if ("VRAM" in state):
            for i, value in state["VRAM"].items():
                self._VRAM[i] = value & 0xF
        if ("IORAM" in state):
            for i, value in state["IORAM"].items():
                if i < len(self._io_tbl):
                    list(self._io_tbl.values())[i][1](self, value & 0xF)
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])

    def _init_registers(self):
        self._A = 0
        self._B = 0
        self._IX = 0
        self._IY = 0
        self._SP = 0

        self._PC = 0x100
        self._NPC = 0x100

        self._CF = 0
        self._ZF = 0
        self._DF = 0
        self._IF = 0

        self._RAM = [0] * RAM_SIZE
        self._VRAM = [0] * VRAM_SIZE
        
        self._HALT = 0

        self._P0_OUTPUT_DATA = 0
        self._P1_OUTPUT_DATA = 0
        self._P2_OUTPUT_DATA = 0
        self._P3_OUTPUT_DATA = 0

        self._IT = 0
        self._ISW = 0
        self._IPT = 0
        self._ISIO = 0
        self._IK0 = 0
        self._IK1 = 0
        self._EIT = 0
        self._EISW = 0
        self._EIPT = 0
        self._EISIO = 0
        self._EIK0 = 0
        self._EIK1 = 0
        self._TM = 0
        self._SWL = 0
        self._SWH = 0
        self._PT = 0
        self._RD = 0
        self._SD = 0
        self._K0 = self._port_pullup['K0']
        self._DFK0 = 0xF
        self._K1 = self._port_pullup['K1']
        self._R0 = 0
        self._R1 = 0
        self._R2 = 0
        self._R3 = 0
        self._R4 = 0xF
        self._P0 = 0
        self._P1 = 0
        self._P2 = 0
        self._P3 = 0
        self._CTRL_OSC = 0
        self._CTRL_LCD = IO_ALOFF
        self._LC = 0
        self._CTRL_SVD = IO_SVDDT
        self._CTRL_BZ1 = 0
        self._CTRL_BZ2 = 0
        self._CTRL_SW = 0
        self._CTRL_PT = 0
        self._PTC = 0
        self._SC = 0
        self._HZR = 0
        self._IOC = 0
        self._PUP = 0

    def _reset(self):
        self._init_registers()

        self._OSC1_counter = 0
        self._timer_counter = 0
        self._stopwatch_counter = 0
        self._execution_counter = 0
        
        self._sound.set_buzzer_off()
        self._sound.set_envelope_off()

    def reset(self):
        self._reset()

    def _get_io_dummy(self):
        return 0
    
    def _set_io_dummy(self, value):
        pass

    def _get_io_it(self):
        ret = self._IT
        self._IT = 0
        return ret

    def _get_io_isw(self):
        ret = self._ISW
        self._ISW = 0
        return ret

    def _get_io_ipt(self):
        ret = self._IPT
        self._IPT = 0
        return ret

    def _get_io_isio(self):
        ret = self._ISIO
        self._ISIO = 0
        return ret

    def _get_io_ik0(self):
        ret = self._IK0
        self._IK0 = 0
        return ret

    def _get_io_ik1(self):
        ret = self._IK1
        self._IK1 = 0
        return ret

    def _get_io_eit(self):
        return self._EIT

    def _set_io_eit(self, value):
        self._EIT = value

    def _get_io_eisw(self):
        return self._EISW

    def _set_io_eisw(self, value):
        self._EISW = value & 0x3

    def _get_io_eipt(self):
        return self._EIPT

    def _set_io_eipt(self, value):
        self._EIPT = value & 0x1

    def _get_io_eisio(self):
        return self._EISIO

    def _set_io_eisio(self, value):
        self._EISIO = value & 0x1

    def _get_io_eik0(self):
        return self._EIK0

    def _set_io_eik0(self, value):
        self._EIK0 = value

    def _get_io_eik1(self):
        return self._EIK1

    def _set_io_eik1(self, value):
        self._EIK1 = value

    def _get_io_tm30(self):
        return self._TM & 0xF

    def _get_io_tm74(self):
        return self._TM >> 4 & 0xF

    def _get_io_swl(self):
        return self._SWL & 0xF

    def _get_io_swh(self):
        return self._SWH & 0xF

    def _get_io_pt30(self):
        return self._PT & 0xF
    
    def _get_io_pt74(self):
        return self._PT >> 4 & 0xF

    def _get_io_rd30(self):
        return self._PRD & 0xF

    def _set_io_rd30(self, value):
        self._RD = (self._RD & 0xF0) | (value & 0x0F)

    def _get_io_rd74(self):
        return self._RD >> 4 & 0xF

    def _set_io_rd74(self, value):
        self._RD = (self._RD & 0x0F) | (value << 4 & 0xF0)
    
    def _get_io_sd30(self):
        return self._SD & 0xF

    def _set_io_sd30(self, value):
        self._SD = (self._SD & 0xF0) | (value & 0x0F)

    def _get_io_sd74(self):
        return self._SD >> 4 & 0xF

    def _set_io_sd74(self, value):
        self._SD = (self._SD & 0x0F) | (value << 4 & 0xF0)
    
    def _get_io_k0(self):
        return self._K0

    def _get_io_dfk0(self):
        return self._DFK0

    def _set_io_dfk0(self, value):
        self._DFK0 = value
    
    def _get_io_k1(self):
        return self._K1

    def _get_io_r0(self):
        return self._R0

    def _set_io_r0(self, value):
        self._R0 = value

    def _get_io_r1(self):
        return self._R1

    def _set_io_r1(self, value):
        self._R1 = value

    def _get_io_r2(self):
        return self._R2

    def _set_io_r2(self, value):
        self._R2 = value

    def _get_io_r3(self):
        return self._R3

    def _set_io_r3(self, value):
        self._R3 = value

    def _get_io_r4(self):
        return self._R4

    def _set_io_r4(self, value):
        self._R4 = value
        if (value & IO_R43):
            self._sound.set_buzzer_off()
        else:
            self._sound.set_buzzer_on()

    def _get_io_p0(self):
        return self._P0

    def _set_io_p0(self, value):
        self._P0_OUTPUT_DATA = value
        if (self._IOC & IO_IOC0):
            self._P0 = value

    def _get_io_p1(self):
        return self._P1

    def _set_io_p1(self, value):
        self._P1_OUTPUT_DATA = value
        if (self._IOC & IO_IOC1):
            self._P1 = value

    def _get_io_p2(self):
        return self._P2

    def _set_io_p2(self, value):
        self._P2_OUTPUT_DATA = value
        if (self._IOC & IO_IOC2):
            self._P2 = value

    def _get_io_p3(self):
        return self._P3

    def _set_io_p3(self, value):
        self._P3_OUTPUT_DATA = value
        if (self._IOC & IO_IOC3 or self._p3_dedicated):
            self._P3 = value


    def _get_io_ioc(self):
        return self._IOC
    
    def _set_io_ioc(self, value):
        self._IOC = value
        if (self._IOC & IO_IOC0):
            self._P0 = self._P0_OUTPUT_DATA
        if (self._IOC & IO_IOC1):
            self._P1 = self._P1_OUTPUT_DATA
        if (self._IOC & IO_IOC2):
            self._P2 = self._P2_OUTPUT_DATA
        if (self._IOC & IO_IOC3):
            self._P3 = self._P3_OUTPUT_DATA

    def _get_io_pup(self):
        return self._PUP
    
    def _set_io_pup(self, value):
        self._PUP = value

    def _get_io_ctrl_osc(self):
        return self._CTRL_OSC
    
    def _set_io_ctrl_osc(self, value):
        self._CTRL_OSC = value

    def _get_io_ctrl_lcd(self):
        return self._CTRL_LCD
    
    def _set_io_ctrl_lcd(self, value):
        self._CTRL_LCD = value

    def _get_io_lc(self):
        return self._LC
    
    def _set_io_lc(self, value):
        self._LC = value

    def _get_io_ctrl_svd(self):
        return 0

    def _get_io_ctrl_bz1(self):
        return self._CTRL_BZ1

    def _set_io_ctrl_bz1(self, value):
        self._CTRL_BZ1 = value
        self._sound.set_freq(self._CTRL_BZ1 & IO_BZFQ)

    def _get_io_ctrl_bz2(self):
        return self._CTRL_BZ2 & (IO_ENVRT | IO_ENVON) | (IO_BZSHOT * self._sound.is_one_shot_ringing())

    def _set_io_ctrl_bz2(self, value):
        self._CTRL_BZ2 = value & (IO_ENVRT | IO_ENVON)
        
        self._sound.set_envelope_cycle(int(value & IO_ENVRT > 0))
        if (value & IO_BZSHOT):
            self._sound.one_shot((self._CTRL_BZ1 & IO_SHOTPW) > 0)
        if (value & IO_ENVON):
            self._sound.set_envelope_on()
        else:
            self._sound.set_envelope_off()
        if (value & IO_ENVRST):
            self._sound.reset_envelope()


    def _set_io_ctrl_tm(self, value):
        if (value & IO_TMRST):
            self._TM = 0

    def _get_io_ctrl_sw(self):
        return self._CTRL_SW & IO_SWRUN

    def _set_io_ctrl_sw(self, value):
        if (value & IO_SWRST):
            self._SWL = self._SWH = 0
        self._CTRL_SW = value & IO_SWRUN

    def _get_io_ctrl_pt(self):
        return self._CTRL_PT & IO_PTRUN

    def _set_io_ctrl_pt(self, value):
        if (value & IO_PTRST):
            self._PT = self._RD
        self._CTRL_PT = value & IO_PTRUN

    def _get_io_ptc(self):
        return self._PTC

    def _set_io_ptc(self, value):
        self._PTC = value

    def pin_set(self, port, pin, level):
        if (port == 'K0'):
            new_K0 =  ~(1 << pin) & self._K0 | level << pin
            if (self._EIK0 and self._DFK0 >> pin != level and self._K0 >> pin != level):
               self._IK0 |= IO_IK0
            if (pin == 3 and self._PTC & IO_PTC < 2 and self._DFK0 >> pin != level and self._K0 >> pin != level):
               self._process_ptimer()
            self._K0 = new_K0
        if (port == 'K1'):
            new_K1 =  ~(1 << pin) & self._K1 | level << pin
            if (self._EIK1 and level == 0 and self._K1 >> pin != level):
               self._IK1 |= IO_IK1
            self._K1 = new_K1
        elif (port == 'P0'):
            if (not(self._IOC & IO_IOC0)):
                self._P0 = ~(1 << pin) & self._P0 | level << pin
        elif (port == 'P1'):
            if (not(self._IOC & IO_IOC1)):
                self._P1 = ~(1 << pin) & self._P1 | level << pin
        elif (port == 'P2'):
            if (not(self._IOC & IO_IOC2)):
                self._P2 = ~(1 << pin) & self._P2 | level << pin
        elif (port == 'P3'):
            if (not(self._IOC & IO_IOC3) and (not self._p3_dedicated)):
                self._P3 = ~(1 << pin) & self._P3 | level << pin
        elif (port == 'RES'):
            self._reset()
            self._RESET = 1

    def pin_release(self, port, pin):
        if (port == 'K0'):
            level = self._port_pullup['K0'] >> pin & 0x1
            new_K0 =  ~(1 << pin) & self._K0 | level << pin
            if (self._EIK0 and self._DFK0 >> pin != level and self._K0 >> pin != level):
                self._IK0 |= IO_IK0
            if (pin == 3 and self._PTC & IO_PTC < 2 and self._DFK0 >> pin != level and self._K0 >> pin != level):
               self._process_ptimer()
            self._K0 = new_K0
        if (port == 'K1'):
            level = self._port_pullup['K1'] >> pin & 0x1
            new_K1 =  ~(1 << pin) & self._K1 | level << pin
            if (self._EIK1 and level == 0 and self._K1 >> pin != level):
                self._IK1 |= IO_IK1
            self._K1 = new_K1
        elif (port == 'P0'):
            if (not(self._IOC & IO_IOC0)):
                self._P0 = ~(1 << pin) & self._P0 | (self._PUP & IO_PUP0)
        elif (port == 'P1'):
            if (not(self._IOC & IO_IOC1)):
                self._P1 = ~(1 << pin) & self._P1 | (self._PUP & IO_PUP1)
        elif (port == 'P2'):
            if (not(self._IOC & IO_IOC2)):
                self._P2 = ~(1 << pin) & self._P2 | (self._PUP & IO_PUP2)
        elif (port == 'P3'):
            if (not(self._IOC & IO_IOC3) and (not self._p3_dedicated)):
                self._P3 = ~(1 << pin) & self._P3 | (self._PUP & IO_PUP3)
        elif (port == 'RES'):
            self._RESET = 0


    def pc(self):
        return self._PC & 0x1FFF
    
    def get_VRAM(self):
        if ((self._CTRL_LCD & IO_ALOFF) | self._RESET):
            return EMPTY_VRAM
        elif (self._CTRL_LCD & IO_ALON):
            return FULL_VRAM
        return tuple(self._VRAM)

    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter
            
    def clock(self):
        exec_cycles = 7
        if (not self._RESET):

            if (not self._HALT):
                self._if_delay = False
                opcode = self._ROM.getWord(self._PC * 2)
                exec_cycles = self._execute[opcode](self, opcode)
                self._instr_counter += 1

            if (self._IF and not self._if_delay):
                if (self._IPT):
                    exec_cycles += self._interrupt(0xC)
                elif (self._ISIO):
                    exec_cycles += self._interrupt(0xA)
                elif (self._IK1):
                    exec_cycles += self._interrupt(0x8)
                elif (self._IK0):
                    exec_cycles += self._interrupt(0x6)
                elif (self._ISW):
                    exec_cycles += self._interrupt(0x4)
                elif (self._IT):
                    exec_cycles += self._interrupt(0x2)

            self._OSC1_counter -= exec_cycles
            while (self._OSC1_counter <= 0):
                self._OSC1_counter += self._OSC1_clock_div
                self._clock_OSC1()
        
        return exec_cycles

    def _clock_OSC1(self):
        self._sound.clock()

        if (self._PTC & IO_PTC > 1):
            self._ptimer_counter -= 1
            if (self._ptimer_counter <= 0):
                self._ptimer_counter += PTIMER_CLOCK_DIV[self._PTC & IO_PTC]
                self._process_ptimer()

        self._stopwatch_counter -= 1
        if (self._stopwatch_counter <= 0):
            self._stopwatch_counter += STOPWATCH_CLOCK_DIV
            self._process_stopwatch()

        self._timer_counter -= 1
        if (self._timer_counter <= 0):
            self._timer_counter += TIMER_CLOCK_DIV
            self._process_timer()

    def _process_ptimer(self):
        self._PT = (self._PT - 1) & 0xFF
        if (self._PT == 0):
            self._PT = self._RD
            if (self._EIPT & IO_EIPT):
                self._IPT |= IO_IPT
        if (self._PTC & IO_PTCOUT):
            self._R3 ^= IO_R33

    def _process_stopwatch(self):
        if (self._CTRL_SW & IO_SWRUN):
            self._SWL = self._SWL + 1 if self._SWL < 9 else 0
            if (self._SWL == 0):
                self._SWH = self._SWH + 1 if self._SWH < 9 else 0
                if (self._EISW & IO_EISW0 and self._SWH == 0):
                    self._ISW |= IO_ISW0
                if (self._EISW & IO_EISW1):
                    self._ISW |= IO_ISW1

    def _process_timer(self):
        new_TM = (self._TM + 1) & 0xFF
        if (self._EIT & IO_EIT32 and new_TM & IO_TM2 < self._TM & IO_TM2):
            self._IT |= IO_IT32
        if (self._EIT & IO_EIT8 and new_TM >> 4 & IO_TM4 < self._TM >> 4 & IO_TM4):
            self._IT |= IO_IT8
        if (self._EIT & IO_EIT2 and new_TM >> 4 & IO_TM6 < self._TM >> 4 & IO_TM6):
            self._IT |= IO_IT2
        if (self._EIT & IO_EIT1 and new_TM >> 4 & IO_TM7 < self._TM >> 4 & IO_TM7):
            self._IT |= IO_IT1
        self._TM = new_TM
    
    def _interrupt(self, vector):
        self.set_mem(self._SP - 1 & 0xFF, self._PC >> 8 & 0x0F)
        self.set_mem(self._SP - 2 & 0xFF, self._PC >> 4 & 0x0F)
        self._SP = self._SP - 3 & 0xFF
        self.set_mem(self._SP, self._PC & 0x0F)
        self._IF = 0
        self._HALT = 0
        self._PC = self._NPC = (self._NPC & 0x1000) | 0x0100 | vector
        
        return 13

    def get_mem(self, addr):
        if (addr < RAM_SIZE):
            return self._RAM[addr]
        elif (addr >= VRAM_PART1_OFFSET and addr < VRAM_PART1_OFFSET + VRAM_PART_SIZE):
            return self._VRAM[addr - VRAM_PART1_OFFSET]
        elif (addr >= VRAM_PART2_OFFSET and addr < VRAM_PART2_OFFSET + VRAM_PART_SIZE):
            return self._VRAM[addr - VRAM_PART2_OFFSET + VRAM_PART_SIZE]
        elif (addr >= IORAM_OFFSET and addr < IORAM_OFFSET + IORAM_SIZE):
            io = self._io_tbl.get(addr)
            if (io != None):
                return io[0](self)
        return 0

    def set_mem(self, addr, value):
        if (addr < RAM_SIZE):
            self._RAM[addr] = value & 0xF
        elif (addr >= VRAM_PART1_OFFSET and addr < VRAM_PART1_OFFSET + VRAM_PART_SIZE):
            self._VRAM[addr - VRAM_PART1_OFFSET] = value & 0xF
        elif (addr >= VRAM_PART2_OFFSET and addr < VRAM_PART2_OFFSET + VRAM_PART_SIZE):
            self._VRAM[addr - VRAM_PART2_OFFSET + VRAM_PART_SIZE] = value & 0xF
        elif (addr >= IORAM_OFFSET and addr < IORAM_OFFSET + IORAM_SIZE):
            io = self._io_tbl.get(addr)
            if (io != None):
                io[1](self, value)

    def get_A(self):
        return self._A

    def set_A(self, value):
        self._A = value & 0xF

    def get_B(self):
        return self._B

    def set_B(self, value):
        self._B = value & 0xF

    def get_MX(self):
        return self.get_mem(self._IX)

    def set_MX(self, value):
        self.set_mem(self._IX, value)

    def get_MY(self):
        return self.get_mem(self._IY)

    def set_MY(self, value):
        self.set_mem(self._IY, value)

    def _jp_s(self, opcode):
        #PCB←NBP, PCP←NPP, PCS←s7~s0
        self._PC = (self._NPC & 0x1F00) | (opcode & 0x0FF)

        return 5

    def _retd_l(self, opcode):
        #PCSL ← M(SP), PCSH ← M(SP+1), PCP ← M(SP+2) SP←SP+3, M(X)←l3~l0, M(X+1)←l7~l4, X←X+2
        self._PC = self._NPC = (self._PC & 0x1000) | (self._RAM[self._SP + 2] << 8) | (self._RAM[self._SP + 1] << 4) | self._RAM[self._SP]
        self._SP = self._SP + 3 & 0xFF
        self.set_mem(self._IX, opcode & 0x00F)
        self.set_mem((self._IX & 0xF00) | (self._IX + 1 & 0xFF), opcode >> 4 & 0x00F)
        self._IX = (self._IX & 0xF00) | (self._IX + 2 & 0xFF)

        return 12

    def _jp_c_s(self, opcode):
        #PCB←NBP, PCP←NPP, PCS←s7~s0 if C=1
        if (self._CF):
            self._PC = (self._NPC & 0x1F00) | (opcode & 0x0FF)
        else:
            self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _jp_nc_s(self, opcode):
        #PCB←NBP, PCP←NPP, PCS←s7~s0 if C=0
        if (not self._CF):
            self._PC = (self._NPC & 0x1F00) | (opcode & 0x0FF)
        else:
            self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _call_s(self, opcode):
        #M(SP-1) ←PCP, M(SP-2) ←PCSH, M(SP-3) ←PCSL+1 SP←SP-3, PCP←NPP, PCS←s7~s0
        self.set_mem(self._SP - 1 & 0xFF, self._PC + 1 >> 8 & 0x0F)
        self.set_mem(self._SP - 2 & 0xFF, self._PC + 1 >> 4 & 0x0F)
        self._SP = self._SP - 3 & 0xFF
        self.set_mem(self._SP, self._PC + 1 & 0x0F)
        self._PC = (self._NPC & 0x1F00) | (opcode & 0x0FF)

        return 7    

    def _calz_s(self, opcode):
        #M(SP-1)←PCP, M(SP-2)←PCSH, M(SP-3)←PCSL+1 SP ← SP-3, PCP ← 0, PCS ← s7~s0
        self.set_mem(self._SP - 1 & 0xFF, self._PC + 1 >> 8 & 0x0F)
        self.set_mem(self._SP - 2 & 0xFF, self._PC + 1 >> 4 & 0x0F)
        self._SP = self._SP - 3 & 0xFF
        self.set_mem(self._SP, self._PC + 1 & 0x0F)
        self._PC = self._NPC = (self._NPC & 0x1000) | (opcode & 0x0FF)

        return 7

    def _jp_z_s(self, opcode):
        #PCB←NBP, PCP←NPP, PCS←s7~s0 if Z=1
        if (self._ZF):
            self._PC = (self._NPC & 0x1F00) | (opcode & 0x0FF)
        else:
            self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _jp_nz_s(self, opcode):
        #PCB←NBP, PCP←NPP, PCS←s7~s0 if Z=0
        if (not self._ZF):
            self._PC = (self._NPC & 0x1F00) | (opcode & 0x0FF)
        else:
            self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5 

    def _ld_y_y(self, opcode):
        #YH ← y7~y4, YL ← y3~y0
        self._IY = (self._IY & 0xF00) | (opcode & 0x0FF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _lbpx_mx_l(self, opcode):
        #M(X)←l3~l0, M(X+1)← l7~l4, X←X+2
        self.set_mem(self._IX, opcode & 0x00F)
        self.set_mem((self._IX & 0xF00) | (self._IX + 1 & 0xFF), opcode >> 4 & 0x00F)
        self._IX = (self._IX & 0xF00) | (self._IX + 2 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)
        
        return 5

    def _adc_xh_i(self, opcode):
        #XH← XH+i3~i0+C
        xh = (self._IX >> 4 & 0x00F) + (opcode & 0x00F) + self._CF
        self._ZF = xh & 0xF == 0
        self._CF = xh > 15
        self._IX = (self._IX & 0xF0F) | (xh << 4 & 0x0F0)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _adc_xl_i(self, opcode):
        #XL ← XL+i3~i0+C
        xl = (self._IX & 0x00F) + (opcode & 0x00F) + self._CF
        self._ZF = xl & 0xF == 0
        self._CF = xl > 15
        self._IX = (self._IX & 0xFF0) | (xl & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _adc_yh_i(self, opcode):
        #YH← YH+i3~i0+C
        yh = (self._IY >> 4 & 0x00F) + (opcode & 0x00F) + self._CF
        self._ZF = yh & 0xF == 0
        self._CF = yh > 15
        self._IY = (self._IY & 0xF0F) | (yh << 4 & 0x0F0)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _adc_yl_i(self, opcode):
        #YL ← YL+i3~i0+C
        yl = (self._IY & 0x00F) + (opcode & 0x00F) + self._CF
        self._ZF = yl & 0xF == 0
        self._CF = yl > 15
        self._IY = (self._IY & 0xFF0) | (yl & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _cp_xh_i(self, opcode):
        #XH-i3~i0
        cp = (self._IX >> 4 & 0x00F) - (opcode & 0x00F)
        self._ZF = cp == 0
        self._CF = cp < 0
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _cp_xl_i(self, opcode):
        #XL-i3~i0
        cp = (self._IX & 0x00F) - (opcode & 0x00F)
        self._ZF = cp == 0
        self._CF = cp < 0
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _cp_yh_i(self, opcode):
        #YH-i3~i0
        cp = (self._IY >> 4 & 0x00F) - (opcode & 0x00F)
        self._ZF = cp == 0
        self._CF = cp < 0
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _cp_yl_i(self, opcode):
        #YL-i3~i0
        cp = (self._IY & 0x00F) - (opcode & 0x00F)
        self._ZF = cp == 0
        self._CF = cp < 0
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _add_r_q(self, opcode):
        #r←r+q
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        res = self._get_abmxmy_tbl[r](self) + self._get_abmxmy_tbl[q](self)
        self._CF = res > 15
        if (self._DF and res > 9):
            res += 6
            self._CF = 1
        self._ZF = res & 0xF == 0
        self._set_abmxmy_tbl[r](self, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _adc_r_q(self, opcode):
        #r ← r+q+C
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        res = self._get_abmxmy_tbl[r](self) + self._get_abmxmy_tbl[q](self) + self._CF
        self._CF = res > 15
        if (self._DF and res > 9):
            res += 6
            self._CF = 1
        self._ZF = res & 0xF == 0
        self._set_abmxmy_tbl[r](self, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _sub_r_q(self, opcode):
        #r←r-q
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        res = self._get_abmxmy_tbl[r](self) - self._get_abmxmy_tbl[q](self)
        self._CF = res < 0
        if (self._DF and res < 0):
            res += 10
        self._ZF = res & 0xF == 0
        self._set_abmxmy_tbl[r](self, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _sbc_r_q(self, opcode):
        #r ← r-q-C
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        res = self._get_abmxmy_tbl[r](self) - self._get_abmxmy_tbl[q](self) - self._CF
        self._CF = res < 0
        if (self._DF and res < 0):
            res += 10
        self._ZF = res & 0xF == 0
        self._set_abmxmy_tbl[r](self, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _and_r_q(self, opcode):
        #r←r and q
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        res = self._get_abmxmy_tbl[r](self) & self._get_abmxmy_tbl[q](self)
        self._ZF = res == 0
        self._set_abmxmy_tbl[r](self, res)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _or_r_q(self, opcode):
        #r←r or q
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        res = self._get_abmxmy_tbl[r](self) | self._get_abmxmy_tbl[q](self)
        self._ZF = res == 0
        self._set_abmxmy_tbl[r](self, res)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _xor_r_q(self, opcode):
        #r←r xor q
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        res = self._get_abmxmy_tbl[r](self) ^ self._get_abmxmy_tbl[q](self)
        self._ZF = res == 0
        self._set_abmxmy_tbl[r](self, res)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7
   
    def _rlc_r(self, opcode):
        #d3 ←d2, d2 ←d1, d1 ←d0, d0 ←C, C← d3
        r = opcode & 0x3
        res = (self._get_abmxmy_tbl[r](self) << 1) + self._CF
        self._CF = res > 15
        self._set_abmxmy_tbl[r](self, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _ld_x_x(self, opcode):
        #XH ← x7~x4, XL ← x3~x0
        self._IX = (self._IX & 0xF00) | (opcode & 0x0FF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _add_r_i(self, opcode):
        #r ← r+i3~i0
        r = opcode >> 4 & 0x3
        res = self._get_abmxmy_tbl[r](self) + (opcode & 0x00F)
        self._CF = res > 15
        if (self._DF and res > 9):
            res += 6
            self._CF = 1
        self._ZF = res & 0xF == 0
        self._set_abmxmy_tbl[r](self, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _adc_r_i(self, opcode):
        #r ← r+i3~i0+C
        r = opcode >> 4 & 0x3
        res = self._get_abmxmy_tbl[r](self) + (opcode & 0x00F) + self._CF
        self._CF = res > 15
        if (self._DF and res > 9):
            res += 6
            self._CF = 1
        self._ZF = res & 0xF == 0
        self._set_abmxmy_tbl[r](self, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _and_r_i(self, opcode):
        #r ← r and i3~i0
        r = opcode >> 4 & 0x3
        res = self._get_abmxmy_tbl[r](self) & opcode & 0x00F
        self._ZF = res == 0
        self._set_abmxmy_tbl[r](self, res)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _or_r_i(self, opcode):
        #r ← r   i3~i0
        r = opcode >> 4 & 0x3
        res = self._get_abmxmy_tbl[r](self) | opcode & 0x00F
        self._ZF = res == 0
        self._set_abmxmy_tbl[r](self, res)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7
   
    def _xor_r_i(self, opcode):
        #r ← r i3~i0
        r = opcode >> 4 & 0x3
        res = self._get_abmxmy_tbl[r](self) ^ opcode & 0x00F
        self._ZF = res == 0
        self._set_abmxmy_tbl[r](self, res)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _sbc_r_i(self, opcode):
        #r ← r-i3~i0-C
        r = opcode >> 4 & 0x3
        res = self._get_abmxmy_tbl[r](self) - (opcode & 0x00F) - self._CF
        self._CF = res < 0
        if (self._DF and self._CF):
            res += 10
        self._ZF = res & 0xF == 0
        self._set_abmxmy_tbl[r](self, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _fan_r_i(self, opcode):
        #r and i3~i0
        r = opcode >> 4 & 0x3
        self._ZF = (self._get_abmxmy_tbl[r](self) & opcode & 0x00F) == 0
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _cp_r_i(self, opcode):
        #r-i3~i0
        r = opcode >> 4 & 0x3
        cp = self._get_abmxmy_tbl[r](self) - (opcode & 0x00F)
        self._ZF = cp == 0
        self._CF = cp < 0
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _ld_r_i(self, opcode):
        #r ← i3~i0
        r = opcode >> 4 & 0x3
        self._set_abmxmy_tbl[r](self, opcode & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
 
    def _pset_p(self, opcode):
        #NBP ←p4, NPP ← p3~p0
        self._if_delay = True
        self._NPC = opcode << 8 & 0x1F00
        self._PC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ldpx_mx_i(self, opcode):
        #M(X) ← i3~i0, X ← X+1
        self.set_mem(self._IX, opcode & 0x00F)
        self._IX = (self._IX & 0xF00) | (self._IX + 1 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ldpy_my_i(self, opcode):
        #M(Y) ← i3~i0, Y ← Y+1
        self.set_mem(self._IY, opcode & 0x00F)
        self._IY = (self._IY & 0xF00) | (self._IY + 1 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
  
    def _ld_xp_r(self, opcode):
        #XP ← r
        r = opcode & 0x3
        self._IX = (self._get_abmxmy_tbl[r](self) << 8) | (self._IX & 0x0FF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ld_xh_r(self, opcode):
        #XH← r
        r = opcode & 0x3
        self._IX = (self._get_abmxmy_tbl[r](self) << 4) | (self._IX & 0xF0F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
 
    def _ld_xl_r(self, opcode):
        #XL←r
        r = opcode & 0x3
        self._IX = self._get_abmxmy_tbl[r](self) | (self._IX & 0xFF0)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _rrc_r(self, opcode):
        #d3 ←C, d2 ←d3, d1 ←d2, d0 ←d1, C← d0
        r = opcode & 0x3
        res = self._get_abmxmy_tbl[r](self) + (self._CF << 4)
        self._CF = res & 0x1
        self._set_abmxmy_tbl[r](self, res >> 1)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ld_yp_r(self, opcode):
        #YP ← r
        r = opcode & 0x3
        self._IY = (self._get_abmxmy_tbl[r](self) << 8) | (self._IY & 0x0FF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ld_yh_r(self, opcode):
        #YH← r
        r = opcode & 0x3
        self._IY = (self._get_abmxmy_tbl[r](self) << 4) | (self._IY & 0xF0F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
 
    def _ld_yl_r(self, opcode):
        #YL←r
        r = opcode & 0x3
        self._IY = self._get_abmxmy_tbl[r](self) | (self._IY & 0xFF0)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _dummy(self, opcode):
        return 5

    def _ld_r_xp(self, opcode):
        #r←XP
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._IX >> 8)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ld_r_xh(self, opcode):
        #r←XH
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._IX >> 4 & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
  
    def _ld_r_xl(self, opcode):
        #r←XL
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._IX & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
  
    def _ld_r_yp(self, opcode):
        #r←YP
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._IY >> 8)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ld_r_yh(self, opcode):
        #r←YH
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._IY >> 4 & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
  
    def _ld_r_yl(self, opcode):
        #r←YL
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._IY & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ld_r_q(self, opcode):
        #r←q
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._get_abmxmy_tbl[q](self))
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ldpx_r_q(self, opcode):
        #r←q, X←X+1
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._get_abmxmy_tbl[q](self))
        self._IX = (self._IX & 0xF00) | (self._IX + 1 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ldpy_r_q(self, opcode):
        #r←q, Y←Y+1
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._get_abmxmy_tbl[q](self))
        self._IY = (self._IY & 0xF00) | (self._IY + 1 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _cp_r_q(self, opcode):
        #r-q
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        cp = self._get_abmxmy_tbl[r](self) - self._get_abmxmy_tbl[q](self)
        self._ZF = cp == 0
        self._CF = cp < 0
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7
   
    def _fan_r_q(self, opcode):
        #r and q
        r = opcode >> 2 & 0x3
        q = opcode & 0x3
        self._ZF = (self._get_abmxmy_tbl[r](self) & self._get_abmxmy_tbl[q](self)) == 0
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7
  
    def _acpx_mx_r(self, opcode):
        #M(X) ← M(X)+r+C, X ← X+1
        r = opcode & 0x3
        res = self.get_mem(self._IX) + self._get_abmxmy_tbl[r](self) + self._CF
        self._CF = res > 15
        if (self._DF and res > 9):
            res += 6
            self._CF = 1
        self._ZF = res & 0xF == 0
        self.set_mem(self._IX, res & 0xF)
        self._IX = (self._IX & 0xF00) | (self._IX + 1 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _acpy_my_r(self, opcode):
        #M(Y) ← M(Y)+r+C, Y ← Y+1
        r = opcode & 0x3
        res = self.get_mem(self._IY) + self._get_abmxmy_tbl[r](self) + self._CF
        self._CF = res > 15
        if (self._DF and res > 9):
            res += 6
            self._CF = 1
        self._ZF = res & 0xF == 0
        self.set_mem(self._IY, res & 0xF)
        self._IY = (self._IY & 0xF00) | (self._IY + 1 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7
  
    def _scpx_mx_r(self, opcode):
        # M(X) ← M(X)-r-C, X ← X+1
        r = opcode & 0x3
        res = self.get_mem(self._IX) - self._get_abmxmy_tbl[r](self) - self._CF
        self._CF = res < 0
        if (self._DF and res < 0):
            res += 10
        self._ZF = res & 0xF == 0
        self.set_mem(self._IX, res & 0xF)
        self._IX = (self._IX & 0xF00) | (self._IX + 1 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7
 
    def _scpy_my_r(self, opcode):
        #M(Y) ← M(Y)-r-C, Y ← Y+1
        r = opcode & 0x3
        res = self.get_mem(self._IY) - self._get_abmxmy_tbl[r](self) - self._CF
        self._CF = res < 0
        if (self._DF and res < 0):
            res += 10
        self._ZF = res & 0xF == 0
        self.set_mem(self._IY, res & 0xF)
        self._IY = (self._IY & 0xF00) | (self._IY + 1 & 0xFF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _set_f_i(self, opcode):
        #F ← F or i3~i0
        self._CF |= (opcode & 0x001)
        self._ZF |= (opcode >> 1 & 0x001)
        self._DF |= (opcode >> 2 & 0x001)
        new_IF = (opcode >> 3 & 0x001)
        self._if_delay = (new_IF and not self._IF)
        self._IF |= new_IF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _rst_f_i(self, opcode):
        #F ← F   i3~i0
        self._CF &= opcode
        self._ZF &= opcode >> 1
        self._DF &= opcode >> 2
        self._IF &= opcode >> 3
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _inc_mn(self, opcode):
        #M(n3~n0) ←M(n3~n0)+1
        mn = opcode & 0x00F
        res = self.get_mem(mn) + 1
        self._ZF = res == 16
        self._CF = res > 15
        self.set_mem(mn, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7

    def _dec_mn(self, opcode):
        #M(n3~n0) ←M(n3~n0)-1
        mn = opcode & 0x00F
        res = self.get_mem(mn) - 1
        self._ZF = res == 0
        self._CF = res < 0
        self.set_mem(mn, res & 0xF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7
   
    def _ld_mn_a(self, opcode):
        #M(n3~n0) ← A
        self.set_mem(opcode & 0x00F, self._A)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _ld_mn_b(self, opcode):
        #M(n3~n0) ← B
        self.set_mem(opcode & 0x00F, self._B)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
   
    def _ld_a_mn(self, opcode):
        #A ← M(n3~n0)
        self._A = self.get_mem(opcode & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
 
    def _ld_b_mn(self, opcode):
        #B ← M(n3~n0)
        self._B = self.get_mem(opcode & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
    
    def _push_r(self, opcode):
        #SP← SP-1, M(SP)←r
        r = opcode & 0x3
        self._SP = self._SP - 1 & 0xFF
        self.set_mem(self._SP, self._get_abmxmy_tbl[r](self))
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _push_xp(self, opcode):
        #SP ← SP-1, M(SP) ← XP
        self._SP = self._SP - 1 & 0xFF
        self.set_mem(self._SP, self._IX >> 8)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _push_xh(self, opcode):
        #SP ← SP-1, M(SP) ← XH
        self._SP = self._SP - 1 & 0xFF
        self.set_mem(self._SP, self._IX >> 4 & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
 
    def _push_xl(self, opcode):
        #SP ← SP-1, M(SP) ← XL
        self._SP = self._SP - 1 & 0xFF
        self.set_mem(self._SP, self._IX & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
    
    def _push_yp(self, opcode):
        #SP ← SP-1, M(SP) ← YP
        self._SP = self._SP - 1 & 0xFF
        self.set_mem(self._SP, self._IY >> 8)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _push_yh(self, opcode):
        #SP ← SP-1, M(SP) ← YH
        self._SP = self._SP - 1 & 0xFF
        self.set_mem(self._SP, self._IY >> 4 & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
 
    def _push_yl(self, opcode):
        #SP ← SP-1, M(SP) ← YL
        self._SP = self._SP - 1 & 0xFF
        self.set_mem(self._SP, self._IY & 0x00F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _push_f(self, opcode):
        #SP← SP-1, M(SP)←F
        self._SP = self._SP - 1 & 0xFF
        self.set_mem(self._SP, self._IF << 3 | self._DF << 2 | self._ZF << 1 | self._CF)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
  
    def _dec_sp(self, opcode):
        #SP← SP-1
        self._SP = self._SP - 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
  
    def _pop_r(self, opcode):
        #r←M(SP), SP←SP+1
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self.get_mem(self._SP))
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _pop_xp(self, opcode):
        #XP ← M(SP), SP ← SP+1
        self._IX = self.get_mem(self._SP) << 8 | (self._IX & 0x0FF)
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _pop_xh(self, opcode):
        #XH← M(SP), SP ← SP+1
        self._IX = self.get_mem(self._SP) << 4 | (self._IX & 0xF0F)
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _pop_xl(self, opcode):
        #XL ← M(SP), SP ← SP+1
        self._IX = self.get_mem(self._SP) | (self._IX & 0xFF0)
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
 
    def _pop_yp(self, opcode):
        #YP ← M(SP), SP ← SP+1
        self._IY = self.get_mem(self._SP) << 8 | (self._IY & 0x0FF)
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _pop_yh(self, opcode):
        #YH← M(SP), SP ← SP+1
        self._IY = self.get_mem(self._SP) << 4 | (self._IY & 0xF0F)
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _pop_yl(self, opcode):
        #YL ← M(SP), SP ← SP+1
        self._IY = self.get_mem(self._SP) | (self._IY & 0xFF0)
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _pop_f(self, opcode):
        #F←M(SP), SP←SP+1
        f = self.get_mem(self._SP)
        self._CF = f & 0x1
        self._ZF = f >> 1 & 0x1
        self._DF = f >> 2 & 0x1
        new_IF = f >> 3 & 0x1
        self._if_delay  = (new_IF and not self._IF)
        self._IF = new_IF
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _inc_sp(self, opcode):
        #SP← SP+1
        self._SP = self._SP + 1 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5
   
    def _rets(self, opcode):
        #PCSL ← M(SP), PCSH ← M(SP+1), PCP ← M(SP+2) SP←SP+3, PC←PC+1
        self._PC = (self._PC & 0x1000) | self.get_mem(self._SP) | self.get_mem(self._SP + 1) << 4 | self.get_mem(self._SP + 2) << 8
        self._SP = self._SP + 3 & 0xFF
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 12

    def _ret(self, opcode):
        #PCSL ← M(SP), PCSH ← M(SP+1), PCP ← M(SP+2) SP ← SP+3
        self._PC = self._NPC = (self._PC & 0x1000) | self.get_mem(self._SP) | self.get_mem(self._SP + 1) << 4 | self.get_mem(self._SP + 2) << 8
        self._SP = self._SP + 3 & 0xFF

        return 7

    def _ld_sph_r(self, opcode):
        # SPH←r
        r = opcode & 0x3
        self._SP = self._get_abmxmy_tbl[r](self) << 4 | (self._SP & 0x0F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)
        
        return 5

    def _ld_r_sph(self, opcode):
        #r←SPH
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._SP >> 4)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _jpba(self, opcode):
        #PCB←NBP, PCP←NPP, PCSH←B, PCSL ←A
        self._PC = (self._NPC & 0x1F00) | self._B << 4 | self._A

        return 5

    def _ld_spl_r(self, opcode):
        #SPL ← r
        r = opcode & 0x3
        self._SP = self._get_abmxmy_tbl[r](self) | (self._SP & 0xF0)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)
        
        return 5

    def _ld_r_spl(self, opcode):
        r = opcode & 0x3
        self._set_abmxmy_tbl[r](self, self._SP & 0x0F)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _halt(self, opcode):
        #Halt (stop clock)
        self._HALT = 1
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5           #1 1 1 1  1 1 1 1  1 0 0 0                          5
  
    def _nop5(self, opcode):
        #No operation (5 clock cycles)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 5

    def _nop7(self, opcode):
        #No operation (7 clock cycles)
        self._PC = self._NPC = (self._PC & 0x1000) | (self._PC + 1 & 0xFFF)

        return 7
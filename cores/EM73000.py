from .rom import ROM
from .EM73000sound import EM73000sound

ROM_SIZE = 0x1FFF
RAM_SIZE = 256 + 128

EMPTY_VRAM = tuple([0] * RAM_SIZE)

STACK_OFFSET = 0x0C0

INT0_ID = 5
IRESERVED_ID = 4
TRGA_ID = 3
TRGB_ID = 2
TBI_ID = 1
INT1_ID = 0

INT_ENTRYS = {INT0_ID: 0x002, IRESERVED_ID: 0x004, TRGA_ID: 0x006, TRGB_ID: 0x008, TBI_ID: 0x00A, INT1_ID: 0x00C}

TIMER_DIV = [1 <<  10, 1 <<  14, 1 <<  18, 1 <<  22]
TIME_BASE_DIV = [0, 0, 0, 0, 1 <<  10, 1 <<  11, 1 <<  12, 1 <<  13, 0, 0, 0, 0, 1 <<  9, 1 <<  8, 1 <<  15, 1 <<  17]
WARMUP_TIME = [1 <<  18, 1 <<  14, 1 <<  16, 8]

MASK2IL = [0x20, 0x21, 0x26, 0x27, 0x28, 0x29, 0x2E, 0x2F, 0x30, 0x31, 0x36, 0x37, 0x38, 0x39, 0x3E, 0x3F]

P0_WAKEUP0 = 1
P0_WAKEUP1 = 2
P0_WAKEUP2 = 4
P0_WAKEUP3 = 8
P4_NSOUND = 1
P8_NINT1 = 1
P8_NWAKEUPA = 1
P8_TRGB = 2
P8_NWAKEUPB = 2
P8_NINT0 = 4
P8_NWAKEUPC = 4
P8_TRGA = 8
P8_NWAKEUPD = 8
P9_RAM_BANK = 8
P16_SWWT = 3
P16_SWWTL = 1
P16_SWWTH = 2
P16_SE = 4
P16_WM = 8
P27_LDC = 0xC
P27_LDCL = 4
P27_LDCH = 8
P28_IPSA = 3
P28_IPSAL = 1
P28_IPSAH = 2
P28_TMSA = 0xC
P28_TMSAL = 4
P28_TMSAH = 8
P29_IPSB = 3
P29_IPSBL = 1
P29_IPSBH = 2
P29_TMSB = 0xC
P29_TMSBL = 4
P29_TMSBH = 8
P30_SMODE = 0x3
P30_SMODEL = 1
P30_SMODEH = 2
P30_BFREQ = 0xC
P30_BFREQL = 4
P30_BFREQH = 8

class EM73000():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = EM73000sound(clock)
        
        self._P0_pullup_mask = mask['port_pullup']['P0']
        self._P7_pullup_mask = mask['port_pullup']['P7']
        self._P8_pullup_mask = 0xF
    
        self._P0_wakeup_mask = mask['port_wakeup']['P0']
        self._P8_wakeup_mask = mask['port_wakeup']['P8']

        self._reset()

        self._instr_counter = 0
        self._cycle_counter = 0

        self._io_tbl = {
            0: (EM73000._get_io_P0, EM73000._set_io_dummy),
            4: (EM73000._get_io_P4, EM73000._set_io_P4),
            5: (EM73000._get_io_dummy, EM73000._set_io_P5),
            6: (EM73000._get_io_dummy, EM73000._set_io_P6),
            7: (EM73000._get_io_P7, EM73000._set_io_dummy),
            8: (EM73000._get_io_P8, EM73000._set_io_P8),
            9: (EM73000._get_io_dummy, EM73000._set_io_P9),
            16: (EM73000._get_io_dummy, EM73000._set_io_P16),
            23: (EM73000._get_io_dummy, EM73000._set_io_P23),
            24: (EM73000._get_io_dummy, EM73000._set_io_P24),
            25: (EM73000._get_io_dummy, EM73000._set_io_P25),
            27: (EM73000._get_io_dummy, EM73000._set_io_P27),
            28: (EM73000._get_io_dummy, EM73000._set_io_P28),
            29: (EM73000._get_io_dummy, EM73000._set_io_P29),
            30: (EM73000._get_io_dummy, EM73000._set_io_P30),
        }

        self._execute = (
            *([EM73000._sbr_a] * 64),       #00aa aaaa If SF=1 then PC¬PC12-6.a5-0 1 1 - - 1 else null
            *([EM73000._lcall_a] * 8),      #0100 0aaa aaaa aaaa STACK[SP]¬PC, 2 2 - - - SP¬SP -1, PC¬a
            EM73000._std_k_y,               #0100 1000 kkkk yyyy RAM[y]¬k 2 2 - - 1
            EM73000._add_k_y,               #0100 1001 kkkk yyyy RAM[y]¬RAM[y] +k 2 2 - Z C'
            EM73000._out_k_p,               #0100 1010 kkkk pppp PORT[p]¬k 2 2 - - 1
            EM73000._cmp_k_y,               #0100 1011 kkkk yyyy k-RAM[y] 2 2 C Z Z'
            EM73000._exhl_x,                #0100 1100 xxxx xx00 LR«RAM[x], HR«RAM[x+1] 2 2 - - 1
            EM73000._rti,                   #0100 1101 SP¬SP+1,FLAG.PC 1 2 * * * ¬STACK[SP],EIF ¬1
            EM73000._ldhl_x,                #0100 1110 xxxx xx00 LR¬RAM[x],HR¬RAM[x+1] 2 2 - - 1
            EM73000._ret,                   #0100 1111 SP¬SP + 1, PC¬STACK[SP] 1 2 - - -
            EM73000._rlca,                  #0101 0000 ¬CF¬Acc¬ 1 1 C Z C'
            EM73000._rrca,                  #0101 0001 ®CF®Acc® 1 1 C Z C'
            EM73000._ttcfs,                 #0101 0010 SF¬CF, CF¬1 1 1 1 - *
            EM73000._tfcfc,                 #0101 0011 SF¬CF', CF¬0 1 1 0 - *
            EM73000._dummy,
            EM73000._slbr1_a,               #0101 0101 1100 aaaa aaaa aaaa (a:1000h~1FFFh) SF=1; PC ¬ a ( branch condition satisified)
            EM73000._nop,                   #0101 0110 no operation 1 1 - - -
            EM73000._slbr0_a,               #0101 0111 1100 aaaa aaaa aaaa (a:0000h~0FFFh) SF=1; PC ¬ a ( branch condition satisified)
            EM73000._exam,                  #0101 1000 Acc«RAM[HL] 1 1 - Z 1
            EM73000._stam,                  #0101 1001 RAM[HL]¬Acc 1 1 - - 1
            EM73000._ldam,                  #0101 1010 Acc ¬RAM[HL] 1 1 - Z 1
            EM73000._tzs,                   #0101 1011 SF¬ZF 1 1 - - *
            EM73000._deca,                  #0101 1100 Acc¬Acc-1 1 1 - Z C
            EM73000._decm,                  #0101 1101 RAM[HL]¬RAM[HL] -1 1 1 - Z C
            EM73000._inca,                  #0101 1110 Acc¬Acc + 1 1 1 - Z C'
            EM73000._incm,                  #0101 1111 RAM[HL]¬RAM[HL]+1 1 1 - Z C'
            EM73000._clpl,                  #0110 0000 PORT[LR3-2+4]LR1-0¬0 1 2 - - 1
            EM73000._tfpl,                  #0110 0001 SF¬PORT[LR 3-2 +4]LR1-0' 1 2 - - *
            EM73000._sepl,                  #0110 0010 PORT[LR3-2+4]LRl-0¬1 1 2 - - 1
            EM73000._cil,                   #0110 0011
            EM73000._exal,                  #0110 0100 Acc«LR 1 2 - Z 1
            EM73000._ldax,                  #0110 0101 Acc¬ROM[DP]L 1 2 - Z 1
            EM73000._exah,                  #0110 0110 Acc«HR 1 2 - Z 1
            EM73000._ldaxi,                 #0110 0111 Acc¬ROM[DP]H,DP+1 1 2 - Z 1
            EM73000._exa_x,                 #0110 1000 xxxx xxxx Acc«RAM[x] 2 2 - Z 1
            EM73000._sta_x,                 #0110 1001 xxxx xxxx RAM[x]¬Acc 2 2 - - 1
            EM73000._lda_x,                 #0110 1010 xxxx xxxx Acc¬RAM[x] 2 2 - Z 1
            EM73000._cmpa_x,                #0110 1011 xxxx xxxx RAM[x]-Acc 2 2 C Z Z'
            EM73000._bit_y_b,               #0110 1100
            EM73000._bit_p_b,               #0110 1101 
            EM73000._math_k,                #0110 1110
            EM73000._io_p,                  #0110 1111
            EM73000._adcam,                 #0111 0000 Acc¬Acc + RAM[HL] + CF 1 1 C Z C'
            EM73000._addam,                 #0111 0001 Acc¬Acc + RAM[HL] 1 1 - Z C'
            EM73000._sbcam,                 #0111 0010 Acc¬RAM[HLl - Acc - CF' 1 1 C Z C
            EM73000._cmpam,                 #0111 0011 RAM[HL] - Acc 1 1 C Z Z'
            EM73000._tla,                   #0111 0100 Acc¬LR 1 1 - Z 1
            EM73000._exae,                  #0111 0101 MASK«Acc 1 1 - - 1
            EM73000._tha,                   #0111 0110 Acc¬HR 1 1 - Z 1
            EM73000._dummy,
            EM73000._oram,                  #0111 1000 Acc ¬Acc RAM[HL] 1 1 - Z Z'
            EM73000._xoram,                 #0111 1001 Acc¬Acc^RAM[HL] 1 1 - Z Z'
            EM73000._dummy,
            EM73000._andam,                 #0111 1011 Acc¬Acc & RAM[HL] 1 1 - Z Z'
            EM73000._decl,                  #0111 1100 LR¬LR-1 1 1 - Z C
            EM73000._stamd,                 #0111 1101 RAM[HL]¬Acc, LR-1 1 1 - Z C
            EM73000._incl,                  #0111 1110 LR¬LR + 1 1 1 - Z C'
            EM73000._stami,                 #0111 1111 RAM[HL]¬Acc, LR+1 1 1 - Z C'
            *([EM73000._ldl_k] * 16),       #1000 kkkk LR¬k 1 1 - - 1
            *([EM73000._ldh_k] * 16),       #1001 kkkk HR¬k 1 1 - - 1
            *([EM73000._stdmi_k] * 16),     #1010 kkkk RAM[HL]¬k, LR+1 1 1 - Z C'
            *([EM73000._cmpia_k] * 16),     #1011 kkkk k - Acc 1 1 C Z Z'
            *([EM73000._lbr_a] * 16),       #1100 aaaa aaaa aaaa If SF= 1 then PC¬a else null 2 2 - - 1
            *([EM73000._ldia_k] * 16),      #1101 kkkk Acc¬k 1 1 - Z 1
            *([EM73000._scall_a] * 16),     #1110 nnnn STACK[SP]¬PC, 1 2 - - - SP¬SP - 1, PC¬a, a = 8n + 6 (n =1~15),0086h (n = 0)
            *([EM73000._clm_b] * 4),        #1111 00bb RAM[HL]b¬0 1 1 - - 1
            *([EM73000._sem_b] * 4),        #1111 01bb RAM[HL]b¬1 1 1 - - 1
            *([EM73000._tfa_b] * 4),        #1111 10bb SF¬Accb' 1 1 - - *
            *([EM73000._tfm_b] * 4),        #1111 11bb SF¬RAM[HL]b' 1 1 - - *
        )

        self._execute_cil = (
            EM73000._dummy,
            EM73000._eicil_r,               #0110 0011 01rr rrrr EIF¬1,IL¬IL&r 2 2 - - 1
            EM73000._dicil_r,               #0110 0011 10rr rrrr EIF¬0,IL¬IL&r 2 2 - - 1
            EM73000._cil_r,                 #0110 0011 11rr rrrr IL¬IL & r 2 2 - - 1
        )

        self._execute_bit_y_b = (
            EM73000._tf_y_b,                #0110 1100 00bb yyyy SF¬RAM[y]b' 2 2 - - *
            EM73000._set_y_b,               #0110 1100 01bb yyyy RAM[y]b¬1 2 2 - - 1
            EM73000._tt_y_b,                #0110 1100 10bb yyyy SF¬RAM[y]b 2 2 - - *
            EM73000._clr_y_b,               #0110 1100 11bb yyyy RAM[y]b¬0 2 2 - - 1
        )

        self._execute_bit_p_b = (
            EM73000._tfp_p_b,               #0110 1101 00bb pppp SF¬PORT[p]b' 2 2 - - *
            EM73000._sep_p_b,               #0110 1101 01bb pppp PORT[p]b¬1 2 2 - - 1
            EM73000._ttp_p_b,               #0110 1101 10bb pppp SF¬PORT[p]b 2 2 - - *
            EM73000._clp_p_b,               #0110 1101 11bb pppp PORT[p]b¬0 2 2 - - 1
        )

        self._execute_math_k = (
            EM73000._dummy,
            EM73000._addl_k,                #0110 1110 0001 kkkk LR¬LR+k 2 2 - Z C'
            EM73000._dummy,
            EM73000._cmpl_k,                #0110 1110 0011 kkkk k-LR 2 2 - Z C
            EM73000._ora_k,                 #0110 1110 0100 kkkk Acc¬Acc k 2 2 - Z Z'
            EM73000._adda_k,                #0110 1110 0101 kkkk Acc¬Acc+k 2 2 - Z C'
            EM73000._anda_k,                #0110 1110 0110 kkkk Acc¬Acc&k 2 2 - Z Z'
            EM73000._suba_k,                #0110 1110 0111 kkkk Acc¬k-Acc 2 2 - Z C
            EM73000._dummy,
            EM73000._addh_k,                #0110 1110 1001 kkkk HR¬HR+k 2 2 - Z C'
            EM73000._dummy,
            EM73000._cmph_k,                #0110 1110 1011 kkkk k - HR 2 2 - Z C
            EM73000._orm_k,                 #0110 1110 1100 kkkk RAM[HL]¬RAM[HL] k 2 2 - Z Z'
            EM73000._addm_k,                #0110 1110 1101 kkkk RAM[HL]¬RAM[HL] +k 2 2 - Z C'
            EM73000._andm_k,                #0110 1110 1110 kkkk RAM[HL]¬RAM[HL]&k 2 2 - Z Z'
            EM73000._subm_k,                #0110 1110 1111 kkkk RAM[HL]¬k - RAM[HL] 2 2 - Z C
        )

        self._execute_io_p = (
            EM73000._outa_p,                #0110 1111 000p pppp PORT[p]¬Acc 2 2 - - 1
            EM73000._ina_p,                 #0110 1111 0100 pppp Acc¬PORT[p] 2 2 - Z Z'
            EM73000._outm_p,                #0110 1111 100p pppp PORT[p]¬RAM[HL] 2 2 - - 1
            EM73000._inm_p,                 #0110 1111 1100 pppp RAM[HL]¬PORT[p] 2 2 - - Z'
        )

    def _reset(self):
        self._ACC = 0

        self._PC = 0
        self._SP = 0
        self._DP = 0

        self._HL = 0

        self._EI = 0
       
        self._CF = 0
        self._ZF = 0
        self._SF = 1

        self._TIMERA = 0
        self._TIMERB = 0

        self._IL = 0
        self._IMASK = 0
        
        self._RAM = [0] * RAM_SIZE

        self._P0 = self._P0_pullup_mask
        self._P4 = 0x0
        self._P5 = 0x0
        self._P6 = 0x0
        self._P7 = self._P7_pullup_mask
        self._P8 = self._P8_pullup_mask
        self._P9 = 0x0
        self._P16 = 0x0
        self._P23 = 0xF
        self._P24 = 0xF
        self._P25 = 0x0
        self._P27 = 0x0
        self._P28 = 0x0
        self._P29 = 0x0
        self._P30 = 0x0

        self._timerA_counter = 0
        self._timerB_counter = 0
        self._time_base_counter = 0

        self._ram_bank = 0

    def reset(self):
        self._reset()

    def _set_io_dummy(self, value):
        pass

    def _get_io_dummy(self):
        return 0

    def _get_io_P0(self):
        return self._P0

    def _set_io_P0(self, value):
        pass

    def _get_io_P4(self):
        return self._P4

    def _set_io_P5(self, value):
        self._P5 = value

    def _set_io_P6(self, value):
        self._P6 = value

    def _set_io_P4(self, value):
        self._P4 = value

    def _get_io_P7(self):
        return self._P7
    
    def _get_io_P8(self):
        return self._P8

    def _set_io_P8(self, value):
        pass

    def _set_io_P9(self, value):
        self._ram_bank = (value >> P9_RAM_BANK) * 256
        self._P9 = value

    def _set_io_P16(self, value):
        self._P16 = value

    def _set_io_P23(self, value):
        self._sound.set_freq_div(((self._P24 << 4) | value) + 1, self._cycle_counter)
        self._P23 = value

    def _set_io_P24(self, value):
        self._P24 = value

    def _set_io_P25(self, value):
        self._P25 = value

    def _set_io_P27(self, value):
        self._P27 = value

    def _set_io_P28(self, value):
        self._P28 = value
        self._timerA_counter = 0

    def _set_io_P29(self, value):
        self._P29 = value
        self._timerB_counter = 0

    def _set_io_P30(self, value):
        self._sound.set_basic_freq_div(4 << ((value & P30_BFREQ) >> 2))
        self._sound.set_mode(value & P30_SMODE, self._cycle_counter)
        self._P30 = value

    def examine(self):
        return {
            "ACC": self._ACC,
            "HL": self._HL,
            "PC": self._PC & 0xFFF,
            "SP": self._SP,
            "DP": self._DP,
            "IL": self._IL,
            "IMASK": self._IMASK,
            "TIMERA": self._TIMERA,
            "TIMERB": self._TIMERB,
            "CF": self._CF,
            "ZF": self._ZF,
            "SF": self._SF,
            "EI": self._EI,
            "RAM0": self._RAM[:256],
            "RAM1": self._RAM[256:384],
            "IO": (
                self._P0,
                self._P4,
                self._P5,
                self._P6,
                self._P7,
                self._P8,
                self._P9,
                self._P16,
                self._P23,
                self._P24,
                self._P25,
                self._P27,
                self._P28,
                self._P29,
                self._P30
            )
        }

    def edit_state(self, state):
        if ("CF" in state):
            self._CF = state["CF"]
        if ("ZF" in state):
            self._ZF = state["ZF"]
        if ("SF" in state):
            self._SF = state["SF"]
        if ("EI" in state):
            self._EI = state["EI"]
        if ("PC" in state):
            self._PC = state["PC"] & 0x1FFF
        if ("DP" in state):
            self._DP = state["DP"] & 0xFFF
        if ("SP" in state):
            self._SP = state["SP"] & 0xF
        if ("IL" in state):
            self._IF = state["IL"] & 0x3F
        if ("IMASK" in state):
            self._IMASK = state["IMASK"] & 0xF
        if ("ACC" in state):
            self._ACC = state["ACC"] & 0xF
        if ("HL" in state):
            self._HL = state["HL"] & 0xFF
        if ("TIMERA" in state):
            self._TIMERA = state["TIMERA"] & 0xFFF
        if ("TIMERB" in state):
            self._TIMERB = state["TIMERB"] & 0xFFF
        if ("RAM0" in state):
            for i, value in state["RAM0"].items():
                self._RAM[i] = value & 0xF
        if ("RAM1" in state):
            for i, value in state["RAM1"].items():
                self._RAM[256 + i] = value & 0xF
        if ("IO" in state):
            for i, value in state["IO"].items():
                if i in self._io_tbl:
                    list(self._io_tbl.values())[i][1](self, value & 0xF)
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
    
    def pin_set(self, port, pin, level):
        pin_mask = (1 << pin)
        if (port == 'P0'):
            prev_P0 = self._P0
            self._P0 = ~pin_mask & (self._P0 | (level << pin))
            if ((self._P0_wakeup_mask & prev_P0 & pin_mask) and ~(self._P0 & pin_mask)):
                self._P16 &= ~P16_SE
        elif (port == 'P7'):
            self._P7 = ~pin_mask & self._P7 | level << pin
        elif (port == 'P8'):
            prev_P8 = self._P8
            self._P8 = ~pin_mask & self._P8 | level << pin
            if ((self._P8_wakeup_mask & prev_P8 & pin_mask) and ~(self._P8 & pin_mask)):
                self._P16 &= ~P16_SE
            if ((prev_P8 & pin_mask) and ~(self._P8 & pin_mask)):
                self._IL |= ((pin == 0) << INT1_ID) | ((pin == 2) << INT0_ID)

    def pin_release(self, port, pin):
        pin_mask = (1 << pin)
        if (port == 'P0'):
            prev_P0 = self._P0
            self._P0 = self._P0 & ~pin_mask | self._P0_pullup_mask & pin_mask
            if ((self._P0_wakeup_mask & prev_P0 & pin_mask) and ~(self._P0 & pin_mask)):
                self._P16 &= ~P16_SE
        elif (port == 'P7'):
            self._P7 = self._P7 & ~pin_mask | self._P7_pullup_mask & pin_mask
        elif (port == 'P8'):
            prev_P8 = self._P8
            self._P8 = self._P8 & ~pin_mask | self._P8_pullup_mask & pin_mask
            if ((self._P8_wakeup_mask & prev_P8 & pin_mask) and ~(self._P8 & pin_mask)):
                self._P16 &= ~P16_SE

    def pc(self):
        return self._PC & 0xFFF
    
    def get_VRAM(self):
        if (not (self._P16 & P16_SE)):
            return tuple(self._RAM)
        else:
            return EMPTY_VRAM
    
    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter
            
    def _process_timer(self, exec_cycles):
        if (self._P28 & P28_TMSA == 0x8):
            self._timerA_counter -= exec_cycles
            if (self._timerA_counter <= 0):
                self._timerA_counter += TIMER_DIV[self._P28 & P28_IPSA]
                self._TIMERA = (self._TIMERA + 1) & 0xFFF
                if (self._TIMERA == 0):
                    self._IL |= 1 << TRGA_ID

        if (self._P29 & P29_TMSB == 0x8):
            self._timerB_counter -= exec_cycles
            if (self._timerB_counter <= 0):
                self._timerB_counter += TIMER_DIV[self._P29 & P29_IPSB]
                self._TIMERB = (self._TIMERB + 1) & 0xFFF
                if (self._TIMERB == 0):
                    self._IL |= 1 << TRGB_ID

        if (TIME_BASE_DIV[self._P25] > 0):
            self._time_base_counter -= exec_cycles
            if (self._time_base_counter <= 0):
                self._timerB_counter += TIME_BASE_DIV[self._P25]
                self._IL |= 1 << TBI_ID

    def _interrupt(self):
        for id in range(6):
            if (self._IL & (0x20 >> id) & MASK2IL[self._IMASK]): 
                pc = self._PC
                sp = STACK_OFFSET + (self._SP << 2)
                self._RAM[sp] = ((self._CF & 0x1) << 3) | ((self._ZF & 0x1) << 2) | ((self._SF & 0x1) << 1) | ((pc >> 12) & 0x1)
                self._RAM[sp + 1] = (pc >> 8) & 0xF
                self._RAM[sp + 2] = (pc >> 4) & 0xF
                self._RAM[sp + 3] = pc & 0xF
                self._SP = (self._SP - 1) & 0xF
                self._PC = INT_ENTRYS[5 - id]
                self._SF = 1
                self._EI = 0
                self._IL &= ~(0x20 >> id)
                return
            
    def clock(self):       
        if self._EI:
            self._interrupt()

        if (not (self._P16 & P16_SE)):
            opcode = self._ROM.getByte(self._PC)
            exec_cycles = self._execute[opcode](self, opcode)
            self._instr_counter += 1
            self._process_timer(exec_cycles)
            self._cycle_counter += exec_cycles
            return exec_cycles

        self._cycle_counter += WARMUP_TIME[self._P16 & P16_SWWT]
        return WARMUP_TIME[self._P16 & P16_SWWT]

    def _sbr_a(self, opcode):
        #00aa aaaa If SF=1 then PC¬PC12-6.a5-0 1 1 - - 1 else null
        self._PC = (self._PC + 1) & 0x1FFF
        if (self._SF):
            self._PC = (self._PC & 0x1FC0) | (opcode & 0x003F)
        self._SF = 1
        return 8
        
    def _lcall_a(self, opcode):
        #0100 0aaa aaaa aaaa STACK[SP]¬PC, 2 2 - - - SP¬SP -1, PC¬a
        pc = self._PC + 2
        sp = STACK_OFFSET + (self._SP << 2)
        self._RAM[sp] = pc >> 12
        self._RAM[sp + 1] = (pc >> 8) & 0xF
        self._RAM[sp + 2] = (pc >> 4) & 0xF
        self._RAM[sp + 3] = (pc) & 0xF
        self._PC = ((opcode & 0x07) << 8) | self._ROM.getByte((self._PC + 1) & 0x1FFF)
        self._SP = (self._SP - 1) & 0xF
        return 16
        
    def _std_k_y(self, opcode):
        #0100 1000 kkkk yyyy RAM[y]¬k 2 2 - - 1
        ky = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        k = (ky >> 4) & 0x0F
        y = ky & 0x0F
        self._RAM[y] = k
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _add_k_y(self, opcode):
        #0100 1001 kkkk yyyy RAM[y]¬RAM[y] +k 2 2 - Z C'
        ky = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        k = (ky >> 4) & 0x0F
        y = ky & 0x0F
        self._RAM[y] = (self._RAM[y] + k) & 0xF
        self._ZF = self._RAM[y] == 0
        self._SF = self._RAM[y] >= k
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _out_k_p(self, opcode):
        #0100 1010 kkkk pppp PORT[p]¬k 2 2 - - 1
        kp = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        k = (kp >> 4) & 0x0F
        p = kp & 0x0F
        self._io_tbl[p][1](self, k)
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _cmp_k_y(self, opcode):
        #0100 1011 kkkk yyyy k-RAM[y] 2 2 C Z Z'
        ky = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        k = (ky >> 4) & 0x0F
        y = ky & 0x0F
        self._CF = k >= self._RAM[y]
        self._ZF = k == self._RAM[y]
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _exhl_x(self, opcode):
        #0100 1100 xxxx xx00 LR«RAM[x], HR«RAM[x+1] 2 2 - - 1
        x = (self._ROM.getByte((self._PC + 1) & 0x1FFF)) & 0x00FF
        hl_tmp = self._HL
        self._HL = (self._RAM[self._ram_bank + x + 1] << 4) | self._RAM[self._ram_bank + x] 
        self._RAM[self._ram_bank + x] = hl_tmp & 0x0F
        self._RAM[self._ram_bank + x + 1] = (hl_tmp >> 4) & 0x0F
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _rti(self, opcode):
        #0100 1101 SP¬SP+1,FLAG.PC 1 2 * * * ¬STACK[SP],EIF ¬1
        self._SP = (self._SP + 1) & 0xF
        sp = STACK_OFFSET + (self._SP << 2)
        self._PC = ((self._RAM[sp] & 0x1) << 12) | (self._RAM[sp + 1] << 8) | (self._RAM[sp + 2] << 4) | self._RAM[sp + 3]
        self._CF = (self._RAM[sp] & 0x8) > 0
        self._ZF = (self._RAM[sp] & 0x4) > 0
        self._SF = (self._RAM[sp] & 0x2) > 0
        self._EI = 1
        return 16
        
    def _ldhl_x(self, opcode):
        #0100 1110 xxxx xx00 LR¬RAM[x],HR¬RAM[x+1] 2 2 - - 1
        x = (self._ROM.getByte((self._PC + 1) & 0x1FFF)) & 0x00FF
        self._HL = (self._RAM[self._ram_bank + x + 1] << 4) | self._RAM[self._ram_bank + x] 
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _ret(self, opcode):
        #0100 1111 SP¬SP + 1, PC¬STACK[SP] 1 2 - - -
        self._SP = (self._SP + 1) & 0xF
        sp = STACK_OFFSET + (self._SP << 2)
        self._PC = ((self._RAM[sp] & 0x1) << 12) | (self._RAM[sp + 1] << 8) | (self._RAM[sp + 2] << 4) | self._RAM[sp + 3]
        return 16
        
    def _rlca(self, opcode):
        #0101 0000 ¬CF¬Acc¬ 1 1 C Z C'
        cf = (self._ACC & 0x8) > 0
        self._ACC = ((self._ACC << 1) & 0xE) | (self._CF & 0x1)
        self._CF = cf
        self._ZF = self._ACC == 0
        self._SF = 1 - cf
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _rrca(self, opcode):
        #0101 0001 ®CF®Acc® 1 1 C Z C'
        cf = (self._ACC & 0x1) > 0
        self._ACC = ((self._ACC >> 1) & 0x7) | ((self._CF << 3) & 0x8)
        self._CF = cf
        self._ZF = self._ACC == 0
        self._SF = 1 - cf
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _ttcfs(self, opcode):
        #0101 0010 SF¬CF, CF¬1 1 1 1 - *
        self._SF = self._CF
        self._CF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _tfcfc(self, opcode):
        #0101 0011 SF¬CF', CF¬0 1 1 0 - *
        self._SF = 1 - self._CF
        self._CF = 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _slbr1_a(self, opcode):
        #0101 0101 1100 aaaa aaaa aaaa (a:1000h~1FFFh) SF=1; PC ¬ a ( branch condition satisified)
        self._PC = (self._PC + 3) & 0x1FFF
        if (self._SF):
            self._PC = 0x1000 | (self._ROM.getWord((self._PC - 2) & 0x1FFF) & 0x0FFF)
        self._SF = 1
        return 24

    def _slbr0_a(self, opcode):
        #0101 0111 1100 aaaa aaaa aaaa (a:0000h~0FFFh) SF=1; PC ¬ a ( branch condition satisified)
        self._PC = (self._PC + 3) & 0x1FFF
        if (self._SF):
            self._PC = self._ROM.getWord((self._PC - 2) & 0x1FFF) & 0x0FFF
        self._SF = 1
        return 24
            
    def _nop(self, opcode):
        #0101 0110 no operation 1 1 - - -
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _exam(self, opcode):
        #0101 1000 Acc«RAM[HL] 1 1 - Z 1
        acc_tmp = self._ACC
        self._ACC = self._RAM[self._ram_bank + self._HL]
        self._RAM[self._ram_bank + self._HL] = acc_tmp
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _stam(self, opcode):
        #0101 1001 RAM[HL]¬Acc 1 1 - - 1
        self._RAM[self._ram_bank + self._HL] = self._ACC
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _ldam(self, opcode):
        #0101 1010 Acc ¬RAM[HL] 1 1 - Z 1
        self._ACC = self._RAM[self._ram_bank + self._HL]
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _tzs(self, opcode):
        #0101 1011 SF¬ZF 1 1 - - *
        self._SF = self._ZF
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _deca(self, opcode):
        #0101 1100 Acc¬Acc-1 1 1 - Z C
        self._ACC = self._ACC - 1 & 0x0F
        self._ZF = self._ACC == 0
        self._SF = self._ACC != 15
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _decm(self, opcode):
        #0101 1101 RAM[HL]¬RAM[HL] -1 1 1 - Z C
        self._RAM[self._ram_bank + self._HL] = (self._RAM[self._ram_bank + self._HL] - 1) & 0x0F
        self._ZF = self._RAM[self._ram_bank + self._HL] == 0
        self._SF = self._RAM[self._ram_bank + self._HL] != 15
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _inca(self, opcode):
        #0101 1110 Acc¬Acc + 1 1 1 - Z C'
        self._ACC = self._ACC + 1 & 0x0F
        self._ZF = self._ACC == 0
        self._SF = self._ACC != 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _incm(self, opcode):
        #0101 1111 RAM[HL]¬RAM[HL]+1 1 1 - Z C'
        self._RAM[self._ram_bank + self._HL] = (self._RAM[self._ram_bank + self._HL] + 1) & 0x0F
        self._ZF = self._RAM[self._ram_bank + self._HL] == 0
        self._SF = self._RAM[self._ram_bank + self._HL] != 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _clpl(self, opcode):
        #0110 0000 PORT[LR3-2+4]LR1-0¬0 1 2 - - 1
        bit = self._HL & 0x03
        port = ((self._HL & 0x0C) >> 2) + 4                           #to-do (>> 2)?
        new_value = self._io_tbl[port][0](self) & ~(0x1 << bit) 
        self._io_tbl[port][1](self, new_value)
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 16
        
    def _tfpl(self, opcode):
        #0110 0001 SF¬PORT[LR 3-2 +4]LR1-0' 1 2 - - *
        bit = self._HL & 0x03
        port = ((self._HL & 0x0C) >> 2) + 4
        self._SF = (self._io_tbl[port][0](self) & (0x1 << bit)) == 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 16
        
    def _sepl(self, opcode):
        #0110 0010 PORT[LR3-2+4]LRl-0¬1 1 2 - - 1
        bit = self._HL & 0x03
        port = ((self._HL & 0x0C) >> 2) + 4
        new_value = self._io_tbl[port][0](self) | (0x1 << bit) 
        self._io_tbl[port][1](self, new_value)
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 16
    
    def _cil(self, opcode):
        #0110 0011
        id = (self._ROM.getByte((self._PC + 1) & 0x1FFF) >> 6) & 0x03
        return self._execute_cil[id](self, opcode)
        
    def _cil_r(self, opcode):
        #0110 0011 11rr rrrr IL¬IL & r 2 2 - - 1
        r = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x3F
        self._IL &= r
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
    
    def _dicil_r(self, opcode):
        #0110 0011 10rr rrrr EIF¬0,IL¬IL&r 2 2 - - 1
        r = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x3F
        self._IL &= r
        self._EI = 0
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
    
    def _eicil_r(self, opcode):
        #0110 0011 01rr rrrr EIF¬1,IL¬IL&r 2 2 - - 1
        r = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x3F
        self._IL &= r
        self._EI = 1
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
                    
    def _exal(self, opcode):
        #0110 0100 Acc«LR 1 2 - Z 1
        acc_tmp = self._ACC
        self._ACC = self._HL & 0x0F
        self._HL = (self._HL & 0xF0) | acc_tmp
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 16
        
    def _ldax(self, opcode):
        #0110 0101 Acc¬ROM[DP]L 1 2 - Z 1
        self._ACC = self._ROM.getByte(0x1000 | self._DP) & 0x0F
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 16
        
    def _exah(self, opcode):
        #0110 0110 Acc«HR 1 2 - Z 1
        acc_tmp = self._ACC
        self._ACC = (self._HL >> 4) & 0x0F
        self._HL = (self._HL & 0x0F) | (acc_tmp << 4)
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 16
        
    def _ldaxi(self, opcode):
        #0110 0111 Acc¬ROM[DP]H,DP+1 1 2 - Z 1
        self._ACC = (self._ROM.getByte(0x1000 | self._DP) >> 4) & 0x0F
        self._DP = (self._DP + 1) & 0xFFF
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 16
        
    def _exa_x(self, opcode):
        #0110 1000 xxxx xxxx Acc«RAM[x] 2 2 - Z 1
        x = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        acc_tmp = self._ACC
        self._ACC = self._RAM[self._ram_bank + x]
        self._RAM[self._ram_bank + x] = acc_tmp
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _sta_x(self, opcode):
        #0110 1001 xxxx xxxx RAM[x]¬Acc 2 2 - - 1
        x = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        if (x < 0xF4):
            self._RAM[self._ram_bank + x] = self._ACC
        elif (x == 0xF4):
            self._TIMERA = (self._TIMERA & 0xFF0) | self._ACC
        elif (x == 0xF5):
            self._TIMERA = (self._TIMERA & 0xF0F) | (self._ACC << 4)
        elif (x == 0xF6):
            self._TIMERA = (self._TIMERA & 0x0FF) | (self._ACC << 8)
        elif (x == 0xF8):
            self._TIMERB = (self._TIMERB & 0xFF0) | self._ACC
        elif (x == 0xF9):
            self._TIMERB = (self._TIMERB & 0xF0F) | (self._ACC << 4)
        elif (x == 0xFA):
            self._TIMERB = (self._TIMERB & 0x0FF) | (self._ACC << 8)
        elif (x == 0xFC):
            self._DP = (self._DP & 0xFF0) | self._ACC
        elif (x == 0xFD):
            self._DP = (self._DP & 0xF0F) | (self._ACC << 4)
        elif (x == 0xFE):
            self._DP = (self._DP & 0x0FF) | (self._ACC << 8)
        elif (x == 0xFF):
            self._SP = self._ACC
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _lda_x(self, opcode):
        #0110 1010 xxxx xxxx Acc¬RAM[x] 2 2 - Z 1
        x = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        if (x < 0xF4):
            self._ACC = self._RAM[self._ram_bank + x]
        elif (x == 0xF4):
            self._ACC = self._TIMERA & 0x00F
        elif (x == 0xF5):
            self._ACC = (self._TIMERA >> 4) & 0x00F
        elif (x == 0xF6):
            self._ACC = (self._TIMERA >> 8) & 0x00F
        elif (x == 0xF8):
            self._ACC = self._TIMERB & 0x00F
        elif (x == 0xF9):
            self._ACC = (self._TIMERB >> 4) & 0x00F
        elif (x == 0xFA):
            self._ACC = (self._TIMERB >> 8) & 0x00F
        elif (x == 0xFC):
            self._ACC = self._DP & 0x00F
        elif (x == 0xFD):
            self._ACC = (self._DP >> 4) & 0x00F
        elif (x == 0xFE):
            self._ACC = (self._DP >> 8) & 0x00F
        elif (x == 0xFF):
            self._ACC = self._SP
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
        
    def _cmpa_x(self, opcode):
        #0110 1011 xxxx xxxx RAM[x]-Acc 2 2 C Z Z'
        x = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        self._CF = self._RAM[self._ram_bank + x] >= self._ACC
        self._ZF = self._RAM[self._ram_bank + x] == self._ACC
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _bit_y_b(self, opcode):
        #0110 1100
        id = (self._ROM.getByte((self._PC + 1) & 0x1FFF) >> 6) & 0x03
        return self._execute_bit_y_b[id](self, opcode)
    
    def _tf_y_b(self, opcode):
        #0110 1100 00bb yyyy SF¬RAM[y]b' 2 2 - - *
        by = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        b = (by >> 4) & 0x03
        y = by & 0x0F
        self._SF = self._RAM[y] & (0x1 << b) == 0
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _set_y_b(self, opcode):
        #0110 1100 01bb yyyy RAM[y]b¬1 2 2 - - 1
        by = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        b = (by >> 4) & 0x03
        y = by & 0x0F
        self._RAM[y] = self._RAM[y] | (0x1 << b)
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _tt_y_b(self, opcode):
        #0110 1100 10bb yyyy SF¬RAM[y]b 2 2 - - *
        by = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        b = (by >> 4) & 0x03
        y = by & 0x0F
        self._SF = (self._RAM[y] & (0x1 << b)) > 0
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _clr_y_b(self, opcode):
        #0110 1100 11bb yyyy RAM[y]b¬0 2 2 - - 1
        by = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        b = (by >> 4) & 0x03
        y = by & 0x0F
        self._RAM[y] = self._RAM[y] & ~(0x1 << b)
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _bit_p_b(self, opcode):
        #0110 1101
        id = (self._ROM.getByte((self._PC + 1) & 0x1FFF) >> 6) & 0x03
        return self._execute_bit_p_b[id](self, opcode)
    
    def _tfp_p_b(self, opcode):
        #0110 1101 00bb pppp SF¬PORT[p]b' 2 2 - - *
        bp = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        b = (bp >> 4) & 0x03
        p = bp & 0x0F
        self._SF = (self._io_tbl[p][0](self) & (0x1 << b)) == 0
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _sep_p_b(self, opcode):
        #0110 1101 01bb pppp PORT[p]b¬1 2 2 - - 1
        bp = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        b = (bp >> 4) & 0x03
        p = bp & 0x0F
        self._io_tbl[p][1](self, self._io_tbl[p][0](self) | (0x1 << b))
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _ttp_p_b(self, opcode):
        #0110 1101 10bb pppp SF¬PORT[p]b 2 2 - - *
        bp = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        b = (bp >> 4) & 0x03
        p = bp & 0x0F
        self._SF = (self._io_tbl[p][0](self) & (0x1 << b)) > 0
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _clp_p_b(self, opcode):
        #0110 1101 11bb pppp PORT[p]b¬0 2 2 - - 1
        bp = self._ROM.getByte((self._PC + 1) & 0x1FFF)
        b = (bp >> 4) & 0x03
        p = bp & 0x0F
        self._io_tbl[p][1](self, self._io_tbl[p][0](self) & ~(0x1 << b))
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _math_k(self, opcode):
        #0110 1110
        id = (self._ROM.getByte((self._PC + 1) & 0x1FFF) >> 4) & 0x0F
        return self._execute_math_k[id](self, opcode)

    def _addl_k(self, opcode):
        #0110 1110 0001 kkkk LR¬LR+k 2 2 - Z C'
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._HL = (self._HL & 0xF0) | ((self._HL + k) & 0x0F)
        self._ZF = (self._HL & 0x0F) == 0
        self._SF = (self._HL & 0x0F) >= k
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _cmpl_k(self, opcode):
        #0110 1110 0011 kkkk k-LR 2 2 - Z C
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._ZF = k == (self._HL & 0x0F)
        self._SF = k >= (self._HL & 0x0F)
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _ora_k(self, opcode):
        #0110 1110 0100 kkkk Acc¬Acc k 2 2 - Z Z'
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._ACC |= k
        self._ZF = self._ACC == 0
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _adda_k(self, opcode):
        #0110 1110 0101 kkkk Acc¬Acc+k 2 2 - Z C'
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._ACC = self._ACC + k & 0xF
        self._ZF = self._ACC == 0
        self._SF = self._ACC >= k
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _anda_k(self, opcode):
        #0110 1110 0110 kkkk Acc¬Acc&k 2 2 - Z Z'
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._ACC &= k
        self._ZF = self._ACC == 0
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _suba_k(self, opcode):
        #0110 1110 0111 kkkk Acc¬k-Acc 2 2 - Z C
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._ACC = k - self._ACC & 0xF
        self._ZF = self._ACC == 0
        self._SF = k >= self._ACC
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _addh_k(self, opcode):
        #0110 1110 1001 kkkk HR¬HR+k 2 2 - Z C'
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._HL = (self._HL + (k << 4)) & 0xFF
        self._ZF = (self._HL >> 4) == 0
        self._SF = (self._HL >> 4) >= k
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _cmph_k(self, opcode):
        #0110 1110 1011 kkkk k - HR 2 2 - Z C
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._ZF = (self._HL >> 4) == k
        self._SF = k >= (self._HL >> 4)
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _orm_k(self, opcode):
        #0110 1110 1100 kkkk RAM[HL]¬RAM[HL] k 2 2 - Z Z'
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._RAM[self._ram_bank + self._HL] |= k
        self._ZF = self._RAM[self._ram_bank + self._HL] == 0
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _addm_k(self, opcode):
        #0110 1110 1101 kkkk RAM[HL]¬RAM[HL] +k 2 2 - Z C'
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._RAM[self._ram_bank + self._HL] = (self._RAM[self._ram_bank + self._HL] + k) & 0xF
        self._ZF = self._RAM[self._ram_bank + self._HL] == 0
        self._SF = self._RAM[self._ram_bank + self._HL] >= k
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _andm_k(self, opcode):
        #0110 1110 1110 kkkk RAM[HL]¬RAM[HL]&k 2 2 - Z Z'
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._RAM[self._ram_bank + self._HL] &= k
        self._ZF = self._RAM[self._ram_bank + self._HL] == 0
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _subm_k(self, opcode):
        #0110 1110 1111 kkkk RAM[HL]¬k - RAM[HL] 2 2 - Z C
        k = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._RAM[self._ram_bank + self._HL] = (k - self._RAM[self._ram_bank + self._HL]) & 0xF
        self._ZF = self._RAM[self._ram_bank + self._HL] == 0
        self._SF = k >= self._RAM[self._ram_bank + self._HL]
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _io_p(self, opcode):
        #0110 1111
        id = (self._ROM.getByte((self._PC + 1) & 0x1FFF) >> 6) & 0x03
        return self._execute_io_p[id](self, opcode)

    def _ina_p(self, opcode):
        #0110 1111 0100 pppp Acc¬PORT[p] 2 2 - Z Z'
        p = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._ACC = self._io_tbl[p][0](self)
        self._ZF = self._ACC == 0
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 2) & 0x1FFF
        return 16
    
    def _inm_p(self, opcode):
        #0110 1111 1100 pppp RAM[HL]¬PORT[p] 2 2 - - Z'
        p = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x0F
        self._RAM[self._ram_bank + self._HL] = self._io_tbl[p][0](self)
        self._SF = self._RAM[self._ram_bank + self._HL] != 0
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _outa_p(self, opcode):
        #0110 1111 000p pppp PORT[p]¬Acc 2 2 - - 1
        p = self._ROM.getByte((self._PC + 1) & 0x1FFF) & 0x1F
        self._io_tbl[p][1](self, self._ACC)
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _outm_p(self, opcode):
        #0110 1111 100p pppp PORT[p]¬RAM[HL] 2 2 - - 1
        p = self._ROM.getByte(self._PC + 1) & 0x1F
        self._io_tbl[p][1](self, self._RAM[self._ram_bank + self._HL])
        self._SF = 1
        self._PC = (self._PC + 2) & 0x1FFF
        return 16

    def _adcam(self, opcode):
        #0111 0000 Acc¬Acc + RAM[HL] + CF 1 1 C Z C'
        self._ACC = (self._ACC + self._RAM[self._ram_bank + self._HL] + self._CF) & 0xF
        self._CF = self._ACC < (self._RAM[self._ram_bank + self._HL] + self._CF)
        self._ZF = self._ACC == 0
        self._SF = 1 - self._CF
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _addam(self, opcode):
        #0111 0001 Acc¬Acc + RAM[HL] 1 1 - Z C'
        self._ACC = (self._ACC + self._RAM[self._ram_bank + self._HL]) & 0xF
        self._ZF = self._ACC == 0
        self._SF = self._ACC >= self._RAM[self._ram_bank + self._HL]
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _sbcam(self, opcode):
        #0111 0010 Acc¬RAM[HLl - Acc - CF' 1 1 C Z C
        self._ACC = (self._RAM[self._ram_bank + self._HL] - self._ACC - (self._CF == 0)) & 0xF
        self._CF = self._RAM[self._ram_bank + self._HL] >= (self._ACC + (self._CF == 0))
        self._ZF = self._ACC == 0
        self._SF = self._CF
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
    
    def _cmpam(self, opcode):
        #0111 0011 RAM[HL] - Acc 1 1 C Z Z'
        self._CF = self._RAM[self._ram_bank + self._HL] >= self._ACC
        self._ZF = self._RAM[self._ram_bank + self._HL] == self._ACC
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _tla(self, opcode):
        #0111 0100 Acc¬LR 1 1 - Z 1
        self._ACC = self._HL & 0x0F
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
    
    def _exae(self, opcode):
        #0111 0101 MASK«Acc 1 1 - - 1
        acc_tmp = self._ACC
        self._ACC = self._IMASK
        self._IMASK = acc_tmp
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _tha(self, opcode):
        #0111 0110 Acc¬HR 1 1 - Z 1
        self._ACC = self._HL >> 4
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _oram(self, opcode):
        #0111 1000 Acc ¬Acc RAM[HL] 1 1 - Z Z'
        self._ACC |= self._RAM[self._ram_bank + self._HL]
        self._ZF = self._ACC == 0
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _xoram(self, opcode):
        #0111 1001 Acc¬Acc^RAM[HL] 1 1 - Z Z'
        self._ACC ^= self._RAM[self._ram_bank + self._HL]
        self._ZF = self._ACC == 0
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _andam(self, opcode):
        #0111 1011 Acc¬Acc & RAM[HL] 1 1 - Z Z'
        self._ACC &= self._RAM[self._ram_bank + self._HL]
        self._ZF = self._ACC == 0
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _decl(self, opcode):
        #0111 1100 LR¬LR-1 1 1 - Z C
        self._HL = (self._HL & 0xF0) | ((self._HL - 1) & 0x0F)
        self._ZF = (self._HL & 0x0F) == 0
        self._SF = (self._HL & 0x0F) != 15
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _stamd(self, opcode):
        #0111 1101 RAM[HL]¬Acc, LR-1 1 1 - Z C
        self._RAM[self._ram_bank + self._HL] = self._ACC
        self._HL = (self._HL & 0xF0) | ((self._HL - 1) & 0x0F)
        self._ZF = (self._HL & 0x0F) == 0
        self._SF = (self._HL & 0x0F) != 15
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _incl(self, opcode):
        #0111 1110 LR¬LR + 1 1 1 - Z C'
        self._HL = (self._HL & 0xF0) | ((self._HL + 1) & 0x0F)
        self._ZF = (self._HL & 0x0F) == 0
        self._SF = (self._HL & 0x0F) != 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _stami(self, opcode):
        #0111 1111 RAM[HL]¬Acc, LR+1 1 1 - Z C'
        self._RAM[self._ram_bank + self._HL] = self._ACC
        self._HL = (self._HL & 0xF0) | ((self._HL + 1) & 0x0F)
        self._ZF = (self._HL & 0x0F) == 0
        self._SF = (self._HL & 0x0F) != 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _ldl_k(self, opcode):
        #1000 kkkk LR¬k 1 1 - - 1
        k = opcode & 0x0F
        self._HL = (self._HL & 0xF0) | k
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _ldh_k(self, opcode):
        #1001 kkkk HR¬k 1 1 - - 1
        k = opcode & 0x0F
        self._HL = (self._HL & 0x0F) | (k << 4)
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _stdmi_k(self, opcode):
        #1010 kkkk RAM[HL]¬k, LR+1 1 1 - Z C'
        k = opcode & 0x0F
        self._RAM[self._ram_bank + self._HL] = k
        self._HL = (self._HL & 0xF0) | ((self._HL + 1) & 0x0F)
        self._ZF = (self._HL & 0x0F) == 0
        self._SF = (self._HL & 0x0F) != 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _cmpia_k(self, opcode):
        #1011 kkkk k - Acc 1 1 C Z Z'
        k = opcode & 0x0F
        self._CF = k >= self._ACC
        self._ZF = k == self._ACC
        self._SF = 1 - self._ZF
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _lbr_a(self, opcode):
        #1100 aaaa aaaa aaaa If SF= 1 then PC¬a else null 2 2 - - 1
        self._PC = (self._PC + 2) & 0x1FFF
        if (self._SF):
            a = ((opcode << 8) | self._ROM.getByte((self._PC - 1) & 0x1FFF)) & 0x0FFF
            self._PC = (self._PC & 0x1000) | a
        self._SF = 1
        return 16
    
    def _ldia_k(self, opcode):
        #1101 kkkk Acc¬k 1 1 - Z 1
        k = opcode & 0x0F
        self._ACC = k
        self._ZF = self._ACC == 0
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _scall_a(self, opcode):
        #1110 nnnn STACK[SP]¬PC, 1 2 - - - SP¬SP - 1, PC¬a, a = 8n + 6 (n =1~15),0086h (n = 0)
        pc = self._PC + 1
        sp = STACK_OFFSET + (self._SP << 2)
        self._RAM[sp] = pc >> 12
        self._RAM[sp + 1] = (pc >> 8) & 0xF
        self._RAM[sp + 2] = (pc >> 4) & 0xF
        self._RAM[sp + 3] = (pc) & 0xF
        self._SP = (self._SP - 1) & 0xF
        n = opcode & 0x0F
        self._PC = n * 8 + 6 + (0x80 * (n == 0))
        return 16
        
    def _clm_b(self, opcode):
        #1111 00bb RAM[HL]b¬0 1 1 - - 1
        b = opcode & 0x03
        self._RAM[self._ram_bank + self._HL] &= ~(0x1 << b)
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _sem_b(self, opcode):
        #1111 01bb RAM[HL]b¬1 1 1 - - 1
        b = opcode & 0x03
        self._RAM[self._ram_bank + self._HL] |= 0x1 << b
        self._SF = 1
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
    
    def _tfa_b(self, opcode):
        #1111 10bb SF¬Accb' 1 1 - - *
        b = opcode & 0x03
        self._SF = (self._ACC & (0x1 << b)) == 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _tfm_b(self, opcode):
        #1111 11bb SF¬RAM[HL]b' 1 1 - - *
        b = opcode & 0x03
        self._SF = (self._RAM[self._ram_bank + self._HL] & (0x1 << b)) == 0
        self._PC = (self._PC + 1) & 0x1FFF
        return 8
        
    def _dummy(self, opcode):
        self._PC = (self._PC + 1) & 0x1FFF
        return 8

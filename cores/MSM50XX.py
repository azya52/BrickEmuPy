from .rom import ROM
from .MSM50XXsound import MSM50XXsound

RAM_SIZE = 128
GRAM_SIZE = 32
FULL_GRAM = tuple([255] * GRAM_SIZE)

MCLOCK_DIV = 4

class MSM50XX():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = MSM50XXsound(mask, clock)

        self._format_tbl_offset = (self._ROM.size() // 2) - 64
        self._instr_counter = 0
        self._timer_counter32 = 0
        self._timer_counter16 = 0

        self._reset()

        self._execute = (
            MSM50XX._nop,                          #00 0000 0000 0000
            MSM50XX._dummy,
            MSM50XX._ror_a0,                       #00 0000 0010 AAAA
            MSM50XX._asr_a0,                       #00 0000 0011 AAAA
            MSM50XX._add_acc_a0,                   #00 0000 0100 AAAA
            MSM50XX._adc_acc_a0,                   #00 0000 0101 AAAA
            MSM50XX._bis_acc_a0,                   #00 0000 0110 AAAA
            MSM50XX._xor_acc_a0,                   #00 0000 0111 AAAA
            MSM50XX._dummy,
            MSM50XX._clc,                          #00 0000 1001 0000
            MSM50XX._clz,                          #00 0000 1010 0000
            MSM50XX._cla,                          #00 0000 1011 0000
            MSM50XX._dummy,
            MSM50XX._jmp_a0,                       #00 0000 1101 AAAA
            MSM50XX._bit_acc_a0,                   #00 0000 1110 AAAA
            *([MSM50XX._dummy] * 3),
            MSM50XX._ror_ap,                       #00 0001 0010 AAAA
            MSM50XX._asr_ap,                       #00 0001 0011 AAAA
            MSM50XX._add_acc_ap,                   #00 0001 0100 AAAA
            MSM50XX._adc_acc_ap,                   #00 0001 0101 AAAA
            MSM50XX._bis_acc_ap,                   #00 0001 0110 AAAA
            MSM50XX._xor_acc_ap,                   #00 0001 0111 AAAA
            *([MSM50XX._dummy] * 5),
            MSM50XX._jmp_ap,                       #00 0001 1101 AAAA
            MSM50XX._bit_acc_ap,                   #00 0001 1110 AAAA
            *([MSM50XX._dummy] * 4),
            MSM50XX._asl_a0,                       #00 0010 0011 AAAA
            MSM50XX._sub_acc_a0,                   #00 0010 0100 AAAA
            MSM50XX._sbc_acc_a0,                   #00 0010 0101 AAAA
            MSM50XX._bic_acc_a0,                   #00 0010 0110 AAAA
            *([MSM50XX._dummy] * 2),
            MSM50XX._sec,                          #00 0010 1001 0000
            MSM50XX._sez,                          #00 0010 1010 0000
            MSM50XX._sea,                          #00 0010 1011 0000
            MSM50XX._dummy,
            MSM50XX._jmpio_a0,                     #00 0010 1101 AAAA
            MSM50XX._cmp_acc_a0,                   #00 0010 1110 AAAA
            *([MSM50XX._dummy] * 4),
            MSM50XX._asl_ap,                       #00 0011 0011 AAAA
            MSM50XX._sub_acc_ap,                   #00 0011 0100 AAAA
            MSM50XX._sbc_acc_ap,                   #00 0011 0101 AAAA
            MSM50XX._bic_acc_ap,                   #00 0011 0110 AAAA
            *([MSM50XX._dummy] * 6),
            MSM50XX._jmpio_ap,                     #00 0011 1101 AAAA
            MSM50XX._cmp_acc_ap,                   #00 0011 1110 AAAA
            MSM50XX._dummy,
            MSM50XX._halt,                         #00 0100 0000 0000
            MSM50XX._lmp_bkp_on_off,               #00 0100 0001 BBLL
            MSM50XX._matrix_mn,                    #00 0100 0010 MMMM
            MSM50XX._format_n,                     #00 0100 0011 NNNN
            MSM50XX._int16,                        #00 0100 0100 00ED
            MSM50XX._page_n,                       #00 0100 0101 NNNN
            MSM50XX._adrs_n,                       #00 0100 0110 NNNN
            MSM50XX._dummy,
            MSM50XX._rstrate,                      #00 0100 1000 1000
            *([MSM50XX._dummy] * 2),
            MSM50XX._int32,                        #00 0100 1011 ED00
            MSM50XX._buzzer_freq_sound,            #00 0100 1100 BBBB
            MSM50XX._freq_n,                       #00 0100 1101 NNNN
            *([MSM50XX._dummy] * 18),
            *([MSM50XX._bcs_n] * 2),               #00 0110 000N NNNN
            *([MSM50XX._dummy] * 2),
            *([MSM50XX._bze_n] * 2),               #00 0110 010N NNNN
            *([MSM50XX._ble_n] * 2),               #00 0110 011N NNNN
            *([MSM50XX._bcc_n] * 2),               #00 0110 100N NNNN
            *([MSM50XX._dummy] * 2),
            *([MSM50XX._bnz_n] * 2),               #00 0110 110N NNNN
            *([MSM50XX._bgt_n] * 2),               #00 0110 111N NNNN
            *([MSM50XX._dummy] * 16),
            *([MSM50XX._dsp_digit_a0] * 16),       #00 1000 DDDD AAAA
            *([MSM50XX._dsp_digit_ap] * 16),       #00 1001 DDDD AAAA
            *([MSM50XX._dsp_digit_a0] * 16),       #00 1010 DDDD AAAA
            *([MSM50XX._dsp_digit_ap] * 16),       #00 1011 DDDD AAAA
            *([MSM50XX._dspf_digit_ap] * 64),      #00 11HP DDDD AAAA
            *([MSM50XX._bis_d_a0] * 16),           #01 0000 DDDD AAAA
            *([MSM50XX._bis_d_ap] * 16),           #01 0001 DDDD AAAA
            *([MSM50XX._bic_d_a0] * 16),           #01 0010 DDDD AAAA
            *([MSM50XX._bic_d_ap] * 16),           #01 0011 DDDD AAAA
            *([MSM50XX._bit_d_a0] * 16),           #01 0100 DDDD AAAA
            *([MSM50XX._bit_d_ap] * 16),           #01 0101 DDDD AAAA
            *([MSM50XX._cmp_d_a0] * 16),           #01 0110 DDDD AAAA
            *([MSM50XX._cmp_d_ap] * 16),           #01 0111 DDDD AAAA
            *([MSM50XX._add_d_a0] * 16),           #01 1000 DDDD AAAA
            *([MSM50XX._add_d_ap] * 16),           #01 1001 DDDD AAAA
            *([MSM50XX._sub_d_a0] * 16),           #01 1010 DDDD AAAA
            *([MSM50XX._sub_d_ap] * 16),           #01 1011 DDDD AAAA
            *([MSM50XX._mov_d_a0] * 16),           #01 1100 DDDD AAAA
            *([MSM50XX._mov_d_ap] * 16),           #01 1101 DDDD AAAA
            *([MSM50XX._xor_d_a0] * 16),           #01 1110 DDDD AAAA
            *([MSM50XX._xor_d_ap] * 16),           #01 1111 DDDD AAAA
            *([MSM50XX._jmp_adrs] * 256),          #10 AAAA AAAA AAAA
            *([MSM50XX._adjust_n_a0] * 16),        #11 0000 NNNN AAAA
            *([MSM50XX._adjust_n_ap] * 16),        #11 0001 NNNN AAAA
            *([MSM50XX._dummy] * 33),
            MSM50XX._switch_a0,                    #11 0100 0001 AAAA
            MSM50XX._kswitch_a0,                   #11 0100 0010 AAAA
            MSM50XX._dummy,
            MSM50XX._intmode_a0,                   #11 0100 0100 AAAA
            *([MSM50XX._dummy] * 4),
            MSM50XX._rate_a0,                      #11 0100 1001 AAAA
            *([MSM50XX._dummy] * 7),
            MSM50XX._switch_ap,                    #11 0101 0001 AAAA
            MSM50XX._kswitch_ap,                   #11 0101 0010 AAAA
            MSM50XX._dummy,
            MSM50XX._intmode_ap,                   #11 0101 0100 AAAA
            *([MSM50XX._dummy] * 4),
            MSM50XX._rate_ap,                      #11 0101 1001 AAAA
            *([MSM50XX._dummy] * 8),
            MSM50XX._matrix_a0,                    #11 0110 0010 AAAA
            MSM50XX._format_a0,                    #11 0110 0011 AAAA
            MSM50XX._dummy,
            MSM50XX._page_a0,                      #11 0110 0101 AAAA
            MSM50XX._adrs_a0,                      #11 0110 0110 AAAA
            *([MSM50XX._dummy] * 11),
            MSM50XX._matrix_ap,                    #11 0111 0010 AAAA
            MSM50XX._format_ap,                    #11 0111 0011 AAAA
            *([MSM50XX._dummy] * 2),
            MSM50XX._adrs_ap,                      #11 0111 0110 AAAA
            *([MSM50XX._dummy] * 9),
            *([MSM50XX._chg_ax] * 8),              #11 1000 0XXX AAAA
            *([MSM50XX._dummy] * 8),
            MSM50XX._chg_ap,                       #11 1001 0000 AAAA
            *([MSM50XX._dummy] * 47),
            *([MSM50XX._mov_acc_ax] * 8),          #11 1100 0XXX AAAA
            *([MSM50XX._dummy] * 8),
            MSM50XX._mov_acc_ap,                   #11 1101 0000 AAAA
            *([MSM50XX._dummy] * 15),
            *([MSM50XX._mov_ax_acc] * 8),          #11 1110 0XXX AAAA
            *([MSM50XX._dummy] * 8),
            MSM50XX._mov_ap_acc,                   #11 1111 0000 AAAA
            *([MSM50XX._dummy] * 15)
        )

    def _reset(self):
        self._ACC = 0
        self._PC = 0

        self._CF = 0
        self._ZF = 0
        
        self._HALT = 0

        self._TC = 0
        self._INT16 = 0
        self._INT32 = 0
        self._INT = 0

        self._PM = 0
        self._PS = 0
        self._PK = 0
        self._LD = 0

        self._FMT = 0
        self._BACKUP = 0
        self._PAGE = 0
        self._AREG = 0xF

        self._RAM = [0] * RAM_SIZE
        self._GRAM = [0] * GRAM_SIZE

    def reset(self):
        self._reset()

    def examine(self):
        return {
            "ACC": self._ACC,
            "PC": self._PC & 0xFFF,
            "PAGE": self._PAGE,
            "CF": self._CF,
            "ZF": self._ZF,
            "HALT": self._HALT,
            "FMT": self._FMT,
            "TC": self._TC,
            "PM": self._PM,
            "PS": self._PS,
            "PK": self._PK,
            "LD": self._LD,
            "RAM": tuple(self._RAM),
            "GRAM": tuple(self._GRAM),
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] & 0xFFF
        if ("ACC" in state):
            self._ACC = state["ACC"] & 0xF
        if ("CF" in state):
            self._CF = state["CF"] & 0x1
        if ("ZF" in state):
            self._ZF = state["ZF"] & 0x1
        if ("PAGE" in state):
            self._PAGE = state["PAGE"] & 0xF
        if ("HALT" in state):
            self._HALT = state["HALT"] & 0x1
        if ("FMT" in state):
            self._FMT = state["FMT"] & 0xF
        if ("TC" in state):
            self._TC = state["TC"] & 0xF
        if ("PM" in state):
            self._PM = state["PM"] & 0xF
        if ("PS" in state):
            self._PS = state["PS"] & 0xF
        if ("PK" in state):
            self._PK = state["PK"] & 0xF
        if ("LD" in state):
            self._LD = state["LD"] & 0xF
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xF
        if ("GRAM" in state):
            for i, value in state["GRAM"].items():
                self._GRAM[i] = value & 0xF
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
    
    def pin_set(self, port, pin, level):
        if (port == 'PS'):
            self._PS = ~(1 << pin) & self._PS | level << pin
            self._HALT = 0
        elif (port == 'PK'):
            self._PK = ~(1 << pin) & self._PK | level << pin
            self._HALT = 0
        elif (port == 'RES'):
            self._reset()
            self._HALT = 1

    def pin_release(self, port, pin):
        if (port == 'PS'):
            self._PS &= ~(1 << pin)
            self._HALT = 0
        elif (port == 'PK'):
            self._PK &= ~(1 << pin)
            self._HALT = 0
        elif (port == 'RES'):
            self._HALT = 0

    def pc(self):
        return self._PC & 0xFFF
    
    def get_VRAM(self):
        if (self._GRAM[15] == 1):
            return FULL_GRAM
        return tuple(self._GRAM)
    
    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter
            
    def clock(self):
        if (not self._HALT):
            opcode = self._ROM.getWord(self._PC << 1)
            self._PC += 1
            self._execute[opcode >> 4](self, opcode)
            self._instr_counter += 1

        if (self._INT16):
            self._timer_counter16 -= MCLOCK_DIV
            if (self._timer_counter16 <= 0):
                self._timer_counter16 += 2048
                self._TC = (self._TC + 1) & 0xF
                if (self._TC == 0):
                    self._INT |= 0x8
                self._HALT = 0

        if (self._INT32):
            self._timer_counter32 -= MCLOCK_DIV
            if (self._timer_counter32 <= 0):
                self._timer_counter32 += 1024
                self._TC = (self._TC + 1) & 0xF
                if (self._TC == 0):
                    self._INT |= 0x8
                self._HALT = 0

        self._sound.clock(MCLOCK_DIV)
        return MCLOCK_DIV

    def _get_ap(self, opcode):
        a = opcode & 0xF
        return (self._PAGE << 4) | (self._AREG if (a == 0xF) else a)
    
    def _nop(self, opcode):
        #00 0000 0000 0000
        return

    def _ror_a0(self, opcode):
        #00 0000 0010 AAAA
        a = opcode & 0xF
        cfb = self._RAM[a] & 0x1
        self._ACC = self._RAM[a] = (self._CF << 3) | (self._RAM[a] >> 1)
        self._CF = cfb
        self._ZF = not self._ACC

    def _asr_a0(self, opcode):
        #00 0000 0011 AAAA
        a = opcode & 0xF
        self._CF = self._RAM[a] & 0x1
        self._ACC = self._RAM[a] = self._RAM[a] >> 1
        self._ZF = not self._ACC

    def _add_acc_a0(self, opcode):
        #00 0000 0100 AAAA
        a = opcode & 0xF
        res = self._RAM[a] + self._ACC
        self._ACC = self._RAM[a] = res & 0xF
        self._CF = res > 15
        self._ZF = not self._ACC

    def _adc_acc_a0(self, opcode):
        #00 0000 0101 AAAA
        a = opcode & 0xF
        res = self._RAM[a] + self._ACC + self._CF
        self._ACC = self._RAM[a] = res % 10
        self._CF = res >= 10
        self._ZF = not self._ACC

    def _bis_acc_a0(self, opcode):
        #00 0000 0110 AAAA
        a = opcode & 0xF
        self._ACC = self._RAM[a] = self._RAM[a] | self._ACC
        self._ZF = not self._ACC

    def _xor_acc_a0(self, opcode):
        #00 0000 0111 AAAA
        a = opcode & 0xF
        self._ACC = self._RAM[a] = self._RAM[a] ^ self._ACC
        self._ZF = not self._ACC

    def _clc(self, opcode):
        #00 0000 1001 0000
        self._CF = 0

    def _clz(self, opcode):
        #00 0000 1010 0000
        self._ZF = 0

    def _cla(self, opcode):
        #00 0000 1011 0000
        self._CF = self._ZF = 0

    def _jmp_a0(self, opcode):
        #00 0000 1101 AAAA
        self._PC += self._RAM[opcode & 0xF]

    def _bit_acc_a0(self, opcode):
        #00 0000 1110 AAAA
        a = opcode & 0xF
        self._ZF = (~self._RAM[a] & self._ACC) > 0

    def _ror_ap(self, opcode):
        #00 0001 0010 AAAA
        a = self._get_ap(opcode)
        cfb = self._RAM[a] & 0x1
        self._ACC = self._RAM[a] = (self._CF << 3) | (self._RAM[a] >> 1)
        self._CF = cfb
        self._ZF = not self._ACC

    def _asr_ap(self, opcode):
        #00 0001 0011 AAAA
        a = self._get_ap(opcode)
        self._CF = self._RAM[a] & 0x1
        self._ACC = self._RAM[a] = self._RAM[a] >> 1
        self._ZF = not self._ACC

    def _add_acc_ap(self, opcode):
        #00 0001 0100 AAAA
        a = self._get_ap(opcode)
        res = self._RAM[a] + self._ACC
        self._ACC = self._RAM[a] = res & 0xF
        self._CF = res > 15
        self._ZF = not self._ACC

    def _adc_acc_ap(self, opcode):
        #00 0001 0101 AAAA
        a = self._get_ap(opcode)
        res = self._RAM[a] + self._ACC + self._CF
        self._ACC = self._RAM[a] = res % 10
        self._CF = res >= 10
        self._ZF = not self._ACC

    def _bis_acc_ap(self, opcode):
        #00 0001 0110 AAAA
        a = self._get_ap(opcode)
        self._ACC = self._RAM[a] = self._RAM[a] | self._ACC
        self._ZF = not self._ACC

    def _xor_acc_ap(self, opcode):
        #00 0001 0111 AAAA
        a = self._get_ap(opcode)
        self._ACC = self._RAM[a] = self._RAM[a] ^ self._ACC
        self._ZF = not self._ACC

    def _jmp_ap(self, opcode):
        #00 0001 1101 AAAA
        self._PC += self._RAM[self._get_ap(opcode)]

    def _bit_acc_ap(self, opcode):
        #00 0001 1110 AAAA
        a = self._get_ap(opcode)
        self._ZF = (~self._RAM[a] & self._ACC) > 0

    def _asl_a0(self, opcode):
        #00 0010 0011 AAAA
        a = opcode & 0xF
        self._CF = (self._RAM[a] > 7)
        self._ACC = self._RAM[a] = (self._RAM[a] << 1) & 0xF
        self._ZF = not self._ACC

    def _sub_acc_a0(self, opcode):
        #00 0010 0100 AAAA
        a = (opcode & 0xF)
        self._CF = self._RAM[a] < self._ACC
        self._ACC = self._RAM[a] = (self._RAM[a] - self._ACC) & 0xF
        self._ZF = not self._ACC

    def _sbc_acc_a0(self, opcode):
        #00 0010 0101 AAAA
        a = (opcode & 0xF)
        res = self._RAM[a] - self._ACC - self._CF
        self._CF = res < 0
        self._ACC = self._RAM[a] = res % 10
        self._ZF = not self._ACC

    def _bic_acc_a0(self, opcode):
        #00 0010 0110 AAAA
        a = (opcode & 0xF)
        self._ACC = self._RAM[a] = self._RAM[a] & (~self._ACC)
        self._ZF = not self._ACC

    def _sec(self, opcode):
        #00 0010 1001 0000
        self._CF = 1

    def _sez(self, opcode):
        #00 0010 1010 0000
        self._ZF = 1

    def _sea(self, opcode):
        #00 0010 1011 0000
        self._CF = self._ZF = 1

    def _jmpio_a0(self, opcode):
        #00 0010 1101 AAAA
        self._PC += self._RAM[opcode & 0xF] & 0x7

    def _cmp_acc_a0(self, opcode):
        #00 0010 1110 AAAA
        self._ZF = self._RAM[opcode & 0xF] == self._ACC

    def _asl_ap(self, opcode):
        #00 0011 0011 AAAA
        a = self._get_ap(opcode)
        self._CF = (self._RAM[a] > 7)
        self._ACC = self._RAM[a] = (self._RAM[a] << 1) & 0xF
        self._ZF = not self._ACC

    def _sub_acc_ap(self, opcode):
        #00 0011 0100 AAAA
        a = self._get_ap(opcode)
        self._CF = self._RAM[a] < self._ACC
        self._ACC = self._RAM[a] = (self._RAM[a] - self._ACC) & 0xF
        self._ZF = not self._ACC

    def _sbc_acc_ap(self, opcode):
        #00 0011 0101 AAAA
        a = self._get_ap(opcode)
        res = self._RAM[a] - self._ACC - self._CF
        self._CF = res < 0
        self._ACC = self._RAM[a] = res % 10
        self._ZF = not self._ACC

    def _bic_acc_ap(self, opcode):
        #00 0011 0110 AAAA
        a = self._get_ap(opcode)
        self._ACC = self._RAM[a] = self._RAM[a] & (~self._ACC)
        self._ZF = not self._RAM[a]

    def _jmpio_ap(self, opcode):
        #00 0011 1101 AAAA
        self._PC += self._RAM[self._get_ap(opcode)] & 0x7

    def _cmp_acc_ap(self, opcode):
        #00 0011 1110 AAAA
        self._ZF = self._RAM[self._get_ap(opcode)] == self._ACC

    def _halt(self, opcode):
        #00 0100 0000 0000
        self._HALT = 1

    def _lmp_bkp_on_off(self, opcode):
        #00 0100 0001 BBLL
        if (opcode & 0x2):
            self._LD = 1
        elif (opcode & 0x1):
            self._LD = 0

        if (opcode & 0x8):
            self._BACKUP = 1
        elif (opcode & 0x4):
            self._BACKUP = 0

    def _matrix_mn(self, opcode):
        #00 0100 0010 MMMM
        self._PM = opcode & 0xF

    def _format_n(self, opcode):
        #00 0100 0011 NNNN
        self._FMT = opcode & 0xF

    def _int16(self, opcode):
        #00 0100 0100 00ED
        self._INT16 = (opcode & 0x2) > 0

    def _page_n(self, opcode):
        #00 0100 0101 NNNN
        self._PAGE = opcode & 0xF

    def _adrs_n(self, opcode):
        #00 0100 0110 NNNN
        self._AREG = opcode & 0xF

    def _rstrate(self, opcode):
        #00 0100 1000 1000
        self._TC = 0

    def _int32(self, opcode):
        #00 0100 1011 ED00
        self._INT32 = (opcode & 0x8) > 0

    def _buzzer_freq_sound(self, opcode):
        #00 0100 1100 BBBB
        #print(self._instr_counter, "_buzzer_freq_sound", (opcode & 0xC) >> 2, opcode & 0x3)
        self._sound.set_sound(opcode & 0xF)

    def _freq_n(self, opcode):
        #00 0100 1101 NNNN
        #print(self._instr_counter, "_freq_n", opcode & 0xF)
        self._sound.set_freq(opcode & 0xF)

    def _bcs_n(self, opcode):
        #00 0110 000N NNNN
        if (self._CF):
            self._PC += (opcode & 0x1F)

    def _bze_n(self, opcode):
        #00 0110 010N NNNN
        if (self._ZF):
            self._PC += (opcode & 0x1F)

    def _ble_n(self, opcode):
        #00 0110 011N NNNN
        if (self._ZF | self._CF):
            self._PC += (opcode & 0x1F)

    def _bcc_n(self, opcode):
        #00 0110 100N NNNN
        if (not self._CF):
            self._PC += (opcode & 0x1F)

    def _bnz_n(self, opcode):
        #00 0110 110N NNNN
        if (not self._ZF):
            self._PC += (opcode & 0x1F)

    def _bgt_n(self, opcode):
        #00 0110 111N NNNN
        if (not (self._ZF | self._CF)):
            self._PC += (opcode & 0x1F)

    def _dsp_digit_a0(self, opcode):
        #00 1000 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 5 & 0x10) | ((opcode >> 4) & 0xF)
        self._GRAM[d] = (self._RAM[a] << 4) | self._ACC

    def _dsp_digit_ap(self, opcode):
        #00 1001 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 5 & 0x10) | ((opcode >> 4) & 0xF)
        self._GRAM[d] = (self._RAM[a] << 4) | self._ACC

    def _dspf_digit_ap(self, opcode):
        #00 110P DDDD AAAA
        a = (opcode & 0xF)
        if (opcode & 0x0100):
            a = self._get_ap(opcode)
        d = (opcode >> 5 & 0x10) | ((opcode >> 4) & 0xF)
        offset = self._format_tbl_offset + (((self._FMT & 0x6) << 3) | self._RAM[a])
        word = self._ROM.getWord(offset * 2)
        if (self._FMT & 0x1):
            word >>= 7
        self._GRAM[d] = (word << 1) & 0xFE

    def _bis_d_a0(self, opcode):
        #01 0000 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = self._RAM[a] | d
        self._ZF = not self._ACC

    def _bis_d_ap(self, opcode):
        #01 0001 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = self._RAM[a] | d
        self._ZF = not self._ACC

    def _bic_d_a0(self, opcode):
        #01 0010 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = self._RAM[a] & ~d
        self._ZF = not self._ACC

    def _bic_d_ap(self, opcode):
        #01 0011 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = self._RAM[a] & ~d
        self._ZF = not self._ACC

    def _bit_d_a0(self, opcode):
        #01 0100 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 4) & 0xF
        self._ZF = (~self._RAM[a] & d) > 0

    def _bit_d_ap(self, opcode):
        #01 0101 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 4) & 0xF
        self._ZF = (~self._RAM[a] & d) > 0

    def _cmp_d_a0(self, opcode):
        #01 0110 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 4) & 0xF
        self._ZF = self._RAM[a] == d

    def _cmp_d_ap(self, opcode):
        #01 0111 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 4) & 0xF
        self._ZF = self._RAM[a] == d

    def _add_d_a0(self, opcode):
        #01 1000 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = (self._RAM[a] + d) & 0xF
        self._CF = self._ACC < d
        self._ZF = not self._ACC

    def _add_d_ap(self, opcode):
        #01 1001 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = (self._RAM[a] + d) & 0xF
        self._CF = self._ACC < d
        self._ZF = not self._ACC

    def _sub_d_a0(self, opcode):
        #01 1010 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 4) & 0xF
        self._CF = self._RAM[a] < d
        self._ACC = self._RAM[a] = (self._RAM[a] - d) & 0xF
        self._ZF = not self._ACC

    def _sub_d_ap(self, opcode):
        #01 1011 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 4) & 0xF
        self._CF = self._RAM[a] < d
        self._ACC = self._RAM[a] = (self._RAM[a] - d) & 0xF
        self._ZF = not self._ACC

    def _mov_d_a0(self, opcode):
        #01 1100 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = d
        self._ZF = not d

    def _mov_d_ap(self, opcode):
        #01 1101 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = d
        self._ZF = not d

    def _xor_d_a0(self, opcode):
        #01 1110 DDDD AAAA
        a = opcode & 0xF
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = self._RAM[a] ^ d
        self._ZF = not self._ACC

    def _xor_d_ap(self, opcode):
        #01 1111 DDDD AAAA
        a = self._get_ap(opcode)
        d = (opcode >> 4) & 0xF
        self._ACC = self._RAM[a] = self._RAM[a] ^ d
        self._ZF = not self._ACC

    def _jmp_adrs(self, opcode):
        #10 0AAA AAAA AAAA
        self._PC = opcode & 0x7FF

    def _adjust_n_a0(self, opcode):
        #11 0000 NNNN AAAA
        a = opcode & 0xF
        value = self._RAM[a]
        mod = ~((opcode >> 4) - 1) & 0xF
        self._ACC = self._RAM[a] = value % mod
        self._CF = value >= mod
        self._ZF = not self._ACC

    def _adjust_n_ap(self, opcode):
        #11 0001 NNNN AAAA
        a = self._get_ap(opcode)
        value = self._RAM[a]
        mod = ~((opcode >> 4) - 1) & 0xF
        self._ACC = self._RAM[a] = value % mod
        self._CF = value >= mod
        self._ZF = not self._ACC

    def _switch_a0(self, opcode):
        #11 0100 0001 AAAA
        self._ACC = self._RAM[opcode & 0xF] = self._PS

    def _kswitch_a0(self, opcode):
        #11 0100 0010 AAAA
        self._ACC = self._RAM[opcode & 0xF] = self._PK

    def _intmode_a0(self, opcode):
        #11 0100 0100 AAAA
        self._ACC = self._RAM[opcode & 0xF] = self._INT
        self._INT = 0 #?
        self._ZF = not self._ACC

    def _rate_a0(self, opcode):
        #11 0100 1001 AAAA
        self._ACC = self._RAM[opcode & 0xF] = self._TC
        self._ZF = not self._ACC

    def _switch_ap(self, opcode):
        #11 0101 0001 AAAA
        self._ACC = self._RAM[self._get_ap(opcode)] = self._PS
        self._ZF = not self._ACC

    def _kswitch_ap(self, opcode):
        #11 0101 0010 AAAA
        self._ACC = self._RAM[self._get_ap(opcode)] = self._PK
        self._ZF = not self._ACC

    def _intmode_ap(self, opcode):
        #11 0101 0100 AAAA
        self._ACC = self._RAM[self._get_ap(opcode)] = self._INT
        self._INT = 0 #?
        self._ZF = not self._ACC

    def _rate_ap(self, opcode):
        #11 0101 1001 AAAA
        self._ACC = self._RAM[self._get_ap(opcode)] = self._TC
        self._ZF = not self._ACC

    def _matrix_a0(self, opcode):
        #11 0110 0010 AAAA
        self._PM = self._RAM[opcode & 0xF]

    def _format_a0(self, opcode):
        #11 0110 0011 AAAA
        self._FMT = self._RAM[opcode & 0xF] 

    def _page_a0(self, opcode):
        #11 0110 0101 AAAA
        self._PAGE = self._RAM[opcode & 0xF]

    def _adrs_a0(self, opcode):
        #11 0110 0110 AAAA
        self._AREG = self._RAM[opcode & 0xF]

    def _matrix_ap(self, opcode):
        #11 0111 0010 AAAA
        self._PM = self._RAM[self._get_ap(opcode)]

    def _format_ap(self, opcode):
        #11 0111 0011 AAAA
        self._FMT = self._RAM[self._get_ap(opcode)] 

    def _adrs_ap(self, opcode):
        #11 0111 0110 AAAA
        self._AREG = self._RAM[self._get_ap(opcode)] 

    def _chg_ax(self, opcode):
        #11 1000 0XXX AAAA
        a = opcode & 0x7F
        b = self._ACC
        self._ACC = self._RAM[a]
        self._RAM[a] = self._ACC

    def _chg_ap(self, opcode):
        #11 1001 0000 AAAA
        a = self._get_ap(opcode)
        b = self._ACC
        self._ACC = self._RAM[a]
        self._RAM[a] = self._ACC

    def _mov_acc_ax(self, opcode):
        #11 1100 0XXX AAAA
        self._RAM[opcode & 0x7F] = self._ACC

    def _mov_acc_ap(self, opcode):
        #11 1101 0000 AAAA
        self._RAM[self._get_ap(opcode)] = self._ACC

    def _mov_ax_acc(self, opcode):
        #11 1110 0XXX AAAA
        self._ACC = self._RAM[opcode & 0x7F]
        self._ZF = not self._ACC

    def _mov_ap_acc(self, opcode):
        #11 1111 0000 AAAA
        self._ACC = self._RAM[self._get_ap(opcode)]
        self._ZF = not self._ACC

    def _dummy(self, opcode):
        #11 1111 0000 AAAA
        print("undefined instruction", "%0.3X" % self._PC)
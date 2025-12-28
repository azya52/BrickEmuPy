from .rom import ROM
from .LC5732sound import LC5732sound

RAM_SIZE = 48
LCDRAM_SIZE = 16

MCLOCK_DIV = 4
MCLOCKx2_DIV = MCLOCK_DIV * 2

STS_SCF0_PREDIV_OVFW = 0x01
STS_SCF1_PREDIV = 0x02
STS_SCF2_PS = 0x04
STS_SCF3_PM = 0x08
STS_SCF4_CHRONO = 0x10

HEF_0_PREDIV_OVFW = 0x01
HEF_1_PREDIV = 0x02
HEF_2_PS = 0x04
HEF_3_PM = 0x08
HEF_4_CHRONO = 0x10

PDF_PS = 0x1
PDF_PM = 0x2

class LC5732():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = LC5732sound(mask, clock)

        self._instr_counter = 0
        self._cycle_counter = 0
        
        self._500ms_div = clock / 2
        self._100ms_div = clock / 10
        self._32ms_div = clock / (1000 / 32)

        self._reset()

        self._execute = (
            LC5732._halt,                   #00000000           1 1
            LC5732._taat,                   #00000001           1 2   (AC, TREG) <- ROM(PGX, AC, M(DP))
            LC5732._twrt,                   #00000010           1 2   PORT <- ROM(PGX, AC, M(DP))
            LC5732._tmel,                   #00000011           1 2   ALM <- ROM(PGX, AC, M(DP))
            LC5732._csp,                    #00000100           1 1   CSTF <- 0; CSTF
            LC5732._cst,                    #00000101           1 1   CSTF <- 1; CSTF
            LC5732._rc5,                    #00000110           1 1   HEF0 <- 0; HEF0
            LC5732._sc5,                    #00000111           1 1   HEF0 <- 1; HEF0
            *([LC5732._jmp_x] * 8),         #00001XXX XXXXXXXX  2 2   PC <- X
            LC5732._jmp_p,                  #00010000           1 1   PC <- (PAGE, AC, M(DP))
            LC5732._page,                   #00010001           1 1   page <- [M(DP)]
            LC5732._mtr,                    #00010010           1 1   M(DP) <- TREG
            LC5732._rts,                    #00010011           1 1   PC <- (STACK)
            LC5732._mpcl,                   #00010100           1 1   M(DP) <- PC3-0
            LC5732._mpcm,                   #00010101           1 1   M(DP) <- PC7-4
            LC5732._mpch,                   #00010110           1 1   M(DP) <- PC10-8
            LC5732._in,                     #00010111           1 1   AC <- (PORT)
            LC5732._asr0,                   #00011000           1 1   ACn <- ACn+1; AC3 <- 0
            LC5732._asr1,                   #00011001           1 1   ACn <- ACn+1; AC3 <- 1
            LC5732._asl0,                   #00011010           1 1   ACn <- ACn-1; AC0 <- 0
            LC5732._asl1,                   #00011011           1 1   ACn <- ACn-1; AC0 <- 1
            LC5732._sdpl,                   #00011100           1 1   DPL <- (AC)
            LC5732._sdph,                   #00011101           1 1   DPH <- (AC)
            LC5732._edpl,                   #00011110           1 1   (DPL) <-> (EDPL)
            LC5732._edph,                   #00011111           1 1   (DPH) <-> (EDPH)
            *([LC5732._mvi_x] * 16),        #0010XXXX           1 1   M(DP) <- X
            *([LC5732._ldi_x] * 16),        #0011XXXX           1 1   AC <- X
            *([LC5732._baz_x] * 8),         #01000XXX XXXXXXXX  2 2   PC <- X if AC == 0
            *([LC5732._bab0_x] * 8),        #01001XXX XXXXXXXX  2 2   PC <- X if AC0
            *([LC5732._banz_x] * 8),        #01010XXX XXXXXXXX  2 2   PC <- X if AC != 0
            *([LC5732._bab1_x] * 8),        #01011XXX XXXXXXXX  2 2   PC <- X if AC1
            *([LC5732._bcnh_x] * 8),        #01100XXX XXXXXXXX  2 2   PC <- X if CF == 0
            *([LC5732._bab2_x] * 8),        #01101XXX XXXXXXXX  2 2   PC <- X if AC2
            *([LC5732._bch_x] * 8),         #01110XXX XXXXXXXX  2 2   PC <- X if CF != 0
            *([LC5732._bab3_x] * 8),        #01111XXX XXXXXXXX  2 2   PC <- X if AC3
            LC5732._adc,                    #10000000           1 1   AC <- (AC) + [M(DP)] + (CF); CF
            LC5732._sbc,                    #10000001           1 1   AC <- (AC) + ~[M(DP)] + (CF); CF
            LC5732._add,                    #10000010           1 1   AC <- (AC) + [M(DP)]; CF
            LC5732._sub,                    #10000011           1 1   AC <- (AC) + ~[M(DP)] + 1; CF
            LC5732._adn,                    #10000100           1 1   AC <- (AC) + [M(DP)]
            LC5732._and,                    #10000101           1 1   AC <- (AC) and [M(DP)]
            LC5732._eor,                    #10000110           1 1   AC <- (AC) xor [M(DP)]
            LC5732._or,                     #10000111           1 1   AC <- (AC) or [M(DP)]
            LC5732._adc_m,                  #10001000           1 1   AC, M(DP) <- (AC) + [M(DP)] + (CF); CF
            LC5732._sbc_m,                  #10001001           1 1   AC, M(DP) <- (AC) + ~[M(DP)] + (CF); CF
            LC5732._add_m,                  #10001010           1 1   AC, M(DP) <- (AC) + [M(DP)]; CF
            LC5732._sub_m,                  #10001011           1 1   AC, M(DP) <- (AC) + ~[M(DP)] + 1; CF
            LC5732._adn_m,                  #10001100           1 1   AC, M(DP) <- (AC) + [M(DP)]
            LC5732._and_m,                  #10001101           1 1   AC, M(DP) <- (AC) and [M(DP)]
            LC5732._eor_m,                  #10001110           1 1   AC, M(DP) <- (AC) xor [M(DP)]
            LC5732._or_m,                   #10001111           1 1   AC, M(DP) <- (AC) or [M(DP)]
            LC5732._adci,                   #10010000 ----XXXX  2 2   AC <- (AC) + X + (CF); CF
            LC5732._sbci,                   #10010001 ----XXXX  2 2   AC <- (AC) + ~X + (CF); CF
            LC5732._addi,                   #10010010 ----XXXX  2 2   AC <- (AC) + X; CF
            LC5732._subi,                   #10010011 ----XXXX  2 2   AC <- (AC) + ~X + 1; CF
            LC5732._adni,                   #10010100 ----XXXX  2 2   AC <- (AC) + X
            LC5732._andi,                   #10010101 ----XXXX  2 2   AC <- (AC) and X
            LC5732._eori,                   #10010110 ----XXXX  2 2   AC <- (AC) xor X
            LC5732._ori,                    #10010111 ----XXXX  2 2   AC <- (AC) or X
            LC5732._inc,                    #10011000           1 1   M(DP), AC <- M(DP) + 1
            LC5732._dec,                    #10011001           1 1   M(DP), AC <- M(DP) - 1
            LC5732._idpl,                   #10011010           1 1   DPL <- (DPL) + 1
            LC5732._ddpl,                   #10011011           1 1   DPL <- (DPL) - 1
            LC5732._idph,                   #10011100           1 1   DPH <- (DPH) + 1
            LC5732._ddph,                   #10011101           1 1   DPH <- (DPH) - 1
            LC5732._isp,                    #10011110           1 1   SP <- (SP) + 1
            LC5732._dsp,                    #10011111           1 1   SP <- (SP) - 1
            *([LC5732._jsr_x] * 8),         #10100XXX XXXXXXXX  2 2   STACK <- PC + 2; PC <- X
            LC5732._ipm,                    #10101000           1 1   AC <- [P(M)]
            LC5732._lda,                    #10101001           1 1   AC <- [M(DP)]
            LC5732._lsp,                    #10101010           1 1   AC <- (SP)
            LC5732._lhlt,                   #10101011           1 1   AC <- (STS2); STS2 <- 0; SCF1-4
            LC5732._l500,                   #10101100           1 1   AC <- (STS1); SCF0 <- 0; SCF0
            LC5732._sta,                    #10101101           1 1   M(DP) <- (AC)           
            LC5732._ssp,                    #10101110           1 1   SP <- (AC)
            LC5732._ips,                    #10101111           1 1   AC <- [P(S)]           
            *([LC5732._mdpl_x] * 16),       #1011XXXX           1 1   DPL <- X
            *([LC5732._mdph_x] * 16),       #1100XXXX           1 1   DPH <- X
            *([LC5732._sic_x] * 16),        #1101XXXX           1 1   HEFn+1 = Xn; HEF1-4
            *([LC5732._msp_x] * 16),        #1110XXXX           1 1   SP <- X
            LC5732._rcf,                    #11110000           1 1   CF <- 0; CF
            LC5732._scf,                    #11110001           1 1   CF <- 1; CF
            LC5732._rlgt,                   #11110010           1 1   LIGHT <- 0
            LC5732._slgt,                   #11110011           1 1   LIGHT <- 1
            *([LC5732._spdr_x] * 4),        #111101XX           1 1   PDF <- X; PDF
            LC5732._rbak,                   #11111000           1 1   BCF <- 0
            LC5732._sbak,                   #11111001           1 1   BCF <- 1
            LC5732._sas_x,                  #11111010 XXXXXXXX  2 2   ALM <- X
            #LC5732._ras,                   #11111010 11111111  2 2
            LC5732._csec,                   #11111011           1 1   PREDIV15-11 <- 0; SCF0,1,4 <- 0; SCF0,1,4 
            LC5732._out,                    #11111100           1 1   PORT <- (AC, M(DP))
            LC5732._ldpl,                   #11111101           1 1   AC <- (DPL)
            LC5732._ldph,                   #11111110           1 1   AC <- (DPH)
            LC5732._nop,                    #11111111           1 1
        )

    def _reset(self):
        self._AC = 0
        self._DP = 0
        self._EDP = 0
        self._SP = 0
        self._PC = 0

        self._CF = 0
        
        self._STACK = 0
        self._TREG = 0
        self._PAGE = 0

        self._HALT = 0

        self._ALM = 0xFF
        self._CSTF = 0
        self._HEF = HEF_0_PREDIV_OVFW
        self._STS = 0

        self._PS = 0
        self._PM = 0
        self._LIGHT = 0
        self._PDF = 0

        self._RAM = [0] * RAM_SIZE
        self._LCDRAM = [0xFF] * LCDRAM_SIZE

        self._sound.set_alm(self._ALM, self._cycle_counter)

    def reset(self):
        self._reset()

    def examine(self):
        return {
            "PC": self._PC & 0x7FF,
            "AC": self._AC,
            "DP": self._DP,
            "EDP": self._EDP,
            "SP": self._SP,
            "TREG": self._TREG,
            "STACK": self._STACK,
            "PAGE": self._PAGE,
            "HEF": self._HEF,
            "STS": self._STS,
            "ALM": self._ALM,
            "CF": self._CF,
            "CSTF": self._CSTF,
            "HALT": self._HALT,
            "PS": self._PS,
            "PM": self._PM,
            "LGT": self._LIGHT,
            "PDF": self._PDF,
            "RAM": tuple(self._RAM),
            "LCDRAM": tuple(self._LCDRAM),
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] & 0x7FF
        if ("AC" in state):
            self._AC = state["AC"]
        if ("DP" in state):
            self._DP = state["DP"]
        if ("EDP" in state):
            self._self = state["EDP"]
        if ("SP" in state):
            self._SP = state["SP"]
        if ("TREG" in state):
            self._TREG = state["TREG"]
        if ("STACK" in state):
            self._STACK = state["STACK"]
        if ("PAGE" in state):
            self._PAGE = state["PAGE"]
        if ("HEF" in state):
            self._HEF = state["HEF"]
        if ("STS" in state):
            self._STS = state["STS"]
        if ("ALM" in state):
            self._ALM = state["ALM"]
        if ("CF" in state):
            self._CF = state["CF"]
        if ("CSTF" in state):
            self._CSTF = state["CSTF"]
        if ("HALT" in state):
            self._HALT = state["HALT"]
        if ("PS" in state):
            self._PS = state["PS"]
        if ("PM" in state):
            self._PM = state["PM"]
        if ("LGT" in state):
            self._LGT = state["LGT"]
        if ("PDF" in state):
            self._PDF = state["PDF"]
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value
        if ("LCDRAM" in state):
            for i, value in state["LCDRAM"].items():
                self._LCDRAM[i] = value
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
    
    def pin_set(self, port, pin, level):
        if (port == 'PS'):
            self._PS = ~pin & self._PS | pin
            self._STS |= STS_SCF2_PS
            if (self._HEF & HEF_2_PS):
                self._HALT = 0
        elif (port == 'PM'):
            self._PM = ~pin & self._PM | pin
            self._STS |= STS_SCF3_PM
            if (self._HEF & HEF_3_PM):
                self._HALT = 0
        elif (port == 'RES'):
            self._reset()
            self._HALT = 1

    def pin_release(self, port, pin):
        if (port == 'PS'):
            self._PS &= ~pin
        elif (port == 'PM'):
            self._PM &= ~pin
        elif (port == 'RES'):
            self._HALT = 0

    def pc(self):
        return self._PC & 0xFFF
    
    def get_VRAM(self):
        return tuple(self._LCDRAM)
    
    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter
            
    def _timers_clock(self, exec_cycles):
        if (self._cycle_counter % self._32ms_div <= exec_cycles):
            self._STS |= STS_SCF1_PREDIV
            if (self._HEF & HEF_1_PREDIV):
                self._HALT = 0
    
        if (self._CSTF):
            if (self._cycle_counter % self._100ms_div <= exec_cycles):
                self._STS |= STS_SCF4_CHRONO
                if (self._HEF & HEF_4_CHRONO):
                    self._HALT = 0
                            
        if (self._cycle_counter % self._500ms_div <= exec_cycles):
            self._STS |= STS_SCF0_PREDIV_OVFW
            if (self._HEF & HEF_0_PREDIV_OVFW):
                    self._HALT = 0
                        
    def clock(self):
        exec_cycles = MCLOCK_DIV

        if (self._PS == 0xF):
            self._reset()
            self._PS = 0xF

        if (not self._HALT):
            opcode = self._ROM.getByte(self._PC)
            self._PC += 1
            exec_cycles = self._execute[opcode](self, opcode)
            self._instr_counter += 1

        self._cycle_counter += exec_cycles
        self._timers_clock(exec_cycles)
        return exec_cycles
    
    def _get_ram(self):
        if (self._DP < RAM_SIZE):
            return self._RAM[self._DP]
        return 0

    def _set_ram(self, value):
        if (self._DP < RAM_SIZE):
            self._RAM[self._DP] = value

    def _halt(self, opcode):
        #00000000
        self._HALT = 1
        return MCLOCK_DIV

    def _taat(self, opcode):
        #00000001   (AC, TREG) <- ROM(PGX, AC, M(DP))
        addr = 0x700 | (self._AC << 4) | self._get_ram()
        data = self._ROM.getByte(addr)
        self._AC = data >> 4
        self._TREG = data & 0xF
        return MCLOCKx2_DIV

    def _twrt(self, opcode):
        #00000010   PORT <- ROM(PGX, AC, M(DP))
        addr = 0x700 | (self._AC << 4) | self._get_ram()
        self._LCDRAM[self._SP] = self._ROM.getByte(addr)
        return MCLOCKx2_DIV

    def _tmel(self, opcode):
        #00000011   ALM <- ROM(PGX, AC, M(DP))
        addr = 0x700 | (self._AC << 4) | self._get_ram()
        data = self._ROM.getByte(addr)
        self._ALM = data
        self._sound.set_alm(data, self._cycle_counter)
        return MCLOCKx2_DIV

    def _csp(self, opcode):
        #00000100   CSTF <- 0; CSTF
        self._CSTF = 0
        return MCLOCK_DIV

    def _cst(self, opcode):
        #00000101   CSTF <- 1; CSTF
        self._CSTF = 1
        return MCLOCK_DIV

    def _rc5(self, opcode):
        #00000110   HEF0 <- 0; HEF0
        self._HEF &= ~HEF_0_PREDIV_OVFW
        return MCLOCK_DIV

    def _sc5(self, opcode):
        #00000111   HEF0 <- 1; HEF0
        self._HEF |= HEF_0_PREDIV_OVFW
        return MCLOCK_DIV

    def _jmp_x(self, opcode):
        #00001XXX XXXXXXXX   PC <- X
        self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        return MCLOCKx2_DIV

    def _jmp_p(self, opcode):
        #00010000   PC <- (PAGE, AC, M(DP))
        self._PC = (self._PAGE << 8) | (self._AC << 4) | self._get_ram()
        return MCLOCK_DIV

    def _page(self, opcode):
        #00010001   page <- [M(DP)]
        self._PAGE = self._get_ram() & 0x7
        return MCLOCK_DIV

    def _mtr(self, opcode):
        #00010010   M(DP) <- TREG
        self._set_ram(self._TREG)
        return MCLOCK_DIV

    def _rts(self, opcode):
        #00010011   PC <- (STACK)
        self._PC = self._STACK
        self._STACK = 0
        return MCLOCK_DIV

    def _mpcl(self, opcode):
        #00010100   M(DP) <- PC3-0
        self._set_ram((self._PC - 1) & 0xF)
        return MCLOCK_DIV

    def _mpcm(self, opcode):
        #00010101   M(DP) <- PC7-4
        self._set_ram(((self._PC - 1) >> 4) & 0xF)
        return MCLOCK_DIV

    def _mpch(self, opcode):
        #00010110   M(DP) <- PC10-8
        self._set_ram(((self._PC - 1) >> 8) & 0xF)
        return MCLOCK_DIV

    def _in(self, opcode):
        #00010111   AC <- (PORT)
        #to-do
        return MCLOCK_DIV

    def _asr0(self, opcode):
        #00011000   ACn <- ACn+1; AC3 <- 0
        self._AC = self._AC >> 1
        return MCLOCK_DIV

    def _asr1(self, opcode):
        #00011001   ACn <- ACn+1; AC3 <- 1
        self._AC = (self._AC >> 1) | 0x8
        return MCLOCK_DIV

    def _asl0(self, opcode):
        #00011010   ACn <- ACn-1; AC0 <- 0
        self._AC = (self._AC << 1) & 0xF
        return MCLOCK_DIV

    def _asl1(self, opcode):
        #00011011   ACn <- ACn-1; AC0 <- 1
        self._AC = ((self._AC << 1) & 0xF) | 0x1
        return MCLOCK_DIV

    def _sdpl(self, opcode):
        #00011100   DPL <- (AC)
        self._DP = (self._DP & 0xF0) | self._AC
        return MCLOCK_DIV

    def _sdph(self, opcode):
        #00011101   DPH <- (AC)
        self._DP = (self._DP & 0x0F) | (self._AC << 4)
        return MCLOCK_DIV

    def _edpl(self, opcode):
        #00011110   (DPL) <-> (EDPL)
        tmp = self._DP
        self._DP = (self._DP & 0xF0) | (self._EDP & 0x0F)
        self._EDP = (self._EDP & 0xF0) | (tmp & 0x0F)
        return MCLOCK_DIV

    def _edph(self, opcode):
        #00011111   (DPH) <-> (EDPH)
        tmp = self._DP
        self._DP = (self._DP & 0x0F) | (self._EDP & 0xF0)
        self._EDP = (self._EDP & 0x0F) | (tmp & 0xF0)
        return MCLOCK_DIV

    def _mvi_x(self, opcode):
        #0010XXXX   M(DP) <- X
        self._set_ram(opcode & 0xF)
        return MCLOCK_DIV

    def _ldi_x(self, opcode):
        #0011XXXX   AC <- X
        self._AC = opcode & 0xF
        return MCLOCK_DIV

    def _baz_x(self, opcode):
        #01000XXX XXXXXXXX   PC <- X if AC == 0
        if (self._AC == 0):
            self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        else:
            self._PC += 1
            return MCLOCK_DIV
        return MCLOCKx2_DIV

    def _bab0_x(self, opcode):
        #01001XXX XXXXXXXX   PC <- X if AC0
        if (self._AC & 0x1):
            self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        else:
            self._PC += 1
            return MCLOCK_DIV
        return MCLOCKx2_DIV

    def _banz_x(self, opcode):
        #01010XXX XXXXXXXX   PC <- X if AC != 0
        if (self._AC):
            self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        else:
            self._PC += 1
            return MCLOCK_DIV
        return MCLOCKx2_DIV

    def _bab1_x(self, opcode):
        #01011XXX XXXXXXXX   PC <- X if AC1
        if (self._AC & 0x2):
            self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        else:
            self._PC += 1
            return MCLOCK_DIV
        return MCLOCKx2_DIV

    def _bcnh_x(self, opcode):
        #01100XXX XXXXXXXX   PC <- X if CF == 0
        if (self._CF == 0):
            self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        else:
            self._PC += 1
            return MCLOCK_DIV
        return MCLOCKx2_DIV

    def _bab2_x(self, opcode):
        #01101XXX XXXXXXXX   PC <- X if AC2
        if (self._AC & 0x4):
            self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        else:
            self._PC += 1
            return MCLOCK_DIV
        return MCLOCKx2_DIV

    def _bch_x(self, opcode):
        #01110XXX XXXXXXXX   PC <- X if CF != 0
        if (self._CF):
            self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        else:
            self._PC += 1
            return MCLOCK_DIV
        return MCLOCKx2_DIV

    def _bab3_x(self, opcode):
        #01111XXX XXXXXXXX   PC <- X if AC3
        if (self._AC & 0x8):
            self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        else:
            self._PC += 1
            return MCLOCK_DIV
        return MCLOCKx2_DIV

    def _adc(self, opcode):
        #10000000   AC <- (AC) + [M(DP)] + (CF); CF
        result = self._AC + self._get_ram() + self._CF
        self._AC = result & 0xF
        self._CF = result > 0xF
        return MCLOCK_DIV

    def _sbc(self, opcode):
        #10000001   AC <- (AC) + ~[M(DP)] + (CF); CF
        result = self._AC + (self._get_ram() ^ 0xF) + self._CF
        self._AC = result & 0xF
        self._CF = result > 0xF
        return MCLOCK_DIV

    def _add(self, opcode):
        #10000010   AC <- (AC) + [M(DP)]; CF
        result = self._AC + self._get_ram()
        self._AC = result & 0xF
        self._CF = result > 0xF
        return MCLOCK_DIV

    def _sub(self, opcode):
        #10000011   AC <- (AC) + ~[M(DP)] + 1; CF
        result = self._AC + (self._get_ram() ^ 0xF) + 1
        self._AC = result & 0xF
        self._CF = result > 0xF
        return MCLOCK_DIV

    def _adn(self, opcode):
        #10000100   AC <- (AC) + [M(DP)]
        self._AC = (self._AC + self._get_ram()) & 0xF
        return MCLOCK_DIV

    def _and(self, opcode):
        #10000101   AC <- (AC) and [M(DP)]
        self._AC = self._AC & self._get_ram()
        return MCLOCK_DIV

    def _eor(self, opcode):
        #10000110   AC <- (AC) xor [M(DP)]
        self._AC = self._AC ^ self._get_ram()
        return MCLOCK_DIV

    def _or(self, opcode):
        #10000111   AC <- (AC) or [M(DP)]
        self._AC = self._AC | self._get_ram()
        return MCLOCK_DIV

    def _adc_m(self, opcode):
        #10001000   AC, M(DP) <- (AC) + [M(DP)] + (CF); CF
        result = self._AC + self._get_ram() + self._CF
        self._AC = result & 0xF
        self._set_ram(self._AC)
        self._CF = result > 0xF
        return MCLOCK_DIV

    def _sbc_m(self, opcode):
        #10001001   AC, M(DP) <- (AC) + ~[M(DP)] + (CF); CF
        result = self._AC + (self._get_ram() ^ 0xF) + self._CF
        self._AC = result & 0xF
        self._set_ram(self._AC)
        self._CF = result > 0xF
        return MCLOCK_DIV

    def _add_m(self, opcode):
        #10001010   AC, M(DP) <- (AC) + [M(DP)]; CF
        result = self._AC + self._get_ram()
        self._AC = result & 0xF
        self._set_ram(self._AC)
        self._CF = result > 0xF
        return MCLOCK_DIV

    def _sub_m(self, opcode):
        #10001011   AC, M(DP) <- (AC) + ~[M(DP)] + 1; CF
        result = self._AC + (self._get_ram() ^ 0xF) + 1
        self._AC = result & 0xF
        self._set_ram(self._AC)
        self._CF = result > 0xF
        return MCLOCK_DIV

    def _adn_m(self, opcode):
        #10001100   AC, M(DP) <- (AC) + [M(DP)]
        self._AC = (self._AC + self._get_ram()) & 0xF
        self._set_ram(self._AC)
        return MCLOCK_DIV

    def _and_m(self, opcode):
        #10001101   AC, M(DP) <- (AC) and [M(DP)]
        self._AC = self._AC & self._get_ram()
        self._set_ram(self._AC)
        return MCLOCK_DIV

    def _eor_m(self, opcode):
        #10001110   AC, M(DP) <- (AC) xor [M(DP)]
        self._AC = self._AC ^ self._get_ram()
        self._set_ram(self._AC)
        return MCLOCK_DIV

    def _or_m(self, opcode):
        #10001111   AC, M(DP) <- (AC) or [M(DP)]
        self._AC = self._AC | self._get_ram()
        self._set_ram(self._AC)
        return MCLOCK_DIV

    def _adci(self, opcode):
        #10010000 ----XXXX   AC <- (AC) + X + (CF); CF
        x = self._ROM.getByte(self._PC) & 0xF
        result = self._AC + x + self._CF
        self._AC = result & 0xF
        self._CF = result > 0xF
        self._PC += 1
        return MCLOCKx2_DIV

    def _sbci(self, opcode):
        #10010001 ----XXXX   AC <- (AC) + ~X + (CF); CF
        x = self._ROM.getByte(self._PC) & 0xF
        result = self._AC + (x ^ 0xF) + self._CF
        self._AC = result & 0xF
        self._CF = result > 0xF
        self._PC += 1
        return MCLOCKx2_DIV

    def _addi(self, opcode):
        #10010010 ----XXXX   AC <- (AC) + X; CF
        x = self._ROM.getByte(self._PC) & 0xF
        result = self._AC + x
        self._AC = result & 0xF
        self._CF = result > 0xF
        self._PC += 1
        return MCLOCKx2_DIV

    def _subi(self, opcode):
        #10010011 ----XXXX   AC <- (AC) + ~X + 1; CF
        x = self._ROM.getByte(self._PC) & 0xF
        result = self._AC + (x ^ 0xF) + 1
        self._AC = result & 0xF
        self._CF = result > 0xF
        self._PC += 1
        return MCLOCKx2_DIV

    def _adni(self, opcode):
        #10010100 ----XXXX   AC <- (AC) + X
        x = self._ROM.getByte(self._PC) & 0xF
        self._AC = (self._AC + x) & 0xF
        self._PC += 1
        return MCLOCKx2_DIV

    def _andi(self, opcode):
        #10010101 ----XXXX   AC <- (AC) and X
        x = self._ROM.getByte(self._PC) & 0xF
        self._AC = self._AC & x
        self._PC += 1
        return MCLOCKx2_DIV

    def _eori(self, opcode):
        #10010110 ----XXXX   AC <- (AC) xor X
        x = self._ROM.getByte(self._PC) & 0xF
        self._AC = self._AC ^ x
        self._PC += 1
        return MCLOCKx2_DIV

    def _ori(self, opcode):
        #10010111 ----XXXX   AC <- (AC) or X
        x = self._ROM.getByte(self._PC) & 0xF
        self._AC = self._AC | x
        self._PC += 1
        return MCLOCKx2_DIV

    def _inc(self, opcode):
        #10011000   M(DP), AC <- M(DP) + 1
        self._AC = (self._get_ram() + 1) & 0xF
        self._set_ram(self._AC)
        return MCLOCK_DIV

    def _dec(self, opcode):
        #10011001   M(DP), AC <- M(DP) - 1
        self._AC = (self._get_ram() - 1) & 0xF
        self._set_ram(self._AC)
        return MCLOCK_DIV

    def _idpl(self, opcode):
        #10011010   DPL <- (DPL) + 1
        self._DP = (self._DP & 0xF0) | ((self._DP + 1) & 0x0F)
        return MCLOCK_DIV

    def _ddpl(self, opcode):
        #10011011   DPL <- (DPL) - 1
        self._DP = (self._DP & 0xF0) | ((self._DP - 1) & 0x0F)
        return MCLOCK_DIV

    def _idph(self, opcode):
        #10011100   DPH <- (DPH) + 1
        self._DP = (self._DP + 0x10) & 0xFF
        return MCLOCK_DIV

    def _ddph(self, opcode):
        #10011101   DPH <- (DPH) - 1
        self._DP = (self._DP - 0x10) & 0xFF
        return MCLOCK_DIV

    def _isp(self, opcode):
        #10011110   SP <- (SP) + 1
        self._SP = (self._SP + 1) & 0xF
        return MCLOCK_DIV

    def _dsp(self, opcode):
        #10011111   SP <- (SP) - 1
        self._SP = (self._SP - 1) & 0xF
        return MCLOCK_DIV

    def _jsr_x(self, opcode):
        #10100XXX XXXXXXXX   STACK <- PC + 2; PC <- X
        self._STACK = self._PC + 1
        self._PC = ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC)
        return MCLOCKx2_DIV

    def _ipm(self, opcode):
        #10101000   AC <- [P(M)]
        self._AC = self._PM
        return MCLOCK_DIV

    def _lda(self, opcode):
        #10101001   AC <- [M(DP)]
        self._AC = self._get_ram()
        return MCLOCK_DIV

    def _lsp(self, opcode):
        #10101010   AC <- (SP)
        self._AC = self._SP
        return MCLOCK_DIV

    def _lhlt(self, opcode):
        #10101011   AC <- (STS2); STS2 <- 0; SCF1-4
        self._AC = self._STS >> 1
        self._STS &= ~(STS_SCF1_PREDIV | STS_SCF2_PS | STS_SCF3_PM | STS_SCF4_CHRONO)
        return MCLOCK_DIV

    def _l500(self, opcode):
        #10101100   AC <- (STS1); SCF0 <- 0; SCF0
        self._AC = self._STS & STS_SCF0_PREDIV_OVFW
        self._STS &= ~STS_SCF0_PREDIV_OVFW
        return MCLOCK_DIV

    def _sta(self, opcode):
        #10101101   M(DP) <- (AC)
        self._set_ram(self._AC)
        return MCLOCK_DIV

    def _ssp(self, opcode):
        #10101110   SP <- (AC)
        self._SP = self._AC
        return MCLOCK_DIV

    def _ips(self, opcode):
        #10101111   AC <- [P(S)]
        self._AC = self._PS
        return MCLOCK_DIV

    def _mdpl_x(self, opcode):
        #1011XXXX   DPL <- X
        self._DP = (self._DP & 0xF0) | (opcode & 0xF)
        return MCLOCK_DIV

    def _mdph_x(self, opcode):
        #1100XXXX   DPH <- X
        self._DP = (self._DP & 0x0F) | ((opcode & 0xF) << 4)
        return MCLOCK_DIV

    def _sic_x(self, opcode):
        #1101XXXX   HEFn+1 = Xn; HEF1-4
        self._HEF = (self._HEF & 0x1) | ((opcode & 0xF) << 1)
        return MCLOCK_DIV

    def _msp_x(self, opcode):
        #1110XXXX   SP <- X
        self._SP = opcode & 0xF
        return MCLOCK_DIV

    def _rcf(self, opcode):
        #11110000   CF <- 0; CF
        self._CF = 0
        return MCLOCK_DIV

    def _scf(self, opcode):
        #11110001   CF <- 1; CF
        self._CF = 1
        return MCLOCK_DIV

    def _rlgt(self, opcode):
        #11110010   LIGHT <- 0
        self._LIGHT = 0
        return MCLOCK_DIV

    def _slgt(self, opcode):
        #11110011   LIGHT <- 1
        self._LIGHT = 1
        return MCLOCK_DIV

    def _spdr_x(self, opcode):
        #111101XX   PDF <- X; PDF
        self._PDF = opcode & 0x3
        return MCLOCK_DIV

    def _rbak(self, opcode):
        #11111000   BCF <- 0
        self._BACKUP = 0
        return MCLOCK_DIV

    def _sbak(self, opcode):
        #11111001   BCF <- 1
        self._BACKUP = 1
        return MCLOCK_DIV

    def _sas_x(self, opcode):
        #11111010 XXXXXXXX   ALM <- X
        self._ALM = self._ROM.getByte(self._PC)
        self._sound.set_alm(self._ALM, self._cycle_counter)
        self._PC += 1
        return MCLOCKx2_DIV

    def _csec(self, opcode):
        #11111011   PREDIV15-11 <- 0; SCF0,1,4 <- 0; SCF0,1,4 
        self._STS &= ~(STS_SCF0_PREDIV_OVFW | STS_SCF1_PREDIV | STS_SCF4_CHRONO)
        #to-do
        return MCLOCK_DIV

    def _out(self, opcode):
        #11111100   PORT <- (AC, M(DP))
        self._LCDRAM[self._SP] = (self._AC << 4) | self._get_ram()
        return MCLOCK_DIV

    def _ldpl(self, opcode):
        #11111101   AC <- (DPL)
        self._AC = self._DP & 0x0F
        return MCLOCK_DIV

    def _ldph(self, opcode):
        #11111110   AC <- (DPH)
        self._AC = self._DP >> 4
        return MCLOCK_DIV

    def _nop(self, opcode):
        #11111111
        return MCLOCK_DIV
from .rom import ROM
from .PinTogglingSound import PinTogglingSound

RAM_SIZE = 128
SEG_COUNT = 36
COM_COUNT = 4
GRAM_SIZE = (SEG_COUNT // 4) * COM_COUNT

SUB_CLOCK = 32768

MCLOCK_DIV0 = 8
MCLOCK_DIV1 = 16
MCLOCK_DIV2 = 20
MCLOCK_DIV3 = 24
MCLOCK_DIV4 = 32

class T6770S():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = PinTogglingSound(clock)

        self._instr_counter = 0
        self._cycle_counter = 0
        self._counter = 0

        self._com_div = 768
        self._frame_div = self._com_div * COM_COUNT

        self._sound_gnd = mask['sound_gnd']

        self._sub_clock_div = SUB_CLOCK / clock

        self._reset()

        self._execute = (
            T6770S._nop,                          #00 0000 0000 CF -, SF 1; CC16; no operation
            T6770S._mov_a_m1l,                    #00 0000 0001 A = M[1L]; CF 0, SF 1; CC16
            T6770S._addc_a_mhl,                   #00 0000 0010 A += M[HL]; CF с, SF !с; CC16
            T6770S._inc_l,                        #00 0000 0011 L++; CF -, SF !c; CC16
            T6770S._scan_0,                       #00 0000 0100 SCAN = 0; CF -, SF 1; CC16; Writing to LCD shift register is enabled
            T6770S._mov_l_b,                      #00 0000 0101 L = B; CF -, SF 1; CC16
            T6770S._ret_a,                        #00 0000 0110 ?PC = STACKA, L = 0; CF -, SF 1; CC32
            T6770S._tst_t1,                       #00 0000 0111 CF -, SF !t1; CC16; test 1 sec event
            T6770S._tst_t8,                       #00 0000 1000 CF -, SF !t8; CC16; test 1/8 sec event
            T6770S._mov_m1l_a,                    #00 0000 1001 M[1L] = A; CF -, SF 1; CC16
            T6770S._rorc_mhl,                     #00 0000 1010 A = M[HL] = (CF << 3) | (M[HL] >> 1); CF c, SF !c; CC16; Rotate right through CF
            T6770S._nop,                          #00 0000 1011 CF -, SF 1; CC16; no operation
            T6770S._incp10,                       #00 0000 1100 inc10(M[HL+1]M[HL]), A = M[HL+1], L++; CF c, SF !c; CC32; Data memory pair (little-endian) increase modulo 10
            T6770S._in_a_ip,                      #00 0000 1101 A = IP; CF 0, SF 1; CC16; Read input port to A
            T6770S._rolc_mhl,                     #00 0000 1110 A = M[HL] = (M[HL] << 1) | CF; CF c, SF !c; CC16; Rotate left through CF
            T6770S._nop,                          #00 0000 1111 CF -, SF 1; CC16; no operation
            T6770S._mov_h_incb,                   #00 0001 0000 H = B = B + 1; CF -, SF !c; CC16
            T6770S._mov_a_b,                      #00 0001 0001 A = B; CF 0, SF 1; CC16
            T6770S._addc_a_b,                     #00 0001 0010 A = A + B + CF; CF c, SF !c; CC16 
            T6770S._inc_b,                        #00 0001 0011 B = B + 1; CF -, SF !c; CC16
            T6770S._nop,                          #00 0001 0100 CF -, SF 1; CC16; no operation
            T6770S._osc_ext,                      #00 0001 0101 ?clock from external oscillator (32k)
            T6770S._out_bz_1,                     #00 0001 0110 BZ = 1; CF -, SF 1; CC32; Set buzzer pin (0V)
            T6770S._delay_b,                      #00 0001 0111 B = 0xF; CF -, SF 0; CC8 * (n - 1) + CC16; Delay (B * CC8 + CC16)
            T6770S._wait_frame,                   #00 0001 1000 ?wait next frame
            T6770S._mov_b_a,                      #00 0001 1001 B = A; CF -, SF 1; CC16
            T6770S._clearm_mhl_dec,               #00 0001 1010 (L = L - 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 0; CC16 * (n - 1) + CC32
            T6770S._nop,                          #00 0001 1011 CF -, SF 1; CC16; no operation
            T6770S._nop2,                         #00 0001 1100 CF -, SF 1; CC32; no operation
            T6770S._in_a_iop,                     #00 0001 1101 A = IOP; CF 0, SF 1; CC16; Read input/output port to A
            T6770S._nop2,                         #00 0001 1110 CF -, SF 1; CC32; no operation
            T6770S._nop,                          #00 0001 1111 CF -, SF 1; CC16; no operation
            T6770S._mov_h_b_a,                    #00 0010 0000 H = B = A; CF -, SF 1; CC16
            T6770S._mov_a_mhl,                    #00 0010 0001 A = M[HL]; CF 0, SF 1; CC16
            T6770S._subc_a_mhl,                   #00 0010 0010 A = M[HL] - A - CF; CF b, SF !b; CC16
            T6770S._dec_l,                        #00 0010 0011 L = L - 1; CF -, SF !b; CC16
            T6770S._scan_1,                       #00 0010 0100 SCAN = 1; CF -, SF 1; CC16; Writing to LCD shift register is inhibited
            T6770S._mov_l_a,                      #00 0010 0101 L = A; CF -, SF 1; CC16
            T6770S._ret_d,                        #00 0010 0110 ?PC = STACKD, L = 0; CF -, SF 1; CC32
            T6770S._0027,                         #00 0010 0111 ?IOP direction; CF -, SF 1; CC16
            T6770S._tst_t64,                      #00 0010 1000 CF -, SF !t64; CC16; test 1/64 sec event
            T6770S._mov_mhl_a,                    #00 0010 1001 M[HL] = A; CF -, SF 1; CC16
            T6770S._exe_cf_a,                     #00 0010 1010 ?exe(PC + 1), exe(CF:A); CF -, SF 1; CC32; Execute the following instruction and then CF:A
            T6770S._nop,                          #00 0010 1011 CF -, SF 1; CC16; no operation
            T6770S._decp10,                       #00 0010 1100 dec10(M[HL+1]M[HL]), A = M[HL+1], L++; CF b, SF !b; CC32; Data memory pair (little-endian) decrease modulo 10
            T6770S._inc_mhl,                      #00 0010 1101 A = M[HL] = M[HL] + 1; CF c, SF !c; CC16
            T6770S._nop2,                         #00 0010 1110 CF -, SF 1; CC32; no operation
            T6770S._nop,                          #00 0010 1111 CF -, SF 1; CC16; no operation
            T6770S._mov_h_dec_b,                  #00 0011 0000 H = B = B - 1; CF -, SF !c; CC16
            T6770S._mov_a_l,                      #00 0011 0001 A = L; CF 0, SF 1; CC16
            T6770S._subc_a_b,                     #00 0011 0010 A = B - A - CF; CF = b, SF = !b; CC16
            T6770S._dec_b,                        #00 0011 0011 B = B - 1; CF -, SF !b; CC16 
            T6770S._movp_mhl_a,                   #00 0011 0100 M[HL] = M[H:L+1] = A, L = L + 2; CF -, SF 1; CC16
            T6770S._osc_int,                      #00 0011 0101 ?clock from interlal oscillation (resistor)
            T6770S._out_bz_0,                     #00 0011 0110 BZ = 0; CF -, SF 1; CC32; Reset buzzer pin (+3V)
            T6770S._0037,                         #00 0011 0111 ?IOP direction; CF -, SF 1; CC16
            T6770S._wait_com,                     #00 0011 1000 ?wait next com
            T6770S._mov_b_l,                      #00 0011 1001 B = L; CF -, SF 1; CC16
            T6770S._clearm_mhl_inc,               #00 0011 1010 (L = L + 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 1; CC16 * (n - 1) + CC32
            T6770S._nop,                          #00 0011 1011 CF -, SF 1; CC16; no operation
            T6770S._nop2,                         #00 0011 1100 CF -, SF 1; CC32; no operation
            T6770S._dec_mhl,                      #00 0011 1101 A = M[HL] = M[HL] - 1; CF b, SF !b; CC16
            T6770S._nop2,                         #00 0011 1110 CF -, SF 1; CC32; no operation
            T6770S._nop,                          #00 0011 1111 CF -, SF 1; CC16; no operation
            *([T6770S._mov_mh4linc_imm] * 16),    #00 0100 iiii M[HL] = IMM, H = B = 4, L = L + 1; CF -, SF !c; CC16
            *([T6770S._mov_mh4ldec_imm] * 16),    #00 0101 iiii M[HL] = IMM, H = B = 4, L = L - 1; CF -, SF !b; CC16
            *([T6770S._mov_mhlinc_imm] * 16),     #00 0110 iiii M[HL] = IMM, L = L + 1; CF -, SF !c; CC16
            *([T6770S._mov_mhl_imm] * 16),        #00 0111 iiii M[HL] = IMM, H = B = B + 1, A = 0; CF 0, SF !c; CC16
            *([T6770S._movm_mhlsubi_mhl] * 16),   #00 1000 iiii (M[H:L-IMM] = M[HL], L = L + 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); CC24 * (n - 1) + CC32
            *([T6770S._movm_mhladdi_mhl] * 16),   #00 1001 iiii (M[H:L+IMM] = M[HL], L = L - 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); CC24 * (n - 1) + CC32
            *([T6770S._inc_m1i] * 16),            #00 1010 iiii A = M[1:IMM] = M[1:IMM] + 1; CF c, SF !c; CC16
            *([T6770S._dec_m1i] * 16),            #00 1011 iiii A = M[1:IMM] = M[1:IMM] - 1; CF b, SF !b; CC16
            *([T6770S._addc10m_mhl_mbl] * 16),    #00 1100 iiii (A = M[HL] = (M[HL] + M[BL] + CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF c, SF 1; CC20 * (n - 1) + CC32
            *([T6770S._subc10m_mhl_mbl] * 16),    #00 1101 iiii (A = M[HL] = (M[HL] - M[BL] - CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF b, SF 1; CC20 * (n - 1) + CC32
            *([T6770S._out_outp_imm] * 16),       #00 1110 iiii A = OUTP = IMM; CF 0, SF 1; CC16
            *([T6770S._out_iop_imm] * 16),        #00 1111 iiii A = IOP = IMM; CF 0, SF 1; CC16
            *([T6770S._sbit_m] * 64),             #01 00bb hiii A = M[(HL if h)/0:IMM].b = 1; CF 0, SF 1; CC16
            *([T6770S._rbit_m] * 64),             #01 01bb hiii A = M[(HL if h)/0:IMM].b = 0; CF 0, SF 1; CC16
            *([T6770S._tbit_m] * 64),             #01 10bb hiii test M[(HL if h)/0:IMM].b; CF -, SF b==0; CC16
            *([T6770S._outm_lcd_mhl] * 16),       #01 1100 iiii (LCDP = M[HL], L = L - 1)WHILE((L + 1) >= IMM); CF -, SF 1; CC16 * (n - 1) + CC32
            *([T6770S._mov_pch_imm] * 16),        #01 1101 iiii PC<11:8> = IMM; CF -, SF -?; CC16
            *([T6770S._cmp_mhl_imm] * 16),        #01 1110 iiii A = M[HL] - IMM; CF b, SF z; CC32
            *([T6770S._addc_a_imm] * 16),         #01 1111 iiii A = A + CF; CF c, SF !c; CC16
            *([T6770S._mov_l_imm] * 16),          #10 0000 iiii L = IMM; CF -, SF 1; CC16
            *([T6770S._calla] * 16),              #10 0001 iiii ?STACKA = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
            *([T6770S._mov_a_m0i] * 16),          #10 0010 iiii A = M[0:IMM]; CF 0, SF 1; CC16
            *([T6770S._calld] * 16),              #10 0011 iiii ?STACKD = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
            *([T6770S._mov_b_imm] * 16),          #10 0100 iiii B = IMM; CF -, SF 1; CC16
            *([T6770S._calla] * 16),              #10 0101 iiii ?STACKA = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
            *([T6770S._mov_m0i_a] * 16),          #10 0110 iiii M[0:IMM] = A; CF -, SF 1; CC16
            *([T6770S._calld] * 16),              #10 0111 iiii ?STACKD = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
            *([T6770S._mov_h_imm] * 16),          #10 1000 iiii H = IMM; CF -, SF 1; CC16
            *([T6770S._calla] * 16),              #10 1001 iiii ?STACKA = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
            *([T6770S._mov_a_m1i] * 16),          #10 1010 iiii A = M[1:IMM]; CF 0, SF 1; CC16
            *([T6770S._calld] * 16),              #10 1011 iiii ?STACKD = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
            *([T6770S._mov_a_imm] * 16),          #10 1100 iiii A = IMM; CF 0, SF 1; CC16
            *([T6770S._calla] * 16),              #10 1101 iiii ?STACKA = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
            *([T6770S._mov_m1i_a] * 16),          #10 1110 iiii M[1:IMM] = A; CF -, SF 1; CC16
            *([T6770S._calld] * 16),              #10 1111 iiii ?STACKD = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
            *([T6770S._bs_imm] * 256)             #11 iiii iiii if SF (PC<7:0> = IMM); CF -, SF 1; CC16
        )

    def _reset(self):
        self._PC = 0xF00
        self._A = 0
        self._B = 0

        self._H = 0
        self._L = 0
        
        self._CF = 0
        self._nSF = 0
        
        self._PZF = 0
        self._PYF = 0
        self._PXF = 0

        self._INP = 0
        self._OUTP = 0
        self._IOP = 0
        self._BZ = 0
        
        self._HALT = 0

        self._GRAM_OFFSET = 0
        self._SCAN = 1
        self._PCHTMP = -1

        self._RAM = [0] * RAM_SIZE
        self._GRAM = [0] * GRAM_SIZE

        self._CLC_SRC = 0

    def reset(self):
        self._reset()

    def examine(self):
        return {
            "PC": self._PC & 0xFFF,
            "A": self._A,
            "B": self._B,
            "H": self._H,
            "L": self._L,
            "CF": self._CF,
            "SF": self._nSF ^ 0x1,
            "PZF": self._PZF,
            "PYF": self._PYF,
            "PXF": self._PXF,
            "INP": self._INP,
            "OUTP": self._OUTP,
            "IOP": self._IOP,
            "BZ": self._BZ,
            "RAM": tuple(self._RAM),
            "GRAM": tuple(self._GRAM),
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] & 0xFFF
        if ("A" in state):
            self._A = state["A"] & 0xF
        if ("B" in state):
            self._B = state["B"] & 0xF
        if ("H" in state):
            self._H = state["H"] & 0x7
        if ("L" in state):
            self._L = state["L"] & 0xF
        if ("CF" in state):
            self._CF = state["CF"] & 0x1
        if ("SF" in state):
            self._nSF = (state["SF"] & 0x1) ^ 0x1
        if ("PZF" in state):
            self._PZF = state["PZF"] & 0x1
        if ("PYF" in state):
            self._PYF = state["PYF"] & 0x1
        if ("PXF" in state):
            self._PXF = state["PXF"] & 0x1
        if ("INP" in state):
            self._INP = state["INP"] & 0xF
        if ("OUTP" in state):
            self._OUTP = state["OUTP"] & 0xF
        if ("IOP" in state):
            self._IOP = state["IOP"] & 0xF
        if ("BZ" in state):
            self._BZ = state["BZ"] & 0xF
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xF
        if ("GRAM" in state):
            for i, value in state["GRAM"].items():
                self._GRAM[i] = value & 0xF
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
    
    def pin_set(self, port, pin, level):
        if (port == 'INP'):
            self._INP = ~(1 << pin) & self._INP | level << pin
        elif (port == 'IOP'):
            self._IOP = ~(1 << pin) & self._IOP | level << pin
        elif (port == 'RES'):
            self._reset()
            self._HALT = 1

    def pin_release(self, port, pin):
        if (port == 'INP'):
            self._INP &= ~(1 << pin)
        elif (port == 'IOP'):
            self._IOP &= ~(1 << pin)
        elif (port == 'RES'):
            self._HALT = 0

    def pc(self):
        return self._PC & 0xFFF
    
    def get_VRAM(self):
        return tuple(self._GRAM)
    
    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter

    def clock(self):
        exec_cycles = MCLOCK_DIV4
        if (not self._HALT):
            opcode = self._ROM.getWord(self._PC << 1)
            self._PC = (self._PC & 0xF00) | ((self._PC + 1) & 0xFF)
            exec_cycles = self._execute[opcode & 0x3FF](self, opcode)
            self._instr_counter += 1

        if (self._CLC_SRC):
            self._counter += exec_cycles
            exec_cycles /= self._sub_clock_div
        else:
            self._counter += exec_cycles * self._sub_clock_div

        if (self._counter % 512 < exec_cycles * self._sub_clock_div):
            self._PZF = True
            if (self._counter % 4096 < exec_cycles * self._sub_clock_div):
                self._PYF = True
                if (self._counter % 32768 < exec_cycles * self._sub_clock_div):
                    self._PXF = True

        self._cycle_counter += exec_cycles
        return exec_cycles
    
    def _nop(self, opcode):
        #CF -, SF 1; CC16; no operation
        self._nSF = 0
        return MCLOCK_DIV1

    def _mov_a_m1l(self, opcode):
        #00 0000 0001 A = M[1L]; CF 0, SF 1; CC16
        self._A = self._RAM[0x10 | self._L]
        self._nSF = self._CF = 0
        return MCLOCK_DIV1

    def _addc_a_mhl(self, opcode):
        #00 0000 0010 A += M[HL]; CF c, SF !c; CC16
        a = self._A + self._RAM[(self._H << 4) | self._L]
        self._A = a & 0xF
        self._nSF = self._CF = a > 15
        return MCLOCK_DIV1

    def _inc_l(self, opcode):
        #00 0000 0011 L++; CF -, SF !c; CC16
        l = self._L + 1
        self._L = l & 0xF
        self._nSF = l > 15
        return MCLOCK_DIV1
    
    def _scan_0(self, opcode):
        #00 0000 0100 SCAN = 0; CF -, SF 1; CC16; Writing to LCD shift register is enabled
        self._SCAN = 0
        self._nSF = 0
        return MCLOCK_DIV1

    def _mov_l_b(self, opcode):
        #00 0000 0101 L = B; CF -, SF 1; CC16
        self._L = self._B
        self._nSF = 0
        return MCLOCK_DIV1

    def _ret_a(self, opcode):
        #00 0000 0110 ?PC = STACKA, L = 0; CF -, SF 1; CC32
        #self._PC = (self._RAM[0x0C] << 8) | (self._RAM[0x0B] << 4) | (self._RAM[0x0A])
        self._PC = self._PCa
        self._L = 0
        self._nSF = 0
        return MCLOCK_DIV4

    def _tst_t1(self, opcode):
        #00 0000 0111 CF -, SF !t1; CC16; test 1 sec event
        self._nSF = self._PXF
        self._PXF = False
        return MCLOCK_DIV1

    def _tst_t8(self, opcode):
        #00 0000 1000 CF -, SF !t8; CC16; test 1/8 sec event
        self._nSF = self._PYF
        self._PYF = False
        return MCLOCK_DIV1

    def _mov_m1l_a(self, opcode):
        #00 0000 1001 M[1L] = A; CF -, SF 1; CC16
        self._RAM[0x10 | self._L] = self._A
        self._nSF = 0
        return MCLOCK_DIV1

    def _rorc_mhl(self, opcode):
        #00 0000 1010 A = M[HL] = (CF << 3) | (M[HL] >> 1); CF c, SF !c; CC16; Rotate right through CF
        hl = (self._H << 4) | self._L
        cf = self._RAM[hl] & 0x1
        self._A = self._RAM[hl] = (self._CF << 3) | (self._RAM[hl] >> 1)
        self._CF = cf
        self._nSF = 0
        return MCLOCK_DIV1

    def _incp10(self, opcode):
        #00 0000 1100 inc10(M[HL]M[HL+1]), A = M[HL+1], L++; CF c, SF !c; CC32; Increment data memory pair (little-endian) modulo 10.
        hll = (self._H << 4) | self._L
        self._L = (self._L + 1) & 0xF
        hlh = (self._H << 4) | self._L 
        mh = self._RAM[hlh]
        self._RAM[hll] += 1
        if (self._RAM[hll] > 9):
            self._RAM[hll] = (self._RAM[hll] + 6) & 0xF
            mh += 1
            self._RAM[hlh] = mh & 0xF
        self._A = self._RAM[hlh]
        self._nSF = self._CF = mh > 15
        return MCLOCK_DIV4

    def _in_a_ip(self, opcode):
        #00 0000 1101 A = IP; CF 0, SF 1; CC16; Read input port to A
        self._A = self._INP
        self._nSF = self._CF = 0
        return MCLOCK_DIV1

    def _rolc_mhl(self, opcode):
        #00 0000 1110 A = M[HL] = (M[HL] << 1) | CF; CF c, SF !c; CC16; Rotate left through CF
        hl = (self._H << 4) | self._L
        cf = self._RAM[hl] >> 3
        self._A = self._RAM[hl] = self._CF | (self._RAM[hl] << 1)
        self._CF = cf
        self._nSF = 0
        return MCLOCK_DIV1

    def _mov_h_incb(self, opcode):
        #00 0001 0000 H = B = B + 1; CF -, SF !c; CC16
        b = self._B + 1
        self._B = b & 0xF
        self._H = b & 0x7
        self._nSF = b > 15
        return MCLOCK_DIV1

    def _mov_a_b(self, opcode):
        #00 0001 0001 A = B; CF 0, SF 1; CC16
        self._A = self._B
        self._nSF = self._CF = 0
        return MCLOCK_DIV1

    def _addc_a_b(self, opcode):
        #00 0001 0010 A = A + B + CF; CF c, SF !c; CC16 
        a = self._A + self._B + self._CF
        self._A = a & 0xF
        self._nSF = self._CF = a > 15
        return MCLOCK_DIV1

    def _inc_b(self, opcode):
        #00 0001 0011 B = B + 1; CF -, SF !c; CC16
        b = self._B + 1
        self._B = b & 0xF
        self._nSF = b > 15
        return MCLOCK_DIV1

    def _osc_ext(self, opcode):
        #00 0001 0101 ?wait
        self._CLC_SRC = 1
        self._nSF = 0
        return MCLOCK_DIV1

    def _out_bz_1(self, opcode):
        #00 0001 0110 BZ = 1; CF -, SF 1; CC32; Set buzzer pin (0V)
        self._BZ = 1
        self._sound.toggle(self._sound_gnd ^ self._BZ, 0, self._cycle_counter)
        self._nSF = 0
        return MCLOCK_DIV4

    def _delay_b(self, opcode):
        #00 0001 0111 B = 0xF; CF -, SF 0; CC8 * (n - 1) + CC16; Delay (B * CC8 + CC16)
        delay = MCLOCK_DIV1 + MCLOCK_DIV0 * self._B
        self._B = 0xF
        self._nSF = 0
        return delay

    def _wait_frame(self, opcode):
        #00 0001 1000 ?wait next frame
        self._GRAM_OFFSET = 0
        self._nSF = 0
        return self._frame_div - (self._cycle_counter % self._frame_div)

    def _mov_b_a(self, opcode):
        #00 0001 1001 B = A; CF -, SF 1; CC16
        self._B = self._A
        self._nSF = 0
        return MCLOCK_DIV1

    def _clearm_mhl_dec(self, opcode):
        #00 0001 1010 (L = L - 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 0; CC16 * (n - 1) + CC32
        count = self._B + 1
        for _ in range(count):
            self._L = (self._L - 1) & 0xF
            self._RAM[(self._H << 4) | self._L] = 0
        self._A = 0
        self._B = 15
        self._nSF = self._CF = 0
        return MCLOCK_DIV1 + MCLOCK_DIV1 * count

    def _nop2(self, opcode):
        #CF -, SF 1; CC32; no operation
        self._nSF = 0
        return MCLOCK_DIV4

    def _in_a_iop(self, opcode):
        #00 0001 1101 A = IOP; CF 0, SF 1; CC16; Read input/output port to A
        self._A = self._IOP
        self._CF = self._nSF = 0
        return MCLOCK_DIV1

    def _mov_h_b_a(self, opcode):
        #00 0010 0000 H = B = A; CF -, SF = 1; CC16
        self._B = self._A
        self._H = self._A & 0x7
        self._nSF = 0
        return MCLOCK_DIV1

    def _mov_a_mhl(self, opcode):
        #00 0010 0001 A = M[HL]; CF 0, SF 1; CC16
        self._A = self._RAM[(self._H << 4) | self._L]
        self._CF = self._nSF = 0
        return MCLOCK_DIV1

    def _subc_a_mhl(self, opcode):
        #00 0010 0010 A = M[HL] - A - CF; CF b, SF !b; CC16
        a = self._RAM[(self._H << 4) | self._L] - self._A - self._CF
        self._A = a & 0xF
        self._CF = self._nSF = a < 0
        return MCLOCK_DIV1

    def _dec_l(self, opcode):
        #00 0010 0011 L = L - 1; CF -, SF !b; CC16
        l = self._L - 1
        self._L = l & 0xF
        self._nSF = l < 0
        return MCLOCK_DIV1

    def _scan_1(self, opcode):
        #00 0010 0100 SCAN = 1; CF -, SF 1; CC16; Writing to LCD shift register is inhibited
        self._SCAN = 1
        self._nSF = 0
        return MCLOCK_DIV1

    def _mov_l_a(self, opcode):
        #00 0010 0101 L = A; CF -, SF 1; CC16
        self._L = self._A
        self._nSF = 0
        return MCLOCK_DIV1

    def _ret_d(self, opcode):
        #00 0010 0110 ?PC = STACKD, L = 0; CF -, SF 1; CC32
        #self._PC = (self._RAM[0x0F] << 8) | (self._RAM[0x0E] << 4) | (self._RAM[0x0D])
        self._PC = self._PCd
        self._L = 0
        self._nSF = 0
        return MCLOCK_DIV4

    def _0027(self, opcode):
        #00 0010 0111 ?IOP direction; CF -, SF 1; CC16
        self._nSF = 0
        return MCLOCK_DIV1
    
    def _tst_t64(self, opcode):
        #00 0010 1000 CF -, SF !t1; CC16; test 1/64 sec event
        self._nSF = self._PZF
        self._PZF = False
        return MCLOCK_DIV1

    def _mov_mhl_a(self, opcode):
        #00 0010 1001 M[HL] = A; CF -, SF 1; CC16
        self._RAM[(self._H << 4) | self._L] = self._A
        self._nSF = 0
        return MCLOCK_DIV1

    def _exe_cf_a(self, opcode):
        #00 0010 1010 ?exe(PC + 1), exe(CF:A); CF -, SF 1; CC32; Execute the following instruction and then CF:A
        addr = ((self._PC & 0xFE0) | ((self._CF << 4) | self._A)) << 1
        opcode = self._ROM.getWord(self._PC << 1)
        exec_cycles = self._execute[opcode & 0x3FF](self, opcode)
        self._PC = (self._PC & 0xF00) | ((self._PC + 1) & 0xFF)
        opcode = self._ROM.getWord(addr)
        exec_cycles += self._execute[opcode & 0x3FF](self, opcode)
        return exec_cycles + MCLOCK_DIV4

    def _decp10(self, opcode):
        #00 0010 1100 dec10(M[HL+1]M[HL]), A = M[HL+1], L++; CF b, SF !b; CC32; Decrement data memory pair (little-endian) modulo 10.
        hl = (self._H << 4) | self._L
        self._L = (self._L + 1) & 0xF
        hl1 = (self._H << 4) | self._L 
        mh = self._RAM[hl1]
        self._RAM[hl] = (self._RAM[hl] - 1) & 0xF
        if (self._RAM[hl] > 9):
            self._RAM[hl] = (self._RAM[hl] + 10) & 0xF
            mh -= 1
            self._RAM[hl1] = mh & 0xF
        self._A = self._RAM[hl1]
        self._nSF = self._CF = mh < 0
        return MCLOCK_DIV4

    def _inc_mhl(self, opcode):
        #00 0010 1101 A = M[HL] = M[HL] + 1; CF c, SF !c; CC16
        hl = (self._H << 4) | self._L
        res = self._RAM[hl] + 1
        self._A = self._RAM[hl] = res & 0xF
        self._nSF = self._CF = res > 15
        return MCLOCK_DIV1

    def _mov_h_dec_b(self, opcode):
        #00 0011 0000 H = B = B - 1; CF -, SF !c; CC16
        res = self._B - 1
        self._B = res & 0xF
        self._H = res & 0x7
        self._nSF = res < 0
        return MCLOCK_DIV1

    def _mov_a_l(self, opcode):
        #00 0011 0001 A = L; CF 0, SF 1; CC16
        self._A = self._L
        self._CF = self._nSF = 0
        return MCLOCK_DIV1

    def _subc_a_b(self, opcode):
        #00 0011 0010 A = B - A - CF; CF = b, SF = !b; CC16
        a = self._B - self._A - self._CF
        self._A = a & 0xF
        self._CF = self._nSF = a < 0
        return MCLOCK_DIV1

    def _dec_b(self, opcode):
        #00 0011 0011 B = B - 1; CF -, SF !b; CC16 
        b = self._B - 1
        self._B = b & 0xF
        self._nSF = b < 0
        return MCLOCK_DIV1

    def _movp_mhl_a(self, opcode):
        #00 0011 0100 M[HL] = M[H:L+1] = A, L = L + 2; CF -, SF 1; CC16
        hl = (self._H << 4) | self._L
        hl1 = (self._H << 4) | ((self._L + 1) & 0xF) 
        self._RAM[hl] = self._RAM[hl1] = self._A
        self._L = (self._L + 2) & 0xF
        self._nSF = 0
        return MCLOCK_DIV1

    def _osc_int(self, opcode):
        #00 0011 0101 ?cntrl
        self._CLC_SRC = 0
        self._nSF = 0
        return MCLOCK_DIV1

    def _out_bz_0(self, opcode):
        #00 0011 0110 BZ = 0; CF -, SF 1; CC32, Reset buzzer pin (+3V)
        self._BZ = 0
        self._sound.toggle(self._sound_gnd ^ self._BZ, 0, self._cycle_counter)
        self._nSF = 0
        return MCLOCK_DIV4

    def _0037(self, opcode):
        #00 0011 0111 ?IOP direction; CF -, SF 1; CC16
        self._nSF = 0
        return MCLOCK_DIV1

    def _wait_com(self, opcode):
        #00 0011 1000 ?wait next com
        self._GRAM_OFFSET = (self._GRAM_OFFSET + SEG_COUNT // 4) % GRAM_SIZE
        self._nSF = 0
        return self._com_div - (self._cycle_counter % self._com_div)

    def _mov_b_l(self, opcode):
        #00 0011 1001 B = L; CF -, SF 1; CC16
        self._B = self._L
        self._nSF = 0
        return MCLOCK_DIV1

    def _clearm_mhl_inc(self, opcode):
        #00 0011 1010 (L = L + 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 1; CC16 * (n - 1) + CC32
        count = self._B + 1
        for _ in range(count):
            self._L = (self._L + 1) & 0xF
            self._RAM[(self._H << 4) | self._L] = 0
        self._A = 0
        self._B = 15
        self._nSF = self._CF = 0
        return MCLOCK_DIV1 + MCLOCK_DIV1 * count
        
    def _dec_mhl(self, opcode):
        #00 0011 1101 A = M[HL] = M[HL] - 1; CF b, SF !b; CC16
        hl = (self._H << 4) | self._L
        res = self._RAM[hl] - 1
        self._A = self._RAM[hl] = res & 0xF
        self._nSF = self._CF = res < 0 
        return MCLOCK_DIV1

    def _mov_mh4linc_imm(self, opcode):
        #00 0100 iiii M[HL] = IMM, H = B = 4, L = L + 1; CF -, SF !c; CC16
        self._RAM[(self._H << 4) | self._L] = opcode & 0xF
        self._H = self._B = 4
        l = self._L + 1
        self._L = l & 0xF
        self._nSF = l > 15
        return MCLOCK_DIV1

    def _mov_mh4ldec_imm(self, opcode):
        #00 0101 iiii M[HL] = IMM, H = B = 4, L = L - 1; CF -, SF !b; CC16
        self._RAM[(self._H << 4) | self._L] = opcode & 0xF
        self._H = self._B = 4
        l = self._L - 1
        self._L = l & 0xF
        self._nSF = l < 0
        return MCLOCK_DIV1

    def _mov_mhlinc_imm(self, opcode):
        #00 0110 iiii M[HL] = IMM, L = L + 1; CF -, SF !c; CC16
        self._RAM[(self._H << 4) | self._L] = opcode & 0xF
        l = self._L + 1
        self._L = l & 0xF
        self._nSF = l > 15
        return MCLOCK_DIV1

    def _mov_mhl_imm(self, opcode):
        #00 0111 iiii M[HL] = IMM, H = B = B + 1, A = 0; CF 0, SF !c; CC16
        self._RAM[(self._H << 4) | self._L] = opcode & 0xF
        b = self._B + 1
        self._B = b & 0xF
        self._H = b & 0x7
        self._nSF = b > 15
        self._A = self._CF = 0
        return MCLOCK_DIV1

    def _movm_mhlsubi_mhl(self, opcode):
        #00 1000 iiii (M[H:L-IMM] = M[HL], L = L + 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); CC24 * (n - 1) + CC32
        i = opcode & 0xF
        count = 16 - self._B
        for _ in range(count):
            self._RAM[(self._H << 4) | ((self._L - i) & 0xF)] = self._RAM[(self._H << 4) | self._L]
            self._L = (self._L + 1) & 0xF
        self._B = (i - 1) & 0xF
        self._CF = 0
        self._nSF = i == 0
        return MCLOCK_DIV3 * (count - 1) + MCLOCK_DIV4

    def _movm_mhladdi_mhl(self, opcode):
        #00 1001 iiii (M[H:L+IMM] = M[HL], L = L - 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); CC24 * (n - 1) + CC32
        i = opcode & 0xF
        count = 16 - self._B
        for _ in range(count):
            self._RAM[(self._H << 4) | ((self._L + i) & 0xF)] = self._RAM[(self._H << 4) | self._L]
            self._L = (self._L - 1) & 0xF
        self._B = (i - 1) & 0xF
        self._CF = 0
        self._nSF = i == 0
        return MCLOCK_DIV3 * (count - 1) + MCLOCK_DIV4
    
    def _inc_m1i(self, opcode):
        #00 1010 iiii A = M[1:IMM] = M[1:IMM] + 1; CF c, SF !c; CC16
        hl = 0x10 | (opcode & 0xF)
        res = self._RAM[hl] + 1
        self._A = self._RAM[hl] = res & 0xF
        self._nSF = self._CF = res > 15 
        return MCLOCK_DIV1

    def _dec_m1i(self, opcode):
        #00 1011 iiii A = M[1:IMM] = M[1:IMM] - 1; CF b, SF !b; CC16
        hl = 0x10 | (opcode & 0xF)
        res = self._RAM[hl] - 1
        self._A = self._RAM[hl] = res & 0xF
        self._nSF = self._CF = res < 0 
        return MCLOCK_DIV1

    def _addc10m_mhl_mbl(self, opcode):
        #00 1100 iiii (A = M[HL] = (M[HL] + M[BL] + CF) mod 10, L = L + 1)WHILE(L - 1 < 16 - IMM); CF c, SF 1; CC20 * (n - 1) + CC32
        count = 16 - (opcode & 0xF) - self._L + 1
        if count <= 0:
            count = 1
        for _ in range(count):
            hl = (self._H << 4) | self._L
            res = self._RAM[hl] + self._RAM[((self._B & 0x7) << 4) | self._L] + self._CF
            if (res > 9):
                res += 6
                self._CF = 1
            else:
                self._CF = 0
            self._A = self._RAM[hl] = res & 0xF
            self._L = (self._L + 1) & 0xF
        self._nSF = 0
        return MCLOCK_DIV4 + MCLOCK_DIV2 * (count - 1)

    def _subc10m_mhl_mbl(self, opcode):
        #00 1101 iiii (A = M[HL] = (M[HL] - M[BL] - CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF b, SF 1; CC20 * (n - 1) + CC32
        count = 16 - (opcode & 0xF) - self._L + 1
        if count <= 0:
            count = 1
        for _ in range(count):
            hl = (self._H << 4) | self._L
            res = self._RAM[hl] - self._RAM[((self._B & 0x7) << 4) | self._L] - self._CF
            if (res < 0 or res > 9):
                res += 10
                self._CF = 1
            else:
                self._CF = 0
            self._A = self._RAM[hl] = res & 0xF
            self._L = (self._L + 1) & 0xF
        self._nSF = 0
        return MCLOCK_DIV4 + MCLOCK_DIV2 * (count - 1)

    def _out_outp_imm(self, opcode):
        #00 1110 iiii A = OUTP = IMM; CF 0, SF 1, CC16
        self._A = self._OUTP = opcode & 0xF
        self._CF = self._nSF = 0 
        return MCLOCK_DIV1

    def _out_iop_imm(self, opcode):
        #00 1111 iiii A = IOP = IMM; CF 0, SF 1, CC16
        self._A = self._IOP = opcode & 0xF
        self._CF = self._nSF = 0 
        return MCLOCK_DIV1

    def _sbit_m(self, opcode):
        #01 00bb hiii A = M[(HL if h)/0:IMM].b = 1; CF 0, SF 1; CC16
        hl = 0
        if (opcode & 0x8):
            hl = (self._H << 4) | self._L
        else:
            hl = opcode & 0x7

        self._A = self._RAM[hl] = self._RAM[hl] | (1 << ((opcode >> 4) & 0x3))
        self._CF = self._nSF = 0
        return MCLOCK_DIV1

    def _rbit_m(self, opcode):
        #01 01bb hiii A = M[(HL if h)/0:IMM].b = 0; CF 0, SF 1; CC16
        hl = 0
        if (opcode & 0x8):
            hl = (self._H << 4) | self._L
        else:
            hl = opcode & 0x7
        self._A = self._RAM[hl] = self._RAM[hl] & ~(1 << ((opcode >> 4) & 0x3))
        self._CF = self._nSF = 0
        return MCLOCK_DIV1
            
    def _tbit_m(self, opcode):
        #01 10bb hiii test M[(HL if h)/0:IMM].b; CF -, SF b==0; CC16
        if (opcode & 0x8):
            self._nSF = (self._RAM[(self._H << 4) | self._L] >> ((opcode >> 4) & 0x3)) & 0x1
        else:
            self._nSF = (self._RAM[opcode & 0x7] >> ((opcode >> 4) & 0x3)) & 0x1
        return MCLOCK_DIV1
            
    def _outm_lcd_mhl(self, opcode):
        #01 1100 iiii (LCDP = M[HL], L = L - 1)WHILE((L + 1) >= IMM); CF -, SF 1, CC16 * (n - 1) + CC32
        count = (self._L - (opcode & 0xF)) + 2
        if count <= 0:
            count = 1
        for _ in range(count):
            self._GRAM[self._GRAM_OFFSET] = self._RAM[(self._H << 4) | self._L]
            self._GRAM_OFFSET = (self._GRAM_OFFSET + 1) % GRAM_SIZE
            self._L = (self._L - 1) & 0xF
        self._nSF = 0
        return MCLOCK_DIV4 + MCLOCK_DIV1 * (count - 1)

    def _mov_pch_imm(self, opcode):
        #01 1101 iiii PC<11:8> = IMM; CF -, SF -?; CC16
        if (not self._nSF):
            self._PCHTMP = opcode & 0xF
        return MCLOCK_DIV1

    def _cmp_mhl_imm(self, opcode):
        #01 1110 iiii A = M[HL] - IMM; CF b, SF z; CC32
        a = self._RAM[(self._H << 4) | self._L] - (opcode & 0xF)
        self._A = a & 0xF
        self._CF = a < 0
        self._nSF = a != 0
        return MCLOCK_DIV4

    def _addc_a_imm(self, opcode):
        #01 1111 iiii A = A + CF; CF c, SF !c; CC16
        a = self._A + (opcode & 0xF) + self._CF
        self._A = a & 0xF
        self._CF = self._nSF = a > 15
        return MCLOCK_DIV1

    def _mov_l_imm(self, opcode):
        #10 0000 iiii L = IMM; CF -, SF 1; CC16
        self._L = opcode & 0xF
        self._nSF = 0 
        return MCLOCK_DIV1

    def _calla(self, opcode):
        #10 hh01 iiii ?STACKA = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
        #self._RAM[0x0C] = (self._PC >> 8) & 0xF
        #self._RAM[0x0B] = (self._PC >> 4) & 0xF
        #self._RAM[0x0A] = self._PC & 0xF
        self._PCa = self._PC
        self._PC = ((opcode & 0xC0) << 4) | 0x1F0 | (opcode & 0xF)
        self._L = 0
        self._nSF = 0
        return MCLOCK_DIV4

    def _mov_a_m0i(self, opcode):
        #10 0010 iiii A = M[0:IMM]; CF 0, SF 1; CC16
        self._A = self._RAM[opcode & 0xF]
        self._CF = self._nSF = 0 
        return MCLOCK_DIV1

    def _calld(self, opcode):
        #10 hh11 iiii ?STACKD = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
        #self._RAM[0x0F] = (self._PC >> 8) & 0xF
        #self._RAM[0x0E] = (self._PC >> 4) & 0xF
        #self._RAM[0x0D] = self._PC & 0xF
        self._PCd = self._PC
        self._PC = ((opcode & 0xC0) << 4) | 0x3F0 | (opcode & 0xF)
        self._L = 0
        self._nSF = 0
        return MCLOCK_DIV4

    def _mov_b_imm(self, opcode):
        #10 0100 iiii B = IMM; CF -, SF 1; CC16
        self._B = opcode & 0xF
        self._nSF = 0 
        return MCLOCK_DIV1

    def _mov_m0i_a(self, opcode):
        #10 0110 iiii M[0:IMM] = A; CF -, SF 1; CC16
        self._RAM[opcode & 0xF] = self._A
        self._nSF = 0 
        return MCLOCK_DIV1

    def _mov_h_imm(self, opcode):
        #10 1000 iiii H = IMM; CF -, SF 1; CC16
        self._H = opcode & 0x7
        self._nSF = 0 
        return MCLOCK_DIV1

    def _mov_a_m1i(self, opcode):
        #10 1010 iiii A = M[1:IMM]; CF 0, SF 1; CC16
        self._A = self._RAM[0x10 | (opcode & 0xF)]
        self._CF = self._nSF = 0 
        return MCLOCK_DIV1

    def _mov_a_imm(self, opcode):
        #10 1100 iiii A = IMM; CF 0, SF 1; CC16
        self._A = opcode & 0xF
        self._CF = self._nSF = 0 
        return MCLOCK_DIV1

    def _mov_m1i_a(self, opcode):
        #10 1110 iiii M[1:IMM] = A; CF -, SF 1; CC16
        self._RAM[0x10 | (opcode & 0xF)] = self._A
        self._nSF = 0 
        return MCLOCK_DIV1

    def _bs_imm(self, opcode):
        #11 iiii iiii if SF (PC<7:0> = IMM); CF -, SF 1; CC16
        if (not self._nSF):
            if (self._PCHTMP >= 0):
                self._PC = (self._PCHTMP << 8) | (opcode & 0xFF)
            else:
                self._PC = (self._PC & 0xF00) | (opcode & 0xFF)
        self._PCHTMP = -1
        self._nSF = 0
        return MCLOCK_DIV1
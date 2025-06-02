from .rom import ROM
from .PinTogglingSound import PinTogglingSound

MCLOCK_DIV1 = 2
MCLOCK_DIV2 = 4

RAM_SIZE = 256
GRAM_SIZE = 24
FULL_GRAM = tuple([255] * GRAM_SIZE)

M_INT_T = 0x1
M_INT_0S = 0x2
M_INT_1 = 0x4

P_DISPLAY_MODE = 0xB
P_CLOCK_MODE = 0xC
P_PORT6_MODE = 0xE
P_SHIFT_MODE = 0xF

class D750X():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = PinTogglingSound(clock)

        self._rom_mask = self._ROM.getMask()

        self._instr_counter = 0
        self._cycle_counter = 0
        self._timer_counter = 0

        self._sound_port = mask['sound']['port']
        self._sound_mask = 1 << mask['sound']['pin']

        self._crystal_clock_div = clock / 32768

        self._counter_div = [256, 64 * self._crystal_clock_div, self._crystal_clock_div, self._crystal_clock_div]

        self._reset()

        self._execute = (
            *([(D750X._aisc_data, 1)] * 16),  #0000iiii A <- A + i Skip if overflow; 1; 1 + S
            *([(D750X._lai_data, 1)] * 16),   #0001iiii A <- i; 1; 1
            *([(D750X._jmp_addr, 2)] * 8),    #00100iii iiiiiiii pc10-0 <- i; 2; 2
            *([(D750X._dummy, 1)] * 8),
            *([(D750X._call_addr, 2)] * 8),   #00110iii iiiiiiii SP <- PCm.PCl.PSW.PCh, pc10-0 <- i, SP <- SP - 4; 2; 2
            (D750X._ladr_addr, 2),            #00111000 0iiiiiii A <- (i); 2; 2
            (D750X._xadr, 2),                 #00111001 0iiiiiii A <-> (i); 2; 2
            (D750X._xhdr, 2),                 #00111010 0iiiiiii H <-> (i); 2; 2
            (D750X._xldr, 2),                 #00111011 0iiiiiii L <-> (i); 2; 2
            (D750X._ddrs_addr, 2),            #00111100 0iiiiiii (i) <- (i) - 1; 2; 2 + S
            (D750X._idrs_addr, 2),            #00111101 0iiiiiii (i) <- (i) + 1; 2; 2 + S
            (D750X._instruction_00111110, 2), #00111110
            (D750X._instruction_00111111, 2), #00111111
            (D750X._lam_dl, 1),               #01000000 A <- (DL); 1; 1
            (D750X._lam_de, 1),               #01000001 A <- (DE); 1; 1
            (D750X._dummy, 1),
            (D750X._rtpsw, 1),                #01000011 PCm.PCl.PSW.PCh <- (SP), SP <- SP + 4; 1; 2
            (D750X._xam_dl, 1),               #01000100 A <-> (DL); 1; 1
            (D750X._xam_de, 1),               #01000101 A <-> (DE); 1; 1
            *([(D750X._dummy, 1)] * 2),
            (D750X._des, 1),                  #01001000 E <- E - 1; 1; 1 + S
            (D750X._ies, 1),                  #01001001 E <- E + 1; 1; 1 + S
            (D750X._xad, 1),                  #01001010 A <-> D; 1; 1
            (D750X._xae, 1),                  #01001011 A <-> E; 1; 1
            (D750X._anp_data, 2),             #01001100 iiiiiiii P(i7-4) <- P(i7-4) & i3-0; 2; 2
            (D750X._orp_data, 2),             #01001101 iiiiiiii P(i7-4) <- P(i7-4) | i3-0; 2; 2
            (D750X._lhli_data, 2),            #01001110 iiiiiiii HL <- i; 2; 2
            (D750X._ldei_data, 2),            #01001111 iiiiiiii DE <- i; 2; 2
            (D750X._lam_hld, 1),              #01010000 A <- (HL-); 1; 1 + S
            (D750X._lam_hli, 1),              #01010001 A <- (HL+); 1; 1 + S
            (D750X._lam_hl, 1),               #01010010 A <- (HL); 1; 1
            (D750X._rt, 1),                   #01010011 PCm.PCl.0000.PCh <- (SP), SP <- SP + 4; 1; 1
            (D750X._xam_hld, 1),              #01010100 A <-> (HL-); 1; 1 + S
            (D750X._xam_hli, 1),              #01010101 A <-> (HL+); 1; 1 + S
            (D750X._xam_hl, 1),               #01010110 A <-> (HL); 1; 1
            (D750X._st, 1),                   #01010111 (HL) <- A; 1; 1
            (D750X._dls, 1),                  #01011000 L <- L - 1; 1; 1 + S
            (D750X._ils, 1),                  #01011001 L <- L + 1; 1; 1 + S
            (D750X._skc, 1),                  #01011010 Skip if C = 1; 1; 1 + S
            (D750X._rts, 1),                  #01011011 PCm.PCl.0000.PCh <- (SP), SP <- SP + 4; 1; 1 + S
            *([(D750X._dummy, 1)] * 2),
            (D750X._lamt, 1),                 #01011110 A <- [PC10-6.0.C.A]h, (HL) <- [PC10-6.0.C.A]l; 1; 2
            (D750X._skaem, 1),                #01011111 Skip if A = (HL); 1; 1 + S
            *([(D750X._skmbf_data, 1)] * 4),  #011000ii Skip if (HL)bi = 0; 1; 1 + S
            *([(D750X._skmbt_data, 1)] * 4),  #011001ii Skip if (HL)bi = 1; 1; 1 + S
            *([(D750X._rmb, 1)] * 4),         #011010ii (HL).bi <- 0; 1; 1
            *([(D750X._smb, 1)] * 4),         #011011ii (HL).bi <- 1; 1; 1
            (D750X._ipl, 1),                  #01110000 A <- P(L); 1; 1
            (D750X._ip1, 1),                  #01110001 A <- P1; 1; 1
            (D750X._opl, 1),                  #01110010 P(L) <- A; 1; 1
            (D750X._op3, 1),                  #01110011 P3 <- A; 1; 1
            *([(D750X._skabt_data, 1)] * 4),  #011101ii Skip if Abi = 1; 1; 1 + S
            (D750X._rc, 1),                   #01111000 C <- 0; 1; 1
            (D750X._sc, 1),                   #01111001 C <- 1; 1; 1
            (D750X._xah, 1),                  #01111010 A <-> H; 1; 1
            (D750X._xal, 1),                  #01111011 A <-> L; 1; 1
            (D750X._acsc, 1),                 #01111100 A, C <- A + (HL) + C; 1; 1 + S
            (D750X._asc, 1),                  #01111101 A <- A + (HL); 1; 1 + S
            (D750X._exl, 1),                  #01111110 A <- A xor (HL); 1; 1
            (D750X._cma, 1),                  #01111111 A <- !A; 1; 1
            *([(D750X._jcp_addr, 1)] * 64),   #10iiiiii PC5.0 <- i; 1; 1
            *([(D750X._lhlt_addr, 1)] * 16),  #1100iiii HL <- [0xC0 + i]; 1; 2
            *([(D750X._calt_addr, 1)] * 48),  #11iiiiii (SP) <- PCm.PCl.PSW.PCh, PC <- [0xC0 + i]h.00.[0xC0 + i]l, SP <- SP - 4; 1; 2
        )

        self._instruction_00111110_tbl = (
            *([(D750X._lei_data, 2)] * 16),   #00111110 0000iiii E <- i; 2; 2
            *([(D750X._lli_data, 2)] * 16),   #00111110 0001iiii L <- i; 2; 2
            *([(D750X._ldi_data, 2)] * 16),   #00111110 0010iiii D <- i; 2; 2
            *([(D750X._lhi_data, 2)] * 16),   #00111110 0011iiii H <- i; 2; 2
            *([(D750X._skeei_data, 2)] * 16), #00111110 0100iiii Skip if E = i; 2; 2 + S
            *([(D750X._sklei_data, 2)] * 16), #00111110 0101iiii Skip if L = i; 2; 2 + S
            *([(D750X._skdei_data, 2)] * 16), #00111110 0110iiii Skip if D = i; 2; 2 + S
            *([(D750X._skhei_data, 2)] * 16), #00111110 0111iiii Skip if H = i; 2; 2 + S
            *([(D750X._dummy, 1)] * 10),
            (D750X._tae, 2),                  #00111110 10001010 E <- A; 2; 2
            (D750X._tea, 2),                  #00111110 10001011 A <- E; 2; 2
            *([(D750X._dummy, 1)] * 2),
            (D750X._pshde, 2),                #00111110 10001110 (SP - 1) <- D, (SP - 2) <- E, SP <- SP - 2; 2; 2
            (D750X._popde, 2),                #00111110 10001111 E <- (SP), D <- (SP + 1), SP <- SP + 2; 2; 2
            *([(D750X._dummy, 1)] * 10),
            (D750X._tal, 2),                  #00111110 10011010 L <- A; 2; 2
            (D750X._tla, 2),                  #00111110 10011011 A <- L; 2; 2
            *([(D750X._dummy, 1)] * 2),
            (D750X._pshhl, 2),                #00111110 10011110 (SP - 1) <- H, (SP - 2) <- L, SP <- SP - 2; 2; 2
            (D750X._pophl, 2),                #00111110 10011111 L <- (SP), H <- (SP + 1), SP <- SP + 2; 2; 2
            *([(D750X._dummy, 1)] * 10),
            (D750X._tad, 2),                  #00111110 10101010 D <- A; 2; 2
            (D750X._tda, 2),                  #00111110 10101011 A <- D; 2; 2
            *([(D750X._dummy, 1)] * 14),
            (D750X._tah, 2),                  #00111110 10111010 H <- A; 2; 2
            (D750X._tha, 2),                  #00111110 10111011 A <- H; 2; 2
            *([(D750X._dummy, 1)] * 68),
        )
        
        self._instruction_00111111_tbl = (
            *([(D750X._dummy, 1)] * 16),
            *([(D750X._jam_addr, 2)] * 8),    #00111111 00010iii pc <- D2-0.A.(HL) ; 2; 2
            *([(D750X._dummy, 1)] * 25),
            (D750X._tamsp, 2),                #00111111 00110001 SPh <- A, SP3-1 <- (HL)3-1; 2; 2
            (D750X._timer, 2),                #00111111 00110010 TCRh <- 0, INTtRQF <- 0; 2; 2
            (D750X._sio, 2),                  #00111111 00110011 SIOCR2-0 <- 0, INT0/sRQF <- 0; 2; 2
            (D750X._dummy, 1),
            (D750X._tspam, 2),                #00111111 00110101 A <- SPh, (HL)3-1 <- SP3-1 (HL)0 <- 0; 2; 2
            (D750X._halt, 2),                 #00111111 00110110 Halt; 2; 2
            (D750X._stop, 2),                 #00111111 00110111 Stop; 2; 2
            (D750X._ip54, 2),                 #00111111 00111000 A <- P5, (HL) <- P4; 2; 2
            (D750X._dummy, 1),
            (D750X._tsioam, 2),               #00111111 00111010 A <- SIOh, (HL) <- SIOl; 2; 2
            (D750X._tcntam, 2),               #00111111 00111011 A <- TCRh, (HL) <- TCRl; 2; 2
            (D750X._op54, 2),                 #00111111 00111100 P5 <- A, P4 <- (HL); 2; 2
            (D750X._dummy, 1),
            (D750X._tamsio, 2),               #00111111 00111110 SIOh <- A, SIOl <- (HL); 2; 2
            (D750X._tammod, 2),               #00111111 00111111 TMRh <- A, TMRl <- (HL); 2; 2
            *([(D750X._ski_data, 2)] * 8),    #00111111 01000iii Skip if INTnRQF & i != 0, INTn <- RQF & !i; 2; 2 + S
            *([(D750X._dummy, 1)] * 24),
            *([(D750X._skaei_data, 2)] * 16), #00111111 0110iiii Skip if A = i; 2; 2 + S
            *([(D750X._dummy, 1)] * 16),
            *([(D750X._di_data, 2)] * 8),     #00111111 10000iii IER <- IER & !i, if i = 0, IME <- 0; 2; 2
            *([(D750X._dummy, 1)] * 8),
            *([(D750X._ei_data, 2)] * 8),     #00111111 10010iii IER <- IER | i, if i = 0, IME <- 1; 2; 2
            *([(D750X._dummy, 1)] * 26),
            (D750X._anl, 2),                  #00111111 10110010 A <- A and (HL); 2; 2
            (D750X._rar, 2),                  #00111111 10110011 C >> A >> C; 2; 2
            *([(D750X._dummy, 1)] * 2),
            (D750X._orl, 2),                  #00111111 10110110 A <- A or (HL); 2; 2
            *([(D750X._dummy, 1)] * 9),
            *([(D750X._ip_addr, 2)] * 16),    #00111111 1100iiii A <- P(i); 2; 2
            *([(D750X._dummy, 1)] * 16),
            *([(D750X._op_addr, 2)] * 16),    #00111111 1110iiii P(i) <- A; 2; 2
            *([(D750X._dummy, 1)] * 16),
        )

    def _reset(self):
        self._A = 0
        self._HL = 0
        self._DE = 0
        self._SP = 0
        self._PC = 0

        self._CF = 0
        self._SK = 0
        
        self._HALT = 0
        self._STOP = 0

        self._IER = 0
        self._RQF = 0
        self._IME = 0

        self._P = [0] * 16
        self._SIO = 0
        self._SIOCR = 0
        self._TCR = 0
        self._TMR = 0xFF

        self._RAM = [0] * RAM_SIZE

    def reset(self):
        self._reset()

    def examine(self):
        return {
            "PC": self._PC,
            "A": self._A,
            "HL": self._HL,
            "DE": self._DE,
            "DL": (self._DE & 0xF0) | (self._HL & 0x0F),
            "SP": self._SP,
            "CY": self._CF,
            "IET": self._IER & 0x1,
            "IE0S": self._IER & 0x2,
            "IE1": self._IER & 0x4,
            "IME": self._IME,
            "SIOCR": self._SIOCR,
            "SIO": self._SIO,
            "TCR": self._TCR,
            "TMR": self._TMR,
            "RAM": self._RAM,
            "PORT": self._P
        }

    def edit_state(self, state):
        if ("A" in state):
            self._A = state["A"]
        if ("HL" in state):
            self._HL = state["HL"]
        if ("DE" in state):
            self._DE = state["DE"]
        if ("DL" in state):
            self._DE = (state["DL"] & 0xF0) | (self._DE & 0x0F)
            self._HL = (self._HL & 0xF0) | (state["DL"] & 0x0F)
        if ("CY" in state):
            self._CF = state["CY"]
        if ("IET" in state):
            self._IER = (self._IER & 0xE) | state["IET"]
        if ("IE0S" in state):
            self._IER = (self._IER & 0xD) | (state["IE0S"] << 1)
        if ("IE1" in state):
            self._IER = (self._IER & 0xB) | (state["IE1"] << 2)
        if ("IME" in state):
            self._IME
        if ("SIOCR" in state):
            self._SIOCR = state["SIOCR"]
        if ("SIO" in state):
            self._SIO = state["SIO"]
        if ("TCR" in state):
            self._TCR = state["TCR"]
        if ("TMR" in state):
            self._TMR = state["TMR"]
        if ("PC" in state):
            self._PC = state["PC"] & self._ROM.getMask()
        if ("SP" in state):
            self._SP = state["SP"] & 0xFF
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xF
        if ("PORT" in state):
            for i, value in state["PORT"].items():
                self._P[i] = value & 0xF
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
    
    def pin_set(self, port, pin, level):
        port = int(port)
        self._P[port] = ~(1 << pin) & self._P[port] | level << pin

    def pin_release(self, port, pin):
        port = int(port)
        self._P[port] &= ~(1 << pin)

    def pc(self):
        return self._PC & 0xFFF
    
    def get_VRAM(self):
        return tuple(self._RAM[:GRAM_SIZE])
    
    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter

    def _interrupt(self, addr):
        self._IME = 0
        self._RAM[(self._SP - 1) & 0xFF] = (self._PC >> 4) & 0xF
        self._RAM[(self._SP - 2) & 0xFF] = self._PC & 0xF
        self._RAM[(self._SP - 3) & 0xFF] = (self._SK << 2) | self._CF 
        self._SP = (self._SP - 4) & 0xFF
        self._RAM[self._SP] = (self._PC >> 8) & 0xF
        self._PC = addr

    def clock(self):
        exec_cycles = 1
        if (not (self._HALT or self._STOP)):
            data = opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & self._rom_mask
            if (self._execute[data][1] == 2):
                opcode = (data << 8) | self._ROM.getByte(self._PC)
                self._PC = (self._PC + 1) & self._rom_mask

            exec_cycles = self._execute[data][0](self, opcode)
            self._instr_counter += 1

            if (self._IME):
                if (self._IER & self._RQF & M_INT_T):
                    self._RQF &= ~M_INT_T
                    self._interrupt(0x10)

        if (not(self._STOP) or self._P[P_CLOCK_MODE] > 0):
            self._timer_counter -= exec_cycles
            while (self._timer_counter <= 0):
                self._timer_counter += self._counter_div[self._P[P_CLOCK_MODE] & 0x3]
                self._TCR = (self._TCR + 1) & 0xFF
                if (self._TCR == self._TMR):
                    self._TCR = 0
                    self._RQF |= M_INT_T
                    self._STOP = self._HALT = 0

        self._cycle_counter += exec_cycles
        self._sound.toggle(self._P[self._sound_port] & self._sound_mask, 0, self._cycle_counter)

        return exec_cycles


    def _instruction_00111110(self, opcode):
        #10011001
        return self._instruction_00111110_tbl[opcode & 0xFF][0](self, opcode)
    
    def _instruction_00111111(self, opcode):
        #10011001
        return self._instruction_00111111_tbl[opcode & 0xFF][0](self, opcode)
        
    def _dummy(self, opcode):
        print("undefined instruction", "%0.3X" % self._PC)

    def _skip_next(self):
        opcode = self._ROM.getByte(self._PC)
        byte_count = self._execute[opcode][1]
        self._PC = (self._PC + byte_count) & self._rom_mask
        self._SK = 3
        return byte_count * 2

    def _aisc_data(self, opcode):
        #0000iiii A <- A + i Skip if overflow; 1; 1 + S 
        res = self._A + opcode
        self._A = res & 0xF
        if (res > 15):
            prev = self._ROM.getByte(self._PC - 2)
            if (prev != 0b01111100 or self._CF):   #prev instruction is ACSC
                return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _lai_data(self, opcode):
        #0001iiii A <- i; 1; 1
        self._A = opcode & 0xF
        cycles = MCLOCK_DIV1
        while ((self._ROM.getByte(self._PC) >> 4) == 0b0001):
            self._PC = (self._PC + 1) & self._rom_mask
            cycles += MCLOCK_DIV1
        return cycles

    def _jmp_addr(self, opcode):
        #00100iii iiiiiiii pc10-0 <- i; 2; 2
        self._PC = opcode & 0xFFF
        return MCLOCK_DIV2
        
    def _call_addr(self, opcode):
        #00110iii iiiiiiii SP <- PCm.PCl.PSW.PCh, pc10-0 <- i, SP <- SP - 4; 2; 2
        self._RAM[(self._SP - 1) & 0xFF] = (self._PC >> 4) & 0xF
        self._RAM[(self._SP - 2) & 0xFF] = self._PC & 0xF
        self._RAM[(self._SP - 3) & 0xFF] = (self._SK << 2) | self._CF 
        self._SP = (self._SP - 4) & 0xFF
        self._RAM[self._SP] = (self._PC >> 8) & 0xF
        self._PC = opcode & 0x7FF
        return MCLOCK_DIV2

    def _ladr_addr(self, opcode):
        #00111000 0iiiiiii A <- (i); 2; 2
        self._A = self._RAM[opcode & 0x7F]
        return MCLOCK_DIV2

    def _xadr(self, opcode):
        #00111001 0iiiiiii A <-> (i); 2; 2
        new_A = self._RAM[opcode & 0x7F]
        self._RAM[opcode & 0x7F] = self._A
        self._A = new_A
        return MCLOCK_DIV2

    def _xhdr(self, opcode):
        #00111010 0iiiiiii H <-> (i); 2; 2
        new_H = self._RAM[opcode & 0x7F]
        self._RAM[opcode & 0x7F] = self._HL >> 4
        self._HL = (new_H << 4) | (self._HL & 0x0F)
        return MCLOCK_DIV2

    def _xldr(self, opcode):
        #00111011 0iiiiiii L <-> (i); 2; 2
        new_L = self._RAM[opcode & 0x7F]
        self._RAM[opcode & 0x7F] = self._HL & 0xF
        self._HL = (self._HL & 0xF0) | new_L
        return MCLOCK_DIV2

    def _ddrs_addr(self, opcode):
        #00111100 0iiiiiii (i) <- (i) - 1; 2; 2 + S
        res = self._RAM[opcode & 0x7F] = (self._RAM[opcode & 0x7F] - 1) & 0xF
        if (res == 0xF):
            return MCLOCK_DIV2 + self._skip_next()
        return MCLOCK_DIV2

    def _idrs_addr(self, opcode):
        #00111101 0iiiiiii (i) <- (i) + 1; 2; 2 + S
        res = self._RAM[opcode & 0x7F] = (self._RAM[opcode & 0x7F] + 1) & 0xF
        if (res == 0):
            return MCLOCK_DIV2 + self._skip_next()
        return MCLOCK_DIV2
            
    def _lei_data(self, opcode):
        #00111110 0000iiii E <- i; 2; 2
        self._DE = (self._DE & 0xF0) | (opcode & 0xF)
        return MCLOCK_DIV2

    def _lli_data(self, opcode):
        #00111110 0001iiii L <- i; 2; 2
        self._HL = (self._HL & 0xF0) | (opcode & 0xF)
        return MCLOCK_DIV2

    def _ldi_data(self, opcode):
        #00111110 0010iiii D <- i; 2; 2
        self._DE = ((opcode & 0xF) << 4) | (self._DE & 0x0F)
        return MCLOCK_DIV2

    def _lhi_data(self, opcode):
        #00111110 0011iiii H <- i; 2; 2
        self._HL = ((opcode & 0xF) << 4) | (self._HL & 0x0F)
        return MCLOCK_DIV2

    def _skeei_data(self, opcode):
        #00111110 0100iiii Skip if E = i; 2; 2 + S
        if ((self._DE & 0x0F) == (opcode & 0xF)):
            return MCLOCK_DIV2 + self._skip_next()
        return MCLOCK_DIV2

    def _sklei_data(self, opcode):
        #00111110 0101iiii Skip if L = i; 2; 2 + S
        if ((self._HL & 0x0F) == (opcode & 0xF)):
            return MCLOCK_DIV2 + self._skip_next()
        return MCLOCK_DIV2

    def _skdei_data(self, opcode):
        #00111110 0110iiii Skip if D = i; 2; 2 + S
        if ((self._DE >> 4) == (opcode & 0xF)):
            return MCLOCK_DIV2 + self._skip_next()
        return MCLOCK_DIV2

    def _skhei_data(self, opcode):
        #00111110 0111iiii Skip if H = i; 2; 2 + S
        if ((self._HL >> 4) == (opcode & 0xF)):
            return MCLOCK_DIV2 + self._skip_next()
        return MCLOCK_DIV2

    def _tae(self, opcode):
        #00111110 10001010 E <- A; 2; 2
        self._DE = (self._DE & 0xF0) | self._A
        return MCLOCK_DIV2

    def _pshde(self, opcode):
        #00111110 10001110 (SP - 1) <- D, (SP - 2) <- E, SP <- SP - 2; 2; 2
        self._RAM[(self._SP - 1) & 0xFF] = self._DE >> 4
        self._SP = (self._SP - 2) & 0xFF
        self._RAM[self._SP] = self._DE & 0x0F
        return MCLOCK_DIV2

    def _popde(self, opcode):
        #00111110 10001111 E <- (SP), D <- (SP + 1), SP <- SP + 2; 2; 2
        self._DE = (self._RAM[(self._SP + 1) & 0xFF] << 4) | self._RAM[self._SP]
        self._SP = (self._SP + 2) & 0xFF
        return MCLOCK_DIV2

    def _tea(self, opcode):
        #00111110 10001011 A <- E; 2; 2
        self._A = self._DE & 0x0F
        return MCLOCK_DIV2

    def _tal(self, opcode):
        #00111110 10011010 L <- A; 2; 2
        self._HL = (self._HL & 0xF0) | self._A
        return MCLOCK_DIV2

    def _tla(self, opcode):
        #00111110 10011011 A <- L; 2; 2
        self._A = self._HL & 0x0F
        return MCLOCK_DIV2

    def _pshhl(self, opcode):
        #00111110 10011110 (SP - 1) <- H, (SP - 2) <- L, SP <- SP - 2; 2; 2
        self._RAM[(self._SP - 1) & 0xFF] = self._HL >> 4
        self._SP = (self._SP - 2) & 0xFF
        self._RAM[self._SP] = self._HL & 0xF
        return MCLOCK_DIV2

    def _pophl(self, opcode):
        #00111110 10011111 L <- (SP), H <- (SP + 1), SP <- SP + 2; 2; 2
        self._HL = (self._RAM[(self._SP + 1) & 0xFF] << 4) | self._RAM[self._SP]
        self._SP = (self._SP + 2) & 0xFF
        return MCLOCK_DIV2

    def _tad(self, opcode):
        #00111110 10101010 D <- A; 2; 2
        self._DE = (self._A << 4) | (self._DE & 0x0F)
        return MCLOCK_DIV2

    def _tda(self, opcode):
        #00111110 10101011 A <- D; 2; 2
        self._A = self._DE >> 4
        return MCLOCK_DIV2

    def _tah(self, opcode):
        #00111110 10111010 H <- A; 2; 2
        self._HL = (self._A << 4) | (self._HL & 0x0F)
        return MCLOCK_DIV2

    def _tha(self, opcode):
        #00111110 10111011 A <- H; 2; 2
        self._A = self._HL >> 4
        return MCLOCK_DIV2

    def _jam_addr(self, opcode):
        #00111111 00010iii pc <- D2-0.A.(HL) ; 2; 2
        self._PC = ((opcode & 0x7) << 8) | (self._A << 4) | self._RAM[self._HL]
        return MCLOCK_DIV2

    def _tamsp(self, opcode):
        #00111111 00110001 SPh <- A, SP3-1 <- (HL)3-1; 2; 2
        self._SP = ((self._A << 4) | self._RAM[self._HL]) & 0xF7
        return MCLOCK_DIV2

    def _tspam(self, opcode):
        #00111111 00110101 A <- SPh, (HL)3-1 <- SP3-1 (HL)0 <- 0; 2; 2
        self._A = (self._SP >> 4)
        self._RAM[self._HL] = self._SP & 0xE
        return MCLOCK_DIV2

    def _halt(self, opcode):
        #00111111 00110110 Halt; 2; 2
        self._HALT = 1
        return MCLOCK_DIV2

    def _stop(self, opcode):
        #00111111 00110111 Stop; 2; 2
        self._STOP = 1
        return MCLOCK_DIV2

    def _timer(self, opcode):
        #00111111 00110010 TCR <- 0, INTtRQF <- 0; 2; 2
        self._TCR = 0
        self._RQF &= ~M_INT_T
        return MCLOCK_DIV2

    def _sio(self, opcode):
        #00111111 00110011 SIOCR2-0 <- 0, INT0/sRQF <- 0; 2; 2
        self._SIOCR = 0
        self._RQF &= ~M_INT_0S
        return MCLOCK_DIV2

    def _tsioam(self, opcode):
        #00111111 00111010 A <- SIOh, (HL) <- SIOl; 2; 2
        self._RAM[self._HL] = self._SIO & 0xF
        self._A = self._SIO >> 4
        return MCLOCK_DIV2

    def _tcntam(self, opcode):
        #00111111 00111011 A <- TCRh, (HL) <- TCRl; 2; 2
        self._A = self._TCR >> 4
        self._RAM[self._HL] = self._TCR & 0xF
        return MCLOCK_DIV2

    def _tamsio(self, opcode):
        #00111111 00111110 SIOh <- A, SIOl <- (HL); 2; 2
        self._SIO = (self._A << 4) | self._RAM[self._HL]
        return MCLOCK_DIV2

    def _tammod(self, opcode):
        #00111111 00111111 TMRh <- A, TMRl <- (HL); 2; 2
        self._TMR = (self._A << 4) | self._RAM[self._HL]
        return MCLOCK_DIV2

    def _ski_data(self, opcode):
        #00111111 01000iii Skip if INTnRQF & i != 0, INTn <- RQF & !i; 2; 2 + S
        if (self._RQF & opcode):
            self._RQF &= ~opcode
            return MCLOCK_DIV2 + self._skip_next()
        return MCLOCK_DIV2

    def _skaei_data(self, opcode):
        #00111111 0110iiii Skip if A = i; 2; 2 + S
        if (self._A == (opcode & 0xF)):
            return MCLOCK_DIV2 + self._skip_next()
        return MCLOCK_DIV2

    def _ip54(self, opcode):
        #00111111 00111000 A <- P5, (HL) <- P4; 2; 2
        self._A = self._P[5]
        self._RAM[self._HL] = self._P[4]
        return MCLOCK_DIV2

    def _op54(self, opcode):
        #00111111 00111100 P5 <- A, P4 <- (HL); 2; 2
        self._P[5] = self._A
        self._P[4] = self._RAM[self._HL]
        return MCLOCK_DIV2

    def _anl(self, opcode):
        #00111111 10110010 A <- A and (HL); 2; 2
        self._A &= self._RAM[self._HL]
        return MCLOCK_DIV2

    def _rar(self, opcode):
        #00111111 10110011 C >> A >> C; 2; 2
        cf = self._A & 0x1
        self._A = (self._CF << 3) | (self._A >> 1)
        self._CF = cf
        return MCLOCK_DIV2

    def _orl(self, opcode):
        #00111111 10110110 A <- A or (HL); 2; 2
        self._A |= self._RAM[self._HL]
        return MCLOCK_DIV2

    def _ip_addr(self, opcode):
        #00111111 1100iiii A <- P(i); 2; 2
        self._A = self._P[opcode & 0xF]
        return MCLOCK_DIV2

    def _op_addr(self, opcode):
        #00111111 1110iiii P(i) <- A; 2; 2
        self._P[opcode & 0xF] = self._A
        return MCLOCK_DIV2

    def _di_data(self, opcode):
        #00111111 10000iii IER <- IER & !i, if i = 0, IME <- 0; 2; 2
        if (opcode & 0x7 == 0):
            self._IME = 0
        else:
            self._IER &= ~opcode
        return MCLOCK_DIV2

    def _ei_data(self, opcode):
        #00111111 10010iii IER <- IER | i, if i = 0, IME <- 1; 2; 2
        self._IER |= opcode & 0x7
        if (opcode & 0x7 == 0):
            self._IME = 1
        return MCLOCK_DIV2
            
    def _lam_dl(self, opcode):
        #01000000 A <- (DL); 1; 1
        self._A = self._RAM[(self._DE & 0xF0) | (self._HL & 0x0F)]
        return MCLOCK_DIV1

    def _lam_de(self, opcode):
        #01000001 A <- (DE); 1; 1
        self._A = self._RAM[self._DE]
        return MCLOCK_DIV1

    def _rtpsw(self, opcode):
        #01000011 PCm.PCl.PSW.PCh <- (SP), SP <- SP + 4; 1; 2
        self._PC = self._RAM[self._SP] << 8
        psw = self._RAM[(self._SP + 1) & 0xFF]
        self._CF = psw & 0x1
        self._SK = psw >> 2
        self._PC |= self._RAM[(self._SP + 2) & 0xFF]
        self._PC |= self._RAM[(self._SP + 3) & 0xFF] << 4
        self._SP = (self._SP + 4) & 0xFF
        return MCLOCK_DIV2
        
    def _xam_dl(self, opcode):
        #01000100 A <-> (DL); 1; 1
        dl = (self._DE & 0xF0) | (self._HL & 0x0F)
        a = self._RAM[dl]
        self._RAM[dl] = self._A
        self._A = a
        return MCLOCK_DIV1
        
    def _xam_de(self, opcode):
        #01000101 A <-> (DE); 1; 1
        a = self._RAM[self._DE]
        self._RAM[self._DE] = self._A
        self._A = a
        return MCLOCK_DIV1
        
    def _des(self, opcode):
        #01001000 E <- E - 1; 1; 1 + S
        self._DE = (self._DE & 0xF0) | ((self._DE - 1) & 0x0F)
        if (self._DE & 0x0F == 0xF):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1
        
    def _ies(self, opcode):
        #01001001 E <- E + 1; 1; 1 + S
        self._DE = (self._DE & 0xF0) | ((self._DE + 1) & 0x0F)
        if (self._DE & 0x0F == 0):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1
        
    def _xad(self, opcode):
        #01001010 A <-> D; 1; 1
        a = self._DE >> 4
        self._DE = (self._A << 4) | (self._DE & 0x0F)
        self._A = a
        return MCLOCK_DIV1
        
    def _xae(self, opcode):
        #01001011 A <-> E; 1; 1
        a = self._DE & 0x0F
        self._DE = (self._DE & 0xF0) | self._A
        self._A = a
        return MCLOCK_DIV1
        
    def _anp_data(self, opcode):
        #01001100 iiiiiiii P(i7-4) <- P(i7-4) & i3-0; 2; 2
        self._P[(opcode >> 4) & 0xF] &= opcode
        return MCLOCK_DIV2
        
    def _orp_data(self, opcode):
        #01001101 iiiiiiii P(i7-4) <- P(i7-4) | i3-0; 2; 2
        self._P[(opcode >> 4) & 0xF] |= opcode & 0xF
        return MCLOCK_DIV2

    def _lhli_data(self, opcode):
        #01001110 iiiiiiii HL <- i; 2; 2
        self._HL = opcode & 0xFF
        cycles = MCLOCK_DIV2
        opcode = self._ROM.getByte(self._PC)
        while (opcode == 0b01001110 or (opcode >> 4) == 0b1100):
            cycles += self._skip_next()
            opcode = self._ROM.getByte(self._PC)
        return cycles

    def _ldei_data(self, opcode):
        #01001111 iiiiiiii DE <- i; 2; 2
        self._DE = opcode & 0xFF
        return MCLOCK_DIV2

    def _lam_hld(self, opcode):
        #01010000 A <- (HL-); 1; 1 + S
        self._A = self._RAM[self._HL]
        self._HL = (self._HL & 0xF0) | ((self._HL - 1) & 0x0F)
        if (self._HL & 0x0F == 0x0F):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _lam_hli(self, opcode):
        #01010001 A <- (HL+); 1; 1 + S
        self._A = self._RAM[self._HL]
        self._HL = (self._HL & 0xF0) | ((self._HL + 1) & 0x0F)
        if (self._HL & 0x0F == 0):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _lam_hl(self, opcode):
        #01010010 A <- (HL); 1; 1
        self._A = self._RAM[self._HL]
        return MCLOCK_DIV1

    def _rt(self, opcode):
        #01010011 PCm.PCl.0000.PCh <- (SP), SP <- SP + 4; 1; 1
        self._PC = self._RAM[self._SP] << 8
        self._PC |= self._RAM[(self._SP + 2) & 0xFF]
        self._PC |= self._RAM[(self._SP + 3) & 0xFF] << 4
        self._SP = (self._SP + 4) & 0xFF
        return MCLOCK_DIV1

    def _xam_hld(self, opcode):
        #01010100 A <-> (HL-); 1; 1 + S
        a = self._RAM[self._HL]
        self._RAM[self._HL] = self._A
        self._A = a
        self._HL = (self._HL & 0xF0) | ((self._HL - 1) & 0x0F)
        if ((self._HL & 0x0F) == 0x0F):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _xam_hli(self, opcode):
        #01010101 A <-> (HL+); 1; 1 + S
        a = self._RAM[self._HL]
        self._RAM[self._HL] = self._A
        self._A = a
        self._HL = (self._HL & 0xF0) | ((self._HL + 1) & 0x0F)
        if (self._HL & 0x0F == 0):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _xam_hl(self, opcode):
        #01010110 A <-> (HL); 1; 1
        a = self._RAM[self._HL]
        self._RAM[self._HL] = self._A
        self._A = a
        return MCLOCK_DIV1

    def _st(self, opcode):
        #01010111 (HL) <- A; 1; 1
        self._RAM[self._HL] = self._A
        return MCLOCK_DIV1

    def _dls(self, opcode):
        #01011000 L <- L - 1; 1; 1 + S
        self._HL = (self._HL & 0xF0) | ((self._HL - 1) & 0x0F)
        if ((self._HL & 0xF) == 0xF):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _ils(self, opcode):
        #01011001 L <- L + 1; 1; 1 + S
        self._HL = (self._HL & 0xF0) | ((self._HL + 1) & 0x0F)
        if ((self._HL & 0xF) == 0):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _skc(self, opcode):
        #01011010 Skip if C = 1; 1; 1 + S
        if (self._CF):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _rts(self, opcode):
        #01011011 PCm.PCl.0000.PCh <- (SP), SP <- SP + 4; 1; 1 + S
        self._PC = self._RAM[self._SP] << 8
        self._PC |= self._RAM[(self._SP + 2) & 0xFF]
        self._PC |= self._RAM[(self._SP + 3) & 0xFF] << 4
        self._SP = (self._SP + 4) & 0xFF
        return MCLOCK_DIV1 + self._skip_next()
        
    def _lamt(self, opcode):
        #01011110 A <- [PC10-6.0.C.A]h, (HL) <- [PC10-6.0.C.A]l; 1; 2
        data = self._ROM.getByte((self._PC & 0x7C0) | (self._CF << 4) | self._A)
        self._A = data >> 4
        self._RAM[self._HL] = data & 0xF
        return MCLOCK_DIV2

    def _skaem(self, opcode):
        #01011111 Skip if A = (HL); 1; 1 + S
        if (self._A == self._RAM[self._HL]):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _skmbf_data(self, opcode):
        #011000ii Skip if (HL)bi = 0; 1; 1 + S
        if ((self._RAM[self._HL] & (1 << (opcode & 0x3))) == 0):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _skmbt_data(self, opcode):
        #011001ii Skip if (HL)bi = 1; 1; 1 + S
        if (self._RAM[self._HL] & (1 << (opcode & 0x3))):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _rmb(self, opcode):
        #011010ii (HL).bi <- 0; 1; 1
        self._RAM[self._HL] &= ~(1 << (opcode & 0x3))
        return MCLOCK_DIV1

    def _smb(self, opcode):
        #011011ii (HL).bi <- 1; 1; 1
        self._RAM[self._HL] |= 1 << (opcode & 0x3)
        return MCLOCK_DIV1

    def _ipl(self, opcode):
        #01110000 A <- P(L); 1; 1
        self._A = self._P[self._HL & 0xF]
        return MCLOCK_DIV1

    def _ip1(self, opcode):
        #01110001 A <- P1; 1; 1
        self._A = self._P[1]
        return MCLOCK_DIV1

    def _opl(self, opcode):
        #01110010 P(L) <- A; 1; 1
        self._P[self._HL & 0xF] = self._A
        return MCLOCK_DIV1

    def _op3(self, opcode):
        #01110011 P3 <- A; 1; 1
        self._P[3] = self._A
        return MCLOCK_DIV1

    def _skabt_data(self, opcode):
        #011101ii Skip if Abi = 1; 1; 1 + S
        if (self._A & (1 << (opcode & 0x3))):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _rc(self, opcode):
        #01111000 C <- 0; 1; 1
        self._CF = 0
        return MCLOCK_DIV1
        
    def _sc(self, opcode):
        #01111001 C <- 1; 1; 1
        self._CF = 1
        return MCLOCK_DIV1

    def _xah(self, opcode):
        #01111010 A <-> H; 1; 1
        a = self._HL >> 4
        self._HL = (self._A << 4) | (self._HL & 0x0F)
        self._A = a
        return MCLOCK_DIV1

    def _xal(self, opcode):
        #01111011 A <-> L; 1; 1
        a = self._HL & 0xF
        self._HL = (self._HL & 0xF0) | self._A
        self._A = a
        return MCLOCK_DIV1

    def _acsc(self, opcode):
        #01111100 A, C <- A + (HL) + C; 1; 1 + S
        res = self._A + self._RAM[self._HL] + self._CF
        self._A = res & 0xF
        if (res > 0xF):
            self._CF = 1
            return MCLOCK_DIV1 + self._skip_next()
        self._CF = 0
        return MCLOCK_DIV1

    def _asc(self, opcode):
        #01111101 A <- A + (HL); 1; 1 + S
        res = self._A + self._RAM[self._HL]
        self._A = res & 0xF
        if (res > 0xF):
            return MCLOCK_DIV1 + self._skip_next()
        return MCLOCK_DIV1

    def _exl(self, opcode):
        #01111110 A <- A xor (HL); 1; 1
        self._A ^= self._RAM[self._HL]
        return MCLOCK_DIV1

    def _cma(self, opcode):
        #01111111 A <- !A; 1; 1
        self._A ^= 0xF
        return MCLOCK_DIV1

    def _jcp_addr(self, opcode):
        #10iiiiii PC5.0 <- i; 1; 1
        self._PC = (self._PC & 0x7C0) | (opcode & 0x3F)
        return MCLOCK_DIV1

    def _lhlt_addr(self, opcode):
        #1100iiii HL <- [0xC0 + i]; 1; 2
        self._HL = self._ROM.getByte(0xC0 | (opcode & 0xF))
        cycles = MCLOCK_DIV2
        opcode = self._ROM.getByte(self._PC)
        while (opcode == 0b01001110 or (opcode >> 4) == 0b1100):
            cycles += self._skip_next()
            opcode = self._ROM.getByte(self._PC)
        return cycles

    def _calt_addr(self, opcode):
        #11iiiiii (SP) <- PCm.PCl.PSW.PCh, PC <- [0xC0 + i]h.00.[0xC0 + i]l, SP <- SP - 4; 1; 2
        self._RAM[(self._SP - 1) & 0xFF] = (self._PC >> 4) & 0xF
        self._RAM[(self._SP - 2) & 0xFF] = self._PC & 0xF
        self._RAM[(self._SP - 3) & 0xFF] = (self._SK << 2) | self._CF 
        self._SP = (self._SP - 4) & 0xFF
        self._RAM[self._SP] = (self._PC >> 8) & 0xF
        tdata = self._ROM.getByte(opcode)
        self._PC = ((tdata << 2) & 0x380) | (tdata & 0x1F)
        return MCLOCK_DIV2
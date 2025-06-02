class D750Xdasm():

    def __init__(self):
        self._addrbase = '%0.3X'
        self._opbase = '%0.3X'
        
        self.last_call = 0

        self._instruction_tbl = (
            *([(D750Xdasm._aisc_data, 1)] * 16),  #0000iiii A <- A + i Skip if overflow; 1; 1 + S
            *([(D750Xdasm._lai_data, 1)] * 16),   #0001iiii A <- i; 1; 1
            *([(D750Xdasm._jmp_addr, 2)] * 8),    #00100iii iiiiiiii pc10-0 <- i; 2; 2
            *([(D750Xdasm._dummy, 1)] * 8),
            *([(D750Xdasm._call_addr, 2)] * 8),   #00110iii iiiiiiii SP <- PCm.PCl.PSW.PCh, pc10-0 <- i, SP <- SP - 4; 2; 2
            (D750Xdasm._ladr_addr, 2),            #00111000 0iiiiiii A <- (i); 2; 2
            (D750Xdasm._xadr, 2),                 #00111001 0iiiiiii A <-> (i); 2; 2
            (D750Xdasm._xhdr, 2),                 #00111010 0iiiiiii H <-> (i); 2; 2
            (D750Xdasm._xldr, 2),                 #00111011 0iiiiiii L <-> (i); 2; 2
            (D750Xdasm._ddrs_addr, 2),            #00111100 0iiiiiii (i) <- (i) - 1; 2; 2 + S
            (D750Xdasm._idrs_addr, 2),            #00111101 0iiiiiii (i) <- (i) + 1; 2; 2 + S
            (D750Xdasm._instruction_00111110, 2), #00111110
            (D750Xdasm._instruction_00111111, 2), #00111111
            (D750Xdasm._lam_dl, 1),               #01000000 A <- (DL); 1; 1
            (D750Xdasm._lam_de, 1),               #01000001 A <- (DE); 1; 1
            (D750Xdasm._dummy, 1),
            (D750Xdasm._rtpsw, 1),                #01000011 PCm.PCl.PSW.PCh <- (SP), SP <- SP + 4; 1; 2
            (D750Xdasm._xam_dl, 1),               #01000100 A <-> (DL); 1; 1
            (D750Xdasm._xam_de, 1),               #01000101 A <-> (DE); 1; 1
            *([(D750Xdasm._dummy, 1)] * 2),
            (D750Xdasm._des, 1),                  #01001000 E <- E - 1; 1; 1 + S
            (D750Xdasm._ies, 1),                  #01001001 E <- E + 1; 1; 1 + S
            (D750Xdasm._xad, 1),                  #01001010 A <-> D; 1; 1
            (D750Xdasm._xae, 1),                  #01001011 A <-> E; 1; 1
            (D750Xdasm._anp_data, 2),             #01001100 iiiiiiii P(i7-4) <- P(i7-4) & i3-0; 2; 2
            (D750Xdasm._orp_data, 2),             #01001101 iiiiiiii P(i7-4) <- P(i7-4) | i3-0; 2; 2
            (D750Xdasm._lhli_data, 2),            #01001110 iiiiiiii HL <- i; 2; 2
            (D750Xdasm._ldei_data, 2),            #01001111 iiiiiiii DE <- i; 2; 2
            (D750Xdasm._lam_hld, 1),              #01010000 A <- (HL-); 1; 1 + S
            (D750Xdasm._lam_hli, 1),              #01010001 A <- (HL+); 1; 1 + S
            (D750Xdasm._lam_hl, 1),               #01010010 A <- (HL); 1; 1
            (D750Xdasm._rt, 1),                   #01010011 PCm.PCl.0000.PCh <- (SP), SP <- SP + 4; 1; 1
            (D750Xdasm._xam_hld, 1),              #01010100 A <-> (HL-); 1; 1 + S
            (D750Xdasm._xam_hli, 1),              #01010101 A <-> (HL+); 1; 1 + S
            (D750Xdasm._xam_hl, 1),               #01010110 A <-> (HL); 1; 1
            (D750Xdasm._st, 1),                   #01010111 (HL) <- A; 1; 1
            (D750Xdasm._dls, 1),                  #01011000 L <- L - 1; 1; 1 + S
            (D750Xdasm._ils, 1),                  #01011001 L <- L + 1; 1; 1 + S
            (D750Xdasm._skc, 1),                  #01011010 Skip if C = 1; 1; 1 + S
            (D750Xdasm._rts, 1),                  #01011011 PCm.PCl.0000.PCh <- (SP), SP <- SP + 4; 1; 1 + S
            *([(D750Xdasm._dummy, 1)] * 2),
            (D750Xdasm._lamt, 1),                 #01011110 A <- [PC10-6.0.C.A]h, (HL) <- [PC10-6.0.C.A]l; 1; 2
            (D750Xdasm._skaem, 1),                #01011111 Skip if A = (HL); 1; 1 + S
            *([(D750Xdasm._skmbf_data, 1)] * 4),  #011000ii Skip if (HL)bi = 0; 1; 1 + S
            *([(D750Xdasm._skmbt_data, 1)] * 4),  #011001ii Skip if (HL)bi = 1; 1; 1 + S
            *([(D750Xdasm._rmb, 1)] * 4),         #011010ii (HL).bi <- 0; 1; 1
            *([(D750Xdasm._smb, 1)] * 4),         #011011ii (HL).bi <- 1; 1; 1
            (D750Xdasm._ipl, 1),                  #01110000 A <- P(L); 1; 1
            (D750Xdasm._ip1, 1),                  #01110001 A <- P1; 1; 1
            (D750Xdasm._opl, 1),                  #01110010 P(L) <- A; 1; 1
            (D750Xdasm._op3, 1),                  #01110011 P3 <- A; 1; 1
            *([(D750Xdasm._skabt_data, 1)] * 4),  #011101ii Skip if Abi = 1; 1; 1 + S
            (D750Xdasm._rc, 1),                   #01111000 C <- 0; 1; 1
            (D750Xdasm._sc, 1),                   #01111001 C <- 1; 1; 1
            (D750Xdasm._xah, 1),                  #01111010 A <-> H; 1; 1
            (D750Xdasm._xal, 1),                  #01111011 A <-> L; 1; 1
            (D750Xdasm._acsc, 1),                 #01111100 A, C <- A + (HL) + C; 1; 1 + S
            (D750Xdasm._asc, 1),                  #01111101 A <- A + (HL); 1; 1 + S
            (D750Xdasm._exl, 1),                  #01111110 A <- A xor (HL); 1; 1
            (D750Xdasm._cma, 1),                  #01111111 A <- !A; 1; 1
            *([(D750Xdasm._jcp_addr, 1)] * 64),   #10iiiiii PC5.0 <- i; 1; 1
            *([(D750Xdasm._lhlt_addr, 1)] * 16),  #1100iiii HL <- [0xC0 + i]; 1; 2
            *([(D750Xdasm._calt_addr, 1)] * 48),  #11iiiiii (SP) <- PCm.PCl.PSW.PCh, PC <- [0xC0 + i]h.00.[0xC0 + i]l, SP <- SP - 4; 1; 2
        )

        self._instruction_00111110_tbl = (
            *([(D750Xdasm._lei_data, 2)] * 16),   #00111110 0000iiii E <- i; 2; 2
            *([(D750Xdasm._lli_data, 2)] * 16),   #00111110 0001iiii L <- i; 2; 2
            *([(D750Xdasm._ldi_data, 2)] * 16),   #00111110 0010iiii D <- i; 2; 2
            *([(D750Xdasm._lhi_data, 2)] * 16),   #00111110 0011iiii H <- i; 2; 2
            *([(D750Xdasm._skeei_data, 2)] * 16), #00111110 0100iiii Skip if E = i; 2; 2 + S
            *([(D750Xdasm._sklei_data, 2)] * 16), #00111110 0101iiii Skip if L = i; 2; 2 + S
            *([(D750Xdasm._skdei_data, 2)] * 16), #00111110 0110iiii Skip if D = i; 2; 2 + S
            *([(D750Xdasm._skhei_data, 2)] * 16), #00111110 0111iiii Skip if H = i; 2; 2 + S
            *([(D750Xdasm._dummy, 1)] * 10),
            (D750Xdasm._tae, 2),                  #00111110 10001010 E <- A; 2; 2
            (D750Xdasm._tea, 2),                  #00111110 10001011 A <- E; 2; 2
            *([(D750Xdasm._dummy, 1)] * 2),
            (D750Xdasm._pshde, 2),                #00111110 10001110 (SP - 1) <- D, (SP - 2) <- E, SP <- SP - 2; 2; 2
            (D750Xdasm._popde, 2),                #00111110 10001111 E <- (SP), D <- (SP + 1), SP <- SP + 2; 2; 2
            *([(D750Xdasm._dummy, 1)] * 10),
            (D750Xdasm._tal, 2),                  #00111110 10011010 L <- A; 2; 2
            (D750Xdasm._tla, 2),                  #00111110 10011011 A <- L; 2; 2
            *([(D750Xdasm._dummy, 1)] * 2),
            (D750Xdasm._pshhl, 2),                #00111110 10011110 (SP - 1) <- H, (SP - 2) <- L, SP <- SP - 2; 2; 2
            (D750Xdasm._pophl, 2),                #00111110 10011111 L <- (SP), H <- (SP + 1), SP <- SP + 2; 2; 2
            *([(D750Xdasm._dummy, 1)] * 10),
            (D750Xdasm._tad, 2),                  #00111110 10101010 D <- A; 2; 2
            (D750Xdasm._tda, 2),                  #00111110 10101011 A <- D; 2; 2
            *([(D750Xdasm._dummy, 1)] * 14),
            (D750Xdasm._tah, 2),                  #00111110 10111010 H <- A; 2; 2
            (D750Xdasm._tha, 2),                  #00111110 10111011 A <- H; 2; 2
            *([(D750Xdasm._dummy, 1)] * 68),
        )
        
        self._instruction_00111111_tbl = (
            *([(D750Xdasm._dummy, 1)] * 16),
            *([(D750Xdasm._jam_addr, 2)] * 8),    #00111111 00010iii pc <- D2-0.A.(HL) ; 2; 2
            *([(D750Xdasm._dummy, 1)] * 25),
            (D750Xdasm._tamsp, 2),                #00111111 00110001 SPh <- A, SP3-1 <- (HL)3-1; 2; 2
            (D750Xdasm._timer, 2),                #00111111 00110010 TCRh <- 0, INTtRQF <- 0; 2; 2
            (D750Xdasm._sio, 2),                  #00111111 00110011 SIOCR2-0 <- 0, INT0/sRQF <- 0; 2; 2
            (D750Xdasm._dummy, 1),
            (D750Xdasm._tspam, 2),                #00111111 00110101 A <- SPh, (HL)3-1 <- SP3-1 (HL)0 <- 0; 2; 2
            (D750Xdasm._halt, 2),                 #00111111 00110110 Halt; 2; 2
            (D750Xdasm._stop, 2),                 #00111111 00110111 Stop; 2; 2
            (D750Xdasm._ip54, 2),                 #00111111 00111000 A <- P5, (HL) <- P4; 2; 2
            (D750Xdasm._dummy, 1),
            (D750Xdasm._tsioam, 2),               #00111111 00111010 A <- SIOh, (HL) <- SIOl; 2; 2
            (D750Xdasm._tcntam, 2),               #00111111 00111011 A <- TCRh, (HL) <- TCRl; 2; 2
            (D750Xdasm._op54, 2),                 #00111111 00111100 P5 <- A, P4 <- (HL); 2; 2
            (D750Xdasm._dummy, 1),
            (D750Xdasm._tamsio, 2),               #00111111 00111110 SIOh <- A, SIOl <- (HL); 2; 2
            (D750Xdasm._tammod, 2),               #00111111 00111111 TMRh <- A, TMRl <- (HL); 2; 2
            *([(D750Xdasm._ski_data, 2)] * 8),    #00111111 01000iii Skip if INTnRQF & i != 0, INTn <- RQF & !i; 2; 2 + S
            *([(D750Xdasm._dummy, 1)] * 24),
            *([(D750Xdasm._skaei_data, 2)] * 16), #00111111 0110iiii Skip if A = i; 2; 2 + S
            *([(D750Xdasm._dummy, 1)] * 16),
            *([(D750Xdasm._di_data, 2)] * 8),     #00111111 10000iii IER <- IER & !i, if i = 0, IME <- 0; 2; 2
            *([(D750Xdasm._dummy, 1)] * 8),
            *([(D750Xdasm._ei_data, 2)] * 8),     #00111111 10010iii IER <- IER | i, if i = 0, IME <- 1; 2; 2
            *([(D750Xdasm._dummy, 1)] * 26),
            (D750Xdasm._anl, 2),                  #00111111 10110010 A <- A and (HL); 2; 2
            (D750Xdasm._rar, 2),                  #00111111 10110011 C >> A >> C; 2; 2
            *([(D750Xdasm._dummy, 1)] * 2),
            (D750Xdasm._orl, 2),                  #00111111 10110110 A <- A or (HL); 2; 2
            *([(D750Xdasm._dummy, 1)] * 9),
            *([(D750Xdasm._ip_addr, 2)] * 16),    #00111111 1100iiii A <- P(i); 2; 2
            *([(D750Xdasm._dummy, 1)] * 16),
            *([(D750Xdasm._op_addr, 2)] * 16),    #00111111 1110iiii P(i) <- A; 2; 2
            *([(D750Xdasm._dummy, 1)] * 16),
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            listing = [None] * rom.size()
            listing = self._disassemble(0x00, listing, rom)
            listing = self._disassemble(0x10, listing, rom)
            listing = self._disassemble(0x20, listing, rom)
            listing = self._disassemble(0x30, listing, rom)

            for i in range(len(listing)):
                if (listing[i] is None):
                    byte = rom.getByte(i)
                    listing[i] = (1, byte, 'db 0x%0.2X' % byte)
                listing[i] = (self._opbase % listing[i][1], listing[i][2])
            
            return {"LISTING": tuple(listing)}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        listing = self.disassemble(rom)["LISTING"]
        result = ""
        for i, line in enumerate(listing):
            if (line[1]):
                result += (self._addrbase % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(30) + "\n"
        with open(file_path, 'w') as f:
            f.write(result)
    
    def _disassemble(self, pc, listing, rom):
        while (pc < len(listing) and pc >= 0 and listing[pc] is None):
            opcode = rom.getByte(pc)
            instruction = self._instruction_tbl[opcode]
            if (instruction[1] == 2):
                opcode = rom.getWord(pc)
            next_pcs, mnemonic = instruction[0](self, pc, opcode, rom)
            instruction_size = instruction[1]
            listing[pc] = (instruction[1], opcode, mnemonic)
            if (instruction_size == 2):
                listing[pc + 1] = (1, rom.getByte(pc + 1), '')
            pc = next_pcs[0]
            for i in range(1, len(next_pcs), +1):
                if (next_pcs[i] == -1):
                    next_op = rom.getByte(pc)
                    next_size = self._instruction_tbl[next_op][1]
                    listing = self._disassemble(pc + next_size, listing, rom)
                else:
                    listing = self._disassemble(next_pcs[i], listing, rom)
        return listing

    def _instruction_00111110(self, pc, opcode, rom):
        #10011001
        return self._instruction_00111110_tbl[opcode & 0xFF][0](self, pc, opcode, rom)
    
    def _instruction_00111111(self, pc, opcode, rom):
        #10011001
        return self._instruction_00111111_tbl[opcode & 0xFF][0](self, pc, opcode, rom)
        
    def _dummy(self, pc, opcode, rom):
        return (pc + 1,), "undefined"
            
    def _aisc_data(self, pc, opcode, rom):
        #0000iiii A <- A + i Skip if overflow; 1; 1 + S 
        if (opcode == 0):
            return (pc + 1,), "nop"
        return (pc + 1, -1), "aisc 0x%0.1X" % (opcode & 0xF)

    def _lai_data(self, pc, opcode, rom):
        #0001iiii A <- i; 1; 1
        return (pc + 1, -1), "lai 0x%0.1X" % (opcode & 0xF)

    def _jmp_addr(self, pc, opcode, rom):
        #00100iii iiiiiiii pc10-0 <- i; 2; 2
        addr = opcode & 0x7FF
        return (addr,), "jmp %0.3X" % addr
        
    def _call_addr(self, pc, opcode, rom):
        #00110iii iiiiiiii SP <- PCm.PCl.PSW.PCh, pc10-0 <- i, SP <- SP - 4; 2; 2
        next_op = rom.getByte(pc + 2)
        next_size = self._instruction_tbl[next_op][1]
        
        self.last_call = pc + 2
        addr = opcode & 0x7FF
        return (pc + 2, pc + 2 + next_size, addr, -3), "call %0.3X" % addr

    def _ladr_addr(self, pc, opcode, rom):
        #00111000 0iiiiiii A <- (i); 2; 2
        return (pc + 2,), "ladr (%0.2X)" % (opcode & 0x7F)

    def _xadr(self, pc, opcode, rom):
        #00111001 0iiiiiii A <-> (i); 2; 2
        return (pc + 2,), "xadr (%0.2X)" % (opcode & 0x7F)

    def _xhdr(self, pc, opcode, rom):
        #00111010 0iiiiiii H <-> (i); 2; 2
        return (pc + 2,), "xhdr (%0.2X)" % (opcode & 0x7F)

    def _xldr(self, pc, opcode, rom):
        #00111011 0iiiiiii L <-> (i); 2; 2
        return (pc + 2,), "xldr (%0.2X)" % (opcode & 0x7F)

    def _ddrs_addr(self, pc, opcode, rom):
        #00111100 0iiiiiii (i) <- (i) - 1; 2; 2 + S
        return (pc + 2, -1), "ddrs (%0.2X)" % (opcode & 0x7F)

    def _idrs_addr(self, pc, opcode, rom):
        #00111101 0iiiiiii (i) <- (i) + 1; 2; 2 + S
        return (pc + 2, -1), "idrs (%0.2X)" % (opcode & 0x7F)
            
    def _lei_data(self, pc, opcode, rom):
        #00111110 0000iiii E <- i; 2; 2
        return (pc + 2,), "lei 0x%0.1X" % (opcode & 0xF)

    def _lli_data(self, pc, opcode, rom):
        #00111110 0001iiii L <- i; 2; 2
        return (pc + 2,), "lli 0x%0.1X" % (opcode & 0xF)

    def _ldi_data(self, pc, opcode, rom):
        #00111110 0010iiii D <- i; 2; 2
        return (pc + 2,), "ldi 0x%0.1X" % (opcode & 0xF)

    def _lhi_data(self, pc, opcode, rom):
        #00111110 0011iiii H <- i; 2; 2
        return (pc + 2,), "lhi 0x%0.1X" % (opcode & 0xF)

    def _skeei_data(self, pc, opcode, rom):
        #00111110 0100iiii Skip if E = i; 2; 2 + S
        return (pc + 2, -1), "skeei 0x%0.1X" % (opcode & 0xF)

    def _sklei_data(self, pc, opcode, rom):
        #00111110 0101iiii Skip if L = i; 2; 2 + S
        return (pc + 2, -1), "sklei 0x%0.1X" % (opcode & 0xF)

    def _skdei_data(self, pc, opcode, rom):
        #00111110 0110iiii Skip if D = i; 2; 2 + S
        return (pc + 2, -1), "skdei 0x%0.1X" % (opcode & 0xF)

    def _skhei_data(self, pc, opcode, rom):
        #00111110 0111iiii Skip if H = i; 2; 2 + S
        return (pc + 2, -1), "skhei 0x%0.1X" % (opcode & 0xF)

    def _tae(self, pc, opcode, rom):
        #00111110 10001010 E <- A; 2; 2
        return (pc + 2,), "tae"

    def _pshde(self, pc, opcode, rom):
        #00111110 10001110 (SP - 1) <- D, (SP - 2) <- E, SP <- SP - 2; 2; 2
        return (pc + 2,), "pshde"

    def _popde(self, pc, opcode, rom):
        #00111110 10001111 E <- (SP), D <- (SP + 1), SP <- SP + 2; 2; 2
        return (pc + 2,), "popde"

    def _tea(self, pc, opcode, rom):
        #00111110 10001011 A <- E; 2; 2
        return (pc + 2,), "tea"

    def _tal(self, pc, opcode, rom):
        #00111110 10011010 L <- A; 2; 2
        return (pc + 2,), "tal"

    def _tla(self, pc, opcode, rom):
        #00111110 10011011 A <- L; 2; 2
        return (pc + 2,), "tla"

    def _pshhl(self, pc, opcode, rom):
        #00111110 10011110 (SP - 1) <- H, (SP - 2) <- L, SP <- SP - 2; 2; 2
        return (pc + 2,), "pshhl"

    def _pophl(self, pc, opcode, rom):
        #00111110 10011111 L <- (SP), H <- (SP + 1), SP <- SP + 2; 2; 2
        return (pc + 2,), "pophl"

    def _tad(self, pc, opcode, rom):
        #00111110 10101010 D <- A; 2; 2
        return (pc + 2,), "tad"

    def _tda(self, pc, opcode, rom):
        #00111110 10101011 A <- D; 2; 2
        return (pc + 2,), "tda"

    def _tah(self, pc, opcode, rom):
        #00111110 10111010 H <- A; 2; 2
        return (pc + 2,), "tah"

    def _tha(self, pc, opcode, rom):
        #00111110 10111011 A <- H; 2; 2
        return (pc + 2,), "tha"

    def _jam_addr(self, pc, opcode, rom):
        #00111111 00010iii pc <- D2-0.A.(HL) ; 2; 2
        addr = (opcode & 0x7) << 8
        return (addr,), "jam %0.3X" % addr

    def _tamsp(self, pc, opcode, rom):
        #00111111 00110001 SPh <- A, SP3-1 <- (HL)3-1; 2; 2
        return (pc + 2,), "tamsp"

    def _tspam(self, pc, opcode, rom):
        #00111111 00110101 A <- SPh, (HL)3-1 <- SP3-1 (HL)0 <- 0; 2; 2
        return (pc + 2,), "tspam"

    def _halt(self, pc, opcode, rom):
        #00111111 00110110 Halt; 2; 2
        return (pc + 2,), "halt"

    def _stop(self, pc, opcode, rom):
        #00111111 00110111 Stop; 2; 2
        return (pc + 2,), "stop"

    def _timer(self, pc, opcode, rom):
        #00111111 00110010 TCRh <- 0, INTtRQF <- 0; 2; 2
        return (pc + 2,), "timer"

    def _sio(self, pc, opcode, rom):
        #00111111 00110011 SIOCR2-0 <- 0, INT0/sRQF <- 0; 2; 2
        return (pc + 2,), "sio"

    def _tsioam(self, pc, opcode, rom):
        #00111111 00111010 A <- SIOh, (HL) <- SIOl; 2; 2
        return (pc + 2,), "tsioam"

    def _tcntam(self, pc, opcode, rom):
        #00111111 00111011 A <- TCRh, (HL) <- TCRl; 2; 2
        return (pc + 2,), "tcntam"

    def _tamsio(self, pc, opcode, rom):
        #00111111 00111110 SIOh <- A, SIOl <- (HL); 2; 2
        return (pc + 2,), "tamsio"

    def _tammod(self, pc, opcode, rom):
        #00111111 00111111 TMRh <- A, TMRl <- (HL); 2; 2
        return (pc + 2,), "tammod"

    def _ski_data(self, pc, opcode, rom):
        #00111111 01000iii Skip if INTnRQF & i != 0, INTn <- RQF & !i; 2; 2 + S
        return (pc + 2, -1), "ski 0x%0.1X" % (opcode & 0x7)

    def _skaei_data(self, pc, opcode, rom):
        #00111111 0110iiii Skip if A = i; 2; 2 + S
        return (pc + 2, -1), "skaei 0x%0.1X" % (opcode & 0xF)

    def _ip54(self, pc, opcode, rom):
        #00111111 00111000 A <- P5, (HL) <- P4; 2; 2
        return (pc + 2,), "ip54"

    def _op54(self, pc, opcode, rom):
        #00111111 00111100 P5 <- A, P4 <- (HL); 2; 2
        return (pc + 2,), "op54"

    def _anl(self, pc, opcode, rom):
        #00111111 10110010 A <- A and (HL); 2; 2
        return (pc + 2,), "anl"

    def _rar(self, pc, opcode, rom):
        #00111111 10110011 C >> A >> C; 2; 2
        return (pc + 2,), "rar"

    def _orl(self, pc, opcode, rom):
        #00111111 10110110 A <- A or (HL); 2; 2
        return (pc + 2,), "orl"

    def _ip_addr(self, pc, opcode, rom):
        #00111111 1100iiii A <- P(i); 2; 2
        return (pc + 2,), "ip P%0.1X" % (opcode & 0xF)

    def _op_addr(self, pc, opcode, rom):
        #00111111 1110iiii P(i) <- A; 2; 2
        return (pc + 2,), "op P%0.1X" % (opcode & 0xF)

    def _di_data(self, pc, opcode, rom):
        #00111111 10000iii IER <- IER & !i, if i = 0, IME <- 0; 2; 2
        return (pc + 2,), "di 0x%0.1X" % (opcode & 0x7)

    def _ei_data(self, pc, opcode, rom):
        #00111111 10010iii IER <- IER | i, if i = 0, IME <- 1; 2; 2
        return (pc + 2,), "ei 0x%0.1X" % (opcode & 0x7)
            
    def _lam_dl(self, pc, opcode, rom):
        #01000000 A <- (DL); 1; 1
        return (pc + 1,), "lam (DL)"

    def _lam_de(self, pc, opcode, rom):
        #01000001 A <- (DE); 1; 1
        return (pc + 1,), "lam (DE)"

    def _rtpsw(self, pc, opcode, rom):
        #01000011 PCm.PCl.PSW.PCh <- (SP), SP <- SP + 4; 1; 2
        return (-3,), "rtpsw"
        
    def _xam_dl(self, pc, opcode, rom):
        #01000100 A <-> (DL); 1; 1
        return (pc + 1,), "xam (DL)"
        
    def _xam_de(self, pc, opcode, rom):
        #01000101 A <-> (DE); 1; 1
        return (pc + 1,), "xam (DE)"
        
    def _des(self, pc, opcode, rom):
        #01001000 E <- E - 1; 1; 1 + S
        return (pc + 1, -1), "des"
        
    def _ies(self, pc, opcode, rom):
        #01001001 E <- E + 1; 1; 1 + S
        return (pc + 1, -1), "ies"
        
    def _xad(self, pc, opcode, rom):
        #01001010 A <-> D; 1; 1
        return (pc + 1,), "xad"
        
    def _xae(self, pc, opcode, rom):
        #01001011 A <-> E; 1; 1
        return (pc + 1,), "xae"
        
    def _anp_data(self, pc, opcode, rom):
        #01001100 iiiiiiii P(i7-4) <- P(i7-4) & i3-0; 2; 2
        return (pc + 2,), "anp P%0.1X, 0x%0.1X" % (((opcode >> 4) & 0x0F), (opcode & 0x0F))
        
    def _orp_data(self, pc, opcode, rom):
        #01001101 iiiiiiii P(i7-4) <- P(i7-4) | i3-0; 2; 2
        return (pc + 2,), "orp P%0.1X, 0x%0.1X" % (((opcode >> 4) & 0x0F), (opcode & 0x0F))

    def _lhli_data(self, pc, opcode, rom):
        #01001110 iiiiiiii HL <- i; 2; 2
        return (pc + 2,), "lhli 0x%0.2X" % (opcode & 0xFF)

    def _ldei_data(self, pc, opcode, rom):
        #01001111 iiiiiiii DE <- i; 2; 2
        return (pc + 2,), "ldei 0x%0.2X" % (opcode & 0xFF)

    def _lam_hld(self, pc, opcode, rom):
        #01010000 A <- (HL-); 1; 1 + S
        return (pc + 1, -1), "lam (HL-)"

    def _lam_hli(self, pc, opcode, rom):
        #01010001 A <- (HL+); 1; 1 + S
        return (pc + 1, -1), "lam (HL+)"

    def _lam_hl(self, pc, opcode, rom):
        #01010010 A <- (HL); 1; 1
        return (pc + 1,), "lam (HL)"

    def _rt(self, pc, opcode, rom):
        #01010011 PCm.PCl.0000.PCh <- (SP), SP <- SP + 4; 1; 1
        return (-3,), "rt"

    def _xam_hld(self, pc, opcode, rom):
        #01010100 A <-> (HL-); 1; 1 + S
        return (pc + 1, -1), "xam (HL-)"

    def _xam_hli(self, pc, opcode, rom):
        #01010101 A <-> (HL-); 1; 1 + S
        return (pc + 1, -1), "xam (HL+)"

    def _xam_hl(self, pc, opcode, rom):
        #01010110 A <-> (HL); 1; 1
        return (pc + 1,), "xam (HL)"

    def _st(self, pc, opcode, rom):
        #01010111 (HL) <- A; 1; 1
        return (pc + 1,), "st"

    def _dls(self, pc, opcode, rom):
        #01011000 L <- L - 1; 1; 1 + S
        return (pc + 1, -1), "dls"

    def _ils(self, pc, opcode, rom):
        #01011001 L <- L + 1; 1; 1 + S
        return (pc + 1, -1), "ils"

    def _skc(self, pc, opcode, rom):
        #01011010 Skip if C = 1; 1; 1 + S
        return (pc + 1, -1), "skc"

    def _rts(self, pc, opcode, rom):
        #01011011 PCm.PCl.0000.PCh <- (SP), SP <- SP + 4; 1; 1 + S
        return (-3,), "rts"
        
    def _lamt(self, pc, opcode, rom):
        #01011110 A <- [PC10-6.0.C.A]h, (HL) <- [PC10-6.0.C.A]l; 1; 2
        return (pc + 1,), "lamt"

    def _skaem(self, pc, opcode, rom):
        #01011111 Skip if A = (HL); 1; 1 + S
        return (pc + 1, -1), "skaem"

    def _skmbf_data(self, pc, opcode, rom):
        #011000ii Skip if (HL)bi = 0; 1; 1 + S
        return (pc + 1, -1), "skmbf (HL).b%0.1X" % (opcode & 0x03)

    def _skmbt_data(self, pc, opcode, rom):
        #011001ii Skip if (HL)bi = 1; 1; 1 + S
        return (pc + 1, -1), "skmbt (HL).b%0.1X" % (opcode & 0x03)

    def _rmb(self, pc, opcode, rom):
        #011010ii (HL).bi <- 0; 1; 1
        return (pc + 1,), "rmb (HL).b%0.1X" % (opcode & 0x03)

    def _smb(self, pc, opcode, rom):
        #011011ii (HL).bi <- 1; 1; 1
        return (pc + 1,), "smb (HL).b%0.1X" % (opcode & 0x03)

    def _ipl(self, pc, opcode, rom):
        #01110000 A <- P(L); 1; 1
        return (pc + 1,), "ipl"

    def _ip1(self, pc, opcode, rom):
        #01110001 A <- P1; 1; 1
        return (pc + 1,), "ip1"

    def _opl(self, pc, opcode, rom):
        #01110010 P(L) <- A; 1; 1
        return (pc + 1,), "opl"

    def _op3(self, pc, opcode, rom):
        #01110011 P3 <- A; 1; 1
        return (pc + 1,), "op3"

    def _skabt_data(self, pc, opcode, rom):
        #011101ii Skip if Abi = 1; 1; 1 + S
        return (pc + 1, -1), "skabt A.b%0.1X" % (opcode & 0x03)

    def _rc(self, pc, opcode, rom):
        #01111000 C <- 0; 1; 1
        return (pc + 1,), "rc"
        
    def _sc(self, pc, opcode, rom):
        #01111001 C <- 1; 1; 1
        return (pc + 1,), "sc"

    def _xah(self, pc, opcode, rom):
        #01111010 A <-> H; 1; 1
        return (pc + 1,), "xah"

    def _xal(self, pc, opcode, rom):
        #01111011 A <-> L; 1; 1
        return (pc + 1,), "xal"

    def _acsc(self, pc, opcode, rom):
        #01111100 A, C <- A + (HL) + C; 1; 1 + S
        return (pc + 1, -1), "acsc"

    def _asc(self, pc, opcode, rom):
        #01111101 A <- A + (HL); 1; 1 + S
        return (pc + 1, -1), "asc"

    def _exl(self, pc, opcode, rom):
        #01111110 A <- A xor (HL); 1; 1
        return (pc + 1,), "exl"

    def _cma(self, pc, opcode, rom):
        #01111111 A <- !A; 1; 1
        return (pc + 1,), "cma"

    def _jcp_addr(self, pc, opcode, rom):
        #10iiiiii PC5.0 <- i; 1; 1
        addr = (pc & 0x7C0) | (opcode & 0x3F)
        return (addr,), "jcp %0.3X" % addr

    def _lhlt_addr(self, pc, opcode, rom):
        #1100iiii HL <- [0xC0 + i]; 1; 2
        return (pc + 1,), "lhlt [%0.3X]" % (0xC0 | (opcode & 0xF))

    def _calt_addr(self, pc, opcode, rom):
        #11iiiiii (SP) <- PCm.PCl.PSW.PCh, PC <- [0xC0 + i]h.00.[0xC0 + i]l, SP <- SP - 4; 1; 2
        self.last_call = pc + 1
        next_op = rom.getByte(pc + 1)
        next_size = self._instruction_tbl[next_op][1]
                    
        data = rom.getByte(opcode)
        addr = ((data << 2) & 0x380) | (data & 0x1F)
        return (pc + 1, pc + 1 + next_size, addr), "calt %0.3X" % addr
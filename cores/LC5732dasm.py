class LC5732dasm():

    def __init__(self):
        self._bytebase = '0x%0.2X'
        self._nibblebase = '0x%0.1X'
        self._addrbase = '%0.3X'
        self._opbase = '%0.2X'

        self._instructions = (
            LC5732dasm._halt,                   #00000000           1 1
            LC5732dasm._taat,                   #00000001           1 2   (AC, TREG) <- ROM(PGX, AC, M(DP))
            LC5732dasm._twrt,                   #00000010           1 2   PORT <- ROM(PGX, AC, M(DP))
            LC5732dasm._tmel,                   #00000011           1 2   ALM <- ROM(PGX, AC, M(DP))
            LC5732dasm._csp,                    #00000100           1 1   CSTF <- 0; CSTF
            LC5732dasm._cst,                    #00000101           1 1   CSTF <- 1; CSTF
            LC5732dasm._rc5,                    #00000110           1 1   HEF0 <- 0; HEF0
            LC5732dasm._sc5,                    #00000111           1 1   HEF0 <- 1; HEF0
            *([LC5732dasm._jmp_x] * 8),         #00001XXX XXXXXXXX  2 2   PC <- X
            LC5732dasm._jmp_p,                  #00010000           1 1   PC <- (PAGE, AC, M(DP))
            LC5732dasm._page,                   #00010001           1 1   page <- [M(DP)]
            LC5732dasm._mtr,                    #00010010           1 1   M(DP) <- TREG
            LC5732dasm._rts,                    #00010011           1 1   PC <- (STACK)
            LC5732dasm._mpcl,                   #00010100           1 1   M(DP) <- PC3-0
            LC5732dasm._mpcm,                   #00010101           1 1   M(DP) <- PC7-4
            LC5732dasm._mpch,                   #00010110           1 1   M(DP) <- PC10-8
            LC5732dasm._in,                     #00010111           1 1   AC <- (PORT)
            LC5732dasm._asr0,                   #00011000           1 1   ACn <- ACn+1; AC3 <- 0
            LC5732dasm._asr1,                   #00011001           1 1   ACn <- ACn+1; AC3 <- 1
            LC5732dasm._asl0,                   #00011010           1 1   ACn <- ACn-1; AC0 <- 0
            LC5732dasm._asl1,                   #00011011           1 1   ACn <- ACn-1; AC0 <- 1
            LC5732dasm._sdpl,                   #00011100           1 1   DPL <- (AC)
            LC5732dasm._sdph,                   #00011101           1 1   DPH <- (AC)
            LC5732dasm._edpl,                   #00011110           1 1   (DPL) <-> (EDPL)
            LC5732dasm._edph,                   #00011111           1 1   (DPH) <-> (EDPH)
            *([LC5732dasm._mvi_x] * 16),        #0010XXXX           1 1   M(DP) <- X
            *([LC5732dasm._ldi_x] * 16),        #0011XXXX           1 1   AC <- X
            *([LC5732dasm._baz_x] * 8),         #01000XXX XXXXXXXX  2 2   PC <- X if AC == 0
            *([LC5732dasm._bab0_x] * 8),        #01001XXX XXXXXXXX  2 2   PC <- X if AC0
            *([LC5732dasm._banz_x] * 8),        #01010XXX XXXXXXXX  2 2   PC <- X if AC != 0
            *([LC5732dasm._bab1_x] * 8),        #01011XXX XXXXXXXX  2 2   PC <- X if AC1
            *([LC5732dasm._bcnh_x] * 8),        #01100XXX XXXXXXXX  2 2   PC <- X if CF == 0
            *([LC5732dasm._bab2_x] * 8),        #01101XXX XXXXXXXX  2 2   PC <- X if AC2
            *([LC5732dasm._bch_x] * 8),         #01110XXX XXXXXXXX  2 2   PC <- X if CF != 0
            *([LC5732dasm._bab3_x] * 8),        #01111XXX XXXXXXXX  2 2   PC <- X if AC3
            LC5732dasm._adc,                    #10000000           1 1   AC <- (AC) + [M(DP)] + (CF); CF
            LC5732dasm._sbc,                    #10000001           1 1   AC <- (AC) + ~[M(DP)] + (CF); CF
            LC5732dasm._add,                    #10000010           1 1   AC <- (AC) + [M(DP)]; CF
            LC5732dasm._sub,                    #10000011           1 1   AC <- (AC) + ~[M(DP)] + 1; CF
            LC5732dasm._adn,                    #10000100           1 1   AC <- (AC) + [M(DP)]
            LC5732dasm._and,                    #10000101           1 1   AC <- (AC) and [M(DP)]
            LC5732dasm._eor,                    #10000110           1 1   AC <- (AC) xor [M(DP)]
            LC5732dasm._or,                     #10000111           1 1   AC <- (AC) or [M(DP)]
            LC5732dasm._adc_m,                  #10001000           1 1   AC, M(DP) <- (AC) + [M(DP)] + (CF); CF
            LC5732dasm._sbc_m,                  #10001001           1 1   AC, M(DP) <- (AC) + ~[M(DP)] + (CF); CF
            LC5732dasm._add_m,                  #10001010           1 1   AC, M(DP) <- (AC) + [M(DP)]; CF
            LC5732dasm._sub_m,                  #10001011           1 1   AC, M(DP) <- (AC) + ~[M(DP)] + 1; CF
            LC5732dasm._adn_m,                  #10001100           1 1   AC, M(DP) <- (AC) + [M(DP)]
            LC5732dasm._and_m,                  #10001101           1 1   AC, M(DP) <- (AC) and [M(DP)]
            LC5732dasm._eor_m,                  #10001110           1 1   AC, M(DP) <- (AC) xor [M(DP)]
            LC5732dasm._or_m,                   #10001111           1 1   AC, M(DP) <- (AC) or [M(DP)]
            LC5732dasm._adci,                   #10010000 ----XXXX  2 2   AC <- (AC) + X + (CF); CF
            LC5732dasm._sbci,                   #10010001 ----XXXX  2 2   AC <- (AC) + ~X + (CF); CF
            LC5732dasm._addi,                   #10010010 ----XXXX  2 2   AC <- (AC) + X; CF
            LC5732dasm._subi,                   #10010011 ----XXXX  2 2   AC <- (AC) + ~X + 1; CF
            LC5732dasm._adni,                   #10010100 ----XXXX  2 2   AC <- (AC) + X
            LC5732dasm._andi,                   #10010101 ----XXXX  2 2   AC <- (AC) and X
            LC5732dasm._eori,                   #10010110 ----XXXX  2 2   AC <- (AC) xor X
            LC5732dasm._ori,                    #10010111 ----XXXX  2 2   AC <- (AC) or X
            LC5732dasm._inc,                    #10011000           1 1   M(DP), AC <- M(DP) + 1
            LC5732dasm._dec,                    #10011001           1 1   M(DP), AC <- M(DP) - 1
            LC5732dasm._idpl,                   #10011010           1 1   DPL <- (DPL) + 1
            LC5732dasm._ddpl,                   #10011011           1 1   DPL <- (DPL) - 1
            LC5732dasm._idph,                   #10011100           1 1   DPH <- (DPH) + 1
            LC5732dasm._ddph,                   #10011101           1 1   DPH <- (DPH) - 1
            LC5732dasm._isp,                    #10011110           1 1   SP <- (SP) + 1
            LC5732dasm._dsp,                    #10011111           1 1   SP <- (SP) - 1
            *([LC5732dasm._jsr_x] * 8),         #10100XXX XXXXXXXX  2 2   STACK <- PC + 2; PC <- X
            LC5732dasm._ipm,                    #10101000           1 1   AC <- [P(M)]
            LC5732dasm._lda,                    #10101001           1 1   AC <- [M(DP)]
            LC5732dasm._lsp,                    #10101010           1 1   AC <- (SP)
            LC5732dasm._lhlt,                   #10101011           1 1   AC <- (STS2); STS2 <- 0; SCF1-4
            LC5732dasm._l500,                   #10101100           1 1   AC <- (STS1); SCF0 <- 0; SCF0
            LC5732dasm._sta,                    #10101101           1 1   M(DP) <- (AC)           
            LC5732dasm._ssp,                    #10101110           1 1   SP <- (AC)
            LC5732dasm._ips,                    #10101111           1 1   AC <- [P(S)]           
            *([LC5732dasm._mdpl_x] * 16),       #1011XXXX           1 1   DPL <- X
            *([LC5732dasm._mdph_x] * 16),       #1100XXXX           1 1   DPH <- X
            *([LC5732dasm._sic_x] * 16),        #1101XXXX           1 1   HEFn+1 = Xn; HEF1-4
            *([LC5732dasm._msp_x] * 16),        #1110XXXX           1 1   SP <- X
            LC5732dasm._rcf,                    #11110000           1 1   CF <- 0; CF
            LC5732dasm._scf,                    #11110001           1 1   CF <- 1; CF
            LC5732dasm._rlgt,                   #11110010           1 1   LIGHT <- 0
            LC5732dasm._slgt,                   #11110011           1 1   LIGHT <- 1
            *([LC5732dasm._spdr_x] * 4),        #111101XX           1 1   PDF <- X; PDF
            LC5732dasm._rbak,                   #11111000           1 1   BCF <- 0
            LC5732dasm._sbak,                   #11111001           1 1   BCF <- 1
            LC5732dasm._sas_x,                  #11111010 XXXXXXXX  2 2   ALM <- X
            #LC5732dasm._ras,                   #11111010 11111111  2 2
            LC5732dasm._csec,                   #11111011           1 1   PREDIV15-11 <- 0; SCF0,1,4 <- 0; SCF0,1,4 
            LC5732dasm._out,                    #11111100           1 1   PORT <- (AC, M(DP))
            LC5732dasm._ldpl,                   #11111101           1 1   AC <- (DPL)
            LC5732dasm._ldph,                   #11111110           1 1   AC <- (DPH)
            LC5732dasm._nop,                    #11111111           1 1
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            listing = [None] * rom.size()
            listing = self._disassemble(0x0, listing, rom)

            for i in range(len(listing)):
                if (listing[i] is None):
                    byte = rom.getByte(i)
                    listing[i] = (1, byte, 'db ' + self._bytebase % byte, '')
                listing[i] = (self._opbase % listing[i][1], (listing[i][2] + "\t;" + listing[i][3]).expandtabs(10))
            
            return {"LISTING": tuple(listing)}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        listing = self.disassemble(rom)["LISTING"]
        result = ""
        for i, line in enumerate(listing):
            if (line[1]):
                result += (self._addrbase % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(46) + "\n"
        with open(file_path, 'w') as f:
            f.write(result)
    
    def _disassemble(self, pc, listing, rom):
        while (pc < len(listing) and listing[pc] is None):
            opcode = rom.getByte(pc)
            next_pcs, listing[pc] = self._instructions[opcode](self, pc, opcode, rom)
            instruction_size = listing[pc][0]
            while (instruction_size > 1  and (pc + 1) < len(listing)):
                instruction_size -= 1
                pc += 1
                listing[pc] = (1, rom.getByte(pc), '', '')
            pc = next_pcs[0]
            if (len(next_pcs) > 1):
                listing = self._disassemble(next_pcs[1], listing, rom)
        return listing



    def _halt(self, pc, opcode, rom):
        #00000000           1 1
        return (pc + 1,), (1, opcode, "halt", "")

    def _taat(self, pc, opcode, rom):
        #00000001           1 2   (AC, TREG) <- ROM(PGX, AC, M(DP))
        return (pc + 1,), (1, opcode, "taat", "(AC, TREG) <- ROM(PGX, AC, M(DP))")

    def _twrt(self, pc, opcode, rom):
        #00000010           1 2   PORT <- ROM(PGX, AC, M(DP))
        return (pc + 1,), (1, opcode, "twrt", "PORT <- ROM(PGX, AC, M(DP))")

    def _tmel(self, pc, opcode, rom):
        #00000011           1 2   ALM <- ROM(PGX, AC, M(DP))
        return (pc + 1,), (1, opcode, "tmel", "ALM <- ROM(PGX, AC, M(DP))")

    def _csp(self, pc, opcode, rom):
        #00000100           1 1   CSTF <- 0; CSTF
        return (pc + 1,), (1, opcode, "csp", "CSTF <- 0; CSTF")

    def _cst(self, pc, opcode, rom):
        #00000101           1 1   CSTF <- 1; CSTF
        return (pc + 1,), (1, opcode, "cst", "CSTF <- 1; CSTF")

    def _rc5(self, pc, opcode, rom):
        #00000110           1 1   HEF0 <- 0; HEF0
        return (pc + 1,), (1, opcode, "rc5", "HEF0 <- 0; HEF0")

    def _sc5(self, pc, opcode, rom):
        #00000111           1 1   HEF0 <- 1; HEF0
        return (pc + 1,), (1, opcode, "sc5", "HEF0 <- 1; HEF0")

    def _jmp_x(self, pc, opcode, rom):
        #00001XXX XXXXXXXX  2 2   PC <- X
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x,), (2, opcode, "jmp " + self._addrbase % x, "PC <- %0.3X" % x)

    def _jmp_p(self, pc, opcode, rom):
        #00010000           1 1   PC <- (PAGE, AC, M(DP))
        return (pc + 1,), (1, opcode, "jmp*", "PC <- (PAGE, AC, M(DP)")

    def _page(self, pc, opcode, rom):
        #00010001           1 1   page <- [M(DP)]
        return (pc + 1,), (1, opcode, "page", "page <- [M(DP)]")

    def _mtr(self, pc, opcode, rom):
        #00010010           1 1   M(DP) <- TREG
        return (pc + 1,), (1, opcode, "mtr", "M(DP) <- TREG")

    def _rts(self, pc, opcode, rom):
        #00010011           1 1   PC <- (STACK)
        return (pc,), (1, opcode, "rts", "PC <- (STACK)")

    def _mpcl(self, pc, opcode, rom):
        #00010100           1 1   M(DP) <- PC3-0
        return (pc + 1,), (1, opcode, "mpcl", "M(DP) <- PC3-0")

    def _mpcm(self, pc, opcode, rom):
        #00010101           1 1   M(DP) <- PC7-4
        return (pc + 1,), (1, opcode, "mpcm", "M(DP) <- PC7-4")

    def _mpch(self, pc, opcode, rom):
        #00010110           1 1   M(DP) <- PC10-8
        return (pc + 1,), (1, opcode, "mpch", "M(DP) <- PC10-8")

    def _in(self, pc, opcode, rom):
        #00010111           1 1   AC <- (PORT)
        return (pc + 1,), (1, opcode, "in", "AC <- (PORT)")

    def _asr0(self, pc, opcode, rom):
        #00011000           1 1   ACn <- ACn+1; AC3 <- 0
        return (pc + 1,), (1, opcode, "asr0", "ACn <- ACn+1; AC3 <- 0")

    def _asr1(self, pc, opcode, rom):
        #00011001           1 1   ACn <- ACn+1; AC3 <- 1
        return (pc + 1,), (1, opcode, "asr1", "ACn <- ACn+1; AC3 <- 1")

    def _asl0(self, pc, opcode, rom):
        #00011010           1 1   ACn <- ACn-1; AC0 <- 0
        return (pc + 1,), (1, opcode, "asl0", "ACn <- ACn-1; AC0 <- 0")

    def _asl1(self, pc, opcode, rom):
        #00011011           1 1   ACn <- ACn-1; AC0 <- 1
        return (pc + 1,), (1, opcode, "asl1", "ACn <- ACn-1; AC0 <- 1")

    def _sdpl(self, pc, opcode, rom):
        #00011100           1 1   DPL <- (AC)
        return (pc + 1,), (1, opcode, "sdpl", "DPL <- (AC)")

    def _sdph(self, pc, opcode, rom):
        #00011101           1 1   DPH <- (AC)
        return (pc + 1,), (1, opcode, "sdph", "DPH <- (AC)")

    def _edpl(self, pc, opcode, rom):
        #00011110           1 1   (DPL) <-> (EDPL)
        return (pc + 1,), (1, opcode, "edpl", "(DPL) <-> (EDPL)")

    def _edph(self, pc, opcode, rom):
        #00011111           1 1   (DPH) <-> (EDPH)
        return (pc + 1,), (1, opcode, "edph", "(DPH) <-> (EDPH)")

    def _mvi_x(self, pc, opcode, rom):
        #0010XXXX           1 1   M(DP) <- X
        x = (opcode & 0xF)
        return (pc + 1,), (1, opcode, "mvi " + self._nibblebase % x, "M(DP) <- 0x%0.1X" % x)

    def _ldi_x(self, pc, opcode, rom):
        #0011XXXX           1 1   AC <- X
        x = (opcode & 0xF)
        return (pc + 1,), (1, opcode, "ldi " + self._nibblebase % x, "AC <- 0x%0.1X" % x)

    def _baz_x(self, pc, opcode, rom):
        #01000XXX XXXXXXXX  2 2   PC <- X if AC == 0
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "baz " + self._addrbase % x, "PC <- X if AC == 0")

    def _bab0_x(self, pc, opcode, rom):
        #01001XXX XXXXXXXX  2 2   PC <- X if AC0
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "bab0 " + self._addrbase % x, "PC <- X if AC0")

    def _banz_x(self, pc, opcode, rom):
        #01010XXX XXXXXXXX  2 2   PC <- X if AC != 0
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "banz " + self._addrbase % x, "PC <- X if AC != 0")

    def _bab1_x(self, pc, opcode, rom):
        #01011XXX XXXXXXXX  2 2   PC <- X if AC1
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "bab1 " + self._addrbase % x, "PC <- X if AC1")

    def _bcnh_x(self, pc, opcode, rom):
        #01100XXX XXXXXXXX  2 2   PC <- X if CF == 0
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "bcnh " + self._addrbase % x, "PC <- X if CF == 0")

    def _bab2_x(self, pc, opcode, rom):
        #01101XXX XXXXXXXX  2 2   PC <- X if AC2
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "bab2 " + self._addrbase % x, "PC <- X if AC2")

    def _bch_x(self, pc, opcode, rom):
        #01110XXX XXXXXXXX  2 2   PC <- X if CF != 0
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "bch " + self._addrbase % x, "PC <- X if CF != 0")

    def _bab3_x(self, pc, opcode, rom):
        #01111XXX XXXXXXXX  2 2   PC <- X if AC3
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "bab3 " + self._addrbase % x, "PC <- X if AC3")

    def _adc(self, pc, opcode, rom):
        #10000000           1 1   AC <- (AC) + [M(DP)] + (CF); CF
        return (pc + 1,), (1, opcode, "adc", "AC <- (AC) + [M(DP)] + (CF); CF")

    def _sbc(self, pc, opcode, rom):
        #10000001           1 1   AC <- (AC) + ~[M(DP)] + (CF); CF
        return (pc + 1,), (1, opcode, "sbc", "AC <- (AC) + ~[M(DP)] + (CF); CF")

    def _add(self, pc, opcode, rom):
        #10000010           1 1   AC <- (AC) + [M(DP)]; CF
        return (pc + 1,), (1, opcode, "add", "AC <- (AC) + [M(DP)]; CF")

    def _sub(self, pc, opcode, rom):
        #10000011           1 1   AC <- (AC) + ~[M(DP)] + 1; CF
        return (pc + 1,), (1, opcode, "sub", "AC <- (AC) + ~[M(DP)] + 1; CF")

    def _adn(self, pc, opcode, rom):
        #10000100           1 1   AC <- (AC) + [M(DP)]
        return (pc + 1,), (1, opcode, "adn", "AC <- (AC) + [M(DP)]")

    def _and(self, pc, opcode, rom):
        #10000101           1 1   AC <- (AC) and [M(DP)]
        return (pc + 1,), (1, opcode, "and", "AC <- (AC) and [M(DP)]")

    def _eor(self, pc, opcode, rom):
        #10000110           1 1   AC <- (AC) xor [M(DP)]
        return (pc + 1,), (1, opcode, "eor", "AC <- (AC) xor [M(DP)]")

    def _or(self, pc, opcode, rom):
        #10000111           1 1   AC <- (AC) or [M(DP)]
        return (pc + 1,), (1, opcode, "or", "AC <- (AC) or [M(DP)]")

    def _adc_m(self, pc, opcode, rom):
        #10001000           1 1   AC, M(DP) <- (AC) + [M(DP)] + (CF); CF
        return (pc + 1,), (1, opcode, "adc*", "AC, M(DP) <- (AC) + [M(DP)] + (CF); CF")

    def _sbc_m(self, pc, opcode, rom):
        #10001001           1 1   AC, M(DP) <- (AC) + ~[M(DP)] + (CF); CF
        return (pc + 1,), (1, opcode, "sbc*", "AC, M(DP) ← (AC) + ~[M(DP)] + (CF); CF")

    def _add_m(self, pc, opcode, rom):
        #10001010           1 1   AC, M(DP) <- (AC) + [M(DP)]; CF
        return (pc + 1,), (1, opcode, "add*", "AC, M(DP) <- (AC) + [M(DP)]; CF")

    def _sub_m(self, pc, opcode, rom):
        #10001011           1 1   AC, M(DP) <- (AC) + ~[M(DP)] + 1; CF
        return (pc + 1,), (1, opcode, "sub*", "AC, M(DP) <- (AC) + ~[M(DP)] + 1; CF")

    def _adn_m(self, pc, opcode, rom):
        #10001100           1 1   AC, M(DP) <- (AC) + [M(DP)]
        return (pc + 1,), (1, opcode, "adn*", "AC, M(DP) <- (AC) + [M(DP)]")

    def _and_m(self, pc, opcode, rom):
        #10001101           1 1   AC, M(DP) <- (AC) and [M(DP)]
        return (pc + 1,), (1, opcode, "and*", "AC, M(DP) <- (AC) and [M(DP)]")

    def _eor_m(self, pc, opcode, rom):
        #10001110           1 1   AC, M(DP) <- (AC) xor [M(DP)]
        return (pc + 1,), (1, opcode, "eor*", "AC, M(DP) <- (AC) xor [M(DP)]")

    def _or_m(self, pc, opcode, rom):
        #10001111           1 1   AC, M(DP) <- (AC) or [M(DP)]
        return (pc + 1,), (1, opcode, "or*", "AC, M(DP) <- (AC) or [M(DP)]")

    def _adci(self, pc, opcode, rom):
        #10010000 ----XXXX  2 2   AC <- (AC) + X + (CF); CF
        x = rom.getByte(pc + 1) & 0xF
        return (pc + 2,), (2, opcode, "adci " + self._nibblebase % x, "AC <- (AC) + X + (CF); CF")

    def _sbci(self, pc, opcode, rom):
        #10010001 ----XXXX  2 2   AC <- (AC) + ~X + (CF); CF
        x = rom.getByte(pc + 1) & 0xF
        return (pc + 2,), (2, opcode, "sbci " + self._nibblebase % x, "AC <- (AC) + ~X + (CF); CF")

    def _addi(self, pc, opcode, rom):
        #10010010 ----XXXX  2 2   AC <- (AC) + X; CF
        x = rom.getByte(pc + 1) & 0xF
        return (pc + 2,), (2, opcode, "addi " + self._nibblebase % x, "AC <- (AC) + X; CF")

    def _subi(self, pc, opcode, rom):
        #10010011 ----XXXX  2 2   AC <- (AC) + ~X + 1; CF
        x = rom.getByte(pc + 1) & 0xF
        return (pc + 2,), (2, opcode, "subi " + self._nibblebase % x, "AC <- (AC) + ~X + 1; CF")

    def _adni(self, pc, opcode, rom):
        #10010100 ----XXXX  2 2   AC <- (AC) + X
        x = rom.getByte(pc + 1) & 0xF
        return (pc + 2,), (2, opcode, "adni " + self._nibblebase % x, "AC <- (AC) + X")

    def _andi(self, pc, opcode, rom):
        #10010101 ----XXXX  2 2   AC <- (AC) and X
        x = rom.getByte(pc + 1) & 0xF
        return (pc + 2,), (2, opcode, "andi " + self._nibblebase % x, "AC <- (AC) and X")

    def _eori(self, pc, opcode, rom):
        #10010110 ----XXXX  2 2   AC <- (AC) xor X
        x = rom.getByte(pc + 1) & 0xF
        return (pc + 2,), (2, opcode, "eori " + self._nibblebase % x, "AC <- (AC) xor X")

    def _ori(self, pc, opcode, rom):
        #10010111 ----XXXX  2 2   AC <- (AC) or X
        x = rom.getByte(pc + 1) & 0xF
        return (pc + 2,), (2, opcode, "ori " + self._nibblebase % x, "AC <- (AC) or X")

    def _inc(self, pc, opcode, rom):
        #10011000           1 1   M(DP), AC <- M(DP) + 1
        return (pc + 1,), (1, opcode, "inc", "M(DP), AC <- M(DP) + 1")

    def _dec(self, pc, opcode, rom):
        #10011001           1 1   M(DP), AC <- M(DP) - 1
        return (pc + 1,), (1, opcode, "dec", "M(DP), AC <- M(DP) - 1")

    def _idpl(self, pc, opcode, rom):
        #10011010           1 1   DPL <- (DPL) + 1
        return (pc + 1,), (1, opcode, "idpl", "DPL <- (DPL) + 1")

    def _ddpl(self, pc, opcode, rom):
        #10011011           1 1   DPL <- (DPL) - 1
        return (pc + 1,), (1, opcode, "ddpl", "DPL <- (DPL) - 1")

    def _idph(self, pc, opcode, rom):
        #10011100           1 1   DPH <- (DPH) + 1
        return (pc + 1,), (1, opcode, "idph", "DPH <- (DPH) + 1")

    def _ddph(self, pc, opcode, rom):
        #10011101           1 1   DPH <- (DPH) - 1
        return (pc + 1,), (1, opcode, "ddph", "DPH <- (DPH) - 1")

    def _isp(self, pc, opcode, rom):
        #10011110           1 1   SP <- (SP) + 1
        return (pc + 1,), (1, opcode, "isp", "SP <- (SP) + 1")

    def _dsp(self, pc, opcode, rom):
        #10011111           1 1   SP <- (SP) - 1
        return (pc + 1,), (1, opcode, "dsp", "SP <- (SP) - 1")

    def _jsr_x(self, pc, opcode, rom):
        #10100XXX XXXXXXXX  2 2   STACK <- PC + 2; PC <- X
        x = ((opcode & 0x7) << 8) | rom.getByte(pc + 1)
        return (x, pc + 2,), (2, opcode, "jsr " + self._addrbase % x, "STACK <- PC + 2; PC <- X")

    def _ipm(self, pc, opcode, rom):
        #10101000           1 1   AC <- [P(M)]
        return (pc + 1,), (1, opcode, "ipm", "AC <- [P(M)]")

    def _lda(self, pc, opcode, rom):
        #10101001           1 1   AC <- [M(DP)]
        return (pc + 1,), (1, opcode, "lda", "AC <- [M(DP)]")

    def _lsp(self, pc, opcode, rom):
        #10101010           1 1   AC <- (SP)
        return (pc + 1,), (1, opcode, "lsp", "AC <- (SP)")

    def _lhlt(self, pc, opcode, rom):
        #10101011           1 1   AC <- (STS2); STS2 <- 0; SCF1-4
        return (pc + 1,), (1, opcode, "lhlt", "AC <- (STS2); STS2 <- 0; SCF1-4")

    def _l500(self, pc, opcode, rom):
        #10101100           1 1   AC <- (STS1); SCF0 <- 0; SCF0
        return (pc + 1,), (1, opcode, "l500", "AC <- (STS1); SCF0 <- 0; SCF0")

    def _sta(self, pc, opcode, rom):
        #10101101           1 1   M(DP) <- (AC)           
        return (pc + 1,), (1, opcode, "sta", "M(DP) <- (AC)  ")

    def _ssp(self, pc, opcode, rom):
        #10101110           1 1   SP <- (AC)
        return (pc + 1,), (1, opcode, "ssp", "SP <- (AC)")

    def _ips(self, pc, opcode, rom):
        #10101111           1 1   AC <- [P(S)]
        return (pc + 1,), (1, opcode, "ips", "AC <- [P(S)]")

    def _mdpl_x(self, pc, opcode, rom):
        #1011XXXX           1 1   DPL <- X
        x = opcode & 0xF
        return (pc + 1,), (1, opcode, "mdpl " + self._nibblebase % x, "DPL <- 0x%0.1X" % x)

    def _mdph_x(self, pc, opcode, rom):
        #1100XXXX           1 1   DPH <- X
        x = opcode & 0xF
        return (pc + 1,), (1, opcode, "mdph " + self._nibblebase % x, "DPH <- 0x%0.1X" % x)

    def _sic_x(self, pc, opcode, rom):
        #1101XXXX           1 1   HEFn+1 = Xn; HEF1-4
        x = opcode & 0xF
        return (pc + 1,), (1, opcode, "sic " + self._nibblebase % x, "HEFn+1 = Xn; HEF1-4")

    def _msp_x(self, pc, opcode, rom):
        #1110XXXX           1 1   SP <- X
        x = opcode & 0xF
        return (pc + 1,), (1, opcode, "msp " + self._nibblebase % x, "SP <- 0x%0.1X" % x)

    def _rcf(self, pc, opcode, rom):
        #11110000           1 1   CF <- 0; CF
        return (pc + 1,), (1, opcode, "rcf", "CF <- 0; CF")

    def _scf(self, pc, opcode, rom):
        #11110001           1 1   CF <- 1; CF
        return (pc + 1,), (1, opcode, "scf", "CF <- 1; CF")

    def _rlgt(self, pc, opcode, rom):
        #11110010           1 1   LIGHT <- 0
        return (pc + 1,), (1, opcode, "rlgt", "LIGHT <- 0")

    def _slgt(self, pc, opcode, rom):
        #11110011           1 1   LIGHT <- 1
        return (pc + 1,), (1, opcode, "slgt", "LIGHT <- 1")

    def _spdr_x(self, pc, opcode, rom):
        #111101XX           1 1   PDF <- X; PDF
        x = opcode & 0x3
        return (pc + 1,), (1, opcode, "spdr " + self._nibblebase % x, "PDF <- 0x%0.1X; PDF" % x)

    def _rbak(self, pc, opcode, rom):
        #11111000           1 1   BCF <- 0
        return (pc + 1,), (1, opcode, "rbak", "BCF <- 0")

    def _sbak(self, pc, opcode, rom):
        #11111001           1 1   BCF <- 1
        return (pc + 1,), (1, opcode, "sbak", "BCF <- 1")

    def _sas_x(self, pc, opcode, rom):
        #11111010 XXXXXXXX  2 2   ALM <- X
        x = rom.getByte(pc + 1)
        return (pc + 2,), (2, opcode, "sas " + self._bytebase % x, "ALM <- 0x%0.1X" % x)

    def _csec(self, pc, opcode, rom):
        #11111011   1 1   PREDIV15-11 <- 0; SCF0,1,4 <- 0; SCF0,1,4 
        return (pc + 1,), (1, opcode, "csec", "PREDIV15-11 <- 0; SCF0,1,4 <- 0; SCF0,1,4 ")

    def _out(self, pc, opcode, rom):
        #11111100           1 1   PORT <- (AC, M(DP))
        return (pc + 1,), (1, opcode, "out", "PORT <- (AC, M(DP))")

    def _ldpl(self, pc, opcode, rom):
        #11111101           1 1   AC <- (DPL)
        return (pc + 1,), (1, opcode, "ldpl", "AC <- (DPL)")

    def _ldph(self, pc, opcode, rom):
        #11111110           1 1   AC <- (DPH)
        return (pc + 1,), (1, opcode, "ldph", "AC <- (DPH)")

    def _nop(self, pc, opcode, rom):
        #11111111           1 1
        return (pc + 1,), (1, opcode, "nop", "")
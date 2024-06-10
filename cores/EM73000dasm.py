class EM73000dasm():

    def __init__(self):
        self._base = '0x%X'
        self._bytebase = '0x%0.2X'
        self._wordbase = '0x%0.4X'
        self._nibblebase = '0x%0.1X'
        self._portbase = '%d'
        self._addrbase = '%0.4X'
        self._opbase = '%0.2X'

        self._instructions = (
            *([EM73000dasm._sbr_a] * 64),       #00aa aaaa If SF=1 then PC¬PC12-6.a5-0 1 1 - - 1 else null
            *([EM73000dasm._lcall_a] * 8),      #0100 0aaa aaaa aaaa STACK[SP]¬PC, 2 2 - - - SP¬SP -1, PC¬a
            EM73000dasm._std_k_y,               #0100 1000 kkkk yyyy RAM[y]¬k 2 2 - - 1
            EM73000dasm._add_k_y,               #0100 1001 kkkk yyyy RAM[y]¬RAM[y] +k 2 2 - Z C'
            EM73000dasm._out_k_p,               #0100 1010 kkkk pppp PORT[p]¬k 2 2 - - 1
            EM73000dasm._cmp_k_y,               #0100 1011 kkkk yyyy k-RAM[y] 2 2 C Z Z'
            EM73000dasm._exhl_x,                #0100 1100 xxxx xx00 LR«RAM[x], HR«RAM[x+1] 2 2 - - 1
            EM73000dasm._rti,                   #0100 1101 SP¬SP+1,FLAG.PC 1 2 * * * ¬STACK[SP],EIF ¬1
            EM73000dasm._ldhl_x,                #0100 1110 xxxx xx00 LR¬RAM[x],HR¬RAM[x+1] 2 2 - - 1
            EM73000dasm._ret,                   #0100 1111 SP¬SP + 1, PC¬STACK[SP] 1 2 - - -
            EM73000dasm._rlca,                  #0101 0000 ¬CF¬Acc¬ 1 1 C Z C'
            EM73000dasm._rrca,                  #0101 0001 ®CF®Acc® 1 1 C Z C'
            EM73000dasm._ttcfs,                 #0101 0010 SF¬CF, CF¬1 1 1 1 - *
            EM73000dasm._tfcfc,                 #0101 0011 SF¬CF', CF¬0 1 1 0 - *
            EM73000dasm._dummy,
            EM73000dasm._slbr1_a,               #0101 0101 1100 aaaa aaaa aaaa (a:1000h~1FFFh) SF=1; PC ¬ a ( branch condition satisified)
            EM73000dasm._nop,                   #0101 0110 no operation 1 1 - - -
            EM73000dasm._slbr0_a,               #0101 0111 1100 aaaa aaaa aaaa (a:0000h~0FFFh) SF=1; PC ¬ a ( branch condition satisified)
            EM73000dasm._exam,                  #0101 1000 Acc«RAM[HL] 1 1 - Z 1
            EM73000dasm._stam,                  #0101 1001 RAM[HL]¬Acc 1 1 - - 1
            EM73000dasm._ldam,                  #0101 1010 Acc ¬RAM[HL] 1 1 - Z 1
            EM73000dasm._tzs,                   #0101 1011 SF¬ZF 1 1 - - *
            EM73000dasm._deca,                  #0101 1100 Acc¬Acc-1 1 1 - Z C
            EM73000dasm._decm,                  #0101 1101 RAM[HL]¬RAM[HL] -1 1 1 - Z C
            EM73000dasm._inca,                  #0101 1110 Acc¬Acc + 1 1 1 - Z C'
            EM73000dasm._incm,                  #0101 1111 RAM[HL]¬RAM[HL]+1 1 1 - Z C'
            EM73000dasm._clpl,                  #0110 0000 PORT[LR3-2+4]LR1-0¬0 1 2 - - 1
            EM73000dasm._tfpl,                  #0110 0001 SF¬PORT[LR 3-2 +4]LR1-0' 1 2 - - *
            EM73000dasm._sepl,                  #0110 0010 PORT[LR3-2+4]LRl-0¬1 1 2 - - 1
            EM73000dasm._cil,                   #0110 0011
            EM73000dasm._exal,                  #0110 0100 Acc«LR 1 2 - Z 1
            EM73000dasm._ldax,                  #0110 0101 Acc¬ROM[DP]L 1 2 - Z 1
            EM73000dasm._exah,                  #0110 0110 Acc«HR 1 2 - Z 1
            EM73000dasm._ldaxi,                 #0110 0111 Acc¬ROM[DP]H,DP+1 1 2 - Z 1
            EM73000dasm._exa_x,                 #0110 1000 xxxx xxxx Acc«RAM[x] 2 2 - Z 1
            EM73000dasm._sta_x,                 #0110 1001 xxxx xxxx RAM[x]¬Acc 2 2 - - 1
            EM73000dasm._lda_x,                 #0110 1010 xxxx xxxx Acc¬RAM[x] 2 2 - Z 1
            EM73000dasm._cmpa_x,                #0110 1011 xxxx xxxx RAM[x]-Acc 2 2 C Z Z'
            EM73000dasm._bit_y_b,               #0110 1100
            EM73000dasm._bit_p_b,               #0110 1101 
            EM73000dasm._math_k,                #0110 1110
            EM73000dasm._io_p,                  #0110 1111
            EM73000dasm._adcam,                 #0111 0000 Acc¬Acc + RAM[HL] + CF 1 1 C Z C'
            EM73000dasm._addam,                 #0111 0001 Acc¬Acc + RAM[HL] 1 1 - Z C'
            EM73000dasm._sbcam,                 #0111 0010 Acc¬RAM[HLl - Acc - CF' 1 1 C Z C
            EM73000dasm._cmpam,                 #0111 0011 RAM[HL] - Acc 1 1 C Z Z'
            EM73000dasm._tla,                   #0111 0100 Acc¬LR 1 1 - Z 1
            EM73000dasm._exae,                  #0111 0101 MASK«Acc 1 1 - - 1
            EM73000dasm._tha,                   #0111 0110 Acc¬HR 1 1 - Z 1
            EM73000dasm._dummy,
            EM73000dasm._oram,                  #0111 1000 Acc ¬Acc RAM[HL] 1 1 - Z Z'
            EM73000dasm._xoram,                 #0111 1001 Acc¬Acc^RAM[HL] 1 1 - Z Z'
            EM73000dasm._dummy,
            EM73000dasm._andam,                 #0111 1011 Acc¬Acc & RAM[HL] 1 1 - Z Z'
            EM73000dasm._decl,                  #0111 1100 LR¬LR-1 1 1 - Z C
            EM73000dasm._stamd,                 #0111 1101 RAM[HL]¬Acc, LR-1 1 1 - Z C
            EM73000dasm._incl,                  #0111 1110 LR¬LR + 1 1 1 - Z C'
            EM73000dasm._stami,                 #0111 1111 RAM[HL]¬Acc, LR+1 1 1 - Z C'
            *([EM73000dasm._ldl_k] * 16),       #1000 kkkk LR¬k 1 1 - - 1
            *([EM73000dasm._ldh_k] * 16),       #1001 kkkk HR¬k 1 1 - - 1
            *([EM73000dasm._stdmi_k] * 16),     #1010 kkkk RAM[HL]¬k, LR+1 1 1 - Z C'
            *([EM73000dasm._cmpia_k] * 16),     #1011 kkkk k - Acc 1 1 C Z Z'
            *([EM73000dasm._lbr_a] * 16),       #1100 aaaa aaaa aaaa If SF= 1 then PC¬a else null 2 2 - - 1
            *([EM73000dasm._ldia_k] * 16),      #1101 kkkk Acc¬k 1 1 - Z 1
            *([EM73000dasm._scall_a] * 16),     #1110 nnnn STACK[SP]¬PC, 1 2 - - - SP¬SP - 1, PC¬a, a = 8n + 6 (n =1~15),0086h (n = 0)
            *([EM73000dasm._clm_b] * 4),        #1111 00bb RAM[HL]b¬0 1 1 - - 1
            *([EM73000dasm._sem_b] * 4),        #1111 01bb RAM[HL]b¬1 1 1 - - 1
            *([EM73000dasm._tfa_b] * 4),        #1111 10bb SF¬Accb' 1 1 - - *
            *([EM73000dasm._tfm_b] * 4),        #1111 11bb SF¬RAM[HL]b' 1 1 - - *
        )

        self._instructions_cil = (
            EM73000dasm._dummy,
            EM73000dasm._eicil_r,               #0110 0011 01rr rrrr EIF¬1,IL¬IL&r 2 2 - - 1
            EM73000dasm._dicil_r,               #0110 0011 10rr rrrr EIF¬0,IL¬IL&r 2 2 - - 1
            EM73000dasm._cil_r,                 #0110 0011 11rr rrrr IL¬IL & r 2 2 - - 1
        )

        self._instructions_bit_y_b = (
            EM73000dasm._tf_y_b,                #0110 1100 00bb yyyy SF¬RAM[y]b' 2 2 - - *
            EM73000dasm._set_y_b,               #0110 1100 01bb yyyy RAM[y]b¬1 2 2 - - 1
            EM73000dasm._tt_y_b,                #0110 1100 10bb yyyy SF¬RAM[y]b 2 2 - - *
            EM73000dasm._clr_y_b,               #0110 1100 11bb yyyy RAM[y]b¬0 2 2 - - 1
        )

        self._instructions_bit_p_b = (
            EM73000dasm._tfp_p_b,               #0110 1101 00bb pppp SF¬PORT[p]b' 2 2 - - *
            EM73000dasm._sep_p_b,               #0110 1101 01bb pppp PORT[p]b¬1 2 2 - - 1
            EM73000dasm._ttp_p_b,               #0110 1101 10bb pppp SF¬PORT[p]b 2 2 - - *
            EM73000dasm._clp_p_b,               #0110 1101 11bb pppp PORT[p]b¬0 2 2 - - 1
        )

        self._instructions_math_k = (
            EM73000dasm._dummy,
            EM73000dasm._addl_k,                #0110 1110 0001 kkkk LR¬LR+k 2 2 - Z C'
            EM73000dasm._dummy,
            EM73000dasm._cmpl_k,                #0110 1110 0011 kkkk k-LR 2 2 - Z C
            EM73000dasm._ora_k,                 #0110 1110 0100 kkkk Acc¬Acc k 2 2 - Z Z'
            EM73000dasm._adda_k,                #0110 1110 0101 kkkk Acc¬Acc+k 2 2 - Z C'
            EM73000dasm._anda_k,                #0110 1110 0110 kkkk Acc¬Acc&k 2 2 - Z Z'
            EM73000dasm._suba_k,                #0110 1110 0111 kkkk Acc¬k-Acc 2 2 - Z C
            EM73000dasm._dummy,
            EM73000dasm._addh_k,                #0110 1110 1001 kkkk HR¬HR+k 2 2 - Z C'
            EM73000dasm._dummy,
            EM73000dasm._cmph_k,                #0110 1110 1011 kkkk k - HR 2 2 - Z C
            EM73000dasm._orm_k,                 #0110 1110 1100 kkkk RAM[HL]¬RAM[HL] k 2 2 - Z Z'
            EM73000dasm._addm_k,                #0110 1110 1101 kkkk RAM[HL]¬RAM[HL] +k 2 2 - Z C'
            EM73000dasm._andm_k,                #0110 1110 1110 kkkk RAM[HL]¬RAM[HL]&k 2 2 - Z Z'
            EM73000dasm._subm_k,                #0110 1110 1111 kkkk RAM[HL]¬k - RAM[HL] 2 2 - Z C
        )

        self._instructions_io_p = (
            EM73000dasm._outa_p,                #0110 1111 000p pppp PORT[p]¬Acc 2 2 - - 1
            EM73000dasm._ina_p,                 #0110 1111 0100 pppp Acc¬PORT[p] 2 2 - Z Z'
            EM73000dasm._outm_p,                #0110 1111 100p pppp PORT[p]¬RAM[HL] 2 2 - - 1
            EM73000dasm._inm_p,                 #0110 1111 1100 pppp RAM[HL]¬PORT[p] 2 2 - - Z'
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            listing = [None] * rom.size()
            listing = self._disassemble(0x0, listing, rom)
            listing = self._disassemble(0x2, listing, rom)
            listing = self._disassemble(0x4, listing, rom)
            listing = self._disassemble(0x6, listing, rom)
            listing = self._disassemble(0x8, listing, rom)
            listing = self._disassemble(0xA, listing, rom)
            listing = self._disassemble(0xC, listing, rom)

            for i in range(len(listing)):
                if (listing[i] is None):
                    byte = rom.getByte(i)
                    listing[i] = (1, byte, 'db ' + self._bytebase % byte)
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
        while (pc < len(listing) and listing[pc] is None):
            opcode = rom.getByte(pc)
            next_pcs, listing[pc] = self._instructions[opcode](self, pc, opcode, rom)
            instruction_size = listing[pc][0]
            while (instruction_size > 1  and (pc + 1) < len(listing)):
                instruction_size -= 1
                pc += 1
                listing[pc] = (1, rom.getByte(pc), '')
            pc = next_pcs[0]
            if (len(next_pcs) > 1):
                listing = self._disassemble(next_pcs[1], listing, rom)
        return listing

    def _sbr_a(self, pc, opcode, rom):
        #00aa aaaa If SF=1 then PC¬PC12-6.a5-0 1 1 - - 1 else null
        addr = ((pc + 1) & 0x1FC0) | (opcode & 0x003F)
        return (pc + 1, addr), (1, opcode, "sbr " + self._addrbase % addr)
        
    def _lcall_a(self, pc, opcode, rom):
        #0100 0aaa aaaa aaaa STACK[SP]¬PC, 2 2 - - - SP¬SP -1, PC¬a
        opcode = opcode << 8 | rom.getByte(pc + 1)
        addr = opcode & 0x07FF
        return (pc + 2, addr), (2, opcode, "lcall " + self._addrbase % addr)
        
    def _std_k_y(self, pc, opcode, rom):
        #0100 1000 kkkk yyyy RAM[y]¬k 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        k = opcode >> 4 & 0x000F
        y = opcode & 0x000F
        return (pc + 2,), (2, opcode, "std " + self._nibblebase % k + ", RAM[" + self._nibblebase % y + "]")
        
    def _add_k_y(self, pc, opcode, rom):
        #0100 1001 kkkk yyyy RAM[y]¬RAM[y] +k 2 2 - Z C'
        opcode = opcode << 8 | rom.getByte(pc + 1)
        k = opcode >> 4 & 0x000F
        y = opcode & 0x000F
        return (pc + 2,), (2, opcode, "add RAM[" + self._nibblebase % y + "] + " + self._nibblebase % k + ", RAM[" + self._nibblebase % y + "]")
        
    def _out_k_p(self, pc, opcode, rom):
        #0100 1010 kkkk pppp PORT[p]¬k 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        k = opcode >> 4 & 0x000F
        p = opcode & 0x000F
        return (pc + 2,), (2, opcode, "out " + self._nibblebase % k + ", PORT[" + self._portbase % p + "]")
        
    def _cmp_k_y(self, pc, opcode, rom):
        #0100 1011 kkkk yyyy k-RAM[y] 2 2 C Z Z'
        opcode = opcode << 8 | rom.getByte(pc + 1)
        k = opcode >> 4 & 0x000F
        y = opcode & 0x000F
        return (pc + 2,), (2, opcode, "cmp " + self._nibblebase % k + ", RAM[" + self._nibblebase % y + "]")
        
    def _exhl_x(self, pc, opcode, rom):
        #0100 1100 xxxx xx00 LR«RAM[x], HR«RAM[x+1] 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        x = opcode & 0x00FF
        return (pc + 2,), (2, opcode, "exhl RAM[" + self._bytebase % x + "]")
        
    def _rti(self, pc, opcode, rom):
        #0100 1101 SP¬SP+1,FLAG.PC 1 2 * * * ¬STACK[SP],EIF ¬1
        return (pc,), (1, opcode, "rti")
        
    def _ldhl_x(self, pc, opcode, rom):
        #0100 1110 xxxx xx00 LR¬RAM[x],HR¬RAM[x+1] 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        x = opcode & 0x00FF
        return (pc + 2,), (2, opcode, "ldhl RAM[" + self._bytebase % x + "]")
        
    def _ret(self, pc, opcode, rom):
        #0100 1111 SP¬SP + 1, PC¬STACK[SP] 1 2 - - -
        return (pc,), (1, opcode, "ret")
        
    def _rlca(self, pc, opcode, rom):
        #0101 0000 ¬CF¬Acc¬ 1 1 C Z C'
        return (pc + 1,), (1, opcode, "rlca")
        
    def _rrca(self, pc, opcode, rom):
        #0101 0001 ®CF®Acc® 1 1 C Z C'
        return (pc + 1,), (1, opcode, "rrca")
        
    def _ttcfs(self, pc, opcode, rom):
        #0101 0010 SF¬CF, CF¬1 1 1 1 - *
        return (pc + 1,), (1, opcode, "ttcfs")
        
    def _tfcfc(self, pc, opcode, rom):
        #0101 0011 SF¬CF', CF¬0 1 1 0 - *
        return (pc + 1,), (1, opcode, "tfcfc")
        
    def _slbr1_a(self, pc, opcode, rom):
        #0101 0101 1100 aaaa aaaa aaaa (a:1000h~1FFFh) SF=1; PC ¬ a ( branch condition satisified)
        opcode = opcode << 16 | rom.getWord(pc + 1)
        addr = 0x1000 | (opcode & 0x0FFF)
        return (pc + 3, addr), (3, opcode, "slbr " + self._addrbase % addr)

    def _slbr0_a(self, pc, opcode, rom):
        #0101 0111 1100 aaaa aaaa aaaa (a:0000h~0FFFh) SF=1; PC ¬ a ( branch condition satisified)
        opcode = opcode << 16 | rom.getWord(pc + 1)
        addr = opcode & 0x0FFF
        return (pc + 3, addr), (3, opcode, "slbr " + self._addrbase % addr)
            
    def _nop(self, pc, opcode, rom):
        #0101 0110 no operation 1 1 - - -
        return (pc + 1,), (1, opcode, "nop")
        
    def _exam(self, pc, opcode, rom):
        #0101 1000 Acc«RAM[HL] 1 1 - Z 1
        return (pc + 1,), (1, opcode, "exam")
        
    def _stam(self, pc, opcode, rom):
        #0101 1001 RAM[HL]¬Acc 1 1 - - 1
        return (pc + 1,), (1, opcode, "stam")
        
    def _ldam(self, pc, opcode, rom):
        #0101 1010 Acc ¬RAM[HL] 1 1 - Z 1
        return (pc + 1,), (1, opcode, "ldam")
        
    def _tzs(self, pc, opcode, rom):
        #0101 1011 SF¬ZF 1 1 - - *
        return (pc + 1,), (1, opcode, "tzs")
        
    def _deca(self, pc, opcode, rom):
        #0101 1100 Acc¬Acc-1 1 1 - Z C
        return (pc + 1,), (1, opcode, "deca")
        
    def _decm(self, pc, opcode, rom):
        #0101 1101 RAM[HL]¬RAM[HL] -1 1 1 - Z C
        return (pc + 1,), (1, opcode, "decm")
        
    def _inca(self, pc, opcode, rom):
        #0101 1110 Acc¬Acc + 1 1 1 - Z C'
        return (pc + 1,), (1, opcode, "inca")
        
    def _incm(self, pc, opcode, rom):
        #0101 1111 RAM[HL]¬RAM[HL]+1 1 1 - Z C'
        return (pc + 1,), (1, opcode, "incm")
        
    def _clpl(self, pc, opcode, rom):
        #0110 0000 PORT[LR3-2+4]LR1-0¬0 1 2 - - 1
        return (pc + 1,), (1, opcode, "clpl")
        
    def _tfpl(self, pc, opcode, rom):
        #0110 0001 SF¬PORT[LR 3-2 +4]LR1-0' 1 2 - - *
        return (pc + 1,), (1, opcode, "tfpl")
        
    def _sepl(self, pc, opcode, rom):
        #0110 0010 PORT[LR3-2+4]LRl-0¬1 1 2 - - 1
        return (pc + 1,), (1, opcode, "sepl")
        
    def _cil(self, pc, opcode, rom):
        #0110 0011
        id = rom.getByte(pc + 1) >> 6 & 0x03
        return self._instructions_cil[id](self, pc, opcode, rom)
        
    def _cil_r(self, pc, opcode, rom):
        #0110 0011 11rr rrrr IL¬IL & r 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        r = opcode & 0x003F
        return (pc + 2,), (2, opcode, "cil " + self._bytebase % r)
    
    def _dicil_r(self, pc, opcode, rom):
        #0110 0011 10rr rrrr EIF¬0,IL¬IL&r 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        r = opcode & 0x003F
        return (pc + 2,), (2, opcode, "dicil " + self._bytebase % r)
    
    def _eicil_r(self, pc, opcode, rom):
        #0110 0011 01rr rrrr EIF¬1,IL¬IL&r 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        r = opcode & 0x003F
        return (pc + 2,), (2, opcode, "eicil " + self._bytebase % r)
                    
    def _exal(self, pc, opcode, rom):
        #0110 0100 Acc«LR 1 2 - Z 1
        return (pc + 1,), (1, opcode, "exal")
        
    def _ldax(self, pc, opcode, rom):
        #0110 0101 Acc¬ROM[DP]L 1 2 - Z 1
        return (pc + 1,), (1, opcode, "ldax")
        
    def _exah(self, pc, opcode, rom):
        #0110 0110 Acc«HR 1 2 - Z 1
        return (pc + 1,), (1, opcode, "exah")
        
    def _ldaxi(self, pc, opcode, rom):
        #0110 0111 Acc¬ROM[DP]H,DP+1 1 2 - Z 1
        return (pc + 1,), (1, opcode, "ldaxi")
        
    def _exa_x(self, pc, opcode, rom):
        #0110 1000 xxxx xxxx Acc«RAM[x] 2 2 - Z 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        x = opcode & 0x00FF
        return (pc + 2,), (2, opcode, "exa RAM[" + self._bytebase % x + "]")
        
    def _sta_x(self, pc, opcode, rom):
        #0110 1001 xxxx xxxx RAM[x]¬Acc 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        x = opcode & 0x00FF
        if (x < 0xF4):
            return (pc + 2,), (2, opcode, "sta RAM[" + self._bytebase % x + "]")
        elif (x == 0xF4):
            return (pc + 2,), (2, opcode, "STATAL")
        elif (x == 0xF5):
            return (pc + 2,), (2, opcode, "STATAM")
        elif (x == 0xF6):
            return (pc + 2,), (2, opcode, "STATAH")
        elif (x == 0xF8):
            return (pc + 2,), (2, opcode, "STATBL")
        elif (x == 0xF9):
            return (pc + 2,), (2, opcode, "STATBM")
        elif (x == 0xFA):
            return (pc + 2,), (2, opcode, "STATBH")
        elif (x == 0xFC):
            return (pc + 2,), (2, opcode, "STADPL")
        elif (x == 0xFD):
            return (pc + 2,), (2, opcode, "STADPM")
        elif (x == 0xFE):
            return (pc + 2,), (2, opcode, "STADPH")
        elif (x == 0xFF):
            return (pc + 2,), (2, opcode, "STASP")
        else:
            return (pc + 2,), (2, opcode, "dw " + self._wordbase % opcode)
        
    def _lda_x(self, pc, opcode, rom):
        #0110 1010 xxxx xxxx Acc¬RAM[x] 2 2 - Z 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        x = opcode & 0x00FF
        if (x < 0xF4):
            return (pc + 2,), (2, opcode, "lda RAM[" + self._bytebase % x + "]")
        elif (x == 0xF4):
            return (pc + 2,), (2, opcode, "LDATAL")
        elif (x == 0xF5):
            return (pc + 2,), (2, opcode, "LDATAM")
        elif (x == 0xF6):
            return (pc + 2,), (2, opcode, "LDATAH")
        elif (x == 0xF8):
            return (pc + 2,), (2, opcode, "LDATBL")
        elif (x == 0xF9):
            return (pc + 2,), (2, opcode, "LDATBM")
        elif (x == 0xFA):
            return (pc + 2,), (2, opcode, "LDATBH")
        elif (x == 0xFC):
            return (pc + 2,), (2, opcode, "LDADPL")
        elif (x == 0xFD):
            return (pc + 2,), (2, opcode, "LDADPM")
        elif (x == 0xFE):
            return (pc + 2,), (2, opcode, "LDADPH")
        elif (x == 0xFF):
            return (pc + 2,), (2, opcode, "LDASP")
        else:
            return (pc + 2,), (2, opcode, "dw " + self._wordbase % opcode)
        
    def _cmpa_x(self, pc, opcode, rom):
        #0110 1011 xxxx xxxx RAM[x]-Acc 2 2 C Z Z'
        opcode = opcode << 8 | rom.getByte(pc + 1)
        x = opcode & 0x00FF
        return (pc + 2,), (2, opcode, "cmpa RAM[" + self._bytebase % x + "]")
        
    def _bit_y_b(self, pc, opcode, rom):
        #0110 1100
        id = rom.getByte(pc + 1) >> 6 & 0x03
        return self._instructions_bit_y_b[id](self, pc, opcode, rom)
    
    def _tf_y_b(self, pc, opcode, rom):
        #0110 1100 00bb yyyy SF¬RAM[y]b' 2 2 - - *
        opcode = opcode << 8 | rom.getByte(pc + 1)
        b = opcode >> 4 & 0x03
        y = opcode & 0x0F
        return (pc + 2,), (2, opcode, "tf RAM[" + self._nibblebase % y + "]" + "%X" % b)

    def _set_y_b(self, pc, opcode, rom):
        #0110 1100 01bb yyyy RAM[y]b¬1 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        b = opcode >> 4 & 0x03
        y = opcode & 0x0F
        return (pc + 2,), (2, opcode, "set RAM[" + self._nibblebase % y + "]" + "%X" % b)

    def _tt_y_b(self, pc, opcode, rom):
        #0110 1100 10bb yyyy SF¬RAM[y]b 2 2 - - *
        opcode = opcode << 8 | rom.getByte(pc + 1)
        b = opcode >> 4 & 0x03
        y = opcode & 0x0F
        return (pc + 2,), (2, opcode, "tt RAM[" + self._nibblebase % y + "]" + "%X" % b)

    def _clr_y_b(self, pc, opcode, rom):
        #0110 1100 11bb yyyy RAM[y]b¬0 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        b = opcode >> 4 & 0x03
        y = opcode & 0x0F
        return (pc + 2,), (2, opcode, "clr RAM[" + self._nibblebase % y + "]" + "%X" % b)

    def _bit_p_b(self, pc, opcode, rom):
        #0110 1101
        id = rom.getByte(pc + 1) >> 6 & 0x03
        return self._instructions_bit_p_b[id](self, pc, opcode, rom)
    
    def _tfp_p_b(self, pc, opcode, rom):
        #0110 1101 00bb pppp SF¬PORT[p]b' 2 2 - - *
        opcode = opcode << 8 | rom.getByte(pc + 1)
        b = opcode >> 4 & 0x03
        p = opcode & 0x0F
        return (pc + 2,), (2, opcode, "tfp PORT[" + self._portbase % p + "]" + "%X" % b)

    def _sep_p_b(self, pc, opcode, rom):
        #0110 1101 01bb pppp PORT[p]b¬1 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        b = opcode >> 4 & 0x03
        p = opcode & 0x0F
        return (pc + 2,), (2, opcode, "sep PORT[" + self._portbase % p + "]" + "%X" % b)

    def _ttp_p_b(self, pc, opcode, rom):
        #0110 1101 10bb pppp SF¬PORT[p]b 2 2 - - *
        opcode = opcode << 8 | rom.getByte(pc + 1)
        b = opcode >> 4 & 0x03
        p = opcode & 0x0F
        return (pc + 2,), (2, opcode, "ttp PORT[" + self._portbase % p + "]" + "%X" % b)

    def _clp_p_b(self, pc, opcode, rom):
        #0110 1101 11bb pppp PORT[p]b¬0 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        b = opcode >> 4 & 0x03
        p = opcode & 0x0F
        return (pc + 2,), (2, opcode, "clp PORT[" + self._portbase % p + "]" + "%X" % b)

    def _math_k(self, pc, opcode, rom):
        #0110 1110
        id = rom.getByte(pc + 1) >> 4 & 0x0F
        return self._instructions_math_k[id](self, pc, opcode, rom)

    def _addl_k(self, pc, opcode, rom):
        #0110 1110 0001 kkkk LR¬LR+k 2 2 - Z C'
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "addl " + self._nibblebase % k)

    def _cmpl_k(self, pc, opcode, rom):
        #0110 1110 0011 kkkk k-LR 2 2 - Z C
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "cmpl " + self._nibblebase % k)

    def _ora_k(self, pc, opcode, rom):
        #0110 1110 0100 kkkk Acc¬Acc k 2 2 - Z Z'
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "ora " + self._nibblebase % k)

    def _adda_k(self, pc, opcode, rom):
        #0110 1110 0101 kkkk Acc¬Acc+k 2 2 - Z C'
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "adda " + self._nibblebase % k)

    def _anda_k(self, pc, opcode, rom):
        #0110 1110 0110 kkkk Acc¬Acc&k 2 2 - Z Z'
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "anda " + self._nibblebase % k)

    def _suba_k(self, pc, opcode, rom):
        #0110 1110 0111 kkkk Acc¬k-Acc 2 2 - Z C
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "suba " + self._nibblebase % k)

    def _addh_k(self, pc, opcode, rom):
        #0110 1110 1001 kkkk HR¬HR+k 2 2 - Z C'
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "addh " + self._nibblebase % k)

    def _cmph_k(self, pc, opcode, rom):
        #0110 1110 1011 kkkk k - HR 2 2 - Z C
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "cmph " + self._nibblebase % k)

    def _orm_k(self, pc, opcode, rom):
        #0110 1110 1100 kkkk RAM[HL]¬RAM[HL] k 2 2 - Z Z'
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "orm " + self._nibblebase % k)

    def _addm_k(self, pc, opcode, rom):
        #0110 1110 1101 kkkk RAM[HL]¬RAM[HL] +k 2 2 - Z C'
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "addm " + self._nibblebase % k)

    def _andm_k(self, pc, opcode, rom):
        #0110 1110 1110 kkkk RAM[HL]¬RAM[HL]&k 2 2 - Z Z'
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "andm " + self._nibblebase % k)

    def _subm_k(self, pc, opcode, rom):
        #0110 1110 1111 kkkk RAM[HL]¬k - RAM[HL] 2 2 - Z C
        k = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "subm " + self._nibblebase % k)

    def _io_p(self, pc, opcode, rom):
        #0110 1111
        id = rom.getByte(pc + 1) >> 6 & 0x03
        return self._instructions_io_p[id](self, pc, opcode, rom)

    def _ina_p(self, pc, opcode, rom):
        #0110 1111 0100 pppp Acc¬PORT[p] 2 2 - Z Z'
        p = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "ina PORT[" + self._portbase % p + "]")
    
    def _inm_p(self, pc, opcode, rom):
        #0110 1111 1100 pppp RAM[HL]¬PORT[p] 2 2 - - Z'
        p = rom.getByte(pc + 1) & 0x0F
        return (pc + 2,), (2, opcode, "inm PORT[" + self._portbase % p + "]")

    def _outa_p(self, pc, opcode, rom):
        #0110 1111 000p pppp PORT[p]¬Acc 2 2 - - 1
        p = rom.getByte(pc + 1) & 0x1F
        return (pc + 2,), (2, opcode, "outa PORT[" + self._portbase % p + "]")

    def _outm_p(self, pc, opcode, rom):
        #0110 1111 100p pppp PORT[p]¬RAM[HL] 2 2 - - 1
        p = rom.getByte(pc + 1) & 0x1F
        return (pc + 2,), (2, opcode, "outm PORT[" + self._portbase % p + "]")

    def _adcam(self, pc, opcode, rom):
        #0111 0000 Acc¬Acc + RAM[HL] + CF 1 1 C Z C'
        return (pc + 1,), (1, opcode, "adcam")
        
    def _addam(self, pc, opcode, rom):
        #0111 0001 Acc¬Acc + RAM[HL] 1 1 - Z C'
        return (pc + 1,), (1, opcode, "addam")
        
    def _sbcam(self, pc, opcode, rom):
        #0111 0010 Acc¬RAM[HLl - Acc - CF' 1 1 C Z C
        return (pc + 1,), (1, opcode, "sbcam")
        
    def _cmpam(self, pc, opcode, rom):
        #0111 0011 RAM[HL] - Acc 1 1 C Z Z'
        return (pc + 1,), (1, opcode, "cmpam")
        
    def _tla(self, pc, opcode, rom):
        #0111 0100 Acc¬LR 1 1 - Z 1
        return (pc + 1,), (1, opcode, "tla")
        
    def _exae(self, pc, opcode, rom):
        #0111 0101 MASK«Acc 1 1 - - 1
        return (pc + 1,), (1, opcode, "exae")
        
    def _tha(self, pc, opcode, rom):
        #0111 0110 Acc¬HR 1 1 - Z 1
        return (pc + 1,), (1, opcode, "tha")
        
    def _oram(self, pc, opcode, rom):
        #0111 1000 Acc ¬Acc RAM[HL] 1 1 - Z Z'
        return (pc + 1,), (1, opcode, "oram")
        
    def _xoram(self, pc, opcode, rom):
        #0111 1001 Acc¬Acc^RAM[HL] 1 1 - Z Z'
        return (pc + 1,), (1, opcode, "xoram")
        
    def _andam(self, pc, opcode, rom):
        #0111 1011 Acc¬Acc & RAM[HL] 1 1 - Z Z'
        return (pc + 1,), (1, opcode, "andam")
        
    def _decl(self, pc, opcode, rom):
        #0111 1100 LR¬LR-1 1 1 - Z C
        return (pc + 1,), (1, opcode, "decl")
        
    def _stamd(self, pc, opcode, rom):
        #0111 1101 RAM[HL]¬Acc, LR-1 1 1 - Z C
        return (pc + 1,), (1, opcode, "stamd")
        
    def _incl(self, pc, opcode, rom):
        #0111 1110 LR¬LR + 1 1 1 - Z C'
        return (pc + 1,), (1, opcode, "incl")
        
    def _stami(self, pc, opcode, rom):
        #0111 1111 RAM[HL]¬Acc, LR+1 1 1 - Z C'
        return (pc + 1,), (1, opcode, "stami")
        
    def _ldl_k(self, pc, opcode, rom):
        #1000 kkkk LR¬k 1 1 - - 1
        k = opcode & 0x0F
        return (pc + 1,), (1, opcode, "ldl " + self._nibblebase % k)
        
    def _ldh_k(self, pc, opcode, rom):
        #1001 kkkk HR¬k 1 1 - - 1
        k = opcode & 0x0F
        return (pc + 1,), (1, opcode, "ldh " + self._nibblebase % k)
        
    def _stdmi_k(self, pc, opcode, rom):
        #1010 kkkk RAM[HL]¬k, LR+1 1 1 - Z C'
        k = opcode & 0x0F
        return (pc + 1,), (1, opcode, "stdmi " + self._nibblebase % k)
        
    def _cmpia_k(self, pc, opcode, rom):
        #1011 kkkk k - Acc 1 1 C Z Z'
        k = opcode & 0x0F
        return (pc + 1,), (1, opcode, "cmpia " + self._nibblebase % k)
        
    def _lbr_a(self, pc, opcode, rom):
        #1100 aaaa aaaa aaaa If SF= 1 then PC¬a else null 2 2 - - 1
        opcode = opcode << 8 | rom.getByte(pc + 1)
        addr = (pc & 0x1000) | (opcode & 0x0FFF)
        return (pc + 2, addr), (2, opcode, "lbr " + self._addrbase % addr)
        
    def _ldia_k(self, pc, opcode, rom):
        #1101 kkkk Acc¬k 1 1 - Z 1
        k = opcode & 0x0F
        return (pc + 1,), (1, opcode, "ldia " + self._nibblebase % k)
        
    def _scall_a(self, pc, opcode, rom):
        #1110 nnnn STACK[SP]¬PC, 1 2 - - - SP¬SP - 1, PC¬a, a = 8n + 6 (n =1~15),0086h (n = 0)
        n = opcode & 0x0F
        addr = n * 8 + 6 + (0x80 * (n == 0))
        return (pc + 1,), (1, opcode, "scall " + self._addrbase % addr)
        
    def _clm_b(self, pc, opcode, rom):
        #1111 00bb RAM[HL]b¬0 1 1 - - 1
        b = opcode & 0x03
        return (pc + 1,), (1, opcode, "clm " + self._nibblebase % b)
        
    def _sem_b(self, pc, opcode, rom):
        #1111 01bb RAM[HL]b¬1 1 1 - - 1
        b = opcode & 0x03
        return (pc + 1,), (1, opcode, "sem " + self._nibblebase % b)
        
    def _tfa_b(self, pc, opcode, rom):
        #1111 10bb SF¬Accb' 1 1 - - *
        b = opcode & 0x03
        return (pc + 1,), (1, opcode, "tfa " + self._nibblebase % b)
        
    def _tfm_b(self, pc, opcode, rom):
        #1111 11bb SF¬RAM[HL]b' 1 1 - - *
        b = opcode & 0x03
        return (pc + 1,), (1, opcode, "tfm " + self._nibblebase % b)
        
    def _dummy(self, pc, opcode, rom):
        return (pc + 1,), (1, opcode, "db " + self._bytebase % opcode)

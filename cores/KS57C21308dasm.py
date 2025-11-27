class KS57C21308dasm():

    def __init__(self):
        self._base = '0x%X'
        self._nibbase = '0x%0.1X'
        self._bytebase = '0x%0.2X'
        self._rambase = '0x%0.3X'
        self._addrbase = '%00.4X'
        self._opbase = '%0.3X'

        self._reg_tbl = (
            "A",
            "E",
            "L",
            "H",
            "X",
            "W",
            "Z",
            "Y"
        )

        self._rpe_tbl = (
            "EA",
            "EA'",
            "HL",
            "HL'",
            "WX",
            "WX'",
            "YZ",
            "YZ'"
        )

        self._clr_fmem_tbl = {
            0b10110010: "di",
            0b10011000: "di IEBT",
            0b10011010: "di IEW",
            0b10011011: "di IETPG",
            0b10011100: "di IET0",
            0b10011101: "di IEP0",
            0b10011110: "di IE0",
            0b10011111: "di IE2",
            0b10111000: "di IE4",
            0b10111011: "di IEKS",
            0b10111110: "di IE1"
        }

        self._set_fmem_tbl = {
            0b10110010: "ei",
            0b10100011: "halt",
            0b10110011: "stop",
            0b10011000: "ei IEBT",
            0b10011010: "ei IEW",
            0b10011011: "ei IETPG",
            0b10011100: "ei IET0",
            0b10011101: "ei IEP0",
            0b10011110: "ei IE0",
            0b10011111: "ei IE2",
            0b10111000: "ei IE4",
            0b10111011: "ei IEKS",
            0b10111110: "ei IE1"
        }

        self._instruction_tbl = (
            *([KS57C21308dasm._br_mraddr] * 16),           #0000AAAA
            *([KS57C21308dasm._br_raddr] * 16),            #0001AAAA
            *([KS57C21308dasm._ref] * 8),                  #00100XXX
            KS57C21308dasm._pop_ea,                        #00101000
            KS57C21308dasm._push_ea,                       #00101001
            KS57C21308dasm._pop_hl,                        #00101010
            KS57C21308dasm._push_hl,                       #00101011
            KS57C21308dasm._pop_wx,                        #00101100
            KS57C21308dasm._push_wx,                       #00101101
            KS57C21308dasm._pop_yz,                        #00101110
            KS57C21308dasm._push_yz,                       #00101111
            *([KS57C21308dasm._ref] * 8),                  #00110XXX
            KS57C21308dasm._cpse_a_ahl,                    #00111000 
            KS57C21308dasm._and_a_ahl,                     #00111001
            KS57C21308dasm._or_a_ahl,                      #00111010
            KS57C21308dasm._xor_a_ahl,                     #00111011
            KS57C21308dasm._sbc_a_ahl,                     #00111100
            KS57C21308dasm._sbs_a_ahl,                     #00111101
            KS57C21308dasm._adc_a_ahl,                     #00111110
            KS57C21308dasm._ads_a_ahl,                     #00111111
            *([KS57C21308dasm._ref] * 8),                  #01000XXX
            *([KS57C21308dasm._decs_r] * 8),               #01001RRR
            *([KS57C21308dasm._ref] * 8),                  #01010XXX
            *([KS57C21308dasm._incs_r] * 8),               #01011RRR
            *([KS57C21308dasm._ref] * 8),                  #01100XXX
            *([KS57C21308dasm._xch_a_ra] * 8),             #01101RRR
            *([KS57C21308dasm._ref] * 8),                  #01110XXX
            KS57C21308dasm._dummy,                         #01111000
            KS57C21308dasm._xch_a_da,                      #01111001 AAAAAAAA
            KS57C21308dasm._xchi_a_ahl,                    #01111010
            KS57C21308dasm._xchd_a_ahl,                    #01111011
            KS57C21308dasm._dummy,                         #01111100
            KS57C21308dasm._xch_a_ahl,                     #01111101
            KS57C21308dasm._xch_a_awx,                     #01111110
            KS57C21308dasm._xch_a_awl,                     #01111111
            KS57C21308dasm._dummy,                         #10000000
            KS57C21308dasm._ld_ea_imm,                     #10000001 DDDDDDDD
            KS57C21308dasm._incs_hl,                       #10000010
            KS57C21308dasm._ld_hl_imm,                     #10000011 DDDDDDDD
            KS57C21308dasm._incs_wx,                       #10000100
            KS57C21308dasm._ld_wx_imm,                     #10000101 DDDDDDDD
            KS57C21308dasm._incs_yz,                       #10000110
            KS57C21308dasm._ld_yz_imm,                     #10000111 DDDDDDDD
            KS57C21308dasm._rrc_a,                         #10001000
            KS57C21308dasm._ld_da_a,                       #10001001 AAAAAAAA
            KS57C21308dasm._ldi_a_ahl,                     #10001010
            KS57C21308dasm._ldd_a_ahl,                     #10001011
            KS57C21308dasm._ld_a_da,                       #10001100 AAAAAAAA
            KS57C21308dasm._ld_a_ahl,                      #10001101
            KS57C21308dasm._ld_a_awx,                      #10001110
            KS57C21308dasm._ld_a_awl,                      #10001111
            *([KS57C21308dasm._jps_addr12] * 16),          #1001AAAA AAAAAAAA
            *([KS57C21308dasm._ads_a_im] * 16),            #1010DDDD
            *([KS57C21308dasm._ld_a_im] * 16),             #1011DDDD
            KS57C21308dasm._bitr_da_bit,                   #11000000 AAAAAAAA
            KS57C21308dasm._bits_da_bit,                   #11000001 AAAAAAAA
            KS57C21308dasm._btsf_da_bit,                   #11000010 AAAAAAAA
            KS57C21308dasm._btst_da_bit,                   #11000011 AAAAAAAA
            KS57C21308dasm._ld_ahl_a,                      #11000100
            KS57C21308dasm._ret,                           #11000101
            KS57C21308dasm._dummy,                         #11000110
            KS57C21308dasm._dummy,                         #11000111
            KS57C21308dasm._ldc_ea_aea,                    #11001000
            KS57C21308dasm._ads_ea_imm,                    #11001001 DDDDDDDD
            KS57C21308dasm._incs_da,                       #11001010 AAAAAAAA
            KS57C21308dasm._dummy,                         #11001011
            KS57C21308dasm._ldc_ea_awx,                    #11001100
            KS57C21308dasm._ld_da_ea,                      #11001101 AAAAAAAA
            KS57C21308dasm._ld_ea_da,                      #11001110 AAAAAAAA
            KS57C21308dasm._xch_ea_da,                     #11001111 AAAAAAAA
            KS57C21308dasm._bitr_da_bit,                   #11010000 AAAAAAAA
            KS57C21308dasm._bits_da_bit,                   #11010001 AAAAAAAA
            KS57C21308dasm._btsf_da_bit,                   #11010010 AAAAAAAA
            KS57C21308dasm._btst_da_bit,                   #11010011 AAAAAAAA
            KS57C21308dasm._dummy,                         #11010100
            KS57C21308dasm._iret,                          #11010101
            KS57C21308dasm._ccf,                           #11010110
            KS57C21308dasm._btst_cy,                       #11010111
            KS57C21308dasm._dummy,                         #11011000
            KS57C21308dasm._instruction_11011001,          #11011001
            KS57C21308dasm._dummy,                         #11011010
            KS57C21308dasm._instruction_11011011,          #11011011
            KS57C21308dasm._instruction_11011100,          #11011100
            KS57C21308dasm._instruction_11011101,          #11011101
            KS57C21308dasm._dummy,                         #11011110
            KS57C21308dasm._dummy,                         #11011111
            KS57C21308dasm._bitr_da_bit,                   #11100000 AAAAAAAA
            KS57C21308dasm._bits_da_bit,                   #11100001 AAAAAAAA
            KS57C21308dasm._btsf_da_bit,                   #11100010 AAAAAAAA
            KS57C21308dasm._btst_da_bit,                   #11100011 AAAAAAAA
            KS57C21308dasm._dummy,                         #11100100
            KS57C21308dasm._sret,                          #11100101
            KS57C21308dasm._bitr_cy,                       #11100110
            KS57C21308dasm._bits_cy,                       #11100111
            *([KS57C21308dasm._calls_addr11] * 8),         #11101AAA AAAAAAAA
            KS57C21308dasm._bitr_da_bit,                   #11110000 AAAAAAAA
            KS57C21308dasm._bits_da_bit,                   #11110001 AAAAAAAA
            KS57C21308dasm._btsf_da_bit,                   #11110010 AAAAAAAA
            KS57C21308dasm._btst_da_bit,                   #11110011 AAAAAAAA
            KS57C21308dasm._instruction_11110100,          #11110100
            KS57C21308dasm._instruction_11110101,          #11110101
            KS57C21308dasm._instruction_11110110,          #11110110
            KS57C21308dasm._instruction_11110111,          #11110111
            KS57C21308dasm._instruction_11111000,          #11111000
            KS57C21308dasm._instruction_11111001,          #11111001
            KS57C21308dasm._dummy,                         #11111010
            KS57C21308dasm._dummy,                         #11111011
            KS57C21308dasm._instruction_11111100,          #11111100
            KS57C21308dasm._instruction_11111101,          #11111101
            KS57C21308dasm._instruction_11111110,          #11111110
            KS57C21308dasm._instruction_11111111,          #11111111
        )

        self._instruction_11011001_tbl = (
            KS57C21308dasm._cpse_r_im,                     #11011001 DDDD0RRR
            KS57C21308dasm._ld_ra_im                       #11011001 DDDD1RRR
        )

        self._instruction_11011011_tbl = (
            KS57C21308dasm._jp_addr14,                     #11011011 00AAAAAA AAAAAAAA
            KS57C21308dasm._call_addr14                    #11011011 01AAAAAA AAAAAAAA
        )
        
        self._instruction_11011100_tbl = (
            KS57C21308dasm._ld_ahl_ea,                     #11011100 00000000
            KS57C21308dasm._xch_ea_ahl,                    #11011100 00000001
            *([KS57C21308dasm._dummy] * 6),
            KS57C21308dasm._ld_ea_ahl,                     #11011100 00001000
            KS57C21308dasm._cpse_ea_ahl,                   #11011100 00001001
            *([KS57C21308dasm._dummy] * 6),
            *([KS57C21308dasm._and_rrb_ea] * 8),           #11011100 00010RR0
            *([KS57C21308dasm._and_ea_rr] * 8),            #11011100 00011RR0
            *([KS57C21308dasm._or_rrb_ea] * 8),            #11011100 00100RR0
            *([KS57C21308dasm._or_ea_rr] * 8),             #11011100 00101RR0
            *([KS57C21308dasm._xor_rrb_ea] * 8),           #11011100 00110RR0
            *([KS57C21308dasm._xor_ea_rr] * 8),            #11011100 00111RR0
            *([KS57C21308dasm._dummy] * 64),               #11011100 01XXXXXX
            *([KS57C21308dasm._dummy] * 16),               #11011100 1000XXXX
            *([KS57C21308dasm._ads_rrb_ea] * 8),           #11011100 10010RR0
            *([KS57C21308dasm._ads_ea_rr] * 8),            #11011100 10011RR0
            *([KS57C21308dasm._adc_rrb_ea] * 8),           #11011100 10100RR0
            *([KS57C21308dasm._adc_ea_rr] * 8),            #11011100 10101RR0
            *([KS57C21308dasm._sbs_rrb_ea] * 8),           #11011100 10110RR0
            *([KS57C21308dasm._sbs_ea_rr] * 8),            #11011100 10111RR0
            *([KS57C21308dasm._sbc_rrb_ea] * 8),           #11011100 11000RR0
            *([KS57C21308dasm._sbc_ea_rr] * 8),            #11011100 11001RR0
            *([KS57C21308dasm._dummy] * 8),                #11011100 11010XXX
            *([KS57C21308dasm._decs_rr] * 8),              #11011100 11011RR0
            *([KS57C21308dasm._xch_ea_rrb] * 8),           #11011100 11100RR0
            *([KS57C21308dasm._cpse_ea_rr] * 8),           #11011100 11101RR0
            *([KS57C21308dasm._ld_rrb_ea] * 8),            #11011100 11110RR0
            *([KS57C21308dasm._ld_ea_rrb] * 8),            #11011100 11111RR0
        )
        
        self._instruction_11011101_tbl = (
            *([KS57C21308dasm._ld_ra_a] * 8),              #11011101 00000RRR
            *([KS57C21308dasm._ld_a_r] * 8),               #11011101 00001RRR
            *([KS57C21308dasm._and_a_im] * 16),            #11011101 0001DDDD
            *([KS57C21308dasm._or_a_im] * 16),             #11011101 0010DDDD
            *([KS57C21308dasm._xor_a_im] * 16),            #11011101 0011DDDD
            *([KS57C21308dasm._smb_n] * 16),               #11011101 0100NNNN
            *([KS57C21308dasm._srb_n] * 4),                #11011101 010100NN
            *([KS57C21308dasm._dummy] * 4),                #11011101 010101XX
            *([KS57C21308dasm._dummy] * 8),                #11011101 01011XXX
            KS57C21308dasm._jr_aea,                        #11011101 01100000
            KS57C21308dasm._dummy,                         #11011101 01100001
            KS57C21308dasm._incs_ahl,                      #11011101 01100010
            KS57C21308dasm._dummy,                         #11011101 01100011
            KS57C21308dasm._jr_awx,                        #11011101 01100100
            KS57C21308dasm._dummy,                         #11011101 01100101
            KS57C21308dasm._pop_sb,                        #11011101 01100110
            KS57C21308dasm._push_sb,                       #11011101 01100111
            *([KS57C21308dasm._cpse_a_r] * 8),             #11011101 01101RRR
            *([KS57C21308dasm._cpse_ahl_im] * 16),         #11011101 0111DDDD
            *([KS57C21308dasm._dummy] * 128),              #11011101 1XXXXXXX
        )
        
        self._instruction_11110101_tbl = (
            KS57C21308dasm._band_cy_ahda_bit,              #11110101 00BBAAAA
            KS57C21308dasm._band_cy_memb_al,               #11110101 0100AAAA
            KS57C21308dasm._band_cy_mema_bit,              #11110101 10BBAAAA
            KS57C21308dasm._band_cy_mema_bit               #11110101 11BBAAAA
        )
        
        self._instruction_11110110_tbl = (
            KS57C21308dasm._bor_cy_ahda_bit,               #11110110 00BBAAAA
            KS57C21308dasm._bor_cy_memb_al,                #11110110 0100AAAA
            KS57C21308dasm._bor_cy_mema_bit,               #11110110 10BBAAAA
            KS57C21308dasm._bor_cy_mema_bit                #11110110 11BBAAAA
        )

        self._instruction_11110111_tbl = (
            KS57C21308dasm._bxor_cy_ahda_bit,              #11110111 00BBAAAA
            KS57C21308dasm._bxor_cy_memb_al,               #11110111 0100AAAA
            KS57C21308dasm._bxor_cy_mema_bit,              #11110111 10BBAAAA
            KS57C21308dasm._bxor_cy_mema_bit               #11110111 11BBAAAA
        )
        
        self._instruction_11110100_tbl = (
            KS57C21308dasm._ldb_cy_ahda_bit,               #11110100 00BBAAAA
            KS57C21308dasm._ldb_cy_memb_al,                #11110100 0100AAAA
            KS57C21308dasm._ldb_cy_mema_bit,               #11110100 10BBAAAA
            KS57C21308dasm._ldb_cy_mema_bit                #11110100 11BBAAAA
        )
        
        self._instruction_11111000_tbl = (
            KS57C21308dasm._btsf_ahda_bit,                 #11111000 00BBAAAA
            KS57C21308dasm._btsf_memb_al,                  #11111000 0100AAAA
            KS57C21308dasm._btsf_mema_bit,                 #11111000 10BBAAAA
            KS57C21308dasm._btsf_mema_bit                  #11111000 11BBAAAA
        )

        self._instruction_11111001_tbl = (
            KS57C21308dasm._btst_ahda_bit,                 #11111001 00BBAAAA
            KS57C21308dasm._btst_memb_al,                  #11111001 0100AAAA
            KS57C21308dasm._btst_mema_bit,                 #11111001 10BBAAAA
            KS57C21308dasm._btst_mema_bit                  #11111001 11BBAAAA
        )
                
        self._instruction_11111100_tbl = (
            KS57C21308dasm._ldb_ahda_bit_cy,               #11111100 00BBAAAA
            KS57C21308dasm._ldb_memb_al_cy,                #11111100 0100AAAA
            KS57C21308dasm._ldb_mema_bit_cy,               #11111100 10BBAAAA
            KS57C21308dasm._ldb_mema_bit_cy                #11111100 11BBAAAA
        )
        
        self._instruction_11111110_tbl = (
            KS57C21308dasm._bitr_ahda_bit,                 #11111110 00BBAAAA
            KS57C21308dasm._bitr_memb_al,                  #11111110 0100AAAA
            KS57C21308dasm._bitr_mema_bit,                 #11111110 10BBAAAA
            KS57C21308dasm._bitr_mema_bit                  #11111110 11BBAAAA
        )
        
        self._instruction_11111111_tbl = (
            KS57C21308dasm._bits_ahda_bit,                 #11111111 00BBAAAA
            KS57C21308dasm._bits_memb_al,                  #11111111 0100AAAA
            KS57C21308dasm._bits_mema_bit,                 #11111111 10BBAAAA
            KS57C21308dasm._bits_mema_bit                  #11111111 11BBAAAA
        )

        self._instruction_11111101_tbl = (
            KS57C21308dasm._btstz_ahda_bit,                #11111101 00BBAAAA
            KS57C21308dasm._btstz_memb_al,                 #11111101 0100AAAA
            KS57C21308dasm._btstz_mema_bit,                #11111101 10BBAAAA
            KS57C21308dasm._btstz_mema_bit                 #11111101 11BBAAAA
        )


    def disassemble(self, rom):
        if (rom.size() > 0):
            listing = [None] * rom.size()
            vector = rom.getWord(0) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(2) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(4) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(6) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(8) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(10) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)

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
                result += (self._addrbase % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(35) + "\n"
        with open(file_path, 'w') as f:
            f.write(result)
    
    def _disassemble(self, pc, listing, rom):
        while (pc > 0 and pc < len(listing) and listing[pc] is None):
            opcode = rom.getByte(pc)
            next_pcs, listing[pc] = self._instruction_tbl[opcode](self, pc, opcode, rom)
            instruction_size = listing[pc][0]
            while (instruction_size > 1  and (pc + 1) < len(listing)):
                instruction_size -= 1
                pc += 1
                listing[pc] = (1, rom.getByte(pc), '')
            prev_pc = pc
            pc = next_pcs[0]
            if (self._instruction_tbl[opcode] == KS57C21308dasm._ref):
                listing = self._disassemble_ref(pc, next_pcs[1], listing, rom)
                listing[prev_pc] = (listing[prev_pc][0], listing[prev_pc][1], listing[prev_pc][2] + "    ;" + listing[next_pcs[1]][2])
            elif (len(next_pcs) > 1):
                listing = self._disassemble(next_pcs[1], listing, rom)
                if (len(next_pcs) > 2):
                    listing = self._disassemble(next_pcs[2], listing, rom)
        return listing

    def _disassemble_ref(self, pc, ref_pc, listing, rom):
        opcode = rom.getByte(ref_pc)
        if ((opcode & 0xC0) == 0x00):
            opcode = rom.getWord(ref_pc)
            a = opcode & 0x3FFF
            listing[ref_pc] = (2, opcode, "tbr " + self._addrbase % a)
            listing[ref_pc + 1] = (1, opcode & 0xFF, '')
            listing = self._disassemble(a, listing, rom)
        elif ((opcode & 0xC0) == 0x40):
            opcode = rom.getWord(ref_pc)
            a = opcode & 0x3FFF
            listing[ref_pc] = (2, opcode, "tcall " + self._addrbase % a)
            listing[ref_pc + 1] = (1, opcode & 0xFF, '')
            listing = self._disassemble(a, listing, rom)
        else:
            _, listing[ref_pc] = self._instruction_tbl[opcode](self, ref_pc, opcode, rom)
            instruction_size = listing[ref_pc][0]
            ref_pc += 1
            if (instruction_size == 2):
                listing[ref_pc] = (1, rom.getByte(ref_pc), '')
            elif (instruction_size == 1):
                opcode = rom.getByte(ref_pc)
                _, listing[ref_pc] = self._instruction_tbl[opcode](self, ref_pc, opcode, rom)

            listing = self._disassemble(self._get_instr_skip_pc(pc, rom), listing, rom)
            
        return listing
        
    def _get_instr_skip_pc(self, pc, rom):
        opcode = rom.getByte(pc)
        _, desc = self._instruction_tbl[opcode](self, pc, opcode, rom)
        return pc + desc[0]

    def _instruction_11011011(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11011011_tbl[(op >> 6) & 0x1](self, pc, opcode, rom)

    def _instruction_11011101(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11011101_tbl[op & 0x7F](self, pc, opcode, rom)
        
    def _instruction_11011001(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11011001_tbl[(op >> 3) & 0x1](self, pc, opcode, rom)

    def _instruction_11111100(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11111100_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_11111110(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11111110_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_11111111(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11111111_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_11111101(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11111101_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_11011100(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11011100_tbl[op](self, pc, opcode, rom)

    def _instruction_11110101(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11110101_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_11110110(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11110110_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)
    
    def _instruction_11110111(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11110111_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_11110100(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11110100_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_11111000(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11111000_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_11111001(self, pc, opcode, rom):
        op = rom.getByte(pc + 1)
        return self._instruction_11111001_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _br_raddr(self, pc, opcode, rom):
        #0001AAAA
        a = pc + 1 + (opcode & 0x0F)
        return (a, ), (1, opcode, "br " + self._addrbase % a)

    def _br_mraddr(self, pc, opcode, rom):
        #0000AAAA
        a = pc - (15 - (opcode & 0x0F))
        return (a,), (1, opcode, "br " + self._addrbase % a)

    def _ref(self, pc, opcode, rom):
        #TTTTTTTT
        a = (opcode & 0xF0) | ((opcode << 1) & 0x0E)
        return (pc + 1, a), (1, opcode, "ref " + self._addrbase % a)

    def _calls_addr11(self, pc, opcode, rom):
        #11101AAA AAAAAAAA
        op = rom.getByte(pc + 1)
        a = ((opcode & 0x7) << 8) | op
        return (pc + 2, a, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "calls " + self._addrbase % a)

    def _pop_ea(self, pc, opcode, rom):
        #00101000
        return (pc + 1,), (1, opcode, "pop EA")

    def _push_ea(self, pc, opcode, rom):
        #00101001
        return (pc + 1,), (1, opcode, "push EA")

    def _pop_hl(self, pc, opcode, rom):
        #00101010
        return (pc + 1,), (1, opcode, "pop HL")

    def _push_hl(self, pc, opcode, rom):
        #00101011
        return (pc + 1,), (1, opcode, "push HL")

    def _pop_wx(self, pc, opcode, rom):
        #00101100
        return (pc + 1,), (1, opcode, "pop WX")

    def _push_wx(self, pc, opcode, rom):
        #00101101
        return (pc + 1,), (1, opcode, "push WX")

    def _pop_yz(self, pc, opcode, rom):
        #00101110
        return (pc + 1,), (1, opcode, "pop YZ")

    def _push_yz(self, pc, opcode, rom):
        #00101111
        return (pc + 1,), (1, opcode, "push YZ")

    def _jps_addr12(self, pc, opcode, rom):
        #1001AAAA AAAAAAAA
        op = rom.getByte(pc + 1)
        a = (pc & 0xF000) | ((opcode & 0xF) << 8) | op
        return (a,), (2, (opcode << 8) | op, "jps " + self._addrbase % a)

    def _ads_a_im(self, pc, opcode, rom):
        #1010DDDD
        i = opcode & 0xF
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, ("adds A, " + self._nibbase % i) if i else "nop")

    def _ld_a_im(self, pc, opcode, rom):
        #1011DDDD
        i = opcode & 0xF
        return (pc + 1,), (1, opcode, "ld A, " + self._nibbase % i)

    def _cpse_a_ahl(self, pc, opcode, rom):
        #00111000
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "cpse A, @HL")

    def _incs_da(self, pc, opcode, rom):
        #11001010 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "incs RAM[" + self._nibbase % op + "]")

    def _bitr_da_bit(self, pc, opcode, rom):
        #11BB0000 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "bitr RAM[" + self._nibbase % op + "].%d" % ((opcode >> 4) & 0x3))

    def _bits_da_bit(self, pc, opcode, rom):
        #11BB0001 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "bits RAM[" + self._nibbase % op + "].%d" % ((opcode >> 4) & 0x3))

    def _btsf_da_bit(self, pc, opcode, rom):
        #11BB0010 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btsf RAM[" + self._nibbase % op + "].%d" % ((opcode >> 4) & 0x3))

    def _btst_da_bit(self, pc, opcode, rom):
        #11BB0011 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btst RAM[" + self._nibbase % op + "].%d" % ((opcode >> 4) & 0x3))

    def _ld_ea_imm(self, pc, opcode, rom):
        #10000001 DDDDDDDD
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "ld EA, " + self._bytebase % op)

    def _incs_hl(self, pc, opcode, rom):
        #10000010
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "incs HL")

    def _ld_hl_imm(self, pc, opcode, rom):
        #10000011 DDDDDDDD
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "ld HL, " + self._bytebase % op)
        
    def _incs_wx(self, pc, opcode, rom):
        #10000100
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "incs WX")

    def _ld_wx_imm(self, pc, opcode, rom):
        #10000101 DDDDDDDD
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "ld WX, " + self._bytebase % op)

    def _incs_yz(self, pc, opcode, rom):
        #10000110
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "incs YZ")

    def _ld_yz_imm(self, pc, opcode, rom):
        #10000111 DDDDDDDD
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "ld YZ, " + self._bytebase % op)

    def _and_a_ahl(self, pc, opcode, rom):
        #00111001
        return (pc + 1,), (1, opcode, "and A, @HL")

    def _ld_da_ea(self, pc, opcode, rom):
        #11001101 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "ld RAM[" + self._bytebase % op + "], EA")

    def _ld_da_a(self, pc, opcode, rom):
        #10001001 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "ld RAM[" + self._bytebase % op + "], A")

    def _rrc_a(self, pc, opcode, rom):
        #10001000
        return (pc + 1,), (1, opcode, "rrc A")

    def _or_a_ahl(self, pc, opcode, rom):
        #00111010
        return (pc + 1,), (1, opcode, "or A, @HL")

    def _ld_ea_da(self, pc, opcode, rom):
        #11001110 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "ld EA, RAM[" + self._bytebase % op + "]")

    def _ld_a_da(self, pc, opcode, rom):
        #10001100 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "ld A, RAM[" + self._bytebase % op + "]")

    def _sbs_a_ahl(self, pc, opcode, rom):
        #00111101
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "sbs A, @HL")

    def _adc_a_ahl(self, pc, opcode, rom):
        #00111110
        return (pc + 1,), (1, opcode, "adc A, @HL")

    def _jp_addr14(self, pc, opcode, rom):
        #11011011 00AAAAAA AAAAAAAA
        a = rom.getWord(pc + 1)
        return (pc + 3, a), (3, (opcode << 16) | a, "br " + self._addrbase % a)

    def _call_addr14(self, pc, opcode, rom):
        #11011011 01AAAAAA AAAAAAAA
        a = rom.getWord(pc + 1) & 0x3FFF
        return (pc + 3, a, self._get_instr_skip_pc(pc + 2, rom)), (3, (opcode << 16) | a, "call " + self._addrbase % a)

    def _xor_a_ahl(self, pc, opcode, rom):
        #00111011
        return (pc + 1,), (1, opcode, "xor A, @HL")

    def _xch_ea_da(self, pc, opcode, rom):
        #11001111 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "xch EA, RAM[" + self._bytebase % op + "]")

    def _xch_a_da(self, pc, opcode, rom):
        #01111001 AAAAAAAA
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "xch A, RAM[" + self._bytebase % op + "]")

    def _sbc_a_ahl(self, pc, opcode, rom):
        #00111100
        return (pc + 1,), (1, opcode, "sbc A, @HL")

    def _ads_ea_imm(self, pc, opcode, rom):
        #11001001 DDDDDDDD
        op = rom.getByte(pc + 1)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "adds EA, " + self._bytebase % op)

    def _incs_r(self, pc, opcode, rom):
        #01011RRR
        r = opcode & 0x7
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "incs " + self._reg_tbl[r])

    def _decs_r(self, pc, opcode, rom):
        #101001RRR
        r = opcode & 0x7
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "decs " + self._reg_tbl[r])

    def _ldc_ea_aea(self, pc, opcode, rom):
        #11001000
        return (pc + 1,), (1, opcode, "ldc EA, @PCEA")

    def _ads_a_ahl(self, pc, opcode, rom):
        #00111111
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "ads A, @HL")

    def _ldc_ea_awx(self, pc, opcode, rom):
        #11001100
        return (pc + 1,), (1, opcode, "ldc EA, @PCWX")

    def _ccf(self, pc, opcode, rom):
        #11010110
        return (pc + 1,), (1, opcode, "not1 CY")

    def _btst_cy(self, pc, opcode, rom):
        #11010111
        return (pc + 1, self._get_instr_skip_pc(pc + 1, rom)), (1, opcode, "btst CY")

    def _xch_a_ra(self, pc, opcode, rom):
        #01101RRR
        r = opcode & 0x7
        return (pc + 1,), (1, opcode, "xch A, " + self._reg_tbl[r])

    def _sret(self, pc, opcode, rom):
        #11100101
        return (-1,), (1, opcode, "sret")

    def _ld_a_ahl(self, pc, opcode, rom):
        #10001101
        return (pc + 1,), (1, opcode, "ld A, @HL")

    def _ldi_a_ahl(self, pc, opcode, rom):
        #10001010
        return (pc + 1,), (1, opcode, "ldi A, @HL")

    def _ldd_a_ahl(self, pc, opcode, rom):
        #10001011
        return (pc + 1,), (1, opcode, "ldd A, @HL")

    def _ld_a_awx(self, pc, opcode, rom):
        #10001110
        return (pc + 1,), (1, opcode, "ld A, @WX")

    def _ld_a_awl(self, pc, opcode, rom):
        #10001111
        return (pc + 1,), (1, opcode, "ld A, @WL")

    def _bitr_cy(self, pc, opcode, rom):
        #11100110
        return (pc + 1,), (1, opcode, "bitr CY")

    def _bits_cy(self, pc, opcode, rom):
        #11100111
        return (pc + 1,), (1, opcode, "bits CY")

    def _ld_ahl_a(self, pc, opcode, rom):
        #11000100
        return (pc + 1,), (1, opcode, "ld @HL, A")

    def _xch_a_ahl(self, pc, opcode, rom):
        #01111101
        return (pc + 1,), (1, opcode, "xch A, @HL")

    def _xchi_a_ahl(self, pc, opcode, rom):
        #01111010
        return (pc + 1,), (1, opcode, "xchi A, @HL")

    def _xchd_a_ahl(self, pc, opcode, rom):
        #01111011
        return (pc + 1,), (1, opcode, "xchd A, @HL")

    def _xch_a_awx(self, pc, opcode, rom):
        #01111110
        return (pc + 1,), (1, opcode, "xch A, WX")

    def _xch_a_awl(self, pc, opcode, rom):
        #01111111
        return (pc + 1,), (1, opcode, "xch A, WL")

    def _ret(self, pc, opcode, rom):
        #11000101
        return (-1,), (1, opcode, "ret")

    def _iret(self, pc, opcode, rom):
        #11010101
        return (-1,), (1, opcode, "iret")

    def _jr_aea(self, pc, opcode, rom):
        #11011101 01100000
        return (pc + 2,), (2, (opcode << 8) | 0b01100000, "jr PCEA")

    def _incs_ahl(self, pc, opcode, rom):
        #11011101 01100010
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | 0b01100010, "incs @HL")

    def _jr_awx(self, pc, opcode, rom):
        #11011101 01100100
        return (pc + 2,), (2, (opcode << 8) | 0b01100100, "jr PCWX")

    def _pop_sb(self, pc, opcode, rom):
        #11011101 01100110
        return (pc + 2,), (2, (opcode << 8) | 0b01100110, "pop sb")

    def _push_sb(self, pc, opcode, rom):
        #11011101 01100111
        return (pc + 2,), (2, (opcode << 8) | 0b01100111, "push sb")

    def _cpse_a_r(self, pc, opcode, rom):
        #11011101 01101RRR
        op = rom.getByte(pc + 1)
        r = op & 0x7
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "cpse A, " + self._reg_tbl[r])

    def _smb_n(self, pc, opcode, rom):
        #11011101 0100NNNN
        op = rom.getByte(pc + 1)
        n = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "smb " + str(n))

    def _srb_n(self, pc, opcode, rom):
        #11011101 010100NN
        op = rom.getByte(pc + 1)
        n = op & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "srb " + str(n))

    def _and_a_im(self, pc, opcode, rom):
        #11011101 0001DDDD
        op = rom.getByte(pc + 1)
        i = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "and A, " + self._nibbase % i)

    def _or_a_im(self, pc, opcode, rom):
        #11011101 0010DDDD
        op = rom.getByte(pc + 1)
        i = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "or A, " + self._nibbase % i)

    def _xor_a_im(self, pc, opcode, rom):
        #11011101 0011DDDD
        op = rom.getByte(pc + 1)
        i = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "xor A, " + self._nibbase % i)

    def _cpse_ahl_im(self, pc, opcode, rom):
        #11011101 0111DDDD
        op = rom.getByte(pc + 1)
        i = op & 0xF
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "cpse @HL, " + self._nibbase % i)

    def _ld_ra_a(self, pc, opcode, rom):
        #11011101 00000RRR
        op = rom.getByte(pc + 1)
        r = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "ld " + self._reg_tbl[r] + ", A")

    def _ld_a_r(self, pc, opcode, rom):
        #11011101 00001RRR
        op = rom.getByte(pc + 1)
        r = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "ld A, " + self._reg_tbl[r])

    def _cpse_r_im(self, pc, opcode, rom):
        #11011001 DDDD0RRR
        op = rom.getByte(pc + 1)
        r = op & 0x7
        i = (op >> 4) & 0xF
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "cpse " + self._reg_tbl[r] + ", " + self._nibbase % i)

    def _ld_ra_im(self, pc, opcode, rom):
        #11011001 DDDD1RRR
        op = rom.getByte(pc + 1)
        r = op & 0x7
        i = (op >> 4) & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "ld " + self._reg_tbl[r] + ", " + self._nibbase % i)

    def _ldb_ahda_bit_cy(self, pc, opcode, rom):
        #11111100 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "ldb RAM[@H + " + self._nibbase % d + "]." + str(b) + ", CY")

    def _ldb_memb_al_cy(self, pc, opcode, rom):
        #11111100 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "ldb RAM[" + self._rambase % pmem + " + @L3-2].@L1-0, CY")

    def _ldb_mema_bit_cy(self, pc, opcode, rom):
        #11111100 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        return (pc + 2,), (2, (opcode << 8) | op, "ldb RAM[" + self._rambase % fmem + "]." + str(b) + ", CY")

    def _bitr_ahda_bit(self, pc, opcode, rom):
        #11111110 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "bitr RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _bitr_memb_al(self, pc, opcode, rom):
        #11111110 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "bitr RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _bitr_mema_bit(self, pc, opcode, rom):
        #111111110 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (op in self._clr_fmem_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, self._clr_fmem_tbl[op])
        #elif (fmem in self._io_tbl):
        #    return (pc + 2,), (2, (opcode << 8) | op, "bitr " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "bitr RAM[" + self._rambase % fmem + "]." + str(b))

    def _bits_ahda_bit(self, pc, opcode, rom):
        #11111111 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "bits RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _bits_memb_al(self, pc, opcode, rom):
        #11111111 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "bits RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _bits_mema_bit(self, pc, opcode, rom):
        #11111111 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (op in self._set_fmem_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, self._set_fmem_tbl[op])
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "bits RAM[" + self._rambase % fmem + "]." + str(b))

    def _btstz_ahda_bit(self, pc, opcode, rom):
        #11111101 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btstz RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _btstz_memb_al(self, pc, opcode, rom):
        #11111101 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btstz RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _btstz_mema_bit(self, pc, opcode, rom):
        #11111101 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btstz RAM[" + self._rambase % fmem + "]." + str(b))

    def _ld_ahl_ea(self, pc, opcode, rom):
        #11011100 00000000
        return (pc + 2,), (2, (opcode << 8) | 0b00000000, "ld @HL, EA")

    def _xch_ea_ahl(self, pc, opcode, rom):
        #11011100 00000001
        return (pc + 2,), (2, (opcode << 8) | 0b00000001, "xch EA, @HL")

    def _ld_ea_ahl(self, pc, opcode, rom):
        #10101010 | 00001000
        return (pc + 2,), (2, (opcode << 8) | 0b00001000, "ld EA, @HL")

    def _cpse_ea_ahl(self, pc, opcode, rom):
        #10101010 | 00001001
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | 0b00001001, "cpse EA, @HL")

    def _xch_ea_rrb(self, pc, opcode, rom):
        #11011100 11100RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "xch EA, " + self._rpe_tbl[p])

    def _cpse_ea_rr(self, pc, opcode, rom):
        #11011100 11101RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "cpse EA, " + self._rpe_tbl[p])

    def _ld_rrb_ea(self, pc, opcode, rom):
        #11011100 11110RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "ld " + self._rpe_tbl[p] + ", EA")

    def _ld_ea_rrb(self, pc, opcode, rom):
        #11011100 11111RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "ld EA, " + self._rpe_tbl[p])

    def _decs_rr(self, pc, opcode, rom):
        #11011100 11011RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "decs " + self._rpe_tbl[p])

    def _and_rrb_ea(self, pc, opcode, rom):
        #11011100 00010RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "and " + self._rpe_tbl[p] + ", EA")

    def _and_ea_rr(self, pc, opcode, rom):
        #11011100 00011RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "and EA, " + self._rpe_tbl[p])

    def _or_rrb_ea(self, pc, opcode, rom):
        #11011100 00100RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "or " + self._rpe_tbl[p] + ", EA")

    def _or_ea_rr(self, pc, opcode, rom):
        #11011100 00101RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "or EA, " + self._rpe_tbl[p])

    def _xor_rrb_ea(self, pc, opcode, rom):
        #11011100 00110RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "xor " + self._rpe_tbl[p] + ", EA")

    def _xor_ea_rr(self, pc, opcode, rom):
        #11011100 00111RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "xor EA, " + self._rpe_tbl[p])

    def _ads_rrb_ea(self, pc, opcode, rom):
        #11011100 10010RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "adds " + self._rpe_tbl[p] + ", EA")

    def _ads_ea_rr(self, pc, opcode, rom):
        #11011100 10011RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "adds EA, " + self._rpe_tbl[p])

    def _adc_rrb_ea(self, pc, opcode, rom):
        #11011100 10100RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "adc " + self._rpe_tbl[p] + ", EA")

    def _adc_ea_rr(self, pc, opcode, rom):
        #11011100 10101RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "adc EA, " + self._rpe_tbl[p])

    def _sbs_rrb_ea(self, pc, opcode, rom):
        #11011100 10110RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "subs " + self._rpe_tbl[p] + ", EA")

    def _sbs_ea_rr(self, pc, opcode, rom):
        #11011100 10111RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "subs EA, " + self._rpe_tbl[p])

    def _sbc_rrb_ea(self, pc, opcode, rom):
        #11011100 11000RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "subc " + self._rpe_tbl[p] + ", EA")

    def _sbc_ea_rr(self, pc, opcode, rom):
        #11011100 11001RR0
        op = rom.getByte(pc + 1)
        p = op & 0x6
        return (pc + 2,), (2, (opcode << 8) | op, "subc EA, " + self._rpe_tbl[p])

    def _band_cy_ahda_bit(self, pc, opcode, rom):
        #11110101 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "band CY, RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _band_cy_memb_al(self, pc, opcode, rom):
        #11110101 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "band CY, RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _band_cy_mema_bit(self, pc, opcode, rom):
        #11110101 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        return (pc + 2,), (2, (opcode << 8) | op, "band CY, RAM[" + self._rambase % fmem + "]." + str(b))

    def _bor_cy_ahda_bit(self, pc, opcode, rom):
        #11110110 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "bor CY, RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _bor_cy_memb_al(self, pc, opcode, rom):
        #11110110 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "bor CY, RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _bor_cy_mema_bit(self, pc, opcode, rom):
        #11110110 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        return (pc + 2,), (2, (opcode << 8) | op, "or1 CY, RAM[" + self._rambase % fmem + "]." + str(b))

    def _bxor_cy_ahda_bit(self, pc, opcode, rom):
        #11110111 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "bxor CY, RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _bxor_cy_memb_al(self, pc, opcode, rom):
        #11110111 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "bxor CY, RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _bxor_cy_mema_bit(self, pc, opcode, rom):
        #11110111 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        return (pc + 2,), (2, (opcode << 8) | op, "bxor CY, RAM[" + self._rambase % fmem + "]." + str(b))

    def _ldb_cy_ahda_bit(self, pc, opcode, rom):
        #11110100 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "ldb CY, RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _ldb_cy_memb_al(self, pc, opcode, rom):
        #11110100 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "ldb CY, RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _ldb_cy_mema_bit(self, pc, opcode, rom):
        #11110100 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        return (pc + 2,), (2, (opcode << 8) | op, "ldb CY, RAM[" + self._rambase % fmem + "]." + str(b))

    def _btsf_ahda_bit(self, pc, opcode, rom):
        #11111000 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btsf RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _btsf_memb_al(self, pc, opcode, rom):
        #11111000 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btsf RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _btsf_mema_bit(self, pc, opcode, rom):
        #111111000 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btsf RAM[" + self._rambase % fmem + "]." + str(b))

    def _btst_ahda_bit(self, pc, opcode, rom):
        #11111001 00BBAAAA
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btst RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _btst_memb_al(self, pc, opcode, rom):
        #11111001 0100AAAA
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btst RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _btst_mema_bit(self, pc, opcode, rom):
        #11111001 1XBBAAAA
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        return (pc + 2, self._get_instr_skip_pc(pc + 2, rom)), (2, (opcode << 8) | op, "btst RAM[" + self._rambase % fmem + "]." + str(b))

    def _dummy(self, pc, opcode, rom):
        return (pc + 1,), (1, opcode, "db " + self._bytebase % opcode)

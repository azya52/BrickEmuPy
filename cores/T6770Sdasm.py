class T6770Sdasm():

    def __init__(self):
        self._addrbase = '%0.3X'
        self._opbase = '%0.3X'
        
        """
        A, B, H, L - 4-bit registers,
        M[] - 128 nibbles RAM
        CF - carry/borrow flag
        SF - status flag
        MC1, MC2 - machine cicles
        c - carry 
        b - borrow
        """

        self._instructions = (
            T6770Sdasm._nop,                          #00 0000 0000 CF -, SF 1; MC1; no operation
            T6770Sdasm._mov_a_m1l,                    #00 0000 0001 A = M[1L]; CF 0, SF 1; MC1
            T6770Sdasm._addc_a_mhl,                   #00 0000 0010 A += M[HL]; CF с, SF !с; MC1
            T6770Sdasm._inc_l,                        #00 0000 0011 L++; CF -, SC !c; MC1
            T6770Sdasm._scan_0,                       #00 0000 0100 SCAN = 0; CF -, SF 1; MC1; Writing to LCD shift register is enabled
            T6770Sdasm._mov_l_b,                      #00 0000 0101 L = B; CF -, SF 1; MC1
            T6770Sdasm._ret_a,                        #00 0000 0110 ?PC = M[0x0A]:M[0x0B]:M[0x0C], L = 0xC; CF -, SF 1; MC2
            T6770Sdasm._tst_t1,                       #00 0000 0111 CF -, SF !t1; MC1; test 1 sec event
            T6770Sdasm._tst_t8,                       #00 0000 1000 CF -, SF !t8; MC1; test 1/8 sec event
            T6770Sdasm._mov_m1l_a,                    #00 0000 1001 M[1L] = A; CF -, SF 1; MC1
            T6770Sdasm._rorc_mhl,                     #00 0000 1010 A = M[HL] = (CF << 3) | (M[HL] >> 1); CF c, SF !c; MC1; Rotate right through CF
            T6770Sdasm._nop,                          #00 0000 1011 ?CF -, SF 1; MC1; no operation
            T6770Sdasm._incp10,                       #00 0000 1100 ?inc10(M[HL+1]M[HL]), A = M[HL+1], L++; CF c, SF !c; MC2; Data memory pair (little-endian) increase modulo 10
            T6770Sdasm._in_a_ip,                      #00 0000 1101 A = IP; CF 0, SF 1; MC1; Read input port to A
            T6770Sdasm._rolc_mhl,                     #00 0000 1110 A = M[HL] = (M[HL] << 1) | CF; CF c, SF !c; MC1; Rotate left through CF
            T6770Sdasm._nop,                          #00 0000 1111 ?CF -, SF 1; MC1; no operation
            T6770Sdasm._mov_h_incb,                   #00 0001 0000 H = B = B + 1; CF -, SF !c; MC1
            T6770Sdasm._mov_a_b,                      #00 0001 0001 A = B; CF 0, SF 1; MC1
            T6770Sdasm._addc_a_b,                     #00 0001 0010 A = A + B + CF; CF c, SF !c; MC1 
            T6770Sdasm._inc_b,                        #00 0001 0011 B = B + 1; CF -, SF !c; MC1
            T6770Sdasm._nop,                          #00 0001 0100 ?CF -, SF 1; MC1; no operation
            T6770Sdasm._osc_ext,                      #00 0001 0101 ?clock from external oscillator (32k)
            T6770Sdasm._out_soundp_1,                 #00 0001 0110 SOUNDP = 1; CF -, SF 1; MC2; Set sound pin (0V)
            T6770Sdasm._delay_b,                      #00 0001 0111 ?B = 0xF; CF -, SF 0; MC1 + MC2 * B; Delay (B * MC2 + MC1)
            T6770Sdasm._wait_frame,                   #00 0001 1000 ?wait next frame
            T6770Sdasm._mov_b_a,                      #00 0001 1001 B = A; CF -, SF 1; MC1
            T6770Sdasm._clearm_mhl_dec,               #00 0001 1010 ?(L = L - 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 0; MC2 * (B + 1)
            T6770Sdasm._nop,                          #00 0001 1011 ?CF -, SF 1; MC1; no operation
            T6770Sdasm._nop2,                         #00 0001 1100 ?CF -, SF 1; MC2; no operation
            T6770Sdasm._in_a_iop,                     #00 0001 1101 A = IOP; CF 0, SF 1; MC1; Read input/output port to A
            T6770Sdasm._nop2,                         #00 0001 1110 ?CF -, SF 1; MC2; no operation
            T6770Sdasm._nop,                          #00 0001 1111 ?CF -, SF 1; MC1; no operation
            T6770Sdasm._mov_h_b_a,                    #00 0010 0000 H = B = A; CF -, SF 1; MC1
            T6770Sdasm._mov_a_mhl,                    #00 0010 0001 A = M[HL]; CF 0, SF 1; MC1
            T6770Sdasm._subc_a_mhl,                   #00 0010 0010 A = M[HL] - A - CF; CF b, SF !b; MC1
            T6770Sdasm._dec_l,                        #00 0010 0011 L = L - 1; CF -, SF !b; MC1
            T6770Sdasm._scan_1,                       #00 0010 0100 SCAN = 1; CF -, SF 1; MC1; Writing to LCD shift register is inhibited
            T6770Sdasm._mov_l_a,                      #00 0010 0101 L = A; CF -, SF 1; MC1
            T6770Sdasm._ret_d,                        #00 0010 0110 ?PC = M[0x0D]M[0x0E]M[0x0F], L = 0xF; CF -, SF 1; MC2
            T6770Sdasm._0027,                         #00 0010 0111 ?IOP direction; CF -, SF 1; MC1
            T6770Sdasm._tst_t64,                      #00 0010 1000 CF -, SF !t64; MC1; test 1/64 sec event
            T6770Sdasm._mov_mhl_a,                    #00 0010 1001 M[HL] = A; CF -, SF 1; MC1
            T6770Sdasm._br_cf_a,                      #00 0010 1010 ?PC = CF:A; CF -, SF 1; MC2
            T6770Sdasm._nop,                          #00 0010 1011 ?CF -, SF 1; MC1; no operation
            T6770Sdasm._decp10,                       #00 0010 1100 ?dec10(M[HL+1]M[HL]), A = M[HL+1], L++; CF b, SF !b; MC2; Data memory pair (little-endian) decrease modulo 10
            T6770Sdasm._inc_mhl,                      #00 0010 1101 ?A = M[HL] = M[HL] + 1; CF c, SF !c; MC1
            T6770Sdasm._nop2,                         #00 0010 1110 ?CF -, SF 1; MC2; no operation
            T6770Sdasm._nop,                          #00 0010 1111 ?CF -, SF 1; MC1; no operation
            T6770Sdasm._mov_h_dec_b,                  #00 0011 0000 H = B = B - 1; CF -, SF !c; MC1
            T6770Sdasm._mov_a_l,                      #00 0011 0001 A = L; CF 0, SF 1; MC1
            T6770Sdasm._subc_a_b,                     #00 0011 0010 A = B - A - CF; CF = b, SF = !b; MC1
            T6770Sdasm._dec_b,                        #00 0011 0011 B = B - 1; CF -, SF !b; MC1 
            T6770Sdasm._movp_mhl_a,                   #00 0011 0100 M[HL] = M[H:L+1] = A, L = L + 2; CF -, SF 1; MC1
            T6770Sdasm._osc_int,                      #00 0011 0101 ?clock from interlal oscillation (resistor)
            T6770Sdasm._out_soundp_0,                 #00 0011 0110 SOUNDP = 0; CF -, SF 1; MC2; Reset sound pin (+3V)
            T6770Sdasm._0037,                         #00 0011 0111 ?IOP direction; CF -, SF 1; MC1
            T6770Sdasm._wait_com,                     #00 0011 1000 ?wait next com
            T6770Sdasm._mov_b_l,                      #00 0011 1001 B = L; CF -, SF 1; MC1
            T6770Sdasm._clearm_mhl_inc,               #00 0011 1010 ?(L = L + 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 1; MC1 + MC1 * (B + 1)
            T6770Sdasm._nop,                          #00 0011 1011 ?CF -, SF 1; MC1; no operation
            T6770Sdasm._nop2,                         #00 0011 1100 ?CF -, SF 1; MC2; no operation
            T6770Sdasm._dec_mhl,                      #00 0011 1101 ?A = M[HL] = M[HL] - 1; CF b, SF !b; MC1
            T6770Sdasm._nop2,                         #00 0011 1110 ?CF -, SF 1; MC2; no operation
            T6770Sdasm._nop,                          #00 0011 1111 ?CF -, SF 1; MC1; no operation
            *([T6770Sdasm._mov_mh4linc_imm] * 16),    #00 0100 iiii ?M[HL] = IMM, H = B = 4, L = L + 1; CF -, SF !c; MC1
            *([T6770Sdasm._mov_mh4ldec_imm] * 16),    #00 0101 iiii ?M[HL] = IMM, H = B = 4, L = L - 1; CF -, SF !b; MC1
            *([T6770Sdasm._mov_mhlinc_imm] * 16),     #00 0110 iiii M[HL] = IMM, L = L + 1; CF -, SF !c; MC1
            *([T6770Sdasm._mov_mhl_imm] * 16),        #00 0111 iiii M[HL] = IMM, H = B = B + 1, A = 0; CF 0, SF !c; MC1
            *([T6770Sdasm._movm_mhlsubi_mhl] * 16),   #00 1000 iiii (M[H:L-IMM] = M[HL], L = L + 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); MC1 * count + MC1
            *([T6770Sdasm._movm_mhladdi_mhl] * 16),   #00 1001 iiii (M[H:L+IMM] = M[HL], L = L - 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); MC1 * count + MC1
            *([T6770Sdasm._inc_m1i] * 16),            #00 1010 iiii A = M[1:IMM] = M[1:IMM] + 1; CF c, SF !c; MC1
            *([T6770Sdasm._dec_m1i] * 16),            #00 1011 iiii A = M[1:IMM] = M[1:IMM] - 1; CF b, SF !b; MC1
            *([T6770Sdasm._addc10m_mhl_mbl] * 16),    #00 1100 iiii (A = M[HL] = (M[HL] + M[BL] + CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF c, SF 1; MC2 * count
            *([T6770Sdasm._subc10m_mhl_mbl] * 16),    #00 1101 iiii (A = M[HL] = (M[HL] - M[BL] - CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF b, SF 1; MC2 * count
            *([T6770Sdasm._out_outp_imm] * 16),       #00 1110 iiii A = OUTP = IMM; CF 0, SF 1; MC1
            *([T6770Sdasm._out_iop_imm] * 16),        #00 1111 iiii A = IOP = IMM; CF 0, SF 1; MC1
            *([T6770Sdasm._sbit_m] * 64),             #01 00bb hiii A = M[(HL if h)/0:IMM].b = 1; CF 0, SF 1; MC1
            *([T6770Sdasm._rbit_m] * 64),             #01 01bb hiii A = M[(HL if h)/0:IMM].b = 0; CF 0, SF 1; MC1
            *([T6770Sdasm._tbit_m] * 64),             #01 10bb hiii test M[(HL if h)/0:IMM].b; CF -, SF b==0; MC1
            *([T6770Sdasm._outm_lcd_mhl] * 16),       #01 1100 iiii ?(LCDP = M[HL], L = L - 1)WHILE((L + 1) >= IMM); CF -, SF 1, MC1 * count
            *([T6770Sdasm._mov_pch_imm] * 16),        #01 1101 iiii ?PC<11:8> = IMM; CF -, SF -?; MC1
            *([T6770Sdasm._cmp_mhl_imm] * 16),        #01 1110 iiii A = M[HL] - IMM; CF b, SF z; MC2
            *([T6770Sdasm._addc_a_imm] * 16),         #01 1111 iiii ?addc A, IMM; CF c, SF !c; MC1
            *([T6770Sdasm._mov_l_imm] * 16),          #10 0000 iiii L = IMM; CF -, SF 1; MC1
            *([T6770Sdasm._calla] * 16),              #10 0001 iiii ?M[0x0A]:M[0x0B]:M[0x0C] = PC, PC = hh:0b011111:IMM, L = 0xC; CF -, SF 1; MC2
            *([T6770Sdasm._mov_a_m0i] * 16),          #10 0010 iiii A = M[0:IMM]; CF 0, SF 1; MC1
            *([T6770Sdasm._calld] * 16),              #10 0011 iiii ?M[0x0D]:M[0x0E]:M[0x0F] = PC, PC = hh:0b111111:IMM, L = 0xF; CF -, SF 1; MC2
            *([T6770Sdasm._mov_b_imm] * 16),          #10 0100 iiii B = IMM; CF -, SF 1; MC1
            *([T6770Sdasm._calla] * 16),              #10 0101 iiii ?M[0x0A]:M[0x0B]:M[0x0C] = PC, PC = hh:0b011111:IMM, L = 0xC; CF -, SF 1; MC2
            *([T6770Sdasm._mov_m0i_a] * 16),          #10 0110 iiii M[0:IMM] = A; CF -, SF 1; MC1
            *([T6770Sdasm._calld] * 16),              #10 0111 iiii ?M[0x0D]:M[0x0E]:M[0x0F] = PC, PC = hh:0b111111:IMM, L = 0xF; CF -, SF 1; MC2
            *([T6770Sdasm._mov_h_imm] * 16),          #10 1000 iiii H = IMM; CF -, SF 1; MC1
            *([T6770Sdasm._calla] * 16),              #10 1001 iiii ?M[0x0A]:M[0x0B]:M[0x0C] = PC, PC = hh:0b011111:IMM, L = 0xC; CF -, SF 1; MC2
            *([T6770Sdasm._mov_a_m1i] * 16),          #10 1010 iiii A = M[1:IMM]; CF 0, SF 1; MC1
            *([T6770Sdasm._calld] * 16),              #10 1011 iiii ?M[0x0D]:M[0x0E]:M[0x0F] = PC, PC = hh:0b111111:IMM, L = 0xF; CF -, SF 1; MC2
            *([T6770Sdasm._mov_a_imm] * 16),          #10 1100 iiii A = IMM; CF 0, SF 1; MC1
            *([T6770Sdasm._calla] * 16),              #10 1101 iiii ?M[0x0A]:M[0x0B]:M[0x0C] = PC, PC = hh:0b011111:IMM, L = 0xC; CF -, SF 1; MC2
            *([T6770Sdasm._mov_m1i_a] * 16),          #10 1110 iiii M[1:IMM] = A; CF -, SF 1; MC1
            *([T6770Sdasm._calld] * 16),              #10 1111 iiii ?M[0x0D]:M[0x0E]:M[0x0F] = PC, PC = hh:0b111111:IMM, L = 0xF; CF -, SF 1; MC2
            *([T6770Sdasm._bs_imm] * 256)             #11 iiii iiii if SF (PC<7:0> = IMM); CF -, SF 1; MC1
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            return {"LISTING": tuple(self._disassemble(0, rom))}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        listing = self.disassemble(rom)["LISTING"]
        result = ""
        for i, line in enumerate(listing):
            if (type(line[1]) is tuple):
                result += (self._addrbase % i) + ":\t" + ((line[1][0] + "\t;" + line[0]).expandtabs(35) + "\t" + line[1][1]).expandtabs(10) + "\n"
            else:
                result += (self._addrbase % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(35) + "\n"
        with open(file_path, 'w') as f:
            f.write(result)
    
    def _disassemble(self, pc, rom):
        listing = []
        self._prev_opcode = 0
        while ((pc * 2) < rom.size()):
            opcode = rom.getWord(pc * 2)
            instr = self._instructions[opcode](self, pc, opcode)
            self._prev_opcode = opcode
            if (type(instr) is tuple):
                listing.append((self._opbase % opcode, instr[0]))
            else:
                listing.append((self._opbase % opcode, instr))
            pc += 1
        return listing

    def _nop(self, pc, opcode):
        #?CF -, SF 1; MC1; no operation
        return ("nop", "?CF -, SF 1; MC1; no operation")

    def _mov_a_m1l(self, pc, opcode):
        #00 0000 0001 A = M[1L]; CF 0, SF 1; MC1
        return ("mov A, M[1L]", "A = M[1L]; CF 0, SF 1")

    def _addc_a_mhl(self, pc, opcode):
        #00 0000 0010 A += M[HL]; CF c, SF !c; MC1
        return ("addc A, M[HL]", "A += M[HL]; CF c, SF !c")

    def _inc_l(self, pc, opcode):
        #00 0000 0011 L++; CF -, SC !c; MC1
        return ("inc L", "L++; CF -, SC !c")
    
    def _scan_0(self, pc, opcode):
        #00 0000 0100 SCAN = 0; CF -, SF 1; MC1; Writing to LCD shift register is enabled
        return ("scan 0", "SCAN = 0; CF -, SF 1; Writing to LCD shift register is enabled")

    def _mov_l_b(self, pc, opcode):
        #00 0000 0101 L = B; CF -, SF 1; MC1
        return ("mov L, B", "L = B; CF -, SF 1")

    def _ret_a(self, pc, opcode):
        #00 0000 0110 ?PC = M[0x0A]:M[0x0B]:M[0x0C], L = 0xC; CF -, SF 1; MC2
        return ("reta", "?PC = M[0x0A]:M[0x0B]:M[0x0C], L = 0xC; CF -, SF 1")

    def _tst_t1(self, pc, opcode):
        #00 0000 0111 CF -, SF !t1; MC1; test 1 sec event
        return ("tst T1", "CF -, SF !t1; test 1 sec event")

    def _tst_t8(self, pc, opcode):
        #00 0000 1000 CF -, SF !t8; MC1; test 1/8 sec event
        return ("tst T8", "CF -, SF !t1; test 1/8 sec event")

    def _mov_m1l_a(self, pc, opcode):
        #00 0000 1001 M[1L] = A; CF -, SF 1; MC1
        return ("mov M[1L], A", "M[1L] = A; CF -, SF 1")

    def _rorc_mhl(self, pc, opcode):
        #00 0000 1010 A = M[HL] = (CF << 3) | (M[HL] >> 1); CF c, SF !c; MC1; Rotate right through CF
        return ("rorc M[HL]", "A = M[HL] = (CF << 3) | (M[HL] >> 1); CF c, SF !c; Rotate right through CF")

    def _incp10(self, pc, opcode):
        #00 0000 1100 ?inc10(M[HL]M[HL+1]), A = M[HL+1], L++; CF c, SF !c; MC2; Increment data memory pair (little-endian) modulo 10.
        return ("incp10 M[HL]", "inc10(M[HL]M[HL+1]), A = M[HL+1], L++; CF c, SF !c")

    def _in_a_ip(self, pc, opcode):
        #00 0000 1101 A = IP; CF 0, SF 1; MC1; Read input port to A
        return ("in A, IP", "A = IP; CF 0, SF 1; Read input port to A")

    def _rolc_mhl(self, pc, opcode):
        #00 0000 1110 A = M[HL] = (M[HL] << 1) | CF; CF c, SF !c; MC1; Rotate left through CF
        return ("rolc M[HL]", "A = M[HL] = (M[HL] << 1) | CF; CF c, SF !c; Rotate left through CF")

    def _mov_h_incb(self, pc, opcode):
        #00 0001 0000 H = B = B + 1; CF -, SF !c; MC1
        return ("mov H, ++B", "H = B = B + 1; CF -, SF !c")

    def _mov_a_b(self, pc, opcode):
        #00 0001 0001 A = B; CF 0, SF 1; MC1
        return ("mov A, B", "A = B; CF 0, SF 1")

    def _addc_a_b(self, pc, opcode):
        #00 0001 0010 A = A + B + CF; CF c, SF !c; MC1 
        return ("addc A, B", "A = A + B + CF; CF c, SF !c")

    def _inc_b(self, pc, opcode):
        #00 0001 0011 B = B + 1; CF -, SF !c; MC1
        return ("inc B", "B = B + 1; CF -, SF !c")

    def _osc_ext(self, pc, opcode):
        #00 0001 0101 ?clock from external oscillator (32k); CF -, SF 1; MC1
        return ("osc ext", "?clock from external oscillator (32k); CF -, SF 1")

    def _out_soundp_1(self, pc, opcode):
        #00 0001 0110 SOUNDP = 1; CF -, SF 1; MC2; Set sound pin (0V)
        return ("out SOUNDP, 1", "SOUNDP = 1; CF -, SF 1; Set sound pin (0V)")

    def _delay_b(self, pc, opcode):
        #00 0001 0111 ?B = 0xF; CF -, SF 0; MC1 + MC2 * B; Delay (B * MC2 + MC1)
        return ("delay B", "?B = 0xF; CF -, SF 0; MC1 + MC2 * B; Delay (B * MC2 + MC1)")

    def _wait_frame(self, pc, opcode):
        #00 0001 1000 ?wait next frame
        return "wait frame"

    def _mov_b_a(self, pc, opcode):
        #00 0001 1001 B = A; CF -, SF 1; MC1
        return "mov B, A"

    def _clearm_mhl_dec(self, pc, opcode):
        #00 0001 1010 ?(L = L - 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 0; MC2 * (B + 1)
        return ("clearm M[H:--L] (--B >= 0)", "?(L = L - 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 0; MC2 * (B + 1)")

    def _nop2(self, pc, opcode):
        #?CF -, SF 1; MC2; no operation
        return ("nop2", "?CF -, SF 1; MC2; no operation")

    def _in_a_iop(self, pc, opcode):
        #00 0001 1101 A = IOP; CF 0, SF 1; MC1; Read input/output port to A
        return ("in A, IOP", "A = IOP; CF 0, SF 1; Read input/output port to A")

    def _mov_h_b_a(self, pc, opcode):
        #00 0010 0000 H = B = A; CF -, SF = 1; MC1
        return ("mov H, B, A", "H = B = A; CF -, SF 1")

    def _mov_a_mhl(self, pc, opcode):
        #00 0010 0001 A = M[HL]; CF 0, SF 1; MC1
        return ("mov A, M[HL]", "A = M[HL]; CF 0, SF 1; MC1")

    def _subc_a_mhl(self, pc, opcode):
        #00 0010 0010 A = M[HL] - A - CF; CF b, SF !b; MC1
        return ("subc A, M[HL]", "A = M[HL] - A - CF; CF b, SF !b")

    def _dec_l(self, pc, opcode):
        #00 0010 0011 L = L - 1; CF -, SF !b; MC1
        return ("dec L", "L = L - 1; CF -, SF !b")

    def _scan_1(self, pc, opcode):
        #00 0010 0100 SCAN = 1; CF -, SF 1; MC1; Writing to LCD shift register is inhibited
        return ("scan 1", "SCAN = 1; CF -, SF 1; MC1; Writing to LCD shift register is inhibited")

    def _mov_l_a(self, pc, opcode):
        #00 0010 0101 L = A; CF -, SF 1; MC1
        return ("mov L, A", "L = A; CF -, SF 1")

    def _ret_d(self, pc, opcode):
        #00 0010 0110 ?PC = M[0x0D]:M[0x0E]:M[0x0F], L = 0xF; CF -, SF 1; MC2
        return ("retd", "?PC = M[0x0D]:M[0x0E]:M[0x0F], L = 0xF; CF -, SF 1")

    def _0027(self, pc, opcode):
        #00 0010 0111 ?IOP direction; CF -, SF 1; MC1
        return "?IOP direction"

    def _tst_t64(self, pc, opcode):
        #00 0010 1000 CF -, SF !t1; MC1; test 1/64 sec event
        return ("tst T64", "CF -, SF !t1; MC1; test 1/64 sec event")

    def _mov_mhl_a(self, pc, opcode):
        #00 0010 1001 M[HL] = A; CF -, SF 1; MC1
        return ("mov M[HL], A", "M[HL] = A; CF -, SF 1")

    def _br_cf_a(self, pc, opcode):
        #00 0010 1010 ?PC = CF:A; CF -, SF 1; MC2
        return ("br CF:A", "PC = CF:A; CF -, SF 1")

    def _decp10(self, pc, opcode):
        #00 0010 1100 ?dec10(M[HL+1]M[HL]), A = M[HL+1], L++; CF b, SF !b; MC2; Decrement data memory pair (little-endian) modulo 10.
        return ("decp10 M[H:L++]", "?dec10(M[HL+1]M[HL]), A = M[HL+1], L++; CF b, SF !b; MC2")

    def _inc_mhl(self, pc, opcode):
        #00 0010 1101 ?A = M[HL] = M[HL] + 1; CF c, SF !c; MC1
        return ("inc M[HL]", "?A = M[HL] = M[HL] + 1; CF c, SF !c")

    def _mov_h_dec_b(self, pc, opcode):
        #00 0011 0000 H = B = B - 1; CF -, SF !c; MC1
        return ("mov H, --B", "H = B = B - 1; CF -, SF !c")

    def _mov_a_l(self, pc, opcode):
        #00 0011 0001 A = L; CF 0, SF 1; MC1
        return ("mov A, L", "A = L; CF 0, SF 1")

    def _subc_a_b(self, pc, opcode):
        #00 0011 0010 A = B - A - CF; CF = c, SF = !c; MC1
        return ("subc A, B", "A = B - A - CF; CF = b, SF = !b")

    def _dec_b(self, pc, opcode):
        #00 0011 0011 B = B - 1; CF -, SF !c; MC1 
        return ("dec B", "B = B - 1; CF -, SF !b")

    def _movp_mhl_a(self, pc, opcode):
        #00 0011 0100 M[HL] = M[H:L+1] = A, L = L + 2; CF -, SF 1; MC1
        return ("movp M[HL], A", "M[HL] = M[H:L+1] = A, L = L + 2; CF -, SF 1")

    def _osc_int(self, pc, opcode):
        #00 0011 0101 ?clock from interlal oscillation (resistor); CF -, SF 1; MC1
        return ("osc int", "?clock from interlal oscillation (resistor); CF -, SF 1")

    def _out_soundp_0(self, pc, opcode):
        #00 0011 0110 SOUNDP = 0; CF -, SF 1; MC2, Reset sound pin (+3V)
        return ("out SOUNDP, 0", "SOUNDP = 0; CF -, SF 1; Reset sound pin (+3V)")

    def _0037(self, pc, opcode):
        #00 0011 0111 ?IOP direction; CF -, SF 1; MC1
        return "?IOP direction"

    def _wait_com(self, pc, opcode):
        #00 0011 1000 ?wait next com
        return "wait com"

    def _mov_b_l(self, pc, opcode):
        #00 0011 1001 B = L; CF -, SF 1; MC1
        return ("mov B, L", "B = L; CF -, SF 1")

    def _clearm_mhl_inc(self, pc, opcode):
        #00 0011 1010 ?(L = L + 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 1; MC2 * (B + 1)
        return ("clearm M[H:++L] (--B >= 0)", "?(L = L + 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 1; MC1 + MC1 * (B + 1)")
        
    def _dec_mhl(self, pc, opcode):
        #00 0011 1101 ?A = M[HL] = M[HL] - 1; CF b, SF !b; MC1
        return ("dec M[HL]", "A = M[HL] = M[HL] - 1; CF b, SF !b")

    def _mov_mh4linc_imm(self, pc, opcode):
        #00 0100 iiii ?M[HL] = IMM, H = B = 4, L = L + 1; CF -, SF !c; MC1
        return ("mov M[H(4):L++], 0x%0.1X" % (opcode & 0xF), "?M[HL] = IMM, H = B = 4, L = L + 1; CF -, SF !c")

    def _mov_mh4ldec_imm(self, pc, opcode):
        #00 0101 iiii ?M[HL] = IMM, H = B = 4, L = L - 1; CF -, SF !b; MC1
        return ("mov M[H(4):L--], 0x%0.1X" % (opcode & 0xF), "?M[HL] = IMM, H = B = 4, L = L - 1; CF -, SF !b")

    def _mov_mhlinc_imm(self, pc, opcode):
        #00 0110 iiii M[HL] = IMM, L = L + 1; CF -, SF !c; MC1
        return ("mov M[H:L++], 0x%0.1X" % (opcode & 0xF), "M[HL] = IMM, L = L + 1; CF -, SF !c")

    def _mov_mhl_imm(self, pc, opcode):
        #00 0111 iiii M[HL] = IMM, H = B = B + 1, A = 0; CF 0, SF !c; MC1
        return ("mov M[H(B++):L], 0x%0.1X" % (opcode & 0xF), "M[HL] = IMM, H = B = B + 1, A = 0; CF 0, SF 1")

    def _movm_mhlsubi_mhl(self, pc, opcode):
        #00 1000 iiii (M[H:L-IMM] = M[HL], L = L + 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); MC1 * count + MC1
        return ("movm M[H:L-0x%0.1X], M[H:L++] (++B <= 15)" % (opcode & 0xF), "(M[H:L-IMM] = M[HL], L = L + 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0)")

    def _movm_mhladdi_mhl(self, pc, opcode):
        #00 1001 iiii (M[H:L+IMM] = M[HL], L = L - 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); MC1 * count + MC1
        return ("movm M[H:L+0x%0.1X], M[H:L--] (++B <= 15)" % (opcode & 0xF), "(M[H:L+IMM] = M[HL], L = L - 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0)")

    def _inc_m1i(self, pc, opcode):
        #00 1010 iiii A = M[1:IMM] = M[1:IMM] + 1; CF c, SF !c; MC1
        return ("inc M[0x1%0.1X]" % (opcode & 0xF), "A = M[1:IMM] = M[1:IMM] + 1; CF c, SF !c")

    def _dec_m1i(self, pc, opcode):
        #00 1011 iiii A = M[1:IMM] = M[1:IMM] - 1; CF b, SF !b; MC1
        return ("dec M[0x1%0.1X]" % (opcode & 0xF), "A = M[1:IMM] = M[1:IMM] - 1; CF b, SF !b")

    def _addc10m_mhl_mbl(self, pc, opcode):
        #00 1100 iiii (A = M[HL] = (M[HL] + M[BL] + CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF c, SF 0; MC2 * count
        return ("addc10m M[H:L++], M[BL] (L < 0x%0.1X)" % (16 - (opcode & 0xF)), "(A = M[HL] = (M[HL] + M[BL] + CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF c, SF 0")

    def _subc10m_mhl_mbl(self, pc, opcode):
        #00 1101 iiii (A = M[HL] = (M[HL] - M[BL] - CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF b, SF 0; MC2 * count
        return ("subc10m M[H:L++], M[BL] (L < 0x%0.1X)" % (16 - (opcode & 0xF)), "(A = M[HL] = (M[HL] - M[BL] - CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF b, SF 0")

    def _out_outp_imm(self, pc, opcode):
        #00 1110 iiii A = OUTP = IMM; CF 0, SF 1, MC1
        return ("out OUTP, 0x%0.1X" % (opcode & 0xF), "A = OUTP = IMM; CF 0, SF 1")

    def _out_iop_imm(self, pc, opcode):
        #00 1111 iiii A = IOP = IMM; CF 0, SF 1, MC1
        return ("out IOP, 0x%0.1X" % (opcode & 0xF), "A = IOP = IMM; CF 0, SF 1")

    def _sbit_m(self, pc, opcode):
        #01 00bb hiii A = M[(HL if h)/0:IMM].b = 1; CF 0, SF 1; MC1
        if (opcode & 0x8):
            return ("sbit M[HL].%0.1X" % ((opcode >> 4) & 0x3), "A = M[HL].b = 1; CF 0, SF 1")
        else:
            return ("sbit M[0x%0.2X].%0.1X" % ((opcode & 0x7), ((opcode >> 4) & 0x3)), "A = M[0:IMM].b = 1; CF 0, SF 1")

    def _rbit_m(self, pc, opcode):
        #01 01bb hiii A = M[(HL if h)/0:IMM].b = 0; CF 0, SF 1; MC1
        if (opcode & 0x8):
            return ("rbit A M[HL].%0.1X" % ((opcode >> 4) & 0x3), "A = M[HL].b = 0; CF 0, SF 1")
        else:
            return ("rbit A M[0x%0.2X].%0.1X" % ((opcode & 0x7), ((opcode >> 4) & 0x3)), "A = M[0:IMM].b = 0; CF 0, SF 1")
            
    def _tbit_m(self, pc, opcode):
        #01 10bb hiii test M[(HL if h)/0:IMM].b; CF -, SF b==0; MC1
        if (opcode & 0x8):
            return ("tbit M[HL].%0.1X" % ((opcode >> 4) & 0x3), "test M[HL].b; CF -, SF b==0")
        else:
            return ("tbit M[0x%0.2X].%0.1X" % ((opcode & 0x7), ((opcode >> 4) & 0x3)), "test M[0:IMM].b; CF -, SF b==0")
            
    def _outm_lcd_mhl(self, pc, opcode):
        #01 1100 iiii ?(LCDP = M[HL], L = L - 1)WHILE((L + 1) >= IMM); CF -, SF 1, MC1 * count
        return ("outm LCDP, M[H:L--] (L>=0x%0.1X)" % ((opcode - 1) & 0xF), "?(LCDP = M[HL], L = L - 1)WHILE((L + 1) >= IMM); CF -, SF 1")

    def _mov_pch_imm(self, pc, opcode):
        #01 1101 iiii ?PC<11:8> = IMM; CF -, SF -?; MC1
        return ("mov PC<11:8>, 0x%0.1X" % (opcode & 0xF), "?PC<11:8> = IMM; CF -, SF -?")

    def _cmp_mhl_imm(self, pc, opcode):
        #01 1110 iiii A = M[HL] - IMM; CF b, SF z; MC2
        return ("cmp M[HL], 0x%0.1X" % (opcode & 0xF), "A = M[HL] - IMM; CF b, SF z")

    def _addc_a_imm(self, pc, opcode):
        #01 1111 iiii ?addc A, IMM; CF c, SF !c; MC1
        return ("addc A, 0x%0.1X" % (opcode & 0xF), "?addc A, IMM; CF c, SF !c")

    def _mov_l_imm(self, pc, opcode):
        #10 0000 iiii L = IMM; CF -, SF 1; MC1
        return ("mov L, 0x%0.1X" % (opcode & 0xF), "L = IMM; CF -, SF 1")

    def _calla(self, pc, opcode):
        #10 hh01 iiii ?M[0x0A]:M[0x0B]:M[0x0C] = PC, PC = hh:0b011111:IMM, L = 0xC; CF -, SF 1; MC2
        return ("calla %0.3X" % (((opcode & 0xF0) << 4) | 0xF0 | (opcode & 0xF)), "?M[0x0A]:M[0x0B]:M[0x0C] = PC, PC = hh:0b011111:IMM, L = 0xC; CF -, SF 1")

    def _mov_a_m0i(self, pc, opcode):
        #10 0010 iiii A = M[0:IMM]; CF 0, SF 1; MC1
        return ("mov A, M[0x0%0.1X]" % (opcode & 0xF), "A = M[0:IMM]; CF 0, SF 1")

    def _calld(self, pc, opcode):
        #10 hh11 iiii ?M[0x0D]:M[0x0E]:M[0x0F] = PC, PC = hh:0b111111:IMM, L = 0xF; CF -, SF 1; MC2
        return ("calld %0.3X" % (((opcode & 0xF0) << 4) | 0xF0 | (opcode & 0xF)), "?M[0x0D]:M[0x0E]:M[0x0F] = PC, PC = hh:0b111111:IMM, L = 0xF; CF -, SF 1")

    def _mov_b_imm(self, pc, opcode):
        #10 0100 iiii B = IMM; CF -, SF 1; MC1
        return ("mov B, 0x%0.1X" % (opcode & 0xF), "B = IMM; CF -, SF 1")

    def _mov_m0i_a(self, pc, opcode):
        #10 0110 iiii M[0:IMM] = A; CF -, SF 1; MC1
        return ("mov M[0x0%0.1X], A" % (opcode & 0xF), "M[0:IMM] = A; CF -, SF 1")

    def _mov_h_imm(self, pc, opcode):
        #10 1000 iiii H = IMM; CF -, SF 1; MC1
        return ("mov H, 0x%0.1X" % (opcode & 0xF), "H = IMM; CF -, SF 1")

    def _mov_a_m1i(self, pc, opcode):
        #10 1010 iiii A = M[1:IMM]; CF 0, SF 1; MC1
        return ("mov A, M[0x1%0.1X]" % (opcode & 0xF), "A = M[1:IMM]; CF 0, SF 1")

    def _mov_a_imm(self, pc, opcode):
        #10 1100 iiii A = IMM; CF 0, SF 1; MC1
        return ("mov A, 0x%0.1X" % (opcode & 0xF), "A = IMM; CF 0, SF 1")

    def _mov_m1i_a(self, pc, opcode):
        #10 1110 iiii M[1:IMM] = A; CF -, SF 1; MC1
        return ("mov M[0x1%0.1X], A" % (opcode & 0xF), "M[1:IMM] = A; CF -, SF 1")

    def _bs_imm(self, pc, opcode):
        #11 iiii iiii if SF (PC<7:0> = IMM); CF -, SF 1; MC1
        if ((self._prev_opcode & 0x3F0) == 0b0111010000):
            return ("bs %0.3X" % (((self._prev_opcode & 0xF) << 8) | (opcode & 0x0FF)), "if SF (PC<7:0> = IMM); CF -, SF 1")
        return ("bs %0.3X" % ((pc & 0xF00) | (opcode & 0x0FF)), "if SF (PC<7:0> = IMM); CF -, SF 1")
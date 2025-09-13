class T7741dasm():

    def __init__(self):
        self._addrbase = '%0.3X'
        self._opbase = '%0.3X'
        
        """
        A, B - 4-bit registers
        H - RAM Address Register, upper 3 bit
        L - RAM Address Register, lower 4 bit
        M[] - 128 nibbles RAM
        CF - carry/borrow flag
        SF - status flag
        CCx - clock cicles
        STACKx - return address (I didn't figure out how exactly it is stored)
        n - number of steps for multi-instructions
        c - carry 
        b - borrow
        """

        self._instructions = (
            T7741dasm._nop,                          #00 0000 0000 CF -, SF 1; CC16; no operation
            T7741dasm._mov_l_b,                      #00 0000 0001 L = B; CF -, SF 1; CC16
            T7741dasm._addc_a_mhl,                   #00 0000 0010 A += M[HL]; CF с, SF !с; CC16
            T7741dasm._inc_l,                        #00 0000 0011 L++; CF -, SC !c; CC16
            T7741dasm._scan_0,                       #00 0000 0100 SCAN = 0; CF -, SF 1; CC16; Writing to LCD shift register is enabled
            T7741dasm._nop,                          #00 0000 0101 CF -, SF 1; CC16; no operation
            T7741dasm._ret0,                         #00 0000 0110 ?PC = STACK0, L = 0xC; CF -, SF 1; CC32
            T7741dasm._tst_px,                       #00 0000 0111 CF -, SF !PXF; CC16; Test Prescaler Event Flag X (prescaler bit hardwired via mask option)
            T7741dasm._tst_py,                       #00 0000 1000 CF -, SF !PYF; CC16; Test Prescaler Event Flag Y (prescaler bit hardwired via mask option)
            T7741dasm._mov_m1l_a,                    #00 0000 1001 M[1L] = A; CF -, SF 1; CC16
            T7741dasm._rorc_mhl,                     #00 0000 1010 A = M[HL] = (CF << 3) | (M[HL] >> 1); CF c, SF !c; CC16; Rotate right through CF
            T7741dasm._mov_a_m1l,                    #00 0000 1011 A = M[1L]; CF -, SF 1; CC16
            T7741dasm._incp10,                       #00 0000 1100 inc10(M[HL+1]M[HL]), A = M[HL+1], L++; CF c, SF !c; CC32; Data memory pair (little-endian) increase modulo 10
            T7741dasm._in_a_ip,                      #00 0000 1101 A = IP; CF 0, SF 1; CC16; Read input port to A
            T7741dasm._rolc_mhl,                     #00 0000 1110 A = M[HL] = (M[HL] << 1) | CF; CF c, SF !c; CC16; Rotate left through CF
            T7741dasm._mov_a_mhl,                    #00 0000 1111 A = M[HL]; CF -, SF 1; CC16
            T7741dasm._mov_h_incb,                   #00 0001 0000 H = B = B + 1; CF -, SF !c; CC16
            T7741dasm._mov_a_b,                      #00 0001 0001 A = B; CF 0, SF 1; CC16
            T7741dasm._addc_a_b,                     #00 0001 0010 A = A + B + CF; CF c, SF !c; CC16 
            T7741dasm._inc_b,                        #00 0001 0011 B = B + 1; CF -, SF !c; CC16
            T7741dasm._nop,                          #00 0001 0100 CF -, SF 1; CC16; no operation
            T7741dasm._osc_ext,                      #00 0001 0101 ?clock from external oscillator (32k)
            T7741dasm._nop2,                         #00 0001 0110 CF -, SF 1; CC32; no operation
            T7741dasm._nop,                          #00 0001 0111 CF -, SF 1; CC16; no operation
            T7741dasm._wait_frame,                   #00 0001 1000 ?wait next frame
            T7741dasm._mov_b_a,                      #00 0001 1001 B = A; CF -, SF 1; CC16
            T7741dasm._clearm_mhl_dec,               #00 0001 1010 (L = L - 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 0; CC16 * (n - 1) + CC32
            T7741dasm._out_bz_1,                     #00 0001 1011 BZ = 1; CF -, SF 1; CC16; Set buzzer pin (0V)
            T7741dasm._nop2,                         #00 0001 1100 CF -, SF 1; CC32; no operation
            T7741dasm._in_a_iop,                     #00 0001 1101 A = IOP; CF 0, SF 1; CC16; Read input/output port to A
            T7741dasm._nop2,                         #00 0001 1110 CF -, SF 1; CC32; no operation
            T7741dasm._nop,                          #00 0001 1111 CF -, SF 1; CC16; no operation
            T7741dasm._mov_h_a,                      #00 0010 0000 H = A; CF -, SF 1; CC16
            T7741dasm._mov_l_a,                      #00 0010 0001 L = A; CF -, SF 1; CC16
            T7741dasm._subc_a_mhl,                   #00 0010 0010 A = M[HL] - A - CF; CF b, SF !b; CC16
            T7741dasm._dec_l,                        #00 0010 0011 L = L - 1; CF -, SF !b; CC16
            T7741dasm._scan_1,                       #00 0010 0100 SCAN = 1; CF -, SF 1; CC16; Writing to LCD shift register is inhibited
            T7741dasm._nop,                          #00 0010 0101 CF -, SF 1; CC16; no operation
            T7741dasm._ret1,                         #00 0010 0110 ?PC = STACK1, L = 0xF; CF -, SF 1; CC32
            T7741dasm._0027,                         #00 0010 0111 ?IOP direction; CF -, SF 1; CC16
            T7741dasm._tst_pz,                       #00 0010 1000 CF -, SF !PZF; CC16; Test Prescaler Event Flag Z (prescaler bit hardwired via mask option)
            T7741dasm._mov_mhl_a,                    #00 0010 1001 M[HL] = A; CF -, SF 1; CC16
            T7741dasm._exe_cf_a,                     #00 0010 1010 ?exe(PC + 1), exe(CF:A); CF -, SF 1; CC32; Execute the following instruction and then CF:A
            T7741dasm._nop,                          #00 0010 1011 CF -, SF 1; CC16; no operation
            T7741dasm._decp10,                       #00 0010 1100 dec10(M[HL+1]M[HL]), A = M[HL+1], L++; CF b, SF !b; CC32; Data memory pair (little-endian) decrease modulo 10
            T7741dasm._inc_mhl,                      #00 0010 1101 A = M[HL] = M[HL] + 1; CF c, SF !c; CC16
            T7741dasm._nop2,                         #00 0010 1110 CF -, SF 1; CC32; no operation
            T7741dasm._nop,                          #00 0010 1111 CF -, SF 1; CC16; no operation
            T7741dasm._mov_h_dec_b,                  #00 0011 0000 H = B = B - 1; CF -, SF !c; CC16
            T7741dasm._mov_a_l,                      #00 0011 0001 A = L; CF 0, SF 1; CC16
            T7741dasm._subc_a_b,                     #00 0011 0010 A = B - A - CF; CF = b, SF = !b; CC16
            T7741dasm._dec_b,                        #00 0011 0011 B = B - 1; CF -, SF !b; CC16 
            T7741dasm._nop,                          #00 0011 0100 CF -, SF 1; CC16; no operation
            T7741dasm._osc_int,                      #00 0011 0101 ?clock from interlal oscillation (resistor)
            T7741dasm._nop2,                         #00 0011 0110 CF -, SF 1; CC32; no operation
            T7741dasm._0037,                         #00 0011 0111 ?IOP direction; CF -, SF 1; CC16
            T7741dasm._wait_com,                     #00 0011 1000 ?wait next com
            T7741dasm._mov_b_l,                      #00 0011 1001 B = L; CF -, SF 1; CC16
            T7741dasm._clearm_mhl_inc,               #00 0011 1010 (L = L + 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 1; CC16 * (n - 1) + CC32
            T7741dasm._out_bz_0,                     #00 0011 1011 BZ = 0; CF -, SF 1; CC16; Reset buzzer pin (+3V)
            T7741dasm._nop2,                         #00 0011 1100 CF -, SF 1; CC32; no operation
            T7741dasm._dec_mhl,                      #00 0011 1101 A = M[HL] = M[HL] - 1; CF b, SF !b; CC16
            T7741dasm._nop2,                         #00 0011 1110 CF -, SF 1; CC32; no operation
            T7741dasm._nop,                          #00 0011 1111 CF -, SF 1; CC16; no operation
            *([T7741dasm._addc_a_imm] * 16),         #00 0100 iiii A = A + IMM + CF; CF c, SF !c; CC16 
            *([T7741dasm._subc_a_imm] * 16),         #00 0101 iiii A = IMM - A - CF; CF = b, SF = !b; CC16
            *([T7741dasm._mov_mhlinc_imm] * 16),     #00 0110 iiii M[HL] = IMM, L = L + 1; CF -, SF !c; CC16
            *([T7741dasm._mov_mhl_imm] * 16),        #00 0111 iiii M[HL] = IMM, H = B = B + 1; CF -, SF !c; CC16
            *([T7741dasm._movm_mhlsubi_mhl] * 16),   #00 1000 iiii (M[H:L-IMM] = M[HL], L = L + 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); CC24 * (n - 1) + CC32
            *([T7741dasm._movm_mhladdi_mhl] * 16),   #00 1001 iiii (M[H:L+IMM] = M[HL], L = L - 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); CC24 * (n - 1) + CC32
            *([T7741dasm._inc_m1i] * 16),            #00 1010 iiii A = M[1:IMM] = M[1:IMM] + 1; CF c, SF !c; CC16
            *([T7741dasm._dec_m1i] * 16),            #00 1011 iiii A = M[1:IMM] = M[1:IMM] - 1; CF b, SF !b; CC16
            *([T7741dasm._addc10m_mhl_mbl] * 16),    #00 1100 iiii (A = M[HL] = (M[HL] + M[BL] + CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF c, SF 1; CC20 * (n - 1) + CC32
            *([T7741dasm._subc10m_mhl_mbl] * 16),    #00 1101 iiii (A = M[HL] = (M[HL] - M[BL] - CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF b, SF 1; CC20 * (n - 1) + CC32
            *([T7741dasm._out_outp_imm] * 16),       #00 1110 iiii A = OUTP = IMM; CF 0, SF 1; CC16
            *([T7741dasm._out_iop_imm] * 16),        #00 1111 iiii A = IOP = IMM; CF 0, SF 1; CC16
            *([T7741dasm._sbit_m] * 64),             #01 00bb hiii if (h) (if (b == 1) A = M[HL] = M[HL] | B else A = M[HL]) else (A = M[0:IMM].b = 1); CF 0, SF 1; CC16
            *([T7741dasm._rbit_m] * 64),             #01 01bb hiii if (h) (if (b == 1) A = M[HL] = M[HL] & ~B else A = M[HL]) else (A = M[0:IMM].b = 0); CF 0, SF 1; CC16
            *([T7741dasm._tbit_m] * 64),             #01 10bb hiii if (h and b == 1) (M[HL] > (M[HL] | B)) else (M[(HL if h)/0:IMM].b == 0); CF -, SF res; CC16
            *([T7741dasm._outm_lcd_mhl] * 16),       #01 1100 iiii (LCDP = M[HL], L = L - 1)WHILE((L + 1) >= IMM), H = A = A + 1, L = 0xF; CF A==0, SF !(A==0), CC16 * (n - 1) + CC32
            *([T7741dasm._mov_pch_imm] * 16),        #01 1101 iiii PC<11:8> = IMM; CF -, SF -?; CC16
            *([T7741dasm._cmp_mhl_imm] * 16),        #01 1110 iiii A = M[HL] - IMM; CF b, SF z; CC32
            *([T7741dasm._delay_nl_imm] * 16),       #01 1111 iiii L = IMM; CF -, SF 0; CC4 * (15 - L) + CC16
            *([T7741dasm._mov_l_imm] * 16),          #10 0000 iiii L = IMM; CF -, SF 1; CC16
            *([T7741dasm._call0] * 16),              #10 0001 iiii ?STACK0 = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
            *([T7741dasm._mov_a_m0i] * 16),          #10 0010 iiii A = M[0:IMM]; CF 0, SF 1; CC16
            *([T7741dasm._call1] * 16),              #10 0011 iiii ?STACK1 = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
            *([T7741dasm._mov_b_imm] * 16),          #10 0100 iiii B = IMM; CF -, SF 1; CC16
            *([T7741dasm._call0] * 16),              #10 0101 iiii ?STACK0 = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
            *([T7741dasm._mov_m0i_a] * 16),          #10 0110 iiii M[0:IMM] = A; CF -, SF 1; CC16
            *([T7741dasm._call1] * 16),              #10 0111 iiii ?STACK1 = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
            *([T7741dasm._mov_h_imm] * 16),          #10 1000 iiii H = IMM; CF -, SF 1; CC16
            *([T7741dasm._call0] * 16),              #10 1001 iiii ?STACK0 = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
            *([T7741dasm._mov_a_m1i] * 16),          #10 1010 iiii A = M[1:IMM]; CF 0, SF 1; CC16
            *([T7741dasm._call1] * 16),              #10 1011 iiii ?STACK1 = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
            *([T7741dasm._mov_a_imm] * 16),          #10 1100 iiii A = IMM; CF 0, SF 1; CC16
            *([T7741dasm._call0] * 16),              #10 1101 iiii ?STACK0 = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
            *([T7741dasm._mov_m1i_a] * 16),          #10 1110 iiii M[1:IMM] = A; CF -, SF 1; CC16
            *([T7741dasm._call1] * 16),              #10 1111 iiii ?STACK1 = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
            *([T7741dasm._bs_imm] * 256)             #11 iiii iiii if SF (PC<7:0> = IMM); CF -, SF 1; CC16
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            return {"LISTING": tuple(self._disassemble(0, rom, False))}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        if (rom.size() > 0):
            listing = tuple(self._disassemble(0, rom, True))
            result = ""
            for i, line in enumerate(listing):
                if (type(line[1]) is tuple):
                    result += (self._addrbase % i) + ":\t" + ((line[1][0] + "\t;" + line[0]).expandtabs(38) + "\t" + line[1][1]).expandtabs(10) + "\n"
                else:
                    result += (self._addrbase % i) + ":\t" + line[1] + "\n"
            with open(file_path, 'w') as f:
                f.write(result)
    
    def _disassemble(self, pc, rom, comments):
        listing = []
        self._prev_opcode = 0
        while ((pc * 2) < rom.size()):
            opcode = rom.getWord(pc * 2)
            instr = self._instructions[opcode](self, pc, opcode)
            self._prev_opcode = opcode
            if ((type(instr) is tuple) and (not comments)):
                listing.append((self._opbase % opcode, instr[0]))
            else:
                listing.append((self._opbase % opcode, instr))
            pc += 1
        return listing

    def _nop(self, pc, opcode):
        #CF -, SF 1; CC16; no operation
        return ("nop", "CF -, SF 1; CC16; no operation")

    def _mov_a_m1l(self, pc, opcode):
        #00 0000 0001 A = M[1L]; CF 0, SF 1; CC16
        return ("mov A, M[1L]", "A = M[1L]; CF 0, SF 1")

    def _addc_a_mhl(self, pc, opcode):
        #00 0000 0010 A += M[HL]; CF c, SF !c; CC16
        return ("addc A, M[HL]", "A += M[HL]; CF c, SF !c")

    def _inc_l(self, pc, opcode):
        #00 0000 0011 L++; CF -, SC !c; CC16
        return ("inc L", "L++; CF -, SC !c")
    
    def _scan_0(self, pc, opcode):
        #00 0000 0100 SCAN = 0; CF -, SF 1; CC16; Writing to LCD shift register is enabled
        return ("scan 0", "SCAN = 0; CF -, SF 1; Writing to LCD shift register is enabled")

    def _mov_l_b(self, pc, opcode):
        #00 0000 0001 L = B; CF -, SF 1; CC16
        return ("mov L, B", "L = B; CF -, SF 1")

    def _ret0(self, pc, opcode):
        #00 0000 0110 ?PC = STACK0, L = 0xC; CF -, SF 1; CC32
        return ("ret0", "?PC = STACK0, L = 0xC; CF -, SF 1")

    def _tst_px(self, pc, opcode):
        #00 0000 0111 CF -, SF !PXF; CC16; Test Prescaler Event Flag X (prescaler bit hardwired via mask option)
        return ("tst PX", "CF -, SF !PXF; CC16; Test Prescaler Event Flag X")

    def _tst_py(self, pc, opcode):
        #00 0000 1000 CF -, SF !PYF; CC16; Test Prescaler Event Flag Y (prescaler bit hardwired via mask option)
        return ("tst PY", "CF -, SF !PXF; CC16; Test Prescaler Event Flag Y")

    def _mov_m1l_a(self, pc, opcode):
        #00 0000 1001 M[1L] = A; CF -, SF 1; CC16
        return ("mov M[1L], A", "M[1L] = A; CF -, SF 1")

    def _rorc_mhl(self, pc, opcode):
        #00 0000 1010 A = M[HL] = (CF << 3) | (M[HL] >> 1); CF c, SF !c; CC16; Rotate right through CF
        return ("rorc M[HL]", "A = M[HL] = (CF << 3) | (M[HL] >> 1); CF c, SF !c; Rotate right through CF")

    def _incp10(self, pc, opcode):
        #00 0000 1100 inc10(M[HL]M[HL+1]), A = M[HL+1], L++; CF c, SF !c; CC32; Increment data memory pair (little-endian) modulo 10.
        return ("incp10 M[HL]", "inc10(M[HL]M[HL+1]), A = M[HL+1], L++; CF c, SF !c")

    def _in_a_ip(self, pc, opcode):
        #00 0000 1101 A = IP; CF 0, SF 1; CC16; Read input port to A
        return ("in A, IP", "A = IP; CF 0, SF 1; Read input port to A")

    def _rolc_mhl(self, pc, opcode):
        #00 0000 1110 A = M[HL] = (M[HL] << 1) | CF; CF c, SF !c; CC16; Rotate left through CF
        return ("rolc M[HL]", "A = M[HL] = (M[HL] << 1) | CF; CF c, SF !c; Rotate left through CF")

    def _mov_h_incb(self, pc, opcode):
        #00 0001 0000 H = B = B + 1; CF -, SF !c; CC16
        return ("mov H, ++B", "H = B = B + 1; CF -, SF !c")

    def _mov_a_b(self, pc, opcode):
        #00 0001 0001 A = B; CF 0, SF 1; CC16
        return ("mov A, B", "A = B; CF 0, SF 1")

    def _addc_a_b(self, pc, opcode):
        #00 0001 0010 A = A + B + CF; CF c, SF !c; CC16 
        return ("addc A, B", "A = A + B + CF; CF c, SF !c")

    def _inc_b(self, pc, opcode):
        #00 0001 0011 B = B + 1; CF -, SF !c; CC16
        return ("inc B", "B = B + 1; CF -, SF !c")

    def _osc_ext(self, pc, opcode):
        #00 0001 0101 ?clock from external oscillator (32k); CF -, SF 1; CC16
        return ("osc ext", "?clock from external oscillator (32k); CF -, SF 1")

    def _out_bz_1(self, pc, opcode):
        #00 0001 1011 BZ = 1; CF -, SF 1; CC16; Set buzzer pin (0V)
        return ("out BZ, 1", "BZ = 1; CF -, SF 1; Set buzzer pin (0V)")

    def _wait_frame(self, pc, opcode):
        #00 0001 1000 ?wait next frame
        return ("wait frame", "?wait next frame")

    def _mov_b_a(self, pc, opcode):
        #00 0001 1001 B = A; CF -, SF 1; CC16
        return ("mov B, A", "B = A; CF -, SF 1")

    def _clearm_mhl_dec(self, pc, opcode):
        #00 0001 1010 (L = L - 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 0; CC16 * (n - 1) + CC32
        return ("clearm M[H:--L] (B-- > 0)", "(L = L - 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 0")

    def _nop2(self, pc, opcode):
        #CF -, SF 1; CC32; no operation
        return ("nop2", "CF -, SF 1; CC32; no operation")

    def _in_a_iop(self, pc, opcode):
        #00 0001 1101 A = IOP; CF 0, SF 1; CC16; Read input/output port to A
        return ("in A, IOP", "A = IOP; CF 0, SF 1; Read input/output port to A")

    def _mov_h_a(self, pc, opcode):
        #00 0010 0000 H = A; CF -, SF 1; CC16
        return ("mov H, A", "H = A; CF -, SF 1")

    def _mov_a_mhl(self, pc, opcode):
        #00 0000 1111 A = M[HL]; CF 0, SF 1; CC16
        return ("mov A, M[HL]", "A = M[HL]; CF 0, SF 1; CC16")

    def _subc_a_mhl(self, pc, opcode):
        #00 0010 0010 A = M[HL] - A - CF; CF b, SF !b; CC16
        return ("subc A, M[HL]", "A = M[HL] - A - CF; CF b, SF !b")

    def _dec_l(self, pc, opcode):
        #00 0010 0011 L = L - 1; CF -, SF !b; CC16
        return ("dec L", "L = L - 1; CF -, SF !b")

    def _scan_1(self, pc, opcode):
        #00 0010 0100 SCAN = 1; CF -, SF 1; CC16; Writing to LCD shift register is inhibited
        return ("scan 1", "SCAN = 1; CF -, SF 1; CC16; Writing to LCD shift register is inhibited")

    def _mov_l_a(self, pc, opcode):
        #00 0010 0001 L = A; CF -, SF 1; CC16
        return ("mov L, A", "L = A; CF -, SF 1")

    def _ret1(self, pc, opcode):
        #00 0010 0110 ?PC = STACK1, L = 0xF; CF -, SF 1; CC32
        return ("ret1", "?PC = STACK1, L = 0xF; CF -, SF 1")

    def _0027(self, pc, opcode):
        #00 0010 0111 ?IOP direction; CF -, SF 1; CC16
        return "?IOP direction"

    def _tst_pz(self, pc, opcode):
        #00 0010 1000 CF -, SF !PZF; CC16; Test Prescaler Event Flag Z (prescaler bit hardwired via mask option)
        return ("tst PZ", "CF -, SF !PZF; CC16; Test Prescaler Event Flag Z")

    def _mov_mhl_a(self, pc, opcode):
        #00 0010 1001 M[HL] = A; CF -, SF 1; CC16
        return ("mov M[HL], A", "M[HL] = A; CF -, SF 1")

    def _exe_cf_a(self, pc, opcode):
        #00 0010 1010 ?exe(PC + 1), exe(CF:A); CF -, SF 1; CC32; Execute the following instruction and then CF:A
        return ("exe CF:A", "?exe(PC + 1), exe(CF:A); CF -, SF 1; Execute the following instruction and then CF:A")

    def _decp10(self, pc, opcode):
        #00 0010 1100 dec10(M[HL+1]M[HL]), A = M[HL+1], L++; CF b, SF !b; CC32; Decrement data memory pair (little-endian) modulo 10.
        return ("decp10 M[H:L++]", "dec10(M[HL+1]M[HL]), A = M[HL+1], L++; CF b, SF !b; CC32")

    def _inc_mhl(self, pc, opcode):
        #00 0010 1101 A = M[HL] = M[HL] + 1; CF c, SF !c; CC16
        return ("inc M[HL]", "A = M[HL] = M[HL] + 1; CF c, SF !c")

    def _mov_h_dec_b(self, pc, opcode):
        #00 0011 0000 H = B = B - 1; CF -, SF !c; CC16
        return ("mov H, --B", "H = B = B - 1; CF -, SF !c")

    def _mov_a_l(self, pc, opcode):
        #00 0011 0001 A = L; CF 0, SF 1; CC16
        return ("mov A, L", "A = L; CF 0, SF 1")

    def _subc_a_b(self, pc, opcode):
        #00 0011 0010 A = B - A - CF; CF = c, SF = !c; CC16
        return ("subc A, B", "A = B - A - CF; CF = b, SF = !b")

    def _dec_b(self, pc, opcode):
        #00 0011 0011 B = B - 1; CF -, SF !c; CC16 
        return ("dec B", "B = B - 1; CF -, SF !b")

    def _movp_mhl_a(self, pc, opcode):
        #00 0011 0100 M[HL] = M[H:L+1] = A, L = L + 2; CF -, SF 1; CC16
        return ("movp M[HL], A", "M[HL] = M[H:L+1] = A, L = L + 2; CF -, SF 1")

    def _osc_int(self, pc, opcode):
        #00 0011 0101 ?clock from interlal oscillation (resistor); CF -, SF 1; CC16
        return ("osc int", "?clock from interlal oscillation (resistor); CF -, SF 1")

    def _out_bz_0(self, pc, opcode):
        #00 0011 1011 BZ = 0; CF -, SF 1; CC16, Reset buzzer pin (+3V)
        return ("out BZ, 0", "BZ = 0; CF -, SF 1; Reset buzzer pin (+3V)")

    def _0037(self, pc, opcode):
        #00 0011 0111 ?IOP direction; CF -, SF 1; CC16
        return "?IOP direction"

    def _wait_com(self, pc, opcode):
        #00 0011 1000 ?wait next com
        return ("wait com", "?wait next com")

    def _mov_b_l(self, pc, opcode):
        #00 0011 1001 B = L; CF -, SF 1; CC16
        return ("mov B, L", "B = L; CF -, SF 1")

    def _clearm_mhl_inc(self, pc, opcode):
        #00 0011 1010 (L = L + 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 1; CC16 * (n - 1) + CC32
        return ("clearm M[H:++L] (B-- > 0)", "(L = L + 1, M[HL] = A = 0, B = B - 1)WHILE(B >= 0); CF 0, SF 1")
        
    def _dec_mhl(self, pc, opcode):
        #00 0011 1101 A = M[HL] = M[HL] - 1; CF b, SF !b; CC16
        return ("dec M[HL]", "A = M[HL] = M[HL] - 1; CF b, SF !b")

    def _mov_mh4linc_imm(self, pc, opcode):
        #00 0100 iiii M[HL] = IMM, H = B = 4, L = L + 1; CF -, SF !c; CC16
        return ("mov M[H(4):L++], 0x%0.1X" % (opcode & 0xF), "M[HL] = IMM, H = B = 4, L = L + 1; CF -, SF !c")

    def _mov_mh4ldec_imm(self, pc, opcode):
        #00 0101 iiii M[HL] = IMM, H = B = 4, L = L - 1; CF -, SF !b; CC16
        return ("mov M[H(4):L--], 0x%0.1X" % (opcode & 0xF), "M[HL] = IMM, H = B = 4, L = L - 1; CF -, SF !b")

    def _mov_mhlinc_imm(self, pc, opcode):
        #00 0110 iiii M[HL] = IMM, L = L + 1; CF -, SF !c; CC16
        return ("mov M[H:L++], 0x%0.1X" % (opcode & 0xF), "M[HL] = IMM, L = L + 1; CF -, SF !c")

    def _mov_mhl_imm(self, pc, opcode):
        #00 0111 iiii M[HL] = IMM, H = B = B + 1, A = 0; CF 0, SF !c; CC16
        return ("mov M[H(B++):L], 0x%0.1X" % (opcode & 0xF), "M[HL] = IMM, H = B = B + 1, A = 0; CF 0, SF 1")

    def _movm_mhlsubi_mhl(self, pc, opcode):
        #00 1000 iiii (M[H:L-IMM] = M[HL], L = L + 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); CC24 * (n - 1) + CC32
        return ("movm M[H:L-0x%0.1X], M[H:L++] (B++ < 15)" % (opcode & 0xF), "(M[H:L-IMM] = M[HL], L = L + 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0)")

    def _movm_mhladdi_mhl(self, pc, opcode):
        #00 1001 iiii (M[H:L+IMM] = M[HL], L = L - 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0); CC24 * (n - 1) + CC32
        return ("movm M[H:L+0x%0.1X], M[H:L--] (B++ < 15)" % (opcode & 0xF), "(M[H:L+IMM] = M[HL], L = L - 1, B = B + 1)WHILE(B <= 15), B = IMM - 1; CF 0, SF (IMM != 0)")

    def _inc_m1i(self, pc, opcode):
        #00 1010 iiii A = M[1:IMM] = M[1:IMM] + 1; CF c, SF !c; CC16
        return ("inc M[0x1%0.1X]" % (opcode & 0xF), "A = M[1:IMM] = M[1:IMM] + 1; CF c, SF !c")

    def _dec_m1i(self, pc, opcode):
        #00 1011 iiii A = M[1:IMM] = M[1:IMM] - 1; CF b, SF !b; CC16
        return ("dec M[0x1%0.1X]" % (opcode & 0xF), "A = M[1:IMM] = M[1:IMM] - 1; CF b, SF !b")

    def _addc10m_mhl_mbl(self, pc, opcode):
        #00 1100 iiii (A = M[HL] = (M[HL] + M[BL] + CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF c, SF 0; CC20 * (n - 1) + CC32
        return ("addc10m M[H:L++], M[BL] (L < 0x%0.1X)" % (16 - (opcode & 0xF)), "(A = M[HL] = (M[HL] + M[BL] + CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF c, SF 0")

    def _subc10m_mhl_mbl(self, pc, opcode):
        #00 1101 iiii (A = M[HL] = (M[HL] - M[BL] - CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF b, SF 0; CC20 * (n - 1) + CC32
        return ("subc10m M[H:L++], M[BL] (L < 0x%0.1X)" % (16 - (opcode & 0xF)), "(A = M[HL] = (M[HL] - M[BL] - CF) mod 10, L = L + 1)WHILE(L < 16 - IMM); CF b, SF 0")

    def _out_outp_imm(self, pc, opcode):
        #00 1110 iiii A = OUTP = IMM; CF 0, SF 1, CC16
        return ("out OUTP, 0x%0.1X" % (opcode & 0xF), "A = OUTP = IMM; CF 0, SF 1")

    def _out_iop_imm(self, pc, opcode):
        #00 1111 iiii A = IOP = IMM; CF 0, SF 1, CC16
        return ("out IOP, 0x%0.1X" % (opcode & 0xF), "A = IOP = IMM; CF 0, SF 1")

    def _sbit_m(self, pc, opcode):
        #01 00bb hiii if (h) (if (b == 1) A = M[HL] |= B else A = M[HL]) else (A = M[0:IMM].b = 1); CF 0, SF 1; CC16
        bb = (opcode >> 4) & 0x3
        if (opcode & 0x8):
            if (((opcode >> 4) & 0x3) == 1):
                return ("sbit A M[HL], B", "A = M[HL] |= B; CF 0, SF 1")
            return ("sbit A M[HL], 0", "A = M[HL] | 0; CF 0, SF 1")
        else:
            return ("sbit M[0x%0.2X].%0.1X" % ((opcode & 0x7), bb), "A = M[0:IMM].b = 1; CF 0, SF 1")

    def _rbit_m(self, pc, opcode):
        #01 01bb hiii if (h) (if (b == 1) A = M[HL] &= ~B else A = M[HL]) else (A = M[0:IMM].b = 0); CF 0, SF 1; CC16
        bb = (opcode >> 4) & 0x3
        if (opcode & 0x8):
            if (((opcode >> 4) & 0x3) == 1):
                return ("rbit A M[HL], B", "A = M[HL] = M[HL] & ~B; CF 0, SF 1")
            return ("rbit A M[HL], 0", "A = M[HL] = M[HL] & ~0; CF 0, SF 1")
        else:
            return ("rbit A M[0x%0.2X].%0.1X" % ((opcode & 0x7), bb), "A = M[0:IMM].b = 0; CF 0, SF 1")
            
    def _tbit_m(self, pc, opcode):
        #01 10bb hiii if (h and b == 1) (M[HL] > (M[HL] | B)) else (M[(HL if h)/0:IMM].b == 0); CF -, SF res; CC16
        bb = (opcode >> 4) & 0x3
        if (opcode & 0x8):
            if (bb == 1):
                return ("tbit M[HL], B", "M[HL] > (M[HL] | B); CF -, SF res")
            return ("tbit M[HL], 0", "M[HL] > (M[HL] | 0); CF -, SF res")
        else:
            return ("tbit M[0x%0.2X].%0.1X" % ((opcode & 0x7), bb), "M[0:IMM].b == 0; CF -, SF res")
            
    def _outm_lcd_mhl(self, pc, opcode):
        #01 1100 iiii (LCDP = M[HL], L = L - 1)WHILE((L + 1) >= IMM), H = A = A + 1, L = 0xF; CF A==0, SF !(A==0), CC16 * (n - 1) + CC32
        return ("outm LCDP, M[H:L--] (L >= 0x%0.1X)" % ((opcode - 1) & 0xF), "(LCDP = M[HL], L = L - 1)WHILE((L + 1) >= IMM), H = A = A + 1, L = 0xF; CF A==0, SF !(A==0)")

    def _mov_pch_imm(self, pc, opcode):
        #01 1101 iiii PC<11:8> = IMM; CF -, SF -?; CC16
        return ("mov PC<11:8>, 0x%0.1X" % (opcode & 0xF), "PC<11:8> = IMM; CF -, SF -?")

    def _cmp_mhl_imm(self, pc, opcode):
        #01 1110 iiii A = M[HL] - IMM; CF b, SF z; CC32
        return ("cmp M[HL], 0x%0.1X" % (opcode & 0xF), "A = M[HL] - IMM; CF b, SF z")

    def _delay_nl_imm(self, pc, opcode):
        #01 1111 iiii L = IMM; CF -, SF 0; CC4 * (15 - L) + CC16
        return ("delay L, 0x%0.1X (L++ < 15)" % (opcode & 0xF), "L = IMM; CF -, SF 0; CC4 * (15 - L) + CC16")
    
    def _addc_a_imm(self, pc, opcode):
        #00 0100 iiii addc A, IMM; CF c, SF !c; CC16
        return ("addc A, 0x%0.1X" % (opcode & 0xF), "A = A + IMM + CF; CF c, SF !c; CC16 ")

    def _subc_a_imm(self, pc, opcode):
        #00 0101 iiii A = IMM - A - CF; CF = b, SF = !b; CC16
        return ("subc A, 0x%0.1X" % (opcode & 0xF), "A = IMM - A - CF; CF = b, SF = !b; CC16")

    def _mov_l_imm(self, pc, opcode):
        #10 0000 iiii L = IMM; CF -, SF 1; CC16
        return ("mov L, 0x%0.1X" % (opcode & 0xF), "L = IMM; CF -, SF 1")

    def _call0(self, pc, opcode):
        #10 hh01 iiii ?STACK0 = PC, PC = hh:0b011111:IMM, L = 0; CF -, SF 1; CC32
        return ("call0 %0.3X" % (((opcode & 0xF0) << 4) | 0xF0 | (opcode & 0xF)), "?STACK0 = PC, PC = hh:0b011111:IMM, L = 0xC; CF -, SF 1")

    def _mov_a_m0i(self, pc, opcode):
        #10 0010 iiii A = M[0:IMM]; CF 0, SF 1; CC16
        return ("mov A, M[0x0%0.1X]" % (opcode & 0xF), "A = M[0:IMM]; CF 0, SF 1")

    def _call1(self, pc, opcode):
        #10 hh11 iiii ?STACK1 = PC, PC = hh:0b111111:IMM, L = 0; CF -, SF 1; CC32
        return ("call1 %0.3X" % (((opcode & 0xF0) << 4) | 0xF0 | (opcode & 0xF)), "?STACK1 = PC, PC = hh:0b111111:IMM, L = 0xF; CF -, SF 1")

    def _mov_b_imm(self, pc, opcode):
        #10 0100 iiii B = IMM; CF -, SF 1; CC16
        return ("mov B, 0x%0.1X" % (opcode & 0xF), "B = IMM; CF -, SF 1")

    def _mov_m0i_a(self, pc, opcode):
        #10 0110 iiii M[0:IMM] = A; CF -, SF 1; CC16
        return ("mov M[0x0%0.1X], A" % (opcode & 0xF), "M[0:IMM] = A; CF -, SF 1")

    def _mov_h_imm(self, pc, opcode):
        #10 1000 iiii H = IMM; CF -, SF 1; CC16
        return ("mov H, 0x%0.1X" % (opcode & 0xF), "H = IMM; CF -, SF 1")

    def _mov_a_m1i(self, pc, opcode):
        #10 1010 iiii A = M[1:IMM]; CF 0, SF 1; CC16
        return ("mov A, M[0x1%0.1X]" % (opcode & 0xF), "A = M[1:IMM]; CF 0, SF 1")

    def _mov_a_imm(self, pc, opcode):
        #10 1100 iiii A = IMM; CF 0, SF 1; CC16
        return ("mov A, 0x%0.1X" % (opcode & 0xF), "A = IMM; CF 0, SF 1")

    def _mov_m1i_a(self, pc, opcode):
        #10 1110 iiii M[1:IMM] = A; CF -, SF 1; CC16
        return ("mov M[0x1%0.1X], A" % (opcode & 0xF), "M[1:IMM] = A; CF -, SF 1")

    def _bs_imm(self, pc, opcode):
        #11 iiii iiii if SF (PC<7:0> = IMM); CF -, SF 1; CC16
        if ((self._prev_opcode & 0x3F0) == 0b0111010000):
            return ("bs %0.3X" % (((self._prev_opcode & 0xF) << 8) | (opcode & 0x0FF)), "if SF (PC<7:0> = IMM); CF -, SF 1")
        return ("bs %0.3X" % ((pc & 0xF00) | (opcode & 0x0FF)), "if SF (PC<7:0> = IMM); CF -, SF 1")
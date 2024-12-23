class HT4BITdasm():

    def __init__(self):
        self._base = '0x%X'
        self._bytebase = '0x%0.2X'
        self._addrbase = '%0.3X'
        self._opbase = '%0.2X'

        self._instructions = [
            HT4BITdasm._rr_a,                          #0 0 0 0 0 0 0 0
            HT4BITdasm._rl_a,                          #0 0 0 0 0 0 0 1
            HT4BITdasm._rrc_a,                         #0 0 0 0 0 0 1 0
            HT4BITdasm._rlc_a,                         #0 0 0 0 0 0 1 1
            HT4BITdasm._mov_a_r1r0,                    #0 0 0 0 0 1 0 0
            HT4BITdasm._mov_r1r0_a,                    #0 0 0 0 0 1 0 1
            HT4BITdasm._mov_a_r3r2,                    #0 0 0 0 0 1 1 0
            HT4BITdasm._mov_r3r2_a,                    #0 0 0 0 0 1 1 1
            HT4BITdasm._adc_a_r1r0,                    #0 0 0 0 1 0 0 0
            HT4BITdasm._add_a_r1r0,                    #0 0 0 0 1 0 0 1
            HT4BITdasm._sbc_a_r1r0,                    #0 0 0 0 1 0 1 0
            HT4BITdasm._sub_a_r1r0,                    #0 0 0 0 1 0 1 1
            HT4BITdasm._inc_r1r0,                      #0 0 0 0 1 1 0 0
            HT4BITdasm._dec_r1r0,                      #0 0 0 0 1 1 0 1
            HT4BITdasm._inc_r3r2,                      #0 0 0 0 1 1 1 0
            HT4BITdasm._dec_r3r2,                      #0 0 0 0 1 1 1 1
            HT4BITdasm._inc_rn,                        #0 0 0 1 0 0 0 0
            HT4BITdasm._dec_rn,                        #0 0 0 1 0 0 0 1
            HT4BITdasm._inc_rn,                        #0 0 0 1 0 0 1 0
            HT4BITdasm._dec_rn,                        #0 0 0 1 0 0 1 1
            HT4BITdasm._inc_rn,                        #0 0 0 1 0 1 0 0
            HT4BITdasm._dec_rn,                        #0 0 0 1 0 1 0 1
            HT4BITdasm._inc_rn,                        #0 0 0 1 0 1 1 0
            HT4BITdasm._dec_rn,                        #0 0 0 1 0 1 1 1
            HT4BITdasm._inc_rn,                        #0 0 0 1 1 0 0 0
            HT4BITdasm._dec_rn,                        #0 0 0 1 1 0 0 1
            HT4BITdasm._and_a_r1r0,                    #0 0 0 1 1 0 1 0
            HT4BITdasm._xor_a_r1r0,                    #0 0 0 1 1 0 1 1
            HT4BITdasm._or_a_r1r0,                     #0 0 0 1 1 1 0 0
            HT4BITdasm._and_r1r0_a,                    #0 0 0 1 1 1 0 1
            HT4BITdasm._xor_r1r0_a,                    #0 0 0 1 1 1 1 0
            HT4BITdasm._or_r1r0_a,                     #0 0 0 1 1 1 1 1
            HT4BITdasm._mov_rn_a,                      #0 0 1 0 0 0 0 0
            HT4BITdasm._mov_a_rn,                      #0 0 1 0 0 0 0 1
            HT4BITdasm._mov_rn_a,                      #0 0 1 0 0 0 1 0
            HT4BITdasm._mov_a_rn,                      #0 0 1 0 0 0 1 1
            HT4BITdasm._mov_rn_a,                      #0 0 1 0 0 1 0 0
            HT4BITdasm._mov_a_rn,                      #0 0 1 0 0 1 0 1
            HT4BITdasm._mov_rn_a,                      #0 0 1 0 0 1 1 0
            HT4BITdasm._mov_a_rn,                      #0 0 1 0 0 1 1 1
            HT4BITdasm._mov_rn_a,                      #0 0 1 0 1 0 0 0
            HT4BITdasm._mov_a_rn,                      #0 0 1 0 1 0 0 1
            HT4BITdasm._clc,                           #0 0 1 0 1 0 1 0
            HT4BITdasm._stc,                           #0 0 1 0 1 0 1 1
            HT4BITdasm._ei,                            #0 0 1 0 1 1 0 0
            HT4BITdasm._di,                            #0 0 1 0 1 1 0 1
            HT4BITdasm._ret,                           #0 0 1 0 1 1 1 0
            HT4BITdasm._reti,                          #0 0 1 0 1 1 1 1
            HT4BITdasm._out_pa_a,                      #0 0 1 1 0 0 0 0
            HT4BITdasm._inc_a,                         #0 0 1 1 0 0 0 1
            HT4BITdasm._in_a_pm,                       #0 0 1 1 0 0 1 0
            HT4BITdasm._in_a_ps,                       #0 0 1 1 0 0 1 1
            HT4BITdasm._in_a_pp,                       #0 0 1 1 0 1 0 0
            HT4BITdasm._dummy,                         #0 0 1 1 0 1 0 1
            HT4BITdasm._daa,                           #0 0 1 1 0 1 1 0
            HT4BITdasm._halt,                          #0 0 1 1 0 1 1 1  0 0 1 1 1 1 1 0
            HT4BITdasm._timer_on,                      #0 0 1 1 1 0 0 0
            HT4BITdasm._timer_off,                     #0 0 1 1 1 0 0 1
            HT4BITdasm._mov_a_tmrl,                    #0 0 1 1 1 0 1 0
            HT4BITdasm._mov_a_tmrh,                    #0 0 1 1 1 0 1 1
            HT4BITdasm._mov_tmrl_a,                    #0 0 1 1 1 1 0 0
            HT4BITdasm._mov_tmrh_a,                    #0 0 1 1 1 1 0 1
            HT4BITdasm._nop,                           #0 0 1 1 1 1 1 0
            HT4BITdasm._dec_a,                         #0 0 1 1 1 1 1 1
            HT4BITdasm._add_a_x,                       #0 1 0 0 0 0 0 0  0 0 0 0 d d d d
            HT4BITdasm._sub_a_x,                       #0 1 0 0 0 0 0 1  0 0 0 0 d d d d
            HT4BITdasm._and_a_x,                       #0 1 0 0 0 0 1 0  0 0 0 0 d d d d
            HT4BITdasm._xor_a_x,                       #0 1 0 0 0 0 1 1  0 0 0 0 d d d d
            HT4BITdasm._or_a_x,                        #0 1 0 0 0 1 0 0  0 0 0 0 d d d d
            HT4BITdasm._sound_n,                       #0 1 0 0 0 1 0 1  0 0 0 0 n n n n
            HT4BITdasm._mov_r4_x,                      #0 1 0 0 0 1 1 0  0 0 0 0 d d d d
            HT4BITdasm._timer_xx,                      #0 1 0 0 0 1 1 1  d d d d d d d d
            HT4BITdasm._sound_one,                     #0 1 0 0 1 0 0 0
            HT4BITdasm._sound_loop,                    #0 1 0 0 1 0 0 1
            HT4BITdasm._sound_off,                     #0 1 0 0 1 0 1 0
            HT4BITdasm._sound_a,                       #0 1 0 0 1 0 1 1
            HT4BITdasm._read_r4a,                      #0 1 0 0 1 1 0 0
            HT4BITdasm._readf_r4a,                     #0 1 0 0 1 1 0 1
            HT4BITdasm._read_mr0a,                     #0 1 0 0 1 1 1 0
            HT4BITdasm._readf_mr0a,                    #0 1 0 0 1 1 1 1
            *([HT4BITdasm._mov_r1r0_xx] * 16),         #0 1 0 1 d d d d  0 0 0 0 d d d d
            *([HT4BITdasm._mov_r3r2_xx] * 16),         #0 1 1 0 d d d d  0 0 0 0 d d d d
            *([HT4BITdasm._mov_a_x] * 16),             #0 1 1 1 d d d d
            *([HT4BITdasm._jan_address] * 32),         #1 0 0 n n a a a  a a a a a a a a
            *([HT4BITdasm._jnz_R0_address] * 8),       #1 0 1 0 0 a a a  a a a a a a a a
            *([HT4BITdasm._jnz_R1_address] * 8),       #1 0 1 0 1 a a a  a a a a a a a a
            *([HT4BITdasm._jz_a_address] * 8),         #1 0 1 1 0 a a a  a a a a a a a a
            *([HT4BITdasm._jnz_a_address] * 8),        #1 0 1 1 1 a a a  a a a a a a a a
            *([HT4BITdasm._jc_address] * 8),           #1 1 0 0 0 a a a  a a a a a a a a
            *([HT4BITdasm._jnc_address] * 8),          #1 1 0 0 1 a a a  a a a a a a a a
            *([HT4BITdasm._jtmr_address] * 8),         #1 1 0 1 0 a a a  a a a a a a a a
            *([HT4BITdasm._jnz_R4_address] * 8),       #1 1 0 1 1 a a a  a a a a a a a a
            *([HT4BITdasm._jmp_address] * 16),         #1 1 1 0 a a a a  a a a a a a a a
            *([HT4BITdasm._call_address] * 16),        #1 1 1 1 a a a a  a a a a a a a a
        ]

    def _instructions_override(self, overrides):
        for index, instruction in overrides.items():
            if isinstance(instruction, list):
                for i, m in enumerate(instruction):
                    if index + i < len(self._instructions):
                        self._instructions[index + i] = m
            elif index < len(self._instructions):
                self._instructions[index] = instruction

        return tuple(self._instructions)

    def disassemble(self, rom):
        if (rom.size() > 0):
            listing = [None] * rom.size()
            listing = self._disassemble(0, listing, rom)
            listing = self._disassemble(4, listing, rom)
            listing = self._disassemble(8, listing, rom)

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
            opcode = rom.getWord(pc)
            next_pcs, listing[pc] = self._instructions[opcode >> 8](self, pc, opcode)
            if (listing[pc][0] == 2 and (pc + 1) < len(listing)):
                listing[pc + 1] = (1, opcode & 0xFF, '')
            pc = next_pcs[0]
            for i, next_pc in enumerate(next_pcs):
                if (i > 0):
                    listing = self._disassemble(next_pc, listing, rom)
        return listing

    def _rr_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "rr A")

    def _rl_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "rl A")
    
    def _rrc_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "rrc A")
        
    def _rlc_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "rlc A")

    def _mov_a_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "mov A, [R1R0]")
    
    def _mov_r1r0_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "mov [R1R0], A")

    def _mov_a_r3r2(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "mov A, [R3R2]")

    def _mov_r3r2_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "mov [R3R2], A")

    def _adc_a_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "adc A, [R1R0]")
    
    def _add_a_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "add A, [R1R0]")
    
    def _sbc_a_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "sbc A, [R1R0]")
    
    def _sub_a_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "sub A, [R1R0]")

    def _inc_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "inc [R1R0]")

    def _dec_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "dec [R1R0]")

    def _inc_r3r2(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "inc [R3R2]")

    def _dec_r3r2(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "dec [R3R2]")

    def _inc_rn(self, pc, opcode):
        Rn = (opcode >> 9) & 0x7
        return (pc + 1,), (1, opcode >> 8, "inc R" + str(Rn))
    
    def _dec_rn(self, pc, opcode):
        Rn = (opcode >> 9) & 0x7
        return (pc + 1,), (1, opcode >> 8, "dec R" + str(Rn))
    
    def _and_a_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "and A, [R1R0]")
    
    def _xor_a_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "xor A, [R1R0]")
    
    def _or_a_r1r0(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "or A, [R1R0]")
    
    def _and_r1r0_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "and [R1R0], A")
    
    def _xor_r1r0_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "xor [R1R0], A")
    
    def _or_r1r0_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "or [R1R0], A")
    
    def _mov_rn_a(self, pc, opcode):
        Rn = (opcode >> 9) & 0x7
        return (pc + 1,), (1, opcode >> 8, "mov R" + str(Rn) + ", A")
    
    def _mov_a_rn(self, pc, opcode):
        Rn = (opcode >> 9) & 0x7
        return (pc + 1,), (1, opcode >> 8, "mov A, R" + str(Rn))

    def _clc(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "clc")

    def _ei(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "ei")

    def _di(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "di")
        
    def _ret(self, pc, opcode):
        return (pc,), (1, opcode >> 8, "ret")

    def _reti(self, pc, opcode):
        return (pc,), (1, opcode >> 8, "reti")

    def _stc(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "stc")
    
    def _out_pa_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "out PA, A")

    def _inc_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "inc A")

    def _in_a_pm(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "in A, PM")

    def _in_a_ps(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "in A, PS")

    def _in_a_pp(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "in A, PP")

    def _dummy(self, pc, opcode):
        npc = (pc + 1) & 0xFFF
        return (npc, 0x3000 | npc, 0x2000 | npc,), (1, opcode >> 8, "db " + self._bytebase % (opcode >> 8))

    def _daa(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "daa")

    def _halt(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "halt")

    def _timer_on(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "timer on")
    
    def _timer_off(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "timer off")

    def _mov_a_tmrl(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "mov A, TMRL")

    def _mov_a_tmrh(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "mov A, TMRH")

    def _mov_tmrl_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "mov TMRL, A")

    def _mov_tmrh_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "mov TMRH, A")

    def _nop(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "nop")

    def _dec_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "dec A")
    
    def _add_a_x(self, pc, opcode):
        return (pc + 2,), (2, opcode, "add A, " + self._base % (opcode & 0xF))

    def _sub_a_x(self, pc, opcode):
        return (pc + 2,), (2, opcode, "sub A, " + self._base % (opcode & 0xF))

    def _and_a_x(self, pc, opcode):
        return (pc + 2,), (2, opcode, "and A, " + self._base % (opcode & 0xF))

    def _xor_a_x(self, pc, opcode):
        return (pc + 2,), (2, opcode, "xor A, " + self._base % (opcode & 0xF))

    def _or_a_x(self, pc, opcode):
        return (pc + 2,), (2, opcode, "or A, " + self._base % (opcode & 0xF))

    def _sound_n(self, pc, opcode):
        return (pc + 2,), (2, opcode, "sound " + str(opcode & 0xF))

    def _mov_r4_x(self, pc, opcode):
        return (pc + 2,), (2, opcode, "mov R4, " + self._base % (opcode & 0xF))

    def _timer_xx(self, pc, opcode):
        return (pc + 2,), (2, opcode >> 8, "timer " + self._base % (opcode & 0xFF))

    def _sound_one(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "sound one")

    def _sound_loop(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "sound loop")

    def _sound_off(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "sound off")

    def _sound_a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "sound A")

    def _read_r4a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "read R4A")
    
    def _readf_r4a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "readf R4A")

    def _read_mr0a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "read MR0A")

    def _readf_mr0a(self, pc, opcode):
        return (pc + 1,), (1, opcode >> 8, "readf MR0A")

    def _mov_r1r0_xx(self, pc, opcode):
        xx = ((opcode & 0x0F00) >> 8) | ((opcode & 0x0F) << 4)
        return (pc + 2,), (2, opcode, "mov R1R0, " + self._bytebase % xx)

    def _mov_r3r2_xx(self, pc, opcode):
        xx = ((opcode & 0x0F00) >> 8) | ((opcode & 0x0F) << 4)
        return (pc + 2,), (2, opcode, "mov R3R2, " + self._bytebase % xx)

    def _mov_a_x(self, pc, opcode):
        x = (opcode >> 8) & 0xF
        #if (opcode & 0xFF == 0b00110101):
        #    bank_p = ((x & 0x3) << 12) | ((pc + 2) & 0xFFF)
        #    return (pc + 1, bank_p), (1, opcode >> 8, "mov A, " + self._base % x)
        return (pc + 1,), (1, opcode >> 8, "mov A, " + self._base % x)

    def _jan_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "ja" + str((opcode >> 11) & 0x3) + " " + self._addrbase % addr)

    def _jnz_a_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "jnz A, " + self._addrbase % addr)

    def _jnz_R0_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "jnz R0, " + self._addrbase % addr)

    def _jnz_R1_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "jnz R1, " + self._addrbase % addr)

    def _jz_a_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "jz A, " + self._addrbase % addr)

    def _jc_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "jc " + self._addrbase % addr)

    def _jnc_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "jnc " + self._addrbase % addr)

    def _jtmr_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "jtmr " + self._addrbase % addr)

    def _jnz_R4_address(self, pc, opcode):
        addr = (pc & 0xF800) | (opcode & 0x07FF)
        return (pc + 2, addr), (2, opcode, "jnz R4, " + self._addrbase % addr)

    def _jmp_address(self, pc, opcode):
        addr = (pc & 0xF000) | (opcode & 0x0FFF)
        return (addr,), (2, opcode, "jmp " + self._addrbase % addr)

    def _call_address(self, pc, opcode):
        addr = (pc & 0xF000) | (opcode & 0x0FFF)
        return (pc + 2, addr), (2, opcode, "call " + self._addrbase % addr)
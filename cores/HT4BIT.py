from .rom import ROM
from .HT4BITsound import HT4BITsound

TIMER_INT_LOCATION = 4
EXTERNAL_INT_LOCATION = 8

MCLOCK_DIV = 4

class HT4BIT():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = HT4BITsound(mask, clock)

        self._timer_div = mask['timer_clock_div']

        self._instructions = [
            HT4BIT._rr_a,                          #0 0 0 0 0 0 0 0
            HT4BIT._rl_a,                          #0 0 0 0 0 0 0 1
            HT4BIT._rrc_a,                         #0 0 0 0 0 0 1 0
            HT4BIT._rlc_a,                         #0 0 0 0 0 0 1 1
            HT4BIT._mov_a_r1r0,                    #0 0 0 0 0 1 0 0
            HT4BIT._mov_r1r0_a,                    #0 0 0 0 0 1 0 1
            HT4BIT._mov_a_r3r2,                    #0 0 0 0 0 1 1 0
            HT4BIT._mov_r3r2_a,                    #0 0 0 0 0 1 1 1
            HT4BIT._adc_a_r1r0,                    #0 0 0 0 1 0 0 0
            HT4BIT._add_a_r1r0,                    #0 0 0 0 1 0 0 1
            HT4BIT._sbc_a_r1r0,                    #0 0 0 0 1 0 1 0
            HT4BIT._sub_a_r1r0,                    #0 0 0 0 1 0 1 1
            HT4BIT._inc_r1r0,                      #0 0 0 0 1 1 0 0
            HT4BIT._dec_r1r0,                      #0 0 0 0 1 1 0 1
            HT4BIT._inc_r3r2,                      #0 0 0 0 1 1 1 0
            HT4BIT._dec_r3r2,                      #0 0 0 0 1 1 1 1
            HT4BIT._inc_rn,                        #0 0 0 1 0 0 0 0
            HT4BIT._dec_rn,                        #0 0 0 1 0 0 0 1
            HT4BIT._inc_rn,                        #0 0 0 1 0 0 1 0
            HT4BIT._dec_rn,                        #0 0 0 1 0 0 1 1
            HT4BIT._inc_rn,                        #0 0 0 1 0 1 0 0
            HT4BIT._dec_rn,                        #0 0 0 1 0 1 0 1
            HT4BIT._inc_rn,                        #0 0 0 1 0 1 1 0
            HT4BIT._dec_rn,                        #0 0 0 1 0 1 1 1
            HT4BIT._inc_rn,                        #0 0 0 1 1 0 0 0
            HT4BIT._dec_rn,                        #0 0 0 1 1 0 0 1
            HT4BIT._and_a_r1r0,                    #0 0 0 1 1 0 1 0
            HT4BIT._xor_a_r1r0,                    #0 0 0 1 1 0 1 1
            HT4BIT._or_a_r1r0,                     #0 0 0 1 1 1 0 0
            HT4BIT._and_r1r0_a,                    #0 0 0 1 1 1 0 1
            HT4BIT._xor_r1r0_a,                    #0 0 0 1 1 1 1 0
            HT4BIT._or_r1r0_a,                     #0 0 0 1 1 1 1 1
            HT4BIT._mov_rn_a,                      #0 0 1 0 0 0 0 0
            HT4BIT._mov_a_rn,                      #0 0 1 0 0 0 0 1
            HT4BIT._mov_rn_a,                      #0 0 1 0 0 0 1 0
            HT4BIT._mov_a_rn,                      #0 0 1 0 0 0 1 1
            HT4BIT._mov_rn_a,                      #0 0 1 0 0 1 0 0
            HT4BIT._mov_a_rn,                      #0 0 1 0 0 1 0 1
            HT4BIT._mov_rn_a,                      #0 0 1 0 0 1 1 0
            HT4BIT._mov_a_rn,                      #0 0 1 0 0 1 1 1
            HT4BIT._mov_rn_a,                      #0 0 1 0 1 0 0 0
            HT4BIT._mov_a_rn,                      #0 0 1 0 1 0 0 1
            HT4BIT._clc,                           #0 0 1 0 1 0 1 0
            HT4BIT._stc,                           #0 0 1 0 1 0 1 1
            HT4BIT._ei,                            #0 0 1 0 1 1 0 0
            HT4BIT._di,                            #0 0 1 0 1 1 0 1
            HT4BIT._ret,                           #0 0 1 0 1 1 1 0
            HT4BIT._reti,                          #0 0 1 0 1 1 1 1
            HT4BIT._dummy,                         #0 0 1 1 0 0 0 0
            HT4BIT._inc_a,                         #0 0 1 1 0 0 0 1
            HT4BIT._dummy,                         #0 0 1 1 0 0 1 0
            HT4BIT._dummy,                         #0 0 1 1 0 0 1 1
            HT4BIT._dummy,                         #0 0 1 1 0 1 0 0
            HT4BIT._dummy,                         #0 0 1 1 0 1 0 1
            HT4BIT._daa,                           #0 0 1 1 0 1 1 0
            HT4BIT._halt,                          #0 0 1 1 0 1 1 1  0 0 1 1 1 1 1 0
            HT4BIT._timer_on,                      #0 0 1 1 1 0 0 0
            HT4BIT._timer_off,                     #0 0 1 1 1 0 0 1
            HT4BIT._mov_a_tmrl,                    #0 0 1 1 1 0 1 0
            HT4BIT._mov_a_tmrh,                    #0 0 1 1 1 0 1 1
            HT4BIT._mov_tmrl_a,                    #0 0 1 1 1 1 0 0
            HT4BIT._mov_tmrh_a,                    #0 0 1 1 1 1 0 1
            HT4BIT._nop,                           #0 0 1 1 1 1 1 0
            HT4BIT._dec_a,                         #0 0 1 1 1 1 1 1
            HT4BIT._add_a_x,                       #0 1 0 0 0 0 0 0  0 0 0 0 d d d d
            HT4BIT._sub_a_x,                       #0 1 0 0 0 0 0 1  0 0 0 0 d d d d
            HT4BIT._and_a_x,                       #0 1 0 0 0 0 1 0  0 0 0 0 d d d d
            HT4BIT._xor_a_x,                       #0 1 0 0 0 0 1 1  0 0 0 0 d d d d
            HT4BIT._or_a_x,                        #0 1 0 0 0 1 0 0  0 0 0 0 d d d d
            HT4BIT._sound_n,                       #0 1 0 0 0 1 0 1  0 0 0 0 n n n n
            HT4BIT._mov_r4_x,                      #0 1 0 0 0 1 1 0  0 0 0 0 d d d d
            HT4BIT._timer_xx,                      #0 1 0 0 0 1 1 1  d d d d d d d d
            HT4BIT._sound_one,                     #0 1 0 0 1 0 0 0
            HT4BIT._sound_loop,                    #0 1 0 0 1 0 0 1
            HT4BIT._sound_off,                     #0 1 0 0 1 0 1 0
            HT4BIT._sound_a,                       #0 1 0 0 1 0 1 1
            HT4BIT._read_r4a,                      #0 1 0 0 1 1 0 0
            HT4BIT._readf_r4a,                     #0 1 0 0 1 1 0 1
            HT4BIT._read_mr0a,                     #0 1 0 0 1 1 1 0
            HT4BIT._readf_mr0a,                    #0 1 0 0 1 1 1 1
            *([HT4BIT._mov_r1r0_xx] * 16),         #0 1 0 1 d d d d  0 0 0 0 d d d d
            *([HT4BIT._mov_r3r2_xx] * 16),         #0 1 1 0 d d d d  0 0 0 0 d d d d
            *([HT4BIT._mov_a_x] * 16),             #0 1 1 1 d d d d
            *([HT4BIT._jan_address] * 32),         #1 0 0 n n a a a  a a a a a a a a
            *([HT4BIT._jnz_R0_address] * 8),       #1 0 1 0 0 a a a  a a a a a a a a
            *([HT4BIT._jnz_R1_address] * 8),       #1 0 1 0 1 a a a  a a a a a a a a
            *([HT4BIT._jz_a_address] * 8),         #1 0 1 1 0 a a a  a a a a a a a a
            *([HT4BIT._jnz_a_address] * 8),        #1 0 1 1 1 a a a  a a a a a a a a
            *([HT4BIT._jc_address] * 8),           #1 1 0 0 0 a a a  a a a a a a a a
            *([HT4BIT._jnc_address] * 8),          #1 1 0 0 1 a a a  a a a a a a a a
            *([HT4BIT._jtmr_address] * 8),         #1 1 0 1 0 a a a  a a a a a a a a
            *([HT4BIT._jnz_R4_address] * 8),       #1 1 0 1 1 a a a  a a a a a a a a
            *([HT4BIT._jmp_address] * 16),         #1 1 1 0 a a a a  a a a a a a a a
            *([HT4BIT._call_address] * 16),        #1 1 1 1 a a a a  a a a a a a a a
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
    
    def _reset(self):
        self._ACC = 0
        self._WR = [0] * 5

        self._PC = 0
        self._STACK = 0

        self._EI = 0
        self._CF = 0
        self._TF = 0
        self._EF = 0
        self._HALT = 0
        self._RESET = 0

        self._TIMERF = 0

        self._TC = 0
        self._timer_clock_counter = 0

        self._instr_counter = 0

        self._sound.set_sound_off()
        self._sound.set_one_cycle()

    def reset(self):
        self._reset()

    def pc(self):
        return self._PC
    
    def get_ROM(self):
        return self._ROM

    def istr_counter(self):
        return self._instr_counter

    def clock(self):
        if (not self._HALT | self._RESET):
            if (self._EI and self._STACK == 0):
                if (self._EF):
                    self._EF = 0
                    self._interrupt(EXTERNAL_INT_LOCATION)
                elif (self._TF):
                    self._TF = 0
                    self._interrupt(TIMER_INT_LOCATION)

            opcode = self._ROM.getByte(self._PC)
            exec_cycles = self._execute[opcode](self, opcode)

            self._sound.clock(exec_cycles)

            self._timer_clock_counter -= exec_cycles
            while (self._timer_clock_counter <= 0):
                self._timer_clock_counter += self._timer_div
                if (self._TIMERF):
                    self._TC = (self._TC + 1) & 0xFF
                    if (self._TC == 0):
                        self._TF = 1

            self._instr_counter += 1
            return exec_cycles
        
        return 8

    def _interrupt(self, location):
        self._STACK = (self._CF << 12) | (self._PC & 0xFFF)
        self._PC =  (self._PC & 0xF000) | location

    def _read_RAM(self, rp):
        return self._RAM[(self._WR[rp + 1] << 4) | self._WR[rp]]
         
    def _write_RAM(self, rp, value):
        self._RAM[(self._WR[rp + 1] << 4) | self._WR[rp]] = value
    
    def _rr_a(self, opcode):
        self._CF = self._ACC & 0x1
        self._ACC = (self._CF << 3) | (self._ACC >> 1)
        self._PC += 1

        return 4

    def _rl_a(self, opcode):
        self._CF = self._ACC >> 3
        self._ACC = self._CF | (self._ACC << 1) & 0xF
        self._PC += 1

        return 4
    
    def _rrc_a(self, opcode):
        new_CF = self._ACC & 0x1
        self._ACC = (self._CF << 3) | (self._ACC >> 1)
        self._CF = new_CF
        self._PC += 1

        return 4
        
    def _rlc_a(self, opcode):
        new_CF = self._ACC >> 3
        self._ACC = self._CF | (self._ACC << 1) & 0xF
        self._CF = new_CF
        self._PC += 1

        return 4

    def _mov_a_r1r0(self, opcode):
        self._ACC = self._read_RAM(0)
        self._PC += 1

        return 4
    
    def _mov_r1r0_a(self, opcode):
        self._write_RAM(0, self._ACC)
        self._PC += 1

        return 4

    def _mov_a_r3r2(self, opcode):
        self._ACC = self._read_RAM(2) 
        self._PC += 1

        return 4

    def _mov_r3r2_a(self, opcode):
        self._write_RAM(2, self._ACC)
        self._PC += 1

        return 4

    def _adc_a_r1r0(self, opcode):
        self._ACC += self._read_RAM(0) + self._CF
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 4
    
    def _add_a_r1r0(self, opcode):
        self._ACC += self._read_RAM(0)
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 4
    
    def _sbc_a_r1r0(self, opcode):
        self._ACC += (~self._read_RAM(0) & 0xF) + self._CF
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 4
    
    def _sub_a_r1r0(self, opcode):
        self._ACC += (~self._read_RAM(0) & 0xF) + 1
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 4

    def _inc_r1r0(self, opcode):
        self._write_RAM(0, (self._read_RAM(0) + 1) & 0xF)
        self._PC += 1

        return 4

    def _dec_r1r0(self, opcode):
        self._write_RAM(0, (self._read_RAM(0) - 1) & 0xF)
        self._PC += 1

        return 4

    def _inc_r3r2(self, opcode):
        self._write_RAM(2, (self._read_RAM(2) + 1) & 0xF)
        self._PC += 1

        return 4

    def _dec_r3r2(self, opcode):
        self._write_RAM(2, (self._read_RAM(2) - 1) & 0xF)
        self._PC += 1

        return 4

    def _inc_rn(self, opcode):
        WRi = (opcode >> 1) & 0x7
        self._WR[WRi] = (self._WR[WRi] + 1) & 0xF
        self._PC += 1

        return 4
    
    def _dec_rn(self, opcode):
        WRi = (opcode >> 1) & 0x7
        self._WR[WRi] = (self._WR[WRi] - 1) & 0xF
        self._PC += 1

        return 4
    
    def _and_a_r1r0(self, opcode):
        self._ACC &= self._read_RAM(0) 
        self._PC += 1

        return 4
    
    def _xor_a_r1r0(self, opcode):
        self._ACC ^= self._read_RAM(0) 
        self._PC += 1

        return 4
    
    def _or_a_r1r0(self, opcode):
        self._ACC |= self._read_RAM(0) 
        self._PC += 1

        return 4
    
    def _and_r1r0_a(self, opcode):
        self._write_RAM(0, self._read_RAM(0) & self._ACC)
        self._PC += 1

        return 4
    
    def _xor_r1r0_a(self, opcode):
        self._write_RAM(0, self._read_RAM(0) ^ self._ACC)
        self._PC += 1

        return 4
    
    def _or_r1r0_a(self, opcode):
        self._write_RAM(0, self._read_RAM(0) | self._ACC)
        self._PC += 1

        return 4
    
    def _mov_rn_a(self, opcode):
        self._WR[(opcode >> 1) & 0x7] = self._ACC
        self._PC += 1

        return 4
    
    def _mov_a_rn(self, opcode):
        self._ACC = self._WR[(opcode >> 1) & 0x7]
        self._PC += 1

        return 4

    def _clc(self, opcode):
        self._CF = 0
        self._PC += 1

        return 4

    def _ei(self, opcode):
        self._EI = 1
        self._PC += 1

        return 4

    def _di(self, opcode):
        self._EI = 0
        self._PC += 1

        return 4
        
    def _ret(self, opcode):
        self._PC =  (self._PC & 0xF000) | (self._STACK & 0xFFF)
        self._STACK = 0

        return 4

    def _reti(self, opcode):
        self._PC =  (self._PC & 0xF000) | (self._STACK & 0xFFF)
        self._CF = (self._STACK >> 12)
        self._STACK = 0

        return 4

    def _stc(self, opcode):
        self._CF = 1
        self._PC += 1

        return 4

    def _inc_a(self, opcode):
        self._ACC = (self._ACC + 1) & 0xF
        self._PC += 1

        return 4

    def _dummy(self, opcode):
        self._PC += 1

        return 4

    def _daa(self, opcode):
        if (self._ACC > 9 or self._CF):
            self._ACC = (self._ACC + 6) & 0xF
            self._CF = 1
        self._PC += 1

        return 4

    def _halt(self, opcode):
        self._PC += 2
        self._HALT = 1
        self._EF = 0
        self._sound.set_sound_off()

        return 8

    def _timer_on(self, opcode):
        self._TIMERF = 1
        self._PC += 1

        return 4

    def _timer_off(self, opcode):
        self._TIMERF = 0
        self._PC += 1

        return 4

    def _mov_a_tmrl(self, opcode):
        self._ACC = self._TC & 0xF
        self._PC += 1

        return 4

    def _mov_a_tmrh(self, opcode):
        self._ACC = (self._TC >> 4) & 0xF
        self._PC += 1

        return 4

    def _mov_tmrl_a(self, opcode):
        self._TC = (self._TC & 0xF0) | self._ACC
        self._PC += 1

        return 4

    def _mov_tmrh_a(self, opcode):
        self._TC = (self._TC & 0x0F) | (self._ACC << 4)
        self._PC += 1

        return 4

    def _nop(self, opcode):
        self._PC += 1

        return 4

    def _dec_a(self, opcode):
        self._ACC = (self._ACC - 1) & 0xF
        self._PC += 1

        return 4

    def _add_a_x(self, opcode):
        self._ACC += self._ROM.getByte(self._PC + 1) & 0xF
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 2

        return 8

    def _sub_a_x(self, opcode):
        self._ACC += (~self._ROM.getByte(self._PC + 1) & 0xF) + 1
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 2

        return 8

    def _and_a_x(self, opcode):
        self._ACC &= self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 8

    def _xor_a_x(self, opcode):
        self._ACC ^= self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 8

    def _or_a_x(self, opcode):
        self._ACC |= self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 8

    def _sound_n(self, opcode):
        self._sound.set_sound_channel(self._ROM.getByte(self._PC + 1) & 0xF)
        self._PC += 2

        return 8

    def _mov_r4_x(self, opcode):
        self._WR[4] = self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 8

    def _timer_xx(self, opcode):
        self._TC = self._ROM.getByte(self._PC + 1)
        self._PC += 2

        return 8

    def _sound_one(self, opcode):
        self._sound.set_one_cycle()
        self._PC += 1

        return 4

    def _sound_loop(self, opcode):
        self._sound.set_repeat_cycle()
        self._PC += 1

        return 4

    def _sound_off(self, opcode):
        self._sound.set_sound_off()
        self._PC += 1

        return 4

    def _sound_a(self, opcode):
        self._sound.set_sound_channel(self._ACC)
        self._PC += 1

        return 4

    def _read_r4a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte((self._PC & 0xFF00) | (self._ACC << 4) | self._read_RAM(0))
        self._ACC = byte & 0xF
        self._WR[4] = (byte >> 4) & 0xF

        return 8
    
    def _readf_r4a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte((self._PC & 0xF000) | 0xF00 | (self._ACC << 4) | self._read_RAM(0))
        self._ACC = byte & 0xF
        self._WR[4] = (byte >> 4) & 0xF

        return 8

    def _read_mr0a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte((self._PC & 0xFF00) | (self._ACC << 4) | self._WR[4])
        self._ACC = byte & 0xF
        self._write_RAM(0, (byte >> 4) & 0xF)

        return 8

    def _readf_mr0a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte((self._PC & 0xF000) | 0xF00 | (self._ACC << 4) | self._WR[4])
        self._ACC = byte & 0xF
        self._write_RAM(0, (byte >> 4) & 0xF)

        return 8

    def _mov_r1r0_xx(self, opcode):
        self._WR[0] = opcode & 0xF
        self._WR[1] = self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 8

    def _mov_r3r2_xx(self, opcode):
        self._WR[2] = opcode & 0xF
        self._WR[3] = self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 8

    def _mov_a_x(self, opcode):
        self._ACC = opcode & 0xF
        self._PC += 1

        return 4

    def _jan_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (self._ACC & (0x1 << ((opcode >> 3) & 0x3))):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al

        return 8

    def _jnz_R0_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (self._WR[0]):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al

        return 8

    def _jnz_R1_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (self._WR[1]):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al

        return 8

    def _jz_a_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (self._ACC == 0):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al

        return 8

    def _jnz_a_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (self._ACC):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al

        return 8

    def _jc_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (self._CF):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al

        return 8

    def _jnc_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (not self._CF):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al

        return 8

    def _jtmr_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (self._TF):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al
            self._TF = 0

        return 8

    def _jnz_R4_address(self, opcode):
        al = self._ROM.getByte(self._PC + 1)
        self._PC += 2
        if (self._WR[4]):
            self._PC = (self._PC & 0xF800) | ((opcode & 0x7) << 8) | al

        return 8

    def _jmp_address(self, opcode):
        self._PC = (self._PC & 0xF000) | ((opcode & 0xF) << 8) | self._ROM.getByte(self._PC + 1)

        return 8

    def _call_address(self, opcode):
        self._STACK = (self._PC + 2) & 0xFFF
        self._PC = (self._PC & 0xF000) | ((opcode & 0xF) << 8) | self._ROM.getByte(self._PC + 1)

        return 8
from .rom import ROM
from .HT943sound import HT943sound

ROM_SIZE = 0x1000

TIMER_INT_LOCATION = 4
EXTERNAL_INT_LOCATION = 8
EMPTY_VRAM = tuple([0] * 256)
FUULL_VRAM = tuple([255] * 256)

MCLOCK_DIV = 4

class HT943():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = HT943sound(mask, clock)
        
        self._reset()

        self._PP = mask['port_pullup']['PP']
        self._PS = mask['port_pullup']['PS']
        self._PM = mask['port_pullup']['PM']

        self._PP_pullup_mask = mask['port_pullup']['PP']
        self._PS_pullup_mask = mask['port_pullup']['PS']
        self._PM_pullup_mask = mask['port_pullup']['PM']

        self._PP_wakeup_mask = mask['port_wakeup']['PP']
        self._PS_wakeup_mask = mask['port_wakeup']['PS']
        self._PM_wakeup_mask = mask['port_wakeup']['PM']


        self._timer_div = mask['timer_clock_div']

        self._execute = (
            HT943._rr_a,                          #0 0 0 0 0 0 0 0
            HT943._rl_a,                          #0 0 0 0 0 0 0 1
            HT943._rrc_a,                         #0 0 0 0 0 0 1 0
            HT943._rlc_a,                         #0 0 0 0 0 0 1 1
            HT943._mov_a_r1r0,                    #0 0 0 0 0 1 0 0
            HT943._mov_r1r0_a,                    #0 0 0 0 0 1 0 1
            HT943._mov_a_r3r2,                    #0 0 0 0 0 1 1 0
            HT943._mov_r3r2_a,                    #0 0 0 0 0 1 1 1
            HT943._adc_a_r1r0,                    #0 0 0 0 1 0 0 0
            HT943._add_a_r1r0,                    #0 0 0 0 1 0 0 1
            HT943._sbc_a_r1r0,                    #0 0 0 0 1 0 1 0
            HT943._sub_a_r1r0,                    #0 0 0 0 1 0 1 1
            HT943._inc_r1r0,                      #0 0 0 0 1 1 0 0
            HT943._dec_r1r0,                      #0 0 0 0 1 1 0 1
            HT943._inc_r3r2,                      #0 0 0 0 1 1 1 0
            HT943._dec_r3r2,                      #0 0 0 0 1 1 1 1
            HT943._inc_rn,                        #0 0 0 1 0 0 0 0
            HT943._dec_rn,                        #0 0 0 1 0 0 0 1
            HT943._inc_rn,                        #0 0 0 1 0 0 1 0
            HT943._dec_rn,                        #0 0 0 1 0 0 1 1
            HT943._inc_rn,                        #0 0 0 1 0 1 0 0
            HT943._dec_rn,                        #0 0 0 1 0 1 0 1
            HT943._inc_rn,                        #0 0 0 1 0 1 1 0
            HT943._dec_rn,                        #0 0 0 1 0 1 1 1
            HT943._inc_rn,                        #0 0 0 1 1 0 0 0
            HT943._dec_rn,                        #0 0 0 1 1 0 0 1
            HT943._and_a_r1r0,                    #0 0 0 1 1 0 1 0
            HT943._xor_a_r1r0,                    #0 0 0 1 1 0 1 1
            HT943._or_a_r1r0,                     #0 0 0 1 1 1 0 0
            HT943._and_r1r0_a,                    #0 0 0 1 1 1 0 1
            HT943._xor_r1r0_a,                    #0 0 0 1 1 1 1 0
            HT943._or_r1r0_a,                     #0 0 0 1 1 1 1 1
            HT943._mov_rn_a,                      #0 0 1 0 0 0 0 0
            HT943._mov_a_rn,                      #0 0 1 0 0 0 0 1
            HT943._mov_rn_a,                      #0 0 1 0 0 0 1 0
            HT943._mov_a_rn,                      #0 0 1 0 0 0 1 1
            HT943._mov_rn_a,                      #0 0 1 0 0 1 0 0
            HT943._mov_a_rn,                      #0 0 1 0 0 1 0 1
            HT943._mov_rn_a,                      #0 0 1 0 0 1 1 0
            HT943._mov_a_rn,                      #0 0 1 0 0 1 1 1
            HT943._mov_rn_a,                      #0 0 1 0 1 0 0 0
            HT943._mov_a_rn,                      #0 0 1 0 1 0 0 1
            HT943._clc,                           #0 0 1 0 1 0 1 0
            HT943._stc,                           #0 0 1 0 1 0 1 1
            HT943._ei,                            #0 0 1 0 1 1 0 0
            HT943._di,                            #0 0 1 0 1 1 0 1
            HT943._ret,                           #0 0 1 0 1 1 1 0
            HT943._reti,                          #0 0 1 0 1 1 1 1
            HT943._out_pa_a,                      #0 0 1 1 0 0 0 0
            HT943._inc_a,                         #0 0 1 1 0 0 0 1
            HT943._in_a_pm,                       #0 0 1 1 0 0 1 0
            HT943._in_a_ps,                       #0 0 1 1 0 0 1 1
            HT943._in_a_pp,                       #0 0 1 1 0 1 0 0
            HT943._dummy,                         #0 0 1 1 0 1 0 1
            HT943._daa,                           #0 0 1 1 0 1 1 0
            HT943._halt,                          #0 0 1 1 0 1 1 1  0 0 1 1 1 1 1 0
            HT943._timer_on,                      #0 0 1 1 1 0 0 0
            HT943._timer_off,                     #0 0 1 1 1 0 0 1
            HT943._mov_a_tmrl,                    #0 0 1 1 1 0 1 0
            HT943._mov_a_tmrh,                    #0 0 1 1 1 0 1 1
            HT943._mov_tmrl_a,                    #0 0 1 1 1 1 0 0
            HT943._mov_tmrh_a,                    #0 0 1 1 1 1 0 1
            HT943._nop,                           #0 0 1 1 1 1 1 0
            HT943._dec_a,                         #0 0 1 1 1 1 1 1
            HT943._add_a_x,                       #0 1 0 0 0 0 0 0  0 0 0 0 d d d d
            HT943._sub_a_x,                       #0 1 0 0 0 0 0 1  0 0 0 0 d d d d
            HT943._and_a_x,                       #0 1 0 0 0 0 1 0  0 0 0 0 d d d d
            HT943._xor_a_x,                       #0 1 0 0 0 0 1 1  0 0 0 0 d d d d
            HT943._or_a_x,                        #0 1 0 0 0 1 0 0  0 0 0 0 d d d d
            HT943._sound_n,                       #0 1 0 0 0 1 0 1  0 0 0 0 n n n n
            HT943._mov_r4_x,                      #0 1 0 0 0 1 1 0  0 0 0 0 d d d d
            HT943._timer_xx,                      #0 1 0 0 0 1 1 1  d d d d d d d d
            HT943._sound_one,                     #0 1 0 0 1 0 0 0
            HT943._sound_loop,                    #0 1 0 0 1 0 0 1
            HT943._sound_off,                     #0 1 0 0 1 0 1 0
            HT943._sound_a,                       #0 1 0 0 1 0 1 1
            HT943._read_r4a,                      #0 1 0 0 1 1 0 0
            HT943._readf_r4a,                     #0 1 0 0 1 1 0 1
            HT943._read_mr0a,                     #0 1 0 0 1 1 1 0
            HT943._readf_mr0a,                    #0 1 0 0 1 1 1 1
            *([HT943._mov_r1r0_xx] * 16),         #0 1 0 1 d d d d  0 0 0 0 d d d d
            *([HT943._mov_r3r2_xx] * 16),         #0 1 1 0 d d d d  0 0 0 0 d d d d
            *([HT943._mov_a_x] * 16),             #0 1 1 1 d d d d
            *([HT943._jan_address] * 32),         #1 0 0 n n a a a  a a a a a a a a
            *([HT943._jnz_R0_address] * 8),       #1 0 1 0 0 a a a  a a a a a a a a
            *([HT943._jnz_R1_address] * 8),       #1 0 1 0 1 a a a  a a a a a a a a
            *([HT943._jz_a_address] * 8),         #1 0 1 1 0 a a a  a a a a a a a a
            *([HT943._jnz_a_address] * 8),        #1 0 1 1 1 a a a  a a a a a a a a
            *([HT943._jc_address] * 8),           #1 1 0 0 0 a a a  a a a a a a a a
            *([HT943._jnc_address] * 8),          #1 1 0 0 1 a a a  a a a a a a a a
            *([HT943._jtmr_address] * 8),         #1 1 0 1 0 a a a  a a a a a a a a
            *([HT943._jnz_R4_address] * 8),       #1 1 0 1 1 a a a  a a a a a a a a
            *([HT943._jmp_address] * 16),         #1 1 1 0 a a a a  a a a a a a a a
            *([HT943._call_address] * 16),        #1 1 1 1 a a a a  a a a a a a a a
        )

    def _reset(self):
        self._ACC = 0
        self._WR = [0] * 5

        self._PC = 0
        self._STACK = 0
        self._TC = 0

        self._EI = 0
       
        self._CF = 0
        self._TF = 0
        self._EF = 0
        self._HALT = 0
        self._RESET = 0
        
        self._RAM = [0] * 256

        self._timer_clock_counter = 0

        self._instr_counter = 0
        
        self._PA = 0

        self._sound.set_sound_off()
        self._sound.set_one_cycle()

    def reset(self):
        self._reset()

    def get_clocl_div():
        return 4

    def examine(self):
        return {
            "ACC": self._ACC,
            "PC": self._PC & 0xFFF,
            "ST": self._STACK,
            "TC": self._TC,
            "CF": self._CF,
            "EF": self._EF,
            "TF": self._TF,
            "EI": self._EI,
            "HALT": self._HALT,
            "WR0": self._WR[0],
            "WR1": self._WR[1],
            "WR2": self._WR[2],
            "WR3": self._WR[3],
            "WR4": self._WR[4],
            "PP": self._PP,
            "PM": self._PM,
            "PS": self._PS,
            "PA": self._PA,
            "RAM": tuple(self._RAM),
            **self._ROM.examine(),
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] & 0xFFF
        if ("ST" in state):
            self._STACK = state["ST"] & 0xFFF
        if ("CF" in state):
            self._CF = state["CF"] & 0x1
        if ("EF" in state):
            self._EF = state["EF"] & 0x1
        if ("TF" in state):
            self._TF = state["TF"] & 0x1
        if ("EI" in state):
            self._EI = state["EI"] & 0x1
        if ("HALT" in state):
            self._HALT = state["HALT"] & 0x1
        if ("WR0" in state):
            self._WR[0] = state["WR0"] & 0xF
        if ("WR1" in state):
            self._WR[1] = state["WR1"] & 0xF
        if ("WR2" in state):
            self._WR[2] = state["WR2"] & 0xF
        if ("WR3" in state):
            self._WR[3] = state["WR3"] & 0xF
        if ("WR4" in state):
            self._WR[4] = state["WR4"] & 0xF
        if ("TC" in state):
            self._TC = state["TC"] & 0xFF
        if ("PA" in state):
            self._PA = state["PA"] & 0xF
        if ("PP" in state):
            self._PP = state["PP"] & 0xF
        if ("PM" in state):
            self._PM = state["PM"] & 0xF
        if ("PS" in state):
            self._PS = state["PS"] & 0xF
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xF
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
    
    def pin_set(self, port, pin, level):
        if (port == 'PP'):
            self._PP = ~(1 << pin) & self._PP | level << pin
            if (self._HALT):
                self._EF = (self._PP_wakeup_mask & (1 << pin)) > 0
        elif (port == 'PM'):
            self._PM = ~(1 << pin) & self._PP | level << pin
            if (self._HALT):
                self._EF = (self._PM_wakeup_mask & (1 << pin)) > 0
        elif (port == 'PS'):
            self._PS = ~(1 << pin) & self._PP | level << pin
            if (self._HALT):
                self._EF = (self._PS_wakeup_mask & (1 << pin)) > 0
        elif (port == 'RES'):
            self._reset()
            self._RESET = 1

    def pin_release(self, port, pin):
        if (port == 'PP'):
            self._PP &= ~(1 << pin)
            self._PP |= self._PP_pullup_mask & (1 << pin)
        elif (port == 'PM'):
            self._PM &= ~(1 << pin)
            self._PM |= self._PM_pullup_mask & (1 << pin)
        elif (port == 'PS'):
            self._PS &= ~(1 << pin)
            self._PS |= self._PS_pullup_mask & (1 << pin)
        elif (port == 'RES'):
            self._RESET = 0

    def pc(self):
        return self._PC & 0xFFF
    
    def get_VRAM(self):
        if (self._HALT | self._RESET):
            return EMPTY_VRAM
        return tuple(self._RAM)
    
    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter
            
    def clock(self):
        if ((not self._HALT | self._RESET) | self._EF):
            self._HALT = 0
            if (self._EI and self._STACK == 0):
                if (self._EF):
                    self._external_int()
                if (self._TF):
                    self._timer_int()

            opcode = self._ROM.getByte(self._PC)
            exec_cycles = self._execute[opcode](self, opcode)

            self._sound.clock(exec_cycles)
            self._timer_clock_counter -= exec_cycles
            if (self._timer_clock_counter <= 0):
                self._timer_clock_counter += self._timer_div
                self._TC = (self._TC + 1) & 0xFF
                if (self._TC == 0):
                    self._TF = 1

            self._instr_counter += 1
            return exec_cycles
        
        return 8

    def _timer_int(self):
        self._TF = 0
        self._STACK = (self._CF << 12) | self._PC & 0xFFF
        self._PC = TIMER_INT_LOCATION
    
    def _external_int(self):
        self._EF = 0
        self._STACK = (self._CF << 12) | self._PC & 0xFFF
        self._PC = EXTERNAL_INT_LOCATION
        
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
        self._ACC = self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._PC += 1

        return 4
    
    def _mov_r1r0_a(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] = self._ACC
        self._PC += 1

        return 4

    def _mov_a_r3r2(self, opcode):
        self._ACC = self._RAM[self._WR[3] << 4 | self._WR[2]]
        self._PC += 1

        return 4

    def _mov_r3r2_a(self, opcode):
        self._RAM[self._WR[3] << 4 | self._WR[2]] = self._ACC
        self._PC += 1

        return 4

    def _adc_a_r1r0(self, opcode):
        self._ACC += self._RAM[self._WR[1] << 4 | self._WR[0]] + self._CF
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 4
    
    def _add_a_r1r0(self, opcode):
        self._ACC += self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 4
    
    def _sbc_a_r1r0(self, opcode):
        self._ACC += (~self._RAM[self._WR[1] << 4 | self._WR[0]] & 0xF) + self._CF
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 4
    
    def _sub_a_r1r0(self, opcode):
        self._ACC += (~self._RAM[self._WR[1] << 4 | self._WR[0]] & 0xF) + 1
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 4

    def _inc_r1r0(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] = (self._RAM[self._WR[1] << 4 | self._WR[0]] + 1) & 0xF
        self._PC += 1

        return 4

    def _dec_r1r0(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] = (self._RAM[self._WR[1] << 4 | self._WR[0]] - 1) & 0xF
        self._PC += 1

        return 4

    def _inc_r3r2(self, opcode):
        self._RAM[self._WR[3] << 4 | self._WR[2]] = (self._RAM[self._WR[3] << 4 | self._WR[2]] + 1) & 0xF
        self._PC += 1

        return 4

    def _dec_r3r2(self, opcode):
        self._RAM[self._WR[3] << 4 | self._WR[2]] = (self._RAM[self._WR[3] << 4 | self._WR[2]] - 1) & 0xF
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
        self._ACC &= self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._PC += 1

        return 4
    
    def _xor_a_r1r0(self, opcode):
        self._ACC ^= self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._PC += 1

        return 4
    
    def _or_a_r1r0(self, opcode):
        self._ACC |= self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._PC += 1

        return 4
    
    def _and_r1r0_a(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] &= self._ACC
        self._PC += 1

        return 4
    
    def _xor_r1r0_a(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] ^= self._ACC
        self._PC += 1

        return 4
    
    def _or_r1r0_a(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] |= self._ACC
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
        self._PC = self._STACK & 0xFFF
        self._STACK = 0

        return 4

    def _reti(self, opcode):
        self._PC = self._STACK & 0xFFF
        self._CF = (self._STACK >> 12)
        self._STACK = 0

        return 4

    def _stc(self, opcode):
        self._CF = 1
        self._PC += 1

        return 4

    def _out_pa_a(self, opcode):
        self._PA = self._ACC
        self._PC += 1

        return 4

    def _inc_a(self, opcode):
        self._ACC = (self._ACC + 1) & 0xF
        self._PC += 1

        return 4

    def _in_a_pm(self, opcode):
        self._ACC = self._PM
        self._PC += 1

        return 4

    def _in_a_ps(self, opcode):
        self._ACC = self._PS
        self._PC += 1

        return 4

    def _in_a_pp(self, opcode):
        self._ACC = self._PP
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
        self._ROM.getByte(self._PC + 1)
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
        byte = self._ROM.getByte(self._PC & 0xF00 | (self._ACC << 4) | self._RAM[self._WR[1] << 4 | self._WR[0]])
        self._ACC = byte & 0xF
        self._WR[4] = (byte >> 4) & 0xF

        return 8
    
    def _readf_r4a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte(0xF00 | (self._ACC << 4) | self._RAM[self._WR[1] << 4 | self._WR[0]])
        self._ACC = byte & 0xF
        self._WR[4] = (byte >> 4) & 0xF

        return 8

    def _read_mr0a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte(self._PC & 0xF00 | (self._ACC << 4) | self._WR[4])
        self._ACC = byte & 0xF
        self._RAM[self._WR[1] << 4 | self._WR[0]] = (byte >> 4) & 0xF

        return 8

    def _readf_mr0a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte(0xF00 | (self._ACC << 4) | self._WR[4])
        self._ACC = byte & 0xF
        self._RAM[self._WR[1] << 4 | self._WR[0]] = (byte >> 4) & 0xF

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
        if (self._ACC & (0x1 << ((opcode >> 3) & 0x3))):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 8

    def _jnz_R0_address(self, opcode):
        if (self._WR[0]):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 8

    def _jnz_R1_address(self, opcode):
        if (self._WR[1]):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 8

    def _jz_a_address(self, opcode):
        if (self._ACC == 0):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 8

    def _jnz_a_address(self, opcode):
        if (self._ACC):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 8

    def _jc_address(self, opcode):
        if (self._CF):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 8

    def _jnc_address(self, opcode):
        if (not self._CF):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 8

    def _jtmr_address(self, opcode):
        if (self._TF):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
            self._TF = 0
        else:
            self._PC += 2

        return 8

    def _jnz_R4_address(self, opcode):
        if (self._WR[4]):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 8

    def _jmp_address(self, opcode):
        self._PC = ((opcode & 0xF) << 8) | self._ROM.getByte(self._PC + 1)

        return 8

    def _call_address(self, opcode):
        self._STACK = self._PC + 2
        self._PC = ((opcode & 0xF) << 8) | self._ROM.getByte(self._PC + 1)

        return 8
from rom import ROM
from sound import Sound

TIMER_INT_LOCATION = 4
EXTERNAL_INT_LOCATION = 8

class MCU():
    def __init__(self, mask, sound: Sound):
        self._ROM = ROM(mask['rom_path'])
        self._sound = sound
        
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
        
        self._PP = mask['port_pullup']['PP']
        self._PS = mask['port_pullup']['PS']
        self._PM = mask['port_pullup']['PM']
        self._PA = 0

        self._PP_pullup_mask = mask['port_pullup']['PP']
        self._PS_pullup_mask = mask['port_pullup']['PS']
        self._PM_pullup_mask = mask['port_pullup']['PM']

        self._PP_wakeup_mask = mask['port_wakeup']['PP']
        self._PS_wakeup_mask = mask['port_wakeup']['PS']
        self._PM_wakeup_mask = mask['port_wakeup']['PM']

        self._RAM = [0] * 256

        self._timer_div = mask['timer_clock_div']
        self._timer_clock_counter = 0

        self._execution_counter = 0
        self._mcycles_counter = 0

        self._execute = (
            MCU._rr_a,                          #0 0 0 0 0 0 0 0
            MCU._rl_a,                          #0 0 0 0 0 0 0 1
            MCU._rrc_a,                         #0 0 0 0 0 0 1 0
            MCU._rlc_a,                         #0 0 0 0 0 0 1 1
            MCU._mov_a_r1r0,                    #0 0 0 0 0 1 0 0
            MCU._mov_r1r0_a,                    #0 0 0 0 0 1 0 1
            MCU._mov_a_r3r2,                    #0 0 0 0 0 1 1 0
            MCU._mov_r3r2_a,                    #0 0 0 0 0 1 1 1
            MCU._adc_a_r1r0,                    #0 0 0 0 1 0 0 0
            MCU._add_a_r1r0,                    #0 0 0 0 1 0 0 1
            MCU._sbc_a_r1r0,                    #0 0 0 0 1 0 1 0
            MCU._sub_a_r1r0,                    #0 0 0 0 1 0 1 1
            MCU._inc_r1r0,                      #0 0 0 0 1 1 0 0
            MCU._dec_r1r0,                      #0 0 0 0 1 1 0 1
            MCU._inc_r3r2,                      #0 0 0 0 1 1 1 0
            MCU._dec_r3r2,                      #0 0 0 0 1 1 1 1
            MCU._inc_rn,                        #0 0 0 1 0 0 0 0
            MCU._dec_rn,                        #0 0 0 1 0 0 0 1
            MCU._inc_rn,                        #0 0 0 1 0 0 1 0
            MCU._dec_rn,                        #0 0 0 1 0 0 1 1
            MCU._inc_rn,                        #0 0 0 1 0 1 0 0
            MCU._dec_rn,                        #0 0 0 1 0 1 0 1
            MCU._inc_rn,                        #0 0 0 1 0 1 1 0
            MCU._dec_rn,                        #0 0 0 1 0 1 1 1
            MCU._inc_rn,                        #0 0 0 1 1 0 0 0
            MCU._dec_rn,                        #0 0 0 1 1 0 0 1
            MCU._and_a_r1r0,                    #0 0 0 1 1 0 1 0
            MCU._xor_a_r1r0,                    #0 0 0 1 1 0 1 1
            MCU._or_a_r1r0,                     #0 0 0 1 1 1 0 0
            MCU._and_r1r0_a,                    #0 0 0 1 1 1 0 1
            MCU._xor_r1r0_a,                    #0 0 0 1 1 1 1 0
            MCU._or_r1r0_a,                     #0 0 0 1 1 1 1 1
            MCU._mov_rn_a,                      #0 0 1 0 0 0 0 0
            MCU._mov_a_rn,                      #0 0 1 0 0 0 0 1
            MCU._mov_rn_a,                      #0 0 1 0 0 0 1 0
            MCU._mov_a_rn,                      #0 0 1 0 0 0 1 1
            MCU._mov_rn_a,                      #0 0 1 0 0 1 0 0
            MCU._mov_a_rn,                      #0 0 1 0 0 1 0 1
            MCU._mov_rn_a,                      #0 0 1 0 0 1 1 0
            MCU._mov_a_rn,                      #0 0 1 0 0 1 1 1
            MCU._mov_rn_a,                      #0 0 1 0 1 0 0 0
            MCU._mov_a_rn,                      #0 0 1 0 1 0 0 1
            MCU._clc,                           #0 0 1 0 1 0 1 0
            MCU._stc,                           #0 0 1 0 1 0 1 1
            MCU._ei,                            #0 0 1 0 1 1 0 0
            MCU._di,                            #0 0 1 0 1 1 0 1
            MCU._ret,                           #0 0 1 0 1 1 1 0
            MCU._reti,                          #0 0 1 0 1 1 1 1
            MCU._out_pa_a,                      #0 0 1 1 0 0 0 0
            MCU._inc_a,                         #0 0 1 1 0 0 0 1
            MCU._in_a_pm,                       #0 0 1 1 0 0 1 0
            MCU._in_a_ps,                       #0 0 1 1 0 0 1 1
            MCU._in_a_pp,                       #0 0 1 1 0 1 0 0
            MCU._dummy,                         #0 0 1 1 0 1 0 1
            MCU._daa,                           #0 0 1 1 0 1 1 0
            MCU._halt,                          #0 0 1 1 0 1 1 1  0 0 1 1 1 1 1 0
            MCU._timer_on,                      #0 0 1 1 1 0 0 0
            MCU._timer_off,                     #0 0 1 1 1 0 0 1
            MCU._mov_a_tmrl,                    #0 0 1 1 1 0 1 0
            MCU._mov_a_tmrh,                    #0 0 1 1 1 0 1 1
            MCU._mov_tmrl_a,                    #0 0 1 1 1 1 0 0
            MCU._mov_tmrh_a,                    #0 0 1 1 1 1 0 1
            MCU._nop,                           #0 0 1 1 1 1 1 0
            MCU._dec_a,                         #0 0 1 1 1 1 1 1
            MCU._add_a_x,                       #0 1 0 0 0 0 0 0  0 0 0 0 d d d d
            MCU._sub_a_x,                       #0 1 0 0 0 0 0 1  0 0 0 0 d d d d
            MCU._and_a_x,                       #0 1 0 0 0 0 1 0  0 0 0 0 d d d d
            MCU._xor_a_x,                       #0 1 0 0 0 0 1 1  0 0 0 0 d d d d
            MCU._or_a_x,                        #0 1 0 0 0 1 0 0  0 0 0 0 d d d d
            MCU._sound_n,                       #0 1 0 0 0 1 0 1  0 0 0 0 n n n n
            MCU._mov_r4_x,                      #0 1 0 0 0 1 1 0  0 0 0 0 d d d d
            MCU._timer_xx,                      #0 1 0 0 0 1 1 1  d d d d d d d d
            MCU._sound_one,                     #0 1 0 0 1 0 0 0
            MCU._sound_loop,                    #0 1 0 0 1 0 0 1
            MCU._sound_off,                     #0 1 0 0 1 0 1 0
            MCU._sound_a,                       #0 1 0 0 1 0 1 1
            MCU._read_r4a,                      #0 1 0 0 1 1 0 0
            MCU._readf_r4a,                     #0 1 0 0 1 1 0 1
            MCU._read_mr0a,                     #0 1 0 0 1 1 1 0
            MCU._readf_mr0a,                    #0 1 0 0 1 1 1 1
            *([MCU._mov_r1r0_xx] * 16),         #0 1 0 1 d d d d  0 0 0 0 d d d d
            *([MCU._mov_r3r2_xx] * 16),         #0 1 1 0 d d d d  0 0 0 0 d d d d
            *([MCU._mov_a_x] * 16),             #0 1 1 1 d d d d
            *([MCU._jan_address] * 32),         #1 0 0 n n a a a  a a a a a a a a
            *([MCU._jnz_R0_address] * 8),       #1 0 1 0 0 a a a  a a a a a a a a
            *([MCU._jnz_R1_address] * 8),       #1 0 1 0 1 a a a  a a a a a a a a
            *([MCU._jz_a_address] * 8),         #1 0 1 1 0 a a a  a a a a a a a a
            *([MCU._jnz_a_address] * 8),        #1 0 1 1 1 a a a  a a a a a a a a
            *([MCU._jc_address] * 8),           #1 1 0 0 0 a a a  a a a a a a a a
            *([MCU._jnc_address] * 8),          #1 1 0 0 1 a a a  a a a a a a a a
            *([MCU._jtmr_address] * 8),         #1 1 0 1 0 a a a  a a a a a a a a
            *([MCU._jnz_R4_address] * 8),       #1 1 0 1 1 a a a  a a a a a a a a
            *([MCU._jmp_address] * 16),         #1 1 1 0 a a a a  a a a a a a a a
            *([MCU._call_address] * 16),        #1 1 1 1 a a a a  a a a a a a a a
        )

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
            "WR": tuple(self._WR),
            "PP": self._PP,
            "PM": self._PM,
            "PS": self._PS,
            "PA": self._PA,
            "RAM": tuple(self._RAM),
            **self._ROM.examine(),
        }

    def setRAM(self, index, value):
        self._RAM[index] = value & 0xF

    def setPC(self, value):
        self._PC = value & 0xFFF

    def setSTACK(self, value):
        self._STACK = value & 0xFFF
    
    def setTC(self, value):
        self._TC = value & 0xFF

    def setCF(self, value):
        self._CF = value & 0x1

    def setEF(self, value):
        self._EF = value & 0x1

    def setTF(self, value):
        self._TF = value & 0x1

    def setEI(self, value):
        self._EI = value & 0x1

    def setHALT(self, value):
        self._HALT = value & 0x1

    def setWR(self, index, value):
        self._WR[index] = value & 0xF

    def setPP(self, value):
        self._PP = value & 0xF

    def setPM(self, value):
        self._PM = value & 0xF

    def setPS(self, value):
        self._PS = value & 0xF

    def setPA(self, value):
        self._PA = value & 0xF

    def pin_ground(self, port, pin_mask):
        if (port == 'PP'):
            self._PP &= ~pin_mask
            if (self._HALT):
                self._EF = (self._PP_wakeup_mask & pin_mask) > 0
        elif (port == 'PM'):
            self._PM &= ~pin_mask
            if (self._HALT):
                self._EF = (self._PM_wakeup_mask & pin_mask) > 0
        elif (port == 'PS'):
            self._PS &= ~pin_mask
            if (self._HALT):
                self._EF = (self._PS_wakeup_mask & pin_mask) > 0

    def pin_release(self, port, pin_mask):
        if (port == 'PP'):
            self._PP &= ~pin_mask
            self._PP |= self._PP_pullup_mask & pin_mask
        elif (port == 'PM'):
            self._PM &= ~pin_mask
            self._PM |= self._PM_pullup_mask & pin_mask
        elif (port == 'PS'):
            self._PS &= ~pin_mask
            self._PS |= self._PS_pullup_mask & pin_mask

    def PC(self):
        return self._PC & 0xFFF
    
    def get_pixels(self):
        pixels = []
        for seg in range(40):
            ram = (self._RAM[255 - seg * 2] << 4) | self._RAM[254 - seg * 2]
            for com in range(8):
                pixels.append((com, seg, (ram >> com) & (self._HALT ^ 1)))
        return tuple(pixels)
    
    def get_rom(self):
        return self._ROM
    
    def mcycles(self):
        return self._mcycles_counter
            
    def mclock(self):
        if ((not self._HALT) | self._EF):
            self._timer_clock_counter -= 4
            if (self._timer_clock_counter <= 0):
                self._timer_clock_counter = self._timer_div
                self._TC = (self._TC + 1) & 0xFF
                if (self._TC == 0):
                    self._TF = 1
            
            if (self._execution_counter <= 0):
                self._HALT = 0
                if (self._EI and self._STACK == 0):
                    if (self._EF):
                        self._external_int()
                    if (self._TF):
                        self._timer_int()

                opcode = self._ROM.getByte(self._PC)
                self._execution_counter = self._execute[opcode](self, opcode)

            self._mcycles_counter += 1
            self._execution_counter -= 1
            return self._execution_counter
        
        return 0

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

        return 1

    def _rl_a(self, opcode):
        self._CF = self._ACC >> 3
        self._ACC = self._CF | (self._ACC << 1) & 0xF
        self._PC += 1

        return 1
    
    def _rrc_a(self, opcode):
        new_CF = self._ACC & 0x1
        self._ACC = (self._CF << 3) | (self._ACC >> 1)
        self._CF = new_CF
        self._PC += 1

        return 1
        
    def _rlc_a(self, opcode):
        new_CF = self._ACC >> 3
        self._ACC = self._CF | (self._ACC << 1) & 0xF
        self._CF = new_CF
        self._PC += 1

        return 1

    def _mov_a_r1r0(self, opcode):
        self._ACC = self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._PC += 1

        return 1
    
    def _mov_r1r0_a(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] = self._ACC
        self._PC += 1

        return 1

    def _mov_a_r3r2(self, opcode):
        self._ACC = self._RAM[self._WR[3] << 4 | self._WR[2]]
        self._PC += 1

        return 1

    def _mov_r3r2_a(self, opcode):
        self._RAM[self._WR[3] << 4 | self._WR[2]] = self._ACC
        self._PC += 1

        return 1

    def _adc_a_r1r0(self, opcode):
        self._ACC += self._RAM[self._WR[1] << 4 | self._WR[0]] + self._CF
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 1
    
    def _add_a_r1r0(self, opcode):
        self._ACC += self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 1
    
    def _sbc_a_r1r0(self, opcode):
        self._ACC += (~self._RAM[self._WR[1] << 4 | self._WR[0]] & 0xF) + self._CF
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 1
    
    def _sub_a_r1r0(self, opcode):
        self._ACC += (~self._RAM[self._WR[1] << 4 | self._WR[0]] & 0xF) + 1
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 1

        return 1

    def _inc_r1r0(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] = (self._RAM[self._WR[1] << 4 | self._WR[0]] + 1) & 0xF
        self._PC += 1

        return 1

    def _dec_r1r0(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] = (self._RAM[self._WR[1] << 4 | self._WR[0]] - 1) & 0xF
        self._PC += 1

        return 1

    def _inc_r3r2(self, opcode):
        self._RAM[self._WR[3] << 4 | self._WR[2]] = (self._RAM[self._WR[3] << 4 | self._WR[2]] + 1) & 0xF
        self._PC += 1

        return 1

    def _dec_r3r2(self, opcode):
        self._RAM[self._WR[3] << 4 | self._WR[2]] = (self._RAM[self._WR[3] << 4 | self._WR[2]] - 1) & 0xF
        self._PC += 1

        return 1

    def _inc_rn(self, opcode):
        WRi = (opcode >> 1) & 0x7
        self._WR[WRi] = (self._WR[WRi] + 1) & 0xF
        self._PC += 1

        return 1
    
    def _dec_rn(self, opcode):
        WRi = (opcode >> 1) & 0x7
        self._WR[WRi] = (self._WR[WRi] - 1) & 0xF
        self._PC += 1

        return 1
    
    def _and_a_r1r0(self, opcode):
        self._ACC &= self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._PC += 1

        return 1
    
    def _xor_a_r1r0(self, opcode):
        self._ACC ^= self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._PC += 1

        return 1
    
    def _or_a_r1r0(self, opcode):
        self._ACC |= self._RAM[self._WR[1] << 4 | self._WR[0]]
        self._PC += 1

        return 1
    
    def _and_r1r0_a(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] &= self._ACC
        self._PC += 1

        return 1
    
    def _xor_r1r0_a(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] ^= self._ACC
        self._PC += 1

        return 1
    
    def _or_r1r0_a(self, opcode):
        self._RAM[self._WR[1] << 4 | self._WR[0]] |= self._ACC
        self._PC += 1

        return 1
    
    def _mov_rn_a(self, opcode):
        self._WR[(opcode >> 1) & 0x7] = self._ACC
        self._PC += 1

        return 1
    
    def _mov_a_rn(self, opcode):
        self._ACC = self._WR[(opcode >> 1) & 0x7]
        self._PC += 1

        return 1

    def _clc(self, opcode):
        self._CF = 0
        self._PC += 1

        return 1

    def _ei(self, opcode):
        self._EI = 1
        self._PC += 1

        return 1

    def _di(self, opcode):
        self._EI = 0
        self._PC += 1

        return 1
        
    def _ret(self, opcode):
        self._PC = self._STACK & 0xFFF
        self._STACK = 0

        return 1

    def _reti(self, opcode):
        self._PC = self._STACK & 0xFFF
        self._CF = (self._STACK >> 12)
        self._STACK = 0

        return 1

    def _stc(self, opcode):
        self._CF = 1
        self._PC += 1

        return 1

    def _out_pa_a(self, opcode):
        self._PA = self._ACC
        self._PC += 1

        return 1

    def _inc_a(self, opcode):
        self._ACC = (self._ACC + 1) & 0xF
        self._PC += 1

        return 1

    def _in_a_pm(self, opcode):
        self._ACC = self._PM
        self._PC += 1

        return 1

    def _in_a_ps(self, opcode):
        self._ACC = self._PS
        self._PC += 1

        return 1

    def _in_a_pp(self, opcode):
        self._ACC = self._PP
        self._PC += 1

        return 1

    def _dummy(self, opcode):
        self._PC += 1

        return 1

    def _daa(self, opcode):
        if (self._ACC > 9 or self._CF):
            self._ACC = (self._ACC + 6) & 0xF
            self._CF = 1
        self._PC += 1

        return 1

    def _halt(self, opcode):
        self._ROM.getByte(self._PC + 1)
        self._PC += 2
        self._HALT = 1
        self._EF = 0

        return 2

    def _timer_on(self, opcode):
        self._TIMERF = 1
        self._PC += 1

        return 1

    def _timer_off(self, opcode):
        self._TIMERF = 0
        self._PC += 1

        return 1

    def _mov_a_tmrl(self, opcode):
        self._ACC = self._TC & 0xF
        self._PC += 1

        return 1

    def _mov_a_tmrh(self, opcode):
        self._ACC = (self._TC >> 4) & 0xF
        self._PC += 1

        return 1

    def _mov_tmrl_a(self, opcode):
        self._TC = (self._TC & 0xF0) | self._ACC
        self._PC += 1

        return 1

    def _mov_tmrh_a(self, opcode):
        self._TC = (self._TC & 0x0F) | (self._ACC << 4)
        self._PC += 1

        return 1

    def _nop(self, opcode):
        self._PC += 1

        return 1

    def _dec_a(self, opcode):
        self._ACC = (self._ACC - 1) & 0xF
        self._PC += 1

        return 1

    def _add_a_x(self, opcode):
        self._ACC += self._ROM.getByte(self._PC + 1) & 0xF
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 2

        return 2

    def _sub_a_x(self, opcode):
        self._ACC += (~self._ROM.getByte(self._PC + 1) & 0xF) + 1
        self._CF = self._ACC > 15
        self._ACC &= 0xF
        self._PC += 2

        return 2

    def _and_a_x(self, opcode):
        self._ACC &= self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 2

    def _xor_a_x(self, opcode):
        self._ACC ^= self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 2

    def _or_a_x(self, opcode):
        self._ACC |= self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 2

    def _sound_n(self, opcode):
        self._sound.setSoundChannel(self._ROM.getByte(self._PC + 1) & 0xF)
        self._PC += 2

        return 2

    def _mov_r4_x(self, opcode):
        self._WR[4] = self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 2

    def _timer_xx(self, opcode):
        self._TC = self._ROM.getByte(self._PC + 1)
        self._PC += 2

        return 2

    def _sound_one(self, opcode):
        self._sound.setOneCycle()
        self._PC += 1

        return 1

    def _sound_loop(self, opcode):
        self._sound.setRepeatCycle()
        self._PC += 1

        return 1

    def _sound_off(self, opcode):
        self._sound.stop()
        self._PC += 1

        return 1

    def _sound_a(self, opcode):
        self._sound.setSoundChannel(self._ACC)
        self._PC += 1

        return 1

    def _read_r4a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte(self._PC & 0xF00 | (self._ACC << 4) | self._RAM[self._WR[1] << 4 | self._WR[0]])
        self._ACC = byte & 0xF
        self._WR[4] = (byte >> 4) & 0xF

        return 2
    
    def _readf_r4a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte(0xF00 | (self._ACC << 4) | self._RAM[self._WR[1] << 4 | self._WR[0]])
        self._ACC = byte & 0xF
        self._WR[4] = (byte >> 4) & 0xF

        return 2

    def _read_mr0a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte(self._PC & 0xF00 | (self._ACC << 4) | self._WR[4])
        self._ACC = byte & 0xF
        self._RAM[self._WR[1] << 4 | self._WR[0]] = (byte >> 4) & 0xF

        return 2

    def _readf_mr0a(self, opcode):
        self._PC += 1
        byte = self._ROM.getByte(0xF00 | (self._ACC << 4) | self._WR[4])
        self._ACC = byte & 0xF
        self._RAM[self._WR[1] << 4 | self._WR[0]] = (byte >> 4) & 0xF

        return 2

    def _mov_r1r0_xx(self, opcode):
        self._WR[0] = opcode & 0xF
        self._WR[1] = self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 2

    def _mov_r3r2_xx(self, opcode):
        self._WR[2] = opcode & 0xF
        self._WR[3] = self._ROM.getByte(self._PC + 1) & 0xF
        self._PC += 2

        return 2

    def _mov_a_x(self, opcode):
        self._ACC = opcode & 0xF
        self._PC += 1

        return 1

    def _jan_address(self, opcode):
        if (self._ACC & (0x1 << ((opcode >> 3) & 0x3))):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 2

    def _jnz_R0_address(self, opcode):
        if (self._WR[0]):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 2

    def _jnz_R1_address(self, opcode):
        if (self._WR[1]):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 2

    def _jz_a_address(self, opcode):
        if (self._ACC == 0):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 2

    def _jnz_a_address(self, opcode):
        if (self._ACC):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 2

    def _jc_address(self, opcode):
        if (self._CF):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 2

    def _jnc_address(self, opcode):
        if (not self._CF):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 2

    def _jtmr_address(self, opcode):
        if (self._TF):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
            self._TF = 0
        else:
            self._PC += 2

        return 2

    def _jnz_R4_address(self, opcode):
        if (self._WR[4]):
            self._PC = (self._PC & 0x800) | ((opcode & 0x7) << 8) | self._ROM.getByte(self._PC + 1)
        else:
            self._PC += 2

        return 2

    def _jmp_address(self, opcode):
        self._PC = ((opcode & 0xF) << 8) | self._ROM.getByte(self._PC + 1)

        return 2

    def _call_address(self, opcode):
        self._STACK = self._PC + 2
        self._PC = ((opcode & 0xF) << 8) | self._ROM.getByte(self._PC + 1)

        return 2
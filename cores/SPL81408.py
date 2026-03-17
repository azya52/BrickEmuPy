from .rom import ROM
from .SPL81408sound import SPL81408sound

SUB_CLOCK = 32768

ADDRESS_SPACE_SIZE = 0x8000

VADDR_NMI = 0x7FFA
VADDR_RESET = 0x7FFC
VADDR_IRQ = 0x7FFE

IO_TIMER_CTRL_ENABLE = 0x80
IO_TIMER_CTRL_COUNTER_MODE = 0x10

IO_PORTCD_DIR_OUTPUT = 0x0F
IO_PORTCD_DIR_PUREINPUT = 0x40

IO_WAKEUP_CTRL_PORTEF = 0x01
IO_WAKEUP_CTRL_TIME_BASEL = 0x02
IO_WAKEUP_CTRL_TIMER0 = 0x04
IO_WAKEUP_CTRL_TIME_BASEH = 0x08

IO_INT_CTRL_EXT = 0x01
IO_INT_CTRL_CLK2K = 0x02
IO_INT_CTRL_CLK128 = 0x04
IO_INT_CTRL_TIME_BASEL = 0x08
IO_INT_CTRL_TIME_BASEH = 0x10
IO_INT_CTRL_TIMER0 = 0x40

IO_TIMEBASE_H_MASK = 0x03
IO_TIMEBASE_H_32 = 0x03
IO_TIMEBASE_H_16 = 0x02
IO_TIMEBASE_H_8 = 0x01
IO_TIMEBASE_H_4 = 0x00
IO_TIMEBASE_L_1 = 0x80

IO_LCD_CTRL_STATE = 0x0C
IO_LCD_CTRL_ALL_ON = 0x04
IO_LCD_CTRL_ALL_OFF = 0x08

class SPL81408():
    SFR_OFFSET = 0x0
    SFR_SIZE = 0x20
    CPU_RAM_OFFSET = 0x60
    CPURAM_SIZE = 0xA0
    LCDRAM_OFFSET = 0x20
    LCDRAM_SIZE = 0x1D

    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])

        self._cycle_counter = 0
        self._instr_counter = 0

        self._pullup_ext = {
            **{"CD": 0, "EF": 0, "AB": 0},
            **mask['port_pullup']
        }

        self._port_input = {
            "CD": [0, 0],
            "EF": [0, 0],
            "AB": [0, 0]
        }

        self._clock = clock
        self._sub_clock_div = clock / SUB_CLOCK

        self._sound = SPL81408sound(clock)
        
        self.reset()

        self._io_tbl = {
            0x00: (SPL81408._get_io_portCD_dir, SPL81408._set_io_portCD_dir),
            0x01: (SPL81408._get_io_audio_ch0_data, SPL81408._set_io_audio_ch0_data),
            0x03: (SPL81408._get_io_dummy, SPL81408._set_io_dummy), #to-do AB data
            0x04: (SPL81408._get_io_portCD_data, SPL81408._set_io_portCD_data),
            0x05: (SPL81408._get_io_portEF_data, SPL81408._set_io_portEF_data),
            0x06: (SPL81408._get_io_portEF_dir, SPL81408._set_io_portEF_dir),
            0x07: (SPL81408._get_io_Bank_Select, SPL81408._set_io_Bank_Select),
            0x08: (SPL81408._get_io_wakeup_ctrl, SPL81408._set_io_wakeup_ctrl),
            0x09: (SPL81408._get_io_System_Ctrl, SPL81408._set_io_System_Ctrl),
            0x0A: (SPL81408._get_io_time_base_sel, SPL81408._set_io_time_base_sel),
            0x0B: (SPL81408._get_io_timer_ctrl, SPL81408._set_io_timer_ctrl),
            0x0C: (SPL81408._get_io_clk_32768_en, SPL81408._set_io_clk_32768_en),
            0x0D: (SPL81408._get_io_int_ctrl, SPL81408._set_io_int_ctrl),
            0x0E: (SPL81408._get_io_cpu_ctrl, SPL81408._set_io_cpu_ctrl),
            0x0F: (SPL81408._get_io_dummy, SPL81408._set_io_dummy), #to-do WD
            0x10: (SPL81408._get_io_timer_TM0L, SPL81408._set_io_timer_TM0L),
            0x11: (SPL81408._get_io_timer_TM0H, SPL81408._set_io_timer_TM0H),
            0x12: (SPL81408._get_io_dummy, SPL81408._set_io_timer_TM0_load),
            0x18: (SPL81408._get_io_LCD_ctrl, SPL81408._set_io_LCD_ctrl), #to-do LCD ctrl
            0x19: (SPL81408._get_io_dummy, SPL81408._set_io_dummy), #to-do EF attr
            0x1A: (SPL81408._get_io_dummy, SPL81408._set_io_int_flag_clear),
            0x1B: (SPL81408._get_io_audio_ch0_ctrl, SPL81408._set_io_audio_ch0_ctrl),
            0x1E: (SPL81408._get_io_dummy, SPL81408._set_io_dummy), #to-do AB dir
            0x1F: (SPL81408._get_io_dummy, SPL81408._set_io_dummy), #to-do AB attr
        }

        self._execute = (
            (SPL81408._brk),
            (SPL81408._dummy),
            (SPL81408._rti),
            *([(SPL81408._dummy)] * 2),
            (SPL81408._ora_zp),
            (SPL81408._dummy),
            (SPL81408._eor_zp),
            (SPL81408._bpl),
            (SPL81408._dummy),
            (SPL81408._bvc),
            (SPL81408._dummy),
            *([(SPL81408._dummy)] * 3),
            (SPL81408._eor_zp_x),
            (SPL81408._jsr_abs),
            (SPL81408._bit_zp),
            (SPL81408._rts),
            *([(SPL81408._dummy)] * 2),
            (SPL81408._and_zp),
            (SPL81408._dummy),
            (SPL81408._adc_zp),
            (SPL81408._bmi),
            (SPL81408._dummy),
            (SPL81408._bvs),
            *([(SPL81408._dummy)] * 9),
            (SPL81408._sta_ind_x),
            (SPL81408._sta_zp),
            (SPL81408._dummy),
            (SPL81408._cmp_zp),
            (SPL81408._bcc),
            (SPL81408._dummy),
            (SPL81408._bne),
            *([(SPL81408._dummy)] * 2),
            (SPL81408._sta_zp_x),
            (SPL81408._dummy),
            (SPL81408._cmp_zp_x),
            *([(SPL81408._dummy)] * 2),
            (SPL81408._cpx_imm),
            (SPL81408._cpx_zp),
            (SPL81408._lda_ind_x),
            (SPL81408._lda_zp),
            (SPL81408._dummy),
            (SPL81408._sbc_zp),
            (SPL81408._bcs),
            (SPL81408._dummy),
            (SPL81408._beq),
            *([(SPL81408._dummy)] * 2),
            (SPL81408._lda_zp_x),
            *([(SPL81408._dummy)] * 2),
            (SPL81408._php),
            (SPL81408._dummy),
            (SPL81408._pha),
            (SPL81408._jmp_abs),
            (SPL81408._ora_imm),
            (SPL81408._dummy),
            (SPL81408._eor_imm),
            (SPL81408._dummy),
            (SPL81408._clc),
            (SPL81408._dummy),
            (SPL81408._cli),
            *([(SPL81408._dummy)] * 5),
            (SPL81408._plp),
            (SPL81408._bit_abs),
            (SPL81408._pla),
            (SPL81408._jmp_ind),
            (SPL81408._and_imm),
            (SPL81408._dummy),
            (SPL81408._adc_imm),
            (SPL81408._dummy),
            (SPL81408._sec),
            (SPL81408._dummy),
            (SPL81408._sei),
            *([(SPL81408._dummy)] * 11),
            (SPL81408._cmp_imm),
            *([(SPL81408._dummy)] * 11),
            (SPL81408._inx),
            (SPL81408._dummy),
            (SPL81408._lda_imm),
            (SPL81408._lda_abs),
            (SPL81408._sbc_imm),
            (SPL81408._dummy),
            (SPL81408._clv),
            (SPL81408._dummy),
            (SPL81408._sed),
            *([(SPL81408._dummy)] * 2),
            (SPL81408._lda_abs_x),
            *([(SPL81408._dummy)] * 19),                        
            (SPL81408._rol_zp),
            (SPL81408._dummy),
            (SPL81408._ror_zp),
            *([(SPL81408._dummy)] * 13),   
            (SPL81408._stx_zp),
            (SPL81408._dummy),
            (SPL81408._dec_zp),
            *([(SPL81408._dummy)] * 7),  
            (SPL81408._dec_zp_x),
            *([(SPL81408._dummy)] * 4), 
            (SPL81408._ldx_imm),
            (SPL81408._ldx_zp),
            (SPL81408._dummy),
            (SPL81408._inc_zp),
            *([(SPL81408._dummy)] * 28),           
            (SPL81408._rol_a),
            (SPL81408._dummy),
            (SPL81408._ror_a),
            *([(SPL81408._dummy)] * 13),   
            (SPL81408._txa),
            (SPL81408._stx_abs),
            (SPL81408._dex),
            *([(SPL81408._dummy)] * 5),
            (SPL81408._txs),
            *([(SPL81408._dummy)] * 7),
            (SPL81408._tax),
            (SPL81408._ldx_abs),
            (SPL81408._nop),
            *([(SPL81408._dummy)] * 5),
            (SPL81408._tsx),
            *([(SPL81408._dummy)] * 7)
        )

    def examine(self):
        return {
            "PC": self._PC,
            "A": self._A,
            "X": self._X,
            "SP": self._SP,
            "NF": self._NF,
            "VF": self._VF,
            "DF": self._DF,
            "BF": self._BF,
            "IF": self._IF,
            "ZF": self._ZF,
            "CF": self._CF,
            "RAM": self._RAM,
            "LCDRAM": self._LCDRAM,
            "IORAM": (
                self._PDIR["CD"],
                self._AUDIO_CH0_DATA,
                self._port_read("AB"),
                self._port_read("CD"),
                self._port_read("EF"),
                self._PDIR["EF"],
                self._ROM_BANK,
                self._WAKEUP_CTRL,
                self._SYS_CTRL,
                self._TIME_BASE,
                self._TIMER_CTRL,
                self._CLK32768_DISABLE,
                self._INT_CTRL,
                self._CPU_CTRL,
                0,
                int(self._TM0) & 0xFF,
                int(self._TM0) >> 8,
                0,
                self._LCD_CTRL,
                0,
                0,
                self._AUDIO_CH0_CTRL,
                self._PDIR["AB"],
                0
            )
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] % ADDRESS_SPACE_SIZE
        if ("A" in state):
            self._A = state["A"] & 0xFF
        if ("X" in state):
            self._X = state["X"] & 0xFF
        if ("SP" in state):
            self._SP = state["SP"] & 0xFF
        if ("NF" in state):
            self._NF = state["NF"]
        if ("VF" in state):
            self._VF = state["VF"]
        if ("BF" in state):
            self._BF = state["BF"]
        if ("DF" in state):
            self._DF = state["DF"]
        if ("IF" in state):
            self._IF = state["IF"]
        if ("ZF" in state):
            self._ZF = state["ZF"]
        if ("CF" in state):
            self._CF = state["CF"]
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xFF
        if ("LCDRAM" in state):
            for i, value in state["LCDRAM"].items():
                if (i < self.LCDRAM_SIZE):
                    self._LCDRAM[i] = value & 0xFF
        if ("IORAM" in state):
            for i, value in state["IORAM"].items():
                if i < len(self._io_tbl):
                    list(self._io_tbl.values())[i][1](self, value & 0xFF)

    def reset(self):
        self._T2KHZ_counter = 0
        self._T2KHZ = 0
        self._TM0 = 0
        self._TM0_RELOAD = 0

        self._PC = 0
        self._SP = 0

        self._A = 0
        self._X = 0
        
        self._set_ps(0x04)

        self._CPU_ENBL = 1

        self._RAM = [0] * self.CPURAM_SIZE
        self._LCDRAM = [0] * self.LCDRAM_SIZE

        self._ROM_BANK = 0

        self._WAKEUP_CTRL = 0
        self._WAKEUPREQ = 0
        self._TIME_BASE = 0
        self._TIMER_CTRL = 0
        self._CPU_CTRL = 0
        self._CPU_DIV = 2
        self._CLK32768_DISABLE = 0
        self._CLK32768_ENABLE = True

        self._PDIR = {
            "CD": 0,
            "EF": 0,
            "AB": 0
        }

        self._PDIR = {
            "CD": 0,
            "EF": 0,
            "AB": 0
        }

        self._PLATCH = {
            "CD": 0,
            "EF": 0,
            "AB": 0
        }

        self._IO_CTRL = 0
        self._INT_CTRL = 0
        self._IREQ = 0
        self._SYS_CTRL = 0
        self._LCD_CTRL = 0
        self._AUDIO_CH0_CTRL = 0
        self._AUDIO_CH0_DATA = 0

        self._go_vector(VADDR_RESET)
        
    def _go_vector(self, addr):
        self._PC = self._ROM.getWordLSB(addr)

    def pc(self):
        return self._PC
    
    def get_VRAM(self):
        if (self._CPU_ENBL or self._CLK32768_ENABLE):
            if ((self._LCD_CTRL & IO_LCD_CTRL_STATE) == 0):
                return tuple(self._LCDRAM)
            elif ((self._LCD_CTRL & IO_LCD_CTRL_ALL_OFF) == 0):
                return tuple([0xFF] * self.LCDRAM_SIZE)
        return tuple([0x00] * self.LCDRAM_SIZE)

    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter

    def pin_set(self, port, pin, level):
        self._process_port_input(port, pin, level)

    def pin_release(self, port, pin):
        self._process_port_input(port, pin, -1)

    def _port_read(self, port):
        return (
            (self._PDIR[port] & self._PLATCH[port]) | 
            (~self._PDIR[port] & (~self._port_input[port][0] & 
            (self._port_input[port][1] | self._pullup_ext[port])))
        )

    def _process_port_input(self, port, pin, level):
        if (port == 'RES'):
            if (level == 0):
                self.reset()
        else:
            prev_port = self._port_read(port)
            self._port_input[port][0] &= ~pin
            self._port_input[port][1] &= ~pin
            if (level >= 0):
                self._port_input[port][level] |= pin
            
            if ((port == "CD") and (pin & 0x2)):
                if ((prev_port & 0x2) > (self._port_read(port) & 0x2)):
                    self._IREQ |= IO_INT_CTRL_EXT
            if (port == "EF"):
                if (prev_port != self._port_read(port)):
                    self._IREQ |= IO_INT_CTRL_EXT
                    if (not self._CPU_ENBL):
                        self._WAKEUPREQ |= IO_WAKEUP_CTRL_PORTEF
                        self._CPU_ENBL |= self._WAKEUP_CTRL & IO_WAKEUP_CTRL_PORTEF

    def _IRQ(self):
        if (not self._IF):
            self._write_mem(self._SP, self._PC >> 8)
            self._SP = (self._SP - 1) & 0xFF
            self._write_mem(self._SP, self._PC & 0xFF)
            self._SP = (self._SP - 1) & 0xFF
            self._write_mem(self._SP, self._ps())
            self._SP = (self._SP - 1) & 0xFF
            self._IF = 1
            self._go_vector(VADDR_IRQ)

    def _NMI(self):
        if (self._CPU_ENBL):
            self._write_mem(self._SP, self._PC >> 8)
            self._SP = (self._SP - 1) & 0xFF
            self._write_mem(self._SP, self._PC & 0xFF)
            self._SP = (self._SP - 1) & 0xFF
            self._write_mem(self._SP, self._ps())
            self._SP = (self._SP - 1) & 0xFF
            self._go_vector(VADDR_NMI)

    def _timers_clock(self, exec_cycles):
        if (not self._TIMER_CTRL & IO_TIMER_CTRL_COUNTER_MODE):
            if (self._TIMER_CTRL & IO_TIMER_CTRL_ENABLE):
                self._TM0 += exec_cycles
                while (self._TM0 > 0xFFFF):
                    self._TM0 -= 0x10000 - self._TM0_RELOAD
                    self._IREQ |= IO_INT_CTRL_TIMER0
                    if (not self._CPU_ENBL):
                        self._WAKEUPREQ |= IO_WAKEUP_CTRL_TIMER0
                        self._CPU_ENBL |= self._WAKEUP_CTRL & IO_WAKEUP_CTRL_TIMER0
                    if (self._AUDIO_CH0_CTRL == 0xC0):
                        self._sound.toggle(self._cycle_counter)

        self._T2KHZ_counter -= exec_cycles
        while (self._T2KHZ_counter <= 0):
            self._T2KHZ_counter += self._sub_clock_div * (SUB_CLOCK // 2048)
            self._T2KHZ += 1
            self._IREQ |= IO_INT_CTRL_CLK2K

            if (self._T2KHZ % (2048 // 128) == 0):
                self._IREQ |= IO_INT_CTRL_CLK128

                if (self._T2KHZ % (2048 >> ((self._TIME_BASE & IO_TIMEBASE_H_MASK) + 2)) == 0):
                    self._IREQ |= IO_INT_CTRL_TIME_BASEH
                    if (not self._CPU_ENBL):
                        self._WAKEUPREQ |= IO_WAKEUP_CTRL_TIME_BASEH
                        self._CPU_ENBL |= self._WAKEUP_CTRL & IO_WAKEUP_CTRL_TIME_BASEH

                    if (self._T2KHZ % (2048 >> ((self._TIME_BASE & IO_TIMEBASE_L_1) == 0)) == 0):
                        self._IREQ |= IO_INT_CTRL_TIME_BASEL
                        if (not self._CPU_ENBL):
                            self._WAKEUPREQ |= IO_WAKEUP_CTRL_TIME_BASEL
                            self._CPU_ENBL |= self._WAKEUP_CTRL & IO_WAKEUP_CTRL_TIME_BASEL

    def _interrupt_process(self):
        if (self._IREQ & self._INT_CTRL):
            for i in range(8):
                if (self._IREQ & self._INT_CTRL & (1 << i)):
                    return self._IRQ()
                
    def clock(self):
        if (self._CPU_ENBL):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            exec_cycles = self._execute[opcode](self) * self._CPU_DIV
            self._instr_counter += 1
            self._timers_clock(exec_cycles)
            if (not self._IF):
                self._interrupt_process()
        elif (self._CLK32768_ENABLE):
            exec_cycles = self._sub_clock_div
            self._timers_clock(exec_cycles)
        else:
            exec_cycles = self._sub_clock_div

        self._cycle_counter += exec_cycles
        return exec_cycles

    def _get_io_portCD_dir(self):
        return self._PDIR["CD"]
    
    def _set_io_portCD_dir(self, value):
        self._PDIR["CD"] = value & IO_PORTCD_DIR_OUTPUT

    def _get_io_portCD_data(self):
        return self._port_read("CD")
    
    def _set_io_portCD_data(self, value):
        self._PLATCH["CD"] = value

    def _get_io_portEF_dir(self):
        return self._PDIR["EF"]
    
    def _set_io_portEF_dir(self, value):
        self._PDIR["EF"] = value

    def _get_io_portEF_data(self):
        return self._port_read("EF")
    
    def _set_io_portEF_data(self, value):
        self._PLATCH["EF"] = value

    def _get_io_System_Ctrl(self):
        return self._SYS_CTRL
    
    def _set_io_System_Ctrl(self, value):
        self._CPU_ENBL = 0
        self._SYS_CTRL = value

    def _get_io_audio_ch0_ctrl(self):
        return self._AUDIO_CH0_CTRL

    def _set_io_audio_ch0_ctrl(self, value):
        self._AUDIO_CH0_CTRL = value

    def _get_io_audio_ch0_data(self):
        return 0

    def _set_io_audio_ch0_data(self, value):
        self._AUDIO_CH0_DATA = value
        self._sound.set_data(self._AUDIO_CH0_CTRL, value, self._cycle_counter)
        
    def _get_io_Bank_Select(self):
        return self._ROM_BANK
    
    def _set_io_Bank_Select(self, value):
        self._ROM_BANK = value

    def _get_io_wakeup_ctrl(self):
        return self._WAKEUPREQ
    
    def _set_io_wakeup_ctrl(self, value):
        self._WAKEUP_CTRL = value
        self._WAKEUPREQ = 0

    def _get_io_time_base_sel(self):
        return self._T2KHZ
    
    def _set_io_time_base_sel(self, value):
        self._TIME_BASE = value

    def _get_io_timer_ctrl(self):
        return self._TIMER_CTRL
    
    def _set_io_timer_ctrl(self, value):
        self._TIMER_CTRL = value

    def _get_io_clk_32768_en(self):
        return self._CLK32768_DISABLE
    
    def _set_io_clk_32768_en(self, value):
        self._CLK32768_DISABLE = value
        self._CLK32768_ENABLE = self._CLK32768_DISABLE == 0

    def _get_io_int_ctrl(self):
        return self._IREQ
    
    def _set_io_int_ctrl(self, value):
        self._INT_CTRL = value
        self._IREQ = 0

    def _get_io_cpu_ctrl(self):
        return self._CPU_CTRL
    
    def _set_io_cpu_ctrl(self, value):
        self._CPU_CTRL = value
        self._CPU_DIV = 2 << value

    def _set_io_int_flag_clear(self, value):
        self._IREQ = 0

    def _get_io_timer_TM0L(self):
        return int(self._TM0) & 0xFF

    def _set_io_timer_TM0L(self, value):
        self._TM0_RELOAD = (self._TM0_RELOAD & 0xFF00) | value

    def _get_io_timer_TM0H(self):
        return int(self._TM0) >> 8

    def _set_io_timer_TM0H(self, value):
        self._TM0_RELOAD = (self._TM0_RELOAD & 0xFF) | (value << 8)

    def _set_io_timer_TM0_load(self, value):
        self._TM0 = self._TM0_RELOAD

    def _get_io_LCD_ctrl(self):
        return self._LCD_CTRL
    
    def _set_io_LCD_ctrl(self, value):
        self._LCD_CTRL = value

    def _get_io_dummy(self):
        return 0
    
    def _set_io_dummy(self, value):
        pass
    
    def _write_mem(self, addr, value):
        if ((addr >= self.LCDRAM_OFFSET) and (addr < self.LCDRAM_SIZE + self.LCDRAM_OFFSET)):
            self._LCDRAM[addr - self.LCDRAM_OFFSET] = value
        elif ((addr >= self.CPU_RAM_OFFSET) and (addr < self.CPURAM_SIZE + self.CPU_RAM_OFFSET)):
            self._RAM[addr - self.CPU_RAM_OFFSET] = value
        else:
            io = self._io_tbl.get(addr)
            if (io != None):
                io[1](self, value)

    def _read_mem(self, addr):
        if ((addr >= self.LCDRAM_OFFSET) and (addr < self.LCDRAM_SIZE + self.LCDRAM_OFFSET)):
            return self._LCDRAM[addr - self.LCDRAM_OFFSET]
        elif ((addr >= self.CPU_RAM_OFFSET) and (addr < self.CPURAM_SIZE + self.CPU_RAM_OFFSET)):
            return self._RAM[addr - self.CPU_RAM_OFFSET]
        elif ((addr >= self.SFR_OFFSET) and (addr < self.SFR_SIZE + self.SFR_OFFSET)):
            io = self._io_tbl.get(addr)
            if (io != None):
                return io[0](self)
            return 0
        else:
            #to-do
            if (self._ROM_BANK):
                return self._ROM.getByte(addr)
            addr = (addr & 0x7FFF)
            return self._ROM.getByte(addr)
    
    def _ps(self):
        return (
            (self._NF << 7) |
            (self._VF << 6) |
            (self._BF << 4) |
            (self._DF << 3) |
            (self._IF << 2) |
            (self._ZF << 1) |
            (self._CF)
        )

    def _set_ps(self, ps):
        self._NF = (ps >> 7)
        self._VF = (ps & 0x40 > 0)
        self._BF = (ps & 0x10 > 0)
        self._DF = (ps & 0x08 > 0)
        self._IF = (ps & 0x04 > 0)
        self._ZF = (ps & 0x02 > 0)
        self._CF = ps & 0x1

    def _adc(self, operand):
        A = self._A
        new_value = A + operand + self._CF

        if ((self._DF) and ((A & 0x0F) + (operand & 0x0F) + self._CF > 9)):
            new_value += 6

        self._VF = (~(A ^ operand) & (A ^ new_value)) >> 7
        self._NF = (new_value >> 7) & 0x1

        if ((self._DF) and (new_value > 0x99)):
            new_value += 0x60

        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 255

        self._A = new_value & 0xFF

    def _sbc(self, operand):
        A = self._A
        new_value = A - operand - (not self._CF)

        if (self._DF):
            if ((A & 0x0F) - (operand & 0x0F) - (not self._CF) < 0):
                new_value -= 6
            if (new_value < 0):
                new_value -= 0x60

        self._VF = ((A ^ operand) & (A ^ new_value)) >> 7
        self._NF = (new_value >> 7) & 0x1
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >= 0

        self._A = new_value & 0xFF

    def _brk(self):
        self._BF = 1
        self._PC = (self._PC + 1) & 0xFFFF
        self._IRQ()
        return 7

    def _ora_zp(self):
        self._A |= self._read_mem(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _php(self):
        self._write_mem(self._SP, self._ps())
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _ora_imm(self):
        self._A |= self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _bpl(self):
        if (not self._NF):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            prev_PC = self._PC
            self._PC = (self._PC + opcode - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _clc(self):
        self._CF = 0
        return 2

    def _jsr_abs(self):
        pc = (self._PC + 1) & 0xFFFF
        self._write_mem(self._SP, pc >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, pc & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._PC = self._ROM.getWordLSB(self._PC)
        return 6

    def _bit_zp(self):
        m = self._read_mem(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 3

    def _and_zp(self):
        self._A &= self._read_mem(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _rol_zp(self):
        opcode = self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        new_value = (self._read_mem(opcode) << 1) | self._CF
        self._write_mem(opcode, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 5

    def _plp(self):
        self._SP = (self._SP + 1) & 0xFF
        self._set_ps(self._read_mem(self._SP))
        return 4

    def _and_imm(self):
        self._A &= self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _rol_a(self):
        new_value = (self._A << 1) | self._CF
        self._A = new_value & 0xFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 2

    def _bit_abs(self):
        m = self._read_mem(self._ROM.getWordLSB(self._PC))
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 4

    def _bmi(self):
        if (self._NF):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            prev_PC = self._PC
            self._PC = (self._PC + opcode - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _sec(self):
        self._CF = 1
        return 2

    def _rti(self):
        self._SP = (self._SP + 1) & 0xFF
        self._set_ps(self._read_mem(self._SP))
        self._SP = (self._SP + 1) & 0xFF
        self._PC = self._read_mem(self._SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SP) << 8
        return 6

    def _eor_zp(self):
        self._A ^= self._read_mem(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _pha(self):
        self._write_mem(self._SP, self._A)
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _eor_imm(self):
        self._A ^= self._ROM.getByte(self._PC) & 0xFF
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _jmp_abs(self):
        self._PC = self._ROM.getWordLSB(self._PC)
        return 3

    def _bvc(self):
        if (not self._VF):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            prev_PC = self._PC
            self._PC = (self._PC + opcode - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _eor_zp_x(self):
        self._A ^= self._read_mem((self._ROM.getByte(self._PC) + self._X) & 0xFF)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _cli(self):
        self._IF = 0
        return 2

    def _rts(self):
        self._SP = (self._SP + 1) & 0xFF
        self._PC = self._read_mem(self._SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SP) << 8
        self._PC += 1
        return 6

    def _adc_zp(self):
        self._adc(self._read_mem(self._ROM.getByte(self._PC)))
        self._PC = (self._PC + 1) & 0xFFFF
        return 3

    def _ror_zp(self):
        opcode = self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        prev_value = self._read_mem(opcode)
        self._write_mem(opcode, (prev_value >> 1) | (self._CF << 7))
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 5

    def _pla(self):
        self._SP = (self._SP + 1) & 0xFF
        self._A = self._read_mem(self._SP)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _adc_imm(self):
        self._adc(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _ror_a(self):
        prev_value = self._A
        self._A = (prev_value >> 1) | (self._CF << 7)
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 2

    def _jmp_ind(self):
        addr = self._ROM.getWordLSB(self._PC)
        self._PC = self._read_mem(addr)
        self._PC |= self._read_mem((addr + 1) & 0xFFFF) << 8
        return 6

    def _bvs(self):
        if (self._VF):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            prev_PC = self._PC
            self._PC = (self._PC + opcode - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _sei(self):
        self._IF = 1
        return 2

    def _sta_ind_x(self):
        opcode = self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
    
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        self._write_mem(addr, self._A)
        return 6

    def _sta_zp(self):
        self._write_mem(self._ROM.getByte(self._PC), self._A)
        self._PC = (self._PC + 1) & 0xFFFF
        return 3

    def _stx_zp(self):
        self._write_mem(self._ROM.getByte(self._PC), self._X)
        self._PC = (self._PC + 1) & 0xFFFF
        return 3

    def _txa(self):
        self._A = self._X
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _stx_abs(self):
        self._write_mem(self._ROM.getWordLSB(self._PC), self._X)
        self._PC = (self._PC + 2) & 0xFFFF
        return 4

    def _bcc(self):
        if (not self._CF):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            prev_PC = self._PC
            self._PC = (self._PC + opcode - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _sta_zp_x(self):
        self._write_mem((self._ROM.getByte(self._PC) + self._X) & 0xFF, self._A)
        self._PC = (self._PC + 1) & 0xFFFF
        return 4

    def _txs(self):
        self._SP = self._X
        return 2

    def _lda_ind_x(self):
        value = self._ROM.getByte(self._PC) + self._X
        self._PC = (self._PC + 1) & 0xFFFF
        self._A = self._read_mem(self._read_mem(value & 0xFF) | (self._read_mem((value + 1) & 0xFF) << 8))
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 6

    def _ldx_imm(self):
        self._X = self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _lda_zp(self):
        self._A = self._read_mem(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _ldx_zp(self):
        self._X = self._read_mem(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 3

    def _lda_imm(self):
        self._A = self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _tax(self):
        self._X = self._A
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _lda_abs(self):
        self._A = self._read_mem(self._ROM.getWordLSB(self._PC))
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _ldx_abs(self):
        self._X = self._read_mem(self._ROM.getWordLSB(self._PC))
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 4

    def _bcs(self):
        if (self._CF):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            prev_PC = self._PC
            self._PC = (self._PC + opcode - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _lda_zp_x(self):
        self._A = self._read_mem((self._ROM.getByte(self._PC) + self._X) & 0xFF)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _clv(self):
        self._VF = 0
        return 2

    def _tsx(self):
        self._X = self._SP
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _lda_abs_x(self):   
        base = self._ROM.getWordLSB(self._PC)
        self._PC = (self._PC + 2) & 0xFFFF
        addr = (base + self._X) & 0xFFFF
        self._A = self._read_mem(addr)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((base ^ addr) > 255)
    

    def _cmp_zp(self):
        test_value = self._A - self._read_mem(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3

    def _dec_zp(self):
        opcode = self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        new_value = (self._read_mem(opcode) - 1) & 0xFF
        self._write_mem(opcode, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _cmp_imm(self):
        test_value = self._A - (self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _dex(self):
        self._X = (self._X - 1) & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _bne(self):
        if (not self._ZF):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            prev_PC = self._PC
            self._PC = (self._PC + opcode - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _cmp_zp_x(self):
        test_value = self._A - self._read_mem((self._ROM.getByte(self._PC) + self._X) & 0xFF)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4

    def _dec_zp_x(self):
        addr = (self._ROM.getByte(self._PC) + self._X) & 0xFF
        self._PC = (self._PC + 1) & 0xFFFF
        new_value = (self._read_mem(addr) - 1) & 0xFF
        self._write_mem(addr, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _cpx_imm(self):
        test_value = self._X - self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _cpx_zp(self):
        test_value = self._X - self._read_mem(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3

    def _sbc_zp(self):
        self._sbc(self._read_mem(self._ROM.getByte(self._PC)))
        self._PC = (self._PC + 1) & 0xFFFF
        return 3

    def _inc_zp(self):
        opcode = self._ROM.getByte(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        new_value = (self._read_mem(opcode) + 1) & 0xFF
        self._write_mem(opcode, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _inx(self):
        self._X = (self._X + 1) & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _sbc_imm(self):
        self._sbc(self._ROM.getByte(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _nop(self):
        return 2

    def _beq(self):
        if (self._ZF):
            opcode = self._ROM.getByte(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            prev_PC = self._PC
            self._PC = (self._PC + opcode - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _sed(self):
        self._DF = 1
        return 2
    
    def _dummy(self):
        print("illegal instruction %0.4X" % (self._PC))
        return 2
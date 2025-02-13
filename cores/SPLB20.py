from .rom import ROM
from .SPLB20Sound import SPLB20sound

SUB_CLOCK = 32768
MCLOCK_DIV = 1

ADDRESS_SPACE_SIZE = 0x10000

SFR_OFFSET = 0x40
SFR_SIZE = 0x40
CPU_RAM_OFFSET = 0x80
CPURAM_SIZE = 0x80
DATARAM_OFFSET = 0x1000
DATARAM_SIZE = 0x800
LCDRAM_OFFSET = 0x00
LCDRAM_SIZE = 0x40

VADDR_NMI = 0xFFFA
VADDR_RESET = 0xFFFC
VADDR_IRQ = 0xFFFE

IO_INT_CFG_T2HZ_INT = 0x01
IO_INT_CFG_T128HZ_INT = 0x02
IO_INT_CFG_POWERKEY_INT = 0x04
IO_INT_CFG_NORMALKEY_INT = 0x08
IO_INT_CFG_COUNTER_INT = 0x10
IO_INT_CFG_NMI_ENBL = 0x80

IO_SYS_CTRL_STATUS = 0x03
IO_SYS_CTRL_LCD_ENBL = 0x04
IO_SYS_CTRL_LCD_ON = 0x08
IO_SYS_CTRL_TIMER_ENBL = 0x10
IO_SYS_CTRL_32K_ENBL = 0x20
IO_SYS_CTRL_CPU_STOP = 0x40
IO_SYS_CTRL_ROSC_STOP = 0x80

class SPLB20():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])
        self._sound = SPLB20sound(clock)

        self._rom_offset = ADDRESS_SPACE_SIZE - self._ROM.size()

        self._cycle_counter = 0

        self._pullup_ext = {
            **{"PA": 0xFF}
        }

        self._port_input = {
            "PA": [0, 0]
        }
    
        self._instr_counter = 0
        self._timer_counter = 0
        self._T2HZ_counter = 0
        self._T128HZ_counter = 0

        self._non_crystal_mode = mask['non_crystal_mode']

        self._sub_clock_div = clock / SUB_CLOCK

        self._clock = clock

        if (not self._non_crystal_mode):
            self._sound.set_clock_div(self._sub_clock_div, self._cycle_counter)

        self.reset()

        self._io_tbl = {
            0x70: (SPLB20._get_io_LCD_Configure, SPLB20._set_io_LCD_Configure),
            0x71: (SPLB20._get_io_PortA_IOConfigure, SPLB20._set_io_PortA_IOConfigure),
            0x72: (SPLB20._get_io_PortA_Output, SPLB20._set_io_PortA_Output),
            0x73: (SPLB20._get_io_PortA_Data, SPLB20._set_PortA_Data),
            0x74: (SPLB20._get_io_PortXY_Data, SPLB20._set_PortXY_Data),
            0x75: (SPLB20._get_io_PortZ_Data, SPLB20._set_PortZ_Data),
            0x76: (SPLB20._get_io_LCD_Bias, SPLB20._set_io_LCD_Bias),
            0x77: (SPLB20._get_io_KeyScan_OutputL, SPLB20._set_io_KeyScan_OutputL),
            0x78: (SPLB20._get_io_KeyScan_OutputH, SPLB20._set_io_KeyScan_OutputH),
            0x79: (SPLB20._get_io_Interrupt_Config, SPLB20._set_io_Interrupt_Config),
            0x7A: (SPLB20._get_io_System_Ctrl, SPLB20._set_io_System_Ctrl),
            0x7B: (SPLB20._get_io_DownCounter_PresetValue, SPLB20._set_io_DownCounter_PresetValue),
            0x7C: (SPLB20._get_io_Prescalar_Ctrl, SPLB20._set_io_Prescalar_Ctrl),
            0x7E: (SPLB20._get_io_KeyScan_Ctrl, SPLB20._set_io_KeyScan_Ctrl),
            0x7F: (SPLB20._get_io_Watchdog_Clear, SPLB20._set_io_Watchdog_Clear),
        }

        self._execute = (
            (SPLB20._brk, 1),
            *([(SPLB20._dummy, 1)] * 4),
            (SPLB20._ora_zp, 2),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._php, 1),
            (SPLB20._ora_imm, 2),
            *([(SPLB20._dummy, 1)] * 6),
            (SPLB20._bpl, 2),
            *([(SPLB20._dummy, 1)] * 7),
            (SPLB20._clc, 1),
            *([(SPLB20._dummy, 1)] * 7),
            (SPLB20._jsr_abs, 3),
            *([(SPLB20._dummy, 1)] * 3),
            (SPLB20._bit_zp, 2),
            (SPLB20._and_zp, 2),
            (SPLB20._rol_zp, 2),
            (SPLB20._dummy, 1),
            (SPLB20._plp, 1),
            (SPLB20._and_imm, 2),
            (SPLB20._rol_a, 1),
            (SPLB20._dummy, 1),
            (SPLB20._bit_abs, 3),
            *([(SPLB20._dummy, 1)] * 3),
            (SPLB20._bmi, 2),
            *([(SPLB20._dummy, 1)] * 7),
            (SPLB20._sec, 1),
            *([(SPLB20._dummy, 1)] * 7),
            (SPLB20._rti, 1),
            *([(SPLB20._dummy, 1)] * 4),
            (SPLB20._eor_zp, 2),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._pha, 1),
            (SPLB20._eor_imm, 2),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._jmp_abs, 3),
            *([(SPLB20._dummy, 1)] * 3),
            (SPLB20._bvc, 2),
            *([(SPLB20._dummy, 1)] * 4),
            (SPLB20._eor_zp_x, 2),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._cli, 1),
            *([(SPLB20._dummy, 1)] * 7),
            (SPLB20._rts, 1),
            *([(SPLB20._dummy, 1)] * 4),
            (SPLB20._adc_zp, 2),
            (SPLB20._ror_zp, 2),
            (SPLB20._dummy, 1),
            (SPLB20._pla, 1),
            (SPLB20._adc_imm, 2),
            (SPLB20._ror_a, 1),
            (SPLB20._dummy, 1),
            (SPLB20._jmp_ind, 3),
            *([(SPLB20._dummy, 1)] * 3),
            (SPLB20._bvs, 2),
            *([(SPLB20._dummy, 1)] * 7),
            (SPLB20._sei, 1),
            *([(SPLB20._dummy, 1)] * 8),
            (SPLB20._sta_ind_x, 2),
            *([(SPLB20._dummy, 1)] * 3),
            (SPLB20._sta_zp, 2),
            (SPLB20._stx_zp, 2),
            *([(SPLB20._dummy, 1)] * 3),
            (SPLB20._txa, 1),
            *([(SPLB20._dummy, 1)] * 3),
            (SPLB20._stx_abs, 3),
            (SPLB20._dummy, 1),
            (SPLB20._bcc, 2),
            *([(SPLB20._dummy, 1)] * 4),
            (SPLB20._sta_zp_x, 2),
            *([(SPLB20._dummy, 1)] * 4),
            (SPLB20._txs, 1),
            *([(SPLB20._dummy, 1)] * 6),
            (SPLB20._lda_ind_x, 2),
            (SPLB20._ldx_imm, 2),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._lda_zp, 2),
            (SPLB20._ldx_zp, 2),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._lda_imm, 2),
            (SPLB20._tax, 1),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._lda_abs, 3),
            (SPLB20._ldx_abs, 3),
            (SPLB20._dummy, 1),
            (SPLB20._bcs, 2),
            *([(SPLB20._dummy, 1)] * 4),
            (SPLB20._lda_zp_x, 2),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._clv, 1),
            (SPLB20._dummy, 1),
            (SPLB20._tsx, 1),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._lda_abs_x, 3),
            *([(SPLB20._dummy, 1)] * 7),
            (SPLB20._cmp_zp, 2),
            (SPLB20._dec_zp, 2),
            *([(SPLB20._dummy, 1)] * 2),
            (SPLB20._cmp_imm, 2),
            (SPLB20._dex, 1),
            *([(SPLB20._dummy, 1)] * 5),
            (SPLB20._bne, 2),
            *([(SPLB20._dummy, 1)] * 4),
            (SPLB20._cmp_zp_x, 2),
            (SPLB20._dec_zp_x, 2),
            *([(SPLB20._dummy, 1)] * 9),
            (SPLB20._cpx_imm, 2),
            *([(SPLB20._dummy, 1)] * 3),
            (SPLB20._cpx_zp, 2),
            (SPLB20._sbc_zp, 2),
            (SPLB20._inc_zp, 2),
            (SPLB20._dummy, 1),
            (SPLB20._inx, 1),
            (SPLB20._sbc_imm, 2),
            (SPLB20._nop, 1),
            *([(SPLB20._dummy, 1)] * 5),
            (SPLB20._beq, 2),
            *([(SPLB20._dummy, 1)] * 7),
            (SPLB20._sed, 1),
            *([(SPLB20._dummy, 1)] * 7)
        )

    def examine(self):
        return {
            "PC": self._PC,
            "A": self._A,
            "X": self._X,
            "Y": self._Y,
            "SP": self._SP,
            "NF": self._NF,
            "VF": self._VF,
            "DF": self._DF,
            "BF": self._BF,
            "IF": self._IF,
            "ZF": self._ZF,
            "CF": self._CF,
            "RAM": self._RAM,
            "DATA_RAM": self._DATA_RAM,
            "LCDRAM": self._LCDRAM,
            "IORAM": (
                self._LCD_CFG,
                self._PDIR["PA"],
                self._PCFG["PA"],
                self._port_read("PA"),
                0,
                0,
                self._LCD_BIAS,
                0,
                0,
                self._INT_CFG,
                self._SYS_CTRL,
                self._TC_PRESET,
                self._PRESCALAR,
                self._KEYSCAN_CTRL,
                0
            )
        }

    def edit_state(self, state):
        if ("PC" in state):
            self._PC = state["PC"] & 0xFFFF
        if ("A" in state):
            self._A = state["A"] & 0xFF
        if ("X" in state):
            self._X = state["X"] & 0xFF
        if ("Y" in state):
            self._Y = state["Y"] & 0xFF
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
        if ("DATA_RAM" in state):
            for i, value in state["DATA_RAM"].items():
                self._RAM[i] = value & 0xFF
        if ("LCDRAM" in state):
            for i, value in state["LCDRAM"].items():
                self._LCDRAM[i] = value & 0xFF
        if ("IORAM" in state):
            for i, value in state["IORAM"].items():
                if i < len(self._io_tbl):
                    list(self._io_tbl.values())[i][1](self, value & 0xFF)

    def reset(self):
        self._T2HZ_counter = 0
        self._T128HZ_counter = 0

        self._PC = 0
        self._SP = 0

        self._A = 0
        self._X = 0
        self._Y = 0
        
        self._set_ps(0x04)

        self._ROSC_ENBL = 1
        self._CPU_ENBL = 1
        self._32K_ENBL = 1

        self._RAM = [0] * CPURAM_SIZE
        self._DATA_RAM = [0] * DATARAM_SIZE
        self._LCDRAM = [0] * LCDRAM_SIZE

        self._PCFG = {
            "PA": 0
        }

        self._PDIR = {
            "PA": 0
        }

        self._PULLUP = {
            "PA": 0
        }

        self._PLATCH = {
            "PA": 0
        }

        self._LCD_CFG = 0
        self._LCD_BIAS = 0
        self._SYS_CTRL = 0
        self._INT_CFG = 0
        self._IREQ = 0
        
        self._TC = 0
        self._TC_PRESET = 0
        self._PRESCALAR = 0
        self._KEYSCAN_CTRL = 0

        self._sound.set_enable(False, 0)
        self._go_vector(VADDR_RESET)
        
    def _go_vector(self, addr):
        self._PC = self._ROM.getWordLSB(addr)

    def pc(self):
        return self._PC
    
    def get_VRAM(self):
        if (self._SYS_CTRL & IO_SYS_CTRL_LCD_ENBL):
            return tuple(self._LCDRAM)
        return ()

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
            (~self._PDIR[port] & self._PLATCH[port]) | 
            (self._PDIR[port] & (~self._port_input[port][0] & 
            (self._port_input[port][1] | self._PULLUP[port] | self._pullup_ext[port])))
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
            if (prev_port != self._port_read(port)):
                if (port == "PA" and level == 0):
                    if (self._INT_CFG & IO_INT_CFG_NORMALKEY_INT):
                        self._IREQ |= IO_INT_CFG_NORMALKEY_INT
                        self._NMI()

    def _IRQ(self, addr):
        self._write_mem(self._SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, self._ps())
        self._SP = (self._SP - 1) & 0xFF
        self._IF = 1
        self._go_vector(VADDR_IRQ)

    def _NMI(self):
        if (self._INT_CFG & IO_INT_CFG_NMI_ENBL):
            if (self._ROSC_ENBL and self._CPU_ENBL):
                self._write_mem(self._SP, self._PC >> 8)
                self._SP = (self._SP - 1) & 0xFF
                self._write_mem(self._SP, self._PC & 0xFF)
                self._SP = (self._SP - 1) & 0xFF
                self._write_mem(self._SP, self._ps())
                self._SP = (self._SP - 1) & 0xFF
                self._go_vector(VADDR_NMI)
            else:
                self._CPU_ENBL = self._ROSC_ENBL = 1
                self._go_vector(VADDR_RESET)

    def _timers_clock(self, exec_cycles):
        if (self._SYS_CTRL & IO_SYS_CTRL_TIMER_ENBL):
            self._timer_counter -= exec_cycles
            while (self._timer_counter <= 0):
                if (self._non_crystal_mode):
                    self._timer_counter += (1 << self._PRESCALAR)
                else:
                    self._timer_counter += self._sub_clock_div
                self._TC -= 1
                if (self._TC < 0):
                    self._TC = self._TC_PRESET
                    if (self._INT_CFG & IO_INT_CFG_COUNTER_INT):
                        self._IREQ |= IO_INT_CFG_COUNTER_INT
                        self._NMI()

        self._T2HZ_counter -= exec_cycles
        while (self._T2HZ_counter <= 0):
            if (self._non_crystal_mode):
                self._T2HZ_counter += (1 << self._PRESCALAR) * (SUB_CLOCK // 2)
            else:
                self._T2HZ_counter += self._sub_clock_div * (SUB_CLOCK // 2)
            if (self._INT_CFG & IO_INT_CFG_T2HZ_INT):
                self._IREQ |= IO_INT_CFG_T2HZ_INT
                self._NMI()
        
        self._T128HZ_counter -= exec_cycles
        while (self._T128HZ_counter <= 0):
            if (self._non_crystal_mode):
                self._T128HZ_counter += (1 << self._PRESCALAR) * (SUB_CLOCK // 128)
            else:
                self._T128HZ_counter += self._sub_clock_div * (SUB_CLOCK // 128)
            if (self._INT_CFG & IO_INT_CFG_T128HZ_INT):
                self._IREQ |= IO_INT_CFG_T128HZ_INT
                self._NMI()

    def clock(self):
        exec_cycles = MCLOCK_DIV
        if (self._ROSC_ENBL):
            if (self._CPU_ENBL):
                byte = self._ROM.getByte(self._PC - self._rom_offset)
                bytes_count = self._execute[byte][1]
                opcode = self._ROM.getBytes(self._PC - self._rom_offset, bytes_count)
                self._PC += bytes_count
                exec_cycles = self._execute[byte][0](self, opcode)
                self._instr_counter += 1
            self._timers_clock(exec_cycles)
        elif (self._SYS_CTRL & IO_SYS_CTRL_32K_ENBL):
            exec_cycles = self._sub_clock_div
            self._timers_clock(exec_cycles)

        self._cycle_counter += exec_cycles
        return exec_cycles

    def _get_io_LCD_Configure(self):
        return self._LCD_CFG
    
    def _set_io_LCD_Configure(self, value):
        self._LCD_CFG = value

    def _get_io_PortA_IOConfigure(self):
        return self._PDIR["PA"]
    
    def _set_io_PortA_IOConfigure(self, value):
        self._PDIR["PA"] = value

    def _get_io_PortA_Output(self):
        return self._PCFG["PA"]
    
    def _set_io_PortA_Output(self, value):
        self._PCFG["PA"] = value
        self._sound.set_enable(value & 0xC0 == 0xC0, self._cycle_counter)

    def _get_io_PortA_Data(self):
        return self._port_read("PA")
    
    def _set_PortA_Data(self, value):
        self._PLATCH["PA"] = value

    def _get_io_PortXY_Data(self):
        return 0
    
    def _set_PortXY_Data(self, value):
        pass

    def _get_io_PortZ_Data(self):
        return 0
    
    def _set_PortZ_Data(self, value):
        pass

    def _get_io_LCD_Bias(self):
        return self._LCD_BIAS
    
    def _set_io_LCD_Bias(self, value):
        self._LCD_BIAS = value

    def _get_io_KeyScan_OutputL(self):
        return 0
    
    def _set_io_KeyScan_OutputL(self, value):
        pass

    def _get_io_KeyScan_OutputH(self):
        return 0
    
    def _set_io_KeyScan_OutputH(self, value):
        pass

    def _get_io_Interrupt_Config(self):
        buf = self._IREQ | (self._INT_CFG & 0x80)
        self._IREQ = 0
        return buf

    def _set_io_Interrupt_Config(self, value):
        self._INT_CFG = value

    def _get_io_System_Ctrl(self):
        return self._SYS_CTRL
    
    def _set_io_System_Ctrl(self, value):
        self._ROSC_ENBL = ((self._SYS_CTRL | ~value) & IO_SYS_CTRL_ROSC_STOP) > 0
        self._CPU_ENBL = ((self._SYS_CTRL | ~value) & IO_SYS_CTRL_CPU_STOP) > 0
        self._SYS_CTRL = value
        if ((not self._ROSC_ENBL and self._non_crystal_mode) or (not value & IO_SYS_CTRL_TIMER_ENBL)):
            self._sound.set_enable(False, self._cycle_counter)
        else:
            self._sound.set_enable(self._PCFG["PA"] & 0xC0 == 0xC0, self._cycle_counter)

    def _get_io_DownCounter_PresetValue(self):
        return self._TC_PRESET
     
    def _set_io_DownCounter_PresetValue(self, value):
        self._TC_PRESET = value
        self._sound.set_tc_div(value, self._cycle_counter)

    def _get_io_Prescalar_Ctrl(self):
        return self._PRESCALAR
    
    def _set_io_Prescalar_Ctrl(self, value):
        self._PRESCALAR = value
        if (self._non_crystal_mode):
            self._sound.set_clock_div(1 << value, self._cycle_counter)

    def _get_io_KeyScan_Ctrl(self):
        return self._KEYSCAN_CTRL
    
    def _set_io_KeyScan_Ctrl(self, value):
        self._KEYSCAN_CTRL = value

    def _get_io_Watchdog_Clear(self):
        return 0
    
    def _set_io_Watchdog_Clear(self, value):
        pass

    def _write_mem(self, addr, value):
        if ((addr >= LCDRAM_OFFSET) and (addr < LCDRAM_SIZE + LCDRAM_OFFSET)):
            self._LCDRAM[addr - LCDRAM_OFFSET] = value
        elif ((addr >= CPU_RAM_OFFSET) and (addr < CPURAM_SIZE + CPU_RAM_OFFSET)):
            self._RAM[addr - CPU_RAM_OFFSET] = value
        elif ((addr >= DATARAM_OFFSET) and (addr < DATARAM_SIZE + DATARAM_OFFSET)):
            self._DATA_RAM[addr - DATARAM_OFFSET] = value
        else:
            io = self._io_tbl.get(addr)
            if (io != None):
                io[1](self, value)

    def _read_mem(self, addr):
        if ((addr >= LCDRAM_OFFSET) and (addr < LCDRAM_SIZE + LCDRAM_OFFSET)):
            return self._LCDRAM[addr - LCDRAM_OFFSET]
        elif ((addr >= CPU_RAM_OFFSET) and (addr < CPURAM_SIZE + CPU_RAM_OFFSET)):
            return self._RAM[addr - CPU_RAM_OFFSET]
        elif ((addr >= DATARAM_OFFSET) and (addr < DATARAM_SIZE + DATARAM_OFFSET)):
            return self._DATA_RAM[addr - DATARAM_OFFSET]
        elif ((addr >= SFR_OFFSET) and (addr < SFR_SIZE + SFR_OFFSET)):
            io = self._io_tbl.get(addr)
            if (io != None):
                return io[0](self)
        elif (addr >= self._rom_offset):
            return self._ROM.getByte(addr - self._rom_offset)
        return 0

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

    def _brk(self, opcode):
        self._BF = 1
        self._PC = (self._PC + 1) & 0xFFFF
        self._IRQ()
        return 7

    def _ora_zp(self, opcode):
        self._A |= self._read_mem(opcode & 0xFF)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _php(self, opcode):
        self._write_mem(self._SP, self._ps())
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _ora_imm(self, opcode):
        self._A |= opcode & 0xFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _bpl(self, opcode):
        if (not self._NF):
            prev_PC = self._PC
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        return 2

    def _clc(self, opcode):
        self._CF = 0
        return 2

    def _jsr_abs(self, opcode):
        pc = self._PC - 1
        self._write_mem(self._SP, (pc >> 8) & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, pc & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._PC = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        return 6

    def _bit_zp(self, opcode):
        m = self._read_mem(opcode & 0xFF)
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 3

    def _and_zp(self, opcode):
        self._A &= self._read_mem(opcode & 0xFF)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _rol_zp(self, opcode):
        new_value = (self._read_mem(opcode & 0xFF) << 1) | self._CF
        self._write_mem(opcode & 0xFF, new_value & 0xFF)
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 5

    def _plp(self, opcode):
        self._SP = (self._SP + 1) & 0xFF
        self._set_ps(self._read_mem(self._SP))
        return 4

    def _and_imm(self, opcode):
        self._A &= opcode
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _rol_a(self, opcode):
        new_value = (self._A << 1) | self._CF
        self._A = new_value & 0xFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 2

    def _bit_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        m = self._read_mem(addr)
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 4

    def _bmi(self, opcode):
        if (self._NF):
            prev_PC = self._PC
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        return 2

    def _sec(self, opcode):
        self._CF = 1
        return 2

    def _rti(self, opcode):
        self._SP = (self._SP + 1) & 0xFF
        self._set_ps(self._read_mem(self._SP))
        self._SP = (self._SP + 1) & 0xFF
        self._PC = self._read_mem(self._SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SP) << 8
        return 6

    def _eor_zp(self, opcode):
        self._A ^= self._read_mem(opcode & 0xFF)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _pha(self, opcode):
        self._write_mem(self._SP, self._A)
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _eor_imm(self, opcode):
        self._A ^= opcode & 0xFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _jmp_abs(self, opcode):
        self._PC = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        return 3

    def _bvc(self, opcode):
        if (not self._VF):
            prev_PC = self._PC
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        return 2

    def _eor_zp_x(self, opcode):
        self._A ^= self._read_mem((opcode + self._X) & 0xFF)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _lsr_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, prev_value >> 1)
        self._NF = 0
        self._ZF = prev_value <= 1
        self._CF = prev_value & 0x01
        return 6

    def _cli(self, opcode):
        self._IF = 0
        return 2

    def _rts(self, opcode):
        self._SP = (self._SP + 1) & 0xFF
        self._PC = self._read_mem(self._SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SP) << 8
        self._PC += 1
        return 6

    def _adc_zp(self, opcode):
        self._adc(self._read_mem(opcode & 0xFF))
        return 3

    def _ror_zp(self, opcode):
        prev_value = self._read_mem(opcode & 0xFF)
        self._write_mem(opcode & 0xFF, (prev_value >> 1) | (self._CF << 7))
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 5

    def _pla(self, opcode):
        self._SP = (self._SP + 1) & 0xFF
        self._A = self._read_mem(self._SP)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _adc_imm(self, opcode):
        self._adc(opcode & 0xFF)
        return 2

    def _ror_a(self, opcode):
        prev_value = self._A
        self._A = (prev_value >> 1) | (self._CF << 7)
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 2

    def _jmp_ind(self, opcode):
        addr = ((opcode >> 8) & 0xFF) | ((opcode & 0xFF) << 8)
        self._PC = self._read_mem(addr)
        self._PC |= self._read_mem((addr + 1) & 0xFFFF) << 8
        return 6

    def _bvs(self, opcode):
        if (self._VF):
            prev_PC = self._PC
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        return 2

    def _sei(self, opcode):
        self._IF = 1
        return 2

    def _sta_ind_x(self, opcode):
        addr = self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8)
        self._write_mem(addr, self._A)
        return 6

    def _sta_zp(self, opcode):
        self._write_mem(opcode & 0xFF, self._A)
        return 3

    def _stx_zp(self, opcode):
        self._write_mem(opcode & 0xFF, self._X)
        return 3

    def _txa(self, opcode):
        self._A = self._X
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _stx_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        self._write_mem(addr, self._X)
        return 4

    def _bcc(self, opcode):
        if (not self._CF):
            prev_PC = self._PC
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        return 2

    def _sta_zp_x(self, opcode):
        self._write_mem((opcode + self._X) & 0xFF, self._A)
        return 4

    def _txs(self, opcode):
        self._SP = self._X
        return 2

    def _lda_ind_x(self, opcode):
        self._A = self._read_mem(self._read_mem((opcode + self._X) & 0xFF) | (self._read_mem((opcode + self._X + 1) & 0xFF) << 8))
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 6

    def _ldx_imm(self, opcode):
        self._X = opcode & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _lda_zp(self, opcode):
        self._A = self._read_mem(opcode & 0xFF)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _ldx_zp(self, opcode):
        self._X = self._read_mem(opcode & 0xFF)
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 3

    def _lda_imm(self, opcode):
        self._A = opcode & 0xFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _tax(self, opcode):
        self._X = self._A
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _lda_abs(self, opcode):
        self._A = self._read_mem(((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF))
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _ldx_abs(self, opcode):
        addr = ((opcode & 0xFF) << 8) | ((opcode >> 8) & 0xFF)
        self._X = self._read_mem(addr)
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 4

    def _bcs(self, opcode):
        if (self._CF):
            prev_PC = self._PC
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        return 2

    def _lda_zp_x(self, opcode):
        self._A = self._read_mem((opcode + self._X) & 0xFF)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _clv(self, opcode):
        self._VF = 0
        return 2

    def _tsx(self, opcode):
        self._X = self._SP
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _lda_abs_x(self, opcode):
        addr = (((opcode << 8) | ((opcode >> 8) & 0xFF)) + self._X) & 0xFFFF
        self._A = self._read_mem(addr)
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((self._PC ^ addr) > 255)

    def _cmp_zp(self, opcode):
        test_value = self._A - self._read_mem(opcode & 0xFF)
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3

    def _dec_zp(self, opcode):
        new_value = (self._read_mem(opcode & 0xFF) - 1) & 0xFF
        self._write_mem(opcode & 0xFF, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _cmp_imm(self, opcode):
        test_value = self._A - (opcode & 0xFF)
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _dex(self, opcode):
        self._X = (self._X - 1) & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _bne(self, opcode):
        if (not self._ZF):
            prev_PC = self._PC
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        return 2

    def _cmp_zp_x(self, opcode):
        test_value = self._A - self._read_mem((opcode + self._X) & 0xFF)
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4

    def _dec_zp_x(self, opcode):
        addr = (opcode + self._X) & 0xFF
        new_value = (self._read_mem(addr) - 1) & 0xFF
        self._write_mem(addr, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _cpx_imm(self, opcode):
        test_value = self._X - (opcode & 0xFF)
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _cpx_zp(self, opcode):
        test_value = self._X - self._read_mem(opcode & 0xFF)
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3

    def _sbc_zp(self, opcode):
        self._sbc(self._read_mem(opcode & 0xFF))
        return 3

    def _inc_zp(self, opcode):
        new_value = (self._read_mem(opcode & 0xFF) + 1) & 0xFF
        self._write_mem(opcode & 0xFF, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _inx(self, opcode):
        self._X = (self._X + 1) & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _sbc_imm(self, opcode):
        self._sbc(opcode & 0xFF)
        return 2

    def _nop(self, opcode):
        return 2

    def _beq(self, opcode):
        if (self._ZF):
            prev_PC = self._PC
            self._PC = (self._PC + (opcode & 0xFF) - ((opcode & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        return 2

    def _sed(self, opcode):
        self._DF = 1
        return 2
    
    def _dummy(self, opcode):
        print("illegal instruction %0.4X: %0.4X" % (self._PC, opcode))
        return 2
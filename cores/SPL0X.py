from .rom import ROM
from .SPL0Xsound import SPL0Xsound

SUB_CLOCK = 32768
MCLOCK_DIV = 1

ADDRESS_SPACE_SIZE = 0x2000

VADDR_NMI = 0x1FFA
VADDR_RESET = 0x1FFC
VADDR_IRQ = 0x1FFE

IO_CTRL_ALDIR = 0x01
IO_CTRL_AHDIR = 0x02
IO_CTRL_BDIR = 0x04
IO_CTRL_ROSC = 0x10
IO_CTRL_CPU_CLOCK = 0x20
IO_CTRL_LCD_DUTY = 0xC0

IO_INT_CFG_T2HZ_INT = 0x01
IO_INT_CFG_T256HZ_INT = 0x02
IO_INT_CFG_POWERKEY_INT = 0x04
IO_INT_CFG_NMI_ENBL = 0x80

IO_SYS_CTRL_32K_ENBL = 0x20
IO_SYS_CTRL_CPU_STOP = 0x40
IO_SYS_CTRL_ROSC_STOP = 0x80

IO_SPEECH_CTRL_ENBL = 0x01

class SPL0X():
    def __init__(self, mask, clock):
        self._ROM = ROM(mask['rom_path'])

        self._cycle_counter = 0

        self._pullup_ext = {
            **{"PA": 0, "PB": 0},
            **mask['port_pullup']
        }

        self._port_input = {
            "PA": [0, 0],
            "PB": [0, 0]
        }

        self._port_pkey = {
            **{"PA": 1, "PB": 0},
            **mask['port_pkey']            
        }
    
        self._instr_counter = 0

        self._clock = clock
        self._sub_clock_div = mask['non_crystal_div']
        if (self._sub_clock_div == 0):
            self._sub_clock_div = clock / SUB_CLOCK

        self._sound = SPL0Xsound(clock, self._sub_clock_div)
        
        self.reset()

        self._io_tbl = {
            0xC0: (SPL0X._get_io_IO_Ctrl, SPL0X._set_io_IO_Ctrl),
            0xC1: (SPL0X._get_io_PortA_Data, SPL0X._set_io_PortA_Data),
            0xC3: (SPL0X._get_io_PortB_Data, SPL0X._set_io_PortB_Data),
            0xC4: (SPL0X._get_io_ToneA_Ctrl1, SPL0X._set_io_ToneA_Ctrl1),
            0xC6: (SPL0X._get_io_ToneA_Ctrl2, SPL0X._set_io_ToneA_Ctrl2),
            0xC8: (SPL0X._get_io_ToneB_Ctrl1, SPL0X._set_io_ToneB_Ctrl1),
            0xCA: (SPL0X._get_io_ToneB_Ctrl2, SPL0X._set_io_ToneB_Ctrl2),
            0xCC: (SPL0X._get_io_Noise_Ctrl1, SPL0X._set_io_Noise_Ctrl1),
            0xCE: (SPL0X._get_io_Noise_Ctrl2, SPL0X._set_io_Noise_Ctrl2),
            0xD0: (SPL0X._get_io_System_Ctrl, SPL0X._set_io_System_Ctrl),
            0xD2: (SPL0X._get_io_Interrupt_Config, SPL0X._set_io_Interrupt_Config),
            0xD4: (SPL0X._get_io_Speech_Ctrl, SPL0X._set_io_Speech_Ctrl),
            0xD5: (SPL0X._get_io_Speech_Data_Port, SPL0X._set_io_Speech_Data_Port),
            0xD7: (SPL0X._get_io_Bank_Select, SPL0X._set_io_Bank_Select),
        }

        self._execute = (
            (SPL0X._brk, 1),
            *([(SPL0X._dummy, 1)] * 4),
            (SPL0X._ora_zp, 2),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._php, 1),
            (SPL0X._ora_imm, 2),
            *([(SPL0X._dummy, 1)] * 6),
            (SPL0X._bpl, 2),
            *([(SPL0X._dummy, 1)] * 7),
            (SPL0X._clc, 1),
            *([(SPL0X._dummy, 1)] * 7),
            (SPL0X._jsr_abs, 3),
            *([(SPL0X._dummy, 1)] * 3),
            (SPL0X._bit_zp, 2),
            (SPL0X._and_zp, 2),
            (SPL0X._rol_zp, 2),
            (SPL0X._dummy, 1),
            (SPL0X._plp, 1),
            (SPL0X._and_imm, 2),
            (SPL0X._rol_a, 1),
            (SPL0X._dummy, 1),
            (SPL0X._bit_abs, 3),
            *([(SPL0X._dummy, 1)] * 3),
            (SPL0X._bmi, 2),
            *([(SPL0X._dummy, 1)] * 7),
            (SPL0X._sec, 1),
            *([(SPL0X._dummy, 1)] * 7),
            (SPL0X._rti, 1),
            *([(SPL0X._dummy, 1)] * 4),
            (SPL0X._eor_zp, 2),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._pha, 1),
            (SPL0X._eor_imm, 2),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._jmp_abs, 3),
            *([(SPL0X._dummy, 1)] * 3),
            (SPL0X._bvc, 2),
            *([(SPL0X._dummy, 1)] * 4),
            (SPL0X._eor_zp_x, 2),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._cli, 1),
            *([(SPL0X._dummy, 1)] * 7),
            (SPL0X._rts, 1),
            *([(SPL0X._dummy, 1)] * 4),
            (SPL0X._adc_zp, 2),
            (SPL0X._ror_zp, 2),
            (SPL0X._dummy, 1),
            (SPL0X._pla, 1),
            (SPL0X._adc_imm, 2),
            (SPL0X._ror_a, 1),
            (SPL0X._dummy, 1),
            (SPL0X._jmp_ind, 3),
            *([(SPL0X._dummy, 1)] * 3),
            (SPL0X._bvs, 2),
            *([(SPL0X._dummy, 1)] * 7),
            (SPL0X._sei, 1),
            *([(SPL0X._dummy, 1)] * 8),
            (SPL0X._sta_ind_x, 2),
            *([(SPL0X._dummy, 1)] * 3),
            (SPL0X._sta_zp, 2),
            (SPL0X._stx_zp, 2),
            *([(SPL0X._dummy, 1)] * 3),
            (SPL0X._txa, 1),
            *([(SPL0X._dummy, 1)] * 3),
            (SPL0X._stx_abs, 3),
            (SPL0X._dummy, 1),
            (SPL0X._bcc, 2),
            *([(SPL0X._dummy, 1)] * 4),
            (SPL0X._sta_zp_x, 2),
            *([(SPL0X._dummy, 1)] * 4),
            (SPL0X._txs, 1),
            *([(SPL0X._dummy, 1)] * 6),
            (SPL0X._lda_ind_x, 2),
            (SPL0X._ldx_imm, 2),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._lda_zp, 2),
            (SPL0X._ldx_zp, 2),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._lda_imm, 2),
            (SPL0X._tax, 1),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._lda_abs, 3),
            (SPL0X._ldx_abs, 3),
            (SPL0X._dummy, 1),
            (SPL0X._bcs, 2),
            *([(SPL0X._dummy, 1)] * 4),
            (SPL0X._lda_zp_x, 2),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._clv, 1),
            (SPL0X._dummy, 1),
            (SPL0X._tsx, 1),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._lda_abs_x, 3),
            *([(SPL0X._dummy, 1)] * 7),
            (SPL0X._cmp_zp, 2),
            (SPL0X._dec_zp, 2),
            *([(SPL0X._dummy, 1)] * 2),
            (SPL0X._cmp_imm, 2),
            (SPL0X._dex, 1),
            *([(SPL0X._dummy, 1)] * 5),
            (SPL0X._bne, 2),
            *([(SPL0X._dummy, 1)] * 4),
            (SPL0X._cmp_zp_x, 2),
            (SPL0X._dec_zp_x, 2),
            *([(SPL0X._dummy, 1)] * 9),
            (SPL0X._cpx_imm, 2),
            *([(SPL0X._dummy, 1)] * 3),
            (SPL0X._cpx_zp, 2),
            (SPL0X._sbc_zp, 2),
            (SPL0X._inc_zp, 2),
            (SPL0X._dummy, 1),
            (SPL0X._inx, 1),
            (SPL0X._sbc_imm, 2),
            (SPL0X._nop, 1),
            *([(SPL0X._dummy, 1)] * 5),
            (SPL0X._beq, 2),
            *([(SPL0X._dummy, 1)] * 7),
            (SPL0X._sed, 1),
            *([(SPL0X._dummy, 1)] * 7)
        )

    def _get_pc(self):
        if (self._PC > 0xFFF):
            return (self._PC % ADDRESS_SPACE_SIZE) + (self._ROM_BANK << 12)
        return self._PC

    def examine(self):
        return {
            "PC": self._get_pc(),
            "PC13": self._PC,
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
                self._IO_CTRL,
                self._port_read("PA"),
                self._port_read("PB"),
                self._TONEA_CTRL1,
                self._TONEA_CTRL2,
                self._TONEB_CTRL1,
                self._TONEB_CTRL2,
                self._NOISE_CTRL1,
                self._NOISE_CTRL2,
                self._SYS_CTRL,
                self._INT_CFG,
                self._SPEECH_CTRL,
                self._SPEECH_DATA,
                self._ROM_BANK
            )
        }

    def edit_state(self, state):
        if ("PC13" in state):
            self._PC = state["PC13"] % ADDRESS_SPACE_SIZE
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
                self._LCDRAM[i] = value & 0xFF
        if ("IORAM" in state):
            for i, value in state["IORAM"].items():
                if i < len(self._io_tbl):
                    list(self._io_tbl.values())[i][1](self, value & 0xFF)

    def reset(self):
        self._T2HZ_counter = 0
        self._T256HZ_counter = 0

        self._PC = 0
        self._SP = 0

        self._A = 0
        self._X = 0
        
        self._set_ps(0x04)

        self._CPU_ENBL = 1
        self._ROSC_ENBL = 1
        self._32K_ENBL = 1

        self._RAM = [0] * self.CPURAM_SIZE
        self._LCDRAM = [0] * self.LCDRAM_SIZE

        self._ROM_BANK = 0

        self._PDIR = {
            "PA": 0,
            "PB": 0
        }

        self._PLATCH = {
            "PA": 0,
            "PB": 0
        }

        self._IO_CTRL = 0
        self._INT_CFG = 0
        self._IREQ = 0
        self._SYS_CTRL = 0
        self._PRESCALAR = 1
        self._SPEECH_CTRL = 0
        self._SPEECH_DATA = 0
        self._TONEA_CTRL1 = 0
        self._TONEA_CTRL2 = 0
        self._TONEB_CTRL1 = 0
        self._TONEB_CTRL2 = 0
        self._NOISE_CTRL1 = 0
        self._NOISE_CTRL2 = 0

        self._go_vector(VADDR_RESET)
        
    def _go_vector(self, addr):
        self._PC = self._ROM.getWordLSB(addr + (self._ROM_BANK << 12))

    def pc(self):
        return self._PC
    
    def get_VRAM(self):
        return tuple(self._LCDRAM)

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
            if ((prev_port & self._port_pkey[port]) < (self._port_read(port) & self._port_pkey[port])):
                if (self._INT_CFG & IO_INT_CFG_POWERKEY_INT):
                    self._IREQ |= IO_INT_CFG_POWERKEY_INT
                    self._NMI()

    def _IRQ(self):
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
        self._T2HZ_counter -= exec_cycles
        while (self._T2HZ_counter <= 0):
            self._T2HZ_counter += self._sub_clock_div * (SUB_CLOCK // 2)
            if (self._INT_CFG & IO_INT_CFG_T2HZ_INT):
                self._IREQ |= IO_INT_CFG_T2HZ_INT
                self._NMI()

        self._T256HZ_counter -= exec_cycles
        while (self._T256HZ_counter <= 0):
            self._T256HZ_counter += self._sub_clock_div * (SUB_CLOCK // 256)
            if (self._INT_CFG & IO_INT_CFG_T256HZ_INT):
                self._IREQ |= IO_INT_CFG_T256HZ_INT
                self._NMI()

    def clock(self):
        exec_cycles = MCLOCK_DIV
        if (self._ROSC_ENBL):
            if (self._CPU_ENBL):
                addr = self._get_pc()
                byte = self._ROM.getByte(addr)
                bytes_count = self._execute[byte][1]
                opcode = self._ROM.getBytes(addr, bytes_count)
                self._PC += bytes_count
                exec_cycles = self._execute[byte][0](self, opcode)
                self._instr_counter += 1
            self._timers_clock(exec_cycles)
        elif (self._SYS_CTRL & IO_SYS_CTRL_32K_ENBL):
            exec_cycles = self._sub_clock_div
            self._timers_clock(exec_cycles)

        self._cycle_counter += exec_cycles
        return exec_cycles

    def _get_io_IO_Ctrl(self):
        return self._IO_CTRL
    
    def _set_io_IO_Ctrl(self, value):
        if (value & IO_CTRL_ALDIR):
            self._PDIR["PA"] |= 0x0F
        if (value & IO_CTRL_AHDIR):
            self._PDIR["PA"] |= 0xF0
        if (value & IO_CTRL_BDIR):
            self._PDIR["PB"] |= 0x03
        self._ROSC_ENBL = ((self._IO_CTRL | ~value) & IO_CTRL_ROSC) > 0
        if ((value & IO_CTRL_CPU_CLOCK) > 0):
            self._PRESCALAR = 8
        else:
            self._PRESCALAR = 1
        self._IO_CTRL = value

    def _get_io_PortA_Data(self):
        return self._port_read("PA")
    
    def _set_io_PortA_Data(self, value):
        self._PLATCH["PA"] = value

    def _get_io_PortB_Data(self):
        return self._port_read("PB")
    
    def _set_io_PortB_Data(self, value):
        self._PLATCH["PB"] = value

    def _get_io_ToneA_Ctrl1(self):
        return 0

    def _set_io_ToneA_Ctrl1(self, value):
        self._TONEA_CTRL1 = value
        self._sound.set_toneA(self._TONEA_CTRL1, self._TONEA_CTRL2, self._cycle_counter)        

    def _get_io_ToneA_Ctrl2(self):
        return 0
    
    def _set_io_ToneA_Ctrl2(self, value):
        self._TONEA_CTRL2 = value
        self._sound.set_toneA(self._TONEA_CTRL1, self._TONEA_CTRL2, self._cycle_counter)  

    def _get_io_ToneB_Ctrl1(self):
        return 0
    
    def _set_io_ToneB_Ctrl1(self, value):
        self._TONEB_CTRL1 = value
        self._sound.set_toneB(self._TONEB_CTRL1, self._TONEB_CTRL2, self._cycle_counter)  

    def _get_io_ToneB_Ctrl2(self):
        return 0
    
    def _set_io_ToneB_Ctrl2(self, value):
        self._TONEB_CTRL2 = value
        self._sound.set_toneB(self._TONEB_CTRL1, self._TONEB_CTRL2, self._cycle_counter) 

    def _get_io_Noise_Ctrl1(self):
        return 0
    
    def _set_io_Noise_Ctrl1(self, value):
        self._NOISE_CTRL1 = value
        self._sound.set_noise(self._NOISE_CTRL1, self._NOISE_CTRL2, self._cycle_counter)

    def _get_io_Noise_Ctrl2(self):
        return 0
    
    def _set_io_Noise_Ctrl2(self, value):
        self._NOISE_CTRL2 = value
        self._sound.set_noise(self._NOISE_CTRL1, self._NOISE_CTRL2, self._cycle_counter)

    def _get_io_System_Ctrl(self):
        return self._SYS_CTRL
    
    def _set_io_System_Ctrl(self, value):
        self._ROSC_ENBL = ((self._SYS_CTRL | ~value) & IO_SYS_CTRL_ROSC_STOP) > 0
        self._CPU_ENBL = ((self._SYS_CTRL | ~value) & IO_SYS_CTRL_CPU_STOP) > 0
        self._SYS_CTRL = value

    def _get_io_Interrupt_Config(self):
        buf = self._IREQ | (self._INT_CFG & 0x80)
        self._IREQ = 0
        return buf

    def _set_io_Interrupt_Config(self, value):
        self._INT_CFG = value

    def _get_io_Speech_Ctrl(self):
        return self._SPEECH_CTRL

    def _set_io_Speech_Ctrl(self, value):
        self._SPEECH_CTRL = value
        self._sound.set_speech(self._SPEECH_CTRL, self._SPEECH_DATA, self._cycle_counter)

    def _get_io_Speech_Data_Port(self):
        return (self._cycle_counter >> 3) & 0x1

    def _set_io_Speech_Data_Port(self, value):
        self._SPEECH_DATA = value
        self._sound.set_speech(self._SPEECH_CTRL, self._SPEECH_DATA, self._cycle_counter)
        
    def _get_io_Bank_Select(self):
        return self._ROM_BANK
    
    def _set_io_Bank_Select(self, value):
        self._ROM_BANK = value

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
        if (addr >= 0x1000):
            addr = (addr % ADDRESS_SPACE_SIZE) + (self._ROM_BANK << 12)
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
from .rom import ROM
from .STK55C324sound import STK55C324sound

SUB_CLOCK = 32768

ADDRESS_SPACE_SIZE = 0x10000

RAM_SIZE = 0xA0
RAM_OFFSET = 0x40
LCDRAM_SIZE = 0x40
LCDRAM_OFFSET = 0x00

SFR_SLEEP_MODE_1 = 0x01
SFR_SLEEP_MODE_2 = 0x02

SFR_TIMER_CTRL_FIXTIME_1HZ = 0x02
SFR_TIMER_CTRL_CLKSRC32 = 0x10

SFR_IRQ_1 = 0x01
SFR_IRQ_2 = 0x02
SFR_IRQ_3 = 0x04

SFR_CTRL_TIMER1_INT_ENBL = 0x02
SFR_CTRL_NMI_ENBL = 0x04
SFR_CTRL_TIMER1_ENBL = 0x08
SFR_CTRL_LCD_ENBL = 0x10
SFR_CTRL_FIXTIME_INT_ENBL = 0x40

VADDR_IRQ = 0xFFFE
VADDR_RESET = 0xFFFC
VADDR_NMI = 0xFFFA

class STK55C324():
    def __init__(self, mask, clock, interconnect):
        self._ROM = ROM(mask['rom_path'])
        self._sound = STK55C324sound(clock, interconnect)

        self._interconnect = interconnect
        self._interconnect.register_port_device(self)

        self._rom_offset = ADDRESS_SPACE_SIZE - self._ROM.size()

        self._pullup = mask['port_pullup']

        self._port_input = {
            "P1": [0, 0]
        }
    
        self._instr_counter = 0
        self._64Hz_counter = 0
        self._timer1_counter = 0
        self._fixtime_counter = 0
        
        self._sub_clock_div = clock / SUB_CLOCK

        self.reset()

        self._sfr_tbl = {
            0x1000: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_standby_mode),
            0x1001: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_sleep_mode),
            0x1002: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_watch_timer_ctrl),
            0x1003: (STK55C324._get_sfr_irq_flag, STK55C324._set_sfr_irq_flag),
            0x1004: (STK55C324._get_sfr_port1_data, STK55C324._set_sfr_port1_data),
            0x1005: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_port1_dir),
            0x1008: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_volume_ch1),
            0x1009: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_volume_ch2),
            0x100C: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_port1_int),
            0x100D: (STK55C324._get_sfr_timer1_data, STK55C324._set_sfr_timer1_data),
            0x100E: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_timer1_div_contrast),
            0x100F: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_ctrl),
            0x1010: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_sound_clock),
            0x1011: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_data_ch1),
            0x1012: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_data_ch2),
            0x1013: (STK55C324._get_sfr_dummy, STK55C324._set_sfr_sound_ctrl),
        }

        #Instruction set is unknown. 65C02 is used.
        self._execute = (
            STK55C324._brk,
            STK55C324._ora_ind_x,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._tsb_zp,
            STK55C324._ora_zp,
            STK55C324._asl_zp,
            STK55C324._dummy,
            STK55C324._php,
            STK55C324._ora_imm,
            STK55C324._asl_a,
            STK55C324._dummy,
            STK55C324._tsb_abs,
            STK55C324._ora_abs,
            STK55C324._asl_abs,
            STK55C324._dummy,
            STK55C324._bpl,
            STK55C324._ora_ind_y,
            STK55C324._ora_zp_ind,
            STK55C324._dummy,
            STK55C324._trb_zp,
            STK55C324._ora_zp_x,
            STK55C324._asl_zp_x,
            STK55C324._dummy,
            STK55C324._clc,
            STK55C324._ora_abs_y,
            STK55C324._inc_a,
            STK55C324._dummy,
            STK55C324._trb_abs,
            STK55C324._ora_abs_x,
            STK55C324._asl_abs_x,
            STK55C324._dummy,
            STK55C324._jsr_abs,
            STK55C324._and_ind_x,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._bit_zp,
            STK55C324._and_zp,
            STK55C324._rol_zp,
            STK55C324._dummy,
            STK55C324._plp,
            STK55C324._and_imm,
            STK55C324._rol_a,
            STK55C324._dummy,
            STK55C324._bit_abs,
            STK55C324._and_abs,
            STK55C324._rol_abs,
            STK55C324._dummy,
            STK55C324._bmi,
            STK55C324._and_ind_y,
            STK55C324._and_zp_ind,
            STK55C324._dummy,
            STK55C324._bit_zp_x,
            STK55C324._and_zp_x,
            STK55C324._rol_zp_x,
            STK55C324._dummy,
            STK55C324._sec,
            STK55C324._and_abs_y,
            STK55C324._dec_a,
            STK55C324._dummy,
            STK55C324._bit_abs_x,
            STK55C324._and_abs_x,
            STK55C324._rol_abs_x,
            STK55C324._dummy,
            STK55C324._rti,
            STK55C324._eor_ind_x,
            *([(STK55C324._dummy, 1)] * 3),
            STK55C324._eor_zp,
            STK55C324._lsr_zp,
            STK55C324._dummy,
            STK55C324._pha,
            STK55C324._eor_imm,
            STK55C324._lsr_a,
            STK55C324._dummy,
            STK55C324._jmp_abs,
            STK55C324._eor_abs,
            STK55C324._lsr_abs,
            STK55C324._dummy,
            STK55C324._bvc,
            STK55C324._eor_ind_y,
            STK55C324._eor_zp_ind,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._eor_zp_x,
            STK55C324._lsr_zp_x,
            STK55C324._dummy,
            STK55C324._cli,
            STK55C324._eor_abs_y,
            STK55C324._phy,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._eor_abs_x,
            STK55C324._lsr_abs_x,
            STK55C324._dummy,
            STK55C324._rts,
            STK55C324._adc_ind_x,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._stz_zp,
            STK55C324._adc_zp,
            STK55C324._ror_zp,
            STK55C324._dummy,
            STK55C324._pla,
            STK55C324._adc_imm,
            STK55C324._ror_a,
            STK55C324._dummy,
            STK55C324._jmp_ind,
            STK55C324._adc_abs,
            STK55C324._ror_abs,
            STK55C324._dummy,
            STK55C324._bvs,
            STK55C324._adc_ind_y,
            STK55C324._adc_zp_ind,
            STK55C324._dummy,
            STK55C324._stz_zp_x,
            STK55C324._adc_zp_x,
            STK55C324._ror_zp_x,
            STK55C324._dummy,
            STK55C324._sei,
            STK55C324._adc_abs_y,
            STK55C324._ply,
            STK55C324._dummy,
            STK55C324._jmp_abs_ind_x,
            STK55C324._adc_abs_x,
            STK55C324._ror_abs_x,
            STK55C324._dummy,
            STK55C324._bra,
            STK55C324._sta_ind_x,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._sty_zp,
            STK55C324._sta_zp,
            STK55C324._stx_zp,
            STK55C324._dummy,
            STK55C324._dey,
            STK55C324._bit_imm,
            STK55C324._txa,
            STK55C324._dummy,
            STK55C324._sty_abs,
            STK55C324._sta_abs,
            STK55C324._stx_abs,
            STK55C324._dummy,
            STK55C324._bcc,
            STK55C324._sta_ind_y,
            STK55C324._sta_zp_ind,
            STK55C324._dummy,
            STK55C324._sty_zp_x,
            STK55C324._sta_zp_x,
            STK55C324._stx_zp_y,
            STK55C324._dummy,
            STK55C324._tya,
            STK55C324._sta_abs_y,
            STK55C324._txs,
            STK55C324._dummy,
            STK55C324._stz_abs,
            STK55C324._sta_abs_x,
            STK55C324._stz_abs_x,
            STK55C324._dummy,
            STK55C324._ldy_imm,
            STK55C324._lda_ind_x,
            STK55C324._ldx_imm,
            STK55C324._dummy,
            STK55C324._ldy_zp,
            STK55C324._lda_zp,
            STK55C324._ldx_zp,
            STK55C324._dummy,
            STK55C324._tay,
            STK55C324._lda_imm,
            STK55C324._tax,
            STK55C324._dummy,
            STK55C324._ldy_abs,
            STK55C324._lda_abs,
            STK55C324._ldx_abs,
            STK55C324._dummy,
            STK55C324._bcs,
            STK55C324._lda_ind_y,
            STK55C324._lda_zp_ind,
            STK55C324._dummy,
            STK55C324._ldy_zp_x,
            STK55C324._lda_zp_x,
            STK55C324._ldx_zp_y,
            STK55C324._dummy,
            STK55C324._clv,
            STK55C324._lda_abs_y,
            STK55C324._tsx,
            STK55C324._dummy,
            STK55C324._ldy_abs_x,
            STK55C324._lda_abs_x,
            STK55C324._ldx_abs_y,
            STK55C324._dummy,
            STK55C324._cpy_imm,
            STK55C324._cmp_ind_x,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._cpy_zp,
            STK55C324._cmp_zp,
            STK55C324._dec_zp,
            STK55C324._dummy,
            STK55C324._iny,
            STK55C324._cmp_imm,
            STK55C324._dex,
            STK55C324._dummy,
            STK55C324._cpy_abs,
            STK55C324._cmp_abs,
            STK55C324._dec_abs,
            STK55C324._dummy,
            STK55C324._bne,
            STK55C324._cmp_ind_y,
            STK55C324._cmp_zp_ind,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._cmp_zp_x,
            STK55C324._dec_zp_x,
            STK55C324._dummy,
            STK55C324._cld,
            STK55C324._cmp_abs_y,
            STK55C324._phx,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._cmp_abs_x,
            STK55C324._dec_abs_x,
            STK55C324._dummy,
            STK55C324._cpx_imm,
            STK55C324._sbc_ind_x,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._cpx_zp,
            STK55C324._sbc_zp,
            STK55C324._inc_zp,
            STK55C324._dummy,
            STK55C324._inx,
            STK55C324._sbc_imm,
            STK55C324._nop,
            STK55C324._dummy,
            STK55C324._cpx_abs,
            STK55C324._sbc_abs,
            STK55C324._inc_abs,
            STK55C324._dummy,
            STK55C324._beq,
            STK55C324._sbc_ind_y,
            STK55C324._sbc_zp_ind,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._sbc_zp_x,
            STK55C324._inc_zp_x,
            STK55C324._dummy,
            STK55C324._sed,
            STK55C324._sbc_abs_y,
            STK55C324._plx,
            *([(STK55C324._dummy, 1)] * 2),
            STK55C324._sbc_abs_x,
            STK55C324._inc_abs_x,
            STK55C324._dummy
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
            "TF": self._TF,
            "BF": self._BF,
            "DF": self._DF,
            "IF": self._IF,
            "ZF": self._ZF,
            "CF": self._CF,
            "RAM": self._RAM,
            "LCDRAM": self._LCDRAM,
            "SFR": (
                (self._nSTANDBY & 0x1),
                self._SLEEP_MODE,
                self._WATCH_TIMER_CTRL,
                self._IREQ,
                self._port_read("P1"),
                self._PDIR["P1"],
                self._SOUND_CH1_VOL,
                self._SOUND_CH2_VOL,
                self._P1INT,
                self._TIMER1,
                self._TIMER_CLK_LCD_CONTRAST,
                self._CONTROL,
                self._SOUND_CLK,
                self._SOUND_CH1_DATA,
                self._SOUND_CH2_DATA,
                self._SOUND_CTRL
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
        if ("TF" in state):
            self._TF = state["TF"]
        if ("BF" in state):
            self._BF = state["BF"]
        if ("DF" in state):
            self._DF = state["DF"]
        if ("IF" in state):
            self._IF = state["IF"]
        if ("ZF" in state):
            self._NF = state["ZF"]
        if ("CF" in state):
            self._NF = state["CF"]
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._RAM[i] = value & 0xFF
        if ("LCDRAM" in state):
            for i, value in state["LCDRAM"].items():
                self._LCDRAM[i] = value & 0xFF
        if ("SFR" in state):
            for i, value in state["SFR"].items():
                if i < len(self._sfr_tbl):
                    list(self._sfr_tbl.values())[i][1](self, value & 0xFF)

    def reset(self):
        self._PC = 0

        self._A = 0
        self._X = 0
        self._Y = 0
        
        self._set_ps(0x04)

        self._SP = 0

        self._CONTROL = 0

        self._nSTANDBY = 1
        self._SLEEP_MODE = 0

        self._RAM = [0] * RAM_SIZE
        self._LCDRAM = [0] * LCDRAM_SIZE

        self._PDIR = {
            "P1": 0
        }

        self._PLATCH = {
            "P1": 0
        }

        self._P1INT = 0

        self._TIMER1 = self._TIMER1_LATCH = 0xFF
        self._TIMER_CLK_LCD_CONTRAST = 0xF0
        self._TIMER1_DIV = 2
        self._WATCH_TIMER_CTRL = 0
        
        self._IREQ = 0

        self._SOUND_CH1_VOL = 0
        self._SOUND_CH2_VOL = 0
        self._SOUND_CLK = 0
        self._SOUND_CH1_DATA = 0
        self._SOUND_CH2_DATA = 0
        self._SOUND_CTRL = 0

        self._addr_reset = self._ROM.get_word_LSB(VADDR_RESET)
        self._addr_irq = self._ROM.get_word_LSB(VADDR_IRQ)
        self._addr_nmi = self._ROM.get_word_LSB(VADDR_NMI)
        
        self._PC = self._addr_reset

    def pc(self):
        return self._PC % ADDRESS_SPACE_SIZE
    
    def get_VRAM(self):
        if (self._CONTROL & SFR_CTRL_LCD_ENBL) and ((self._SLEEP_MODE & SFR_SLEEP_MODE_1) == 0):
            return tuple(self._LCDRAM)
        return tuple([0x00] * LCDRAM_SIZE)

    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter

    def _port_read(self, port):
        return (
            (self._PDIR[port] & self._PLATCH[port]) | 
            (~self._PDIR[port] & (~self._port_input[port][0] & 
            (self._port_input[port][1] | self._pullup[port])))
        )

    def port_handler(self, port, mask, level):
        if (port == 'RES'):
            if (level == 0):
                self.reset()
        else:
            prev_port = self._port_read(port)
            self._port_input[port][0] &= ~mask
            self._port_input[port][1] &= ~mask
            if (level >= 0):
                self._port_input[port][level] |= mask
            if (port == "P1"):
                if ((prev_port & self._P1INT) > (self._port_read(port) & self._P1INT)):
                    self._IREQ |= SFR_IRQ_3
                    self._nSTANDBY = 1
                    self._SLEEP_MODE = 0

    def _irq(self):
        self._write_mem(self._SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, self._get_ps())
        self._SP = (self._SP - 1) & 0xFF
        self._IF = 1
        self._PC = self._addr_irq

    def _nmi(self):
        self._write_mem(self._SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, self._get_ps())
        self._SP = (self._SP - 1) & 0xFF
        self._PC = self._addr_nmi

    def _timers_clock(self, exec_cycles):
        self._64Hz_counter -= exec_cycles
        while (self._64Hz_counter <= 0):
            self._64Hz_counter += self._sub_clock_div * (SUB_CLOCK // 64)
            if (self._CONTROL & SFR_CTRL_NMI_ENBL):
                self._nSTANDBY = 1
                self._SLEEP_MODE &= 0x01
                self._nmi()

        if (self._CONTROL & SFR_CTRL_FIXTIME_INT_ENBL):
            self._fixtime_counter -= exec_cycles
            while (self._fixtime_counter <= 0):
                if (self._WATCH_TIMER_CTRL & SFR_TIMER_CTRL_FIXTIME_1HZ):
                    self._fixtime_counter += self._sub_clock_div * SUB_CLOCK
                else:
                    self._fixtime_counter += self._sub_clock_div * (SUB_CLOCK // 2)
                self._IREQ |= SFR_IRQ_1
                self._nSTANDBY = 1
                self._SLEEP_MODE &= 0x01

        if (self._CONTROL & SFR_CTRL_TIMER1_ENBL):
            self._timer1_counter -= exec_cycles
            while (self._timer1_counter <= 0):
                self._timer1_counter += self._TIMER1_DIV
                self._TIMER1 -= 1
                if (self._TIMER1 == 0):
                    self._TIMER1 = self._TIMER1_LATCH
                    if (self._CONTROL & SFR_CTRL_TIMER1_INT_ENBL):
                        self._nSTANDBY = 1
                        self._IREQ |= SFR_IRQ_2

    def clock(self):
        exec_cycles = 64

        if ((self._SLEEP_MODE & SFR_SLEEP_MODE_1) == 0):
            if (self._nSTANDBY) and ((self._SLEEP_MODE & SFR_SLEEP_MODE_2 == 0) or (self._WATCH_TIMER_CTRL & SFR_TIMER_CTRL_CLKSRC32)):
                if ((not self._IF) and self._IREQ):
                    for i in (SFR_IRQ_1, SFR_IRQ_2, SFR_IRQ_3):
                        if (self._IREQ & i):
                            self._irq()
                            break

                opcode = self._ROM.get_byte(self._PC)
                self._PC = (self._PC + 1) & 0xFFFF
                exec_cycles = self._execute[opcode](self)
                self._instr_counter += 1

                if (self._WATCH_TIMER_CTRL & SFR_TIMER_CTRL_CLKSRC32):
                    exec_cycles *= self._sub_clock_div

            self._timers_clock(exec_cycles)

        return exec_cycles

    def _get_sfr_dummy(self):
        return 0
    
    def _set_sfr_dummy(self, value):
        pass

    def _set_sfr_standby_mode(self, value):
        self._nSTANDBY = 0

    def _set_sfr_sleep_mode(self, value):
        self._SLEEP_MODE = value

    def _set_sfr_watch_timer_ctrl(self, value):
        self._WATCH_TIMER_CTRL = value

    def _get_sfr_irq_flag(self):
        return self._IREQ
    
    def _set_sfr_irq_flag(self, value):
        self._IREQ &= value
        
    def _get_sfr_port1_data(self):
        return self._port_read("P1")
    
    def _set_sfr_port1_data(self, value):
        self._PLATCH["P1"] = value
    
    def _set_sfr_port1_dir(self, value):
        self._PDIR["P1"] = value
    
    def _set_sfr_port1_int(self, value):
        self._P1INT = value
        
    def _get_sfr_timer1_data(self):
        return self._TIMER1
    
    def _set_sfr_timer1_data(self, value):
        if (value == 0):
            value = 1
        self._TIMER1 = self._TIMER1_LATCH = value

    def _set_sfr_timer1_div_contrast(self, value):
        self._TIMER1_DIV = 2 << (value & 0x3)
        self._TIMER_CLK_LCD_CONTRAST = value

    def _set_sfr_ctrl(self, value):
        self._CONTROL = value
        if (value & SFR_CTRL_NMI_ENBL): #TODO: replace this workaround with a proper solution
            self._64Hz_counter = 0

    def _set_sfr_volume_ch1(self, value):
        self._SOUND_CH1_VOL = value
        self._sound.set_volume(0, value)
            
    def _set_sfr_volume_ch2(self, value):
        self._SOUND_CH2_VOL = value
        self._sound.set_volume(1, value)

    def _set_sfr_sound_clock(self, value):
        self._SOUND_CLK = value
        self._sound.set_clock(value)

    def _set_sfr_data_ch1(self, value):
        self._SOUND_CH1_DATA = value
        self._sound.set_data(0, value)
            
    def _set_sfr_data_ch2(self, value):
        self._SOUND_CH2_DATA = value
        self._sound.set_data(1, value)

    def _set_sfr_sound_ctrl(self, value):
        self._SOUND_CTRL = value
        self._sound.set_control(value)
        
    def _write_mem(self, addr, value):
        addr_ovrlp = addr & 0xFEFF
        if (addr_ovrlp < LCDRAM_SIZE):
            self._LCDRAM[addr_ovrlp] = value
        elif ((addr_ovrlp >= RAM_OFFSET) and (addr_ovrlp < RAM_SIZE + RAM_OFFSET)):
            self._RAM[addr_ovrlp - RAM_OFFSET] = value
        else:
            io = self._sfr_tbl.get(addr)
            if (io != None):
                io[1](self, value)

    def _read_mem(self, addr):
        addr_ovrlp = addr & 0xFEFF
        if (addr_ovrlp < LCDRAM_SIZE):
            return self._LCDRAM[addr_ovrlp]
        elif ((addr_ovrlp >= RAM_OFFSET) and (addr_ovrlp < RAM_SIZE + RAM_OFFSET)):
            return self._RAM[addr_ovrlp - RAM_OFFSET]
        elif (addr >= self._rom_offset):
            return self._ROM.get_byte(addr - self._rom_offset)
        else:
            io = self._sfr_tbl.get(addr)
            if (io != None):
                return io[0](self)
        return 0

    def _get_ps(self):
        return (
            (self._NF << 7) |
            (self._VF << 6) |
            (self._TF << 5) |
            (self._BF << 4) |
            (self._DF << 3) |
            (self._IF << 2) |
            (self._ZF << 1) |
            (self._CF)
        )

    def _set_ps(self, ps):
        self._NF = (ps >> 7)
        self._VF = (ps & 0x40 > 0)
        self._TF = (ps & 0x20 > 0)
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

        self._VF = ((~(A ^ operand) & (A ^ new_value)) >> 7) & 0x1
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

        self._VF = (((A ^ operand) & (A ^ new_value)) >> 7) & 0x1
        self._NF = (new_value >> 7) & 0x1
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >= 0

        self._A = new_value & 0xFF

    def _brk(self):
        self._BF = 1
        self._IRQ()
        return 7
    
    def _ora_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A |= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 6

    def _tsb_zp(self):
        zp = self._read_mem(self._PC)
        m = self._read_mem(zp)
        res = m | self._A
        self._PC = (self._PC + 1) & 0xFFFF
        self._ZF = not res
        self._write_mem(zp, res & 0xFF)
        return 5

    def _ora_zp(self):
        self._A |= self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3
    
    def _asl_zp(self):
        zp = self._read_mem(self._PC)
        new_value = self._read_mem(zp) << 1
        self._write_mem(zp, new_value & 0xFF)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 5

    def _php(self):
        self._write_mem(self._SP, self._get_ps())
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _ora_imm(self):
        self._A |= self._read_mem(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2
    
    def _asl_a(self):
        new_value = self._A << 1
        self._A = new_value & 0xFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value >> 8
        return 2

    def _tsb_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        m = self._read_mem(addr)
        res = m | self._A
        self._PC = (self._PC + 2) & 0xFFFF
        self._ZF = not res
        self._write_mem(addr, res & 0xFF)
        return 6

    def _ora_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._A |= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4
    
    def _asl_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        new_value = self._read_mem(addr) << 1
        self._write_mem(addr, new_value & 0xFF)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 6
    
    def _bpl(self):
        if (not self._NF):
            rel = self._read_mem(self._PC)
            prev_PC = (self._PC + 1) & 0xFFFF
            self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2
        
    def _ora_ind_y(self):
        zp = self._read_mem(self._PC)
        base = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._A |= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 5 + ((base ^ addr) > 255)

    def _ora_zp_ind(self):
        zp = self._read_mem(self._PC)
        addr = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A |= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 5

    def _trb_zp(self):
        zp = self._read_mem(self._PC)
        m = self._read_mem(zp)
        res = m & (self._A ^ 0xFF)
        self._PC = (self._PC + 1) & 0xFFFF
        self._ZF = not res
        self._write_mem(zp, res)
        return 5

    def _ora_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._A |= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _asl_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        new_value = self._read_mem(addr) << 1
        self._write_mem(addr, new_value & 0xFF)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 6

    def _ora_abs_y(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._A |= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((base ^ addr) > 255)

    def _inc_a(self):
        self._A = (self._A + 1) & 0xFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _and_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A &= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 6

    def _trb_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        m = self._read_mem(addr)
        res = m & (self._A ^ 0xFF)
        self._PC = (self._PC + 2) & 0xFFFF
        self._ZF = not res
        self._write_mem(addr, res)
        return 6

    def _ora_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._A |= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((base ^ addr) > 255)

    def _asl_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        new_value = self._read_mem(addr) << 1
        self._write_mem(addr, new_value & 0xFF)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 6 + ((base ^ addr) > 255)
    
    def _clc(self):
        self._CF = 0
        return 2

    def _jsr_abs(self):
        pc = (self._PC + 1) & 0xFFFF
        self._write_mem(self._SP, pc >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP, pc & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._PC = self._read_mem(self._PC) | (self._read_mem(pc) << 8)
        return 6

    def _and_abs_y(self):
        addr = ((self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)) + self._Y) & 0xFFFF
        self._A &= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _dec_a(self):
        self._A = (self._A - 1) & 0xFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _bit_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        m = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 4 + ((base ^ addr) > 255)

    def _and_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._A &= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((base ^ addr) > 255)

    def _rol_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        new_value = (self._read_mem(addr) << 1) | self._CF
        self._write_mem(addr, new_value & 0xFF)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 6 + ((base ^ addr) > 255)

    def _bit_zp(self):
        m = self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 3

    def _and_zp(self):
        self._A &= self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _rol_zp(self):
        opcode = self._read_mem(self._PC)
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
        self._A &= self._read_mem(self._PC)
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
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        m = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 4
    
    def _and_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._A &= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4
    
    def _rol_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        new_value = (self._read_mem(addr) << 1) | self._CF
        self._write_mem(addr, new_value & 0xFF)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 5

    def _bmi(self):
        if (self._NF):
            rel = self._read_mem(self._PC)
            prev_PC = (self._PC + 1) & 0xFFFF
            self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _and_ind_y(self):
        zp = self._read_mem(self._PC)
        base = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._A &= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 5 + ((base ^ addr) > 255)

    def _and_zp_ind(self):
        zp = self._read_mem(self._PC)
        addr = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A &= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 5

    def _bit_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        m = self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not(self._A & m)
        return 4

    def _and_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._A &= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 6

    def _rol_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        new_value = (self._read_mem(addr) << 1) | self._CF
        self._write_mem(addr, new_value & 0xFF)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = new_value & 0x80 > 0
        self._ZF = not(new_value & 0xFF)
        self._CF = new_value > 0xFF
        return 6
       
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
    
    def _eor_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A ^= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4
    
    def _eor_zp(self):
        self._A ^= self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _lsr_zp(self):
        addr = self._read_mem(self._PC)
        prev_value = self._read_mem(addr)
        self._write_mem(addr, prev_value >> 1)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = 0
        self._ZF = not(prev_value & 0xFE)
        self._CF = prev_value & 0x01
        return 5

    def _pha(self):
        self._write_mem(self._SP, self._A)
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _eor_imm(self):
        self._A ^= self._read_mem(self._PC) & 0xFF
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2
    
    def _lsr_a(self):
        prev_value = self._A
        self._A = (prev_value >> 1)
        self._NF = 0
        self._ZF = not(prev_value & 0xFE)
        self._CF = prev_value & 0x01
        return 2
    
    def _jmp_abs(self):
        self._PC = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        return 3
    
    def _eor_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._A ^= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4
    
    def _lsr_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        prev_value = self._read_mem(addr)
        self._write_mem(addr, prev_value >> 1)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = 0
        self._ZF = not(prev_value & 0xFE)
        self._CF = prev_value & 0x01
        return 6
    
    def _bvc(self):
        if (not self._VF):
            rel = self._read_mem(self._PC)
            prev_PC = (self._PC + 1) & 0xFFFF
            self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _eor_ind_y(self):
        zp = self._read_mem(self._PC)
        base = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._A ^= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 5 + ((base ^ addr) > 255)

    def _eor_zp_ind(self):
        zp = self._read_mem(self._PC)
        addr = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A ^= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 5

    def _eor_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._A ^= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _lsr_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, prev_value >> 1)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = 0
        self._ZF = not(prev_value & 0xFE)
        self._CF = prev_value & 0x01
        return 6

    def _cli(self):
        self._IF = 0
        return 2

    def _eor_abs_y(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._A ^= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((base ^ addr) > 255)

    def _phy(self):
        self._write_mem(self._SP, self._Y)
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _eor_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._A ^= self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((base ^ addr) > 255)

    def _lsr_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, prev_value >> 1)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = 0
        self._ZF = not(prev_value & 0xFE)
        self._CF = prev_value & 0x01
        return 6 + ((base ^ addr) > 255)

    def _rts(self):
        self._SP = (self._SP + 1) & 0xFF
        self._PC = self._read_mem(self._SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SP) << 8
        self._PC += 1
        return 6
    
    def _adc_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._adc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 6

    def _stz_zp(self):
        self._write_mem(self._read_mem(self._PC), 0)
        self._PC = (self._PC + 1) & 0xFFFF
        return 3

    def _adc_zp(self):
        self._adc(self._read_mem(self._read_mem(self._PC)))
        self._PC = (self._PC + 1) & 0xFFFF
        return 3

    def _ror_zp(self):
        opcode = self._read_mem(self._PC)
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
        self._adc(self._read_mem(self._PC))
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
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        
        self._PC = self._read_mem(addr)
        self._PC |= self._read_mem((addr + 1) & 0xFFFF) << 8

        return 6
    
    def _adc_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._adc(self._read_mem(addr))
        self._PC = (self._PC + 2) & 0xFFFF
        return 4

    def _ror_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        prev_value = self._read_mem(addr)
        self._write_mem(addr, (prev_value >> 1) | (self._CF << 7))
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 6
      
    def _bvs(self):
        if (self._VF):
            rel = self._read_mem(self._PC)
            prev_PC = (self._PC + 1) & 0xFFFF
            self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _adc_ind_y(self):
        zp = self._read_mem(self._PC)
        base = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._adc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 5 + ((base ^ addr) > 255)

    def _adc_zp_ind(self):
        zp = self._read_mem(self._PC)
        addr = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._adc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 6

    def _stz_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._write_mem(addr, 0)
        self._PC = (self._PC + 1) & 0xFFFF
        return 4

    def _adc_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._adc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 5

    def _ror_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, (prev_value >> 1) | (self._CF << 7))
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 6
    
    def _sei(self):
        self._IF = 1
        return 2

    def _adc_abs_y(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._adc(self._read_mem(addr))
        self._PC = (self._PC + 2) & 0xFFFF
        return 4 + ((base ^ addr) > 255)

    def _ply(self):
        self._SP = (self._SP + 1) & 0xFF
        self._Y = self._read_mem(self._SP)
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 4

    def _jmp_abs_ind_x(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        ptr = (addr + self._X) & 0xFFFF
        self._PC = self._read_mem(ptr)
        self._PC |= self._read_mem((ptr + 1) & 0xFFFF) << 8
        return 6

    def _adc_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._adc(self._read_mem(addr))
        self._PC = (self._PC + 2) & 0xFFFF
        return 4 + ((base ^ addr) > 255)

    def _ror_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        prev_value = self._read_mem(addr)
        self._write_mem(addr, (prev_value >> 1) | (self._CF << 7))
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._CF
        self._ZF = not(prev_value & 0xFE | self._CF)
        self._CF = prev_value & 0x01
        return 6 + ((base ^ addr) > 255)

    def _bra(self):
        rel = self._read_mem(self._PC)
        prev_PC = (self._PC + 1) & 0xFFFF
        self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
        return 3 + ((self._PC ^ prev_PC) > 255)

    def _sta_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        value = self._read_mem(addr)
        self._write_mem(value, self._A)
        self._PC = (self._PC + 1) & 0xFFFF
        return 6
    
    def _sty_zp(self):
        self._write_mem(self._read_mem(self._PC), self._Y)
        self._PC = (self._PC + 1) & 0xFFFF
        return 3
    
    def _sta_zp(self):
        self._write_mem(self._read_mem(self._PC), self._A)
        self._PC = (self._PC + 1) & 0xFFFF
        return 3

    def _stx_zp(self):
        self._write_mem(self._read_mem(self._PC), self._X)
        self._PC = (self._PC + 1) & 0xFFFF
        return 3
    
    def _dey(self):
        self._Y = (self._Y - 1) & 0xFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 2

    def _bit_imm(self):
        m = self._read_mem(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = m >> 7
        self._VF = m & 0x40 > 0
        self._ZF = not (self._A & m)
        return 2

    def _txa(self):
        self._A = self._X
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _sty_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._write_mem(addr, self._Y)
        self._PC = (self._PC + 2) & 0xFFFF
        return 4
    
    def _sta_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._write_mem(addr, self._A)
        self._PC = (self._PC + 2) & 0xFFFF
        return 4
    
    def _stx_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._write_mem(addr, self._X)
        self._PC = (self._PC + 2) & 0xFFFF
        return 4

    def _bcc(self):
        if (not self._CF):
            rel = self._read_mem(self._PC)
            prev_PC = (self._PC + 1) & 0xFFFF
            self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _sta_ind_y(self):
        zp = self._read_mem(self._PC)
        base = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._write_mem(addr, self._A)
        self._PC = (self._PC + 1) & 0xFFFF
        return 6

    def _sta_zp_ind(self):
        zp = self._read_mem(self._PC)
        addr = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._write_mem(addr, self._A)
        self._PC = (self._PC + 1) & 0xFFFF
        return 6

    def _sty_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._write_mem(addr, self._Y)
        self._PC = (self._PC + 1) & 0xFFFF
        return 4

    def _sta_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._write_mem(addr, self._A)
        self._PC = (self._PC + 1) & 0xFFFF
        return 4

    def _stx_zp_y(self):
        addr = (self._read_mem(self._PC) + self._Y) & 0xFF
        self._write_mem(addr, self._X)
        self._PC = (self._PC + 1) & 0xFFFF
        return 4
    
    def _tya(self):
        self._A = self._Y
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2
    
    def _sta_abs_y(self):
        addr = ((self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)) + self._Y) & 0xFFFF
        self._write_mem(addr, self._A)
        self._PC = (self._PC + 2) & 0xFFFF
        return 5
    
    def _txs(self):
        self._SP = self._X
        return 2

    def _stz_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._write_mem(addr, 0)
        self._PC = (self._PC + 2) & 0xFFFF
        return 4

    def _sta_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._write_mem(addr, self._A)
        self._PC = (self._PC + 2) & 0xFFFF
        return 5

    def _stz_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._write_mem(addr, 0)
        self._PC = (self._PC + 2) & 0xFFFF
        return 5

    def _ldy_imm(self):
        self._Y = self._read_mem(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 2
    
    def _lda_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A = self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 6

    def _ldx_imm(self):
        self._X = self._read_mem(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _ldy_zp(self):
        self._Y = self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 3
    
    def _lda_zp(self):
        self._A = self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 3

    def _ldx_zp(self):
        self._X = self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 3
    
    def _tay(self):
        self._Y = self._A
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 2

    def _lda_imm(self):
        self._A = self._read_mem(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 2

    def _tax(self):
        self._X = self._A
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _ldy_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._Y = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 4

    def _lda_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._A = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _ldx_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._X = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 4

    def _bcs(self):
        if (self._CF):
            rel = self._read_mem(self._PC)
            prev_PC = (self._PC + 1) & 0xFFFF
            self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _lda_ind_y(self):
        zp = self._read_mem(self._PC)
        base = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._A = self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 5 + ((base ^ addr) > 255)

    def _lda_zp_ind(self):
        zp = self._read_mem(self._PC)
        addr = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A = self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 5

    def _ldy_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._Y = self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 4

    def _lda_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._A = self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4

    def _ldx_zp_y(self):
        addr = (self._read_mem(self._PC) + self._Y) & 0xFF
        self._X = self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 4

    def _clv(self):
        self._VF = 0
        return 2
    
    def _lda_abs_y(self):   
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._A = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((base ^ addr) > 255)
    
    def _tsx(self):
        self._X = self._SP
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _ldy_abs_x(self):   
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._Y = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 4 + ((base ^ addr) > 255)

    def _lda_abs_x(self):   
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._A = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
        return 4 + ((base ^ addr) > 255)

    def _ldx_abs_y(self):   
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._X = self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 4 + ((base ^ addr) > 255)

    def _cpy_imm(self):
        test_value = self._Y - self._read_mem(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _cmp_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        test_value = self._A - self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 6

    def _cpy_zp(self):
        test_value = self._Y - self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3
    
    def _cmp_zp(self):
        test_value = self._A - self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3

    def _dec_zp(self):
        opcode = self._read_mem(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        new_value = (self._read_mem(opcode) - 1) & 0xFF
        self._write_mem(opcode, new_value)
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _iny(self):
        self._Y = (self._Y + 1) & 0xFF
        self._NF = self._Y >> 7
        self._ZF = not self._Y
        return 2
    
    def _cmp_imm(self):
        test_value = self._A - (self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _cpy_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        test_value = self._Y - self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3
    
    def _cmp_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        test_value = self._A - self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4

    def _dec_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        new_value = (self._read_mem(addr) - 1) & 0xFF
        self._write_mem(addr, new_value)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 5

    def _dex(self):
        self._X = (self._X - 1) & 0xFF
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 2

    def _bne(self):
        if (not self._ZF):
            rel = self._read_mem(self._PC)
            prev_PC = (self._PC + 1) & 0xFFFF
            self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2
    
    def _cmp_ind_y(self):
        zp = self._read_mem(self._PC)
        base = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        test_value = self._A - self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 5 + ((base ^ addr) > 255)

    def _cmp_zp_ind(self):
        zp = self._read_mem(self._PC)
        addr = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        test_value = self._A - self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 5

    def _cmp_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        test_value = self._A - self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4
    
    def _dec_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        new_value = (self._read_mem(addr) - 1) & 0xFF
        self._write_mem(addr, new_value)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _cld(self):
        self._DF = 0
        return 2

    def _cmp_abs_y(self):   
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        test_value = self._A - self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4 + ((base ^ addr) > 255)

    def _phx(self):
        self._write_mem(self._SP, self._X)
        self._SP = (self._SP - 1) & 0xFF
        return 3

    def _cmp_abs_x(self):   
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        test_value = self._A - self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4 + ((base ^ addr) > 255)

    def _dec_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        new_value = (self._read_mem(addr) - 1) & 0xFF
        self._write_mem(addr, new_value)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 7

    def _cpx_imm(self):
        test_value = self._X - self._read_mem(self._PC)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 2

    def _sbc_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._sbc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 6

    def _cpx_zp(self):
        test_value = self._X - self._read_mem(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 3

    def _sbc_zp(self):
        self._sbc(self._read_mem(self._read_mem(self._PC)))
        self._PC = (self._PC + 1) & 0xFFFF
        return 3

    def _inc_zp(self):
        opcode = self._read_mem(self._PC)
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
        self._sbc(self._read_mem(self._PC))
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _cpx_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        test_value = self._X - self._read_mem(addr)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = (test_value >> 7) & 0x1
        self._ZF = not test_value
        self._CF = test_value >= 0
        return 4
    
    def _sbc_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        self._sbc(self._read_mem(addr))
        self._PC = (self._PC + 2) & 0xFFFF
        return 4
    
    def _inc_abs(self):
        addr = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        new_value = (self._read_mem(addr) + 1) & 0xFF
        self._write_mem(addr, new_value)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _nop(self):
        return 2

    def _beq(self):
        if (self._ZF):
            rel = self._read_mem(self._PC)
            prev_PC = (self._PC + 1) & 0xFFFF
            self._PC = (prev_PC + rel - ((rel & 0x80) << 1)) & 0xFFFF
            return 3 + ((self._PC ^ prev_PC) > 255)
        self._PC = (self._PC + 1) & 0xFFFF
        return 2

    def _sbc_ind_y(self):
        zp = self._read_mem(self._PC)
        base = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._sbc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 4 + ((base ^ addr) > 255)

    def _sbc_zp_ind(self):
        zp = self._read_mem(self._PC)
        addr = self._read_mem(zp) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._sbc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 6

    def _sbc_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        self._sbc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 4

    def _inc_zp_x(self):
        addr = (self._read_mem(self._PC) + self._X) & 0xFF
        new_value = (self._read_mem(addr) + 1) & 0xFF
        self._write_mem(addr, new_value)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 6

    def _sed(self):
        self._DF = 1
        return 2

    def _sbc_abs_y(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._Y) & 0xFFFF
        self._sbc(self._read_mem(addr))
        self._PC = (self._PC + 2) & 0xFFFF
        return 4 + ((base ^ addr) > 255)

    def _plx(self):
        self._SP = (self._SP + 1) & 0xFF
        self._X = self._read_mem(self._SP)
        self._NF = self._X >> 7
        self._ZF = not self._X
        return 4

    def _sbc_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._sbc(self._read_mem(addr))
        self._PC = (self._PC + 2) & 0xFFFF
        return 4 + ((base ^ addr) > 255)

    def _inc_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        new_value = (self._read_mem(addr) + 1) & 0xFF
        self._write_mem(addr, new_value)
        self._PC = (self._PC + 2) & 0xFFFF
        self._NF = new_value >> 7
        self._ZF = not new_value
        return 7

    def _dummy(self):
        print("illegal instruction %0.5X" % self._PC)
        return 2
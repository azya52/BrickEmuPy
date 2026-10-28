from .GPL191Xsound import GPL191Xsound

SUB_CLOCK = 32768

SP = 0x100

VADDR_NMI = 0x7FFA
VADDR_RESET = 0x7FFC
VADDR_IRQ = 0x7FFE

SFR_TIMER_CTRL_ENABLE = 0x80
SFR_TIMER_CTRL_TM0_COUNTER_MODE = 0x10

SFR_TIMER_CTRL_TM0_MASK = 0x20
SFR_TIMER_CTRL_TM0_TIMER1 = 0x20
SFR_TIMER_CTRL_TM0_ROSC = 0x00

SFR_TIMER_CTRL_TM1_MASK = 0x40
SFR_TIMER_CTRL_TM1_32K = 0x40
SFR_TIMER_CTRL_TM1_ROSC = 0x00

SFR_TIMER_CTRL_CNT0_SRCB_MASK = 0x0C
SFR_TIMER_CTRL_CNT0_SRCB_CD1 = 0x00
SFR_TIMER_CTRL_CNT0_SRCB_VDD = 0x04
SFR_TIMER_CTRL_CNT0_SRCB_TIMEBASEH = 0x08
SFR_TIMER_CTRL_CNT0_SRCB_CLK128 = 0x0C
SFR_TIMER_CTRL_CNT0_SRCA_MASK = 0x03
SFR_TIMER_CTRL_CNT0_SRCA_CD0 = 0x00
SFR_TIMER_CTRL_CNT0_SRCA_VDD = 0x01
SFR_TIMER_CTRL_CNT0_SRCA_ROSC = 0x02
SFR_TIMER_CTRL_CNT0_SRCA_CLK32 = 0x03

SFR_WAKEUP_CTRL_EXT = 0x01
SFR_WAKEUP_CTRL_TIME_BASEL = 0x02
SFR_WAKEUP_CTRL_TIMER0 = 0x04
SFR_WAKEUP_CTRL_TIME_BASEH = 0x08

SFR_INT_CTRL_EXT = 0x01
SFR_INT_CTRL_CLK2K = 0x02
SFR_INT_CTRL_CLK128 = 0x04
SFR_INT_CTRL_TIME_BASEL = 0x08
SFR_INT_CTRL_TIME_BASEH = 0x10
SFR_INT_CTRL_TIMER1 = 0x20
SFR_INT_CTRL_TIMER0 = 0x40
SFR_INT_CTRL_UART = 0x80

SFR_NMI_CTRL_TIMER1 = 0x01

SFR_TIMEBASE_L_MASK = 0x80
SFR_TIMEBASE_L_SHIFT = 7
SFR_TIMEBASE_L_2HZ = 0x00
SFR_TIMEBASE_L_1HZ = 0x80

SFR_TIMEBASE_H_MASK = 0x03
SFR_TIMEBASE_H_4HZ = 0x00
SFR_TIMEBASE_H_8HZ = 0x01
SFR_TIMEBASE_H_16HZ = 0x02
SFR_TIMEBASE_H_32HZ = 0x03

SFR_TIMEBASE_H_TBL = (0x0F, 0x07, 0x03, 0x01)
SFR_TIMEBASE_L_TBL = (0x1F, 0x3F)

SFR_AUDIO_CTRL_AUDIO_ENBL = 0x80
SFR_AUDIO_CTRL_TONE_MODE = 0x40
SFR_AUDIO_CTRL_DATA_SRC_MASK = 0x03
SFR_AUDIO_CTRL_DIRECT = 0x00
SFR_AUDIO_CTRL_TM0_OVFLW = 0x01
SFR_AUDIO_CTRL_TM1_OVFLW = 0x02
SFR_AUDIO_CTRL_TM01_OVFLW = 0x03

SFR_CPU_DIV_DEFAULT = 0x02

SFR_LCD_CTRL_ON = 0x02

CPU_RAM_OFFSET = 0x40
RAM_SIZE = 0x2C0
DPRAM_OFFSET = 0x300
DPRAM_SIZE = 0x80
    
class GPL191X():
    def __init__(self, mask, clock, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_pin_device(self)

        self._open_rom(mask['rom_path'])

        self._instr_counter = 0

        self._pullup_ext = {
            **{"AB": 0, "CD": 0, "EF": 0},
            **mask['port_pullup']
        }

        self._port_input = {
            "AB": [0, 0],
            "CD": [0, 0],
            "EF": [0, 0]
        }

        self._clock = clock
        self._sub_clock_div = clock / SUB_CLOCK

        self._sound = GPL191Xsound(interconnect, clock)
        
        self.reset()

        self._sfr_tbl = {
            0x00: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_io_portCD_dir), #P_IO_PortCD_Dir
            0x01: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_io_portAB_dir), #P_IO_PortAB_Dir
            0x02: (GPL191X._get_sfr_io_portAB_data, GPL191X._set_sfr_io_portAB_data), #P_IO_PortAB_Data     
            0x03: (GPL191X._get_sfr_io_portCD_data, GPL191X._set_sfr_io_portCD_data), #P_IO_PortCD_Data
            0x04: (GPL191X._get_sfr_io_portEF_data, GPL191X._set_sfr_io_portEF_data), #P_IO_PortEF_Data
            0x06: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_io_portEF_dir), #P_IO_PortEF_Dir

            0x07: (GPL191X._get_sfr_bank_sel, GPL191X._set_sfr_bank_sel), #P_BANK_Sel

            0x08: (GPL191X._get_sfr_wakeup_ctrl, GPL191X._set_sfr_wakeup_ctrl), #P_WAKEUP_Ctrl

            0x09: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_enter_sleep), #P_Enter_Sleep

            0x0A: (GPL191X._get_sfr_timer_timebase_sel, GPL191X._set_sfr_timer_timebase_sel), #P_TIMER_TimeBase_Sel
            0x0B: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_timer_ctrl), #P_TIMER_Timer_Ctrl

            0x0C: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_clk_32768_en), #P_CLK_32768_En

            0x0D: (GPL191X._get_sfr_int_ctrl, GPL191X._set_sfr_int_ctrl), #P_INT_Ctrl

            0x10: (GPL191X._get_sfr_audio_ch0_data, GPL191X._set_sfr_audio_ch0_data), #P_AUDIO_Ch0_Data
            0x11: (GPL191X._get_sfr_audio_ch1_data, GPL191X._set_sfr_audio_ch1_data), #P_AUDIO_Ch1_Data

            0x12: (GPL191X._get_sfr_timer_TM1L, GPL191X._set_sfr_timer_TM1L), #P_TIMER_TM1Data_LB
            0x13: (GPL191X._get_sfr_timer_TM1H, GPL191X._set_sfr_timer_TM1H), #P_TIMER_TM1Data_HB
            0x14: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_timer_TM1Load_Ctrl), #P_TIMER_TM1Load_Ctrl
            0x15: (GPL191X._get_sfr_timer_TM0L, GPL191X._set_sfr_timer_TM0L), #P_TIMER_TM0Data_LB
            0x16: (GPL191X._get_sfr_timer_TM0H, GPL191X._set_sfr_timer_TM0H), #P_TIMER_TM0Data_HB
            0x17: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_timer_TM0Load_Ctrl), #P_TIMER_TM0Load_Ctrl

            0x18: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_clk_int_clear), #P_INT_Clear
            0x19: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_nmi_ctrl), #P_NMI_Ctrl

            0x1A: (GPL191X._get_sfr_audio_ch0_ctrl, GPL191X._set_sfr_audio_ch0_ctrl), #P_AUDIO_Ch0_Ctrl
            0x1B: (GPL191X._get_sfr_audio_ch1_ctrl, GPL191X._set_sfr_audio_ch1_ctrl), #P_AUDIO_Ch1_Ctrl

            0x1F: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_clk_cpu_ctrl), #P_CLK_CPU_Ctrl

            0x20: (GPL191X._get_sfr_dummy, GPL191X._set_sfr_lcd_ctrl), #P_LCD_Ctrl
        }

        self._execute = (
            GPL191X._brk,
            GPL191X._ora_ind_x,
            *([GPL191X._dummy] * 3),
            GPL191X._ora_zp,
            GPL191X._asl_zp,
            GPL191X._dummy,
            GPL191X._php,
            GPL191X._ora_imm,
            GPL191X._asl_a,
            *([GPL191X._dummy] * 2),
            GPL191X._ora_abs,
            GPL191X._asl_abs,
            GPL191X._dummy,
            GPL191X._bpl,
            GPL191X._ora_ind_y,
            *([GPL191X._dummy] * 3),
            GPL191X._ora_zp_x,
            GPL191X._asl_zp_x,
            GPL191X._dummy,
            GPL191X._clc,
            GPL191X._ora_abs_y,
            *([GPL191X._dummy] * 3),
            GPL191X._ora_abs_x,
            GPL191X._asl_abs_x,
            GPL191X._dummy,
            GPL191X._jsr_abs,
            GPL191X._and_ind_x,
            *([GPL191X._dummy] * 2),
            GPL191X._bit_zp,
            GPL191X._and_zp,
            GPL191X._rol_zp,
            GPL191X._dummy,
            GPL191X._plp,
            GPL191X._and_imm,
            GPL191X._rol_a,
            GPL191X._dummy,
            GPL191X._bit_abs,
            GPL191X._and_abs,
            GPL191X._rol_abs,
            GPL191X._dummy,
            GPL191X._bmi,
            GPL191X._and_ind_y,
            *([GPL191X._dummy] * 3),
            GPL191X._and_zp_x,
            GPL191X._rol_zp_x,
            GPL191X._dummy,
            GPL191X._sec,
            GPL191X._and_abs_y,
            *([GPL191X._dummy] * 3),
            GPL191X._and_abs_x,
            GPL191X._rol_abs_x,
            GPL191X._dummy,
            GPL191X._rti,
            GPL191X._eor_ind_x,
            *([GPL191X._dummy] * 3),
            GPL191X._eor_zp,
            GPL191X._lsr_zp,
            GPL191X._dummy,
            GPL191X._pha,
            GPL191X._eor_imm,
            GPL191X._lsr_a,
            GPL191X._dummy,
            GPL191X._jmp_abs,
            GPL191X._eor_abs,
            GPL191X._lsr_abs,
            GPL191X._dummy,
            GPL191X._bvc,
            GPL191X._eor_ind_y,
            *([GPL191X._dummy] * 3),
            GPL191X._eor_zp_x,
            GPL191X._lsr_zp_x,
            GPL191X._dummy,
            GPL191X._cli,
            GPL191X._eor_abs_y,
            *([GPL191X._dummy] * 3),
            GPL191X._eor_abs_x,
            GPL191X._lsr_abs_x,
            GPL191X._dummy,
            GPL191X._rts,
            GPL191X._adc_ind_x,
            *([GPL191X._dummy] * 3),
            GPL191X._adc_zp,
            GPL191X._ror_zp,
            GPL191X._dummy,
            GPL191X._pla,
            GPL191X._adc_imm,
            GPL191X._ror_a,
            GPL191X._dummy,
            GPL191X._jmp_ind,
            GPL191X._adc_abs,
            GPL191X._ror_abs,
            GPL191X._dummy,
            GPL191X._bvs,
            GPL191X._adc_ind_y,
            *([GPL191X._dummy] * 3),
            GPL191X._adc_zp_x,
            GPL191X._ror_zp_x,
            GPL191X._dummy,
            GPL191X._sei,
            GPL191X._adc_abs_y,
            *([GPL191X._dummy] * 3),
            GPL191X._adc_abs_x,
            GPL191X._ror_abs_x,
            *([GPL191X._dummy] * 2),
            GPL191X._sta_ind_x,
            *([GPL191X._dummy] * 2),
            GPL191X._sty_zp,
            GPL191X._sta_zp,
            GPL191X._stx_zp,
            GPL191X._dummy,
            GPL191X._dey,
            GPL191X._dummy,
            GPL191X._txa,
            GPL191X._dummy,
            GPL191X._sty_abs,
            GPL191X._sta_abs,
            GPL191X._stx_abs,
            GPL191X._dummy,
            GPL191X._bcc,
            GPL191X._sta_ind_y,
            *([GPL191X._dummy] * 2),
            GPL191X._sty_zp_x,
            GPL191X._sta_zp_x,
            GPL191X._stx_zp_y,
            GPL191X._dummy,
            GPL191X._tya,
            GPL191X._sta_abs_y,
            GPL191X._txs,
            *([GPL191X._dummy] * 2),
            GPL191X._sta_abs_x,
            *([GPL191X._dummy] * 2),
            GPL191X._ldy_imm,
            GPL191X._lda_ind_x,
            GPL191X._ldx_imm,
            GPL191X._dummy,
            GPL191X._ldy_zp,
            GPL191X._lda_zp,
            GPL191X._ldx_zp,
            GPL191X._dummy,
            GPL191X._tay,
            GPL191X._lda_imm,
            GPL191X._tax,
            GPL191X._dummy,
            GPL191X._ldy_abs,
            GPL191X._lda_abs,
            GPL191X._ldx_abs,
            GPL191X._dummy,
            GPL191X._bcs,
            GPL191X._lda_ind_y,
            *([GPL191X._dummy] * 2),
            GPL191X._ldy_zp_x,
            GPL191X._lda_zp_x,
            GPL191X._ldx_zp_y,
            GPL191X._dummy,
            GPL191X._clv,
            GPL191X._lda_abs_y,
            GPL191X._tsx,
            GPL191X._dummy,
            GPL191X._ldy_abs_x,
            GPL191X._lda_abs_x,
            GPL191X._ldx_abs_y,
            GPL191X._dummy,
            GPL191X._cpy_imm,
            GPL191X._cmp_ind_x,
            *([GPL191X._dummy] * 2),
            GPL191X._cpy_zp,
            GPL191X._cmp_zp,
            GPL191X._dec_zp,
            GPL191X._dummy,
            GPL191X._iny,
            GPL191X._cmp_imm,
            GPL191X._dex,
            GPL191X._dummy,
            GPL191X._cpy_abs,
            GPL191X._cmp_abs,
            GPL191X._dec_abs,
            GPL191X._dummy,
            GPL191X._bne,
            GPL191X._cmp_ind_y,
            *([GPL191X._dummy] * 3),
            GPL191X._cmp_zp_x,
            GPL191X._dec_zp_x,
            GPL191X._dummy,
            GPL191X._cld,
            GPL191X._cmp_abs_y,
            *([GPL191X._dummy] * 3),
            GPL191X._cmp_abs_x,
            GPL191X._dec_abs_x,
            GPL191X._dummy,
            GPL191X._cpx_imm,
            GPL191X._sbc_ind_x,
            *([GPL191X._dummy] * 2),
            GPL191X._cpx_zp,
            GPL191X._sbc_zp,
            GPL191X._inc_zp,
            GPL191X._dummy,
            GPL191X._inx,
            GPL191X._sbc_imm,
            GPL191X._nop,
            GPL191X._dummy,
            GPL191X._cpx_abs,
            GPL191X._sbc_abs,
            GPL191X._inc_abs,
            GPL191X._dummy,
            GPL191X._beq,
            GPL191X._sbc_ind_y,
            *([GPL191X._dummy] * 3),
            GPL191X._sbc_zp_x,
            GPL191X._inc_zp_x,
            GPL191X._dummy,
            GPL191X._sed,
            GPL191X._sbc_abs_y,
            *([GPL191X._dummy] * 3),
            GPL191X._sbc_abs_x,
            GPL191X._inc_abs_x,
            GPL191X._dummy
        )

    def _open_rom(self, path):
        if (path != None):
            try:
                with open(path, "rb") as bin_f:
                    self._mem = bytearray(bin_f.read())
                    self._mem_size = len(self._mem)
            except FileNotFoundError as e:
                raise FileNotFoundError(e.errno, "ROM file not found, please add the required ROM to this path", e.filename)

    def _get_rom_addr(self, addr):
        return (addr & 0x7FFF) | (self._BANK * (addr & 0x8000))
    
    def examine(self):
        return {
            "PC": self._get_rom_addr(self._PC),
            "PC16": self._PC,
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
            "RAM": self._mem[CPU_RAM_OFFSET:CPU_RAM_OFFSET+RAM_SIZE],
            "LCDRAM": self._mem[DPRAM_OFFSET:DPRAM_OFFSET+DPRAM_SIZE],
            "SFR": (
                0, self._PDIR["CD"],
                0, self._PDIR["AB"],
                self._port_read("AB"), self._PLATCH["AB"],
                self._port_read("CD"), self._PLATCH["CD"],
                self._port_read("EF"), self._PLATCH["EF"],
                -1, self._PDIR["EF"],
                self._BANK, self._BANK,
                self._WAKEUPREQ, self._WAKEUP_CTRL,
                -1, self._ENTER_SLEEP,
                self._T64HZ & 0xFF, self._TIME_BASE,
                -1, self._TIMER_CTRL,
                -1, self._CLK32K_ENABLE,
                self._IREQ, self._INT_CTRL,
                -1, self._AUDIO_CH0_DATA,
                -1, self._AUDIO_CH1_DATA,
                int(self._TM1) & 0xFF, self._TM1_PRELOAD & 0xFF,
                int(self._TM1) >> 8, self._TM1_PRELOAD >> 8,
                -1, self._TM1_LOAD,
                int(self._TM0) & 0xFF, self._TM0_PRELOAD & 0xFF,
                int(self._TM0) >> 8, self._TM0_PRELOAD >> 8,
                -1, self._TM0_LOAD,
                -1, self._INT_CLEAR,
                -1, self._NMI_CTRL,
                -1, self._AUDIO_CH0_CTRL,
                -1, self._AUDIO_CH1_CTRL,
                -1, self._CLK_CPU_CTRL,
                -1, self._LCD_CTRL
            )
        }

    def edit_state(self, state):
        if ("PC16" in state):
            self._BANK = (state["PC16"] >> 15) & 0x3
            self._PC = state["PC16"] & 0x7FFF
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
                self._mem[(CPU_RAM_OFFSET + i) % self._mem_size] = value & 0xFF
        if ("LCDRAM" in state):
            for i, value in state["LCDRAM"].items():
                if (i < DPRAM_SIZE):
                    self._mem[(DPRAM_OFFSET + i) % self._mem_size] = value & 0xFF
        if ("SFR" in state):
            for i, value in state["SFR"].items():
                if (i < len(self._sfr_tbl)) and (i % 2):
                    list(self._sfr_tbl.values())[i // 2][1](self, value & 0xFF)

    def reset(self):
        self._TM0_counter = 0
        self._TM0_div = 0
        self._TM1_counter = 0
        self._TM1_div = 0
        self._T64HZ_counter = 0
        self._T64HZ = 0
        self._T128HZ_counter = 0
        self._T2K_counter = 0
        self._TM0 = 0
        self._TM0_PRELOAD = 0
        self._TM0_LOAD = 0
        self._TM1 = 0
        self._TM1_PRELOAD = 0
        self._TM1_LOAD = 0

        self._PC = 0
        self._A = 0
        self._X = 0
        self._Y = 0
        self._SP = 0
        
        self._set_ps(0x04)

        self._CPU_ENBL = 1

        self._BANK = 0
        self._WAKEUP_CTRL = 0
        self._WAKEUPREQ = 0
        self._ENTER_SLEEP = 0
        self._TIME_BASE = 0
        self._TIMER_CTRL = 0
        self._CLK_CPU_CTRL = 0
        self._CPU_DIV = SFR_CPU_DIV_DEFAULT
        self._CLK32K_ENABLE = 0x80

        self._PDIR = {
            "AB": 0,
            "CD": 0,
            "EF": 0,
        }

        self._PLATCH = {
            "AB": 0,
            "CD": 0,
            "EF": 0,
        }

        self._IO_CTRL = 0
        self._INT_CTRL = 0
        self._INT_CLEAR = 0
        self._IREQ = 0
        self._NMI_CTRL = 0
        self._AUDIO_CH0_CTRL = 0
        self._AUDIO_CH0_DATA = 0
        self._AUDIO_CH1_CTRL = 0
        self._AUDIO_CH1_DATA = 0
        self._LCD_CTRL = 0

        self._PC = (self._mem[(VADDR_RESET + 1) % self._mem_size] << 8) | self._mem[VADDR_RESET % self._mem_size]

    def pc(self):
        return self._get_rom_addr(self._PC)
    
    def get_VRAM(self):
        if (self._CLK32K_ENABLE and (self._LCD_CTRL & SFR_LCD_CTRL_ON)):
            return tuple(self._mem[DPRAM_OFFSET:DPRAM_OFFSET+DPRAM_SIZE])
        return tuple([0x00] * DPRAM_SIZE)

    def get_ROM(self):
        return self._mem
    
    def istr_counter(self):
        return self._instr_counter

    def _port_read(self, port):
        return (
            (~self._PDIR[port] & (self._port_input[port][1] | (self._pullup_ext[port] & ~self._port_input[port][0]))) |
            (self._PDIR[port] & self._PLATCH[port])
            ) & 0xFF

    def pin_handler(self, port, mask, level):
        if (port == 'RES'):
            if (level == 0):
                self.reset()
        else:
            prev_port = self._port_read(port)
            self._port_input[port][0] &= ~mask
            self._port_input[port][1] &= ~mask
            if (level >= 0):
                self._port_input[port][level] |= mask
            
            if ((port == "CD") and (mask & 0x02)):
                if ((prev_port & 0x02) > (self._port_read(port) & 0x02)):
                    self._IREQ |= SFR_INT_CTRL_EXT
                self._update_timers_div()
            if (port == "EF"):
                if (self._port_read(port) & mask):
                    self._WAKEUPREQ |= SFR_WAKEUP_CTRL_EXT & self._WAKEUP_CTRL

    def _IRQ(self):
        self._write_mem(self._SP | SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP | SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP | SP, self._get_ps())
        self._SP = (self._SP - 1) & 0xFF
        self._IF = 1
        addr = VADDR_IRQ | self._BANK * (self._PC & 0x8000)
        self._PC = (self._mem[(addr + 1) % self._mem_size] << 8) | self._mem[addr % self._mem_size]

    def _NMI(self):
        if (self._CPU_ENBL):
            self._write_mem(self._SP | SP, self._PC >> 8)
            self._SP = (self._SP - 1) & 0xFF
            self._write_mem(self._SP | SP, self._PC & 0xFF)
            self._SP = (self._SP - 1) & 0xFF
            self._write_mem(self._SP | SP, self._get_ps())
            self._SP = (self._SP - 1) & 0xFF
            addr = VADDR_NMI | self._BANK * (self._PC & 0x8000)
            self._PC = (self._mem[(addr + 1) % self._mem_size] << 8) | self._mem[addr % self._mem_size]

    def _update_audio_div(self):
        if (self._TIMER_CTRL & SFR_TIMER_CTRL_ENABLE and self._AUDIO_CH0_CTRL & SFR_AUDIO_CTRL_AUDIO_ENBL 
            and self._AUDIO_CH0_CTRL & SFR_AUDIO_CTRL_TONE_MODE):
            div = self._TM0_div * (0x10000 - self._TM0_PRELOAD) * 2
            self._sound.tone(0, div)
        else:
            self._sound.stop(0)
        
        if (self._TIMER_CTRL & SFR_TIMER_CTRL_ENABLE and self._AUDIO_CH1_CTRL & SFR_AUDIO_CTRL_AUDIO_ENBL 
             and self._AUDIO_CH1_CTRL & SFR_AUDIO_CTRL_TONE_MODE):
            div = self._TM1_div * (0x10000 - self._TM1_PRELOAD) * 2
            self._sound.tone(1, div)
        else:
            self._sound.stop(1)

    def _update_timers_div(self):
        if (self._TIMER_CTRL & SFR_TIMER_CTRL_TM1_32K):
            self._TM1_div = self._sub_clock_div
        else:
            self._TM1_div = 1

        self._TM0_div = 0
        if (self._TIMER_CTRL & SFR_TIMER_CTRL_TM0_COUNTER_MODE):
            srcB = self._TIMER_CTRL & SFR_TIMER_CTRL_CNT0_SRCB_MASK
            srcA = self._TIMER_CTRL & SFR_TIMER_CTRL_CNT0_SRCA_MASK

            if (srcA == SFR_TIMER_CTRL_CNT0_SRCA_CLK32):
                if (srcB == SFR_TIMER_CTRL_CNT0_SRCB_VDD):
                    self._TM0_div = self._sub_clock_div
                elif (srcB == SFR_TIMER_CTRL_CNT0_SRCB_TIMEBASEH):
                    time_base_h = self._TIME_BASE & SFR_TIMEBASE_H_MASK
                    self._TM0_div = self._sub_clock_div * (SUB_CLOCK // 64) * (SFR_TIMEBASE_H_TBL[time_base_h])
                elif (srcB == SFR_TIMER_CTRL_CNT0_SRCB_CLK128):
                    self._TM0_div = self._sub_clock_div * (SUB_CLOCK // 128)
                elif (self._port_read("CD") & 0x02):
                        self._TM0_div = self._sub_clock_div
            elif (srcA == SFR_TIMER_CTRL_CNT0_SRCA_ROSC):
                if (srcB == SFR_TIMER_CTRL_CNT0_SRCB_VDD):
                    self._TM0_div = 1
                elif (srcB == SFR_TIMER_CTRL_CNT0_SRCB_TIMEBASEH):
                    time_base_h = self._TIME_BASE & SFR_TIMEBASE_H_MASK
                    self._TM0_div = (SUB_CLOCK // 64) * (SFR_TIMEBASE_H_TBL[time_base_h])
                elif (srcB == SFR_TIMER_CTRL_CNT0_SRCB_CLK128):
                    self._TM0_div = (SUB_CLOCK // 128)
                elif (self._port_read("CD") & 0x02):
                        self._TM0_div = 1
            elif (srcA == SFR_TIMER_CTRL_CNT0_SRCA_VDD):
                if (srcB == SFR_TIMER_CTRL_CNT0_SRCB_TIMEBASEH):
                    time_base_h = self._TIME_BASE & SFR_TIMEBASE_H_MASK
                    self._TM0_div = (SUB_CLOCK // 64) * (SFR_TIMEBASE_H_TBL[time_base_h])
                elif (srcB == SFR_TIMER_CTRL_CNT0_SRCB_CLK128):
                    self._TM0_div = (SUB_CLOCK // 128)
            elif (self._port_read("CD") & 0x01):
                if (srcB == SFR_TIMER_CTRL_CNT0_SRCB_TIMEBASEH):
                    time_base_h = self._TIME_BASE & SFR_TIMEBASE_H_MASK
                    self._TM0_div = (SUB_CLOCK // 64) * (SFR_TIMEBASE_H_TBL[time_base_h])
                elif (srcB == SFR_TIMER_CTRL_CNT0_SRCB_CLK128):
                    self._TM0_div = (SUB_CLOCK // 128)

        else:
            if (self._TIMER_CTRL & SFR_TIMER_CTRL_TM0_TIMER1):
                self._TM0_div = self._TM1_div * (0x10000 - self._TM1_PRELOAD)
            else:
                self._TM0_div = 1

        self._update_audio_div()

    def _timers_clock(self, exec_cycles):
        if (self._TIMER_CTRL & SFR_TIMER_CTRL_ENABLE):
            if (self._TM0_div):
                self._TM0_counter -= exec_cycles
                while (self._TM0_counter <= 0):
                    self._TM0_counter += self._TM0_div
                    self._TM0 += 1

                    if (self._TM0 > 0xFFFF):
                        self._TM0 = self._TM0_PRELOAD
                        self._IREQ |= SFR_INT_CTRL_TIMER0
                        self._WAKEUPREQ |= SFR_WAKEUP_CTRL_TIMER0 & self._WAKEUP_CTRL

            self._TM1_counter -= exec_cycles
            while (self._TM1_counter <= 0):
                self._TM1_counter += self._TM1_div
                self._TM1 += 1

                if (self._TM1 > 0xFFFF):
                    self._TM1 = self._TM1_PRELOAD

                    if not(self._NMI_CTRL & SFR_NMI_CTRL_TIMER1):
                        self._NMI()
                    else:
                        self._IREQ |= SFR_INT_CTRL_TIMER1

        self._T64HZ_counter -= exec_cycles
        while (self._T64HZ_counter <= 0):
            self._T64HZ_counter += self._sub_clock_div * (SUB_CLOCK // 64)
            self._T64HZ += 1
            
            time_base_h = self._TIME_BASE & SFR_TIMEBASE_H_MASK
            if (not(self._T64HZ & SFR_TIMEBASE_H_TBL[time_base_h])):
                self._IREQ |= SFR_INT_CTRL_TIME_BASEH
                self._WAKEUPREQ |= SFR_WAKEUP_CTRL_TIME_BASEH & self._WAKEUP_CTRL

            time_base_l = (self._TIME_BASE & SFR_TIMEBASE_L_MASK) >> SFR_TIMEBASE_L_SHIFT
            if (not(self._T64HZ & SFR_TIMEBASE_L_TBL[time_base_l])):
                self._IREQ |= SFR_INT_CTRL_TIME_BASEL
                self._WAKEUPREQ |= SFR_WAKEUP_CTRL_TIME_BASEL & self._WAKEUP_CTRL

        self._T128HZ_counter -= exec_cycles
        while (self._T128HZ_counter <= 0):
            self._T128HZ_counter += self._sub_clock_div * (SUB_CLOCK // 128)
            self._IREQ |= SFR_INT_CTRL_CLK128

        self._T2K_counter -= exec_cycles
        while (self._T2K_counter <= 0):
            self._T2K_counter += self._sub_clock_div * (SUB_CLOCK // 2048)
            self._IREQ |= SFR_INT_CTRL_CLK2K
                
    def clock(self):
        if (self._CPU_ENBL):
            pc = self._PC
            self._PC = (pc + 1) & 0xFFFF
            opcode = self._mem[(pc & 0x7FFF | self._BANK * (pc & 0x8000)) % self._mem_size]
            exec_cycles = self._execute[opcode](self) * self._CPU_DIV
            self._instr_counter += 1
            self._timers_clock(exec_cycles)
            if ((not self._IF) and (self._IREQ & self._INT_CTRL)):
                self._IRQ()
        else:
            exec_cycles = self._sub_clock_div
            if (self._WAKEUP_CTRL & self._WAKEUPREQ):
                self._CPU_ENBL = 1
                self._CPU_DIV = SFR_CPU_DIV_DEFAULT
            if (self._CLK32K_ENABLE):
                self._timers_clock(exec_cycles)

        return exec_cycles
    
    def _set_sfr_io_portAB_dir(self, value):
        self._PDIR["AB"] = value
        self._interconnect.emit_port(self, "AB", self._port_read("AB"))

    def _get_sfr_io_portAB_data(self):
        return self._port_read("AB")
    
    def _set_sfr_io_portAB_data(self, value):
        self._PLATCH["AB"] = value
        self._interconnect.emit_port(self, "AB", self._port_read("AB"))
    
    def _set_sfr_io_portCD_dir(self, value):
        self._PDIR["CD"] = value
        self._interconnect.emit_port(self, "CD", self._port_read("CD"))
        self._update_timers_div()

    def _get_sfr_io_portCD_data(self):
        return self._port_read("CD")
    
    def _set_sfr_io_portCD_data(self, value):
        self._PLATCH["CD"] = value
        self._interconnect.emit_port(self, "CD", self._port_read("CD"))
        self._update_timers_div()
    
    def _set_sfr_io_portEF_dir(self, value):
        self._PDIR["EF"] = value & 0xFE
        #TODO: In the Tamagotchi Mini 2017, EF dir is set to 1, although EF.0 is used for the button. 
        # Perhaps the port direction is set more complexly than bit-by-bit, or there's an error somewhere.
        self._interconnect.emit_port(self, "EF", self._port_read("EF"))

    def _get_sfr_io_portEF_data(self):
        return self._port_read("EF")
    
    def _set_sfr_io_portEF_data(self, value):
        self._PLATCH["EF"] = value
        self._interconnect.emit_port(self, "EF", self._port_read("EF"))

    def _get_sfr_audio_ch0_ctrl(self):
        return self._AUDIO_CH0_CTRL

    def _set_sfr_audio_ch0_ctrl(self, value):
        self._AUDIO_CH0_CTRL = value
        self._update_audio_div()

    def _get_sfr_audio_ch0_data(self):
        return 0

    def _set_sfr_audio_ch0_data(self, value):
        self._AUDIO_CH0_DATA = value
        self._sound.set_data(0, self._AUDIO_CH0_CTRL, value)
        self._update_audio_div()

    def _get_sfr_audio_ch1_ctrl(self):
        return self._AUDIO_CH1_CTRL

    def _set_sfr_audio_ch1_ctrl(self, value):
        self._AUDIO_CH1_CTRL = value
        self._update_audio_div()

    def _get_sfr_audio_ch1_data(self):
        return 0

    def _set_sfr_audio_ch1_data(self, value):
        self._AUDIO_CH1_DATA = value
        self._sound.set_data(1, self._AUDIO_CH1_CTRL, value)
        self._update_audio_div()

    def _get_sfr_bank_sel(self):
        return self._BANK
    
    def _set_sfr_bank_sel(self, value):
        self._BANK = (value & 0x03)

    def _get_sfr_wakeup_ctrl(self):
        return self._WAKEUPREQ
    
    def _set_sfr_wakeup_ctrl(self, value):
        self._WAKEUP_CTRL = value
        self._WAKEUPREQ &= value

    def _get_sfr_timer_timebase_sel(self):
        return self._T64HZ & 0xFF
    
    def _set_sfr_timer_timebase_sel(self, value):
        self._TIME_BASE = value
        self._update_timers_div()
    
    def _set_sfr_timer_ctrl(self, value):
        self._TIMER_CTRL = value
        self._update_timers_div()
    
    def _set_sfr_clk_32768_en(self, value):
        self._CLK32K_ENABLE = value
    
    def _set_sfr_nmi_ctrl(self, value):
        self._NMI_CTRL = value

    def _get_sfr_int_ctrl(self):
        return self._IREQ
    
    def _set_sfr_int_ctrl(self, value):
        self._INT_CTRL = value
        self._IREQ = 0
    
    def _set_sfr_enter_sleep(self, value):
        self._ENTER_SLEEP = value
        self._CPU_ENBL = 0
    
    def _set_sfr_clk_cpu_ctrl(self, value):
        self._CLK_CPU_CTRL = value
        self._CPU_DIV = 2 << (value & 0x3)

    def _set_sfr_clk_int_clear(self, value):
        self._INT_CLEAR = value
        self._IREQ &= ~value

    def _get_sfr_timer_TM1L(self):
        return int(self._TM1) & 0xFF

    def _set_sfr_timer_TM1L(self, value):
        self._TM1_PRELOAD = (self._TM1_PRELOAD & 0xFF00) | value

    def _get_sfr_timer_TM1H(self):
        return int(self._TM1) >> 8

    def _set_sfr_timer_TM1H(self, value):
        self._TM1_PRELOAD = (self._TM1_PRELOAD & 0xFF) | (value << 8)
        self._TM1 = self._TM1_PRELOAD

    def _set_sfr_timer_TM1Load_Ctrl(self, value):
        self._TM1_LOAD = value

    def _get_sfr_timer_TM0L(self):
        return int(self._TM0) & 0xFF

    def _set_sfr_timer_TM0L(self, value):
        self._TM0_PRELOAD = (self._TM0_PRELOAD & 0xFF00) | value

    def _get_sfr_timer_TM0H(self):
        return int(self._TM0) >> 8

    def _set_sfr_timer_TM0H(self, value):
        self._TM0_PRELOAD = (self._TM0_PRELOAD & 0xFF) | (value << 8)
        self._TM0 = self._TM0_PRELOAD

    def _set_sfr_timer_TM0Load_Ctrl(self, value):
        self._TM0_LOAD = value

    def _get_sfr_lcd_ctrl(self):
        return self._LCD_CTRL
    
    def _set_sfr_lcd_ctrl(self, value):   
        self._LCD_CTRL = value

    def _get_sfr_dummy(self):
        return 0
    
    def _set_sfr_dummy(self, value):
        pass
    
    def _write_mem(self, addr, value):
        if ((addr >= CPU_RAM_OFFSET) and (addr < DPRAM_SIZE + DPRAM_OFFSET)):
            self._mem[addr % self._mem_size] = value
        else:
            io = self._sfr_tbl.get(addr)
            if (io != None):
                io[1](self, value)

    def _read_mem(self, addr):
        if (addr >= CPU_RAM_OFFSET):
            return self._mem[(addr & 0x7FFF | self._BANK * (addr & 0x8000)) % self._mem_size]
        else:
            io = self._sfr_tbl.get(addr)
            if (io != None):
                return io[0](self)
            return 0
    
    def _get_ps(self):
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
        self._write_mem(self._SP | SP, self._get_ps())
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

    def _and_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._A &= self._read_mem(addr)
        self._PC = (self._PC + 1) & 0xFFFF
        self._NF = self._A >> 7
        self._ZF = not self._A
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
        self._write_mem(self._SP | SP, pc >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP | SP, pc & 0xFF)
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
        self._set_ps(self._read_mem(self._SP | SP))
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
        self._set_ps(self._read_mem(self._SP | SP))
        self._SP = (self._SP + 1) & 0xFF
        self._PC = self._read_mem(self._SP | SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SP | SP) << 8
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
        self._write_mem(self._SP | SP, self._A)
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
        self._PC = self._read_mem(self._SP | SP)
        self._SP = (self._SP + 1) & 0xFF
        self._PC |= self._read_mem(self._SP | SP) << 8
        self._PC += 1
        return 6
    
    def _adc_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._adc(self._read_mem(addr))
        self._PC = (self._PC + 1) & 0xFFFF
        return 6

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
        self._A = self._read_mem(self._SP | SP)
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

    def _sta_ind_x(self):
        zp = self._read_mem(self._PC) + self._X
        addr = self._read_mem(zp & 0xFF) | (self._read_mem((zp + 1) & 0xFF) << 8)
        self._write_mem(addr, self._A)
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
    
    def _sta_abs_x(self):
        base = self._read_mem(self._PC) | (self._read_mem((self._PC + 1) & 0xFFFF) << 8)
        addr = (base + self._X) & 0xFFFF
        self._write_mem(addr, self._A)
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
        print("illegal instruction %0.5X" % self._get_rom_addr(self._PC))
        return 2
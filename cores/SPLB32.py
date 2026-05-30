from .rom import ROM
from .SPLB32sound import SPLB32sound

SUB_CLOCK = 32768

SP = 0x100

VADDR_NMI = 0x7FFA
VADDR_RESET = 0x7FFC
VADDR_IRQ = 0x7FFE

SFR_IO_PORTD_MASK = 0x3F

SFR_TIMER_CTRL_ENABLE = 0x80
SFR_TIMER_CTRL_COUNTER_MODE = 0x10

SFR_TIMER_CTRL_TM0_MASK = 0x60
SFR_TIMER_CTRL_TM0_STOP = 0x00
SFR_TIMER_CTRL_TM0_SYS = 0x20
SFR_TIMER_CTRL_TM0_32K = 0x40
SFR_TIMER_CTRL_TM0_EXT = 0x60

SFR_TIMER_CTRL_TM1_MASK = 0x03
SFR_TIMER_CTRL_TM1_STOP = 0x00
SFR_TIMER_CTRL_TM1_SYS = 0x01
SFR_TIMER_CTRL_TM1_32K = 0x02
SFR_TIMER_CTRL_TM1_TM0 = 0x03

SFR_WAKEUP_CTRL_EXT = 0x01
SFR_WAKEUP_CTRL_TIME_BASEL = 0x02
SFR_WAKEUP_CTRL_TIMER0 = 0x04
SFR_WAKEUP_CTRL_TIME_BASEH = 0x08
SFR_WAKEUP_CTRL_TIMER1 = 0x10
SFR_WAKEUP_CTRL_UART_RX = 0x20

SFR_INT_CTRL_EXT = 0x01
SFR_INT_CTRL_TIME_BASEL = 0x04
SFR_INT_CTRL_TIME_BASEH = 0x08
SFR_INT_CTRL_TIMER0 = 0x10
SFR_INT_CTRL_TIMER1 = 0x20
SFR_INT_CTRL_UART_TX = 0x40
SFR_INT_CTRL_UART_RX = 0x80

SFR_NMI_CTRL_LV_DETECT = 0x01
SFR_NMI_CTRL_TIMER1 = 0x02
SFR_NMI_CTRL_ENABLE = 0x80

SFR_TIMEBASE_L_MASK = 0x0C
SFR_TIMEBASE_L_16 = 0x0C
SFR_TIMEBASE_L_8 = 0x04
SFR_TIMEBASE_L_4 = 0x08
SFR_TIMEBASE_L_2 = 0x00
SFR_TIMEBASE_L_SHIFT = 2

SFR_TIMEBASE_H_MASK = 0x03
SFR_TIMEBASE_H_128 = 0x00
SFR_TIMEBASE_H_256 = 0x02
SFR_TIMEBASE_H_512 = 0x01
SFR_TIMEBASE_H_1024 = 0x03

SFR_TIMEBASE_H_TBL = (0x07, 0x01, 0x03, 0x00)
SFR_TIMEBASE_L_TBL = (0x1FF, 0x7F, 0xFF, 0x3F)

SFR_AUDIO_CTRL_TONE_MODE = 0x40
SFR_AUDIO_CTRL_PWM_ENBL = 0x80
SFR_AUDIO_CTRL_TM0_OVFLW = 0x08
SFR_AUDIO_CTRL_TM1_OVFLW = 0x10
SFR_AUDIO_CTRL_TM01_OVFLW = 0x18

SFR_CLK32768_ENABLE = 0x80

SFR_CPU_CTRL_DEFAULT = 0x02

SFR_LCD_CTRL1_STATE = 0x0D
SFR_LCD_CTRL1_ENBL = 0x01
SFR_LCD_CTRL1_ALL_ON = 0x04
SFR_LCD_CTRL1_ALL_OFF = 0x08

SFR_OFFSET = 0x0
SFR_SIZE = 0x40
CPU_RAM_OFFSET = 0x40
RAM_SIZE = 0x4C0
DPRAM_OFFSET = 0x3E00
DPRAM_SIZE = 0x200

ROM_BANK_0_OFFSET = 0xC000
ROM_BANK_LH_OFFSET = 0x4000
    
class SPLB32():
    def __init__(self, mask, clock, interconnect):
        self._interconnect = interconnect
        self._interconnect.register_port_device(self)

        self._ROM = ROM(mask['rom_path'])

        self._instr_counter = 0

        self._pullup_ext = {
            **{"PD": 0, "PC": 0, "PB": 0, "PA": 0},
            **mask['port_pullup']
        }

        self._port_input = {
            "PD": [0, 0],
            "PC": [0, 0],
            "PB": [0, 0],
            "PA": [0, 0],
        }

        self._clock = clock
        self._sub_clock_div = clock / SUB_CLOCK

        self._sound = SPLB32sound(interconnect)
        
        self.reset()

        self._sfr_tbl = {
            0x00: (SPLB32._get_sfr_bank_sel, SPLB32._set_sfr_bank_sel), #P_BANK_Sel

            0x04: (SPLB32._get_sfr_clk_cpu_ctrl, SPLB32._set_sfr_clk_cpu_ctrl), #P_CLK_CPU_Ctrl
            0x0E: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_clk_32768_en), #P_CLK_32768_En

            #0x05: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SFR_IO_PORTA_Strobe_En
            0x06: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_io_portA_attr), #to-do P_SFR_IO_PORTA_Attrib
            0x07: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_io_portA_dir), #P_IO_PortA_Dir
            0x08: (SPLB32._get_sfr_io_portA_data, SPLB32._set_sfr_io_portA_data), #P_IO_PortA_Data     

            0x28: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_io_portB_attr), #to-do P_SFR_IO_PORTB_Attrib
            0x29: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_io_portB_dir), #P_IO_PortB_Dir
            0x0A: (SPLB32._get_sfr_io_portB_data, SPLB32._set_sfr_io_portB_data), #P_IO_PortB_Data

            0x2A: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_io_portC_attr), #to-do P_SFR_IO_PORTC_Attrib
            0x2B: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_io_portC_dir), #P_IO_PortC_Dir
            0x0B: (SPLB32._get_sfr_io_portC_data, SPLB32._set_sfr_io_portC_data), #P_IO_PortC_Data

            0x2C: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_io_portD_attr), #to-do P_SFR_IO_PORTD_Attrib
            0x2D: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_io_portD_dir), #P_IO_PortD_Dir
            0x09: (SPLB32._get_sfr_io_portD_data, SPLB32._set_sfr_io_portD_data), #P_IO_PortD_Data

            0x27: (SPLB32._get_sfr_specialfunc_config, SPLB32._set_sfr_specialfunc_config), #P_IO_SpecialFunc_Config

            0x24: (SPLB32._get_sfr_lcd_ctrl1, SPLB32._set_sfr_lcd_ctrl1), #P_LCD_Ctrl1
            #0x25: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #P_LCD_PUMP_Ctrl
            #0x26: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #P_LCD_VLCD_Ctrl

            0x01: (SPLB32._get_sfr_int_ctrl, SPLB32._set_sfr_int_ctrl), #P_INT_Ctrl
            0x02: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_clk_int_clear), #P_INT_Clear
            0x38: (SPLB32._get_sfr_nmi_ctrl, SPLB32._set_sfr_nmi_ctrl), #P_NMI_Ctrl

            0x18: (SPLB32._get_sfr_wakeup_ctrl, SPLB32._set_sfr_wakeup_ctrl), #P_WAKEUP_Ctrl

            0x0C: (SPLB32._get_sfr_timer_timebase_sel, SPLB32._set_sfr_timer_timebase_sel), #P_TIMER_TimeBase_Sel
            0x0F: (SPLB32._get_sfr_timer_ctrl, SPLB32._set_sfr_timer_ctrl), #P_TIMER_Timer_Ctrl
            0x10: (SPLB32._get_sfr_timer_TM0L, SPLB32._set_sfr_timer_TM0L), #P_TIMER_TM0Data_LB
            0x11: (SPLB32._get_sfr_timer_TM0H, SPLB32._set_sfr_timer_TM0H), #P_TIMER_TM0Data_HB
            0x14: (SPLB32._get_sfr_timer_TM1L, SPLB32._set_sfr_timer_TM1L), #P_TIMER_TM1Data_LB
            0x15: (SPLB32._get_sfr_timer_TM1H, SPLB32._set_sfr_timer_TM1H), #P_TIMER_TM1Data_HB

            #0x3A: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_KEYSCAN_Ctrl
            #0x3B: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_KEYSCAN_Port1_Data
            #0x3C: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_KEYSCAN_Port2_Data

            0x3E: (SPLB32._get_sfr_aux_byte_mirror, SPLB32._set_sfr_aux_byte_mirror), #P_AUX_Byte_Mirror
            0x3F: (SPLB32._get_sfr_aux_nibble_swap, SPLB32._set_sfr_aux_nibble_swap), #P_AUX_Nibble_Swap

            #0x3031: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do #P_WDT_Flag_Clear

            #0x39: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_LVD_Ctrl

            0x12: (SPLB32._get_sfr_audio_ch0_ctrl, SPLB32._set_sfr_audio_ch0_ctrl), #P_AUDIO_Ch0_Ctrl
            0x13: (SPLB32._get_sfr_audio_ch0_data, SPLB32._set_sfr_audio_ch0_data), #P_AUDIO_Ch0_Data
            0x16: (SPLB32._get_sfr_audio_ch1_ctrl, SPLB32._set_sfr_audio_ch1_ctrl), #P_AUDIO_Ch1_Ctrl
            0x17: (SPLB32._get_sfr_audio_ch1_data, SPLB32._set_sfr_audio_ch1_data), #P_AUDIO_Ch1_Data

            #0x19: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_UART_Ctrl1
            #0x1A: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_UART_Ctrl2
            #0x1B: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_UART_Data
            #0x1C: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_UART_BaudScalar_LB
            #0x1D: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_UART_BaudScalar_HB
            #0x1E: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_UART_BaudRate_LB
            #0x1F: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_UART_BaudRate_HB

            #0x0B: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SSRAM_SDA_SCK
            #0x30: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SSRAM_Data
            #0x31: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SSRAM_Addr1
            #0x32: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SSRAM_Addr2
            #0x33: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SSRAM_Addr3
            #0x34: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SSRAM_Ctrl
            #0x35: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SSRAM_Start
            #0x36: (SPLB32._get_sfr_dummy, SPLB32._set_sfr_dummy), #to-do P_SSRAM_Stop
        }

        self._execute = (
            SPLB32._brk,
            SPLB32._ora_ind_x,
            *([SPLB32._dummy] * 3),
            SPLB32._ora_zp,
            SPLB32._asl_zp,
            SPLB32._dummy,
            SPLB32._php,
            SPLB32._ora_imm,
            SPLB32._asl_a,
            *([SPLB32._dummy] * 2),
            SPLB32._ora_abs,
            SPLB32._asl_abs,
            SPLB32._dummy,
            SPLB32._bpl,
            SPLB32._ora_ind_y,
            *([SPLB32._dummy] * 3),
            SPLB32._ora_zp_x,
            SPLB32._asl_zp_x,
            SPLB32._dummy,
            SPLB32._clc,
            SPLB32._ora_abs_y,
            *([SPLB32._dummy] * 3),
            SPLB32._ora_abs_x,
            SPLB32._asl_abs_x,
            SPLB32._dummy,
            SPLB32._jsr_abs,
            SPLB32._and_ind_x,
            *([SPLB32._dummy] * 2),
            SPLB32._bit_zp,
            SPLB32._and_zp,
            SPLB32._rol_zp,
            SPLB32._dummy,
            SPLB32._plp,
            SPLB32._and_imm,
            SPLB32._rol_a,
            SPLB32._dummy,
            SPLB32._bit_abs,
            SPLB32._and_abs,
            SPLB32._rol_abs,
            SPLB32._dummy,
            SPLB32._bmi,
            SPLB32._and_ind_y,
            *([SPLB32._dummy] * 3),
            SPLB32._and_zp_x,
            SPLB32._rol_zp_x,
            SPLB32._dummy,
            SPLB32._sec,
            SPLB32._and_abs_y,
            *([SPLB32._dummy] * 3),
            SPLB32._and_abs_x,
            SPLB32._rol_abs_x,
            SPLB32._dummy,
            SPLB32._rti,
            SPLB32._eor_ind_x,
            *([SPLB32._dummy] * 3),
            SPLB32._eor_zp,
            SPLB32._lsr_zp,
            SPLB32._dummy,
            SPLB32._pha,
            SPLB32._eor_imm,
            SPLB32._lsr_a,
            SPLB32._dummy,
            SPLB32._jmp_abs,
            SPLB32._eor_abs,
            SPLB32._lsr_abs,
            SPLB32._dummy,
            SPLB32._bvc,
            SPLB32._eor_ind_y,
            *([SPLB32._dummy] * 3),
            SPLB32._eor_zp_x,
            SPLB32._lsr_zp_x,
            SPLB32._dummy,
            SPLB32._cli,
            SPLB32._eor_abs_y,
            *([SPLB32._dummy] * 3),
            SPLB32._eor_abs_x,
            SPLB32._lsr_abs_x,
            SPLB32._dummy,
            SPLB32._rts,
            SPLB32._adc_ind_x,
            *([SPLB32._dummy] * 3),
            SPLB32._adc_zp,
            SPLB32._ror_zp,
            SPLB32._dummy,
            SPLB32._pla,
            SPLB32._adc_imm,
            SPLB32._ror_a,
            SPLB32._dummy,
            SPLB32._jmp_ind,
            SPLB32._adc_abs,
            SPLB32._ror_abs,
            SPLB32._dummy,
            SPLB32._bvs,
            SPLB32._adc_ind_y,
            *([SPLB32._dummy] * 3),
            SPLB32._adc_zp_x,
            SPLB32._ror_zp_x,
            SPLB32._dummy,
            SPLB32._sei,
            SPLB32._adc_abs_y,
            *([SPLB32._dummy] * 3),
            SPLB32._adc_abs_x,
            SPLB32._ror_abs_x,
            *([SPLB32._dummy] * 2),
            SPLB32._sta_ind_x,
            *([SPLB32._dummy] * 2),
            SPLB32._sty_zp,
            SPLB32._sta_zp,
            SPLB32._stx_zp,
            SPLB32._dummy,
            SPLB32._dey,
            SPLB32._dummy,
            SPLB32._txa,
            SPLB32._dummy,
            SPLB32._sty_abs,
            SPLB32._sta_abs,
            SPLB32._stx_abs,
            SPLB32._dummy,
            SPLB32._bcc,
            SPLB32._sta_ind_y,
            *([SPLB32._dummy] * 2),
            SPLB32._sty_zp_x,
            SPLB32._sta_zp_x,
            SPLB32._stx_zp_y,
            SPLB32._dummy,
            SPLB32._tya,
            SPLB32._sta_abs_y,
            SPLB32._txs,
            *([SPLB32._dummy] * 2),
            SPLB32._sta_abs_x,
            *([SPLB32._dummy] * 2),
            SPLB32._ldy_imm,
            SPLB32._lda_ind_x,
            SPLB32._ldx_imm,
            SPLB32._dummy,
            SPLB32._ldy_zp,
            SPLB32._lda_zp,
            SPLB32._ldx_zp,
            SPLB32._dummy,
            SPLB32._tay,
            SPLB32._lda_imm,
            SPLB32._tax,
            SPLB32._dummy,
            SPLB32._ldy_abs,
            SPLB32._lda_abs,
            SPLB32._ldx_abs,
            SPLB32._dummy,
            SPLB32._bcs,
            SPLB32._lda_ind_y,
            *([SPLB32._dummy] * 2),
            SPLB32._ldy_zp_x,
            SPLB32._lda_zp_x,
            SPLB32._ldx_zp_y,
            SPLB32._dummy,
            SPLB32._clv,
            SPLB32._lda_abs_y,
            SPLB32._tsx,
            SPLB32._dummy,
            SPLB32._ldy_abs_x,
            SPLB32._lda_abs_x,
            SPLB32._ldx_abs_y,
            SPLB32._dummy,
            SPLB32._cpy_imm,
            SPLB32._cmp_ind_x,
            *([SPLB32._dummy] * 2),
            SPLB32._cpy_zp,
            SPLB32._cmp_zp,
            SPLB32._dec_zp,
            SPLB32._dummy,
            SPLB32._iny,
            SPLB32._cmp_imm,
            SPLB32._dex,
            SPLB32._dummy,
            SPLB32._cpy_abs,
            SPLB32._cmp_abs,
            SPLB32._dec_abs,
            SPLB32._dummy,
            SPLB32._bne,
            SPLB32._cmp_ind_y,
            *([SPLB32._dummy] * 3),
            SPLB32._cmp_zp_x,
            SPLB32._dec_zp_x,
            SPLB32._dummy,
            SPLB32._cld,
            SPLB32._cmp_abs_y,
            *([SPLB32._dummy] * 3),
            SPLB32._cmp_abs_x,
            SPLB32._dec_abs_x,
            SPLB32._dummy,
            SPLB32._cpx_imm,
            SPLB32._sbc_ind_x,
            *([SPLB32._dummy] * 2),
            SPLB32._cpx_zp,
            SPLB32._sbc_zp,
            SPLB32._inc_zp,
            SPLB32._dummy,
            SPLB32._inx,
            SPLB32._sbc_imm,
            SPLB32._nop,
            SPLB32._dummy,
            SPLB32._cpx_abs,
            SPLB32._sbc_abs,
            SPLB32._inc_abs,
            SPLB32._dummy,
            SPLB32._beq,
            SPLB32._sbc_ind_y,
            *([SPLB32._dummy] * 3),
            SPLB32._sbc_zp_x,
            SPLB32._inc_zp_x,
            SPLB32._dummy,
            SPLB32._sed,
            SPLB32._sbc_abs_y,
            *([SPLB32._dummy] * 3),
            SPLB32._sbc_abs_x,
            SPLB32._inc_abs_x,
            SPLB32._dummy
        )

    def _get_rom_addr(self, addr):
        if (addr >= 0xC000):
            return addr & 0x7FFF
        return (addr & 0x7FFF) | self._ROM_BANK
    
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
            "RAM": self._RAM,
            "LCDRAM": self._DPRAM,
            "SFR": (
                self._ROM_BANK >> 15,
                self._CPU_DIV,
                self._CLK32768_ENABLE,
                -1,
                self._ATTR["PA"],
                self._PDIR["PA"],
                self._port_read("PA"),
                self._ATTR["PB"],
                self._PDIR["PB"],
                self._port_read("PB"),
                self._ATTR["PC"],
                self._PDIR["PC"],
                self._port_read("PC"),
                self._ATTR["PD"],
                self._PDIR["PD"],
                self._port_read("PD"),
                -1,
                -1,
                -1,
                -1,
                self._INT_CTRL,
                -1,
                self._NMI_CTRL,
                self._WAKEUP_CTRL,
                self._TIME_BASE,
                self._TIMER_CTRL,
                int(self._TM0) & 0xFF,
                int(self._TM0) >> 8,
                int(self._TM1) & 0xFF,
                int(self._TM1) >> 8,
                -1,
                -1,
                -1,
                self._BYTE_MIRROR,
                self._NIBBLE_SWAP,
                -1,
                -1,
                self._AUDIO_CH0_CTRL,
                self._AUDIO_CH0_DATA,
                self._AUDIO_CH1_CTRL,
                self._AUDIO_CH1_DATA,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1
            )
        }

    def edit_state(self, state):
        if ("PC16" in state):
            self._ROM_BANK = (state["PC16"]) & 0x78000
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
                self._RAM[i] = value & 0xFF
        if ("LCDRAM" in state):
            for i, value in state["LCDRAM"].items():
                if (i < DPRAM_SIZE):
                    self._DPRAM[i] = value & 0xFF
        if ("SFR" in state):
            for i, value in state["SFR"].items():
                if i < len(self._sfr_tbl):
                    list(self._sfr_tbl.values())[i][1](self, value & 0xFF)

    def reset(self):
        self._TM0_counter = 0
        self._TM1_counter = 0
        self._T1KHZ_counter = 0
        self._T1KHZ = 0
        self._TM0 = 0
        self._TM0_RELOAD = 0
        self._TM1 = 0
        self._TM1_RELOAD = 0

        self._PC = 0
        self._A = 0
        self._X = 0
        self._Y = 0
        self._SP = 0
        
        self._set_ps(0x04)

        self._CPU_ENBL = 1

        self._RAM = [0] * RAM_SIZE
        self._DPRAM = [0] * DPRAM_SIZE

        self._ROM_BANK = 0
        self._WAKEUP_CTRL = 0
        self._WAKEUPREQ = 0
        self._TIME_BASE = 0
        self._TIMER_CTRL = 0
        self._CPU_DIV = SFR_CPU_CTRL_DEFAULT
        self._CLK32768_ENABLE = 0x80

        self._PDIR = {
            "PD": 0,
            "PC": 0,
            "PB": 0,
            "PA": 0
        }

        self._ATTR = {
            "PD": 0,
            "PC": 0,
            "PB": 0,
            "PA": 0
        }

        self._PLATCH = {
            "PD": 0,
            "PC": 0,
            "PB": 0,
            "PA": 0
        }

        self._IO_CTRL = 0
        self._INT_CTRL = 0
        self._IREQ = 0
        self._NMI_CTRL = 0
        self._NMIREQ = 0
        self._AUDIO_CH0_CTRL = 0
        self._AUDIO_CH0_DATA = 0
        self._AUDIO_CH1_CTRL = 0
        self._AUDIO_CH1_DATA = 0
        self._BYTE_MIRROR = 0
        self._NIBBLE_SWAP = 0

        self._LCD_CTRL1 = 0

        self._addr_reset = self._ROM.get_word_LSB(VADDR_RESET)
        self._addr_irq = self._ROM.get_word_LSB(VADDR_IRQ)
        self._addr_nmi = self._ROM.get_word_LSB(VADDR_NMI)

        self._PC = self._addr_reset

    def pc(self):
        return self._get_rom_addr(self._PC)
    
    def get_VRAM(self):
        if (self._CLK32768_ENABLE):
            if ((self._LCD_CTRL1 & SFR_LCD_CTRL1_STATE) == SFR_LCD_CTRL1_ENBL):
                return tuple(self._DPRAM)
            elif (self._LCD_CTRL1 & SFR_LCD_CTRL1_ALL_ON):
                return tuple([0xFF] * DPRAM_SIZE)
        return tuple([0x00] * DPRAM_SIZE)

    def get_ROM(self):
        return self._ROM
    
    def istr_counter(self):
        return self._instr_counter

    def _port_read(self, port):
        return (
            (self._PDIR[port] & self._PLATCH[port]) | 
            (~self._PDIR[port] & 
            (~self._port_input[port][0] & (self._port_input[port][1] | (~self._ATTR[port] & self._PLATCH[port]) | self._pullup_ext[port])))
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
            
            if ((port == "PC") and (mask & 0x2)):
                if ((prev_port & 0x10) > (self._port_read(port) & 0x10)):
                    self._IREQ |= SFR_INT_CTRL_EXT
            if (port == "PA"):
                if (self._port_read(port) & mask):
                    self._WAKEUPREQ |= SFR_WAKEUP_CTRL_EXT

    def _IRQ(self):
        self._write_mem(self._SP | SP, self._PC >> 8)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP | SP, self._PC & 0xFF)
        self._SP = (self._SP - 1) & 0xFF
        self._write_mem(self._SP | SP, self._get_ps())
        self._SP = (self._SP - 1) & 0xFF
        self._IF = 1
        self._PC = self._addr_irq

    def _NMI(self):
        if (self._NMI_CTRL & SFR_NMI_CTRL_ENABLE):
            if (self._CPU_ENBL):
                self._write_mem(self._SP | SP, self._PC >> 8)
                self._SP = (self._SP - 1) & 0xFF
                self._write_mem(self._SP | SP, self._PC & 0xFF)
                self._SP = (self._SP - 1) & 0xFF
                self._write_mem(self._SP | SP, self._get_ps())
                self._SP = (self._SP - 1) & 0xFF
                self._PC = self._addr_nmi

    def _timers_clock(self, exec_cycles):
        if (self._TIMER_CTRL & SFR_TIMER_CTRL_TM0_MASK):
            self._TM0_counter -= exec_cycles
            while (self._TM0_counter <= 0):
                if (self._TIMER_CTRL & SFR_TIMER_CTRL_TM0_MASK == SFR_TIMER_CTRL_TM0_SYS):
                    self._TM0_counter = 1
                    self._TM0 += exec_cycles
                elif (self._TIMER_CTRL & SFR_TIMER_CTRL_TM0_MASK == SFR_TIMER_CTRL_TM0_32K):
                    self._TM0_counter += self._sub_clock_div
                    self._TM0 += 1
                else:
                    #to-do SFR_TIMER_CTRL_TM0_EXT
                    pass

                while (self._TM0 > 0xFFFF):
                    self._TM0 -= 0x10000 - self._TM0_RELOAD
                    self._IREQ |= SFR_INT_CTRL_TIMER0
                    self._WAKEUPREQ |= SFR_WAKEUP_CTRL_TIMER0
                        
                    if (self._AUDIO_CH0_CTRL & SFR_AUDIO_CTRL_TM0_OVFLW and self._AUDIO_CH0_CTRL & SFR_AUDIO_CTRL_TONE_MODE):
                        self._sound.toggle(0)
                    if (self._AUDIO_CH1_CTRL & SFR_AUDIO_CTRL_TM0_OVFLW and self._AUDIO_CH1_CTRL & SFR_AUDIO_CTRL_TONE_MODE):
                        self._sound.toggle(1)

        if (self._TIMER_CTRL & SFR_TIMER_CTRL_TM1_MASK):
            self._TM1_counter -= exec_cycles
            while (self._TM1_counter <= 0):
                if (self._TIMER_CTRL & SFR_TIMER_CTRL_TM1_MASK == SFR_TIMER_CTRL_TM1_SYS):
                    self._TM1_counter = 1
                    self._TM1 += exec_cycles
                elif (self._TIMER_CTRL & SFR_TIMER_CTRL_TM1_MASK == SFR_TIMER_CTRL_TM1_32K):
                    self._TM1_counter += self._sub_clock_div
                    self._TM1 += 1
                else:
                    #to-do SFR_TIMER_CTRL_TM1_TM0
                    pass

                while (self._TM1 > 0xFFFF):
                    self._TM1 -= 0x10000 - self._TM1_RELOAD
                    self._IREQ |= SFR_INT_CTRL_TIMER1
                    self._WAKEUPREQ |= SFR_WAKEUP_CTRL_TIMER1

                    self._NMIREQ |= SFR_NMI_CTRL_TIMER1
                    if (self._NMI_CTRL & SFR_NMI_CTRL_TIMER1):
                        self._NMI()

                    if ((self._AUDIO_CH0_CTRL & SFR_AUDIO_CTRL_TM1_OVFLW) and (self._AUDIO_CH0_CTRL & SFR_AUDIO_CTRL_TONE_MODE)):
                        self._sound.toggle(0)
                    if ((self._AUDIO_CH1_CTRL & SFR_AUDIO_CTRL_TM1_OVFLW) and (self._AUDIO_CH1_CTRL & SFR_AUDIO_CTRL_TONE_MODE)):
                        self._sound.toggle(1)

        self._T1KHZ_counter -= exec_cycles
        while (self._T1KHZ_counter <= 0):
            self._T1KHZ_counter += self._sub_clock_div * (SUB_CLOCK // 1024)
            self._T1KHZ += 1
            
            time_base_h = self._TIME_BASE & SFR_TIMEBASE_H_MASK            
            if (not(self._T1KHZ & SFR_TIMEBASE_H_TBL[time_base_h])):
                self._IREQ |= SFR_INT_CTRL_TIME_BASEH
                self._WAKEUPREQ |= SFR_WAKEUP_CTRL_TIME_BASEH
            
            time_base_l = (self._TIME_BASE & SFR_TIMEBASE_L_MASK) >> SFR_TIMEBASE_L_SHIFT
            if (not(self._T1KHZ & SFR_TIMEBASE_L_TBL[time_base_l])):
                self._IREQ |= SFR_INT_CTRL_TIME_BASEL
                self._WAKEUPREQ |= SFR_WAKEUP_CTRL_TIME_BASEL
                
    def clock(self):
        if (self._CPU_ENBL):
            opcode = self._read_mem(self._PC)
            self._PC = (self._PC + 1) & 0xFFFF
            exec_cycles = self._execute[opcode](self) << self._CPU_DIV
            self._instr_counter += 1
            self._timers_clock(exec_cycles)
            if ((not self._IF) and (self._IREQ & self._INT_CTRL)):
                self._IRQ()
        else:
            exec_cycles = self._sub_clock_div
            if (self._WAKEUP_CTRL & self._WAKEUPREQ):
                self._CPU_ENBL = 1
                self._CPU_DIV = SFR_CPU_CTRL_DEFAULT
            if (self._CLK32768_ENABLE):
                self._timers_clock(exec_cycles)

        return exec_cycles
    
    def _set_sfr_io_portA_attr(self, value):
        self._ATTR["PA"] = value
        self._interconnect.emit_port(self, "PA", self._port_read("PA"), 1)
    
    def _set_sfr_io_portA_dir(self, value):
        self._PDIR["PA"] = value
        self._interconnect.emit_port(self, "PA", self._port_read("PA"), 1)

    def _get_sfr_io_portA_data(self):
        return self._port_read("PA")
    
    def _set_sfr_io_portA_data(self, value):
        self._PLATCH["PA"] = value
        self._interconnect.emit_port(self, "PA", self._port_read("PA"), 1)
    
    def _set_sfr_io_portB_attr(self, value):
        self._ATTR["PB"] = ((value & 0x1) * 0x3) | ((value & 0x2) * 0x6) | ((value & 0x4) * 0xC) | ((value & 0x8) * 0x18)
        self._interconnect.emit_port(self, "PB", self._port_read("PB"), 1)

    def _set_sfr_io_portB_dir(self, value):
        self._PDIR["PB"] = ((value & 0x1) * 0x3) | ((value & 0x2) * 0x6) | ((value & 0x4) * 0xC) | ((value & 0x8) * 0x18)
        self._interconnect.emit_port(self, "PB", self._port_read("PB"), 1)

    def _get_sfr_io_portB_data(self):
        return self._port_read("PB")
    
    def _set_sfr_io_portB_data(self, value):
        self._PLATCH["PB"] = value
        self._interconnect.emit_port(self, "PB", self._port_read("PB"), 1)

    def _set_sfr_io_portC_attr(self, value):
        self._ATTR["PC"] = value
        self._interconnect.emit_port(self, "PC", self._port_read("PC"), 1)
    
    def _set_sfr_io_portC_dir(self, value):
        self._PDIR["PC"] = value
        self._interconnect.emit_port(self, "PC", self._port_read("PC"), 1)

    def _get_sfr_io_portC_data(self):
        return self._port_read("PC")
    
    def _set_sfr_io_portC_data(self, value):
        self._PLATCH["PC"] = value
        self._interconnect.emit_port(self, "PC", self._port_read("PC"), 1)

    def _set_sfr_io_portD_dir(self, value):
        self._PDIR["PD"] = value & SFR_IO_PORTD_MASK
        self._interconnect.emit_port(self, "PD", self._port_read("PD"), 1)

    def _set_sfr_io_portD_attr(self, value):
        self._ATTR["PD"] = value & SFR_IO_PORTD_MASK
        self._interconnect.emit_port(self, "PD", self._port_read("PD"), 1)

    def _get_sfr_io_portD_data(self):
        return self._port_read("PD")
    
    def _set_sfr_io_portD_data(self, value):
        self._PLATCH["PD"] = value & SFR_IO_PORTD_MASK
        self._interconnect.emit_port(self, "PD", self._port_read("PD"), 1)

    def _get_sfr_audio_ch0_ctrl(self):
        return self._AUDIO_CH0_CTRL

    def _set_sfr_audio_ch0_ctrl(self, value):
        self._AUDIO_CH0_CTRL = value

    def _get_sfr_audio_ch0_data(self):
        return 0

    def _set_sfr_audio_ch0_data(self, value):
        self._AUDIO_CH0_DATA = value
        self._sound.set_data(0, self._AUDIO_CH0_CTRL, value)

    def _get_sfr_audio_ch1_ctrl(self):
        return self._AUDIO_CH1_CTRL

    def _set_sfr_audio_ch1_ctrl(self, value):
        self._AUDIO_CH1_CTRL = value

    def _get_sfr_audio_ch1_data(self):
        return self._AUDIO_CH1_DATA

    def _set_sfr_audio_ch1_data(self, value):
        self._AUDIO_CH1_DATA = value
        self._sound.set_data(1, self._AUDIO_CH1_CTRL, value)

    def _get_sfr_bank_sel(self):
        return self._ROM_BANK >> 15
    
    def _set_sfr_bank_sel(self, value):
        self._ROM_BANK = (value & 0x0F) << 15

    def _get_sfr_wakeup_ctrl(self):
        value = self._WAKEUPREQ
        return value
    
    def _set_sfr_wakeup_ctrl(self, value):
        self._WAKEUP_CTRL = value
        self._WAKEUPREQ &= value

    def _get_sfr_timer_timebase_sel(self):
        return self._T1KHZ
    
    def _set_sfr_timer_timebase_sel(self, value):
        self._TIME_BASE = value

    def _get_sfr_timer_ctrl(self):
        return self._TIMER_CTRL
    
    def _set_sfr_timer_ctrl(self, value):
        self._TIMER_CTRL = value
    
    def _set_sfr_clk_32768_en(self, value):
        self._CLK32768_ENABLE = value & SFR_CLK32768_ENABLE

    def _get_sfr_nmi_ctrl(self):
        buf = self._NMIREQ | (self._NMI_CTRL & 0x80)
        return buf
    
    def _set_sfr_nmi_ctrl(self, value):
        self._NMI_CTRL = value
        self._NMIREQ &= value

    def _get_sfr_int_ctrl(self):
        return self._IREQ
    
    def _set_sfr_int_ctrl(self, value):
        self._INT_CTRL = value
        self._IREQ = 0

    def _get_sfr_clk_cpu_ctrl(self):
        return self._CPU_DIV
    
    def _set_sfr_clk_cpu_ctrl(self, value):
        if ((value & 0x7) == 0x7):
            self._CPU_ENBL = 0
        else:
            self._CPU_DIV = value & 0x7

    def _set_sfr_clk_int_clear(self, value):
        self._IREQ &= ~value

    def _get_sfr_timer_TM1L(self):
        return int(self._TM1) & 0xFF

    def _set_sfr_timer_TM1L(self, value):
        self._TM1_RELOAD = (self._TM1_RELOAD & 0xFF00) | value

    def _get_sfr_timer_TM1H(self):
        return int(self._TM1) >> 8

    def _set_sfr_timer_TM1H(self, value):
        self._TM1_RELOAD = (self._TM1_RELOAD & 0xFF) | (value << 8)
        self._TM1 = self._TM1_RELOAD

    def _get_sfr_timer_TM0L(self):
        return int(self._TM0) & 0xFF

    def _set_sfr_timer_TM0L(self, value):
        self._TM0_RELOAD = (self._TM0_RELOAD & 0xFF00) | value

    def _get_sfr_timer_TM0H(self):
        return int(self._TM0) >> 8

    def _set_sfr_timer_TM0H(self, value):
        self._TM0_RELOAD = (self._TM0_RELOAD & 0xFF) | (value << 8)
        self._TM0 = self._TM0_RELOAD

    def _get_sfr_lcd_ctrl1(self):
        return self._LCD_CTRL1
    
    def _set_sfr_lcd_ctrl1(self, value):   
        self._LCD_CTRL1 = value

    def _get_sfr_specialfunc_config(self):
        return 0
    
    def _set_sfr_specialfunc_config(self, value):   
        pass  

    def _get_sfr_aux_byte_mirror(self):
        return self._BYTE_MIRROR
    
    def _set_sfr_aux_byte_mirror(self, value):
        b = (value & 0xF0) >> 4 | (value & 0x0F) << 4
        b = (b & 0xCC) >> 2 | (b & 0x33) << 2
        self._BYTE_MIRROR = (b & 0xAA) >> 1 | (b & 0x55) << 1

    def _get_sfr_aux_nibble_swap(self):
        return self._NIBBLE_SWAP
    
    def _set_sfr_aux_nibble_swap(self, value):
        self._NIBBLE_SWAP = ((value & 0x0F) << 4) | ((value & 0xF0) >> 4)

    def _get_sfr_dummy(self):
        return 0
    
    def _set_sfr_dummy(self, value):
        pass
    
    def _write_mem(self, addr, value):
        if ((addr >= CPU_RAM_OFFSET) and (addr < RAM_SIZE + CPU_RAM_OFFSET)):
            self._RAM[addr - CPU_RAM_OFFSET] = value
        elif ((addr >= DPRAM_OFFSET) and (addr < DPRAM_SIZE + DPRAM_OFFSET)):
            self._DPRAM[addr - DPRAM_OFFSET] = value
        else:
            io = self._sfr_tbl.get(addr)
            if (io != None):
                io[1](self, value)

    def _read_mem(self, addr):
        if (addr >= ROM_BANK_0_OFFSET):
            return self._ROM.get_byte(addr & 0x7FFF)
        elif (addr >= ROM_BANK_LH_OFFSET):
            return self._ROM.get_byte((addr & 0x7FFF) | self._ROM_BANK)
        elif (addr >= DPRAM_OFFSET):
            return self._DPRAM[addr - DPRAM_OFFSET]
        elif ((addr >= CPU_RAM_OFFSET) and (addr < RAM_SIZE + CPU_RAM_OFFSET)):
            return self._RAM[addr - CPU_RAM_OFFSET]
        else:
            io = self._sfr_tbl.get(addr)
            if (io != None):
                return io[0](self)
            return 0
    
    def _get_ps(self):
        if self._NF > 0x1 or self._VF > 0x1 or self._BF > 0x1 or self._DF > 0x1 or self._IF > 0x1 or self._ZF > 0x1 or self._CF > 0x1:
            print("Invalid PS: NF=%d, VF=%d, BF=%d, DF=%d, IF=%d, ZF=%d, CF=%d" % (self._NF, self._VF, self._BF, self._DF, self._IF, self._ZF, self._CF))
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
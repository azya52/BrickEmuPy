from .rom import ROM
from .SPL0Xsound import SPL0Xsound
from .SPL0X import SPL0X

class SPL03(SPL0X):
    SFR_OFFSET = 0xC0
    SFR_SIZE = 0x40
    CPU_RAM_OFFSET = 0x30
    CPURAM_SIZE = 0x50
    LCDRAM_OFFSET = 0x00
    LCDRAM_SIZE = 0x30

    def __init__(self, mask, clock):
        super().__init__(mask, clock)

        self._io_tbl = {
            0xC0: (SPL0X._get_io_IO_Ctrl, SPL0X._set_io_IO_Ctrl),
            0xC1: (SPL0X._get_io_PortA_Data, SPL0X._set_io_PortA_Data),
            0xC3: (SPL0X._get_io_PortB_Data, SPL0X._set_io_PortB_Data),
            0xC4: (SPL0X._get_io_ToneA_Ctrl1, SPL0X._set_io_ToneA_Ctrl1),
            0xC6: (SPL0X._get_io_ToneA_Ctrl2, SPL0X._set_io_ToneA_Ctrl2),
            0xCC: (SPL0X._get_io_Noise_Ctrl1, SPL0X._set_io_Noise_Ctrl1),
            0xCE: (SPL0X._get_io_Noise_Ctrl2, SPL0X._set_io_Noise_Ctrl2),
            0xD0: (SPL0X._get_io_System_Ctrl, SPL0X._set_io_System_Ctrl),
            0xD2: (SPL0X._get_io_Interrupt_Config, SPL0X._set_io_Interrupt_Config),
            0xD4: (SPL0X._get_io_Speech_Ctrl, SPL0X._set_io_Speech_Ctrl),
            0xD5: (SPL0X._get_io_Speech_Data_Port, SPL0X._set_io_Speech_Data_Port),
            0xD7: (SPL0X._get_io_Bank_Select, SPL0X._set_io_Bank_Select),
        }

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
                self._NOISE_CTRL1,
                self._NOISE_CTRL2,
                self._SYS_CTRL,
                self._INT_CFG,
                self._SPEECH_CTRL,
                self._SPEECH_DATA,
                self._ROM_BANK
            )
        }

    def _set_io_Speech_Data_Port(self, value):
        self._SPEECH_DATA = value & 0xBE
        self._sound.set_speech(self._SPEECH_CTRL, self._SPEECH_DATA, self._cycle_counter)
    
    def _set_io_Bank_Select(self, value):
        self._ROM_BANK = value & 0x1
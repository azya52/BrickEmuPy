from .rom import ROM
from .SPL0Xsound import SPL0Xsound
from .SPL0X import SPL0X

class SPL02(SPL0X):
    SFR_OFFSET = 0xC0
    SFR_SIZE = 0x40
    CPU_RAM_OFFSET = 0x30
    CPURAM_SIZE = 0x90
    LCDRAM_OFFSET = 0x00
    LCDRAM_SIZE = 0x30
from .HT24LC08 import *
from .matrix_input import *
from .direct_input import *
from .CON_V3_IR import *
from .CON_DGM import *

__all__ = [
    "direct_input",
    "matrix_input",
    "HT24LC08",
    "CON_V3_IR",
    "CON_DGM",
    "peripherals_map"]

peripherals_map = {
    "direct_input": DirectInput,
    "matrix_input": MatrixInput,
    "HT24LC08": HT24LC08,
    "CON_V3_IR": CON_V3_IR,
    "CON_DGM": CON_DGM
}

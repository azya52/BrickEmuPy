from .HT24LC08 import *
from .matrix_input import *
from .direct_input import *
from .CON_V3_IR import *

__all__ = [
    "HT24LC08",
    "CON_V3_IR",
    "direct_input",
    "matrix_input",
    "peripherals_map"]

peripherals_map = {
    "HT24LC08": HT24LC08,
    "CON_V3_IR": CON_V3_IR,
    "direct_input": DirectInput,
    "matrix_input": MatrixInput
}

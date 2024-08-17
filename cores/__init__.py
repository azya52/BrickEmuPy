from .E0C6200 import *
from .E0C6200dasm import *
from .HT943 import *
from .HT943dasm import *
from .EM73000 import *
from .EM73000dasm import *
from .KS56CX2X import *
from .KS56CX2Xdasm import *

__all__ = ["E0C6200", "E0C6200dasm", "HT943", "HT943dasm", "EM73000", "EM73000dasm", "KS56CX2X", "KS56CX2Xdasm", "cores_map"]

cores_map = {
    "E0C6200": {
        "core": E0C6200,
        "dasm": E0C6200dasm
    },
    "HT943": {
        "core": HT943,
        "dasm": HT943dasm
    },
    "EM73000": {
        "core": EM73000,
        "dasm": EM73000dasm
    },
    "KS56CX2X": {
        "core": KS56CX2X,
        "dasm": KS56CX2Xdasm
    }
}

from .E0C6200 import *
from .E0C6200dasm import *
from .HT943 import *
from .HT943dasm import *

__all__ = ["E0C6200", "E0C6200dasm", "HT943", "HT943dasm", "cores_map"]

cores_map = {
    "E0C6200": {
        "core": E0C6200,
        "dasm": E0C6200dasm
    },
    "HT943": {
        "core": HT943,
        "dasm": HT943dasm
    }
}

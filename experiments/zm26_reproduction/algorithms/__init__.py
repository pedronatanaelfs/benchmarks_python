from .optall import OptAll
from .optmpnds import OptMPNDS
from .optmpnds2 import OptMPNDS2
from .optmpnds3 import OptMPNDS3

ALGORITHMS = {
    "OptAll": OptAll,
    "OptMPNDS": OptMPNDS,
    "OptMPNDS2": OptMPNDS2,
    "OptMPNDS3": OptMPNDS3,
}

__all__ = ["OptAll", "OptMPNDS", "OptMPNDS2", "OptMPNDS3", "ALGORITHMS"]

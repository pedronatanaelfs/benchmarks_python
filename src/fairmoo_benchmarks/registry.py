"""Problem registry."""

from __future__ import annotations

from typing import Any, Type

from fairmoo_benchmarks.base import MultiPartyProblem
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP1
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP2
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP3
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP4
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP5
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP6
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP7
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP8
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP9
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP10
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP11
from fairmoo_benchmarks.mpdmp.she2023 import MPDMP12
from fairmoo_benchmarks.mpdmp.mpdmp13 import MPDMP13
from fairmoo_benchmarks.mpdmp.mpdmp14 import MPDMP14
from fairmoo_benchmarks.mpdmp.mpdmp15 import MPDMP15
from fairmoo_benchmarks.mpdmp.mpdmp16 import MPDMP16
from fairmoo_benchmarks.mpdmp.mpdmp17 import MPDMP17
from fairmoo_benchmarks.mpdmp.mpdmp18 import MPDMP18
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP1
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP2
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP3
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP4
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP5
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP6
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP7
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP8
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP9
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP10
from fairmoo_benchmarks.mpmop.liu2020 import MPMOP11
from fairmoo_benchmarks.mpmop.mpmop12 import MPMOP12
from fairmoo_benchmarks.mpmop.mpmop13 import MPMOP13
from fairmoo_benchmarks.mpmop.mpmop14 import MPMOP14
from fairmoo_benchmarks.mpmop.mpmop15 import MPMOP15
from fairmoo_benchmarks.mpmop.mpmop16 import MPMOP16
from fairmoo_benchmarks.mpmop.mpmop17 import MPMOP17

_REGISTRY: dict[str, Type[MultiPartyProblem]] = {
    "MPDMP1": MPDMP1,
    "MPDMP2": MPDMP2,
    "MPDMP3": MPDMP3,
    "MPDMP4": MPDMP4,
    "MPDMP5": MPDMP5,
    "MPDMP6": MPDMP6,
    "MPDMP7": MPDMP7,
    "MPDMP8": MPDMP8,
    "MPDMP9": MPDMP9,
    "MPDMP10": MPDMP10,
    "MPDMP11": MPDMP11,
    "MPDMP12": MPDMP12,
    "MPDMP13": MPDMP13,
    "MPDMP14": MPDMP14,
    "MPDMP15": MPDMP15,
    "MPDMP16": MPDMP16,
    "MPDMP17": MPDMP17,
    "MPDMP18": MPDMP18,
    "MPMOP1": MPMOP1,
    "MPMOP2": MPMOP2,
    "MPMOP3": MPMOP3,
    "MPMOP4": MPMOP4,
    "MPMOP5": MPMOP5,
    "MPMOP6": MPMOP6,
    "MPMOP7": MPMOP7,
    "MPMOP8": MPMOP8,
    "MPMOP9": MPMOP9,
    "MPMOP10": MPMOP10,
    "MPMOP11": MPMOP11,
    "MPMOP12": MPMOP12,
    "MPMOP13": MPMOP13,
    "MPMOP14": MPMOP14,
    "MPMOP15": MPMOP15,
    "MPMOP16": MPMOP16,
    "MPMOP17": MPMOP17,
}


def register(name: str, cls: Type[MultiPartyProblem]) -> None:
    _REGISTRY[name.upper()] = cls


def get_problem(name: str, **kwargs: Any) -> MultiPartyProblem:
    key = name.strip().upper()
    # Accept MPDMP01 style
    if key.endswith(("01","02","03","04","05","06","07","08","09")) and key[-2] == "0":
        key = key[:-2] + key[-1]
    if key not in _REGISTRY:
        raise KeyError(f"Unknown problem {name!r}. Available: {sorted(_REGISTRY)}")
    return _REGISTRY[key](**kwargs)


def list_problems() -> list[str]:
    return sorted(_REGISTRY.keys(), key=lambda s: (s[:5], int(s[5:])))


def describe_problem(name: str) -> dict[str, Any]:
    return get_problem(name).describe()

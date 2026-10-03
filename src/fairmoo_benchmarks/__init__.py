"""fairmoo_benchmarks: MPMOP and MPDMP benchmarks for multi-party MOO research."""

from fairmoo_benchmarks.base import MultiPartyProblem
from fairmoo_benchmarks.registry import describe_problem, get_problem, list_problems

__all__ = [
    "MultiPartyProblem",
    "get_problem",
    "list_problems",
    "describe_problem",
]

__version__ = "0.1.0"

"""Shared helpers for MPMOP12–MPMOP17 from the supplied MATLAB repository."""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from fairmoo_benchmarks.base import MultiPartyProblem
from fairmoo_benchmarks.status import CommonPSStatus

DEFAULT_N_VAR = 10

ZM26_MPMOP_SOURCE = (
    "2026ZhaoNash-main/MPMOP MATLAB classdefs and MPMOP_Value.m "
    "(author-supplied executable reference)."
)

DIMENSION_NOTE = (
    f"The MATLAB class constructor default is D={DEFAULT_N_VAR}; Python exposes "
    "n_var as an override while preserving that source default."
)


class ZM26MPMOP(MultiPartyProblem):
    """Base for ZM26 MPMOP12–17 with disjoint party-wise PS."""

    def __init__(
        self,
        *,
        name: str,
        n_obj_per_dm: Sequence[int],
        xl: Sequence[float],
        xu: Sequence[float],
        n_var: int = DEFAULT_N_VAR,
        notes: str = "",
    ) -> None:
        # n_var is an explicit constructor argument; default is ASSUMED_DEFAULT.
        super().__init__(
            name=name,
            n_var=n_var,
            n_obj_per_dm=n_obj_per_dm,
            xl=xl,
            xu=xu,
            family="MPMOP",
            source=ZM26_MPMOP_SOURCE,
            year=2026,
            common_ps_exists=CommonPSStatus.EMPTY,
            known_ps=True,
            known_pf=True,
            notes=(notes + " " + DIMENSION_NOTE).strip()
            if notes
            else (
                "Party-wise PS mutually disjoint (no common PS). "
                "MATLAB-compatible party PF sampling is implemented. " + DIMENSION_NOTE
            ),
            metadata={
                "dimension_source": "2026ZhaoNash MATLAB class constructor",
                "dimension_default": DEFAULT_N_VAR,
                "dimension_status": "SOURCE_DEFAULT_MATLAB",
            },
        )

    def get_pareto_front(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        ps = self.get_pareto_set(dm=dm, n_points=n_points)
        if ps is None or ps.size == 0:
            return ps
        if dm is None:
            # Common PF does not exist for these problems.
            return np.zeros((0, self.n_obj), dtype=float)
        return self.evaluate_dm(ps, dm)

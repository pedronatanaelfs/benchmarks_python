"""Shared helpers for MPMOP12–MPMOP17 (ZM26 Appendix Table S-VI)."""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from fairmoo_benchmarks.base import MultiPartyProblem
from fairmoo_benchmarks.status import CommonPSStatus

DEFAULT_N_VAR = 10

ZM26_MPMOP_SOURCE = (
    "Zhao, Xu, Luo (2026). Fairness-Aware Performance Evaluation for "
    "Multi-Party Multi-Objective Optimization. arXiv:2601.22497, "
    "Appendix Table S-VI / Section S-IX."
)

DIMENSION_NOTE = (
    "Table S-VI defines objectives for general D but does not fix a numeric D. "
    "ZM26 Table tab:MPMOP_results caption states D=2 for MPMOP1–11 experiments only "
    "(not MPMOP12–17). MPMOP14/17 require D>=3. "
    f"Constructor default n_var={DEFAULT_N_VAR} is an ASSUMED_DEFAULT "
    "(Liu/OptMPNDS convention), not source-confirmed for ZM26 MPMOP12–17."
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
            known_pf=False,
            notes=(notes + " " + DIMENSION_NOTE).strip()
            if notes
            else (
                "Party-wise PS mutually disjoint (no common PS). "
                "PF not tabulated analytically in appendix. " + DIMENSION_NOTE
            ),
            metadata={
                "dimension_source": "not explicitly specified in ZM26 Table S-VI",
                "dimension_default": DEFAULT_N_VAR,
                "dimension_status": "ASSUMED_DEFAULT",
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

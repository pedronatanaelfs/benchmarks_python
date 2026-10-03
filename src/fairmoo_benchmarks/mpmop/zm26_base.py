"""Shared helpers for MPMOP12–MPMOP17 (ZM26 Appendix Table S-VI)."""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from fairmoo_benchmarks.base import MultiPartyProblem

ZM26_MPMOP_SOURCE = (
    "Zhao, Xu, Luo (2026). Fairness-Aware Performance Evaluation for "
    "Multi-Party Multi-Objective Optimization. arXiv:2601.22497, "
    "Appendix Table S-VI / Section S-IX. "
    "Default n_var=10 follows MPMOP1–11 experimental convention in Liu et al. "
    "(CEC 2020 / OptMPNDS); Table S-VI does not state D explicitly "
    "[NEEDS_MANUAL_VERIFICATION if ZM26 used another D]."
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
        n_var: int = 10,
        notes: str = "",
    ) -> None:
        super().__init__(
            name=name,
            n_var=n_var,
            n_obj_per_dm=n_obj_per_dm,
            xl=xl,
            xu=xu,
            family="MPMOP",
            source=ZM26_MPMOP_SOURCE,
            year=2026,
            common_ps_exists="False",
            known_ps=True,
            known_pf=False,
            notes=notes
            or "Party-wise PS mutually disjoint (no common PS). PF not tabulated analytically in appendix.",
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

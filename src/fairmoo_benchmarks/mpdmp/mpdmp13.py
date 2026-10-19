"""MPDMP13 — ZM26 Appendix Table S-V / Section S-X.

Verified against sources/zm26_2026/Appendix.pdf (pdftotext).
Decision space: x in [0, 100]^2.
Objectives: f_mi(x) = Euclidean distance to reference point p_mi.
Common PS: empty (False).
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from fairmoo_benchmarks.mpdmp.distance_base import DistanceBasedMultiPartyProblem, ZM26_SOURCE
from fairmoo_benchmarks.status import CommonPSStatus


class MPDMP13(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        super().__init__(
            name="MPDMP13",
            reference_points={
                0: [(30.0, 40.0), (70.0, 40.0)],
                1: [(30.0, 60.0), (70.0, 60.0)],
            },
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=ZM26_SOURCE,
            year=2026,
            common_ps_exists=CommonPSStatus.EMPTY,
            known_ps=True,
            known_pf=True,
            notes="No common PS (party-wise PS mutually disjoint). x in [0,100]^2.",
            ps_geometry={0: "Line segment", 1: "Line segment"},
        )

    def get_pareto_front(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        if dm is not None:
            return super().get_pareto_front(dm=dm, n_points=n_points)
        # ParallelLines1.PF samples the first party's line at 100 points.
        t = np.linspace(0.0, 1.0, 100)
        X = np.column_stack([30.0 + 40.0 * t, np.full(100, 40.0)])
        return self.evaluate(X)


__all__ = ["MPDMP13"]

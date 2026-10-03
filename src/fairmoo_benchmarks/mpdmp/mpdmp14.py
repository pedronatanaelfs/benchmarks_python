"""MPDMP14 — ZM26 Appendix Table S-V / Section S-X.

Verified against sources/zm26_2026/Appendix.pdf (pdftotext).
Decision space: x in [0, 100]^2.
Objectives: f_mi(x) = Euclidean distance to reference point p_mi.
Common PS: empty (False).
"""

from __future__ import annotations

from fairmoo_benchmarks.mpdmp.distance_base import DistanceBasedMultiPartyProblem, ZM26_SOURCE
from fairmoo_benchmarks.status import CommonPSStatus


class MPDMP14(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        super().__init__(
            name="MPDMP14",
            reference_points={
                0: [(30.0, 35.0), (50.0, 35.0), (40.0, 50.0)],
                1: [(50.0, 50.0), (70.0, 50.0), (60.0, 65.0)],
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
            ps_geometry={0: "Triangle", 1: "Triangle"},
        )


__all__ = ["MPDMP14"]

"""MPDMP18 — ZM26 Appendix Table S-V / Section S-X.

Verified against sources/zm26_2026/Appendix.pdf (pdftotext).
Decision space: x in [0, 100]^2.
Objectives: f_mi(x) = Euclidean distance to reference point p_mi.
Common PS: empty (False).
"""

from __future__ import annotations

from fairmoo_benchmarks.mpdmp.distance_base import DistanceBasedMultiPartyProblem, ZM26_SOURCE


class MPDMP18(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        super().__init__(
            name="MPDMP18",
            reference_points={
                0: [(25.0, 45.0), (35.0, 35.0), (35.0, 55.0)],
                1: [(45.0, 25.0), (55.0, 25.0), (50.0, 40.0)],
                2: [(65.0, 45.0), (75.0, 35.0), (75.0, 55.0)],
            },
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=ZM26_SOURCE,
            year=2026,
            common_ps_exists="False",
            known_ps=True,
            known_pf=True,
            notes="No common PS (party-wise PS mutually disjoint). x in [0,100]^2.",
            ps_geometry={0: "Triangle", 1: "Triangle", 2: "Triangle"},
        )


__all__ = ["MPDMP18"]

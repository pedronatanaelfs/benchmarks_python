"""MPDMP17 — ZM26 Appendix Table S-V / Section S-X.

Verified against sources/zm26_2026/Appendix.pdf (pdftotext).
Decision space: x in [0, 100]^2.
Objectives: f_mi(x) = Euclidean distance to reference point p_mi.
Common PS: empty (False).
"""

from __future__ import annotations

from fairmoo_benchmarks.mpdmp.distance_base import DistanceBasedMultiPartyProblem, ZM26_SOURCE


class MPDMP17(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        super().__init__(
            name="MPDMP17",
            reference_points={
                0: [(25.0, 60.0), (40.0, 70.0)],
                1: [(60.0, 70.0), (75.0, 60.0)],
                2: [(40.0, 30.0), (60.0, 30.0)],
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
            ps_geometry={0: "Line segment", 1: "Line segment", 2: "Line segment"},
        )


__all__ = ["MPDMP17"]

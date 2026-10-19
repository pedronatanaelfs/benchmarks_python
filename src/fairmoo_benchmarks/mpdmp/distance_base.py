"""Distance-based multi-party problems (MPDMP family helpers)."""

from __future__ import annotations

from typing import Mapping, Optional, Sequence, Union

import numpy as np

from fairmoo_benchmarks.base import MultiPartyProblem
from fairmoo_benchmarks.status import CommonPSStatus
from fairmoo_benchmarks.utils import (
    euclidean_distances_to_points,
    linspace_segment,
    sample_convex_polygon,
)

PointsSpec = Mapping[Union[int, str], np.ndarray]


class DistanceBasedMultiPartyProblem(MultiPartyProblem):
    """Generic Euclidean distance multi-party problem.

    For each DM ``m`` with reference points ``P_m`` of shape ``(K_m, n_var)``,

        f_{m,i}(x) = ||x - p_{m,i}||_2
    """

    def __init__(
        self,
        *,
        name: str,
        reference_points: PointsSpec,
        xl: Sequence[float] = (0.0, 0.0),
        xu: Sequence[float] = (100.0, 100.0),
        family: str = "MPDMP",
        source: str = "",
        year: Optional[int] = None,
        common_ps_exists: CommonPSStatus | str | bool | None = CommonPSStatus.UNKNOWN,
        known_ps: bool = True,
        known_pf: bool = True,
        notes: str = "",
        ps_geometry: Optional[Mapping[int, str]] = None,
        metadata: Optional[Mapping] = None,
    ) -> None:
        refs: dict[int, np.ndarray] = {}
        for key, pts in reference_points.items():
            if isinstance(key, str) and key.upper().startswith("DM"):
                dm = int(key.upper().replace("DM", "")) - 1
            else:
                dm = int(key)
            arr = np.asarray(pts, dtype=float)
            if arr.ndim != 2:
                raise ValueError(f"reference_points[{key}] must be 2D")
            refs[dm] = arr

        dms = sorted(refs.keys())
        if dms != list(range(len(dms))):
            raise ValueError("DM indices must be contiguous starting at 0")

        n_obj_per_dm = [refs[dm].shape[0] for dm in dms]
        n_var = int(refs[0].shape[1])
        for dm in dms:
            if refs[dm].shape[1] != n_var:
                raise ValueError("All reference points must share the same dimension")

        meta = dict(metadata or {})
        meta["ps_geometry"] = {int(k): v for k, v in dict(ps_geometry or {}).items()}
        meta["reference_points"] = {dm: refs[dm].tolist() for dm in dms}

        super().__init__(
            name=name,
            n_var=n_var,
            n_obj_per_dm=n_obj_per_dm,
            xl=xl,
            xu=xu,
            family=family,
            source=source,
            year=year,
            common_ps_exists=common_ps_exists,
            known_ps=known_ps,
            known_pf=known_pf,
            notes=notes,
            metadata=meta,
        )
        self.reference_points = refs

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        blocks = [
            euclidean_distances_to_points(X, self.reference_points[dm])
            for dm in range(self.n_dm)
        ]
        return np.concatenate(blocks, axis=1)

    def get_reference_points(self, dm: Optional[int] = None) -> Optional[np.ndarray]:
        if dm is None:
            return np.vstack([self.reference_points[i] for i in range(self.n_dm)])
        return self.reference_points[int(dm)].copy()

    def get_concession(self, rate: float = 0.0) -> np.ndarray:
        """Reproduce MATLAB ``MPDMP.GetConcession``.

        MPDMP1–12 always return zero concession. MPDMP13–18 select one of
        seven author-defined cases from ``rate``.
        """
        number = int(self.name.replace("MPDMP", ""))
        if number <= 12:
            return np.zeros(self.n_dm, dtype=float)

        try:
            value = float(rate)
        except (TypeError, ValueError):
            value = 0.0
        if not np.isfinite(value):
            value = 0.0
        scaled = value * 10.0 if 0.0 < value < 1.0 else value
        # MATLAB round is half-away-from-zero; case ids are then clamped.
        case_id = int(np.floor(scaled + 0.5)) if scaled >= 0 else int(np.ceil(scaled - 0.5))
        case_id = max(1, min(7, case_id))

        if self.n_dm == 2:
            cases = np.array(
                [
                    [0.0, 0.0],
                    [0.3, 0.0],
                    [0.3, 0.3],
                    [0.3, 0.7],
                    [0.5, 0.5],
                    [0.7, 0.7],
                    [1.0, 1.0],
                ]
            )
        else:
            cases = np.array(
                [
                    [0.0, 0.0, 0.0],
                    [0.3, 0.0, 0.0],
                    [0.3, 0.3, 0.3],
                    [0.3, 0.1, 0.6],
                    [0.5, 0.5, 0.5],
                    [0.7, 0.7, 0.7],
                    [1.0, 1.0, 1.0],
                ]
            )
        return cases[case_id - 1].copy()

    def get_pareto_set(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        """Sample the convex hull of a DM's reference points (Köppe/Koppen geometry).

        ``dm is None`` returns the common PS only when explicitly known by a
        subclass override or when ``common_ps_exists == 'False'`` (empty).
        """
        if dm is None:
            if self.common_ps_status is CommonPSStatus.EMPTY:
                return np.zeros((0, self.n_var), dtype=float)
            return None

        pts = self.reference_points[int(dm)]
        if pts.shape[0] == 1:
            return np.repeat(pts, n_points, axis=0)
        if pts.shape[0] == 2:
            return linspace_segment(pts[0], pts[1], n_points)
        if pts.shape[0] >= 3 and self.n_var == 2:
            return sample_convex_polygon(pts, n_points)
        return None

    def get_pareto_front(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        ps = self.get_pareto_set(dm=dm, n_points=n_points)
        if ps is None:
            return None
        if ps.size == 0:
            return np.zeros((0, self.n_obj if dm is None else self.n_obj_per_dm[dm]), dtype=float)
        if dm is None:
            return self.evaluate(ps)
        return self.evaluate_dm(ps, dm)


ZM26_SOURCE = (
    "Zhao, Xu, Luo (2026). Fairness-Aware Performance Evaluation for "
    "Multi-Party Multi-Objective Optimization. arXiv:2601.22497, "
    "Appendix Table S-V / Section S-X."
)

SHE2023_SOURCE = (
    "She, Luo, Lin, Chang, Shi (2023). Multiparty distance minimization: "
    "Problems and an evolutionary approach. Swarm and Evolutionary Computation. "
    "Official code: https://github.com/MiLabHITSZ/2022SheOptMPNDS3"
)


def make_zm26_mpdmp(
    name: str,
    reference_points: Mapping[int, Sequence[Sequence[float]]],
    ps_geometry: Mapping[int, str],
) -> DistanceBasedMultiPartyProblem:
    return DistanceBasedMultiPartyProblem(
        name=name,
        reference_points={dm: np.asarray(pts, dtype=float) for dm, pts in reference_points.items()},
        xl=(0.0, 0.0),
        xu=(100.0, 100.0),
        family="MPDMP",
        source=ZM26_SOURCE,
        year=2026,
        common_ps_exists=CommonPSStatus.EMPTY,
        known_ps=True,
        known_pf=True,
        notes="No common PS (party-wise PS mutually disjoint). x in [0,100]^2.",
        ps_geometry=ps_geometry,
    )


def matlab_centroid_path_front(
    problem: DistanceBasedMultiPartyProblem,
    pairs: Sequence[tuple[int, int]],
    points_per_path: int = 100,
) -> np.ndarray:
    """Reproduce the conflict-map PF samplers used by MATLAB MPDMP14–18."""
    centers = [
        np.mean(problem.reference_points[dm], axis=0)
        for dm in range(problem.n_dm)
    ]
    paths = [
        linspace_segment(centers[start], centers[end], points_per_path)
        for start, end in pairs
    ]
    return problem.evaluate(np.vstack(paths))

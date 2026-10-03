"""MPDMP1–MPDMP12 from She et al. (2023) / MiLabHITSZ/2022SheOptMPNDS3."""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from fairmoo_benchmarks.mpdmp.distance_base import DistanceBasedMultiPartyProblem, SHE2023_SOURCE
from fairmoo_benchmarks.status import CommonPSStatus
from fairmoo_benchmarks.utils import matlab_nsidedpoly_vertices, linspace_segment


def _reorder_objectives(
    points_by_dm: Sequence[np.ndarray],
    objective_order: Sequence[tuple[int, int]],
) -> dict[int, np.ndarray]:
    """Build reference_points dict from (dm, local_idx) objective order.

    For maps that interleave objectives differently from DM blocks, we instead
    pass already-blocked points. This helper is unused for interleaved maps.
    """
    return {i: np.asarray(p, dtype=float) for i, p in enumerate(points_by_dm)}


class _InterleavedDistanceProblem(DistanceBasedMultiPartyProblem):
    """Distance problem where MATLAB concatenates objectives in a custom order.

    We store ``objective_points`` in evaluation order and map DM slices via
    ``dm_index_lists``.
    """

    def __init__(
        self,
        *,
        name: str,
        objective_points: np.ndarray,
        dm_index_lists: Sequence[Sequence[int]],
        common_ps: Optional[np.ndarray] = None,
        notes: str = "",
        known_ps: bool = True,
    ) -> None:
        objective_points = np.asarray(objective_points, dtype=float)
        # Build reference_points as consecutive blocks for the base class API,
        # but override evaluation to preserve MATLAB objective order.
        refs = {
            dm: objective_points[list(idxs)]
            for dm, idxs in enumerate(dm_index_lists)
        }
        super().__init__(
            name=name,
            reference_points=refs,
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS if common_ps is not None else CommonPSStatus.UNKNOWN,
            known_ps=known_ps,
            known_pf=known_ps,
            notes=notes,
        )
        self._objective_points = objective_points
        self._dm_index_lists = [list(idxs) for idxs in dm_index_lists]
        self._common_ps = None if common_ps is None else np.asarray(common_ps, dtype=float)

        # Rebuild slices to match MATLAB concatenated order.
        # Base class concatenates by DM blocks; we need MATLAB order for evaluate().
        # Keep ownership via dm_index_lists pointing into MATLAB-ordered F.
        start = 0
        self._matlab_order = True
        self._dm_slices = {}
        # For evaluate_dm we extract by indices into MATLAB F.
        self._dm_obj_indices = {
            dm: np.asarray(idxs, dtype=int) for dm, idxs in enumerate(self._dm_index_lists)
        }
        # Expose slices as contiguous only if indices are contiguous; else store notes.
        for dm, idxs in self._dm_obj_indices.items():
            if np.all(np.diff(idxs) == 1):
                self._dm_slices[dm] = slice(int(idxs[0]), int(idxs[-1]) + 1)
            else:
                # Non-contiguous: keep a synthetic contiguous remap in metadata.
                self._dm_slices[dm] = slice(start, start + len(idxs))
            start += len(idxs)
        # Force contiguous ownership representation for research API:
        # F is stored as [DM0 | DM1 | ...] (reordered from MATLAB if needed).
        self._use_dm_block_order = True
        # Rebuild standard contiguous slices
        start = 0
        self._dm_slices = {}
        for dm, k in enumerate(self.n_obj_per_dm):
            self._dm_slices[dm] = slice(start, start + k)
            start += k

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        # Evaluate in DM-block order for consistent ownership API.
        from fairmoo_benchmarks.utils import euclidean_distances_to_points

        blocks = [
            euclidean_distances_to_points(X, self.reference_points[dm])
            for dm in range(self.n_dm)
        ]
        return np.concatenate(blocks, axis=1)

    def evaluate_matlab_order(self, X: np.ndarray) -> np.ndarray:
        """Evaluate with the exact objective concatenation order of the MATLAB code."""
        from fairmoo_benchmarks.utils import euclidean_distances_to_points

        X2, was_1d = self._as_2d(X)
        F = euclidean_distances_to_points(X2, self._objective_points)
        return F[0] if was_1d else F

    def get_common_pareto_set(self, n_points: int = 1000) -> Optional[np.ndarray]:
        if self._common_ps is None:
            return None
        ps = np.asarray(self._common_ps, dtype=float)
        if ps.ndim == 1:
            ps = ps.reshape(1, -1)
        if ps.shape[0] == 1 and n_points > 1:
            return np.repeat(ps, n_points, axis=0)
        return ps

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return self.get_common_pareto_set(n_points=n_points)
        return super().get_pareto_set(dm=dm, n_points=n_points)


def _she_problem(
    name: str,
    refs: dict[int, np.ndarray],
    *,
    common_ps: Optional[np.ndarray] = None,
    notes: str = "",
    ps_geometry: Optional[dict] = None,
) -> DistanceBasedMultiPartyProblem:
    return DistanceBasedMultiPartyProblem(
        name=name,
        reference_points=refs,
        xl=(0.0, 0.0),
        xu=(100.0, 100.0),
        family="MPDMP",
        source=SHE2023_SOURCE,
        year=2023,
        common_ps_exists=CommonPSStatus.EXISTS if common_ps is not None else CommonPSStatus.UNKNOWN,
        known_ps=True,
        known_pf=True,
        notes=notes,
        ps_geometry=ps_geometry,
        metadata={"common_ps_points": None if common_ps is None else np.asarray(common_ps).tolist()},
    )


class MPDMP1(_InterleavedDistanceProblem):
    """Two crossed diagonals; MATLAB order [A,C,B,D] with DM={1:2,3:4} => (A,C),(B,D)."""

    def __init__(self) -> None:
        # Points: A(30,70), B(70,70), C(70,30), D(30,30)
        # MATLAB distance = [fA, fC, fB, fD]; DM1->[1,2]=A,C; DM2->[3,4]=B,D
        pts = np.array([[30.0, 70.0], [70.0, 30.0], [70.0, 70.0], [30.0, 30.0]])
        super().__init__(
            name="MPDMP1",
            objective_points=np.array([[30, 70], [70, 30], [70, 70], [30, 30]], dtype=float),
            dm_index_lists=[[0, 1], [2, 3]],
            common_ps=np.array([[50.0, 50.0]]),
            notes="square.m: DM1=(A,C), DM2=(B,D). Common PS=(50,50).",
        )


class MPDMP2(_InterleavedDistanceProblem):
    def __init__(self) -> None:
        # trapezoid1: A(30,70), B(50,70), C(70,30), D(30,30)
        # distance [fA,fC,fB,fD]; DM default {1:2,3:4}
        super().__init__(
            name="MPDMP2",
            objective_points=np.array([[30, 70], [70, 30], [50, 70], [30, 30]], dtype=float),
            dm_index_lists=[[0, 1], [2, 3]],
            common_ps=np.array([[130.0 / 3.0, 170.0 / 3.0]]),
            notes="trapezoid1.m. Common PS=(130/3, 170/3).",
        )


class MPDMP3(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        line = np.array([[30.0, 50.0], [70.0, 50.0]])
        tri = matlab_nsidedpoly_vertices(3, [50.0, 40.0], radius=20.0)
        super().__init__(
            name="MPDMP3",
            reference_points={0: line, 1: tri},
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes="LinearMap.m + nsidedpoly(3, Center=[50,40], Radius=20). DM={1:2,3:5}.",
            ps_geometry={0: "Line segment", 1: "Triangle"},
        )

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is not None:
            return super().get_pareto_set(dm=dm, n_points=n_points)
        # Common PS: segment of the line inside the triangle
        line = linspace_segment([30, 50], [70, 50], max(n_points * 5, 5000))
        tri = self.reference_points[1]
        # Point-in-triangle via barycentric
        def in_tri(P):
            A, B, C = tri
            v0, v1, v2 = C - A, B - A, P - A
            dot00 = np.dot(v0, v0)
            dot01 = np.dot(v0, v1)
            dot02 = np.dot(v0, v2)
            dot11 = np.dot(v1, v1)
            dot12 = np.dot(v1, v2)
            inv = 1.0 / (dot00 * dot11 - dot01 * dot01)
            u = (dot11 * dot02 - dot01 * dot12) * inv
            v = (dot00 * dot12 - dot01 * dot02) * inv
            return (u >= -1e-10) & (v >= -1e-10) & (u + v <= 1 + 1e-10)

        mask = np.array([in_tri(p) for p in line])
        ps = line[mask]
        if ps.shape[0] == 0:
            return ps
        idx = np.linspace(0, ps.shape[0] - 1, n_points).astype(int)
        return ps[idx]

    def get_common_pareto_set(self, n_points: int = 1000) -> Optional[np.ndarray]:
        return self.get_pareto_set(dm=None, n_points=n_points)


class MPDMP4(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        p1 = np.array([[50.0, 70.0], [30.0, 40.0], [70.0, 40.0]])
        p2 = np.array([[50.0, 40.0], [30.0, 10.0], [70.0, 10.0]])
        super().__init__(
            name="MPDMP4",
            reference_points={0: p1, 1: p2},
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes="Explicit polyshape vertices in MPDMP4.m. Common PS=(50,40).",
            ps_geometry={0: "Triangle", 1: "Triangle"},
        )
        self._common = np.array([[50.0, 40.0]])

    def get_common_pareto_set(self, n_points: int = 1000) -> Optional[np.ndarray]:
        return np.repeat(self._common, n_points, axis=0)

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return self.get_common_pareto_set(n_points)
        return super().get_pareto_set(dm=dm, n_points=n_points)


class MPDMP5(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        p1 = matlab_nsidedpoly_vertices(3, [39.0, 40.0], radius=40.0)
        p2 = matlab_nsidedpoly_vertices(3, [60.0, 20.0], radius=40.0)
        super().__init__(
            name="MPDMP5",
            reference_points={0: p1, 1: p2},
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes="nsidedpoly triangles Center=[39,40]/[60,20], Radius=40. Vertices order: MATLAB nsidedpoly.",
            ps_geometry={0: "Triangle", 1: "Triangle"},
        )


class MPDMP6(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        p1 = matlab_nsidedpoly_vertices(4, [38.0, 50.0], side_length=24.0)
        p2 = matlab_nsidedpoly_vertices(4, [60.0, 50.0], side_length=20.0)
        super().__init__(
            name="MPDMP6",
            reference_points={0: p1, 1: p2},
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes="Two squares with common edge; MATLAB PS x=50, y in [40,60].",
            ps_geometry={0: "Square", 1: "Square"},
        )

    def get_common_pareto_set(self, n_points: int = 1000) -> Optional[np.ndarray]:
        y = np.linspace(40.0, 60.0, n_points)
        return np.column_stack([np.full(n_points, 50.0), y])

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return self.get_common_pareto_set(n_points)
        return super().get_pareto_set(dm=dm, n_points=n_points)


class MPDMP7(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        p1 = matlab_nsidedpoly_vertices(4, [30.0, 50.0], side_length=40.0)
        p2 = matlab_nsidedpoly_vertices(4, [60.0, 40.0], side_length=40.0)
        super().__init__(
            name="MPDMP7",
            reference_points={0: p1, 1: p2},
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes="Overlapped squares nsidedpoly SideLength=40.",
            ps_geometry={0: "Square", 1: "Square"},
        )


class MPDMP8(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        p1 = matlab_nsidedpoly_vertices(5, [40.0, 50.0], radius=20.0)
        p2 = matlab_nsidedpoly_vertices(5, [60.0, 45.0], radius=20.0)
        super().__init__(
            name="MPDMP8",
            reference_points={0: p1, 1: p2},
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes="Overlapped pentagons Radius=20.",
            ps_geometry={0: "Pentagon", 1: "Pentagon"},
        )


class MPDMP9(_InterleavedDistanceProblem):
    def __init__(self) -> None:
        # square1: [fA,fC,fB,fD,fE,fF]; DM={1:2,3:4,5:6}
        # A(30,70), C(70,30), B(70,70), D(30,30), E(30,50), F(70,50)
        super().__init__(
            name="MPDMP9",
            objective_points=np.array(
                [[30, 70], [70, 30], [70, 70], [30, 30], [30, 50], [70, 50]], dtype=float
            ),
            dm_index_lists=[[0, 1], [2, 3], [4, 5]],
            common_ps=np.array([[50.0, 50.0]]),
            notes="square1.m three DMs. Common PS=(50,50).",
        )


class MPDMP10(_InterleavedDistanceProblem):
    def __init__(self) -> None:
        # Map10: [fA,fC,fB,fD] + square vertices; DM={1:2,3:4,5:8}
        sq = matlab_nsidedpoly_vertices(4, [50.0, 50.0], side_length=30.0)
        obj = np.vstack(
            [
                np.array([[30.0, 70.0], [70.0, 30.0], [70.0, 70.0], [30.0, 30.0]]),
                sq,
            ]
        )
        super().__init__(
            name="MPDMP10",
            objective_points=obj,
            dm_index_lists=[[0, 1], [2, 3], [4, 5, 6, 7]],
            common_ps=np.array([[50.0, 50.0]]),
            notes="Map10.m: two diagonals + central square. DM3 owns square vertices.",
        )


class MPDMP11(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        refs = {
            0: matlab_nsidedpoly_vertices(3, [30.0, 40.0], radius=20.0),
            1: matlab_nsidedpoly_vertices(3, [50.0, 40.0], radius=20.0),
            2: matlab_nsidedpoly_vertices(3, [40.0, 45.0], radius=20.0),
        }
        super().__init__(
            name="MPDMP11",
            reference_points=refs,
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes=(
                "Three triangles. MATLAB draw() marks PS polygon "
                "[35.56624,40,44.43375]x[35,42.6795,35] — used as approximate common PS."
            ),
            ps_geometry={0: "Triangle", 1: "Triangle", 2: "Triangle"},
        )
        self._common_poly = np.array(
            [[35.56624, 35.0], [40.0, 42.6795], [44.43375, 35.0]], dtype=float
        )

    def get_common_pareto_set(self, n_points: int = 1000) -> Optional[np.ndarray]:
        from fairmoo_benchmarks.utils import sample_convex_polygon

        return sample_convex_polygon(self._common_poly, n_points)

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return self.get_common_pareto_set(n_points)
        return super().get_pareto_set(dm=dm, n_points=n_points)


class MPDMP12(DistanceBasedMultiPartyProblem):
    def __init__(self) -> None:
        refs = {
            0: matlab_nsidedpoly_vertices(4, [30.0, 40.0], radius=20.0),
            1: matlab_nsidedpoly_vertices(4, [50.0, 40.0], radius=20.0),
            2: matlab_nsidedpoly_vertices(4, [40.0, 50.0], radius=20.0),
        }
        super().__init__(
            name="MPDMP12",
            reference_points=refs,
            xl=(0.0, 0.0),
            xu=(100.0, 100.0),
            family="MPDMP",
            source=SHE2023_SOURCE,
            year=2023,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes=(
                "Three squares (nsidedpoly Radius=20). MATLAB draw() PS rectangle "
                "[35.8579,44.1421]^2 used as approximate common PS."
            ),
            ps_geometry={0: "Square", 1: "Square", 2: "Square"},
        )
        self._common_rect = np.array(
            [
                [35.8579, 35.8579],
                [35.8579, 54.1421],
                [44.1421, 54.1421],
                [44.1421, 35.8579],
            ],
            dtype=float,
        )

    def get_common_pareto_set(self, n_points: int = 1000) -> Optional[np.ndarray]:
        from fairmoo_benchmarks.utils import sample_convex_polygon

        return sample_convex_polygon(self._common_rect, n_points)

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return self.get_common_pareto_set(n_points)
        return super().get_pareto_set(dm=dm, n_points=n_points)

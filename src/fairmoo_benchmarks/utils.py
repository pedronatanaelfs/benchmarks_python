"""Utility helpers for multi-party benchmarks."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def ensure_2d(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        return X.reshape(1, -1)
    if X.ndim != 2:
        raise ValueError(f"Expected 1D/2D array, got shape {X.shape}")
    return X


def euclidean_distances_to_points(X: np.ndarray, points: np.ndarray) -> np.ndarray:
    """Compute Euclidean distances from each row of ``X`` to each reference point.

    Parameters
    ----------
    X :
        Shape ``(N, d)``.
    points :
        Shape ``(K, d)``.

    Returns
    -------
    ndarray
        Shape ``(N, K)`` with ``F[n, k] = ||X[n] - points[k]||_2``.
    """
    X = np.asarray(X, dtype=float)
    points = np.asarray(points, dtype=float)
    if points.ndim != 2:
        raise ValueError("points must be 2D")
    # (N, 1, d) - (1, K, d) -> (N, K, d)
    diff = X[:, None, :] - points[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=-1))


def linspace_segment(
    a: Sequence[float], b: Sequence[float], n_points: int
) -> np.ndarray:
    """Sample ``n_points`` along the segment from ``a`` to ``b`` (inclusive)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    t = np.linspace(0.0, 1.0, int(n_points))
    return (1.0 - t)[:, None] * a[None, :] + t[:, None] * b[None, :]


def sample_convex_polygon(vertices: np.ndarray, n_points: int, seed: int = 42) -> np.ndarray:
    """Sample points uniformly (approx.) inside a convex polygon via triangulation barycenters.

    For validation/visualization — not a formal PF generator for non-triangle polygons.
    """
    verts = np.asarray(vertices, dtype=float)
    if verts.shape[0] < 3:
        raise ValueError("Need at least 3 vertices")
    rng = np.random.default_rng(seed)
    # Fan triangulation from vertex 0
    triangles = []
    for i in range(1, verts.shape[0] - 1):
        triangles.append(verts[[0, i, i + 1]])
    triangles = np.asarray(triangles)
    # Area weights
    areas = []
    for tri in triangles:
        # 2D cross magnitude (NumPy >=2 rejects np.cross on 2-vectors)
        d1 = tri[1] - tri[0]
        d2 = tri[2] - tri[0]
        areas.append(0.5 * abs(d1[0] * d2[1] - d1[1] * d2[0]))
    areas = np.asarray(areas, dtype=float)
    areas = areas / areas.sum()
    choices = rng.choice(len(triangles), size=n_points, p=areas)
    out = np.empty((n_points, verts.shape[1]), dtype=float)
    for i, ti in enumerate(choices):
        r1, r2 = rng.random(), rng.random()
        if r1 + r2 > 1.0:
            r1, r2 = 1.0 - r1, 1.0 - r2
        r3 = 1.0 - r1 - r2
        out[i] = r1 * triangles[ti, 0] + r2 * triangles[ti, 1] + r3 * triangles[ti, 2]
    return out


def matlab_grid_polygon_intersection(
    polygons: Sequence[np.ndarray], grid_size: int = 1000
) -> np.ndarray:
    """Reproduce ``polygon.PS``: a MATLAB-ordered grid inside all polygons."""
    axis = np.linspace(0.0, 100.0, int(grid_size))
    X, Y = np.meshgrid(axis, axis)
    points = np.column_stack([X.ravel(order="F"), Y.ravel(order="F")])
    inside = np.ones(points.shape[0], dtype=bool)

    for vertices in polygons:
        vertices = np.asarray(vertices, dtype=float)
        edges = np.roll(vertices, -1, axis=0) - vertices
        rel = points[:, None, :] - vertices[None, :, :]
        cross = edges[None, :, 0] * rel[:, :, 1] - edges[None, :, 1] * rel[:, :, 0]
        tolerance = 1e-10
        inside &= np.all(cross >= -tolerance, axis=1) | np.all(
            cross <= tolerance, axis=1
        )
    return points[inside]


def matlab_nsidedpoly_vertices(
    n: int,
    center: Sequence[float],
    *,
    radius: float | None = None,
    side_length: float | None = None,
) -> np.ndarray:
    """Return vertices in MATLAB ``nsidedpoly(...).Vertices`` order.

    Orientation and ordering were recovered from licensed-MATLAB evaluations
    of MPDMP3–8 and MPDMP10–12. Odd polygons have a top vertex; even polygons
    use a ``π/n`` rotation. ``polyshape.Vertices`` then reports the boundary
    clockwise, beginning at the lowest/left tied vertex.
    """
    if (radius is None) == (side_length is None):
        raise ValueError("Provide exactly one of radius or side_length")
    if side_length is not None:
        radius = float(side_length) / (2.0 * np.sin(np.pi / n))
    assert radius is not None
    cx, cy = float(center[0]), float(center[1])
    start = np.pi / 2.0 if n % 2 else np.pi / n
    angles = start + 2.0 * np.pi * np.arange(n) / n
    vertices = np.column_stack(
        [cx + radius * np.cos(angles), cy + radius * np.sin(angles)]
    )

    # Floating-point trig makes theoretically tied x coordinates differ by a
    # few ulps, so select the MATLAB start vertex using rounded coordinates.
    rounded = np.round(vertices, decimals=12)
    start_index = int(np.lexsort((rounded[:, 0], rounded[:, 1]))[0])
    order = (start_index - np.arange(n)) % n
    return vertices[order]

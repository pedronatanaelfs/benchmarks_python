"""Concession / Chebyshev offset from official ``nash_score/compute_offset_to_pf.m``."""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist


def min_cdist(
    a: np.ndarray,
    b: np.ndarray,
    *,
    metric: str = "euclidean",
    chunk: int = 256,
) -> np.ndarray:
    """Row-wise minimum distance; chunked to avoid n×m broadcasts."""
    a = np.atleast_2d(np.asarray(a, dtype=float))
    b = np.atleast_2d(np.asarray(b, dtype=float))
    if a.shape[0] == 0:
        return np.zeros(0)
    if b.shape[0] == 0:
        return np.full(a.shape[0], np.inf)
    out = np.empty(a.shape[0])
    for i in range(0, a.shape[0], chunk):
        out[i : i + chunk] = cdist(a[i : i + chunk], b, metric=metric).min(axis=1)
    return out


def offset_to_pf(
    points: np.ndarray,
    pf: np.ndarray,
    f_max: np.ndarray,
    max_pf_size: int = 5000,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    points = np.atleast_2d(np.asarray(points, dtype=float))
    pf = np.atleast_2d(np.asarray(pf, dtype=float))
    f_max = np.asarray(f_max, dtype=float).reshape(-1)
    f_max = np.where(f_max == 0.0, np.finfo(float).eps, f_max)
    n_points = points.shape[0]
    if n_points == 0:
        return np.zeros(0)
    if pf.shape[0] == 0:
        return np.full(n_points, np.inf)
    if pf.shape[0] > max_pf_size:
        rng = rng or np.random.default_rng(0)
        idx = rng.choice(pf.shape[0], size=max_pf_size, replace=False)
        pf = pf[idx]
    # Chebyshev distance in f_max-normalized space == MATLAB compute_offset_to_pf.m
    return min_cdist(points / f_max, pf / f_max, metric="chebyshev")


def sample_rows(
    X: np.ndarray, max_rows: int, rng: np.random.Generator | None = None
) -> np.ndarray:
    if X.shape[0] <= max_rows:
        return X
    rng = rng or np.random.default_rng(0)
    idx = rng.choice(X.shape[0], size=max_rows, replace=False)
    return X[idx]

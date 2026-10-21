"""Party-wise IGD.

Matches PlatEMO ``pdist2`` Euclidean IGD used by OptMPNDS ``IGD_GD.m``
and She ``Metrics/IGD.m`` on a single DM's objective block.
"""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist


def igd(reference: np.ndarray, approximation: np.ndarray) -> float:
    if reference.size == 0:
        return np.nan
    if approximation.size == 0:
        return np.inf
    ref = np.atleast_2d(np.asarray(reference, dtype=float))
    app = np.atleast_2d(np.asarray(approximation, dtype=float))
    return float(cdist(ref, app, metric="euclidean").min(axis=1).mean())


def party_igd(
    F: np.ndarray, pf_per_dm: list[np.ndarray], slices: list[slice]
) -> np.ndarray:
    F = np.atleast_2d(np.asarray(F, dtype=float))
    values = np.full(len(slices), np.nan)
    for i, sl in enumerate(slices):
        values[i] = igd(pf_per_dm[i], F[:, sl])
    return values

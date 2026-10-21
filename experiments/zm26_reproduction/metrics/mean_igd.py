"""meanIGD: arithmetic mean of party-wise IGD (ZM26 Section V-A3)."""

from __future__ import annotations

import numpy as np

from .igd import party_igd


def mean_igd(F: np.ndarray, pf_per_dm: list[np.ndarray], slices: list[slice]) -> float:
    vals = party_igd(F, pf_per_dm, slices)
    return float(np.nanmean(vals))

"""Jain fairness index (Jain, Chiu & Hawe, 1984), used in ZM26 Appendix Table S-III."""

from __future__ import annotations

import numpy as np


def jain_index(values: np.ndarray) -> float:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return np.nan
    s = float(x.sum())
    q = float(np.square(x).sum())
    if q <= 0:
        return np.nan
    return (s * s) / (x.size * q)

"""Gini coefficient of a non-negative vector (ZM26 Appendix Table S-III)."""

from __future__ import annotations

import numpy as np


def gini_coefficient(values: np.ndarray) -> float:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return np.nan
    if np.any(x < 0):
        x = x - x.min()
    if x.size == 1:
        return 0.0
    x = np.sort(x)
    n = x.size
    tot = x.sum()
    if tot <= 0:
        return np.nan
    idx = np.arange(1, n + 1, dtype=float)
    return float((2.0 * np.sum(idx * x) / (n * tot)) - (n + 1.0) / n)

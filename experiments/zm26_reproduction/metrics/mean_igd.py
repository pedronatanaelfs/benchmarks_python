"""party_pf_meanIGD: arithmetic mean of party-wise geometric IGD.

Historically stored as ``meanIGD`` in ``results/raw/results.csv``.
That column is the research/diagnostic metric (each DM's sampled PF).

The ZM26 **reproduction** MPDMP metric is ``zm26_meanIGD`` in ``she_igd.py``
(She ``Metrics/IGD.m`` against MATLAB ``problem.PF()``).
"""

from __future__ import annotations

import numpy as np

from .igd import party_igd


def mean_igd(F: np.ndarray, pf_per_dm: list[np.ndarray], slices: list[slice]) -> float:
    vals = party_igd(F, pf_per_dm, slices)
    return float(np.nanmean(vals))

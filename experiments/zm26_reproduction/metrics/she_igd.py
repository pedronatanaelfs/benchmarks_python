"""She 2023 ``Metrics/IGD.m`` and the ZM26-reproduction MPDMP meanIGD.

She IGD.m
---------
For each decision maker, add ``pdist2(PF(:,DM{i}), obj(:,DM{i}))``. Then
``grades = min(dis, [], 2); score = mean(grades)``.

This is **not** the arithmetic mean of party-wise IGDs. It is a single
IGD against the concatenated problem ``PF()`` with party distances summed
before the min.

ZM26 Table III numbers for MPDMP4 match this definition with
``MPDMP4.PF() = CalObj([50,40])``, not a sampled party triangle front.

Metric names
------------
``zm26_meanIGD``
    She IGD.m against MATLAB ``problem.PF()`` (MPDMP reproduction metric).
``party_pf_meanIGD``
    Mean of party-wise Euclidean IGD against each DM's geometric PF
    (research / diagnostic metric; previously stored as ``meanIGD``).
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy.spatial.distance import cdist

from .igd import party_igd
from .mean_igd import mean_igd as party_pf_meanIGD


def she_igd(F: np.ndarray, pf: np.ndarray, slices: Sequence[slice]) -> float:
    """MATLAB ``Metrics/IGD.m`` first returned value (the mean)."""
    F = np.atleast_2d(np.asarray(F, dtype=float))
    pf = np.atleast_2d(np.asarray(pf, dtype=float))
    if pf.size == 0 or F.size == 0:
        return np.nan
    dis = None
    for sl in slices:
        block = cdist(pf[:, sl], F[:, sl], metric="euclidean")
        dis = block if dis is None else dis + block
    return float(np.min(dis, axis=1).mean())


def zm26_meanIGD(F: np.ndarray, matlab_pf: np.ndarray, slices: Sequence[slice]) -> float:
    """ZM26 MPDMP reproduction metric: She IGD.m on MATLAB ``PF()``."""
    return she_igd(F, matlab_pf, slices)


__all__ = ["she_igd", "zm26_meanIGD", "party_pf_meanIGD", "party_igd", "mean_igd_alias"]


def mean_igd_alias(F, pf_per_dm, slices) -> float:
    """Backward-compatible name: party-wise geometric meanIGD."""
    return party_pf_meanIGD(F, pf_per_dm, slices)

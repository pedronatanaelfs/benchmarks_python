"""SBX+PM using explicit random arrays (MATLAB GA.m real-encoding order).

Does not modify the production operator. Two rate conventions:

- matlab_ga: Site = U < pro_m / D   (PlatEMO / She GA.m)
- python_production_mpdmp: Site = U < pro_m   (current ZM26 MPDMP setting)
"""

from __future__ import annotations

import numpy as np


def sbx_pm_from_stream(
    parents: np.ndarray,
    xl: np.ndarray,
    xu: np.ndarray,
    mu_sbx: np.ndarray,
    sign01: np.ndarray,
    beta_skip: np.ndarray,
    proc: np.ndarray,
    site_u: np.ndarray,
    mu_mut: np.ndarray,
    *,
    pro_c: float = 1.0,
    dis_c: float = 15.0,
    pro_m: float = 0.5,
    dis_m: float = 20.0,
    mutation_as_expectation: bool = True,
) -> np.ndarray:
    n_all, d = parents.shape
    n = n_all // 2
    p1 = parents[:n]
    p2 = parents[n : 2 * n]
    mu = np.asarray(mu_sbx, dtype=float)
    beta = np.empty((n, d))
    mask = mu <= 0.5
    beta[mask] = (2.0 * mu[mask]) ** (1.0 / (dis_c + 1.0))
    beta[~mask] = (2.0 - 2.0 * mu[~mask]) ** (-2.0 / (dis_c + 1.0))
    beta *= (-1.0) ** np.asarray(sign01, dtype=int)
    beta[np.asarray(beta_skip) < 0.5] = 1.0
    proc = np.asarray(proc, dtype=float).reshape(-1)
    beta[proc > pro_c, :] = 1.0
    off = np.vstack(
        [
            0.5 * (p1 + p2) + 0.5 * beta * (p1 - p2),
            0.5 * (p1 + p2) - 0.5 * beta * (p1 - p2),
        ]
    )
    off = np.clip(off, xl, xu)
    rate = (pro_m / d) if mutation_as_expectation else pro_m
    site = np.asarray(site_u) < rate
    mu2 = np.asarray(mu_mut, dtype=float)
    span = xu - xl
    temp = site & (mu2 <= 0.5)
    delta1 = (off - xl) / np.where(span == 0, 1.0, span)
    delta2 = (xu - off) / np.where(span == 0, 1.0, span)
    span_b = np.broadcast_to(span, off.shape)
    off = off.copy()
    off[temp] = off[temp] + span_b[temp] * (
        (2.0 * mu2[temp] + (1.0 - 2.0 * mu2[temp]) * (1.0 - delta1[temp]) ** (dis_m + 1.0))
        ** (1.0 / (dis_m + 1.0))
        - 1.0
    )
    temp = site & (mu2 > 0.5)
    off[temp] = off[temp] + span_b[temp] * (
        1.0
        - (
            2.0 * (1.0 - mu2[temp])
            + 2.0 * (mu2[temp] - 0.5) * (1.0 - delta2[temp]) ** (dis_m + 1.0)
        )
        ** (1.0 / (dis_m + 1.0))
    )
    pre_clip = off.copy()
    post = np.clip(off, xl, xu)
    return post, pre_clip

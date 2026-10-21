"""ZM26 Nash-product evaluation.

Two formulas are implemented and stored separately:

1. ``matlab_exp`` — official ``nash-score/nash_score.m``:
   ``u_m = exp(-L_m)``, ``Psi = prod u_m``.
2. ``paper_C`` — ZM26 Theorem 1 / Appendix S-I:
   ``u_m = C - L_m``, ``Psi = prod u_m``.

``L_m = mu_m + lambda_m * mean(mu_ref * phi)`` follows the MATLAB code
(mean penalty, Chebyshev offset). The paper text also writes a sum; that
difference is recorded in PAPER_PARAMETER_AUDIT.md.

Unequal objectives-per-DM are supported via slices. Official MATLAB
``nash_score.m`` requires ``M % dm_num == 0``; ZM26 Table III still reports
MPDMP3/10, so slices are required for a faithful experimental reproduction.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .concession import min_cdist, offset_to_pf, sample_rows
from .igd import igd


@dataclass
class NashDetails:
    mu: np.ndarray
    L_pen: np.ndarray
    L: np.ndarray
    concession_mean: np.ndarray
    penalty_mean: np.ndarray
    utility_exp: np.ndarray
    utility_C: np.ndarray
    nash_exp: float
    nash_C: float
    log_nash_C: float
    C: float
    lambda_: np.ndarray
    epsilon: np.ndarray
    max_offset: np.ndarray
    mu_ref: np.ndarray


def _fmax(pf: np.ndarray, pop: np.ndarray) -> np.ndarray:
    combined = np.vstack([pf, pop]) if pop.size else pf
    mx = combined.max(axis=0)
    mx[mx == 0] = np.finfo(float).eps
    return mx


def nash_components(
    F: np.ndarray,
    pf_per_dm: list[np.ndarray],
    slices: list[slice],
    epsilon: np.ndarray,
    lambda_: np.ndarray | float,
    *,
    C: float = 1.0,
    pf_sample_size: int = 2000,
    offset_pf_sample: int = 5000,
    rng: np.random.Generator | None = None,
) -> NashDetails:
    rng = rng or np.random.default_rng(0)
    F = np.atleast_2d(np.asarray(F, dtype=float))
    n_dm = len(slices)
    epsilon = np.asarray(epsilon, dtype=float).reshape(n_dm)
    if np.isscalar(lambda_):
        lam = np.full(n_dm, float(lambda_))
    else:
        lam = np.asarray(lambda_, dtype=float).reshape(n_dm)

    pop = [F[:, sl] for sl in slices]
    pf = [np.atleast_2d(np.asarray(p, dtype=float)) for p in pf_per_dm]
    fmax = [_fmax(pf[m], pop[m]) for m in range(n_dm)]
    pf_s = [sample_rows(pf[m], pf_sample_size, rng) for m in range(n_dm)]

    max_offset = np.zeros(n_dm)
    mu_ref = np.zeros(n_dm)
    for m in range(n_dm):
        other_off = []
        other_dist = []
        for k in range(n_dm):
            if k == m:
                continue
            other = sample_rows(pf[k], pf_sample_size, rng)
            if other.shape[1] != pf_s[m].shape[1]:
                # Unequal n_obj_per_dm (e.g. MPDMP3/10). MATLAB nash_score.m
                # requires equal blocks; skip cross-space PF geometry.
                continue
            other_off.append(offset_to_pf(other, pf_s[m], fmax[m], offset_pf_sample, rng))
            other_dist.append(min_cdist(other, pf_s[m], metric="euclidean"))
        if other_off:
            max_offset[m] = max(float(np.max(np.concatenate(other_off))), np.finfo(float).eps)
        else:
            max_offset[m] = np.finfo(float).eps
        if other_dist:
            mu_ref[m] = float(np.max(np.concatenate(other_dist)))
        if mu_ref[m] < 1e-10:
            mu_ref[m] = 1.0

    mu = np.zeros(n_dm)
    L_pen = np.zeros(n_dm)
    concession_mean = np.zeros(n_dm)
    penalty_mean = np.zeros(n_dm)
    for m in range(n_dm):
        mu[m] = igd(pf_s[m], pop[m])
        offs = offset_to_pf(pop[m], pf_s[m], fmax[m], offset_pf_sample, rng)
        conc = offs / max_offset[m]
        phi = np.maximum(0.0, conc - epsilon[m])
        point_pen = mu_ref[m] * phi
        L_pen[m] = float(point_pen.mean()) if point_pen.size else 0.0
        concession_mean[m] = float(conc.mean()) if conc.size else np.nan
        penalty_mean[m] = L_pen[m]

    L = mu + lam * L_pen
    util_exp = np.exp(-L)
    util_C = C - L
    nash_exp = float(np.prod(util_exp)) if np.all(np.isfinite(util_exp)) else 0.0
    if np.any(util_C <= 0) or not np.all(np.isfinite(util_C)):
        nash_C = 0.0
        log_nash = np.nan
    else:
        nash_C = float(np.prod(util_C))
        log_nash = float(np.log(nash_C))
    return NashDetails(
        mu=mu,
        L_pen=L_pen,
        L=L,
        concession_mean=concession_mean,
        penalty_mean=penalty_mean,
        utility_exp=util_exp,
        utility_C=util_C,
        nash_exp=nash_exp,
        nash_C=nash_C,
        log_nash_C=log_nash,
        C=float(C),
        lambda_=lam,
        epsilon=epsilon,
        max_offset=max_offset,
        mu_ref=mu_ref,
    )


def estimate_lambda(
    pf_per_dm: list[np.ndarray],
    slices: list[slice],
    epsilon: np.ndarray,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Appendix S-II formula, implemented with IGD and concession of other PFs."""
    rng = rng or np.random.default_rng(0)
    n_dm = len(slices)
    epsilon = np.asarray(epsilon, dtype=float).reshape(n_dm)
    pf = [np.atleast_2d(np.asarray(p, dtype=float)) for p in pf_per_dm]
    lam = np.ones(n_dm)
    for m in range(n_dm):
        others = [
            pf[k]
            for k in range(n_dm)
            if k != m and pf[k].shape[1] == pf[m].shape[1]
        ]
        if not others or pf[m].size == 0:
            continue
        other = np.vstack(others)
        fmax = _fmax(pf[m], other)
        offs = offset_to_pf(other, pf[m], fmax, rng=rng)
        max_off = max(float(offs.max()), np.finfo(float).eps) if offs.size else np.finfo(float).eps
        igds = min_cdist(other, pf[m], metric="euclidean")
        gammas = offs / max_off
        if igds.size == 0:
            continue
        delta = float(igds.max())
        denom = gammas - epsilon[m]
        numer = delta - igds
        valid = denom > 1e-12
        if valid.any():
            lam[m] = max(float(np.max(numer[valid] / denom[valid])), 0.0)
        else:
            lam[m] = 1.0
    return lam

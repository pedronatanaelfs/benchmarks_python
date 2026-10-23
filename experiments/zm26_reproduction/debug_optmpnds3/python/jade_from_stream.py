"""One JADE2 generation from shared arrays. Diagnostic only."""

from __future__ import annotations

import numpy as np

from experiments.zm26_reproduction.algorithms.optmpnds3 import _mp_dominates, _update_archive
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import (
    envsel_optmpnds3,
    matlab_get_best_index,
    python_pbest_index,
)


def jade_generation(
    X,
    F,
    archive_x,
    archive_f,
    cr,
    Fs,
    pbest_k,
    i1,
    i2,
    jrand,
    mask_u,
    xl,
    xu,
    slices,
    n_survive: int,
    *,
    matlab_pbest: bool,
    matlab_parent2_retry: bool,
    matlab_s_from_survivors: bool,
    matlab_post_envsel_archive: bool,
    extras_cr=None,
    extras_f=None,
):
    n, d = X.shape
    if extras_cr is None:
        extras_cr = np.zeros(n)
        extras_f = np.zeros(n)
    front_now = None
    crowd_now = None
    # fronts/crowd must be supplied by caller via pbest_k acting on current ranking
    from experiments.zm26_reproduction.algorithms.operators import crowding_entropy, plnds

    front_now, _ = plnds(F, slices, n)
    crowd_now = crowding_entropy(F, front_now)
    pool_x = X if archive_x.shape[0] == 0 else np.vstack([X, archive_x])
    pool_f = F if archive_x.shape[0] == 0 else np.vstack([F, archive_f])
    off_x = np.empty_like(X)
    for i in range(n):
        k = int(pbest_k[i])
        k = max(1, min(k, max(int(np.ceil(n * 0.05)), 1)))
        pb_i = (
            matlab_get_best_index(front_now, crowd_now, k)
            if matlab_pbest
            else python_pbest_index(front_now, crowd_now, k)
        )
        a = int(i1[i]) % n
        if a == i and n > 1:
            a = (a + 1) % n
        b = int(i2[i]) % pool_x.shape[0]
        if matlab_parent2_retry:
            guard = 0
            while np.allclose(pool_x[b], X[a]) and guard < pool_x.shape[0] + 3:
                b = (b + 1) % pool_x.shape[0]
                guard += 1
        trial = X[i] + Fs[i] * (X[pb_i] - X[i]) + Fs[i] * (pool_x[b] - X[a])
        mask = mask_u[i] < cr[i]
        mask[int(jrand[i]) % d] = True
        child = np.where(mask, trial, X[i])
        off_x[i] = np.clip(child, xl, xu)
    return off_x, front_now, crowd_now, extras_cr, extras_f


def apply_dominance_and_select(
    X,
    F,
    off_x,
    off_f,
    archive_x,
    archive_f,
    cr,
    Fs,
    extras_cr,
    extras_f,
    slices,
    n_cap,
    n_survive,
    *,
    matlab_s_from_survivors: bool,
    matlab_post_envsel_archive: bool,
):
    chosen_x, chosen_f = [], []
    chosen_cr, chosen_fv = [], []
    s_cr, s_f = [], []
    for i in range(off_f.shape[0]):
        child_f = off_f[i]
        if _mp_dominates(child_f, F[i], slices):
            archive_x, archive_f = _update_archive(archive_x, archive_f, X[i], F[i], n_cap)
            chosen_x.append(off_x[i])
            chosen_f.append(child_f)
            chosen_cr.append(cr[i])
            chosen_fv.append(Fs[i])
            s_cr.append(cr[i])
            s_f.append(Fs[i])
        elif _mp_dominates(F[i], child_f, slices):
            archive_x, archive_f = _update_archive(
                archive_x, archive_f, off_x[i], child_f, n_cap
            )
            chosen_x.append(X[i])
            chosen_f.append(F[i])
            chosen_cr.append(extras_cr[i])
            chosen_fv.append(extras_f[i])
        else:
            chosen_x.extend([off_x[i], X[i]])
            chosen_f.extend([child_f, F[i]])
            chosen_cr.extend([cr[i], extras_cr[i]])
            chosen_fv.extend([Fs[i], extras_f[i]])
            s_cr.append(cr[i])
            s_f.append(Fs[i])
    Cx = np.vstack(chosen_x)
    Cf = np.vstack(chosen_f)
    Ccr = np.asarray(chosen_cr, dtype=float)
    Cfv = np.asarray(chosen_fv, dtype=float)
    Xs, Fs_s, front, crowd = envsel_optmpnds3(Cx, Cf, n_survive, slices)
    # map extras onto survivors by nearest F row (deterministic unique-preserving)
    surv_cr = np.zeros(Xs.shape[0])
    surv_fv = np.zeros(Xs.shape[0])
    for j in range(Xs.shape[0]):
        d = np.linalg.norm(Cf - Fs_s[j], axis=1)
        idx = int(np.argmin(d))
        surv_cr[j] = Ccr[idx]
        surv_fv[j] = Cfv[idx]
    if matlab_s_from_survivors:
        s_cr = surv_cr[surv_cr != 0].tolist()
        s_f = surv_fv[surv_fv != 0].tolist()
    if matlab_post_envsel_archive:
        # discarded = rows of Cx not among survivors (by X match)
        for i in range(Cx.shape[0]):
            if not np.any(np.all(np.isclose(Xs, Cx[i], atol=1e-12), axis=1)):
                archive_x, archive_f = _update_archive(
                    archive_x, archive_f, Cx[i], Cf[i], n_cap
                )
    return Xs, Fs_s, front, crowd, archive_x, archive_f, s_cr, s_f, surv_cr, surv_fv

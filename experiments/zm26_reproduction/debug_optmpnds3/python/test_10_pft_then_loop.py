"""From saved PFt init, run 30 JADE gens (production vs MATLAB-faithful). Independent RNG."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import load_matrix, save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import quality_row
from experiments.zm26_reproduction.debug_optmpnds3.python.jade_from_stream import (
    apply_dominance_and_select,
    jade_generation,
)
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT
from experiments.zm26_reproduction.runners.problem_setup import load_problem


def _loop(name, X, F, rng, flags, gens=30):
    problem, _, slices = load_problem(name)
    n = min(200, X.shape[0])
    if X.shape[0] > n:
        pick = rng.choice(X.shape[0], n, replace=False)
        X, F = X[pick], F[pick]
    d = X.shape[1]
    archive_x = np.zeros((0, d))
    archive_f = np.zeros((0, F.shape[1]))
    extras_cr = np.zeros(n)
    extras_fv = np.zeros(n)
    mu_cr = mu_f = 0.5
    c = 0.05
    rows = []
    for g in range(gens + 1):
        q = quality_row(name, X, F, tag=f"g{g}")
        q.update({"generation": g, "archive_size": int(archive_x.shape[0]), "mu_F": mu_f, "n": int(X.shape[0])})
        rows.append(q)
        if g == gens:
            break
        cr = np.clip(rng.normal(mu_cr, 0.1, size=n), 0, 1)
        Fs = rng.standard_cauchy(size=n) * 0.1 + mu_f
        while np.any(Fs <= 0):
            bad = Fs <= 0
            Fs[bad] = rng.standard_cauchy(size=int(bad.sum())) * 0.1 + mu_f
        Fs = np.clip(Fs, 0, 1)
        top = max(int(np.ceil(n * 0.05)), 1)
        k = rng.integers(1, top + 1, size=n)
        i1 = rng.integers(0, n, size=n)
        pool_n = n + archive_x.shape[0]
        i2 = rng.integers(0, max(pool_n, 1), size=n)
        jrand = rng.integers(0, d, size=n)
        mask = rng.random((n, d))
        off_x, _, _, extras_cr, extras_fv = jade_generation(
            X, F, archive_x, archive_f, cr, Fs, k, i1, i2, jrand, mask,
            problem.xl, problem.xu, slices, n,
            extras_cr=extras_cr, extras_f=extras_fv,
            matlab_pbest=flags["matlab_pbest"],
            matlab_parent2_retry=flags["matlab_parent2_retry"],
            matlab_s_from_survivors=flags["matlab_s_from_survivors"],
            matlab_post_envsel_archive=flags["matlab_post_envsel_archive"],
        )
        off_f = problem.evaluate(off_x)
        X, F, _, _, archive_x, archive_f, s_cr, s_f, extras_cr, extras_fv = apply_dominance_and_select(
            X, F, off_x, off_f, archive_x, archive_f, cr, Fs, extras_cr, extras_fv,
            slices, 2 * 200, 200,
            matlab_s_from_survivors=flags["matlab_s_from_survivors"],
            matlab_post_envsel_archive=flags["matlab_post_envsel_archive"],
        )
        n = X.shape[0]
        if s_cr:
            mu_cr = (1 - c) * mu_cr + c * float(np.mean(s_cr))
        if s_f:
            arr = np.asarray(s_f, dtype=float)
            mu_f = (1 - c) * mu_f + c * float(np.sum(arr**2) / np.sum(arr))
    return pd.DataFrame(rows)


def run() -> None:
    flags_prod = dict(matlab_pbest=False, matlab_parent2_retry=False, matlab_s_from_survivors=False, matlab_post_envsel_archive=False)
    flags_mat = dict(matlab_pbest=True, matlab_parent2_retry=True, matlab_s_from_survivors=True, matlab_post_envsel_archive=True)
    parts = []
    for name in ("MPDMP1", "MPDMP4"):
        X = load_matrix(PYTHON_OUT / f"{name.lower()}_init_X.csv")
        F = load_matrix(PYTHON_OUT / f"{name.lower()}_init_F.csv")
        for tag, flags in (("python_production", flags_prod), ("matlab_faithful", flags_mat)):
            rng = np.random.default_rng(7)
            df = _loop(name, X.copy(), F.copy(), rng, flags, gens=30)
            df["benchmark"] = name
            df["mode"] = tag
            parts.append(df)
            last = df.iloc[-1]
            print(f"{name} {tag}: g0 zm26={df.iloc[0].zm26_meanIGD:.4g} g30 zm26={last.zm26_meanIGD:.4g} dist={last.mean_dist_to_common_ps:.3g} n={int(last.n)}")
    save_table(PYTHON_OUT / "test_10_pft_then_loop.csv", pd.concat(parts, ignore_index=True))
    print("python test_10 done")


if __name__ == "__main__":
    run()

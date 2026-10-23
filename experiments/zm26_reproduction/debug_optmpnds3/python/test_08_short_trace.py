"""5-generation shared-stream trace, production vs MATLAB-faithful settings."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import load_matrix, save_matrix, save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import quality_row
from experiments.zm26_reproduction.debug_optmpnds3.python.jade_from_stream import (
    apply_dominance_and_select,
    jade_generation,
)
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT, SHARED
from experiments.zm26_reproduction.runners.problem_setup import load_problem


def _run_mode(tag: str, matlab_flags: dict) -> pd.DataFrame:
    problem, _, slices = load_problem("MPDMP1")
    X = load_matrix(SHARED / "short_X0.csv")
    F = problem.evaluate(X)
    n, d = X.shape
    archive_x = np.zeros((0, d))
    archive_f = np.zeros((0, F.shape[1]))
    extras_cr = np.zeros(n)
    extras_f = np.zeros(n)
    mu_cr, mu_f = 0.5, 0.5
    c = 0.05
    rows = []
    q0 = quality_row("MPDMP1", X, F, tag=f"{tag}_g0")
    q0.update(
        {
            "generation": 0,
            "mode": tag,
            "archive_size": 0,
            "mu_CR": mu_cr,
            "mu_F": mu_f,
            "n_s_cr": 0,
        }
    )
    rows.append(q0)
    save_matrix(PYTHON_OUT / f"test_08_{tag}_X_g0.csv", X, ["x1", "x2"])
    for g in range(5):
        cr = load_matrix(SHARED / f"g{g}_cr.csv").reshape(-1)
        Fs = load_matrix(SHARED / f"g{g}_F.csv").reshape(-1)
        k = load_matrix(SHARED / f"g{g}_pbest_k.csv").reshape(-1)
        i1 = load_matrix(SHARED / f"g{g}_i1.csv").reshape(-1)
        i2 = load_matrix(SHARED / f"g{g}_i2.csv").reshape(-1)
        jrand = load_matrix(SHARED / f"g{g}_jrand.csv").reshape(-1)
        mask = load_matrix(SHARED / f"g{g}_mask.csv")
        off_x, _, _, extras_cr, extras_f = jade_generation(
            X,
            F,
            archive_x,
            archive_f,
            cr,
            Fs,
            k,
            i1,
            i2,
            jrand,
            mask,
            problem.xl,
            problem.xu,
            slices,
            n,
            extras_cr=extras_cr,
            extras_f=extras_f,
            matlab_pbest=matlab_flags["matlab_pbest"],
            matlab_parent2_retry=matlab_flags["matlab_parent2_retry"],
            matlab_s_from_survivors=matlab_flags["matlab_s_from_survivors"],
            matlab_post_envsel_archive=matlab_flags["matlab_post_envsel_archive"],
        )
        off_f = problem.evaluate(off_x)
        X, F, front, crowd, archive_x, archive_f, s_cr, s_f, surv_cr, surv_fv = apply_dominance_and_select(
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
            2 * n,
            n,
            matlab_s_from_survivors=matlab_flags["matlab_s_from_survivors"],
            matlab_post_envsel_archive=matlab_flags["matlab_post_envsel_archive"],
        )
        extras_cr, extras_f = surv_cr, surv_fv
        if s_cr:
            mu_cr = (1 - c) * mu_cr + c * float(np.mean(s_cr))
        if s_f:
            arr = np.asarray(s_f, dtype=float)
            mu_f = (1 - c) * mu_f + c * float(np.sum(arr**2) / np.sum(arr))
        q = quality_row("MPDMP1", X, F, tag=f"{tag}_g{g+1}")
        q.update(
            {
                "generation": g + 1,
                "mode": tag,
                "archive_size": int(archive_x.shape[0]),
                "mu_CR": mu_cr,
                "mu_F": mu_f,
                "n_s_cr": int(len(s_cr)),
            }
        )
        rows.append(q)
        save_matrix(PYTHON_OUT / f"test_08_{tag}_X_g{g+1}.csv", X, ["x1", "x2"])
        save_matrix(PYTHON_OUT / f"test_08_{tag}_archive_X_g{g+1}.csv", archive_x if archive_x.size else np.zeros((0, 2)))
    return pd.DataFrame(rows)


def run() -> None:
    prod = _run_mode(
        "python_production",
        dict(
            matlab_pbest=False,
            matlab_parent2_retry=False,
            matlab_s_from_survivors=False,
            matlab_post_envsel_archive=False,
        ),
    )
    mat = _run_mode(
        "matlab_faithful",
        dict(
            matlab_pbest=True,
            matlab_parent2_retry=True,
            matlab_s_from_survivors=True,
            matlab_post_envsel_archive=True,
        ),
    )
    df = pd.concat([prod, mat], ignore_index=True)
    save_table(PYTHON_OUT / "test_08_short_trace.csv", df)
    # first generation where X files differ
    first = "none"
    for g in range(6):
        a = load_matrix(PYTHON_OUT / f"test_08_python_production_X_g{g}.csv")
        b = load_matrix(PYTHON_OUT / f"test_08_matlab_faithful_X_g{g}.csv")
        if a.shape != b.shape or not np.allclose(a, b, atol=1e-12):
            first = f"X_g{g}"
            break
    save_table(
        PYTHON_OUT / "test_08_first_divergence.csv",
        pd.DataFrame(
            [
                {
                    "first_divergent_component": first,
                    "prod_g5_zm26": float(prod.loc[prod.generation == 5, "zm26_meanIGD"].iloc[0]),
                    "matlab_g5_zm26": float(mat.loc[mat.generation == 5, "zm26_meanIGD"].iloc[0]),
                    "prod_g5_archive": int(prod.loc[prod.generation == 5, "archive_size"].iloc[0]),
                    "matlab_g5_archive": int(mat.loc[mat.generation == 5, "archive_size"].iloc[0]),
                }
            ]
        ),
    )
    print(f"python test_08 done first_divergent={first}")
    print(df[["mode", "generation", "zm26_meanIGD", "archive_size", "mu_F", "n"]].to_string(index=False))


if __name__ == "__main__":
    run()

"""Record Python JADE2 one-step using shared randoms. Compared later vs OptMPNDS3 MATLAB."""

from __future__ import annotations

import numpy as np
import pandas as pd
from fairmoo_benchmarks import get_problem

from .csv_io import load_matrix, save_table
from .paths import PYTHON_OUT, SHARED


def run() -> None:
    problem = get_problem("MPDMP4")
    X = load_matrix(SHARED / "jade_X.csv")
    cr = load_matrix(SHARED / "jade_cr.csv").reshape(-1)
    Fs = load_matrix(SHARED / "jade_F.csv").reshape(-1)
    pbest_idx = load_matrix(SHARED / "jade_pbest_idx.csv").astype(int).reshape(-1)
    i1 = load_matrix(SHARED / "jade_i1.csv").astype(int).reshape(-1)
    i2 = load_matrix(SHARED / "jade_i2.csv").astype(int).reshape(-1)
    jrand = load_matrix(SHARED / "jade_jrand.csv").astype(int).reshape(-1)
    mask_u = load_matrix(SHARED / "jade_mask.csv")
    xl, xu = problem.xl, problem.xu
    d = X.shape[1]
    off = []
    pre = []
    for i in range(X.shape[0]):
        pb = X[int(np.clip(pbest_idx[i], 0, len(X) - 1))]
        a = X[int(np.clip(i1[i], 0, len(X) - 1))]
        b = X[int(np.clip(i2[i], 0, len(X) - 1))]
        trial = X[i] + Fs[i] * (pb - X[i]) + Fs[i] * (b - a)
        mask = mask_u[i] < cr[i]
        mask[int(np.clip(jrand[i], 0, d - 1))] = True
        child = np.where(mask, trial, X[i])
        pre.append(child.copy())
        off.append(np.clip(child, xl, xu))
    save_table(PYTHON_OUT / "test_13_jade_offspring.csv", pd.DataFrame(np.vstack(off), columns=["x1", "x2"]))
    save_table(PYTHON_OUT / "test_13_jade_pre_repair.csv", pd.DataFrame(np.vstack(pre), columns=["x1", "x2"]))
    save_table(
        PYTHON_OUT / "test_13_jade_notes.csv",
        pd.DataFrame(
            {
                "component": [
                    "p-best",
                    "archive update",
                    "F update",
                    "CR update",
                    "mutation",
                    "crossover",
                    "bounds repair",
                ],
                "python": [
                    "lexsort(-crowd, front), k~U{1..ceil(n*p)}",
                    "replace nearest of 2N archive",
                    "mu_F <- (1-c)mu_F + c * sum(sF^2)/sum(sF)",
                    "mu_CR <- (1-c)mu_CR + c * mean(sCR)",
                    "x + F*(pbest-x) + F*(x_r2-x_r1) current-to-pbest/1",
                    "binomial, jrand forced",
                    "np.clip to [xl,xu]",
                ],
            }
        ),
    )
    print("python test_13 done (OptMPNDS3, not required for OptMPNDS)")


if __name__ == "__main__":
    run()

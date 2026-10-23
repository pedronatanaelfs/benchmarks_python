"""μF / μCR update *formula* vs MATLAB. The *set* of S_F/S_CR is a separate issue."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import load_matrix, save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT, SHARED


def mean_lehmer(f: np.ndarray) -> float:
    f = np.asarray(f, dtype=float)
    f = f[f != 0]
    if f.size == 0:
        return 0.5
    return float(np.sum(f**2) / np.sum(f))


def run() -> None:
    c = 0.05
    mu_cr, mu_f = 0.5, 0.5
    rows = []
    for g in range(5):
        cr = load_matrix(SHARED / f"g{g}_cr.csv").reshape(-1)
        Fs = load_matrix(SHARED / f"g{g}_F.csv").reshape(-1)
        # MATLAB: drop zeros
        s_cr = cr[cr != 0]
        s_f = Fs[Fs != 0]
        mu_cr_new = (1 - c) * mu_cr + c * float(np.mean(s_cr)) if s_cr.size else mu_cr
        mu_f_new = (1 - c) * mu_f + c * mean_lehmer(s_f) if s_f.size else mu_f
        rows.append(
            {
                "generation": g,
                "mu_CR_before": mu_cr,
                "mu_F_before": mu_f,
                "sampled_CR_mean": float(np.mean(cr)),
                "sampled_F_mean": float(np.mean(Fs)),
                "mu_CR_after": mu_cr_new,
                "mu_F_after": mu_f_new,
                "n_S_CR": int(s_cr.size),
                "n_S_F": int(s_f.size),
            }
        )
        mu_cr, mu_f = mu_cr_new, mu_f_new
    save_table(PYTHON_OUT / "test_05_f_cr_adaptation.csv", pd.DataFrame(rows))
    print("python test_05 done (formula only; MATLAB should match these numbers on the same S)")


if __name__ == "__main__":
    run()

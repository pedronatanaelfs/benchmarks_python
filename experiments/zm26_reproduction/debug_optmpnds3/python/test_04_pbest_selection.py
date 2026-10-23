"""Compare production lexsort p-best vs MATLAB getBestIndividual.m on shared k."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import load_matrix, save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import (
    matlab_get_best_index,
    python_pbest_index,
)
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT, SHARED


def run() -> None:
    front = load_matrix(SHARED / "pbest_front.csv").reshape(-1)
    crowd = load_matrix(SHARED / "pbest_crowd.csv").reshape(-1)
    ks = load_matrix(SHARED / "pbest_k.csv").reshape(-1).astype(int)
    rows = []
    n_diff = 0
    for i, k in enumerate(ks):
        m = matlab_get_best_index(front, crowd, int(k))
        p = python_pbest_index(front, crowd, int(k))
        n_diff += int(m != p)
        rows.append(
            {
                "point_id": i,
                "k": int(k),
                "matlab_index": m,
                "python_index": p,
                "match": m == p,
                "matlab_front": float(front[m]),
                "python_front": float(front[p]),
                "matlab_crowd": float(crowd[m]),
                "python_crowd": float(crowd[p]),
            }
        )
    df = pd.DataFrame(rows)
    save_table(PYTHON_OUT / "test_04_pbest_selection.csv", df)
    extra = []
    rng = np.random.default_rng(0)
    n_extra_diff = 0
    n_extra = 200
    for _ in range(n_extra):
        n = 20
        fr = rng.integers(1, 6, size=n).astype(float)
        cd = rng.random(n)
        cd[rng.integers(0, n, size=2)] = np.inf
        top = max(int(np.ceil(n * 0.05)), 1)
        k = int(rng.integers(1, top + 1))
        if matlab_get_best_index(fr, cd, k) != python_pbest_index(fr, cd, k):
            n_extra_diff += 1
    save_table(
        PYTHON_OUT / "test_04_pbest_summary.csv",
        pd.DataFrame(
            [
                {
                    "shared_n": len(ks),
                    "shared_mismatches": n_diff,
                    "random_trials": n_extra,
                    "random_mismatches": n_extra_diff,
                }
            ]
        ),
    )
    print(f"python test_04 done shared_mismatch={n_diff}/{len(ks)} random_mismatch={n_extra_diff}/{n_extra}")


if __name__ == "__main__":
    run()

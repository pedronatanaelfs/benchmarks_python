from __future__ import annotations

import numpy as np
import pandas as pd
from fairmoo_benchmarks import get_problem

from experiments.zm26_reproduction.algorithms.operators import random_population

from .csv_io import save_table
from .paths import PYTHON_OUT


def run() -> None:
    problem = get_problem("MPDMP4")
    rng = np.random.default_rng(1)
    X = random_population(rng, 200, problem.xl, problem.xu)
    df = pd.DataFrame(
        {
            "field": [
                "n",
                "min_x1",
                "max_x1",
                "min_x2",
                "max_x2",
                "mean_x1",
                "mean_x2",
                "n_outside_bounds",
                "n_unique_rows",
            ],
            "value": [
                X.shape[0],
                X[:, 0].min(),
                X[:, 0].max(),
                X[:, 1].min(),
                X[:, 1].max(),
                X[:, 0].mean(),
                X[:, 1].mean(),
                int(np.any((X < problem.xl) | (X > problem.xu), axis=1).sum()),
                np.unique(X, axis=0).shape[0],
            ],
        }
    )
    save_table(PYTHON_OUT / "test_05_init_stats.csv", df)
    notes = pd.DataFrame(
        {
            "note": [
                "Python initialization is rng.uniform(xl,xu). Do not compare to MATLAB rng(1).",
                "MATLAB test_05 writes Global.Initialization() stats and PF()/PS() for structure comparison.",
                "OptMPNDS does not use getPF; that is OptMPNDS3-only.",
            ]
        }
    )
    save_table(PYTHON_OUT / "test_05_notes.csv", notes)
    print("python test_05 done")


if __name__ == "__main__":
    run()

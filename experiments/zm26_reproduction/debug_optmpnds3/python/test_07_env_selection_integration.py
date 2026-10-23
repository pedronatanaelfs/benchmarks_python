"""OptMPNDS3 envsel on a shared combined set (unique + PLNDS + entropy removal)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import load_matrix, save_matrix, save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import envsel_optmpnds3
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT, SHARED
from experiments.zm26_reproduction.runners.problem_setup import load_problem


def run() -> None:
    X = load_matrix(SHARED / "envsel_X.csv")
    F = load_matrix(SHARED / "envsel_F.csv")
    _, _, slices = load_problem("MPDMP1")
    Xs, Fs, front, crowd = envsel_optmpnds3(X, F, 20, slices)
    save_matrix(PYTHON_OUT / "test_07_selected_X.csv", Xs, ["x1", "x2"])
    save_table(
        PYTHON_OUT / "test_07_env_selection.csv",
        pd.DataFrame(
            {
                "front": front,
                "entropy": crowd,
                "x1": Xs[:, 0],
                "x2": Xs[:, 1],
            }
        ),
    )
    print(f"python test_07 done selected={Xs.shape[0]} from {X.shape[0]}")


if __name__ == "__main__":
    run()

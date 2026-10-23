from __future__ import annotations

import numpy as np
import pandas as pd
from fairmoo_benchmarks import get_problem

from experiments.zm26_reproduction.algorithms.operators import (
    crowding_distance,
    environmental_selection,
    mpnds,
)

from .csv_io import load_matrix, save_table
from .paths import PYTHON_OUT, SHARED

N_SURVIVE = 100
SLICES = [slice(0, 3), slice(3, 6)]


def run() -> None:
    problem = get_problem("MPDMP4")
    X = load_matrix(SHARED / "envsel_X.csv")
    F = problem.evaluate(X)
    front, max_fno = mpnds(F, SLICES, N_SURVIVE)
    crowd = crowding_distance(F, front)
    Xs, Fs, fs, cs = environmental_selection(X, F, N_SURVIVE, mode="optmpnds", slices=SLICES)

    # Recover selected original indices by matching rows (stable first-hit).
    selected = []
    used = np.zeros(X.shape[0], dtype=bool)
    for row in Xs:
        diffs = np.linalg.norm(X - row[None, :], axis=1)
        diffs[used] = np.inf
        i = int(np.argmin(diffs))
        used[i] = True
        selected.append(i + 1)  # 1-based like MATLAB

    cand = pd.DataFrame(
        {
            "original_index": range(1, X.shape[0] + 1),
            "front": front,
            "crowding": crowd,
            "survived": used.astype(int),
        }
    )
    save_table(PYTHON_OUT / "test_04_candidates.csv", cand)
    save_table(
        PYTHON_OUT / "test_04_selected.csv",
        pd.DataFrame({"selected_original_index": selected, "front": fs, "crowding": cs}),
    )
    save_table(
        PYTHON_OUT / "test_04_meta.csv",
        pd.DataFrame(
            {
                "field": ["n_candidates", "n_survive", "max_fno", "n_selected"],
                "value": [X.shape[0], N_SURVIVE, max_fno, Xs.shape[0]],
            }
        ),
    )
    np.savetxt(PYTHON_OUT / "test_04_selected_X.csv", Xs, delimiter=",", fmt="%.16g")
    print("python test_04 done", "selected", Xs.shape[0])


if __name__ == "__main__":
    run()

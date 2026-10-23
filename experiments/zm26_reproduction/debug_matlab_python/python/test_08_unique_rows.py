from __future__ import annotations

import numpy as np
import pandas as pd
from fairmoo_benchmarks import get_problem

from .csv_io import load_matrix, save_table
from .paths import PYTHON_OUT, SHARED


def run() -> None:
    problem = get_problem("MPDMP4")
    X = load_matrix(SHARED / "unique_X.csv")
    F = problem.evaluate(X)
    # numpy unique sorts rows (like MATLAB unique(...,'rows') default)
    Fu, idx_first, inv = np.unique(F, axis=0, return_index=True, return_inverse=True)
    # MATLAB unique default: sorted unique, first occurrence among sorted order
    df = pd.DataFrame(
        {
            "input_index": range(1, X.shape[0] + 1),
            "duplicate_group": inv + 1,
            "retained_index_0based": idx_first[inv],
        }
    )
    save_table(PYTHON_OUT / "test_08_unique_map.csv", df)
    save_table(
        PYTHON_OUT / "test_08_unique_kept.csv",
        pd.DataFrame({"kept_input_index": idx_first + 1, "unique_order": np.arange(1, Fu.shape[0] + 1)}),
    )
    # OptMPNDS3 production uses return_index=True then X[loc] — first occurrence, sorted unique order
    print("python test_08 done")


if __name__ == "__main__":
    run()

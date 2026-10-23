from __future__ import annotations

import numpy as np
import pandas as pd

from .csv_io import save_table
from .ga_from_stream import sbx_pm_from_stream
from .paths import PYTHON_OUT, SHARED
from .csv_io import load_matrix


def run() -> None:
    xl = np.array([0.0, 0.0])
    xu = np.array([100.0, 100.0])
    # Force extreme crossover: identical randoms already include corner parents
    parents = load_matrix(SHARED / "variation_parents.csv")
    post, pre = sbx_pm_from_stream(
        parents,
        xl,
        xu,
        load_matrix(SHARED / "ga_mu_sbx.csv"),
        load_matrix(SHARED / "ga_sign_sbx.csv"),
        load_matrix(SHARED / "ga_beta_skip.csv"),
        load_matrix(SHARED / "ga_proc.csv"),
        load_matrix(SHARED / "ga_site.csv"),
        load_matrix(SHARED / "ga_mu_mut.csv"),
        mutation_as_expectation=True,
    )
    df = pd.DataFrame(
        {
            "off_id": range(1, post.shape[0] + 1),
            "pre_x1": pre[:, 0],
            "pre_x2": pre[:, 1],
            "post_x1": post[:, 0],
            "post_x2": post[:, 1],
            "was_outside": np.any((pre < xl) | (pre > xu), axis=1).astype(int),
        }
    )
    save_table(PYTHON_OUT / "test_10_boundary.csv", df)
    save_table(
        PYTHON_OUT / "test_10_notes.csv",
        pd.DataFrame(
            {
                "note": [
                    "Python/MATLAB GA.m clip with min(max(x,lower),upper) after SBX and after PM.",
                    "No reflect / regenerate / midpoint repair in GA.m.",
                ]
            }
        ),
    )
    print("python test_10 done")


if __name__ == "__main__":
    run()

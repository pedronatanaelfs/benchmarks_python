"""Nearest-neighbor archive replacement (updateArchive.m)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms.optmpnds3 import _update_archive
from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import load_matrix, save_matrix, save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT, SHARED


def run() -> None:
    seed_x = load_matrix(SHARED / "archive_seed_X.csv")
    seed_f = load_matrix(SHARED / "archive_seed_F.csv")
    ins_x = load_matrix(SHARED / "archive_insert_X.csv")
    ins_f = load_matrix(SHARED / "archive_insert_F.csv")
    n_max = 8
    ax, af = seed_x.copy(), seed_f.copy()
    sizes = [ax.shape[0]]
    for i in range(ins_x.shape[0]):
        ax, af = _update_archive(ax, af, ins_x[i], ins_f[i], n_max)
        sizes.append(ax.shape[0])
    save_matrix(PYTHON_OUT / "test_06_archive_final_X.csv", ax, ["x1", "x2"])
    save_table(
        PYTHON_OUT / "test_06_archive_update.csv",
        pd.DataFrame({"step": np.arange(len(sizes)), "archive_size": sizes}),
    )
    print(f"python test_06 done final_archive_n={ax.shape[0]} sizes={sizes}")


if __name__ == "__main__":
    run()

from __future__ import annotations

import pandas as pd

from experiments.zm26_reproduction.algorithms.operators import mpnds, nd_sort, plnds

from .csv_io import load_matrix, save_table
from .paths import PYTHON_OUT, SHARED

SLICES = [slice(0, 3), slice(3, 6)]


def run() -> None:
    F = load_matrix(SHARED / "mpnds_F.csv")
    n = F.shape[0]
    front_dm1, _ = nd_sort(F[:, SLICES[0]], n)
    front_dm2, _ = nd_sort(F[:, SLICES[1]], n)
    combined, max_fno = mpnds(F, SLICES, n)
    pl, _ = plnds(F, SLICES, n)
    df = pd.DataFrame(
        {
            "point_id": range(1, n + 1),
            "front_DM1": front_dm1,
            "front_DM2": front_dm2,
            "combined_front": combined,
            "plnds_front": pl,
        }
    )
    save_table(PYTHON_OUT / "test_02_mpn_sorting.csv", df)
    save_table(
        PYTHON_OUT / "test_02_meta.csv",
        pd.DataFrame({"field": ["max_fno_mpnds"], "value": [max_fno]}),
    )
    print("python test_02 done")


if __name__ == "__main__":
    run()

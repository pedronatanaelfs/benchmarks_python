from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms.operators import crowding_distance, crowding_entropy

from .csv_io import load_matrix, save_table
from .paths import PYTHON_OUT, SHARED


def run() -> None:
    F = load_matrix(SHARED / "crowding_F.csv")
    front = load_matrix(SHARED / "crowding_front.csv").reshape(-1)
    cd = crowding_distance(F, front)
    ce = crowding_entropy(F, front)
    df = pd.DataFrame(
        {
            "point_id": range(1, F.shape[0] + 1),
            "front": front,
            "crowding_value": cd,
            "entropy_value": ce,
        }
    )
    save_table(PYTHON_OUT / "test_03_crowding.csv", df)
    print("python test_03 done")


if __name__ == "__main__":
    run()

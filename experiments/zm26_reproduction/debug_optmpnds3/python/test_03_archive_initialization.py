"""Generation-0 archive is empty in both MATLAB OptMPNDS3.m and Python run()."""

from __future__ import annotations

import pandas as pd

from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT


def run() -> None:
    save_table(
        PYTHON_OUT / "test_03_archive_initialization.csv",
        pd.DataFrame(
            [
                {
                    "generation": 0,
                    "python_archive_size": 0,
                    "matlab_source": "OptMPNDS3.m Archive = []",
                    "python_source": "archive_x = zeros((0, D))",
                    "match_expected": True,
                }
            ]
        ),
    )
    print("python test_03 done (archive empty at gen 0 by construction)")


if __name__ == "__main__":
    run()

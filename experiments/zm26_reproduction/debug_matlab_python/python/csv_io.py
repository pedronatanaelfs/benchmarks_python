from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


def load_matrix(path: Path) -> np.ndarray:
    return np.loadtxt(path, delimiter=",", ndmin=2)


def save_table(path: Path, df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, na_rep="NaN")


def save_matrix(path: Path, arr: np.ndarray, header: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = np.atleast_2d(arr)
    if header is None:
        np.savetxt(path, arr, delimiter=",", fmt="%.16g")
        return
    df = pd.DataFrame(arr, columns=header)
    save_table(path, df)

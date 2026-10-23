from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


def load_matrix(path: Path) -> np.ndarray:
    try:
        return np.loadtxt(path, delimiter=",", ndmin=2)
    except ValueError:
        return np.loadtxt(path, delimiter=",", ndmin=2, skiprows=1)


def save_table(path: Path, df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, na_rep="NaN")


def save_matrix(path: Path, arr: np.ndarray, header: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = np.atleast_2d(np.asarray(arr, dtype=float))
    if header is None:
        np.savetxt(path, arr, delimiter=",", fmt="%.16g")
        return
    save_table(path, pd.DataFrame(arr, columns=header))

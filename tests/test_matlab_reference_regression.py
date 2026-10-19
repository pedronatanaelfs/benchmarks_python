"""Regression tests against licensed-MATLAB reference outputs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from fairmoo_benchmarks import get_problem, list_problems


REFERENCE_DIR = (
    Path(__file__).resolve().parents[1] / "validation" / "matlab" / "results"
)


@pytest.mark.parametrize("name", list_problems())
def test_objectives_match_matlab_reference(name: str) -> None:
    path = REFERENCE_DIR / f"{name}.csv"
    if not path.exists():
        pytest.skip(f"licensed-MATLAB reference missing: {path}")

    frame = pd.read_csv(path)
    x_columns = sorted(
        (column for column in frame if column.startswith("x")),
        key=lambda column: int(column[1:]),
    )
    f_columns = sorted(
        (column for column in frame if column.startswith("f")),
        key=lambda column: int(column[1:]),
    )
    X = frame[x_columns].to_numpy(dtype=float)
    matlab = frame[f_columns].to_numpy(dtype=float)
    python = get_problem(name).evaluate(X)

    assert python.shape == matlab.shape
    assert np.all(np.isfinite(python))
    assert np.allclose(matlab, python, rtol=1e-9, atol=1e-10)

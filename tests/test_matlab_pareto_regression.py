"""PS/PF regression tests against the licensed-MATLAB export."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from fairmoo_benchmarks import get_problem


REFERENCE_DIR = (
    Path(__file__).resolve().parents[1]
    / "validation"
    / "matlab"
    / "pareto_results"
)
PROBLEMS = [
    *(f"MPMOP{i}" for i in [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17]),
    *(f"MPDMP{i}" for i in range(1, 19)),
]


def read_matrix(path: Path, columns: int) -> np.ndarray:
    if not path.exists() or path.stat().st_size == 0:
        return np.zeros((0, columns))
    return np.loadtxt(path, delimiter=",", ndmin=2).reshape(-1, columns)


@pytest.mark.parametrize("name", PROBLEMS)
def test_ps_pf_match_matlab_reference(name: str) -> None:
    problem = get_problem(name)
    matlab_ps = read_matrix(REFERENCE_DIR / f"{name}_PS.csv", problem.n_var)
    matlab_pf = read_matrix(REFERENCE_DIR / f"{name}_PF.csv", problem.n_obj)
    python_ps = problem.get_common_pareto_set()
    python_pf = problem.get_pareto_front()

    assert python_ps is not None
    assert python_pf is not None
    assert python_ps.shape == matlab_ps.shape
    assert python_pf.shape == matlab_pf.shape
    assert np.allclose(python_ps, matlab_ps, rtol=1e-9, atol=1e-10)
    assert np.allclose(python_pf, matlab_pf, rtol=1e-9, atol=1e-10)

"""Compare MATLAB PS/PF exports with Python benchmark helpers."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np


VALIDATION_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = VALIDATION_DIR.parent
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from fairmoo_benchmarks import get_problem  # noqa: E402


NAMES = [
    *(f"MPMOP{i}" for i in [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17]),
    *(f"MPDMP{i}" for i in range(1, 19)),
]


def read_matrix(path: Path, columns: int) -> np.ndarray:
    if not path.exists() or path.stat().st_size == 0:
        return np.zeros((0, columns))
    matrix = np.loadtxt(path, delimiter=",", ndmin=2)
    return np.asarray(matrix, dtype=float).reshape(-1, columns)


def main() -> None:
    matlab_dir = VALIDATION_DIR / "matlab" / "pareto_results"
    report_path = VALIDATION_DIR / "reports" / "pareto_comparison.csv"
    rows = []
    for name in NAMES:
        problem = get_problem(name)
        matlab_ps = read_matrix(matlab_dir / f"{name}_PS.csv", problem.n_var)
        matlab_pf = read_matrix(matlab_dir / f"{name}_PF.csv", problem.n_obj)
        python_ps = problem.get_common_pareto_set()
        python_pf = problem.get_pareto_front()
        python_ps = None if python_ps is None else np.asarray(python_ps, dtype=float)
        python_pf = None if python_pf is None else np.asarray(python_pf, dtype=float)

        ps_pass = python_ps is not None and python_ps.shape == matlab_ps.shape and np.allclose(
            python_ps, matlab_ps, rtol=1e-9, atol=1e-10
        )
        pf_pass = python_pf is not None and python_pf.shape == matlab_pf.shape and np.allclose(
            python_pf, matlab_pf, rtol=1e-9, atol=1e-10
        )
        rows.append(
            {
                "problem": name,
                "ps_status": "PASS" if ps_pass else "FAIL",
                "matlab_ps_shape": str(matlab_ps.shape),
                "python_ps_shape": "None" if python_ps is None else str(python_ps.shape),
                "pf_status": "PASS" if pf_pass else "FAIL",
                "matlab_pf_shape": str(matlab_pf.shape),
                "python_pf_shape": "None" if python_pf is None else str(python_pf.shape),
            }
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()

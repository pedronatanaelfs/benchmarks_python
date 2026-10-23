from __future__ import annotations

import pandas as pd
from fairmoo_benchmarks import get_problem

from .csv_io import load_matrix, save_table
from .paths import PYTHON_OUT, SHARED


def run() -> None:
    problem = get_problem("MPDMP4")
    X = load_matrix(SHARED / "mpdmp4_X.csv")
    F = problem.evaluate(X)
    cols = ["x1", "x2"] + [f"F{i+1}" for i in range(F.shape[1])]
    df = pd.DataFrame(np_c(X, F), columns=cols)
    save_table(PYTHON_OUT / "test_01_problem.csv", df)
    meta = pd.DataFrame(
        {
            "field": [
                "n_var",
                "n_obj",
                "n_dm",
                "xl0",
                "xl1",
                "xu0",
                "xu1",
                "n_obj_dm1",
                "n_obj_dm2",
                "slice_dm1_start",
                "slice_dm1_stop",
                "slice_dm2_start",
                "slice_dm2_stop",
            ],
            "value": [
                problem.n_var,
                problem.n_obj,
                problem.n_dm,
                problem.xl[0],
                problem.xl[1],
                problem.xu[0],
                problem.xu[1],
                problem.n_obj_per_dm[0],
                problem.n_obj_per_dm[1],
                problem.dm_objective_slices[0].start,
                problem.dm_objective_slices[0].stop,
                problem.dm_objective_slices[1].start,
                problem.dm_objective_slices[1].stop,
            ],
        }
    )
    save_table(PYTHON_OUT / "test_01_meta.csv", meta)
    # Party PF samples (what the reproduction uses for IGD)
    for dm in range(problem.n_dm):
        pf = problem.get_pareto_front(dm=dm, n_points=50)
        save_table(
            PYTHON_OUT / f"test_01_python_party_pf_dm{dm+1}.csv",
            pd.DataFrame(pf, columns=[f"f{j+1}" for j in range(pf.shape[1])]),
        )
    ps = problem.get_pareto_set(dm=None)
    if ps is not None:
        save_table(PYTHON_OUT / "test_01_python_common_ps.csv", pd.DataFrame(ps, columns=["x1", "x2"]))
    print("python test_01 done", F.shape)


def np_c(a, b):
    import numpy as np

    return np.hstack([a, b])


if __name__ == "__main__":
    run()

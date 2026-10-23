from __future__ import annotations

import pandas as pd
from fairmoo_benchmarks import get_problem

from .csv_io import save_table
from .paths import PYTHON_OUT


def run() -> None:
    problem = get_problem("MPDMP4")
    rows = []
    for dm in range(problem.n_dm):
        sl = problem.dm_objective_slices[dm]
        rows.append(
            {
                "dm": dm + 1,
                "matlab_columns_1based": f"{sl.start+1}:{sl.stop}",
                "n_obj": sl.stop - sl.start,
                "used_by_mpnds": "F[:, slice]",
                "used_by_plnds": "F[:, slice]",
                "used_by_envsel": "mpnds then crowding on FULL concatenated F",
            }
        )
    save_table(PYTHON_OUT / "test_11_grouping.csv", pd.DataFrame(rows))
    refs = []
    for dm, pts in problem.reference_points.items():
        for i, p in enumerate(pts):
            refs.append({"dm": dm + 1, "vertex": i + 1, "x": p[0], "y": p[1]})
    save_table(PYTHON_OUT / "test_11_reference_vertices.csv", pd.DataFrame(refs))
    print("python test_11 done")


if __name__ == "__main__":
    run()

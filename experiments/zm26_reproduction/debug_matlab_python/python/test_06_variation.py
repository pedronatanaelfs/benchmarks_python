from __future__ import annotations

import numpy as np
import pandas as pd
from fairmoo_benchmarks import get_problem

from .csv_io import load_matrix, save_table
from .ga_from_stream import sbx_pm_from_stream
from .paths import PYTHON_OUT, SHARED


def run() -> None:
    problem = get_problem("MPDMP4")
    parents = load_matrix(SHARED / "variation_parents.csv")
    args = dict(
        parents=parents,
        xl=problem.xl,
        xu=problem.xu,
        mu_sbx=load_matrix(SHARED / "ga_mu_sbx.csv"),
        sign01=load_matrix(SHARED / "ga_sign_sbx.csv"),
        beta_skip=load_matrix(SHARED / "ga_beta_skip.csv"),
        proc=load_matrix(SHARED / "ga_proc.csv"),
        site_u=load_matrix(SHARED / "ga_site.csv"),
        mu_mut=load_matrix(SHARED / "ga_mu_mut.csv"),
        pro_c=1.0,
        dis_c=15.0,
        pro_m=0.5,
        dis_m=20.0,
    )
    off_matlab_rate, pre_m = sbx_pm_from_stream(**args, mutation_as_expectation=True)
    off_python_rate, pre_p = sbx_pm_from_stream(**args, mutation_as_expectation=False)
    save_table(
        PYTHON_OUT / "test_06_offspring_matlab_rate.csv",
        pd.DataFrame(off_matlab_rate, columns=["x1", "x2"]),
    )
    save_table(
        PYTHON_OUT / "test_06_offspring_python_production_rate.csv",
        pd.DataFrame(off_python_rate, columns=["x1", "x2"]),
    )
    save_table(
        PYTHON_OUT / "test_06_pre_repair_matlab_rate.csv",
        pd.DataFrame(pre_m, columns=["x1", "x2"]),
    )
    save_table(
        PYTHON_OUT / "test_06_meta.csv",
        pd.DataFrame(
            {
                "field": [
                    "pro_c",
                    "dis_c",
                    "pro_m",
                    "dis_m",
                    "matlab_site_formula",
                    "python_production_site_formula",
                    "n_parents",
                    "n_offspring",
                    "n_pre_repair_outside_matlab_rate",
                ],
                "value": [
                    1.0,
                    15.0,
                    0.5,
                    20.0,
                    "rand < pro_m/D",
                    "rand < pro_m  (mutation_as_expectation=False)",
                    parents.shape[0],
                    off_matlab_rate.shape[0],
                    int(np.any((pre_m < 0) | (pre_m > 100), axis=1).sum()),
                ],
            }
        ),
    )
    print("python test_06 done")


if __name__ == "__main__":
    run()

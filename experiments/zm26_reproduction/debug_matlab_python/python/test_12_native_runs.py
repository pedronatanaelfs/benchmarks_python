"""5 native stochastic OptMPNDS runs on MPDMP4 (ZM26 N/FE). Not compared exactly to MATLAB."""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from scipy.spatial.distance import cdist

from experiments.zm26_reproduction.algorithms.optmpnds import OptMPNDS
from experiments.zm26_reproduction.metrics.igd import party_igd
from experiments.zm26_reproduction.metrics.mean_igd import mean_igd
from experiments.zm26_reproduction.runners.problem_setup import load_problem, reference_fronts

from .csv_io import save_table
from .paths import PYTHON_OUT


def she_igd_single_pf(F, pf_row, slices) -> float:
    """MATLAB Metrics/IGD.m: sum party pdist2(PF, obj) then min over approx, then mean.

    MPDMP4.PF() is CalObj([50,40]) — a single reference point, not the triangle PF.
    """
    dis = None
    for sl in slices:
        block = cdist(np.atleast_2d(pf_row[:, sl]), np.atleast_2d(F[:, sl]))
        dis = block if dis is None else dis + block
    return float(np.min(dis, axis=1).mean())


def run(n_runs: int = 5) -> None:
    problem, _, slices = load_problem("MPDMP4")
    pf = reference_fronts(problem, n_points=2000)
    pf_common = problem.evaluate(np.array([[50.0, 40.0]]))
    alg = OptMPNDS(
        population_size=200,
        evaluation_budget=80000,
        pro_c=1.0,
        dis_c=15.0,
        pro_m=0.5,
        dis_m=20.0,
        mutation_as_expectation=False,
    )
    rows = []
    for run_id in range(1, n_runs + 1):
        t0 = time.time()
        rng = np.random.default_rng(run_id)
        X, F = alg.run(problem, rng, slices)
        igds = party_igd(F, pf, slices)
        migd = mean_igd(F, pf, slices)
        she = she_igd_single_pf(F, pf_common, slices)
        dist_ps = float(np.linalg.norm(X - np.array([50.0, 40.0]), axis=1).mean())
        rows.append(
            {
                "run": run_id,
                "seed": run_id,
                "meanIGD": migd,
                "IGD_DM1": igds[0],
                "IGD_DM2": igds[1],
                "she_IGD_single_PF": she,
                "mean_dist_to_common_ps": dist_ps,
                "pop_mean_x1": float(X[:, 0].mean()),
                "pop_mean_x2": float(X[:, 1].mean()),
                "pop_std_x1": float(X[:, 0].std()),
                "pop_std_x2": float(X[:, 1].std()),
                "runtime_sec": time.time() - t0,
                "mutation_as_expectation": False,
                "pro_m": 0.5,
            }
        )
        print(
            f"  native run {run_id} meanIGD={migd:.4g} sheIGD={she:.4g} "
            f"distPS={dist_ps:.4g} t={rows[-1]['runtime_sec']:.1f}s"
        )
    save_table(PYTHON_OUT / "test_12_native_runs.csv", pd.DataFrame(rows))
    print("python test_12 done")


if __name__ == "__main__":
    run()

from __future__ import annotations

import numpy as np
import pandas as pd
from fairmoo_benchmarks import get_problem

from experiments.zm26_reproduction.algorithms.operators import environmental_selection
from experiments.zm26_reproduction.metrics.igd import party_igd
from experiments.zm26_reproduction.metrics.mean_igd import mean_igd
from experiments.zm26_reproduction.runners.problem_setup import reference_fronts

from .csv_io import load_matrix, save_table
from .ga_from_stream import sbx_pm_from_stream
from .paths import PYTHON_OUT, SHARED

N = 20
N_GEN = 5
SLICES = [slice(0, 3), slice(3, 6)]


def _mating_from_tour(tour: np.ndarray) -> np.ndarray:
    """tour is 2 x N of 0-based indices; pick first row then second as GA parent split."""
    # MATLAB TournamentSelection returns N indices. We stored the KxN candidate matrix.
    # For a fully shared comparison, MATLAB will also consume this matrix the same way:
    # index = tour[best, :] with best=0 (first row) would ignore fitness.
    # Instead we save the *already chosen* mating pool as row 0 concatenated with row 1
    # after a dummy min: we use row0 as the selected parents (N indices).
    return tour[0].astype(int)


def run() -> None:
    problem = get_problem("MPDMP4")
    pf = reference_fronts(problem, n_points=200)
    X = load_matrix(SHARED / "short_X0.csv")
    F = problem.evaluate(X)
    X, F, front, crowd = environmental_selection(X, F, N, mode="optmpnds", slices=SLICES)
    rows = []
    for g in range(N_GEN + 1):
        igds = party_igd(F, pf, SLICES)
        rows.append(
            {
                "generation": g,
                "n": X.shape[0],
                "meanIGD": mean_igd(F, pf, SLICES),
                "IGD_DM1": igds[0],
                "IGD_DM2": igds[1],
                "n_front1": int(np.sum(front == 1)),
                "mean_x1": float(X[:, 0].mean()),
                "mean_x2": float(X[:, 1].mean()),
                "dist_to_common_ps": float(np.linalg.norm(X - np.array([50.0, 40.0]), axis=1).mean()),
            }
        )
        np.savetxt(PYTHON_OUT / f"test_07_X_g{g}.csv", X, delimiter=",", fmt="%.16g")
        np.savetxt(PYTHON_OUT / f"test_07_F_g{g}.csv", F, delimiter=",", fmt="%.16g")
        np.savetxt(PYTHON_OUT / f"test_07_front_g{g}.csv", np.atleast_2d(front), delimiter=",", fmt="%.16g")
        np.savetxt(PYTHON_OUT / f"test_07_crowd_g{g}.csv", np.atleast_2d(crowd), delimiter=",", fmt="%.16g")
        if g == N_GEN:
            break
        tour = load_matrix(SHARED / f"short_tour_g{g}.csv").astype(int)
        mating = np.clip(tour[0], 0, X.shape[0] - 1)
        parent_idx = mating[: X.shape[0]]
        parents = X[parent_idx]
        off, _ = sbx_pm_from_stream(
            parents,
            problem.xl,
            problem.xu,
            load_matrix(SHARED / f"short_ga_mu_sbx_g{g}.csv"),
            load_matrix(SHARED / f"short_ga_sign_g{g}.csv"),
            load_matrix(SHARED / f"short_ga_beta_skip_g{g}.csv"),
            load_matrix(SHARED / f"short_ga_proc_g{g}.csv"),
            load_matrix(SHARED / f"short_ga_site_g{g}.csv"),
            load_matrix(SHARED / f"short_ga_mu_mut_g{g}.csv"),
            pro_c=1.0,
            dis_c=15.0,
            pro_m=0.5,
            dis_m=20.0,
            mutation_as_expectation=True,
        )
        off_f = problem.evaluate(off)
        cand_x = np.vstack([X, off])
        cand_f = np.vstack([F, off_f])
        Xs, Fs, front, crowd = environmental_selection(
            cand_x, cand_f, N, mode="optmpnds", slices=SLICES
        )
        used = np.zeros(cand_x.shape[0], dtype=bool)
        survived = []
        for row in Xs:
            diffs = np.linalg.norm(cand_x - row[None, :], axis=1)
            diffs[used] = np.inf
            i = int(np.argmin(diffs))
            used[i] = True
            survived.append(i + 1)
        save_table(
            PYTHON_OUT / f"test_07_mating_g{g}.csv",
            pd.DataFrame({"parent_index_1based": parent_idx + 1}),
        )
        save_table(
            PYTHON_OUT / f"test_07_survived_g{g}.csv",
            pd.DataFrame({"selected_original_index": survived}),
        )
        X, F = Xs, Fs
    save_table(PYTHON_OUT / "test_07_trace.csv", pd.DataFrame(rows))
    print("python test_07 done")


if __name__ == "__main__":
    run()

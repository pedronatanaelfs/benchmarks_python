"""5-seed MPDMP1/MPDMP4 runs under corrected production settings.

Saves F so zm26_meanIGD can be computed. Not a 30-seed table replacement.
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from experiments.zm26_reproduction import ROOT
from experiments.zm26_reproduction.algorithms import ALGORITHMS
from experiments.zm26_reproduction.config.settings import algorithm_kwargs
from experiments.zm26_reproduction.metrics.matlab_mpdmp_pf import matlab_problem_pf
from experiments.zm26_reproduction.metrics.mean_igd import mean_igd
from experiments.zm26_reproduction.metrics.she_igd import zm26_meanIGD
from experiments.zm26_reproduction.runners.problem_setup import load_problem, reference_fronts

OUT_DIR = ROOT / "results" / "validation"
POP_DIR = OUT_DIR / "populations"
CSV = OUT_DIR / "mpdmp_5seed.csv"

PROBLEMS = ["MPDMP4", "MPDMP1"]
ALGS = ["OptAll", "OptMPNDS", "OptMPNDS2", "OptMPNDS3"]
SEEDS = [1, 2, 3, 4, 5]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    POP_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in PROBLEMS:
        problem, family, slices = load_problem(name)
        party_pf = reference_fronts(problem, n_points=2000)
        matlab_pf = matlab_problem_pf(problem)
        kw_base = algorithm_kwargs(family, "OptMPNDS")
        for alg_name in ALGS:
            kw = algorithm_kwargs(family, alg_name)
            for run_id, seed in enumerate(SEEDS, start=1):
                t0 = time.time()
                rng = np.random.default_rng(seed)
                alg = ALGORITHMS[alg_name](**kw)
                X, F = alg.run(problem, rng, slices)
                rec = {
                    "benchmark": name,
                    "algorithm": alg_name,
                    "run": run_id,
                    "seed": seed,
                    "party_pf_meanIGD": mean_igd(F, party_pf, slices),
                    "zm26_meanIGD": zm26_meanIGD(F, matlab_pf, slices),
                    "meanIGD": mean_igd(F, party_pf, slices),
                    "pop_mean_x1": float(X[:, 0].mean()),
                    "pop_mean_x2": float(X[:, 1].mean()),
                    "runtime_sec": time.time() - t0,
                    "mutation_as_expectation": kw.get("mutation_as_expectation", True),
                    "pro_m": kw.get("pro_m", np.nan),
                    "population_size": kw_base["population_size"],
                    "evaluation_budget": kw["evaluation_budget"],
                }
                path = POP_DIR / f"{name}_{alg_name}_run{run_id}_seed{seed}.npz"
                np.savez_compressed(path, X=X, F=F, seed=seed, problem=name, algorithm=alg_name)
                rows.append(rec)
                print(
                    f"{name} {alg_name} seed={seed} "
                    f"party={rec['party_pf_meanIGD']:.4g} zm26={rec['zm26_meanIGD']:.4g} "
                    f"t={rec['runtime_sec']:.1f}s"
                )
    pd.DataFrame(rows).to_csv(CSV, index=False)
    print(f"wrote {CSV}")


if __name__ == "__main__":
    main()

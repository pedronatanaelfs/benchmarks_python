"""5-seed OptMPNDS3 on MPDMP6/8 after the last-generation fix."""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms import ALGORITHMS
from experiments.zm26_reproduction.config.settings import MPDMP
from experiments.zm26_reproduction.metrics.matlab_mpdmp_pf import matlab_problem_pf
from experiments.zm26_reproduction.metrics.she_igd import zm26_meanIGD
from experiments.zm26_reproduction.runners.problem_setup import load_problem

OUT = Path(__file__).resolve().parents[1] / "results" / "validation" / "optmpnds3_5seed_mpdmp68.csv"
PAPER = {"MPDMP6": 0.0838, "MPDMP8": 2.25}


def main() -> None:
    rows = []
    for name in ("MPDMP6", "MPDMP8"):
        problem, _, slices = load_problem(name)
        pf = matlab_problem_pf(problem)
        for seed in range(1, 6):
            rng = np.random.default_rng(seed)
            t0 = time.time()
            X, F = ALGORITHMS["OptMPNDS3"](
                population_size=MPDMP["population_size"],
                evaluation_budget=MPDMP["evaluation_budget"],
            ).run(problem, rng, slices)
            zm26 = float(zm26_meanIGD(F, pf, slices))
            rec = {
                "benchmark": name,
                "algorithm": "OptMPNDS3",
                "seed": seed,
                "n_final": int(X.shape[0]),
                "zm26_meanIGD": zm26,
                "paper_zm26": PAPER[name],
                "pop_mean_x1": float(X[:, 0].mean()),
                "pop_mean_x2": float(X[:, 1].mean()),
                "runtime_sec": time.time() - t0,
            }
            rows.append(rec)
            print(
                f"{name} seed={seed} n={X.shape[0]} zm26={zm26:.4g} paper={PAPER[name]} "
                f"t={rec['runtime_sec']:.1f}s",
                flush=True,
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

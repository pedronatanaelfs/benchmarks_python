"""Optional native OptMPNDS3 5-run (independent RNG). Slow."""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms.optmpnds3 import OptMPNDS3
from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import quality_row
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT
from experiments.zm26_reproduction.runners.problem_setup import load_problem

PAPER = {"MPDMP1": 0.0447, "MPDMP4": 0.0133}


def run(problems=("MPDMP1",), n_runs: int = 5) -> None:
    rows = []
    for name in problems:
        problem, _, slices = load_problem(name)
        for seed in range(1, n_runs + 1):
            rng = np.random.default_rng(seed)
            t0 = time.time()
            X, F = OptMPNDS3().run(problem, rng, slices)
            q = quality_row(name, X, F, tag=f"native_seed{seed}")
            q.update(
                {
                    "seed": seed,
                    "runtime_sec": time.time() - t0,
                    "paper_zm26": PAPER[name],
                }
            )
            rows.append(q)
            print(
                f"python native {name} seed={seed} zm26={q['zm26_meanIGD']:.4g} "
                f"dist={q['mean_dist_to_common_ps']:.3g} t={q['runtime_sec']:.1f}s"
            )
    save_table(PYTHON_OUT / "test_09_native_5run.csv", pd.DataFrame(rows))
    print("python test_09 done")


if __name__ == "__main__":
    run()

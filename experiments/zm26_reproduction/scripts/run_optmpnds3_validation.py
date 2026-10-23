"""5-seed OptMPNDS3 only on MPDMP1/4 after the last-generation fix."""

from __future__ import annotations

import time

import pandas as pd

from experiments.zm26_reproduction.algorithms import ALGORITHMS
from experiments.zm26_reproduction.config.settings import MPDMP
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import quality_row
from experiments.zm26_reproduction.runners.problem_setup import load_problem

OUT = (
    __import__("pathlib").Path(__file__).resolve().parents[1]
    / "results"
    / "validation"
    / "optmpnds3_5seed_after_lastgen_fix.csv"
)
PAPER = {"MPDMP1": 0.0447, "MPDMP4": 0.0133}


def main() -> None:
    rows = []
    for name in ("MPDMP1", "MPDMP4"):
        problem, _, slices = load_problem(name)
        for seed in range(1, 6):
            rng = __import__("numpy").random.default_rng(seed)
            t0 = time.time()
            X, F = ALGORITHMS["OptMPNDS3"](
                population_size=MPDMP["population_size"],
                evaluation_budget=MPDMP["evaluation_budget"],
            ).run(problem, rng, slices)
            q = quality_row(name, X, F, tag=f"seed{seed}")
            q.update(
                {
                    "algorithm": "OptMPNDS3",
                    "seed": seed,
                    "runtime_sec": time.time() - t0,
                    "paper_zm26": PAPER[name],
                    "n_final": int(X.shape[0]),
                }
            )
            rows.append(q)
            print(
                f"{name} seed={seed} n={X.shape[0]} zm26={q['zm26_meanIGD']:.4g} "
                f"paper={PAPER[name]} dist={q['mean_dist_to_common_ps']:.3g} "
                f"t={q['runtime_sec']:.1f}s",
                flush=True,
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

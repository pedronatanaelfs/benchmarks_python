"""Evaluate a population and report per-DM objective blocks."""

from __future__ import annotations

import numpy as np

from fairmoo_benchmarks import get_problem


def main() -> None:
    problem = get_problem("MPMOP17")
    rng = np.random.default_rng(42)
    X = rng.uniform(problem.xl, problem.xu, size=(20, problem.n_var))
    F = problem.evaluate(X)
    print(problem.describe())
    print("F shape:", F.shape)
    for dm in range(problem.n_dm):
        Fd = problem.evaluate_dm(X, dm)
        print(f"DM{dm+1} ({problem.dm_names[dm]}): shape={Fd.shape}, mean={Fd.mean(axis=0)}")


if __name__ == "__main__":
    main()

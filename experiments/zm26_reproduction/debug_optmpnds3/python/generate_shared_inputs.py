"""Shared deterministic arrays for MATLAB wrappers. Not language RNG seeds."""

from __future__ import annotations

import numpy as np

from experiments.zm26_reproduction.algorithms.operators import (
    crowding_entropy,
    plnds,
    random_population,
)
from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import save_matrix
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import SHARED, ensure_dirs
from experiments.zm26_reproduction.runners.problem_setup import load_problem


def main() -> None:
    ensure_dirs()
    rng = np.random.default_rng(20261022)
    problem, _, slices = load_problem("MPDMP1")
    n, gens, d = 20, 5, 2
    X = random_population(rng, n, problem.xl, problem.xu)
    F = problem.evaluate(X)
    front, _ = plnds(F, slices, n)
    crowd = crowding_entropy(F, front)
    save_matrix(SHARED / "short_X0.csv", X)
    save_matrix(SHARED / "short_F0.csv", F)
    save_matrix(SHARED / "short_front0.csv", front.reshape(-1, 1))
    save_matrix(SHARED / "short_crowd0.csv", crowd.reshape(-1, 1))
    save_matrix(SHARED / "pbest_X.csv", X)
    save_matrix(SHARED / "pbest_front.csv", front.reshape(-1, 1))
    save_matrix(SHARED / "pbest_crowd.csv", crowd.reshape(-1, 1))
    top = max(int(np.ceil(n * 0.05)), 1)
    k = rng.integers(1, top + 1, size=n)
    save_matrix(SHARED / "pbest_k.csv", k.reshape(-1, 1))
    # archive update: 8 extra points to insert into a 4-slot archive (cap 8 = 2N with N=4)
    arch_x = X[:4]
    extra_x = random_population(rng, 8, problem.xl, problem.xu)
    save_matrix(SHARED / "archive_seed_X.csv", arch_x)
    save_matrix(SHARED / "archive_insert_X.csv", extra_x)
    save_matrix(SHARED / "archive_seed_F.csv", problem.evaluate(arch_x))
    save_matrix(SHARED / "archive_insert_F.csv", problem.evaluate(extra_x))
    env_x = np.vstack([X, random_population(rng, n, problem.xl, problem.xu)])
    env_f = problem.evaluate(env_x)
    save_matrix(SHARED / "envsel_X.csv", env_x)
    save_matrix(SHARED / "envsel_F.csv", env_f)
    for g in range(gens):
        save_matrix(SHARED / f"g{g}_cr.csv", rng.uniform(0, 1, size=(n, 1)))
        Fs = rng.standard_cauchy(size=(n, 1)) * 0.1 + 0.5
        Fs = np.clip(np.where(Fs <= 0, 0.05, Fs), 0.0, 1.0)
        save_matrix(SHARED / f"g{g}_F.csv", Fs)
        save_matrix(SHARED / f"g{g}_pbest_k.csv", rng.integers(1, top + 1, size=(n, 1)).astype(float))
        save_matrix(SHARED / f"g{g}_i1.csv", rng.integers(0, n, size=(n, 1)).astype(float))
        save_matrix(SHARED / f"g{g}_i2.csv", rng.integers(0, 2 * n, size=(n, 1)).astype(float))
        save_matrix(SHARED / f"g{g}_jrand.csv", rng.integers(0, d, size=(n, 1)).astype(float))
        save_matrix(SHARED / f"g{g}_mask.csv", rng.random((n, d)))
    save_matrix(SHARED / "init_uniform_party.csv", rng.random((100, 2)))
    print(f"shared_inputs written under {SHARED}")


if __name__ == "__main__":
    main()

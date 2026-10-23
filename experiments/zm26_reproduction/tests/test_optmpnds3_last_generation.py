"""OptMPNDS3 must not replace the population with a truncated last generation."""

import numpy as np

from experiments.zm26_reproduction.algorithms.optmpnds3 import OptMPNDS3
from experiments.zm26_reproduction.runners.problem_setup import load_problem


def test_last_generation_keeps_population_size():
    problem, _, slices = load_problem("MPDMP1")
    algo = OptMPNDS3(population_size=40, evaluation_budget=250, fei=100)
    X, F = algo.run(problem, np.random.default_rng(1), slices)
    assert X.shape[0] >= 20, (
        f"population collapsed to {X.shape[0]} rows; last-generation "
        "offspring truncation likely replaced the JADE pool"
    )
    assert F.shape[0] == X.shape[0]

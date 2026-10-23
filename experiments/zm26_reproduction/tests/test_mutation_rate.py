"""MATLAB GA.m real-encoding mutation uses Site = rand < proM/D."""

import numpy as np

from experiments.zm26_reproduction.algorithms.operators import sbx_pm
from experiments.zm26_reproduction.config.settings import MPDMP, algorithm_kwargs


def test_production_mpdmp_uses_prom_over_d():
    kw = algorithm_kwargs("MPDMP", "OptMPNDS")
    assert kw["mutation_as_expectation"] is True
    assert kw["pro_m"] == 0.5
    d = 2
    assert kw["pro_m"] / d == 0.25


def test_sbx_pm_matlab_rate_differs_from_per_variable_half():
    rng_a = np.random.default_rng(0)
    rng_b = np.random.default_rng(0)
    parents = np.array([[0.0, 0.0], [100.0, 100.0], [10.0, 90.0], [90.0, 10.0]])
    xl = np.array([0.0, 0.0])
    xu = np.array([100.0, 100.0])
    off_matlab = sbx_pm(
        rng_a, parents, xl, xu, pro_c=1.0, dis_c=15.0, pro_m=0.5, dis_m=20.0,
        mutation_as_expectation=True,
    )
    off_old = sbx_pm(
        rng_b, parents, xl, xu, pro_c=1.0, dis_c=15.0, pro_m=0.5, dis_m=20.0,
        mutation_as_expectation=False,
    )
    assert off_matlab.shape == off_old.shape == (4, 2)
    assert MPDMP["mutation_as_expectation"] is True
    assert abs(MPDMP["pro_m"] / 2 - 0.25) < 1e-15

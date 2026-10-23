"""MPDMP4: zm26_meanIGD is small near (50,40); party_pf_meanIGD is not."""

import numpy as np
from fairmoo_benchmarks import get_problem

from experiments.zm26_reproduction.metrics.matlab_mpdmp_pf import matlab_problem_pf
from experiments.zm26_reproduction.metrics.mean_igd import mean_igd
from experiments.zm26_reproduction.metrics.she_igd import zm26_meanIGD
from experiments.zm26_reproduction.runners.problem_setup import load_problem, reference_fronts


def test_mpdmp1_analytical_pf():
    problem = get_problem("MPDMP1")
    pf = matlab_problem_pf(problem)
    v = 20.0 * np.sqrt(2.0)
    np.testing.assert_allclose(pf, [[v, v, v, v]], atol=1e-12)


def test_mpdmp4_common_ps_metrics_diverge():
    problem, _, slices = load_problem("MPDMP4")
    rng = np.random.default_rng(0)
    X = np.array([[50.0, 40.0]]) + rng.normal(0.0, 0.05, size=(40, 2))
    X = np.clip(X, 0.0, 100.0)
    F = problem.evaluate(X)
    matlab_pf = matlab_problem_pf(problem)
    zm26 = zm26_meanIGD(F, matlab_pf, slices)
    party_pf = reference_fronts(problem, n_points=2000)
    party = mean_igd(F, party_pf, slices)
    assert zm26 < 0.05, zm26
    assert party > 1.0, party
    assert party / max(zm26, 1e-16) > 50

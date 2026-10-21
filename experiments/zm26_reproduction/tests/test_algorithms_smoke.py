import numpy as np
import pytest

from experiments.zm26_reproduction.algorithms import ALGORITHMS
from experiments.zm26_reproduction.runners.problem_setup import load_problem, reference_fronts


@pytest.mark.parametrize("name", ["OptAll", "OptMPNDS"])
def test_mpmop1_smoke(name):
    problem, family, slices = load_problem("MPMOP1")
    rng = np.random.default_rng(1)
    alg = ALGORITHMS[name](population_size=12, evaluation_budget=36)
    X, F = alg.run(problem, rng, slices)
    assert X.shape[1] == problem.n_var
    assert F.shape[1] == problem.n_obj
    assert X.shape[0] <= 12
    assert np.all(np.isfinite(F))


@pytest.mark.parametrize("name", ["OptAll", "OptMPNDS", "OptMPNDS2"])
def test_mpdmp1_smoke(name):
    problem, family, slices = load_problem("MPDMP1")
    rng = np.random.default_rng(1)
    alg = ALGORITHMS[name](population_size=16, evaluation_budget=48)
    X, F = alg.run(problem, rng, slices)
    assert F.shape[1] == problem.n_obj
    assert np.all(np.isfinite(F))


def test_reference_fronts_exist():
    problem, _, _ = load_problem("MPDMP1")
    pfs = reference_fronts(problem, n_points=50)
    assert len(pfs) == 2
    assert pfs[0].shape[1] == 2


@pytest.mark.parametrize("name", ["MPMOP3", "MPMOP4", "MPMOP6", "MPMOP9", "MPMOP11"])
def test_mpmop_pf_fallback(name):
    problem, _, slices = load_problem(name)
    pfs = reference_fronts(problem, n_points=200)
    assert len(pfs) == problem.n_dm
    for pf, sl in zip(pfs, slices):
        assert pf.size > 0
        assert pf.shape[1] == sl.stop - sl.start
        assert np.all(np.isfinite(pf))

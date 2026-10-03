"""Shape tests for multi-party benchmarks."""

from __future__ import annotations

import numpy as np
import pytest

from fairmoo_benchmarks import get_problem, list_problems


@pytest.mark.parametrize("name", list_problems())
def test_evaluate_shapes(name: str) -> None:
    problem = get_problem(name)
    rng = np.random.default_rng(42)
    x = 0.5 * (problem.xl + problem.xu)
    f = problem.evaluate(x)
    assert f.shape == (problem.n_obj,)

    X = rng.uniform(problem.xl, problem.xu, size=(100, problem.n_var))
    F = problem.evaluate(X)
    assert F.shape == (100, problem.n_obj)

    for dm in range(problem.n_dm):
        Fd = problem.evaluate_dm(X, dm)
        assert Fd.shape == (100, problem.n_obj_per_dm[dm])
        sl = problem.dm_objective_slices[dm]
        np.testing.assert_allclose(Fd, F[:, sl])


@pytest.mark.parametrize("name", list_problems())
def test_bounds(name: str) -> None:
    problem = get_problem(name)
    assert problem.xl.shape == (problem.n_var,)
    assert problem.xu.shape == (problem.n_var,)
    assert np.all(problem.xl <= problem.xu)


def test_registry() -> None:
    names = list_problems()
    assert "MPDMP13" in names
    d = get_problem("MPDMP13").describe()
    assert d["n_dm"] == 2
    assert d["n_obj_per_dm"] == [2, 2]

"""Pareto-set property tests."""

from __future__ import annotations

import numpy as np
import pytest

from fairmoo_benchmarks import get_problem


@pytest.mark.parametrize("name", ["MPDMP13", "MPDMP17", "MPDMP18", "MPMOP12", "MPMOP15"])
def test_ps_inside_bounds_when_known(name: str) -> None:
    p = get_problem(name)
    for dm in range(p.n_dm):
        ps = p.get_pareto_set(dm=dm, n_points=200)
        assert ps is not None
        assert ps.shape[1] == p.n_var
        assert np.all(ps >= p.xl - 1e-9)
        assert np.all(ps <= p.xu + 1e-9)


def test_mpmop12_g_on_ps() -> None:
    p = get_problem("MPMOP12")
    ps0 = p.get_pareto_set(dm=0, n_points=50)
    assert ps0 is not None
    # On DM1 PS, g1 should be 1
    g1 = 1.0 + np.sum((ps0[:, 1:] - 1.0) ** 2, axis=1)
    assert np.allclose(g1, 1.0, atol=1e-12)

    ps1 = p.get_pareto_set(dm=1, n_points=50)
    assert ps1 is not None
    g2 = 1.0 + np.sum(ps1[:, 1:] ** 2, axis=1)
    assert np.allclose(g2, 1.0, atol=1e-12)

    assert p.get_common_pareto_set().shape[0] == 0


def test_mpmop15_g_on_ps() -> None:
    p = get_problem("MPMOP15")
    assert p.n_dm == 3
    ps1 = p.get_pareto_set(dm=1, n_points=40)
    assert ps1 is not None
    g2 = 1.0 + np.sum((ps1[:, 1:] - 0.5) ** 2, axis=1)
    assert np.allclose(g2, 1.0, atol=1e-12)


def test_mpdmp1_common_ps() -> None:
    p = get_problem("MPDMP1")
    cps = p.get_common_pareto_set(n_points=5)
    assert cps is not None
    assert np.allclose(cps[0], [50, 50])
    F = p.evaluate(np.array([50.0, 50.0]))
    # Distances to (30,70), (70,30), (70,70), (30,30) all equal 20*sqrt(2)
    assert np.allclose(F, 20 * np.sqrt(2))


def test_mpdmp6_common_edge() -> None:
    p = get_problem("MPDMP6")
    cps = p.get_common_pareto_set(n_points=100)
    assert cps is not None
    assert np.allclose(cps[:, 0], 50.0)
    assert np.min(cps[:, 1]) >= 40.0 - 1e-9
    assert np.max(cps[:, 1]) <= 60.0 + 1e-9

"""Analytical tests for MPDMP distance problems."""

from __future__ import annotations

import numpy as np
import pytest

from fairmoo_benchmarks import get_problem


@pytest.mark.parametrize(
    "name",
    ["MPDMP13", "MPDMP14", "MPDMP15", "MPDMP16", "MPDMP17", "MPDMP18"],
)
def test_zero_at_own_reference_points(name: str) -> None:
    problem = get_problem(name)
    for dm in range(problem.n_dm):
        pts = problem.get_reference_points(dm)
        assert pts is not None
        F = problem.evaluate_dm(pts, dm)
        # Diagonal: f_i(p_i) == 0
        for i in range(pts.shape[0]):
            assert np.isclose(F[i, i], 0.0, atol=1e-12)


def test_mpdmp13_definition() -> None:
    p = get_problem("MPDMP13")
    assert p.n_var == 2
    assert np.allclose(p.xl, [0, 0])
    assert np.allclose(p.xu, [100, 100])
    from fairmoo_benchmarks.status import CommonPSStatus
    assert p.common_ps_status is CommonPSStatus.EMPTY
    refs0 = p.get_reference_points(0)
    refs1 = p.get_reference_points(1)
    assert np.allclose(refs0, [[30, 40], [70, 40]])
    assert np.allclose(refs1, [[30, 60], [70, 60]])

    # Midpoint of DM1 segment
    x = np.array([50.0, 40.0])
    f0 = p.evaluate_dm(x, 0)
    assert np.allclose(f0, [20.0, 20.0])
    f1 = p.evaluate_dm(x, 1)
    assert np.allclose(f1, [np.hypot(20, 20), np.hypot(20, 20)])

    cps = p.get_common_pareto_set()
    assert cps is not None and cps.shape == (0, 2)

    ps0 = p.get_pareto_set(dm=0, n_points=100)
    assert ps0 is not None
    assert ps0.shape == (100, 2)
    assert np.allclose(ps0[:, 1], 40.0)
    assert np.all(ps0[:, 0] >= 30 - 1e-9) and np.all(ps0[:, 0] <= 70 + 1e-9)


def test_mpdmp17_three_dms() -> None:
    p = get_problem("MPDMP17")
    assert p.n_dm == 3
    assert p.n_obj_per_dm == [2, 2, 2]
    assert np.allclose(p.get_reference_points(2), [[40, 30], [60, 30]])


@pytest.mark.parametrize(
    "name,expected_rows",
    [
        ("MPDMP13", 100),
        ("MPDMP14", 100),
        ("MPDMP15", 100),
        ("MPDMP16", 100),
        ("MPDMP17", 300),
        ("MPDMP18", 300),
    ],
)
def test_conflict_pf_matches_matlab_sampling_shape(
    name: str, expected_rows: int
) -> None:
    p = get_problem(name)
    pf = p.get_pareto_front()
    assert pf is not None
    assert pf.shape == (expected_rows, p.n_obj)
    assert np.all(np.isfinite(pf))


def test_matlab_concession_cases() -> None:
    two_dm = get_problem("MPDMP13")
    assert np.allclose(two_dm.get_concession(0), [0.0, 0.0])
    assert np.allclose(two_dm.get_concession(0.4), [0.3, 0.7])
    assert np.allclose(two_dm.get_concession(7), [1.0, 1.0])

    three_dm = get_problem("MPDMP17")
    assert np.allclose(three_dm.get_concession(0.4), [0.3, 0.1, 0.6])
    assert np.allclose(three_dm.get_concession(0.7), [1.0, 1.0, 1.0])

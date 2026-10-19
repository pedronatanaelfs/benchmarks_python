"""Analytical tests for MPMOP12/15."""

from __future__ import annotations

import numpy as np
import pytest

from fairmoo_benchmarks import get_problem


def test_mpmop12_midpoint_objectives() -> None:
    p = get_problem("MPMOP12")
    # Point on DM1 PS
    x = np.zeros(p.n_var)
    x[0] = 0.5
    x[1:] = 1.0
    f = p.evaluate_dm(x, 0)
    assert np.allclose(f, [0.5, 0.5])


def test_mpmop15_three_party_ps_ranges() -> None:
    p = get_problem("MPMOP15")
    for dm in range(3):
        ps = p.get_pareto_set(dm=dm, n_points=20)
        assert ps is not None
        assert np.isclose(ps[:, 0].min(), 0.0)
        assert np.isclose(ps[:, 0].max(), 1.0)
        assert np.allclose(ps[:, 1:], 0.5 * dm)


@pytest.mark.parametrize(
    "name,expected_shape",
    [
        ("MPMOP12", (200, 4)),
        ("MPMOP13", (200, 4)),
        ("MPMOP14", (1600, 6)),
        ("MPMOP15", (200, 6)),
        ("MPMOP16", (200, 4)),
        ("MPMOP17", (200, 6)),
    ],
)
def test_zhao_mpmop_pf_matches_matlab_sampling_shape(
    name: str, expected_shape: tuple[int, int]
) -> None:
    p = get_problem(name)
    pf = p.get_pareto_front()
    assert pf is not None
    assert pf.shape == expected_shape
    assert np.all(np.isfinite(pf))
    assert p.get_common_pareto_set().shape == (0, p.n_var)

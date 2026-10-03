"""Analytical tests for MPMOP12/15."""

from __future__ import annotations

import numpy as np

from fairmoo_benchmarks import get_problem


def test_mpmop12_midpoint_objectives() -> None:
    p = get_problem("MPMOP12")
    # Point on DM1 PS
    x = np.zeros(p.n_var)
    x[0] = 1.5
    x[1:] = 0.5
    f = p.evaluate_dm(x, 0)
    # g1=1; f11=2/x1; f12=x1/2
    assert np.allclose(f, [2.0 / 1.5, 1.5 / 2.0])


def test_mpmop15_three_party_ps_ranges() -> None:
    p = get_problem("MPMOP15")
    for dm, (lo, hi) in enumerate([(1, 2), (2, 3), (3, 4)]):
        ps = p.get_pareto_set(dm=dm, n_points=20)
        assert ps is not None
        assert ps[:, 0].min() >= lo - 1e-12
        assert ps[:, 0].max() <= hi + 1e-12

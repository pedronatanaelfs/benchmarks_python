"""Bounds tests."""

from __future__ import annotations

import numpy as np
import pytest

from fairmoo_benchmarks import get_problem, list_problems


@pytest.mark.parametrize("name", list_problems())
def test_bounds_consistent(name: str) -> None:
    p = get_problem(name)
    assert p.xl.shape == (p.n_var,)
    assert p.xu.shape == (p.n_var,)
    assert np.all(p.xl <= p.xu)

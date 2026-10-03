"""Pymoo adapter consistency tests."""

from __future__ import annotations

import numpy as np
import pytest

from fairmoo_benchmarks import get_problem
from fairmoo_benchmarks.pymoo import PymooMultiPartyAdapter


@pytest.mark.parametrize("name", ["MPMOP1", "MPMOP15", "MPDMP13", "MPDMP17"])
def test_pymoo_matches_base(name: str) -> None:
    base = get_problem(name)
    adapter = PymooMultiPartyAdapter(base)
    assert adapter.n_var == base.n_var
    assert adapter.n_obj == base.n_obj == sum(base.n_obj_per_dm)
    assert np.allclose(adapter.xl, base.xl)
    assert np.allclose(adapter.xu, base.xu)

    rng = np.random.default_rng(42)
    X = rng.uniform(base.xl, base.xu, size=(25, base.n_var))
    F_base = base.evaluate(X)
    out = {}
    adapter._evaluate(X, out)
    assert np.allclose(out["F"], F_base)

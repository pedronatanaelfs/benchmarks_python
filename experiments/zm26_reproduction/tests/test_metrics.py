import numpy as np

from experiments.zm26_reproduction.metrics.gini import gini_coefficient
from experiments.zm26_reproduction.metrics.igd import igd
from experiments.zm26_reproduction.metrics.jain import jain_index
from experiments.zm26_reproduction.metrics.mean_igd import mean_igd


def test_igd_zero_on_identical_sets():
    pf = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    assert igd(pf, pf) == 0.0


def test_mean_igd_party_wise():
    pf = [np.array([[0.0, 0.0], [1.0, 0.0]]), np.array([[0.0, 1.0], [1.0, 1.0]])]
    F = np.array([[0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 1.0, 1.0]])
    slices = [slice(0, 2), slice(2, 4)]
    assert mean_igd(F, pf, slices) == 0.0


def test_jain_perfectly_equal():
    assert abs(jain_index(np.array([2.0, 2.0, 2.0])) - 1.0) < 1e-12


def test_gini_equal_is_zero():
    assert abs(gini_coefficient(np.array([3.0, 3.0, 3.0]))) < 1e-12


def test_offset_matches_broadcast_chebyshev():
    from experiments.zm26_reproduction.metrics.concession import offset_to_pf

    rng = np.random.default_rng(0)
    pts = rng.random((12, 2))
    pf = rng.random((9, 2))
    fmax = np.array([1.0, 2.0])
    got = offset_to_pf(pts, pf, fmax, max_pf_size=100, rng=rng)
    diff = np.abs(pts[:, None, :] - pf[None, :, :]) / fmax
    expect = diff.max(axis=2).min(axis=1)
    assert np.allclose(got, expect)

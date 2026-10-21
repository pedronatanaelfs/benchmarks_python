import numpy as np

from experiments.zm26_reproduction.metrics.nash_score import nash_components


def _toy():
    pf1 = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    pf2 = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    F = np.array(
        [
            [0.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 1.0],
        ]
    )
    slices = [slice(0, 2), slice(2, 4)]
    return F, [pf1, pf2], slices


def test_perfect_match_has_high_matlab_exp_score():
    F, pf, slices = _toy()
    det = nash_components(
        F, pf, slices, epsilon=np.zeros(2), lambda_=1.0, C=10.0, rng=np.random.default_rng(0)
    )
    assert det.nash_exp > 0.5
    assert np.all(det.mu < 1e-12)


def test_imbalanced_population_has_lower_product_than_balanced():
    pf = [np.array([[0.0, 0.0], [1.0, 0.0]]), np.array([[0.0, 0.0], [0.0, 1.0]])]
    slices = [slice(0, 2), slice(2, 4)]
    balanced = np.array([[0.1, 0.0, 0.0, 0.1], [0.0, 0.1, 0.1, 0.0]])
    biased = np.array([[0.0, 0.0, 5.0, 5.0], [0.01, 0.0, 4.0, 4.0]])
    b = nash_components(balanced, pf, slices, np.zeros(2), 1.0, C=20.0, rng=np.random.default_rng(1))
    w = nash_components(biased, pf, slices, np.zeros(2), 1.0, C=20.0, rng=np.random.default_rng(1))
    assert b.nash_C > w.nash_C
    assert w.utility_C[1] < w.utility_C[0]


def test_unequal_objectives_per_dm_do_not_crash():
    """MPDMP3-style 2+3 objectives; MATLAB nash_score.m cannot run this case."""
    pf = [np.array([[0.0, 0.0], [1.0, 0.0]]), np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])]
    F = np.array([[0.1, 0.0, 0.1, 0.0, 0.0], [0.0, 0.1, 0.0, 0.1, 0.0]])
    slices = [slice(0, 2), slice(2, 5)]
    det = nash_components(F, pf, slices, np.zeros(2), 1.0, C=20.0, rng=np.random.default_rng(0))
    assert np.isfinite(det.nash_C)
    assert det.mu.shape == (2,)


def test_raising_concession_threshold_does_not_decrease_score():
    pf = [np.linspace([0, 0], [1, 0], 20), np.linspace([0, 1], [1, 1], 20)]
    F = np.array([[0.2, 0.2, 0.2, 0.8], [0.5, 0.1, 0.5, 0.6]])
    slices = [slice(0, 2), slice(2, 4)]
    low = nash_components(F, pf, slices, np.zeros(2), 1.0, C=50.0, rng=np.random.default_rng(2))
    high = nash_components(F, pf, slices, np.ones(2) * 0.7, 1.0, C=50.0, rng=np.random.default_rng(2))
    assert high.nash_C + 1e-12 >= low.nash_C

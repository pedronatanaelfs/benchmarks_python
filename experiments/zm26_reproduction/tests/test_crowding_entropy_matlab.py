"""Regression: CrowdingEntropy.m NaN/Inf/finite pattern from the diagnostic."""

from pathlib import Path

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms.operators import crowding_distance, crowding_entropy

DIAG = Path(__file__).resolve().parents[1] / "debug_matlab_python"


def _class_mask(a: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    a = np.asarray(a, dtype=float)
    return np.isfinite(a), np.isnan(a), np.isinf(a)


def test_crowding_entropy_matches_matlab_classes_and_finite_values():
    F = np.loadtxt(DIAG / "shared_inputs" / "crowding_F.csv", delimiter=",")
    front = np.loadtxt(DIAG / "shared_inputs" / "crowding_front.csv", delimiter=",").reshape(-1)
    matlab = pd.read_csv(DIAG / "matlab_outputs" / "test_03_crowding.csv")
    ce = crowding_entropy(F, front)
    cd = crowding_distance(F, front)
    m_ce = matlab["entropy_value"].to_numpy(dtype=float)
    m_cd = matlab["crowding_value"].to_numpy(dtype=float)
    py_fin, py_nan, py_inf = _class_mask(ce)
    ma_fin, ma_nan, ma_inf = _class_mask(m_ce)
    assert np.array_equal(py_nan, ma_nan)
    assert np.array_equal(py_inf, ma_inf)
    assert np.array_equal(py_fin, ma_fin)
    if py_fin.any():
        np.testing.assert_allclose(ce[py_fin], m_ce[ma_fin], atol=1e-9, rtol=1e-12)
    # crowding distance (OptMPNDS) still matches including Inf
    np.testing.assert_allclose(
        np.where(np.isfinite(cd), cd, 0.0),
        np.where(np.isfinite(m_cd), m_cd, 0.0),
        atol=1e-9,
    )
    assert np.array_equal(np.isinf(cd), np.isinf(m_cd))

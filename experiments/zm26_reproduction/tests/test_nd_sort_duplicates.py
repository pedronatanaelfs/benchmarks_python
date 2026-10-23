"""Regression: MATLAB NDSort/MPNDS/PLNDS ranks on the diagnostic duplicate matrix."""

from pathlib import Path

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms.operators import mpnds, nd_sort, plnds

DIAG = Path(__file__).resolve().parents[1] / "debug_matlab_python"
SLICES = [slice(0, 3), slice(3, 6)]


def test_nd_sort_mpnds_plnds_match_matlab_test02():
    F = np.loadtxt(DIAG / "shared_inputs" / "mpnds_F.csv", delimiter=",")
    matlab = pd.read_csv(DIAG / "matlab_outputs" / "test_02_mpn_sorting.csv")
    n = F.shape[0]
    front_dm1, _ = nd_sort(F[:, SLICES[0]], n)
    front_dm2, _ = nd_sort(F[:, SLICES[1]], n)
    combined, _ = mpnds(F, SLICES, n)
    pl, _ = plnds(F, SLICES, n)
    np.testing.assert_array_equal(front_dm1, matlab["front_DM1"].to_numpy())
    np.testing.assert_array_equal(front_dm2, matlab["front_DM2"].to_numpy())
    np.testing.assert_array_equal(combined, matlab["combined_front"].to_numpy())
    np.testing.assert_array_equal(pl, matlab["plnds_front"].to_numpy())
    assert np.all(np.isfinite(front_dm1))
    assert np.all(np.isfinite(combined))

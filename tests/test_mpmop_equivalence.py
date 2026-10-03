"""Octave equivalence tests for MPMOP_Value (MPMOP1–11)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

from fairmoo_benchmarks.mpmop.liu2020 import mpmop_value

OCT_DIR = Path(__file__).resolve().parents[1] / "validation" / "matlab_octave"
OCTAVE = shutil.which("octave")

PROBLEMS = [
    ("MPMOP1", "MPMOP1", 1.0),
    ("MPMOP2", "MPMOP2", 0.0),
    ("MPMOP5", "MPMOP5", 1.5),
    ("MPMOP6", "MPMOP6", 1.0),
]


@pytest.mark.skipif(OCTAVE is None, reason="GNU Octave not available")
@pytest.mark.parametrize("name,value_id,t", PROBLEMS)
def test_mpmop_value_octave(name: str, value_id: str, t: float) -> None:
    from fairmoo_benchmarks import get_problem

    p = get_problem(name)
    rng = np.random.default_rng(0)
    X = np.vstack(
        [
            p.xl,
            p.xu,
            0.5 * (p.xl + p.xu),
            rng.uniform(p.xl, p.xu, size=(30, p.n_var)),
        ]
    )
    xin = OCT_DIR / f"_pytest_{name}_X.csv"
    xout = OCT_DIR / f"_pytest_{name}_F.csv"
    np.savetxt(xin, X, delimiter=",")
    cmd = (
        f"addpath('{OCT_DIR}'); "
        f"eval_mpmop_value('{value_id}', {t:.16g}, '{xin}', '{xout}');"
    )
    subprocess.run(
        [OCTAVE, "--quiet", "--no-gui", "--eval", cmd],
        check=True,
        capture_output=True,
        text=True,
    )
    F_oct = np.loadtxt(xout, delimiter=",")
    if F_oct.ndim == 1:
        F_oct = F_oct.reshape(-1, 1)
    F_py = mpmop_value(value_id, X, t)
    assert np.allclose(F_py, F_oct, rtol=1e-8, atol=1e-10)

#!/usr/bin/env python3
"""Run Octave MPMOP_Value equivalence checks for MPMOP1–MPMOP11."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OCT_DIR = ROOT / "validation" / "matlab_octave"
REF_DIR = ROOT / "validation" / "reference_values"
EQ_DIR = ROOT / "validation" / "equivalence"
sys.path.insert(0, str(ROOT / "src"))

from fairmoo_benchmarks import get_problem  # noqa: E402
from fairmoo_benchmarks.mpmop.liu2020 import mpmop_value  # noqa: E402

# (problem_name, value_id, times)
PROBLEMS = [
    ("MPMOP1", "MPMOP1", [1.0, 2.0]),
    ("MPMOP2", "MPMOP2", [0.0, 3.0]),
    ("MPMOP3", "MPMOP3", [0.0, float(np.pi / 2)]),
    ("MPMOP4", "MPMOP4", [0.0, 1.0]),
    ("MPMOP5", "MPMOP5", [0.0, 1.5]),
    ("MPMOP6", "MPMOP6", [0.0, 1.0]),
    ("MPMOP7", "MPMOP1", [0.0, 1.0, 2.0]),
    ("MPMOP8", "MPMOP2", [0.0, 1.0, 3.0]),
    ("MPMOP9", "MPMOP4", [0.0, 0.5, 1.0]),
    ("MPMOP10", "MPMOP5", [0.0, 1.0, 1.5]),
    ("MPMOP11", "MPMOP6", [0.0, 1.0, 1.5]),
]


def make_X(problem, n_random: int = 100, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    mid = 0.5 * (problem.xl + problem.xu)
    corners = np.vstack([problem.xl, problem.xu, mid])
    rand = rng.uniform(problem.xl, problem.xu, size=(n_random, problem.n_var))
    blocks = [corners, rand]
    ps = problem.get_pareto_set(dm=0, n_points=20)
    if ps is not None and ps.size:
        blocks.append(ps)
    return np.vstack(blocks)


def run_octave_value(value_id: str, t: float, X: np.ndarray, tag: str) -> np.ndarray:
    xin = OCT_DIR / f"_tmp_{tag}_X.csv"
    xout = OCT_DIR / f"_tmp_{tag}_F.csv"
    np.savetxt(xin, X, delimiter=",")
    cmd = (
        f"addpath('{OCT_DIR}'); "
        f"eval_mpmop_value('{value_id}', {t:.16g}, '{xin}', '{xout}');"
    )
    subprocess.run(
        ["octave", "--quiet", "--no-gui", "--eval", cmd],
        check=True,
        cwd=str(OCT_DIR),
        capture_output=True,
        text=True,
    )
    return np.loadtxt(xout, delimiter=",")


def main() -> int:
    EQ_DIR.mkdir(parents=True, exist_ok=True)
    REF_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for name, value_id, times in PROBLEMS:
        problem = get_problem(name)
        X = make_X(problem)
        np.savetxt(REF_DIR / f"{name}_input.csv", X, delimiter=",")
        F_py_blocks = []
        F_oct_blocks = []
        ok = True
        detail = []
        for i, t in enumerate(times):
            F_py = mpmop_value(value_id, X, t)
            try:
                F_oct = run_octave_value(value_id, t, X, f"{name}_t{i}")
            except Exception as exc:  # noqa: BLE001
                ok = False
                detail.append(f"octave_error t={t}: {exc}")
                F_oct = np.full_like(F_py, np.nan)
            if F_oct.ndim == 1:
                F_oct = F_oct.reshape(-1, 1)
            match = np.allclose(F_py, F_oct, rtol=1e-8, atol=1e-10, equal_nan=False)
            ok = ok and match
            max_abs = float(np.nanmax(np.abs(F_py - F_oct)))
            detail.append(f"t={t}: match={match}, max_abs={max_abs:.3e}")
            F_py_blocks.append(F_py)
            F_oct_blocks.append(F_oct)
        F_py_all = np.concatenate(F_py_blocks, axis=1)
        F_oct_all = np.concatenate(F_oct_blocks, axis=1)
        np.savetxt(REF_DIR / f"{name}_python.csv", F_py_all, delimiter=",")
        np.savetxt(REF_DIR / f"{name}_octave.csv", F_oct_all, delimiter=",")
        status = "PASS" if ok else "FAIL"
        report = EQ_DIR / f"{name}.md"
        report.write_text(
            f"# Equivalence {name}\n\n"
            f"- value_id: `{value_id}`\n"
            f"- times: {times}\n"
            f"- n_points: {X.shape[0]}\n"
            f"- rtol=1e-8, atol=1e-10\n"
            f"- status: **{status}**\n\n"
            + "\n".join(f"- {d}" for d in detail)
            + "\n"
        )
        results.append((name, status))
        print(name, status, detail)

    summary = EQ_DIR / "summary.md"
    n_pass = sum(1 for _, s in results if s == "PASS")
    summary.write_text(
        "# Octave equivalence summary (MPMOP1–11 via MPMOP_Value.m)\n\n"
        + "\n".join(f"- {n}: {s}" for n, s in results)
        + f"\n\nPASS: {n_pass}/{len(results)}\n"
    )
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

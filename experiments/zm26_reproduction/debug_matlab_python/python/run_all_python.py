"""Generate shared inputs and run all Python diagnostics."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# python/ -> debug_matlab_python -> zm26_reproduction -> experiments -> repo
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from experiments.zm26_reproduction.debug_matlab_python.python.generate_shared_inputs import main as gen_inputs
from experiments.zm26_reproduction.debug_matlab_python.python.paths import PYTHON_OUT, ensure_dirs
from experiments.zm26_reproduction.debug_matlab_python.python import (
    test_01_problem,
    test_02_mpn_sorting,
    test_03_crowding,
    test_04_environmental_selection,
    test_05_initialization,
    test_06_variation,
    test_07_short_run,
    test_08_unique_rows,
    test_09_one_by_one,
    test_10_boundary,
    test_11_objective_grouping,
    test_12_native_runs,
    test_13_jade2,
)


def main(include_native: bool = True) -> None:
    ensure_dirs()
    print("=== generating shared_inputs ===")
    gen_inputs()
    tests = [
        test_01_problem,
        test_02_mpn_sorting,
        test_03_crowding,
        test_04_environmental_selection,
        test_05_initialization,
        test_06_variation,
        test_07_short_run,
        test_08_unique_rows,
        test_09_one_by_one,
        test_10_boundary,
        test_11_objective_grouping,
        test_13_jade2,
    ]
    for mod in tests:
        print(f"=== {mod.__name__} ===")
        mod.run()
    if include_native:
        print("=== test_12_native_runs (5 OptMPNDS MPDMP4 runs, N=200 FE=80000) ===")
        test_12_native_runs.run(n_runs=5)
    else:
        print("skipped test_12 native runs")
    print(f"Python diagnostics written to {PYTHON_OUT}")
    print("WAITING for MATLAB outputs in matlab_outputs/ before compare_outputs.py")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--skip-native", action="store_true")
    args = p.parse_args()
    main(include_native=not args.skip_native)

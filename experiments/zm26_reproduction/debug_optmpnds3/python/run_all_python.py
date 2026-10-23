"""Generate shared inputs and run Python OptMPNDS3 diagnostics."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from experiments.zm26_reproduction.debug_optmpnds3.python.generate_shared_inputs import main as gen_inputs
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT, ensure_dirs
from experiments.zm26_reproduction.debug_optmpnds3.python import (
    test_01_pft_initialization,
    test_02_initial_population_quality,
    test_03_archive_initialization,
    test_04_pbest_selection,
    test_05_f_cr_adaptation,
    test_06_archive_update,
    test_07_env_selection_integration,
    test_08_short_trace,
    test_09_native_5run,
)


def main(include_native: bool = False) -> None:
    ensure_dirs()
    print("=== generating shared_inputs ===")
    gen_inputs()
    tests = [
        test_04_pbest_selection,
        test_05_f_cr_adaptation,
        test_06_archive_update,
        test_07_env_selection_integration,
        test_08_short_trace,
        test_03_archive_initialization,
        test_01_pft_initialization,
        test_02_initial_population_quality,
    ]
    for mod in tests:
        print(f"=== {mod.__name__} ===")
        if mod is test_01_pft_initialization:
            mod.run(seeds=(1, 2, 3))
        else:
            mod.run()
    if include_native:
        print("=== test_09_native_5run MPDMP1 ===")
        test_09_native_5run.run(problems=("MPDMP1",), n_runs=5)
    else:
        print("skipped test_09 native 5-run (pass --native)")
    print(f"Python diagnostics written to {PYTHON_OUT}")
    print("WAITING for MATLAB matlab_outputs/ then: python compare_optmpnds3_outputs.py")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--native", action="store_true")
    args = p.parse_args()
    main(include_native=args.native)

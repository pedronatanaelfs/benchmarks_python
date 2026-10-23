#!/usr/bin/env python3
"""Convenience wrapper. From the repo root prefer:

    python -m experiments.zm26_reproduction.debug_matlab_python.python.run_all_python
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from experiments.zm26_reproduction.debug_matlab_python.python.run_all_python import main

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--skip-native", action="store_true")
    args = p.parse_args()
    main(include_native=not args.skip_native)

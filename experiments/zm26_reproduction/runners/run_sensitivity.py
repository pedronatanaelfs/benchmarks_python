"""Sensitivity uses stored populations / raw CSV; no extra optimizer runs.

Concession thresholds are evaluation parameters (ZM26 Table S-IV). They are
applied in ``evaluate_population.evaluate_conditions`` for every non-consensus
benchmark. This entry point only verifies that those conditions exist.
"""

from __future__ import annotations

import csv
from collections import Counter

from ..config.settings import CONCESSION_CASES, NONCONSENSUS_BENCHMARKS
from .jobs import RAW_CSV


def main() -> int:
    if not RAW_CSV.exists():
        raise SystemExit(f"missing {RAW_CSV}; run the optimizer jobs first")
    with RAW_CSV.open() as f:
        rows = list(csv.DictReader(f))
    wanted = set(CONCESSION_CASES)
    found = Counter()
    for row in rows:
        if row["benchmark"] in NONCONSENSUS_BENCHMARKS:
            found[(row["benchmark"], row["condition"])] += 1
    missing = []
    for name in NONCONSENSUS_BENCHMARKS:
        for case in wanted:
            if found[(name, case)] == 0:
                missing.append((name, case))
    if missing:
        print("missing conditions:", missing[:20], "...")
        return 1
    print(f"sensitivity conditions present for {len(NONCONSENSUS_BENCHMARKS)} benchmarks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms.operators import crowding_distance, crowding_entropy

from .csv_io import load_matrix, save_table
from .paths import PYTHON_OUT, SHARED

KEEP = 5


def run() -> None:
    F = load_matrix(SHARED / "lastfront_F.csv")
    n = F.shape[0]
    # OptMPNDS production: one-shot crowding sort (NOT iterative)
    front = np.ones(n)
    cd = crowding_distance(F, front)
    order = np.argsort(-cd, kind="mergesort")
    keep_oneshot = np.sort(order[:KEEP]) + 1

    # OptMPNDS3-style iterative entropy removal
    last = list(range(n))
    trace = []
    while len(last) > KEEP:
        ce = crowding_entropy(F[last], np.ones(len(last)))
        j = int(np.argmin(ce))
        removed = last[j]
        trace.append(
            {
                "iteration": len(trace) + 1,
                "candidate_removed_1based": removed + 1,
                "entropy_of_removed": float(ce[j]),
                "remaining_after": ",".join(str(i + 1) for i in last if i != removed),
            }
        )
        last.pop(j)

    save_table(
        PYTHON_OUT / "test_09_optmpnds_oneshot.csv",
        pd.DataFrame({"kept_1based": keep_oneshot, "crowding": cd[keep_oneshot - 1]}),
    )
    save_table(PYTHON_OUT / "test_09_optmpnds3_iterative.csv", pd.DataFrame(trace))
    save_table(
        PYTHON_OUT / "test_09_notes.csv",
        pd.DataFrame(
            {
                "note": [
                    "OptMPNDS MATLAB EnvironmentalSelection sorts crowding ONCE (oneshot).",
                    "OptMPNDS3 MATLAB removes worst entropy one-by-one, recalculating each time.",
                    "Python production OptMPNDS matches oneshot; OptMPNDS3 matches iterative.",
                ]
            }
        ),
    )
    print("python test_09 done")


if __name__ == "__main__":
    run()

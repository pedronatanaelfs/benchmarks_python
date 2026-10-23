"""Gen-0 quality from test_01 dumps + comparison to paper Table III OptMPNDS3."""

from __future__ import annotations

import pandas as pd

from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import quality_row
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT
from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import load_matrix

PAPER = {"MPDMP1": 0.0447, "MPDMP4": 0.0133}


def run() -> None:
    rows = []
    for name in ("MPDMP1", "MPDMP4"):
        X = load_matrix(PYTHON_OUT / f"{name.lower()}_init_X.csv")
        F = load_matrix(PYTHON_OUT / f"{name.lower()}_init_F.csv")
        q = quality_row(name, X, F, tag="python_gen0_seed1")
        q["paper_final_zm26"] = PAPER[name]
        q["init_vs_paper_ratio"] = q["zm26_meanIGD"] / PAPER[name]
        rows.append(q)
        print(
            f"{name} gen0 zm26={q['zm26_meanIGD']:.4g} party={q['party_pf_meanIGD']:.4g} "
            f"meanDistPS={q['mean_dist_to_common_ps']:.3g} n={q['n']} "
            f"paper_final={PAPER[name]}"
        )
    save_table(PYTHON_OUT / "test_02_initial_population_quality.csv", pd.DataFrame(rows))
    print("python test_02 done")


if __name__ == "__main__":
    run()

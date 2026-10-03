"""Run NSGA-II on a small multi-party problem (concatenated objectives)."""

from __future__ import annotations

import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination

from fairmoo_benchmarks import get_problem
from fairmoo_benchmarks.pymoo import PymooMultiPartyAdapter


def main() -> None:
    base = get_problem("MPDMP13")  # 4 objectives total
    problem = PymooMultiPartyAdapter(base)
    algorithm = NSGA2(pop_size=80)
    res = minimize(
        problem,
        algorithm,
        get_termination("n_gen", 50),
        seed=42,
        verbose=True,
    )
    print("n_dm:", base.n_dm, "n_obj_per_dm:", base.n_obj_per_dm)
    print("Final population decision shape:", res.X.shape)
    print("Final population objective shape:", res.F.shape)
    # Party-wise objectives remain available
    F_dm0 = base.evaluate_dm(res.X, 0)
    print("DM1 objective head:\n", F_dm0[:3])


if __name__ == "__main__":
    main()

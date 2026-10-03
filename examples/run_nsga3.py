"""Run NSGA-III on a higher-objective multi-party problem."""

from __future__ import annotations

from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.util.ref_dirs import get_reference_directions

from fairmoo_benchmarks import get_problem
from fairmoo_benchmarks.pymoo import PymooMultiPartyAdapter


def main() -> None:
    base = get_problem("MPDMP17")  # 6 objectives
    problem = PymooMultiPartyAdapter(base)
    ref_dirs = get_reference_directions("das-dennis", problem.n_obj, n_partitions=4)
    algorithm = NSGA3(ref_dirs=ref_dirs, pop_size=ref_dirs.shape[0])
    res = minimize(
        problem,
        algorithm,
        get_termination("n_gen", 40),
        seed=42,
        verbose=True,
    )
    print("n_obj total:", problem.n_obj)
    print("Final X/F:", None if res.X is None else res.X.shape, None if res.F is None else res.F.shape)
    for dm in range(base.n_dm):
        print(f"DM{dm+1} obj block shape:", base.evaluate_dm(res.X, dm).shape)


if __name__ == "__main__":
    main()

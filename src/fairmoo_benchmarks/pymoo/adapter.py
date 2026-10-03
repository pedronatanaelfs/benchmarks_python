"""pymoo adapter for MultiPartyProblem."""

from __future__ import annotations

import numpy as np
from pymoo.core.problem import Problem

from fairmoo_benchmarks.base import MultiPartyProblem


class PymooMultiPartyAdapter(Problem):
    """Wrap a MultiPartyProblem as a pymoo Problem with concatenated objectives.

    The original multi-DM ownership remains available via ``.base`` /
    ``evaluate_dm``.
    """

    def __init__(self, problem: MultiPartyProblem):
        self.base = problem
        super().__init__(
            n_var=problem.n_var,
            n_obj=problem.n_obj,
            xl=problem.xl.copy(),
            xu=problem.xu.copy(),
        )

    def _evaluate(self, X, out, *args, **kwargs):
        out["F"] = np.asarray(self.base.evaluate(X), dtype=float)

    def evaluate_dm(self, X, dm: int):
        return self.base.evaluate_dm(X, dm)

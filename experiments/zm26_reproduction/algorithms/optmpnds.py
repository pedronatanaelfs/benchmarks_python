"""OptMPNDS — multi-party non-dominated sorting (Liu et al. 2020).

Original MATLAB: OptMPNDS-master/Algorithms/OptMPNDS/OptMPNDS.m
                 EnvironmentalSelection.m + Public/MPNDS.m
She MPDMP port uses cell-DM slices (2022SheOptMPNDS3/Public/MPNDS.m).
"""

from __future__ import annotations

import numpy as np

from .operators import (
    environmental_selection,
    random_population,
    sbx_pm,
    tournament_selection,
)


class OptMPNDS:
    name = "OptMPNDS"
    matlab_source = "OptMPNDS-master/Algorithms/OptMPNDS/OptMPNDS.m"
    selection = "MPNDS (intersection of party-wise fronts) + crowding distance"
    variation = "SBX + polynomial mutation (PlatEMO GA.m)"

    def __init__(
        self,
        *,
        population_size: int = 100,
        evaluation_budget: int = 10000,
        pro_c: float = 1.0,
        dis_c: float = 20.0,
        pro_m: float = 1.0,
        dis_m: float = 20.0,
        mutation_as_expectation: bool = True,
    ) -> None:
        self.population_size = int(population_size)
        self.evaluation_budget = int(evaluation_budget)
        self.pro_c = pro_c
        self.dis_c = dis_c
        self.pro_m = pro_m
        self.dis_m = dis_m
        self.mutation_as_expectation = mutation_as_expectation

    def run(self, problem, rng: np.random.Generator, slices):
        n = self.population_size
        X = random_population(rng, n, problem.xl, problem.xu)
        F = problem.evaluate(X)
        evaluated = n
        X, F, front, crowd = environmental_selection(
            X, F, n, mode="optmpnds", slices=slices
        )
        while evaluated < self.evaluation_budget:
            mating = tournament_selection(rng, 2, n, front, -crowd)
            off_x = sbx_pm(
                rng,
                X[mating],
                problem.xl,
                problem.xu,
                pro_c=self.pro_c,
                dis_c=self.dis_c,
                pro_m=self.pro_m,
                dis_m=self.dis_m,
                mutation_as_expectation=self.mutation_as_expectation,
            )
            remaining = self.evaluation_budget - evaluated
            if off_x.shape[0] > remaining:
                off_x = off_x[:remaining]
            off_f = problem.evaluate(off_x)
            evaluated += off_x.shape[0]
            X, F, front, crowd = environmental_selection(
                np.vstack([X, off_x]),
                np.vstack([F, off_f]),
                n,
                mode="optmpnds",
                slices=slices,
            )
        return X, F

"""OptMPNDS2 — PLNDS / MPNDS2 (She et al. 2021/2023).

Original MATLAB: 2022SheOptMPNDS3/Algorithms/OptMPNDS2/OptMPNDS2.m
                 EnvironmentalSelection.m uses Public/PLNDS.m
"""

from __future__ import annotations

import numpy as np

from .operators import (
    environmental_selection,
    random_population,
    sbx_pm,
    tournament_selection,
)


class OptMPNDS2:
    name = "OptMPNDS2"
    matlab_source = (
        "benchmarks_python/sources/mpdmp_2023/2022SheOptMPNDS3/"
        "Algorithms/OptMPNDS2/OptMPNDS2.m"
    )
    selection = "PLNDS (NDSort of party-wise ranks) + crowding distance"
    variation = "SBX + polynomial mutation"

    def __init__(
        self,
        *,
        population_size: int = 200,
        evaluation_budget: int = 80000,
        pro_c: float = 1.0,
        dis_c: float = 15.0,
        pro_m: float = 0.5,
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
            X, F, n, mode="optmpnds2", slices=slices
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
                mode="optmpnds2",
                slices=slices,
            )
        return X, F

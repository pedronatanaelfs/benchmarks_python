"""OptMPNDS3 — PFt initialization + JADE2 (She et al., 2023).

Original MATLAB:
  Algorithms/OptMPNDS3/OptMPNDS3.m
  getPF.m, EnvironmentalSelection.m, EnvironmentalSelection1.m
  Public/CrowdingEntropy.m, getBestIndividual.m, dominated.m

Faithful limitations copied from the MATLAB source:
- ``getPF`` only initializes the first two decision makers.
- JADE parameters: p=0.05, c=0.05 (She 2023, Section 5.1).
- FEI = 10000 evaluations per initialized party, counted in the budget.
"""

from __future__ import annotations

import numpy as np

from .operators import (
    crowding_entropy,
    environmental_selection,
    nd_sort,
    random_population,
    sbx_pm,
    tournament_selection,
)


def _party_nsga2(problem, rng, sl, n, n_evals, xl, xu):
    X = random_population(rng, n, xl, xu)
    Ffull = problem.evaluate(X)
    evaluated = n
    F = Ffull[:, sl]
    front, _ = nd_sort(F, n)
    crowd = crowding_entropy(F, front)  # selection1 uses crowding distance in MATLAB
    from .operators import crowding_distance

    crowd = crowding_distance(F, front)
    while evaluated < n_evals:
        mating = tournament_selection(rng, 2, n, front, -crowd)
        off_x = sbx_pm(
            rng, X[mating], xl, xu, dis_c=15.0, pro_m=0.5, mutation_as_expectation=True
        )
        remaining = n_evals - evaluated
        if off_x.shape[0] > remaining:
            off_x = off_x[:remaining]
        off_full = problem.evaluate(off_x)
        evaluated += off_x.shape[0]
        Xc = np.vstack([X, off_x])
        Fc = np.vstack([Ffull, off_full])
        Fp = Fc[:, sl]
        front, max_fno = nd_sort(Fp, n)
        crowd = crowding_distance(Fp, front)
        next_mask = front < max_fno
        last = np.where(front == max_fno)[0]
        n_fill = n - int(next_mask.sum())
        if n_fill > 0 and last.size:
            order = np.argsort(-crowd[last], kind="mergesort")
            next_mask[last[order[:n_fill]]] = True
        X, Ffull = Xc[next_mask], Fc[next_mask]
        F = Ffull[:, sl]
        front, crowd = front[next_mask], crowd[next_mask]
    front, _ = nd_sort(F, n)
    return X[front == 1], Ffull[front == 1]


def _mp_dominates(fa: np.ndarray, fb: np.ndarray, slices) -> bool:
    ranks = []
    stacked = np.vstack([fa, fb])
    for sl in slices:
        r, _ = nd_sort(stacked[:, sl], 2)
        ranks.append(r)
    temp = np.column_stack(ranks)
    front, _ = nd_sort(temp, 2)
    return bool(front[1] == 2)


def _pbest(rng, X, front, crowd, p=0.05):
    n = X.shape[0]
    top = max(int(np.ceil(n * p)), 1)
    k = int(rng.integers(1, top + 1))
    order = np.lexsort((-crowd, front))
    return X[order[k - 1]]


def _update_archive(archive_x, archive_f, x, f, n_max):
    if archive_x.shape[0] < n_max:
        return np.vstack([archive_x, x[None, :]]), np.vstack([archive_f, f[None, :]])
    d = np.linalg.norm(archive_x - x[None, :], axis=1)
    i = int(np.argmin(d))
    archive_x[i] = x
    archive_f[i] = f
    return archive_x, archive_f


class OptMPNDS3:
    name = "OptMPNDS3"
    matlab_source = (
        "benchmarks_python/sources/mpdmp_2023/2022SheOptMPNDS3/"
        "Algorithms/OptMPNDS3/OptMPNDS3.m"
    )
    selection = "PLNDS + crowding entropy (one-by-one truncation)"
    variation = "JADE2 current-to-pbest/1/bin, p=0.05, c=0.05"
    initialization = "PFt: NSGA-II on first two DMs, FEI=10000 each"

    def __init__(
        self,
        *,
        population_size: int = 200,
        evaluation_budget: int = 80000,
        fei: int = 10000,
        p: float = 0.05,
        c: float = 0.05,
    ) -> None:
        self.population_size = int(population_size)
        self.evaluation_budget = int(evaluation_budget)
        self.fei = int(fei)
        self.p = p
        self.c = c

    def run(self, problem, rng: np.random.Generator, slices):
        n = self.population_size
        evaluated = 0
        parts_x = []
        parts_f = []
        n_init_dm = min(2, len(slices))
        for i in range(n_init_dm):
            budget = evaluated + self.fei
            budget = min(budget, self.evaluation_budget)
            Xi, Fi = _party_nsga2(
                problem, rng, slices[i], 100, budget - evaluated, problem.xl, problem.xu
            )
            evaluated += min(self.fei, self.evaluation_budget - evaluated)
            parts_x.append(Xi)
            parts_f.append(Fi)
            if evaluated >= self.evaluation_budget:
                break
        if parts_x:
            X = np.vstack(parts_x)
            F = np.vstack(parts_f)
        else:
            X = random_population(rng, n, problem.xl, problem.xu)
            F = problem.evaluate(X)
            evaluated += n
        X, F, front, crowd = environmental_selection(
            X, F, X.shape[0], mode="optmpnds3", slices=slices
        )
        mu_cr, mu_f = 0.5, 0.5
        archive_x = np.zeros((0, X.shape[1]))
        archive_f = np.zeros((0, F.shape[1]))
        xl, xu = problem.xl, problem.xu
        d = X.shape[1]
        while evaluated < self.evaluation_budget:
            n_cur = X.shape[0]
            off_x = []
            off_f = []
            s_cr = []
            s_f = []
            cr = np.clip(rng.normal(mu_cr, 0.1, size=n_cur), 0.0, 1.0)
            Fscale = rng.standard_cauchy(size=n_cur) * 0.1 + mu_f
            while np.any(Fscale <= 0):
                bad = Fscale <= 0
                Fscale[bad] = rng.standard_cauchy(size=int(bad.sum())) * 0.1 + mu_f
            Fscale = np.clip(Fscale, 0.0, 1.0)
            pool_x = X if archive_x.shape[0] == 0 else np.vstack([X, archive_x])
            for i in range(n_cur):
                pbest = _pbest(rng, X, front, crowd, self.p)
                i1 = int(rng.integers(0, n_cur))
                while i1 == i and n_cur > 1:
                    i1 = int(rng.integers(0, n_cur))
                i2 = int(rng.integers(0, pool_x.shape[0]))
                trial = X[i] + Fscale[i] * (pbest - X[i]) + Fscale[i] * (pool_x[i2] - X[i1])
                jrand = int(rng.integers(0, d))
                mask = rng.random(d) < cr[i]
                mask[jrand] = True
                child = np.where(mask, trial, X[i])
                child = np.clip(child, xl, xu)
                off_x.append(child)
            off_x = np.asarray(off_x)
            # MATLAB OptMPNDS3.m finishes the for-i=Population generation even if
            # INDIVIDUAL() overshoots Global.evaluation. GLOBAL.NotTermination
            # only stops at the *next* while-header and then saves that full
            # population. Truncating off_x to ``remaining`` here evaluates only
            # the first few parents, envsel-replaces the whole pop with that
            # tiny set, and collapses N=200 → O(10) on the last generation.
            off_eval = problem.evaluate(off_x)
            evaluated += off_x.shape[0]
            chosen_x = []
            chosen_f = []
            for i in range(off_eval.shape[0]):
                child_f = off_eval[i]
                if _mp_dominates(child_f, F[i], slices):
                    archive_x, archive_f = _update_archive(
                        archive_x, archive_f, X[i], F[i], 2 * n
                    )
                    chosen_x.append(off_x[i])
                    chosen_f.append(child_f)
                    s_cr.append(cr[i])
                    s_f.append(Fscale[i])
                elif _mp_dominates(F[i], child_f, slices):
                    archive_x, archive_f = _update_archive(
                        archive_x, archive_f, off_x[i], child_f, 2 * n
                    )
                    chosen_x.append(X[i])
                    chosen_f.append(F[i])
                else:
                    chosen_x.extend([off_x[i], X[i]])
                    chosen_f.extend([child_f, F[i]])
                    s_cr.append(cr[i])
                    s_f.append(Fscale[i])
            Cx = np.vstack(chosen_x)
            Cf = np.vstack(chosen_f)
            X, F, front, crowd = environmental_selection(
                Cx, Cf, n, mode="optmpnds3", slices=slices
            )
            if s_cr:
                mu_cr = (1 - self.c) * mu_cr + self.c * float(np.mean(s_cr))
            if s_f:
                arr = np.asarray(s_f)
                mu_f = (1 - self.c) * mu_f + self.c * float(np.sum(arr**2) / np.sum(arr))
        return X, F

"""Snapshot zm26 inside a copy of production OptMPNDS3.run (diagnostic; no production edit)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms.optmpnds3 import OptMPNDS3, _mp_dominates, _pbest, _party_nsga2, _update_archive
from experiments.zm26_reproduction.algorithms.operators import environmental_selection, random_population
from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import quality_row
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import PYTHON_OUT
from experiments.zm26_reproduction.runners.problem_setup import load_problem


def run_logged(name: str, seed: int) -> pd.DataFrame:
    problem, _, slices = load_problem(name)
    rng = np.random.default_rng(seed)
    algo = OptMPNDS3()
    n = algo.population_size
    evaluated = 0
    parts_x, parts_f = [], []
    for i in range(min(2, len(slices))):
        budget = min(evaluated + algo.fei, algo.evaluation_budget)
        Xi, Fi = _party_nsga2(problem, rng, slices[i], 100, budget - evaluated, problem.xl, problem.xu)
        evaluated += min(algo.fei, algo.evaluation_budget - evaluated)
        parts_x.append(Xi)
        parts_f.append(Fi)
    X = np.vstack(parts_x)
    F = np.vstack(parts_f)
    X, F, front, crowd = environmental_selection(X, F, X.shape[0], mode="optmpnds3", slices=slices)
    rows = []
    snap_at = {evaluated, 25000, 40000, 60000, algo.evaluation_budget}
    def snap(tag):
        q = quality_row(name, X, F, tag=tag)
        q.update({"seed": seed, "evaluated": evaluated, "n": int(X.shape[0])})
        rows.append(q)
        print(f"  {name} seed={seed} eval={evaluated} n={X.shape[0]} zm26={q['zm26_meanIGD']:.4g} dist={q['mean_dist_to_common_ps']:.3g}")
    snap("after_pft")
    mu_cr, mu_f = 0.5, 0.5
    archive_x = np.zeros((0, X.shape[1]))
    archive_f = np.zeros((0, F.shape[1]))
    xl, xu = problem.xl, problem.xu
    d = X.shape[1]
    next_snap = 25000
    while evaluated < algo.evaluation_budget:
        n_cur = X.shape[0]
        cr = np.clip(rng.normal(mu_cr, 0.1, size=n_cur), 0.0, 1.0)
        Fscale = rng.standard_cauchy(size=n_cur) * 0.1 + mu_f
        while np.any(Fscale <= 0):
            bad = Fscale <= 0
            Fscale[bad] = rng.standard_cauchy(size=int(bad.sum())) * 0.1 + mu_f
        Fscale = np.clip(Fscale, 0.0, 1.0)
        pool_x = X if archive_x.shape[0] == 0 else np.vstack([X, archive_x])
        off_x = []
        for i in range(n_cur):
            pbest = _pbest(rng, X, front, crowd, algo.p)
            i1 = int(rng.integers(0, n_cur))
            while i1 == i and n_cur > 1:
                i1 = int(rng.integers(0, n_cur))
            i2 = int(rng.integers(0, pool_x.shape[0]))
            trial = X[i] + Fscale[i] * (pbest - X[i]) + Fscale[i] * (pool_x[i2] - X[i1])
            jrand = int(rng.integers(0, d))
            mask = rng.random(d) < cr[i]
            mask[jrand] = True
            child = np.where(mask, trial, X[i])
            off_x.append(np.clip(child, xl, xu))
        off_x = np.asarray(off_x)
        remaining = algo.evaluation_budget - evaluated
        if off_x.shape[0] > remaining:
            off_x = off_x[:remaining]
        off_eval = problem.evaluate(off_x)
        evaluated += off_x.shape[0]
        chosen_x, chosen_f, s_cr, s_f = [], [], [], []
        for i in range(off_eval.shape[0]):
            child_f = off_eval[i]
            if _mp_dominates(child_f, F[i], slices):
                archive_x, archive_f = _update_archive(archive_x, archive_f, X[i], F[i], 2 * n)
                chosen_x.append(off_x[i]); chosen_f.append(child_f)
                s_cr.append(cr[i]); s_f.append(Fscale[i])
            elif _mp_dominates(F[i], child_f, slices):
                archive_x, archive_f = _update_archive(archive_x, archive_f, off_x[i], child_f, 2 * n)
                chosen_x.append(X[i]); chosen_f.append(F[i])
            else:
                chosen_x.extend([off_x[i], X[i]]); chosen_f.extend([child_f, F[i]])
                s_cr.append(cr[i]); s_f.append(Fscale[i])
        Cx, Cf = np.vstack(chosen_x), np.vstack(chosen_f)
        X, F, front, crowd = environmental_selection(Cx, Cf, n, mode="optmpnds3", slices=slices)
        if s_cr:
            mu_cr = (1 - algo.c) * mu_cr + algo.c * float(np.mean(s_cr))
        if s_f:
            arr = np.asarray(s_f)
            mu_f = (1 - algo.c) * mu_f + algo.c * float(np.sum(arr**2) / np.sum(arr))
        if evaluated >= next_snap or evaluated >= algo.evaluation_budget:
            snap(f"eval_{evaluated}")
            next_snap += 20000
    return pd.DataFrame(rows)


def run() -> None:
    parts = [run_logged("MPDMP1", 1), run_logged("MPDMP1", 2)]
    save_table(PYTHON_OUT / "test_11_production_snapshots.csv", pd.concat(parts, ignore_index=True))
    print("python test_11 done")


if __name__ == "__main__":
    run()

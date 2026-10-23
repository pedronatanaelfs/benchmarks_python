"""Shared diagnostic helpers. Not production code."""

from __future__ import annotations

import numpy as np

from experiments.zm26_reproduction.algorithms.operators import environmental_selection
from experiments.zm26_reproduction.metrics.matlab_mpdmp_pf import matlab_problem_pf
from experiments.zm26_reproduction.metrics.mean_igd import mean_igd
from experiments.zm26_reproduction.metrics.she_igd import zm26_meanIGD
from experiments.zm26_reproduction.runners.problem_setup import load_problem, reference_fronts

COMMON_PS = {
    "MPDMP1": np.array([50.0, 50.0]),
    "MPDMP4": np.array([50.0, 40.0]),
}


def quality_row(name: str, X: np.ndarray, F: np.ndarray, tag: str = "") -> dict:
    problem, _, slices = load_problem(name)
    ps = COMMON_PS[name]
    pf = matlab_problem_pf(problem)
    party = reference_fronts(problem, n_points=2000)
    uniq = np.unique(np.round(F, 12), axis=0).shape[0]
    dist = np.sqrt(((X - ps) ** 2).sum(axis=1))
    return {
        "benchmark": name,
        "tag": tag,
        "n": int(X.shape[0]),
        "n_unique_F": int(uniq),
        "zm26_meanIGD": float(zm26_meanIGD(F, pf, slices)),
        "party_pf_meanIGD": float(mean_igd(F, party, slices)),
        "mean_dist_to_common_ps": float(dist.mean()),
        "min_dist_to_common_ps": float(dist.min()),
        "median_dist_to_common_ps": float(np.median(dist)),
        "pop_mean_x1": float(X[:, 0].mean()),
        "pop_mean_x2": float(X[:, 1].mean()),
        "pop_std_x1": float(X[:, 0].std(ddof=0)),
        "pop_std_x2": float(X[:, 1].std(ddof=0)),
        "frac_within_2_of_ps": float(np.mean(dist < 2.0)),
        "frac_within_5_of_ps": float(np.mean(dist < 5.0)),
    }


def matlab_get_best_index(front: np.ndarray, crowd: np.ndarray, k: int) -> int:
    """Faithful getBestIndividual.m given 1-based k = randi(ceil(N*0.05))."""
    front = np.asarray(front, dtype=float)
    crowd = np.asarray(crowd, dtype=float)
    index = 0
    count = 0
    guard = int(np.nanmax(front[np.isfinite(front)])) + 5 if np.any(np.isfinite(front)) else 2
    while count < k:
        index += 1
        count += int(np.sum(front == index))
        if index > max(guard, 10000):
            raise RuntimeError("MATLAB front walk failed")
    count_before = int(np.sum(front < index))
    last = np.where(front == index)[0]
    rank = np.argsort(-crowd[last], kind="mergesort")
    pos = k - count_before
    return int(last[rank[pos - 1]])


def python_pbest_index(front: np.ndarray, crowd: np.ndarray, k: int) -> int:
    order = np.lexsort((-np.asarray(crowd), np.asarray(front)))
    return int(order[k - 1])


def envsel_optmpnds3(X, F, n, slices):
    return environmental_selection(X, F, n, mode="optmpnds3", slices=slices)

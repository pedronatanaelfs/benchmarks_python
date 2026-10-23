"""PlatEMO / OptMPNDS / OptMPNDS3 variation and selection operators.

Source mapping
--------------
NDSort                 OptMPNDS-master/Public/NDSort.m  (ENS-SS pairwise equivalent)
CrowdingDistance       Algorithms/*/CrowdingDistance.m
CrowdingEntropy        2022SheOptMPNDS3/Public/CrowdingEntropy.m
TournamentSelection    Public/TournamentSelection.m
GA (SBX + PM)          Public/GA.m
MPNDS                  Public/MPNDS.m (She cell-DM form)
PLNDS                  Public/PLNDS.m
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


def nd_sort(F: np.ndarray, n_sort: int | None = None) -> tuple[np.ndarray, int]:
    """Fast non-dominated sort. Returns 1-based front numbers (inf = unsorted)."""
    F = np.asarray(F, dtype=float)
    n = F.shape[0]
    if n == 0:
        return np.array([], dtype=float), 0
    if n_sort is None:
        n_sort = n
    n_sort = min(int(n_sort), n)

    _, unique_inv = np.unique(F, axis=0, return_inverse=True)
    Fu = np.unique(F, axis=0)
    nu = Fu.shape[0]
    table = np.bincount(unique_inv, minlength=nu)

    le = np.all(Fu[:, None, :] <= Fu[None, :, :], axis=2)
    lt = np.any(Fu[:, None, :] < Fu[None, :, :], axis=2)
    dominates = le & lt
    np.fill_diagonal(dominates, False)

    front_u = np.full(nu, np.inf)
    assigned = 0
    max_fno = 0
    remaining = np.ones(nu, dtype=bool)
    # MATLAB NDSort.m ENS_SS:
    #   while sum(Table(FrontNo<inf)) < min(nSort,length(Loc))
    # length(Loc) is the number of original rows (n). assigned already
    # counts original rows via Table, so the unique-count cap was wrong.
    while assigned < n_sort and remaining.any():
        max_fno += 1
        n_dom = dominates[:, remaining].sum(axis=0) if remaining.any() else 0
        cand = np.zeros(nu, dtype=bool)
        cand[remaining] = n_dom == 0
        if not cand.any():
            cand[remaining] = True
        front_u[cand] = max_fno
        remaining[cand] = False
        assigned = int(table[front_u < np.inf].sum())
        dominates[cand, :] = False

    front = front_u[unique_inv]
    return front, max_fno


def crowding_distance(F: np.ndarray, front_no: np.ndarray) -> np.ndarray:
    F = np.asarray(F, dtype=float)
    n, m = F.shape
    crowd = np.zeros(n, dtype=float)
    fronts = np.unique(front_no[np.isfinite(front_no)])
    for fno in fronts:
        idx = np.where(front_no == fno)[0]
        if idx.size == 0:
            continue
        fmax = F[idx].max(axis=0)
        fmin = F[idx].min(axis=0)
        span = np.where(fmax - fmin < 1e-16, 1.0, fmax - fmin)
        for j in range(m):
            order = idx[np.argsort(F[idx, j], kind="mergesort")]
            crowd[order[0]] = np.inf
            crowd[order[-1]] = np.inf
            if order.size <= 2:
                continue
            crowd[order[1:-1]] += (F[order[2:], j] - F[order[:-2], j]) / span[j]
    return crowd


def crowding_entropy(F: np.ndarray, front_no: np.ndarray) -> np.ndarray:
    """She OptMPNDS3 CrowdingEntropy.m, including MATLAB NaN/Inf edge cases.

    Original (Public/CrowdingEntropy.m) divides by ``c`` and
    ``(Fmax-Fmin)`` with no guards, so ``0/0``, ``log2(0)`` and Inf+NaN
    propagate. Reproduction must keep those IEEE results.
    """
    F = np.asarray(F, dtype=float)
    n, m = F.shape
    crowd = np.zeros(n, dtype=float)
    fronts = np.unique(front_no[np.isfinite(front_no)])
    with np.errstate(divide="ignore", invalid="ignore"):
        for fno in fronts:
            idx = np.where(front_no == fno)[0]
            if idx.size == 0:
                continue
            fmax = F[idx].max(axis=0)
            fmin = F[idx].min(axis=0)
            for j in range(m):
                order = idx[np.argsort(F[idx, j], kind="mergesort")]
                crowd[order[0]] = np.inf
                crowd[order[-1]] = np.inf
                if order.size <= 2:
                    continue
                c = F[order[2:], j] - F[order[:-2], j]
                dl = F[order[2:], j] - F[order[1:-1], j]
                du = F[order[1:-1], j] - F[order[:-2], j]
                pl = dl / c
                pu = du / c
                ce = -(dl * np.log2(pl) + du * np.log2(pu)) / (fmax[j] - fmin[j])
                crowd[order[1:-1]] += ce
    return crowd


def tournament_selection(
    rng: np.random.Generator, k: int, n: int, *fitness: np.ndarray
) -> np.ndarray:
    """PlatEMO TournamentSelection: smaller fitness is better."""
    stacked = np.column_stack([np.asarray(f).reshape(-1) for f in fitness])
    order = np.lexsort(stacked.T[::-1])
    rank = np.empty(stacked.shape[0], dtype=int)
    rank[order] = np.arange(stacked.shape[0])
    pop = stacked.shape[0]
    parents = rng.integers(0, pop, size=(k, n))
    best = np.argmin(rank[parents], axis=0)
    return parents[best, np.arange(n)]


def sbx_pm(
    rng: np.random.Generator,
    parents: np.ndarray,
    xl: np.ndarray,
    xu: np.ndarray,
    *,
    pro_c: float = 1.0,
    dis_c: float = 20.0,
    pro_m: float = 1.0,
    dis_m: float = 20.0,
    mutation_as_expectation: bool = True,
) -> np.ndarray:
    """PlatEMO GA.m real encoding: SBX + polynomial mutation.

    ``pro_m`` is the expected number of mutated variables when
    ``mutation_as_expectation`` is True. MATLAB ``Public/GA.m`` real
    encoding (line ``Site = rand(2*N,D) < proM/D``) always uses
    probability ``proM/D``. Production MPDMP must keep that rule
    (``pro_m=0.5``, D=2 ⇒ 0.25), not a per-variable probability of 0.5.
    """
    n_all, d = parents.shape
    n = n_all // 2
    p1 = parents[:n]
    p2 = parents[n : 2 * n]
    mu = rng.random((n, d))
    beta = np.empty((n, d))
    mask = mu <= 0.5
    beta[mask] = (2.0 * mu[mask]) ** (1.0 / (dis_c + 1.0))
    beta[~mask] = (2.0 - 2.0 * mu[~mask]) ** (-2.0 / (dis_c + 1.0))
    beta *= (-1.0) ** rng.integers(0, 2, size=(n, d))
    beta[rng.random((n, d)) < 0.5] = 1.0
    beta[rng.random(n) > pro_c, :] = 1.0
    off = np.vstack(
        [
            0.5 * (p1 + p2) + 0.5 * beta * (p1 - p2),
            0.5 * (p1 + p2) - 0.5 * beta * (p1 - p2),
        ]
    )
    off = np.clip(off, xl, xu)
    rate = (pro_m / d) if mutation_as_expectation else pro_m
    site = rng.random(off.shape) < rate
    mu = rng.random(off.shape)
    span = xu - xl
    temp = site & (mu <= 0.5)
    delta1 = (off - xl) / np.where(span == 0, 1.0, span)
    delta2 = (xu - off) / np.where(span == 0, 1.0, span)
    off[temp] = off[temp] + span[np.newaxis, :].repeat(off.shape[0], 0)[temp] * (
        (
            2.0 * mu[temp]
            + (1.0 - 2.0 * mu[temp]) * (1.0 - delta1[temp]) ** (dis_m + 1.0)
        )
        ** (1.0 / (dis_m + 1.0))
        - 1.0
    )
    temp = site & (mu > 0.5)
    off[temp] = off[temp] + span[np.newaxis, :].repeat(off.shape[0], 0)[temp] * (
        1.0
        - (
            2.0 * (1.0 - mu[temp])
            + 2.0 * (mu[temp] - 0.5) * (1.0 - delta2[temp]) ** (dis_m + 1.0)
        )
        ** (1.0 / (dis_m + 1.0))
    )
    return np.clip(off, xl, xu)


def mpnds(F: np.ndarray, slices: Sequence[slice], n_sort: int) -> tuple[np.ndarray, int]:
    """She MPNDS.m using actual per-DM objective slices."""
    F = np.asarray(F, dtype=float)
    n = F.shape[0]
    if n == 0:
        return np.array([], dtype=float), 0
    _, loc = np.unique(F, axis=0, return_inverse=True)
    Fu = np.unique(F, axis=0)
    nu = Fu.shape[0]
    table = np.bincount(loc, minlength=nu)
    party_num = len(slices)
    party_fronts = np.vstack([nd_sort(Fu[:, sl], nu)[0] for sl in slices])
    front_no = np.full(nu, np.inf)
    front_no_max = party_fronts.max(axis=0)
    max_fno = 1
    fno = 1
    visited = np.zeros(nu, dtype=bool)
    s = np.zeros(nu, dtype=bool)
    n_sort = min(int(n_sort), n)
    # MATLAB MPNDS_Sort: while sum(Table(FrontNo<inf)) < min(nSort,length(Loc))
    # Loc is the inverse index of the original matrix, so length(Loc)=n.
    while table[front_no < np.inf].sum() < n_sort:
        fz = np.ones(nu, dtype=bool)
        for k in range(party_num):
            fz &= (party_fronts[k] == fno) & (~visited)
        if not fz.any():
            for k in range(party_num):
                s |= (party_fronts[k] == fno) & (~visited)
            fno += 1
            fz = s & (front_no_max == fno)
            s[fz] = False
        if fz.any():
            front_no[fz] = max_fno
            visited[fz] = True
            max_fno += 1
        elif fno > int(np.nanmax(party_fronts[np.isfinite(party_fronts)])) + 2:
            break
    return front_no[loc], max_fno - 1


def plnds(F: np.ndarray, slices: Sequence[slice], n_sort: int) -> tuple[np.ndarray, int]:
    """PLNDS.m: party-wise ranks become objectives of a second NDSort."""
    F = np.asarray(F, dtype=float)
    n = F.shape[0]
    if n == 0:
        return np.array([], dtype=float), 0
    ranks = np.column_stack([nd_sort(F[:, sl], n)[0] for sl in slices])
    return nd_sort(ranks, n_sort)


def environmental_selection(
    X: np.ndarray,
    F: np.ndarray,
    n_survive: int,
    *,
    mode: str,
    slices: Sequence[slice],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return surviving X, F, front numbers, crowding values."""
    if mode == "optall":
        front, max_fno = nd_sort(F, n_survive)
        crowd = crowding_distance(F, front)
    elif mode == "optmpnds":
        front, max_fno = mpnds(F, slices, n_survive)
        crowd = crowding_distance(F, front)
    elif mode == "optmpnds2":
        front, max_fno = plnds(F, slices, n_survive)
        crowd = crowding_distance(F, front)
    elif mode == "optmpnds3":
        uniq, loc = np.unique(F, axis=0, return_index=True)
        X, F = X[loc], F[loc]
        front, max_fno = plnds(F, slices, n_survive)
        next_mask = front < max_fno
        last = np.where(front == max_fno)[0].tolist()
        while len(last) > max(n_survive - int(next_mask.sum()), 0):
            ce = crowding_entropy(F[last], np.ones(len(last)))
            last.pop(int(np.argmin(ce)))
        next_mask = next_mask.copy()
        next_mask[last] = True
        crowd = crowding_entropy(F[next_mask], front[next_mask])
        return X[next_mask], F[next_mask], front[next_mask], crowd
    else:
        raise ValueError(mode)

    next_mask = front < max_fno
    last = np.where(front == max_fno)[0]
    n_fill = n_survive - int(next_mask.sum())
    if n_fill > 0 and last.size:
        order = np.argsort(-crowd[last], kind="mergesort")
        next_mask[last[order[:n_fill]]] = True
    elif n_fill < 0:
        keep = np.where(next_mask)[0]
        order = np.argsort(-crowd[keep], kind="mergesort")
        mask = np.zeros_like(next_mask)
        mask[keep[order[:n_survive]]] = True
        next_mask = mask
    return X[next_mask], F[next_mask], front[next_mask], crowd[next_mask]


def random_population(
    rng: np.random.Generator, n: int, xl: np.ndarray, xu: np.ndarray
) -> np.ndarray:
    return rng.uniform(xl, xu, size=(n, xl.size))

from __future__ import annotations

import numpy as np

from fairmoo_benchmarks import get_problem



def load_problem(name: str):
    family = "MPMOP" if name.startswith("MPMOP") else "MPDMP"
    if family == "MPMOP":
        idx = int(name.replace("MPMOP", ""))
        # ZM26 Table II caption: D=2 for MPMOP1–11. MPMOP12–17 keep MATLAB D=10.
        kwargs = {"n_var": 2} if idx <= 11 else {}
        problem = get_problem(name, **kwargs)
    else:
        problem = get_problem(name)
    slices = [problem.dm_objective_slices[i] for i in range(problem.n_dm)]
    return problem, family, slices


def _mpmop4_common_ps(problem, n_div: int = 1000) -> np.ndarray:
    """Common PS of MPMOP4/9: sin(2π(x1+x2))=0, i.e. x1+x2 ∈ {0, 0.5, 1, 1.5, 2}.

    MATLAB ``true_PS.m`` uses meshgrid(linspace(0,1,20000)) which is unsafe
    (documented PARTIAL validation). The matching condition is
    ``abs(sin(2π(x1+x2))/(1+|G_i|) − sin(2π(x1+x2))/(1+|G_j|)) < 1e-4``,
    which holds when sin(2π(x1+x2))≈0. Sampling the diagonals is the same
    manifold at the experimental D, without changing objective equations.
    """
    n_line = max(n_div, 200)
    xs = []
    ys = []
    grid = np.linspace(0.0, 1.0, n_line)
    for s in (0.0, 0.5, 1.0, 1.5, 2.0):
        x1 = grid
        x2 = s - x1
        keep = (x2 >= 0.0) & (x2 <= 1.0)
        xs.append(x1[keep])
        ys.append(x2[keep])
    x1 = np.concatenate(xs)
    x2 = np.concatenate(ys)
    X = np.zeros((x1.size, problem.n_var))
    X[:, 0] = x1
    if problem.n_var > 1:
        X[:, 1] = x2
    if problem.n_var > 2:
        t = np.asarray(problem.times, dtype=float)
        G2 = np.sin(0.5 * np.pi * t[min(1, t.size - 1)])
        xi = np.sin(2.0 * np.pi * (x1 + x2)) / (1.0 + abs(G2))
        X[:, 2:] = xi[:, None]
    return X


def _fallback_ps(problem, n_points: int) -> np.ndarray | None:
    ps = problem.get_pareto_set(dm=None, n_points=n_points)
    if ps is not None and getattr(ps, "size", 0):
        return np.atleast_2d(ps)
    if getattr(problem, "value_id", None) == "MPMOP4":
        return _mpmop4_common_ps(problem, n_div=max(n_points, 800))
    return None


def reference_fronts(problem, n_points: int = 2000) -> list:
    """Party-wise PF. Uses public API, then common-PS fallback, then MPMOP4 manifold."""
    fronts = []
    common_ps = None
    for dm in range(problem.n_dm):
        pf = problem.get_pareto_front(dm=dm, n_points=n_points)
        if pf is None or pf.size == 0:
            ps = problem.get_pareto_set(dm=dm, n_points=n_points)
            if ps is None or ps.size == 0:
                if common_ps is None:
                    common_ps = _fallback_ps(problem, n_points)
                ps = common_ps
            if ps is None or ps.size == 0:
                raise RuntimeError(f"{problem.name}: missing PF for DM{dm+1}")
            pf = problem.evaluate_dm(np.atleast_2d(ps), dm)
        fronts.append(np.atleast_2d(pf))
    return fronts

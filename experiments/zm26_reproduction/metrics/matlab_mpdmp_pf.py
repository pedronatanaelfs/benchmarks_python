"""MATLAB ``problem.PF()`` for MPDMP1–12, reconstructed in the reproduction layer.

Does not modify ``src/fairmoo_benchmarks``. Each branch follows the She
classdef / map ``PF`` method listed in ``MPDMP_IGD_REFERENCE_AUDIT.md``.
"""

from __future__ import annotations

import numpy as np


def matlab_problem_pf(problem, n_grid: int = 1000) -> np.ndarray:
    """Return the concatenated objective PF used by She ``GLOBAL.Metric(@IGD, ...)``.

    MPDMP1 overrides ``PF`` analytically. MPDMP4/9/10 evaluate a single
    common-PS point. Polygon maps evaluate the common-PS grid (or the
    explicit MPDMP6 edge).
    """
    name = getattr(problem, "name", None) or getattr(problem, "value_id", None)
    if name == "MPDMP1":
        v = 20.0 * np.sqrt(2.0)
        return np.array([[v, v, v, v]], dtype=float)

    ps = None
    if name == "MPDMP6":
        # MPDMP6.m: x=50, y=linspace(40,60,10000)
        ps = np.column_stack([np.full(10000, 50.0), np.linspace(40.0, 60.0, 10000)])
    elif hasattr(problem, "get_pareto_set"):
        ps = problem.get_pareto_set(dm=None, n_points=max(n_grid, 1000))

    if ps is None or np.size(ps) == 0:
        raise RuntimeError(f"{name}: no MATLAB-equivalent PS for PF()")
    ps = np.atleast_2d(np.asarray(ps, dtype=float))
    return np.atleast_2d(problem.evaluate(ps))

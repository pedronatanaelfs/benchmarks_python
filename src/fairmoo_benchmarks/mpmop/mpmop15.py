"""MPMOP15 — ZM26 Appendix Table S-VI."""

from __future__ import annotations

from typing import Optional

import numpy as np

from fairmoo_benchmarks.mpmop.zm26_base import ZM26MPMOP


class MPMOP15(ZM26MPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl = np.zeros(n_var)
        xu = np.ones(n_var)
        xl[0], xu[0] = 1.0, 4.0
        super().__init__(
            name="MPMOP15",
            n_obj_per_dm=[2, 2, 2],
            xl=xl,
            xu=xu,
            n_var=n_var,
            notes=(
                "Overall bounds: x1 in [1,4], xi in [0,1] (union of DM columns "
                "[1,2], [2,3], [3,4])."
            ),
        )

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        x1 = X[:, 0]
        g1 = 1.0 + np.sum((X[:, 1:] - 0.5) ** 2, axis=1)
        f11 = g1 * 2.0 / x1
        f12 = g1 * x1 / 2.0

        tmp = 1.0 / (1.0 + np.exp(-5.0 * (x1 - 2.5)))
        g2 = 1.0 + np.sum((X[:, 1:] - tmp[:, None]) ** 2, axis=1)
        f21 = g2 * 3.0 / x1
        f22 = g2 * x1 / 3.0

        g3 = 1.0 + np.sum((X[:, 1:] - 0.5) ** 2, axis=1)
        f31 = g3 * 4.0 / x1
        f32 = g3 * x1 / 4.0
        return np.column_stack([f11, f12, f21, f22, f31, f32])

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        n = int(n_points)
        X = np.zeros((n, self.n_var))
        if dm == 0:
            X[:, 0] = np.linspace(1.0, 2.0, n)
            X[:, 1:] = 0.5
            return X
        if dm == 1:
            X[:, 0] = np.linspace(2.0, 3.0, n)
            tmp = 1.0 / (1.0 + np.exp(-5.0 * (X[:, 0] - 2.5)))
            X[:, 1:] = tmp[:, None]
            return X
        if dm == 2:
            X[:, 0] = np.linspace(3.0, 4.0, n)
            X[:, 1:] = 0.5
            return X
        raise IndexError(dm)


__all__ = ["MPMOP15"]

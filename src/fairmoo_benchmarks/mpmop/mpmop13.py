"""MPMOP13 — port of 2026ZhaoNash ``MPMOP13.m``/``MPMOP_Value.m``."""

from __future__ import annotations

from typing import Optional

import numpy as np

from fairmoo_benchmarks.mpmop.zm26_base import ZM26MPMOP


class MPMOP13(ZM26MPMOP):
    def __init__(self, n_var: int = 10) -> None:
        super().__init__(
            name="MPMOP13",
            n_obj_per_dm=[2, 2],
            xl=np.zeros(n_var),
            xu=np.ones(n_var),
            n_var=n_var,
        )

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        x1 = X[:, 0]
        z = 0.2 + 0.6 * x1
        g1 = 1.0 + np.sum(X[:, 1:] ** 2, axis=1)
        g2 = 1.0 + np.sum((X[:, 1:] - 1.0) ** 2, axis=1)
        f11, f12 = g1 * z, g1 * (1.0 - z)
        f21, f22 = g2 * z, g2 * (1.0 - z)
        return np.column_stack([f11, f12, f21, f22])

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        n = int(n_points)
        X = np.zeros((n, self.n_var))
        if dm == 0:
            X[:, 0] = np.linspace(0.0, 1.0, n)
            return X
        if dm == 1:
            X[:, 0] = np.linspace(0.0, 1.0, n)
            X[:, 1:] = 1.0
            return X
        raise IndexError(dm)

    def get_pareto_front(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        if dm is not None:
            return super().get_pareto_front(dm=dm, n_points=n_points)
        X1 = self.get_pareto_set(dm=0, n_points=200)
        X2 = self.get_pareto_set(dm=1, n_points=200)
        assert X1 is not None and X2 is not None
        return np.column_stack([self.evaluate_dm(X1, 0), self.evaluate_dm(X2, 1)])


__all__ = ["MPMOP13"]

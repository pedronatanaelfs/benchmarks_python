"""MPMOP16 — port of 2026ZhaoNash ``MPMOP16.m``/``MPMOP_Value.m``."""

from __future__ import annotations

from typing import Optional

import numpy as np

from fairmoo_benchmarks.mpmop.zm26_base import ZM26MPMOP


class MPMOP16(ZM26MPMOP):
    def __init__(self, n_var: int = 10) -> None:
        super().__init__(
            name="MPMOP16",
            n_obj_per_dm=[2, 2],
            xl=np.zeros(n_var),
            xu=np.ones(n_var),
            n_var=n_var,
            notes="MATLAB party constants: DM1 c=0.25, DM2 c=0.75.",
        )

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        x1 = X[:, 0]
        g1 = 1.0 + np.sum((X[:, 1:] - 0.25) ** 2, axis=1)
        g2 = 1.0 + np.sum((X[:, 1:] - 0.75) ** 2, axis=1)
        return np.column_stack(
            [g1 * x1, g1 * (1.0 - x1), g2 * x1, g2 * (1.0 - x1)]
        )

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        n = int(n_points)
        X = np.zeros((n, self.n_var))
        if dm not in (0, 1):
            raise IndexError(dm)
        X[:, 0] = np.linspace(0.0, 1.0, n)
        X[:, 1:] = 0.25 + 0.5 * dm
        return X

    def get_pareto_front(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        if dm is not None:
            return super().get_pareto_front(dm=dm, n_points=n_points)
        X1 = self.get_pareto_set(dm=0, n_points=200)
        X2 = self.get_pareto_set(dm=1, n_points=200)
        assert X1 is not None and X2 is not None
        return np.column_stack([self.evaluate_dm(X1, 0), self.evaluate_dm(X2, 1)])


__all__ = ["MPMOP16"]

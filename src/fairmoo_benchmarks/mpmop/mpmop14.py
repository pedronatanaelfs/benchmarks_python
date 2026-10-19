"""MPMOP14 — port of 2026ZhaoNash ``MPMOP14.m``/``MPMOP_Value.m``."""

from __future__ import annotations

from typing import Optional

import numpy as np

from fairmoo_benchmarks.mpmop.zm26_base import ZM26MPMOP


class MPMOP14(ZM26MPMOP):
    def __init__(self, n_var: int = 10) -> None:
        if n_var < 3:
            raise ValueError("MPMOP14 requires n_var >= 3")
        super().__init__(
            name="MPMOP14",
            n_obj_per_dm=[3, 3],
            xl=np.zeros(n_var),
            xu=np.ones(n_var),
            n_var=n_var,
        )

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        x1, x2 = X[:, 0], X[:, 1]
        g1 = 1.0 + np.sum((X[:, 2:] - 1.0) ** 2, axis=1)
        g2 = 1.0 + np.sum(X[:, 2:] ** 2, axis=1)
        c1 = np.cos(0.5 * np.pi * x1)
        f11 = g1 * np.cos(0.5 * np.pi * x2) * c1
        f12 = g1 * np.sin(0.5 * np.pi * x2) * c1
        f13 = g1 * np.sin(0.5 * np.pi * x1)
        f21 = g2 * np.cos(0.5 * np.pi * x2) * c1
        f22 = g2 * np.sin(0.5 * np.pi * x2) * c1
        f23 = g2 * np.sin(0.5 * np.pi * x1)
        return np.column_stack([f11, f12, f13, f21, f22, f23])

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        n = max(int(np.sqrt(n_points)), 2)
        u = np.linspace(0.0, 1.0, n)
        X1, X2 = np.meshgrid(u, u)
        X = np.zeros((X1.size, self.n_var))
        X[:, 0] = X1.ravel(order="F")
        X[:, 1] = X2.ravel(order="F")
        if dm == 0:
            X[:, 2:] = 1.0
            return X
        if dm == 1:
            return X
        raise IndexError(dm)

    def get_pareto_front(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        if dm is not None:
            return super().get_pareto_front(dm=dm, n_points=n_points)
        # MATLAB PF() uses a fixed 40x40 mesh.
        X1 = self.get_pareto_set(dm=0, n_points=1600)
        X2 = self.get_pareto_set(dm=1, n_points=1600)
        assert X1 is not None and X2 is not None
        return np.column_stack([self.evaluate_dm(X1, 0), self.evaluate_dm(X2, 1)])


__all__ = ["MPMOP14"]

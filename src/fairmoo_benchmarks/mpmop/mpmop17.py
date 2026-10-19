"""MPMOP17 — port of 2026ZhaoNash ``MPMOP17.m``/``MPMOP_Value.m``."""

from __future__ import annotations

from typing import Optional

import numpy as np

from fairmoo_benchmarks.mpmop.zm26_base import ZM26MPMOP


class MPMOP17(ZM26MPMOP):
    def __init__(self, n_var: int = 10) -> None:
        super().__init__(
            name="MPMOP17",
            n_obj_per_dm=[2, 2, 2],
            xl=np.zeros(n_var),
            xu=np.ones(n_var),
            n_var=n_var,
            notes="MATLAB party constants: c=0, 0.5, 1.",
        )

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        x1 = X[:, 0]
        blocks = []
        for c in (0.0, 0.5, 1.0):
            g = 1.0 + np.sum((X[:, 1:] - c) ** 2, axis=1)
            blocks.extend([g * x1, g * (1.0 - x1)])
        return np.column_stack(blocks)

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        if dm not in (0, 1, 2):
            raise IndexError(dm)
        X = np.zeros((int(n_points), self.n_var))
        X[:, 0] = np.linspace(0.0, 1.0, int(n_points))
        X[:, 1:] = 0.5 * dm
        return X

    def get_pareto_front(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        if dm is not None:
            return super().get_pareto_front(dm=dm, n_points=n_points)
        blocks = []
        for party in range(3):
            X = self.get_pareto_set(dm=party, n_points=200)
            assert X is not None
            blocks.append(self.evaluate_dm(X, party))
        return np.column_stack(blocks)


__all__ = ["MPMOP17"]

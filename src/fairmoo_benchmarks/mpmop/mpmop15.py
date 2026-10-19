"""MPMOP15 — MATLAB class behavior (an intentional duplicate of MPMOP17)."""

from __future__ import annotations

from typing import Optional

import numpy as np

from fairmoo_benchmarks.mpmop.zm26_base import ZM26MPMOP


class MPMOP15(ZM26MPMOP):
    def __init__(self, n_var: int = 10) -> None:
        super().__init__(
            name="MPMOP15",
            n_obj_per_dm=[2, 2, 2],
            xl=np.zeros(n_var),
            xu=np.ones(n_var),
            n_var=n_var,
            notes=(
                "The MATLAB MPMOP15 class calls the MPMOP17 value kernel at "
                "t=0,0.5,1; it is objective-equivalent to MATLAB MPMOP17."
            ),
        )

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        x1 = X[:, 0]
        g1 = 1.0 + np.sum(X[:, 1:] ** 2, axis=1)
        g2 = 1.0 + np.sum((X[:, 1:] - 0.5) ** 2, axis=1)
        g3 = 1.0 + np.sum((X[:, 1:] - 1.0) ** 2, axis=1)
        f11, f12 = g1 * x1, g1 * (1.0 - x1)
        f21, f22 = g2 * x1, g2 * (1.0 - x1)
        f31, f32 = g3 * x1, g3 * (1.0 - x1)
        return np.column_stack([f11, f12, f21, f22, f31, f32])

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        n = int(n_points)
        X = np.zeros((n, self.n_var))
        if dm not in (0, 1, 2):
            raise IndexError(dm)
        X[:, 0] = np.linspace(0.0, 1.0, n)
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


__all__ = ["MPMOP15"]

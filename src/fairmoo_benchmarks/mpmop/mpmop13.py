"""MPMOP13 — ZM26 Appendix Table S-VI."""

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
        tmp = np.sin(4.0 * np.pi * x1) / 2.0
        g1 = 1.0 + np.sum((X[:, 1:] - tmp[:, None]) ** 2, axis=1) + 100.0 * np.maximum(0.0, x1 - 0.5) ** 2
        s = 0.1 * np.sin(3.0 * np.pi * x1)
        f11 = g1 * (x1 + s)
        f12 = g1 * (1.0 - x1 + s) ** 4.25

        g2 = 1.0 + np.sum(X[:, 1:] ** 2, axis=1) + 100.0 * np.maximum(0.0, 0.5 - x1) ** 2
        f21 = g2 * (x1 + s)
        f22 = g2 * (1.0 - x1 + s) ** 4.25
        return np.column_stack([f11, f12, f21, f22])

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        n = int(n_points)
        X = np.zeros((n, self.n_var))
        if dm == 0:
            # Table: x1 in [0, 0.5)
            X[:, 0] = np.linspace(0.0, 0.5, n, endpoint=False)
            tmp = np.sin(4.0 * np.pi * X[:, 0]) / 2.0
            X[:, 1:] = tmp[:, None]
            return X
        if dm == 1:
            X[:, 0] = np.linspace(0.5, 1.0, n)
            X[:, 1:] = 0.0
            return X
        raise IndexError(dm)


__all__ = ["MPMOP13"]

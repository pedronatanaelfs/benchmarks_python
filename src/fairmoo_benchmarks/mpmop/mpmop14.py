"""MPMOP14 — ZM26 Appendix Table S-VI."""

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
        t1 = np.sin(2.0 * np.pi * (x1 + x2) + np.pi / 4.0) / 2.0
        g1 = 1.0 + np.sum((X[:, 2:] - t1[:, None]) ** 2, axis=1)
        f11 = g1 * np.sin(0.5 * np.pi * x1) ** 2
        f12 = g1 * (np.sin(0.5 * np.pi * x2) ** 2) * (np.cos(0.5 * np.pi * x1) ** 2)
        f13 = g1 * (np.cos(0.5 * np.pi * x2) ** 2) * (np.cos(0.5 * np.pi * x1) ** 2)

        t2 = np.sin(2.0 * np.pi * (x1 + x2) + np.pi / 2.0)
        g2 = 1.0 + np.sum((X[:, 2:] - t2[:, None]) ** 2, axis=1)
        f21 = g2 * np.sin(0.5 * np.pi * x1) ** 2
        f22 = g2 * (np.sin(0.5 * np.pi * x2) ** 2) * (np.cos(0.5 * np.pi * x1) ** 2)
        f23 = g2 * (np.cos(0.5 * np.pi * x2) ** 2) * (np.cos(0.5 * np.pi * x1) ** 2)
        return np.column_stack([f11, f12, f13, f21, f22, f23])

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        n = int(np.sqrt(n_points))
        n = max(n, 2)
        if dm == 0:
            x1 = np.linspace(0.0, 0.5, n)
            x2 = np.linspace(0.0, 1.0, n)
            X1, X2 = np.meshgrid(x1, x2, indexing="ij")
            X = np.zeros((X1.size, self.n_var))
            X[:, 0] = X1.ravel()
            X[:, 1] = X2.ravel()
            t = np.sin(2.0 * np.pi * (X[:, 0] + X[:, 1]) + np.pi / 4.0) / 2.0
            X[:, 2:] = t[:, None]
            return X
        if dm == 1:
            # Table: x1 in (0.5, 1]
            x1 = np.linspace(0.5, 1.0, n)
            x1 = x1[x1 > 0.5]
            if x1.size == 0:
                x1 = np.array([1.0])
            x2 = np.linspace(0.0, 1.0, n)
            X1, X2 = np.meshgrid(x1, x2, indexing="ij")
            X = np.zeros((X1.size, self.n_var))
            X[:, 0] = X1.ravel()
            X[:, 1] = X2.ravel()
            t = np.sin(2.0 * np.pi * (X[:, 0] + X[:, 1]) + np.pi / 2.0)
            X[:, 2:] = t[:, None]
            return X
        raise IndexError(dm)


__all__ = ["MPMOP14"]

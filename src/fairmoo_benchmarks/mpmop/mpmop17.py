"""MPMOP17 — ZM26 Appendix Table S-VI."""

from __future__ import annotations

from typing import Optional

import numpy as np

from fairmoo_benchmarks.mpmop.zm26_base import ZM26MPMOP


class MPMOP17(ZM26MPMOP):
    def __init__(self, n_var: int = 10) -> None:
        if n_var < 3:
            raise ValueError("MPMOP17 requires n_var >= 3")
        super().__init__(
            name="MPMOP17",
            n_obj_per_dm=[3, 3, 3],
            xl=np.zeros(n_var),
            xu=np.ones(n_var),
            n_var=n_var,
            notes="PS thresholds use 0.33/0.66 as written in Table S-VI (not 1/3, 2/3).",
        )

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        x1, x2 = X[:, 0], X[:, 1]

        g1 = 1.0 + np.sum((X[:, 2:] - 0.5 * x1[:, None]) ** 2, axis=1)
        y1 = np.pi / 6.0 + (np.pi / 3.0) * x1
        y2 = 0.5 * np.pi * x2
        f11 = g1 * np.sin(y1)
        f12 = g1 * np.sin(y2) * np.cos(y1)
        f13 = g1 * np.cos(y2) * np.cos(y1)

        g2 = 1.0 + np.sum(X[:, 2:] ** 2, axis=1)
        y1b = 0.5 * np.pi * x1
        y2b = 0.5 * np.pi * x2
        f21 = g2 * np.sin(y1b)
        f22 = g2 * np.sin(y2b) * np.cos(y1b)
        f23 = g2 * np.cos(y2b) * np.cos(y1b)

        g3 = 1.0 + np.sum((X[:, 2:] - 0.5 * x1[:, None]) ** 2, axis=1)
        y1c = np.pi / 6.0 + (np.pi / 3.0) * x1
        y2c = 0.5 * np.pi * x2
        f31 = g3 * np.sin(y1c)
        f32 = g3 * np.sin(y2c) * np.cos(y1c)
        f33 = g3 * np.cos(y2c) * np.cos(y1c)
        return np.column_stack([f11, f12, f13, f21, f22, f23, f31, f32, f33])

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        if dm is None:
            return np.zeros((0, self.n_var), dtype=float)
        n = int(np.sqrt(n_points))
        n = max(n, 2)
        x2 = np.linspace(0.0, 1.0, n)
        if dm == 0:
            x1 = np.linspace(0.0, 0.33, n, endpoint=False)
        elif dm == 1:
            x1 = np.linspace(0.33, 0.66, n, endpoint=False)
        elif dm == 2:
            x1 = np.linspace(0.66, 1.0, n)
        else:
            raise IndexError(dm)
        X1, X2 = np.meshgrid(x1, x2, indexing="ij")
        X = np.zeros((X1.size, self.n_var))
        X[:, 0] = X1.ravel()
        X[:, 1] = X2.ravel()
        if dm in (0, 2):
            X[:, 2:] = 0.5 * X[:, 0:1]
        else:
            X[:, 2:] = 0.0
        return X


__all__ = ["MPMOP17"]

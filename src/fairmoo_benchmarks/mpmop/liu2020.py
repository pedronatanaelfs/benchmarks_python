"""MPMOP1–MPMOP11 from Liu et al. CEC 2020 / OptMPNDS official MATLAB."""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from fairmoo_benchmarks.base import MultiPartyProblem
from fairmoo_benchmarks.status import CommonPSStatus

LIU2020_SOURCE = (
    "Liu, Luo, Lin, Li, Yang (2020). Evolutionary Approach to Multiparty "
    "Multiobjective Optimization Problems with Common Pareto Optimal Solutions. "
    "IEEE CEC 2020. Official code: https://github.com/lwjie595/OptMPNDS "
    "(Problems/MPMOP/MPMOP_Value.m)."
)


def mpmop_value(prob_id: str, X: np.ndarray, t: float) -> np.ndarray:
    """Vectorized port of MATLAB ``MPMOP_Value(probID, x, t)``."""
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(1, -1)
    n = X.shape[1]

    if prob_id == "MPMOP1":
        a = 5.0 * np.cos(0.5 * np.pi * t)
        tmp = 1.0 / (1.0 + np.exp(a * (X[:, 0] - 2.5)))
        g = 1.0 + np.sum((X[:, 1:] - tmp[:, None]) ** 2, axis=1)
        f1 = g * (1.0 + t) / X[:, 0]
        f2 = g * X[:, 0] / (1.0 + t)
        return np.column_stack([f1, f2])

    if prob_id == "MPMOP2":
        G = np.sin(0.5 * np.pi * t)
        a = 2.25 + 2.0 * np.cos(2.0 * np.pi * t)
        tmp = G * np.sin(4.0 * np.pi * X[:, 0]) / (1.0 + abs(G))
        g = 1.0 + np.sum((X[:, 1:] - tmp[:, None]) ** 2, axis=1)
        f1 = g * (X[:, 0] + 0.1 * np.sin(3.0 * np.pi * X[:, 0]))
        f2 = g * (1.0 - X[:, 0] + 0.1 * np.sin(3.0 * np.pi * X[:, 0])) ** a
        return np.column_stack([f1, f2])

    if prob_id == "MPMOP3":
        N = 1 + int(np.floor(10.0 * abs(np.sin(0.5 * np.pi * t))))
        g = np.ones(X.shape[0])
        for i in range(1, n):
            tmp = X[:, i] - np.cos(4.0 * t + X[:, 0] + X[:, i - 1])
            g = g + tmp**2
        bump = np.maximum(0.0, (0.1 + 0.5 / N) * np.sin(2.0 * N * np.pi * X[:, 0]))
        f1 = g * (X[:, 0] + bump)
        f2 = g * (1.0 - X[:, 0] + bump)
        return np.column_stack([f1, f2])

    if prob_id == "MPMOP4":
        G = np.sin(0.5 * np.pi * t)
        H = 2.25 + 2.0 * np.cos(0.5 * np.pi * t)
        # MATLAB: tmp=sin(2*pi*(x(:,1)+x(:,2)))/(1+abs(G));  (scalar / — ok)
        tmp = np.sin(2.0 * np.pi * (X[:, 0] + X[:, 1])) / (1.0 + abs(G))
        g = 1.0 + np.sum((X[:, 2:] - tmp[:, None]) ** 2, axis=1)
        f1 = g * np.sin(0.5 * np.pi * X[:, 0]) ** H
        f2 = g * (np.sin(0.5 * np.pi * X[:, 1]) ** H) * (np.cos(0.5 * np.pi * X[:, 0]) ** H)
        f3 = g * (np.cos(0.5 * np.pi * X[:, 1]) ** H) * (np.cos(0.5 * np.pi * X[:, 0]) ** H)
        return np.column_stack([f1, f2, f3])

    if prob_id == "MPMOP5":
        G = abs(np.sin(0.5 * np.pi * t))
        g = 1.0 + np.sum((X[:, 2:] - 0.5 * G * X[:, 0:1]) ** 2, axis=1)
        y = (np.pi * G / 6.0) + (np.pi / 2.0 - np.pi * G / 3.0) * X[:, 0:2]
        f1 = g * np.sin(y[:, 0])
        f2 = g * np.sin(y[:, 1]) * np.cos(y[:, 0])
        f3 = g * np.cos(y[:, 1]) * np.cos(y[:, 0])
        return np.column_stack([f1, f2, f3])

    if prob_id == "MPMOP6":
        k = int(np.floor(10.0 * np.sin(np.pi * t)))
        r = 1 - (k % 2)
        tmp1 = X[:, 2:] - np.sin(t * X[:, 0:1])
        # MATLAB: abs(sin(floor(k*(2*x(:,1:2)-r))*pi/2))
        tmp2 = np.abs(np.sin(np.floor(k * (2.0 * X[:, 0:2] - r)) * np.pi / 2.0))
        g = 1.0 + np.sum(tmp1**2, axis=1) + np.prod(tmp2, axis=1)
        f1 = g * np.cos(0.5 * np.pi * X[:, 1]) * np.cos(0.5 * np.pi * X[:, 0])
        f2 = g * np.sin(0.5 * np.pi * X[:, 1]) * np.cos(0.5 * np.pi * X[:, 0])
        f3 = g * np.sin(0.5 * np.pi * X[:, 0])
        return np.column_stack([f1, f2, f3])

    raise ValueError(f"Unknown MPMOP_Value id: {prob_id}")


class LiuMPMOP(MultiPartyProblem):
    """MPMOP built by evaluating ``MPMOP_Value`` at party-specific times ``t``."""

    def __init__(
        self,
        *,
        name: str,
        value_id: str,
        times: Sequence[float],
        xl: Sequence[float],
        xu: Sequence[float],
        n_var: int = 10,
        n_obj_each: int,
    ) -> None:
        n_dm = len(times)
        super().__init__(
            name=name,
            n_var=n_var,
            n_obj_per_dm=[n_obj_each] * n_dm,
            xl=xl,
            xu=xu,
            family="MPMOP",
            source=LIU2020_SOURCE,
            year=2020,
            common_ps_exists=CommonPSStatus.EXISTS,
            known_ps=True,
            known_pf=True,
            notes=(
                f"value_id={value_id}, times={list(times)}. "
                "Objective formulas from MPMOP_Value.m. "
                "Default n_var=10 from OptMPNDS classdefs; "
                "ZM26 experiments on MPMOP1–11 used D=2 (table caption)."
            ),
            metadata={
                "value_id": value_id,
                "times": list(times),
                "dimension_source": "OptMPNDS MATLAB default Global.D=10; ZM26 tab:MPMOP_results uses D=2",
                "dimension_default": 10,
                "dimension_status": "SOURCE_DEFAULT_OPTMPNDS",
            },
        )
        self.value_id = value_id
        self.times = [float(t) for t in times]

    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        blocks = [mpmop_value(self.value_id, X, t) for t in self.times]
        return np.concatenate(blocks, axis=1)

    def get_pareto_set(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        # Party-wise analytic PS depends on g(x)=1 manifold; common PS is nontrivial.
        # Provide g=1 manifold samples for each DM when possible; common via heuristic.
        if dm is None:
            return self._common_ps_approx(n_points)
        return self._party_ps(dm, n_points)

    def _party_ps(self, dm: int, n_points: int) -> Optional[np.ndarray]:
        t = self.times[dm]
        n = int(n_points)
        X = np.zeros((n, self.n_var))
        if self.value_id == "MPMOP1":
            X[:, 0] = np.linspace(float(self.xl[0]), float(self.xu[0]), n)
            a = 5.0 * np.cos(0.5 * np.pi * t)
            tmp = 1.0 / (1.0 + np.exp(a * (X[:, 0] - 2.5)))
            X[:, 1:] = tmp[:, None]
            return X
        if self.value_id == "MPMOP2":
            X[:, 0] = np.linspace(0.0, 1.0, n)
            G = np.sin(0.5 * np.pi * t)
            tmp = G * np.sin(4.0 * np.pi * X[:, 0]) / (1.0 + abs(G))
            X[:, 1:] = tmp[:, None]
            return X
        if self.value_id == "MPMOP5":
            # x3:end = 0.5*G*x1; x1,x2 free in [0,1]
            m = int(np.sqrt(n))
            m = max(m, 2)
            x1 = np.linspace(0.0, 1.0, m)
            x2 = np.linspace(0.0, 1.0, m)
            X1, X2 = np.meshgrid(x1, x2, indexing="ij")
            X = np.zeros((X1.size, self.n_var))
            X[:, 0] = X1.ravel()
            X[:, 1] = X2.ravel()
            G = abs(np.sin(0.5 * np.pi * t))
            X[:, 2:] = 0.5 * G * X[:, 0:1]
            return X
        # Fallback: None (needs true_PS numerical procedure)
        return None

    def _common_ps_approx(self, n_points: int) -> Optional[np.ndarray]:
        """Faithful, vectorized port of MATLAB ``true_PS.m`` sampling."""

        def retain_last_in_clusters(indices: np.ndarray) -> np.ndarray:
            if indices.size == 0:
                return indices
            discard = np.zeros(indices.size, dtype=bool)
            discard[:-1] = np.diff(indices) < 10
            return indices[~discard]

        if self.value_id == "MPMOP1":
            divisions = 20000 if self.name == "MPMOP1" else 40000
            x1_grid = np.linspace(1.0, 4.0, divisions)
            a = 5.0 * np.cos(0.5 * np.pi * np.asarray(self.times))
            manifolds = np.vstack(
                [1.0 / (1.0 + np.exp(ai * (x1_grid - 2.5))) for ai in a]
            )
            match = np.all(np.abs(manifolds[0] - manifolds[1:]) < 1e-4, axis=0)
            indices = retain_last_in_clusters(np.flatnonzero(match))
            x1 = x1_grid[indices]
            a2 = a[1]
            tail = 1.0 / (1.0 + np.exp(a2 * (x1 - 2.5)))
            X = np.empty((x1.size, self.n_var))
            X[:, 0] = x1
            X[:, 1:] = tail[:, None]
            return X

        if self.value_id == "MPMOP2":
            x1_grid = np.linspace(0.0, 1.0, 40000)
            G = np.sin(0.5 * np.pi * np.asarray(self.times))
            coefficients = G / (1.0 + np.abs(G))
            manifolds = coefficients[:, None] * np.sin(4.0 * np.pi * x1_grid)
            match = np.all(np.abs(manifolds[0] - manifolds[1:]) < 1e-4, axis=0)
            indices = retain_last_in_clusters(np.flatnonzero(match))
            x1 = x1_grid[indices]
            tail = coefficients[1] * np.sin(4.0 * np.pi * x1)
            X = np.empty((x1.size, self.n_var))
            X[:, 0] = x1
            X[:, 1:] = tail[:, None]
            return X

        if self.value_id == "MPMOP3":
            x1 = np.linspace(0.0, 1.0, 10000)
            keep = np.ones(x1.size, dtype=bool)
            for t in self.times:
                N = 1 + int(np.floor(10.0 * abs(np.sin(0.5 * np.pi * t))))
                for i in range(N):
                    keep &= ~((x1 > i / N) & (x1 < (2 * i + 1) / (2 * N)))
            X = x1[keep, None]
            for _ in range(1, self.n_var):
                next_column = np.cos(4.0 * self.times[0] + X[:, 0] + X[:, -1])
                X = np.column_stack([X, next_column])
            return X

        if self.value_id == "MPMOP5":
            axis = np.linspace(0.0, 1.0, 1000)
            G = np.abs(np.sin(0.5 * np.pi * np.asarray(self.times)))
            coefficients = 0.5 * G
            match = np.all(
                np.abs(
                    coefficients[0] * axis[None, :]
                    - coefficients[1:, None] * axis[None, :]
                )
                < 1e-4,
                axis=0,
            )
            x1 = axis[np.flatnonzero(match)[-1]]
            X = np.zeros((axis.size, self.n_var))
            X[:, 0] = x1
            X[:, 1] = axis
            X[:, 2:] = 0.5 * G[1] * x1
            return X

        if self.value_id == "MPMOP6":
            axis = np.linspace(0.0, 1.0, 1000)
            manifolds = np.vstack([np.sin(t * axis) for t in self.times])
            match = np.all(np.abs(manifolds[0] - manifolds[1:]) < 1e-4, axis=0)
            valid_x1 = axis[match]
            X = np.zeros((valid_x1.size * axis.size, self.n_var))
            X[:, 0] = np.repeat(valid_x1, axis.size)
            X[:, 1] = np.tile(axis, valid_x1.size)
            X[:, 2:] = np.sin(self.times[1] * X[:, 0:1])
            return X

        # MPMOP4/9 use an unsafe 20000x20000 mesh in the MATLAB source.
        return None

    def get_pareto_front(self, dm: Optional[int] = None, n_points: int = 1000) -> Optional[np.ndarray]:
        ps = self.get_pareto_set(dm=dm, n_points=n_points)
        if ps is None or ps.size == 0:
            return ps
        if dm is None:
            return self.evaluate(ps)
        return self.evaluate_dm(ps, dm)


def _bounds_mpmop1(n_var: int):
    xl = np.zeros(n_var)
    xu = np.ones(n_var)
    xl[0], xu[0] = 1.0, 4.0
    return xl, xu


def _bounds_mpmop2(n_var: int):
    xl = -np.ones(n_var)
    xu = np.ones(n_var)
    xl[0] = 0.0
    return xl, xu


def _bounds_mpmop4(n_var: int):
    xl = -np.ones(n_var)
    xu = np.ones(n_var)
    xl[0] = 0.0
    xl[1] = 0.0
    return xl, xu


def _bounds_unit(n_var: int):
    return np.zeros(n_var), np.ones(n_var)


class MPMOP1(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop1(n_var)
        super().__init__(
            name="MPMOP1", value_id="MPMOP1", times=[1.0, 2.0], xl=xl, xu=xu, n_var=n_var, n_obj_each=2
        )


class MPMOP2(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop2(n_var)
        super().__init__(
            name="MPMOP2", value_id="MPMOP2", times=[0.0, 3.0], xl=xl, xu=xu, n_var=n_var, n_obj_each=2
        )


class MPMOP3(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop2(n_var)
        super().__init__(
            name="MPMOP3",
            value_id="MPMOP3",
            times=[0.0, float(np.pi / 2.0)],
            xl=xl,
            xu=xu,
            n_var=n_var,
            n_obj_each=2,
        )


class MPMOP4(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop4(n_var)
        super().__init__(
            name="MPMOP4", value_id="MPMOP4", times=[0.0, 1.0], xl=xl, xu=xu, n_var=n_var, n_obj_each=3
        )


class MPMOP5(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_unit(n_var)
        super().__init__(
            name="MPMOP5", value_id="MPMOP5", times=[0.0, 1.5], xl=xl, xu=xu, n_var=n_var, n_obj_each=3
        )


class MPMOP6(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop4(n_var)
        super().__init__(
            name="MPMOP6", value_id="MPMOP6", times=[0.0, 1.0], xl=xl, xu=xu, n_var=n_var, n_obj_each=3
        )


class MPMOP7(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop1(n_var)
        super().__init__(
            name="MPMOP7", value_id="MPMOP1", times=[0.0, 1.0, 2.0], xl=xl, xu=xu, n_var=n_var, n_obj_each=2
        )


class MPMOP8(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop2(n_var)
        super().__init__(
            name="MPMOP8", value_id="MPMOP2", times=[0.0, 1.0, 3.0], xl=xl, xu=xu, n_var=n_var, n_obj_each=2
        )


class MPMOP9(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop4(n_var)
        super().__init__(
            name="MPMOP9",
            value_id="MPMOP4",
            times=[0.0, 0.5, 1.0],
            xl=xl,
            xu=xu,
            n_var=n_var,
            n_obj_each=3,
        )


class MPMOP10(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_unit(n_var)
        super().__init__(
            name="MPMOP10",
            value_id="MPMOP5",
            times=[0.0, 1.0, 1.5],
            xl=xl,
            xu=xu,
            n_var=n_var,
            n_obj_each=3,
        )


class MPMOP11(LiuMPMOP):
    def __init__(self, n_var: int = 10) -> None:
        xl, xu = _bounds_mpmop4(n_var)
        super().__init__(
            name="MPMOP11",
            value_id="MPMOP6",
            times=[0.0, 1.0, 1.5],
            xl=xl,
            xu=xu,
            n_var=n_var,
            n_obj_each=3,
        )

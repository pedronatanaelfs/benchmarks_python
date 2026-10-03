"""Base abstractions for multi-party multi-objective benchmarks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Sequence, Union

import numpy as np

from fairmoo_benchmarks.status import CommonPSStatus

ArrayLike = Union[np.ndarray, Sequence[float]]


class MultiPartyProblem(ABC):
    """Abstract multi-party multi-objective optimization problem.

    Objectives are concatenated as
    ``[DM0 objectives | DM1 objectives | ... ]``.
    Use :meth:`evaluate_dm` / :attr:`dm_objective_slices` to recover ownership.
    """

    def __init__(
        self,
        *,
        name: str,
        n_var: int,
        n_obj_per_dm: Sequence[int],
        xl: ArrayLike,
        xu: ArrayLike,
        family: str,
        source: str,
        year: Optional[int] = None,
        common_ps_exists: CommonPSStatus | str | bool | None = CommonPSStatus.UNKNOWN,
        known_ps: bool = False,
        known_pf: bool = False,
        dm_names: Optional[Sequence[str]] = None,
        notes: str = "",
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        self.name = name
        self.n_var = int(n_var)
        self.n_obj_per_dm = [int(k) for k in n_obj_per_dm]
        self.n_dm = len(self.n_obj_per_dm)
        self.n_obj = int(sum(self.n_obj_per_dm))
        self.xl = np.asarray(xl, dtype=float).reshape(self.n_var)
        self.xu = np.asarray(xu, dtype=float).reshape(self.n_var)
        if self.xl.shape != (self.n_var,) or self.xu.shape != (self.n_var,):
            raise ValueError("xl/xu must have shape (n_var,)")
        if np.any(self.xl > self.xu):
            raise ValueError("xl must be <= xu componentwise")

        self.dm_names = list(dm_names) if dm_names is not None else [
            f"DM{i + 1}" for i in range(self.n_dm)
        ]
        if len(self.dm_names) != self.n_dm:
            raise ValueError("dm_names length must equal n_dm")

        self._common_ps_status = CommonPSStatus.parse(common_ps_exists)

        self.metadata: dict[str, Any] = {
            "family": family,
            "source": source,
            "year": year,
            "n_dm": self.n_dm,
            "n_obj_per_dm": list(self.n_obj_per_dm),
            "common_ps_exists": self._common_ps_status.value,
            "common_ps_status": self._common_ps_status,
            "known_ps": bool(known_ps),
            "known_pf": bool(known_pf),
            "notes": notes,
        }
        if metadata:
            self.metadata.update(dict(metadata))
            # Keep status object authoritative if metadata overwrote the string.
            if "common_ps_status" in self.metadata and isinstance(
                self.metadata["common_ps_status"], CommonPSStatus
            ):
                self._common_ps_status = self.metadata["common_ps_status"]
                self.metadata["common_ps_exists"] = self._common_ps_status.value

        self._dm_slices: dict[int, slice] = {}
        start = 0
        for dm, k in enumerate(self.n_obj_per_dm):
            self._dm_slices[dm] = slice(start, start + k)
            start += k

    @property
    def dm_objective_slices(self) -> dict[int, slice]:
        return dict(self._dm_slices)

    @property
    def common_ps_status(self) -> CommonPSStatus:
        return self._common_ps_status

    @property
    def common_ps_exists(self) -> CommonPSStatus:
        """Alias for :attr:`common_ps_status` (type-safe enum, not a bool/str)."""
        return self._common_ps_status

    @staticmethod
    def _as_2d(X: ArrayLike) -> tuple[np.ndarray, bool]:
        arr = np.asarray(X, dtype=float)
        if arr.ndim == 1:
            return arr.reshape(1, -1), True
        if arr.ndim != 2:
            raise ValueError(f"X must be 1D or 2D, got shape {arr.shape}")
        return arr, False

    def evaluate(self, X: ArrayLike) -> np.ndarray:
        """Evaluate all objectives. Returns shape (n_obj,) or (N, n_obj)."""
        X2, was_1d = self._as_2d(X)
        if X2.shape[1] != self.n_var:
            raise ValueError(f"Expected n_var={self.n_var}, got {X2.shape[1]}")
        F = self._evaluate_impl(X2)
        F = np.asarray(F, dtype=float)
        if F.shape != (X2.shape[0], self.n_obj):
            raise RuntimeError(
                f"{self.name}._evaluate_impl returned shape {F.shape}, "
                f"expected {(X2.shape[0], self.n_obj)}"
            )
        return F[0] if was_1d else F

    def evaluate_dm(self, X: ArrayLike, dm: int) -> np.ndarray:
        """Evaluate objectives belonging only to decision maker ``dm`` (0-based)."""
        if dm < 0 or dm >= self.n_dm:
            raise IndexError(f"dm must be in [0, {self.n_dm})")
        F = self.evaluate(X)
        sl = self._dm_slices[dm]
        if F.ndim == 1:
            return F[sl]
        return F[:, sl]

    def evaluate_dict(self, X: ArrayLike) -> dict[int, np.ndarray]:
        """Return ``{dm: F_dm}`` for all decision makers."""
        F = self.evaluate(X)
        out: dict[int, np.ndarray] = {}
        for dm, sl in self._dm_slices.items():
            out[dm] = F[sl] if F.ndim == 1 else F[:, sl]
        return out

    @abstractmethod
    def _evaluate_impl(self, X: np.ndarray) -> np.ndarray:
        """Vectorized evaluation for ``X`` of shape ``(N, n_var)``."""

    def get_pareto_set(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        """Return Pareto set samples when known, else ``None``.

        Returned samples may be analytic or densified along a known manifold.
        They are not claimed to be a complete PF discretization unless documented.
        """
        return None

    def get_pareto_front(
        self, dm: Optional[int] = None, n_points: int = 1000
    ) -> Optional[np.ndarray]:
        """Return Pareto front samples when known, else ``None``."""
        return None

    def get_reference_points(self, dm: Optional[int] = None) -> Optional[np.ndarray]:
        """Return reference/target points when applicable, else ``None``."""
        return None

    def get_common_pareto_set(self, n_points: int = 1000) -> Optional[np.ndarray]:
        """Return common PS samples when known.

        - ``CommonPSStatus.EMPTY`` → empty array shape ``(0, n_var)``
        - ``CommonPSStatus.UNKNOWN`` → ``None``
        - ``CommonPSStatus.EXISTS`` → samples from :meth:`get_pareto_set` with ``dm=None``
        """
        status = self.common_ps_status
        if status is CommonPSStatus.EMPTY:
            return np.zeros((0, self.n_var), dtype=float)
        if status is CommonPSStatus.UNKNOWN:
            return None
        return self.get_pareto_set(dm=None, n_points=n_points)

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "family": self.metadata.get("family"),
            "n_var": self.n_var,
            "n_dm": self.n_dm,
            "n_obj_per_dm": list(self.n_obj_per_dm),
            "n_obj_total": self.n_obj,
            "xl": self.xl.tolist(),
            "xu": self.xu.tolist(),
            "source": self.metadata.get("source"),
            "year": self.metadata.get("year"),
            "pareto_set_known": bool(self.metadata.get("known_ps")),
            "pareto_front_known": bool(self.metadata.get("known_pf")),
            "common_ps_status": self.common_ps_status.value,
            "common_ps_exists": self.common_ps_status.value,  # backward-compatible key
            "notes": self.metadata.get("notes", ""),
            "dimension_source": self.metadata.get("dimension_source"),
            "dimension_status": self.metadata.get("dimension_status"),
        }

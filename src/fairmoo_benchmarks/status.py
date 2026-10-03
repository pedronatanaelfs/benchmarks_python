"""Enums and shared status types for multi-party benchmarks."""

from __future__ import annotations

from enum import Enum


class CommonPSStatus(Enum):
    """Whether a common Pareto set across all DMs is known to exist.

    Use this enum instead of strings/bools. In particular, never do
    ``bool("False")`` — that evaluates to ``True`` in Python.
    """

    EXISTS = "exists"
    EMPTY = "empty"
    UNKNOWN = "unknown"

    @classmethod
    def parse(cls, value: "CommonPSStatus | str | bool | None") -> "CommonPSStatus":
        """Parse legacy and current representations."""
        if isinstance(value, cls):
            return value
        if value is None:
            return cls.UNKNOWN
        if isinstance(value, bool):
            return cls.EXISTS if value else cls.EMPTY
        if isinstance(value, str):
            key = value.strip().lower()
            legacy = {
                "true": cls.EXISTS,
                "false": cls.EMPTY,
                "unknown": cls.UNKNOWN,
                "exists": cls.EXISTS,
                "empty": cls.EMPTY,
                "none": cls.UNKNOWN,
            }
            if key in legacy:
                return legacy[key]
        raise ValueError(
            f"Invalid CommonPSStatus {value!r}; "
            f"expected one of {[e.value for e in cls]} or legacy True/False/Unknown"
        )

    def __bool__(self) -> bool:  # pragma: no cover - defensive
        raise TypeError(
            "CommonPSStatus cannot be used as a bool. "
            "Compare against CommonPSStatus.EXISTS / EMPTY / UNKNOWN."
        )

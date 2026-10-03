"""Tests for type-safe CommonPSStatus."""

from __future__ import annotations

import pytest

from fairmoo_benchmarks import CommonPSStatus, get_problem


def test_parse_legacy_strings() -> None:
    assert CommonPSStatus.parse("True") is CommonPSStatus.EXISTS
    assert CommonPSStatus.parse("False") is CommonPSStatus.EMPTY
    assert CommonPSStatus.parse("Unknown") is CommonPSStatus.UNKNOWN
    assert CommonPSStatus.parse("exists") is CommonPSStatus.EXISTS
    assert CommonPSStatus.parse(None) is CommonPSStatus.UNKNOWN
    assert CommonPSStatus.parse(True) is CommonPSStatus.EXISTS
    assert CommonPSStatus.parse(False) is CommonPSStatus.EMPTY


def test_bool_cast_is_rejected() -> None:
    # Document the Python pitfall that motivated the enum.
    assert bool("False") is True
    with pytest.raises(TypeError):
        bool(CommonPSStatus.EMPTY)
    with pytest.raises(TypeError):
        if CommonPSStatus.EMPTY:  # noqa: SIM102
            pass


def test_mpdmp13_status_enum() -> None:
    p = get_problem("MPDMP13")
    assert p.common_ps_status is CommonPSStatus.EMPTY
    assert p.describe()["common_ps_status"] == "empty"
    # Must not be the string "False" that bool()-casts truthily
    assert p.common_ps_status is not True
    assert p.common_ps_status is not False


def test_mpmop1_status_exists() -> None:
    p = get_problem("MPMOP1")
    assert p.common_ps_status is CommonPSStatus.EXISTS

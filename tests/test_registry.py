"""Registry completeness tests."""

from fairmoo_benchmarks import list_problems


def test_registry_counts() -> None:
    names = list_problems()
    mpmops = [n for n in names if n.startswith("MPMOP")]
    mpdmps = [n for n in names if n.startswith("MPDMP")]
    assert len(mpmops) == 17
    assert len(mpdmps) == 18
    assert len(names) == 35
    assert len(set(names)) == 35
    assert mpmops == [f"MPMOP{i}" for i in range(1, 18)]
    assert mpdmps == [f"MPDMP{i}" for i in range(1, 19)]

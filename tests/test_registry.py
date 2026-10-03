"""Registry and describe() tests."""

from fairmoo_benchmarks import describe_problem, get_problem, list_problems


def test_list_count() -> None:
    names = list_problems()
    assert len(names) == 35
    assert "MPMOP1" in names and "MPMOP17" in names
    assert "MPDMP1" in names and "MPDMP18" in names


def test_describe_mpdmp17() -> None:
    d = describe_problem("MPDMP17")
    assert d["name"] == "MPDMP17"
    assert d["family"] == "MPDMP"
    assert d["n_var"] == 2
    assert d["n_dm"] == 3
    assert d["n_obj_per_dm"] == [2, 2, 2]
    assert d["pareto_set_known"] is True


def test_get_problem_aliases() -> None:
    assert get_problem("mpdmp13").name == "MPDMP13"

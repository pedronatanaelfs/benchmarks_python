"""Structural checks used by the MATLAB↔Python equivalence audit."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest


VALIDATION_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = VALIDATION_DIR.parent
sys.path.insert(0, str(VALIDATION_DIR))
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from fairmoo_benchmarks import get_problem, list_problems  # noqa: E402
from generate_reference_inputs import deterministic_points, reference_metadata  # noqa: E402


ALL_PROBLEMS = list_problems()


def test_registry_contains_all_35_problems() -> None:
    assert ALL_PROBLEMS == [
        *(f"MPDMP{i}" for i in range(1, 19)),
        *(f"MPMOP{i}" for i in range(1, 18)),
    ]


@pytest.mark.parametrize("problem_name", ALL_PROBLEMS)
def test_output_shape_and_finiteness(problem_name: str) -> None:
    problem = get_problem(problem_name)
    _, X = deterministic_points(problem.xl, problem.xu)
    F = problem.evaluate(X)
    assert F.shape == (X.shape[0], problem.n_obj)
    assert np.all(np.isfinite(F))


@pytest.mark.parametrize("problem_name", ALL_PROBLEMS)
def test_dm_partition_is_complete_and_ordered(problem_name: str) -> None:
    problem = get_problem(problem_name)
    indices = []
    for dm in range(problem.n_dm):
        sl = problem.dm_objective_slices[dm]
        indices.extend(range(sl.start, sl.stop))
        assert sl.stop - sl.start == problem.n_obj_per_dm[dm]
    assert indices == list(range(problem.n_obj))


@pytest.mark.parametrize("problem_name", ALL_PROBLEMS)
def test_bounds_have_expected_shape_and_order(problem_name: str) -> None:
    problem = get_problem(problem_name)
    assert problem.xl.shape == (problem.n_var,)
    assert problem.xu.shape == (problem.n_var,)
    assert np.all(problem.xl <= problem.xu)


@pytest.mark.parametrize("problem_name", ALL_PROBLEMS)
def test_static_reference_structure_classification(problem_name: str) -> None:
    """Keep known MATLAB metadata disagreements explicit in the audit trail."""
    problem = get_problem(problem_name)
    reference = reference_metadata(problem_name)
    matches = (
        problem.n_var == reference["D"]
        and problem.n_obj == reference["M"]
        and problem.n_dm == reference["DM"]
        and problem.n_obj_per_dm == reference["n_obj_per_dm"]
        and np.array_equal(problem.xl, reference["lower"])
        and np.array_equal(problem.xu, reference["upper"])
    )
    assert matches

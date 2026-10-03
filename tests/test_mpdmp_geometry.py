"""Geometric tests for MATLAB nsidedpoly vertex convention used in MPDMP."""

from __future__ import annotations

import numpy as np
import pytest

from fairmoo_benchmarks import get_problem
from fairmoo_benchmarks.utils import matlab_nsidedpoly_vertices


def test_radius_mode_first_vertex_to_the_right() -> None:
    # MathWorks nsidedpoly: first vertex to the right of center, then CCW.
    V = matlab_nsidedpoly_vertices(3, [50.0, 40.0], radius=20.0)
    assert V.shape == (3, 2)
    assert np.allclose(V[0], [70.0, 40.0], atol=1e-12)
    # CCW: second vertex has positive y relative to center after rightmost
    assert V[1, 1] > 40.0


def test_sidelength_square_axis_aligned_matches_mpdmp6_ps() -> None:
    # MPDMP6.m hardcodes common PS at x=50, y in [40,60], which matches
    # axis-aligned squares with SideLength centers (38,50)/side24 and (60,50)/side20.
    p1 = matlab_nsidedpoly_vertices(4, [38.0, 50.0], side_length=24.0)
    p2 = matlab_nsidedpoly_vertices(4, [60.0, 50.0], side_length=20.0)
    # Axis-aligned: x coords should be {26,50} and {50,70}
    assert np.isclose(p1[:, 0].min(), 26.0, atol=1e-9)
    assert np.isclose(p1[:, 0].max(), 50.0, atol=1e-9)
    assert np.isclose(p2[:, 0].min(), 50.0, atol=1e-9)
    assert np.isclose(p2[:, 0].max(), 70.0, atol=1e-9)
    problem = get_problem("MPDMP6")
    assert np.allclose(problem.get_reference_points(0), p1)
    assert np.allclose(problem.get_reference_points(1), p2)


@pytest.mark.parametrize(
    "name,dm,n_obj",
    [
        ("MPDMP3", 1, 3),
        ("MPDMP5", 0, 3),
        ("MPDMP7", 0, 4),
        ("MPDMP8", 0, 5),
        ("MPDMP11", 0, 3),
        ("MPDMP12", 0, 4),
    ],
)
def test_polygon_vertex_objectives_zero(name: str, dm: int, n_obj: int) -> None:
    p = get_problem(name)
    refs = p.get_reference_points(dm)
    assert refs is not None and refs.shape[0] == n_obj
    F = p.evaluate_dm(refs, dm)
    assert np.allclose(np.diag(F), 0.0, atol=1e-12)

# Mathematical Validation Notes

Licensed MATLAB (unmodified OptMPNDS + 2026ZhaoNash sources) is the
implementation ground truth. See `validation/validation_report.md` and
`validation/equivalence_matrix.md` for the current 33 PASS / 2 PARTIAL
status.

## Distance problems (MPDMP)

For every reference point \(p_{m,i}\):

\[
f_{m,i}(p_{m,i}) = 0
\]

Checked in `tests/test_mpdmp_analytical.py` for MPDMP13–18 and via diagonal
checks for She2023 instances with explicit points. Objective vectors also
match licensed MATLAB at `rtol=1e-9`, `atol=1e-10`.

Koppen/Rudolph geometry: the Pareto set of a single DM with Euclidean
distances to a finite point set is the convex hull of those points.
Party-wise PS samplers for 2-point DMs return the segment; for ≥3 points in
2D they sample the polygon.

Common PS:

- MPDMP13–18: empty (`CommonPSStatus.EMPTY`) per MATLAB construction
- MPDMP1/2/4/6/9/10: explicit points/segments from MATLAB
- Remaining polygon problems: MATLAB 1000×1000 `inpolygon` grids, reproduced
  in Python (PASS against licensed-MATLAB PS/PF exports)

Vertex order follows MATLAB `nsidedpoly` / `polyshape.Vertices`, not
MathWorks documentation alone.

## MPMOP12–17

Python follows the executable MATLAB classes, not Appendix Table S-VI where
they conflict. MATLAB constructors set `Global.D = 10` and unit bounds
`[0,1]^D`. MATLAB MPMOP15 calls the MPMOP17 kernel (duplicate). MPMOP16 has
`M=4`, `DM=2`; MPMOP17/15 have `M=6`, `DM=3`. Objectives, party PS, and PF
match licensed MATLAB.

## MPMOP1–11 (Liu / OptMPNDS)

Objective formulas match `MPMOP_Value.m` against licensed MATLAB.
Python `true_PS` sampling matches MATLAB for MPMOP1–3, 5–8, and 10–11.
MPMOP4/9 objectives pass; their MATLAB `true_PS.m` requests a 20,000×20,000
mesh and is not safely executable, so those two remain PARTIAL.

## MATLAB equivalence (executed)

All 35 benchmarks were evaluated on the same 18 deterministic decision
vectors in licensed MATLAB and Python:

```python
np.allclose(F_python, F_matlab, rtol=1e-9, atol=1e-10)
```

Result: **35/35 objective PASS**. PS/PF: **33/33** for every safely
executable MATLAB reference. Artifacts live under
`validation/matlab/results/`, `validation/matlab/pareto_results/`, and
`validation/reports/`.

GNU Octave remains an optional secondary check for MPMOP1–11 via
`validation/matlab_octave/`. It is not used as proof of MATLAB equivalence.
MPDMP PlatEMO classdefs remain `OCTAVE_INCOMPATIBLE`.

# Mathematical Validation Notes

## Distance problems (MPDMP)

For every reference point \(p_{m,i}\):

\[
f_{m,i}(p_{m,i}) = 0
\]

Checked in `tests/test_mpdmp_analytical.py` for MPDMP13–18 and via diagonal checks for She2023 instances with explicit points.

Koppen/Rudolph geometry: the Pareto set of a single DM with Euclidean distances to a finite point set is the convex hull of those points. Party-wise PS samplers for 2-point DMs return the segment; for ≥3 points in 2D they sample the polygon.

Common PS:
- MPDMP13–18: empty (`common_ps_exists='False'`) per ZM26 construction
- MPDMP1/2/4/6/9/10: explicit points/segments from MATLAB
- Others: intersection sampling left PARTIAL where only `inpolygon` mesh was used in MATLAB

## MPMOP12–17 (ZM26)

On each party PS, the corresponding \(g_m(x)=1\) (plus inactive penalty terms). Checked for MPMOP12/15 in `tests/test_pareto_sets.py` and `tests/test_mpmop_analytical.py`.

## MPMOP1–11 (Liu / OptMPNDS)

Objective formulas match `MPMOP_Value.m`. Common PS generation in MATLAB uses a dense search in `true_PS.m` (Symbolic Math / mesh filters). Python provides manifold samples for simple cases (MPMOP1/2/5) and returns `None` when the MATLAB procedure is not yet ported — this is intentional (no fabricated PF/PS).

## Octave / MATLAB equivalence

Not executed: GNU Octave is not installed. When available, compare:

```python
np.allclose(F_python, F_matlab, rtol=1e-8, atol=1e-10)
```

using CSVs under `validation/matlab_octave/`.

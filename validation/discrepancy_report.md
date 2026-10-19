# Static discrepancy report

This report separates observed source differences from proposed corrections.
The objective-function corrections described below have now been applied and
verified against all 35 licensed-MATLAB CSVs. Historical observations are
retained as an audit trail.

## Remediation status

- MPMOP12–17: **RESOLVED** — equations, bounds, objective counts, DM
  partitions, party PS, and MATLAB-compatible PF samplers now follow the
  executable MATLAB classes.
- MPDMP3–8 and MPDMP10–12: **RESOLVED** — `nsidedpoly` orientation and
  `polyshape.Vertices` objective ordering now match MATLAB.
- MPDMP13–18: MATLAB conflict PF samplers and concession tables are ported.
- Deterministic objective comparison: **PASS 35/35**.
- Deterministic PS/PF comparison: **PASS 33/33 safely executable
  references**. MPMOP4/9 are unexecuted because the reference itself requests
  an unsafe 20000×20000 mesh.

## MPMOP12

**Files:** `2026ZhaoNash-main/MPMOP/MPMOP12.m`,
`MPMOP_Value.m`, and `src/fairmoo_benchmarks/mpmop/mpmop12.py`

**MATLAB behavior:** unit bounds. DM1 uses
`g=1+Σ(x2:D-1)^2`, DM2 uses `g=1+Σ(x2:D-0)^2`; both return
`[g*x1, g*(1-x1)]`.

**Python behavior:** `x1∈[1,4]`; DM1 uses a 0.5 shift and
`[2g/x1, gx1/2]`; DM2 uses a logistic shift and
`[3g/x1, gx1/3]`.

**Difference/impact:** bounds, distance manifolds, objective equations, PS,
and PF all differ. Identical `X` generally produces different `F`.

**Proposed fix:** first decide whether the port targets the published
Appendix Table S-VI or the supplied MATLAB repository. If MATLAB is the
required reference, port the current `MPMOP_Value` case and class bounds.

**Required retest:** all deterministic points plus both party PS manifolds.

## MPMOP13

**Files:** MATLAB `MPMOP13.m`/`MPMOP_Value.m`; Python `mpmop13.py`

**MATLAB behavior:** party constants are 0 and 1; the shape variable is
`z=0.2+0.6*x1`; objectives are `[g*z, g*(1-z)]`.

**Python behavior:** sinusoidal manifolds, one-sided penalties around
`x1=0.5`, a sinusoidal objective perturbation, and exponent 4.25.

**Difference/impact:** metadata agrees, but objective values and party PS/PF
do not.

**Proposed fix:** same specification decision as MPMOP12.

**Required retest:** include `x1` below, at, and above 0.5.

## MPMOP14

**Files:** MATLAB `MPMOP14.m`/`MPMOP_Value.m`; Python `mpmop14.py`

**MATLAB behavior:** party constants are 1 and 0 in columns `x3:D`.
Objectives use the unsquared spherical factors.

**Python behavior:** party manifolds are two different sinusoidal functions
of `x1+x2`; all spherical factors are squared.

**Difference/impact:** objective equations and party PS/PF differ.

**Proposed fix:** port the constant-shift MATLAB case if repository
equivalence is the target.

**Required retest:** heterogeneous `x3:D` and phase-sensitive `x1,x2`.

## MPMOP15

**Files:** MATLAB `MPMOP15.m` calling the `MPMOP17` value case; Python
`mpmop15.py`

**MATLAB behavior:** unit bounds, three parties with constants 0, 0.5, and
1, each returning two linear bi-objective values. The class calls the
`MPMOP17` kernel, so MATLAB MPMOP15 and MPMOP17 are duplicate objective
problems. The separate three-objective `case 'MPMOP15'` in
`MPMOP_Value.m` is orphaned: no supplied class calls it.

**Python behavior:** `x1∈[1,4]`; three rational bi-objective blocks with
0.5/logistic/0.5 manifolds.

**Difference/impact:** bounds, equations, PS, and PF differ.

**Proposed fix:** resolve the benchmark-specification conflict, then port
the selected source explicitly rather than relying on the shared number.

**Required retest:** all three party manifolds and interval endpoints.

## MPMOP16

**Files:** MATLAB `MPMOP16.m`/`MPMOP_Value.m`; Python `mpmop16.py`

**MATLAB behavior:** `M=4`, `DM=2`, constants 0.25 and 0.75, two objectives
per party.

**Python behavior:** `M=6`, `DM=3`, sinusoidal manifolds, interval penalties,
and party-specific powers 2.5/3/3.5.

**Difference/impact:** objective count, DM partition, equations, PS, and PF
differ. Output matrices cannot even be shape-compared.

**Proposed fix:** resolve the source specification and update metadata and
equations together.

**Required retest:** metadata, output shape, and all three Python interval
branches (or both MATLAB parties after correction).

## MPMOP17

**Files:** MATLAB `MPMOP17.m`/`MPMOP_Value.m`; Python `mpmop17.py`

**MATLAB behavior:** `M=6`, three parties, two objectives each; constants
0, 0.5, and 1 are selected by the `t<=0.25`, `t<0.75`, and final branches.

**Python behavior:** `M=9`, three parties, three objectives each; spherical
objectives are used and parties 1/3 share a `0.5*x1` manifold.

**Difference/impact:** objective count, DM objective grouping, equations,
PS, and PF differ.

**Proposed fix:** resolve the source specification and then align both
metadata and implementation.

**Required retest:** all three MATLAB `t` branches and shape comparison.

## PF behavior: MPDMP13–18

**Files:** MATLAB geometry helpers `ParallelLines1.m` through
`ThreeDiagonals.m`; Python numbered MPDMP modules and `distance_base.py`

**MATLAB behavior:** `PS()` is empty, but `PF()` returns 100 or 300 sampled
compromise-path objective vectors.

**Python behavior:** common PS is correctly represented as empty.
`get_pareto_front(dm=None)` evaluates the empty common PS and therefore
returns an empty matrix. Party-specific PF calls instead sample each party's
convex hull.

**Difference/impact:** objective evaluation is statically equivalent, but
the reference PF API and sampling semantics are not.

**Proposed fix:** add a separately named MATLAB-compatible compromise PF
sampler, or document that Python's API intentionally means “front of common
PS.” Do not conflate this with objective-function equivalence.

**Required retest:** compare MATLAB `Map.PF()` independently from `evaluate`.

## MPDMP3–8 and MPDMP10–12: objective geometry/order

Deterministic MATLAB evaluation disproved the Python port's
`matlab_nsidedpoly_vertices` assumptions and exposed `polyshape.Vertices`
ordering differences. These are objective-vector failures, not PF-only
differences.

### Geometry mismatches

- **MPDMP3:** MATLAB's triangle vertices are
  `(32.67949192,30)`, `(50,60)`, `(67.32050808,30)`.
  Python uses `(70,40)`, `(40,57.32050808)`,
  `(40,22.67949192)`.
- **MPDMP5:** both MATLAB triangles point upward; Python rotates them so a
  vertex points right. For DM1, MATLAB starts from the set
  `{(4.35898385,20),(39,80),(73.64101615,20)}`, whereas Python uses
  `{(79,40),(19,74.64101615),(19,5.35898385)}`.
- **MPDMP8:** MATLAB pentagons have a top vertex; Python pentagons have a
  rightmost vertex.
- **MPDMP11:** the same triangle rotation error occurs independently for
  all three DMs.
- **MPDMP12:** MATLAB `Radius=20` squares have corner offsets
  `20/sqrt(2)` (for example `(15.85786438,25.85786438)` around center
  `(30,40)`). Python instead uses cardinal vertices `(50,40)`,
  `(30,60)`, `(10,40)`, `(30,20)`.

### Objective-order-only mismatches

The reference-point sets match for **MPDMP4, MPDMP6, MPDMP7, and MPDMP10**,
but MATLAB `polyshape.Vertices` normalizes boundary order. Python retains a
different constructor/trigonometric order. Therefore identical distances
appear in different objective columns:

- MPDMP4 MATLAB DM1: top, lower-right, lower-left; Python: top,
  lower-left, lower-right.
- MPDMP6/7 MATLAB square order: lower-left, upper-left, upper-right,
  lower-right. Python starts at upper-right.
- MPDMP10's square block has the same ordering issue.

**Impact:** all nine problems fail the required ordered-vector comparison.
Within-DM permutation does not rescue equivalence because objective identity
and ordering are part of the benchmark contract.

**Proposed correction:** replace the approximate `nsidedpoly` conversion
with MATLAB-confirmed orientation and reproduce `polyshape.Vertices` order.
Use the recovered MATLAB coordinates above (and the generated result CSVs)
as regression fixtures. Do not merely sort objective values at comparison
time.

**Required retest:** all deterministic vectors for MPDMP3–8 and MPDMP10–12,
plus zero-distance tests at every MATLAB reference vertex.

## PF/PS behavior: MPMOP1–11 and MPDMP1–12

Python frequently returns a densified geometric helper, an approximation,
or `None`, while MATLAB uses benchmark-specific `true_PS` or map-specific
sampling. Objective evaluation is independent of this difference. Exact
sampling equivalence remains `PARTIAL` until separately tested.

The supplied MATLAB `PF()` implementations for MPDMP9 and MPDMP10 also
contain a reference-code defect: they pass `obj.PS` rather than invoking
`obj.PS()`. The objective functions can still be tested through `CalObj`,
but PF equivalence for those two problems requires either documenting the
MATLAB error or an explicitly approved reference patch.

## High-risk conversion points

1. MATLAB MPMOP classes call `PopDec()` rather than indexing a numeric
   matrix; the harness deliberately supplies a zero-argument function handle.
2. MATLAB indices such as `x(:,3:end)` correspond to Python `X[:,2:]`.
3. MPMOP3 recursively uses the previous transformed coordinate.
4. MPMOP6 combines `floor`, MATLAB `mod`, a product, and trigonometric values
   close to integers.
5. MPDMP objective order is defined by helper output and `DM` cells; it is
   not always the visual vertex label order.
6. `nsidedpoly` orientation and SideLength-versus-Radius construction cause
   confirmed objective failures in MPDMP3/5/8/11/12; normalized
   `polyshape.Vertices` ordering also affects MPDMP4/6/7/10.
7. MPDMP `CalObj` projects a decision vector with more than two columns to
   its first and last columns.
8. MATLAB PF routines and Python common-PF APIs have different meanings in
   conflict cases.
9. Python has no first-class `encoding` attribute; “real” is currently an
   inferred semantic property in the validation metadata.
10. MATLAB MPMOP15 is intentionally evaluated exactly as written—through
    the MPMOP17 kernel—not through the orphan `MPMOP15` value case.
11. MATLAB MPDMP9/10 PF methods have a missing-parentheses defect; this
    must not be mistaken for an objective-function mismatch.

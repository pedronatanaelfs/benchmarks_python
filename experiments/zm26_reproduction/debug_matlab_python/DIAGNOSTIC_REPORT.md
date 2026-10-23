# DIAGNOSTIC_REPORT — MPDMP4 / OptMPNDS

**Status: MATLAB component outputs compared. Production code was not modified.**

Native 5-run MATLAB (`test_12`) is optional and may still be missing.

## Summary

| Test | Component | MATLAB vs Python | Severity |
|---|---|---|---|
| 01 | problem evaluation | PASS | NONE |
| 02 | MPNDS | FAIL | CRITICAL |
| 03a | crowding distance | PASS | NONE |
| 03b | crowding entropy | FAIL | MAJOR |
| 04 | environmental selection | PASS | NONE |
| 05 | initialization | PASS | NONE |
| 06 | variation (SBX+PM matlab rate) | PASS | NONE |
| 07 | short run X_g0 | PASS | NONE |
| 07 | short run X_g1 | PASS | NONE |
| 07 | short run X_g2 | PASS | NONE |
| 07 | short run X_g3 | PASS | NONE |
| 07 | short run X_g4 | PASS | NONE |
| 07 | short run X_g5 | PASS | NONE |
| 08 | unique-row behavior | PASS | NONE |
| 09 | one-by-one entropy removal | PASS | NONE |
| 10 | boundary repair | PASS | NONE |
| 11 | objective grouping | PASS | NONE |
| 13 | JADE2 one-step (OptMPNDS3) | PASS | NONE |
| 12 | native 5-run magnitude | WAITING_MATLAB | UNKNOWN |

## Test 04 environmental selection set comparison

- selected identically: 100
- symmetric difference size: 0
- Jaccard similarity: 1.000000
- only MATLAB (first 20): []
- only Python (first 20): []

## Discrepancy records

### 02 — MPNDS

- MATLAB file/function: `Public/MPNDS.m, NDSort.m, PLNDS.m`
- Python file/function: `algorithms/operators.py mpnds/nd_sort/plnds`
- Input: `shared_inputs/mpnds_F.csv`
- First differing value: front_DM1: index=1 MATLAB=6.0 Python=inf absdiff=inf
- Detail: front_DM1: index=1 MATLAB=6.0 Python=inf absdiff=inf; front_DM2: index=11 MATLAB=8.0 Python=inf absdiff=inf; combined_front: index=0 MATLAB=6.0 Python=2.0 absdiff=4.0; plnds_front: index=5 MATLAB=4.0 Python=inf absdiff=inf
- Likely cause: nd_sort stops when assigned original rows >= n_unique, leaving inf; mpnds leftover dump then collapses combined fronts.
- Impact on optimization: Latent on unique MPDMP4 populations (Tests 04/07 still passed). Breaks duplicate/PLNDS cases.
- Suggested fix: Use assigned < n_sort (MATLAB min(nSort,length(Loc))); remove mpnds leftover assignment.

### 03b — crowding entropy

- MATLAB file/function: `Public/CrowdingEntropy.m`
- Python file/function: `algorithms/operators.py crowding_entropy`
- Input: `shared_inputs/crowding_F.csv`
- First differing value: entropy_value: index=0 MATLAB=nan Python=inf absdiff=nan
- Detail: entropy_value: index=0 MATLAB=nan Python=inf absdiff=nan
- Likely cause: MATLAB NaN on c=0 / zero span; Python uses 0 and keeps boundary Inf.
- Impact on optimization: OptMPNDS3 only. OptMPNDS does not use entropy.
- Suggested fix: Reproduce MATLAB NaN/Inf, or document the guard as intentional.

## Python native OptMPNDS / MPDMP4 (5 runs, N=200, FE=80000)

These numbers are Python-only. They are not a MATLAB comparison.

| run | meanIGD | she_IGD_single_PF | mean_dist_to_common_ps | pop_mean_x1 | pop_mean_x2 |
|---:|---:|---:|---:|---:|---:|
| 1 | 19.3734 | 0.000619387 | 0.338593 | 50.0516 | 39.7695 |
| 2 | 21.387 | 0.000669839 | 0.232089 | 49.976 | 39.8257 |
| 3 | 17.9673 | 0.0016279 | 0.368577 | 49.934 | 39.7705 |
| 4 | 17.0919 | 0.0141559 | 0.39405 | 50.0119 | 39.7441 |
| 5 | 21.1716 | 0.00282524 | 0.26337 | 49.9946 | 39.8169 |

Observation: the search collapses near the common PS `(50,40)` while party-wise triangle `meanIGD` stays O(10). `she_IGD_single_PF` (MATLAB `IGD.m` + `MPDMP4.PF()=CalObj([50,40])`) is O(10^-3).

## Confirmed findings (after MATLAB CSVs)

### A. MPDMP4 evaluation is not the failure

Test 01 matches within `1e-9`. DM grouping is `DM1=1:3`, `DM2=4:6` on both sides. Stop looking at the benchmark package for the MPDMP4 IGD table gap.

### B. OptMPNDS search on typical MPDMP4 populations matches MATLAB

From the **same** `X` / `F` / random streams:

- Test 04 environmental selection: identical 100 survivors, Jaccard `1.0`, matching fronts and crowding.
- Test 06 SBX+PM at MATLAB rate `proM/D`: offspring match.
- Test 07 five-generation trace: `X` matches at every generation `g=0..5`.
- Test 10 bound repair: clip, not reflect/regenerate.

On this evidence, the Python OptMPNDS loop is behaviorally equivalent to MATLAB **when objective rows are unique**, which is the usual MPDMP4 case.

### C. Python `nd_sort` stops too early when duplicate objective rows exist

MATLAB `NDSort.m` ENS-SS:

```matlab
while sum(Table(FrontNo<inf)) < min(nSort,length(Loc))
```

`length(Loc)` is the number of **original** points. Python `operators.nd_sort` uses `while assigned < min(n_sort, nu)` where `nu` is the number of **unique** rows, while `assigned` still counts original rows via `table`. Duplicate rows make `assigned` jump past `nu` and leave later uniques as `inf`.

On `shared_inputs/mpnds_F.csv` (18 points, 16 unique 6-D, 15 unique per party):

| point_id | MATLAB front_DM1 | Python front_DM1 |
|---:|---:|---:|
| 2 | 6 | inf |
| 12 | 8 | inf |
| 18 | 7 | inf |

Python `mpnds` then hits empty `Fz` (because of those `inf` party ranks) and dumps leftovers onto combined front 2. MATLAB combined fronts are `{1,2,3,4,5,6,7,8}`.

Changing the stop condition to `assigned < n_sort` (MATLAB `min(nSort,length(Loc))`) and removing the leftover dump restores exact integer equality for `front_DM1`, `front_DM2`, `combined_front`, and `plnds_front`. **Not applied yet.**

Impact: latent on continuous MPDMP4 (Test 04/07 still passed). Real for duplicate objectives, PLNDS/OptMPNDS2, and any call that does not fully sort.

### D. Crowding distance matches; crowding entropy does not

OptMPNDS uses `CrowdingDistance.m`. Those values match, including `Inf` boundaries.

`CrowdingEntropy.m` (OptMPNDS3) writes `NaN` when `c=0` or `Fmax=Fmin` (`log2(0)`, `x/0`). Python guards those cases to `0` and keeps boundary `Inf`. First mismatch: point 1 MATLAB `NaN` vs Python `Inf`. Interior finite values that are well-defined (point 8) match. Test 09 removal **sequence** still matched because this last-front sample did not hit the NaN path the same way.

### E. The ZM26 table gap on MPDMP4 is not explained by a broken OptMPNDS search

Python native runs sit on `(50,40)` with party-wise triangle `meanIGD≈19` and She-style single-point IGD `≈1e-3` (paper MATLAB meanIGD `≈9.58e-4`). MATLAB `MPDMP4.PF()` is `CalObj([50,40])`, one point. ZM26 Python `mean_igd` uses sampled party triangle fronts. A population collapsed to the common vertex has large IGD to a triangle PF and tiny IGD to that single point.

Optional MATLAB `test_12_native_runs` would confirm MATLAB also sits on `(50,40)`. Component tests already show the search operators match.

## Remaining items (not disproved)

1. Production MPDMP mutation uses `Site = rand < pro_m` (`0.5`). MATLAB `GA.m` uses `proM/D` (`0.25` at D=2). Test 06 compared the MATLAB-rate operator and it matched. The production-rate difference is real but did not prevent collapse to `(50,40)`.
2. MATLAB `CrowdingDistance` can still divide by zero; this matrix did not trigger it.
3. OptMPNDS2 / OptMPNDS3 were not the subject of Tests 04/07. Fix `nd_sort` before trusting PLNDS.

## Next

1. Do **not** rerun the full 18×4×30 ZM26 experiment yet.
2. Fix Python `nd_sort` stop condition (`assigned < n_sort`) and drop the `mpnds` leftover dump; re-run Test 02.
3. Align `meanIGD` for MPDMP1–12 with the MATLAB reference actually used (`Metrics/IGD.m` + problem `PF()`), or document that ZM26 party-triangle IGD is a different metric.
4. Optionally run MATLAB `test_12_native_runs` to confirm native populations also sit on `(50,40)`.
5. Only then repeat the audit for OptMPNDS2 / OptMPNDS3.

---

## Post-fix addendum (2026-10-22)

This report is the original audit. Production code **was** later changed in `experiments/zm26_reproduction/` only (`src/fairmoo_benchmarks/` untouched).

| Item | After the fix |
|---|---|
| Test 02 `nd_sort` / `mpnds` / `plnds` | integer exact match (`tests/test_nd_sort_duplicates.py`) |
| Production mutation | MATLAB `Site = rand < proM/D` (`settings.MPDMP["mutation_as_expectation"]=True`) |
| Crowding entropy | MATLAB NaN/Inf/finite masks (`tests/test_crowding_entropy_matlab.py`) |
| Official MPDMP score | `zm26_meanIGD`; `party_pf_meanIGD` kept |
| Full 18×4×30 rerun | **not** required; see `REPRODUCTION_REPORT.md` |

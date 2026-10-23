# OptMPNDS3 focused diagnostic (after crowding-entropy fix)

| Component | MATLAB | Python after fix | Status |
|---|---|---|---|
| Crowding entropy NaN/Inf | `Public/CrowdingEntropy.m` unguarded `/` and `log2` | `operators.crowding_entropy` IEEE-faithful | **PASS** vs `test_03_crowding.csv` (NaN/Inf/finite masks + finite values) |
| One-by-one last-front removal | `OptMPNDS3/EnvironmentalSelection.m` | `mode="optmpnds3"` loop | **PASS** Test 09 removal sequence (pre-fix; still valid) |
| `unique(objs,'rows')` | sorted unique, first index | `np.unique(..., return_index=True)` | **PASS** Test 08 |
| JADE2 one-step | shared indices | `test_13_jade2` | **PASS** |
| PFt init (`getPF`) | NSGA-II first two DMs, FEI=10000, `GA` `proM/D` | `_party_nsga2` now `mutation_as_expectation=True` | aligned with GA.m; not re-compared with a full MATLAB `getPF` dump |
| Archive / μF / μCR | She JADE2 | existing port (one-step mutation already matched) | no rewrite without new evidence |

Remaining OptMPNDS3 risk is stochastic PFt initialization quality, not the entropy formula. JADE2 one-step and entropy NaN/Inf now match; those working pieces were not rewritten.

## 5-seed / rescore status

| Problem | n | Paper meanIGD | Python zm26 | rel. diff | Scale match? |
|---|---:|---:|---:|---:|---|
| MPDMP4 | 5 | 0.0133 | 0.0644 | 3.84 | same 1e-2 order, high variance |
| MPDMP1 | 5 | 0.0447 | 2.96 | 65 | **no** |
| MPDMP6 | 30 | 0.0838 | 1.62 | 18 | **no** |
| MPDMP8 | 30 | 2.25 | 16.71 | 6.43 | **no** |

**Status: PARTIAL.** Component tests PASS; Table III numbers do not. This is a residual search-quality gap, not the original ~19 vs `1e-3` metric error.

Do **not** retune `N` / `FE` / `p` / `c` / `FEI` to chase Table III. A later focused PFt-init comparison can be scheduled; a full 18×30 MPDMP rerun is not justified yet.

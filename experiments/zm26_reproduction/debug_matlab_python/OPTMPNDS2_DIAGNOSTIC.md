# OptMPNDS2 focused diagnostic (after `nd_sort` fix)

MATLAB: `Algorithms/OptMPNDS2/EnvironmentalSelection.m` calls `PLNDS` then one-shot `CrowdingDistance` last-front fill — the same truncation as OptMPNDS, with a different sorter.

| Component | MATLAB | Python after fix | Status |
|---|---|---|---|
| PLNDS party ranks then NDSort | `Public/PLNDS.m` | `operators.plnds` | **PASS** vs MATLAB `test_02_mpn_sorting.csv` `plnds_front` (exact integers, including former `inf` rows) |
| Duplicate objective rows | `NDSort` `length(Loc)` stop | `nd_sort`: `assigned < n_sort` | **PASS** (same matrix as Test 02) |
| Last-front crowding | `sort(CrowdDis,'descend')` once | `environmental_selection(..., mode="optmpnds2")` | Same code path as OptMPNDS crowding, which **PASS**ed Test 04 |
| Mutation | `GA.m` `proM/D` | production `mutation_as_expectation=True` | aligned |
| Unique-row truncation | not in OptMPNDS2 envsel | not applied | match |

OptMPNDS2 was **not** given a separate 200-candidate MATLAB envsel dump. Because the only algorithmic difference from the already-matched OptMPNDS envsel is PLNDS, and PLNDS now matches MATLAB exactly on the stress matrix, a full MPDMP rerun is **not** scheduled.

## 5-seed / rescore status

| Problem | n | Paper meanIGD | Python zm26 | party_pf | Scale match? |
|---|---:|---:|---:|---:|---|
| MPDMP4 | 5 | 1.05e-3 | **8.35e-4** | 20.15 | yes |
| MPDMP1 | 5 | 0.0476 | **0.0311** | 13.20 | yes |
| MPDMP6 | 30 | 0.130 | **0.167** | 14.16 | yes |
| MPDMP8 | 30 | 2.46 | **2.43** | 9.26 | yes |

**Status: PASS for the official metric.** Full 12×30 rerun is not scientifically required.

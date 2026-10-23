# OptMPNDS3 source mapping

She 2023 tree: `benchmarks_python/sources/mpdmp_2023/2022SheOptMPNDS3/`
Python: `experiments/zm26_reproduction/algorithms/optmpnds3.py` + `operators.py`

This mapping is from reading the MATLAB source. Differences listed here are **hypotheses to test**, not confirmed root causes.

| MATLAB file/function | Python file/function | Role | Notes to test |
|---|---|---|---|
| `Algorithms/OptMPNDS3/OptMPNDS3.m` | `algorithms/optmpnds3.py` `OptMPNDS3.run` | Main loop | PFt concat → envsel → JADE2 while `evaluated < budget` |
| `OptMPNDS3/getPF.m` | `_party_nsga2` called twice | PF-based init / PFt | MATLAB: `Global.N=100`, NSGA-II on `DM{1}` until `evaluated<10000`, then `DM{2}` until `<20000`. Returns **front 1 only**. Python: 10000 local evals per first two DMs, return `front==1`. |
| `GLOBAL.Initialization` / `PROBLEM.Init` | `operators.random_population` | Random start of each party NSGA-II | `unifrnd` vs `rng.uniform`. Do not compare RNG streams across languages. |
| `EnvironmentalSelection1.m` | `_party_nsga2` body | Party NSGA-II envsel | MATLAB: `NDSort` + **CrowdingDistance** (one-shot last front). Python: `nd_sort` + `crowding_distance` (after a leftover entropy line that is overwritten). |
| `Public/GA.m` `Site = rand < proM/D` | `sbx_pm(..., mutation_as_expectation=True)` | Party NSGA-II variation | Production MPDMP now matches `proM/D`. |
| `OptMPNDS3.m` `Population = [PF1, PF2]` | `np.vstack(parts_x)` | Initial population construction | Size = \|front1 DM1\| + \|front1 DM2\|, **not** `Global.N`. |
| `EnvironmentalSelection(Population, length(Population), DM)` | `environmental_selection(..., n_survive=X.shape[0], mode="optmpnds3")` | Rank/entropy, no truncation | Then main loop truncates to `Global.N`. |
| `Archive = []` | `archive_x` empty `(0, D)` | Archive initialization | Both empty at generation 0. |
| `Public/getBestIndividual.m` | `_pbest` | p-best | MATLAB: walk fronts until `ceil(N*0.05)` then `randi`, pick crowding-rank on that front. Python: `lexsort((-crowd, front))` then `k ~ U{1..ceil(N*p)}`. **Must compare on shared k.** |
| `makedist Normal/truncate` CR; `tLocationScale` Cauchy F | `rng.normal`; `standard_cauchy` | F / CR sampling | Same formulas; streams not shared unless diagnostic wrapper. |
| `Parent1` `while Parent1 == i`; `Parent2` `while Parent2 == Parent1` | `i1 != i` only | Parent selection | Python does **not** retry `Parent2 == Parent1`. |
| `x + F*(Pbest-x) + F*(Parent2-Parent1)` | same | JADE2 mutation | One-step diagnostic already PASS with shared indices. |
| binomial `j_rand` / `rand < CR` | same | Crossover | PASS in previous one-step test. |
| `INDIVIDUAL` clips to `[lower,upper]` | `np.clip` | Bounds | PASS previously. |
| `Public/dominated.m` | `_mp_dominates` | MP dominance | Party `NDSort` then `NDSort` on rank matrix; child dominates if `front(2)==2`. |
| `updateArchive` nearest-dec replace at cap `2*Global.N` | `_update_archive` | Archive during parent-child | Same nearest-neighbor rule. |
| `updateArchive(Archive, setdiff(Offsprings, Population), 2N)` | **not implemented** | Archive after envsel | MATLAB adds **discarded survivors of the JADE pool**. Python does not. |
| `Population.adds` → `S_CR`, `S_F` (drop zeros) then `mu` update | `s_cr`/`s_f` collected in the dominance branch **before** envsel | F / CR adaptation | MATLAB uses **surviving** extras. Python uses dominance-event CR/F, including individuals later discarded, and skips the parent-dominates-child case. |
| `mean_Lehmer = sum(F.^2)/sum(F)` | `sum(arr**2)/sum(arr)` | μF update | Formula matches; the **set** of F may not. |
| `c = 0.05` | `self.c = 0.05` | Adaptation rate | Paper §5.1. |
| `Public/PLNDS.m` | `operators.plnds` | Sorter in envsel | Test 02 integers now match. |
| `Public/CrowdingEntropy.m` | `operators.crowding_entropy` | Diversity | NaN/Inf/finite PASS. |
| `OptMPNDS3/EnvironmentalSelection.m` | `environmental_selection(mode="optmpnds3")` | Unique rows, PLNDS, one-by-one entropy removal | Unique + removal sequence PASS (Tests 08/09). |
| `unique(objs,'rows')` then `Population(loc)` | `np.unique(..., return_index=True)` | Duplicate removal | PASS. |
| `GLOBAL.NotTermination` / `evaluated < evaluation` | `evaluated < evaluation_budget` | Termination | getPF’s 20000 evals count toward the 80000 budget in both. |
| `INDIVIDUAL(dec, [CR_i, F_i])` | Python stores CR/F in arrays, not on individuals | Extra parameters | MATLAB can recover CR/F of a surviving parent from a previous generation. Python does not persist extras on individuals. |

## Initialization geometry (expected, both languages)

`getPF` optimizes **each of the first two DMs separately**. For MPDMP1 that is the two diagonals (A–C and B–D), **not** the common PS `(50,50)`. Concatenating those fronts is expected to start **on the party lines**. Table III `zm26_meanIGD` is She `IGD.m` against `PF()=[20√2]*4` (the intersection image), so a two-line population is a **poor** official IGD even if each party PF is well approximated. Convergence to the intersection must happen in the JADE2 loop.

## Confirmed non-causes (previous audit)

- MPDMP evaluation
- crowding entropy formula
- unique-row envsel
- one-by-one entropy removal
- JADE2 **mutation formula** on shared indices
- `nd_sort` / PLNDS ranks after the duplicate-row fix
- `proM/D` in party NSGA-II variation

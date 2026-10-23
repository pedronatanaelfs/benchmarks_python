# OptMPNDS3 MATLAB ↔ Python diagnostic

Isolated audit of the remaining Table III gap (OptMPNDS3). Does **not** modify `src/fairmoo_benchmarks/` or OptAll / OptMPNDS / OptMPNDS2.

Primary problem: **MPDMP1**. Confirm on **MPDMP4**, then MPDMP6/8.

**Root cause (confirmed):** Python truncated the last JADE generation to the leftover FE budget, then envsel replaced N=200 with ~16 individuals. MATLAB finishes that generation and only stops at the next while-header. After the fix, 5-seed `zm26_meanIGD` matches Table III scale on MPDMP1/4/6/8. PFt initialization is **not** the collapse. See `OPTMPNDS3_ROOT_CAUSE_REPORT.md`.

## What Python already did

From `benchmarks_python` with `fairmoo-benchmarks` active:

```bash
python -m experiments.zm26_reproduction.debug_optmpnds3.python.run_all_python
```

Optional full native 5-run (slow):

```bash
python -m experiments.zm26_reproduction.debug_optmpnds3.python.run_all_python --native
```

## What you do in MATLAB

1. `cd` to `debug_optmpnds3/matlab`
2. Run:

```matlab
run_all_optmpnds3_diagnostics
```

`getPF` for MPDMP1 and MPDMP4 uses 20000 evaluations each (minutes). Native 5-run is **off** by default:

```matlab
run_all_optmpnds3_diagnostics(true)
```

3. Copy `matlab_outputs/` back if MATLAB ran elsewhere.
4. From `debug_optmpnds3/`:

```bash
python compare_optmpnds3_outputs.py
```

That writes `OPTMPNDS3_ROOT_CAUSE_REPORT.md` and `comparisons/comparison_summary.csv`.

## Do not compare `rng(1)` to `np.random.seed(1)`

Shared arrays live in `shared_inputs/`. Native PFt / 5-run tests are **scale and region** comparisons only.

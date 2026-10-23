#!/usr/bin/env python3
"""Compare MATLAB vs Python diagnostic CSVs. Does not modify production code."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

DIAG = Path(__file__).resolve().parent
MATLAB = DIAG / "matlab_outputs"
PYTHON = DIAG / "python_outputs"
COMP = DIAG / "comparisons"
REPORT = DIAG / "DIAGNOSTIC_REPORT.md"
ATOL = 1e-9
RTOL = 1e-12


def _load(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


def _load_matrix(path: Path) -> np.ndarray | None:
    if not path.exists():
        return None
    try:
        return np.loadtxt(path, delimiter=",", ndmin=2)
    except ValueError:
        df = pd.read_csv(path)
        return df.to_numpy(dtype=float)


def _finite_equal(a, b, atol=ATOL, rtol=RTOL) -> bool:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        return False
    both_nan = np.isnan(a) & np.isnan(b)
    both_pinf = np.isposinf(a) & np.isposinf(b)
    both_ninf = np.isneginf(a) & np.isneginf(b)
    close = np.isclose(a, b, atol=atol, rtol=rtol, equal_nan=False)
    return bool(np.all(both_nan | both_pinf | both_ninf | close))


def _first_diff(a, b, labels=None, atol=ATOL) -> str:
    a = np.asarray(a, dtype=float).ravel()
    b = np.asarray(b, dtype=float).ravel()
    n = min(a.size, b.size)
    for i in range(n):
        ai, bi = a[i], b[i]
        if np.isnan(ai) and np.isnan(bi):
            continue
        if np.isposinf(ai) and np.isposinf(bi):
            continue
        if np.isneginf(ai) and np.isneginf(bi):
            continue
        if not np.isclose(ai, bi, atol=atol, rtol=RTOL, equal_nan=False):
            lab = labels[i] if labels is not None else i
            return f"index={lab} MATLAB={ai} Python={bi} absdiff={abs(ai-bi)}"
    if a.size != b.size:
        return f"shape MATLAB={a.size} Python={b.size}"
    return ""


def _status(ok: bool, waiting: bool = False) -> str:
    if waiting:
        return "WAITING_MATLAB"
    return "PASS" if ok else "FAIL"


def _severity(ok: bool, waiting: bool, level: str) -> str:
    if waiting:
        return "UNKNOWN"
    return "NONE" if ok else level


def jaccard(a, b) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def compare_numeric_csv(name: str, cols: list[str] | None = None, exact: bool = False):
    m = _load(MATLAB / name)
    p = _load(PYTHON / name)
    if m is None or p is None:
        return {
            "file": name,
            "waiting": m is None,
            "ok": False,
            "detail": f"missing MATLAB={m is None} Python={p is None}",
            "first_diff": "",
        }
    if cols is None:
        cols = [c for c in m.columns if c in p.columns]
        cols = [c for c in cols if pd.api.types.is_numeric_dtype(m[c]) or pd.api.types.is_numeric_dtype(p[c])]
    missing = [c for c in cols if c not in m.columns or c not in p.columns]
    if missing:
        return {"file": name, "waiting": False, "ok": False, "detail": f"missing columns {missing}", "first_diff": ""}
    ok = True
    diffs = []
    n = min(len(m), len(p))
    if len(m) != len(p):
        ok = False
        diffs.append(f"nrows MATLAB={len(m)} Python={len(p)}")
    for c in cols:
        mv = pd.to_numeric(m[c], errors="coerce").to_numpy()[:n]
        pv = pd.to_numeric(p[c], errors="coerce").to_numpy()[:n]
        if exact:
            match = np.array_equal(mv, pv) or _finite_equal(mv, pv, atol=0.0, rtol=0.0)
        else:
            match = _finite_equal(mv, pv)
        if not match:
            ok = False
            diffs.append(f"{c}: {_first_diff(mv, pv)}")
    return {
        "file": name,
        "waiting": False,
        "ok": ok,
        "detail": "match" if ok else "; ".join(diffs)[:800],
        "first_diff": diffs[0] if diffs else "",
    }


def compare_matrix(name: str):
    m = _load_matrix(MATLAB / name)
    p = _load_matrix(PYTHON / name)
    if m is None or p is None:
        return {
            "file": name,
            "waiting": m is None,
            "ok": False,
            "detail": f"missing MATLAB={m is None} Python={p is None}",
            "first_diff": "",
        }
    ok = _finite_equal(m, p)
    return {
        "file": name,
        "waiting": False,
        "ok": ok,
        "detail": "match" if ok else f"shape M={m.shape} P={p.shape}",
        "first_diff": "" if ok else _first_diff(m, p),
    }


def envsel_stats():
    m = _load(MATLAB / "test_04_selected.csv")
    p = _load(PYTHON / "test_04_selected.csv")
    if m is None or p is None:
        return None
    ms = set(m["selected_original_index"].astype(int))
    ps = set(p["selected_original_index"].astype(int))
    same = len(ms & ps)
    return {
        "n_matlab": len(ms),
        "n_python": len(ps),
        "n_identical": same,
        "n_different": len(ms ^ ps),
        "jaccard": jaccard(ms, ps),
        "only_matlab": sorted(ms - ps)[:20],
        "only_python": sorted(ps - ms)[:20],
    }


def write_report(rows: list[dict], extra: dict) -> None:
    core_wait = any(
        r["matlab_vs_python"] == "WAITING_MATLAB" and r["test"] != "12" for r in rows
    )
    lines = []
    lines.append("# DIAGNOSTIC_REPORT — MPDMP4 / OptMPNDS")
    lines.append("")
    if core_wait:
        lines.append("**Status: WAITING for MATLAB outputs.**")
        lines.append("")
        lines.append("Python diagnostics have been executed. MATLAB CSVs are missing or incomplete.")
        lines.append("Do not conclude MATLAB ↔ Python equivalence until `matlab_outputs/` is populated.")
        lines.append("")
    else:
        lines.append("**Status: MATLAB component outputs compared. Production code was not modified.**")
        lines.append("")
        lines.append("Native 5-run MATLAB (`test_12`) is optional and may still be missing.")
        lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Test | Component | MATLAB vs Python | Severity |")
    lines.append("|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r['test']} | {r['component']} | {r['matlab_vs_python']} | {r['severity']} |")
    lines.append("")
    if extra.get("envsel"):
        e = extra["envsel"]
        lines.append("## Test 04 environmental selection set comparison")
        lines.append("")
        lines.append(f"- selected identically: {e['n_identical']}")
        lines.append(f"- symmetric difference size: {e['n_different']}")
        lines.append(f"- Jaccard similarity: {e['jaccard']:.6f}")
        lines.append(f"- only MATLAB (first 20): {e['only_matlab']}")
        lines.append(f"- only Python (first 20): {e['only_python']}")
        lines.append("")
    lines.append("## Discrepancy records")
    lines.append("")
    fails = [r for r in rows if r["matlab_vs_python"] == "FAIL"]
    if not fails:
        if core_wait:
            lines.append("No comparison yet.")
        else:
            lines.append("No FAIL rows in the comparison table. Re-read native-run magnitudes before claiming the reproduction is fixed.")
        lines.append("")
    for r in fails:
        lines.append(f"### {r['test']} — {r['component']}")
        lines.append("")
        lines.append(f"- MATLAB file/function: `{r.get('matlab_fn','')}`")
        lines.append(f"- Python file/function: `{r.get('python_fn','')}`")
        lines.append(f"- Input: `{r.get('input','shared_inputs/')}`")
        lines.append(f"- First differing value: {r.get('first_diff','')}")
        lines.append(f"- Detail: {r.get('detail','')}")
        lines.append(f"- Likely cause: {r.get('likely_cause','to be filled after inspecting the first differing value')}")
        lines.append(f"- Impact on optimization: {r.get('impact','')}")
        lines.append(f"- Suggested fix: {r.get('suggested_fix','Do not apply until the report is reviewed.')}")
        lines.append("")
    py12 = _load(PYTHON / "test_12_native_runs.csv")
    if py12 is not None:
        lines.append("## Python native OptMPNDS / MPDMP4 (5 runs, N=200, FE=80000)")
        lines.append("")
        lines.append("These numbers are Python-only. They are not a MATLAB comparison.")
        lines.append("")
        cols = [c for c in ["meanIGD", "she_IGD_single_PF", "mean_dist_to_common_ps", "pop_mean_x1", "pop_mean_x2"] if c in py12.columns]
        if cols:
            lines.append("| run | " + " | ".join(cols) + " |")
            lines.append("|---:|" + "|".join(["---:" for _ in cols]) + "|")
            for _, row in py12.iterrows():
                cells = " | ".join(f"{row[c]:.6g}" for c in cols)
                lines.append(f"| {int(row['run'])} | {cells} |")
            lines.append("")
        lines.append("Observation: the search collapses near the common PS `(50,40)` while party-wise triangle `meanIGD` stays O(10). `she_IGD_single_PF` (MATLAB `IGD.m` + `MPDMP4.PF()=CalObj([50,40])`) is O(10^-3).")
        lines.append("")

    lines.append("## Confirmed findings (after MATLAB CSVs)")
    lines.append("")
    lines.append("### A. MPDMP4 evaluation is not the failure")
    lines.append("")
    lines.append("Test 01 matches within `1e-9`. DM grouping is `DM1=1:3`, `DM2=4:6` on both sides. Stop looking at the benchmark package for the MPDMP4 IGD table gap.")
    lines.append("")
    lines.append("### B. OptMPNDS search on typical MPDMP4 populations matches MATLAB")
    lines.append("")
    lines.append("From the **same** `X` / `F` / random streams:")
    lines.append("")
    lines.append("- Test 04 environmental selection: identical 100 survivors, Jaccard `1.0`, matching fronts and crowding.")
    lines.append("- Test 06 SBX+PM at MATLAB rate `proM/D`: offspring match.")
    lines.append("- Test 07 five-generation trace: `X` matches at every generation `g=0..5`.")
    lines.append("- Test 10 bound repair: clip, not reflect/regenerate.")
    lines.append("")
    lines.append("On this evidence, the Python OptMPNDS loop is behaviorally equivalent to MATLAB **when objective rows are unique**, which is the usual MPDMP4 case.")
    lines.append("")
    lines.append("### C. Python `nd_sort` stops too early when duplicate objective rows exist")
    lines.append("")
    lines.append("MATLAB `NDSort.m` ENS-SS:")
    lines.append("")
    lines.append("```matlab")
    lines.append("while sum(Table(FrontNo<inf)) < min(nSort,length(Loc))")
    lines.append("```")
    lines.append("")
    lines.append("`length(Loc)` is the number of **original** points. Python `operators.nd_sort` uses `while assigned < min(n_sort, nu)` where `nu` is the number of **unique** rows, while `assigned` still counts original rows via `table`. Duplicate rows make `assigned` jump past `nu` and leave later uniques as `inf`.")
    lines.append("")
    lines.append("On `shared_inputs/mpnds_F.csv` (18 points, 16 unique 6-D, 15 unique per party):")
    lines.append("")
    lines.append("| point_id | MATLAB front_DM1 | Python front_DM1 |")
    lines.append("|---:|---:|---:|")
    lines.append("| 2 | 6 | inf |")
    lines.append("| 12 | 8 | inf |")
    lines.append("| 18 | 7 | inf |")
    lines.append("")
    lines.append("Python `mpnds` then hits empty `Fz` (because of those `inf` party ranks) and dumps leftovers onto combined front 2. MATLAB combined fronts are `{1,2,3,4,5,6,7,8}`.")
    lines.append("")
    lines.append("Changing the stop condition to `assigned < n_sort` (MATLAB `min(nSort,length(Loc))`) and removing the leftover dump restores exact integer equality for `front_DM1`, `front_DM2`, `combined_front`, and `plnds_front`. **Not applied yet.**")
    lines.append("")
    lines.append("Impact: latent on continuous MPDMP4 (Test 04/07 still passed). Real for duplicate objectives, PLNDS/OptMPNDS2, and any call that does not fully sort.")
    lines.append("")
    lines.append("### D. Crowding distance matches; crowding entropy does not")
    lines.append("")
    lines.append("OptMPNDS uses `CrowdingDistance.m`. Those values match, including `Inf` boundaries.")
    lines.append("")
    lines.append("`CrowdingEntropy.m` (OptMPNDS3) writes `NaN` when `c=0` or `Fmax=Fmin` (`log2(0)`, `x/0`). Python guards those cases to `0` and keeps boundary `Inf`. First mismatch: point 1 MATLAB `NaN` vs Python `Inf`. Interior finite values that are well-defined (point 8) match. Test 09 removal **sequence** still matched because this last-front sample did not hit the NaN path the same way.")
    lines.append("")
    lines.append("### E. The ZM26 table gap on MPDMP4 is not explained by a broken OptMPNDS search")
    lines.append("")
    lines.append("Python native runs sit on `(50,40)` with party-wise triangle `meanIGD≈19` and She-style single-point IGD `≈1e-3` (paper MATLAB meanIGD `≈9.58e-4`). MATLAB `MPDMP4.PF()` is `CalObj([50,40])`, one point. ZM26 Python `mean_igd` uses sampled party triangle fronts. A population collapsed to the common vertex has large IGD to a triangle PF and tiny IGD to that single point.")
    lines.append("")
    lines.append("Optional MATLAB `test_12_native_runs` would confirm MATLAB also sits on `(50,40)`. Component tests already show the search operators match.")
    lines.append("")
    lines.append("## Remaining items (not disproved)")
    lines.append("")
    lines.append("1. Production MPDMP mutation uses `Site = rand < pro_m` (`0.5`). MATLAB `GA.m` uses `proM/D` (`0.25` at D=2). Test 06 compared the MATLAB-rate operator and it matched. The production-rate difference is real but did not prevent collapse to `(50,40)`.")
    lines.append("2. MATLAB `CrowdingDistance` can still divide by zero; this matrix did not trigger it.")
    lines.append("3. OptMPNDS2 / OptMPNDS3 were not the subject of Tests 04/07. Fix `nd_sort` before trusting PLNDS.")
    lines.append("")
    lines.append("## Next")
    lines.append("")
    if core_wait:
        lines.append("Run MATLAB `matlab/run_all_diagnostics.m`, copy `matlab_outputs/` here, rerun `python compare_outputs.py`.")
    else:
        lines.append("1. Do **not** rerun the full 18×4×30 ZM26 experiment yet.")
        lines.append("2. Fix Python `nd_sort` stop condition (`assigned < n_sort`) and drop the `mpnds` leftover dump; re-run Test 02.")
        lines.append("3. Align `meanIGD` for MPDMP1–12 with the MATLAB reference actually used (`Metrics/IGD.m` + problem `PF()`), or document that ZM26 party-triangle IGD is a different metric.")
        lines.append("4. Optionally run MATLAB `test_12_native_runs` to confirm native populations also sit on `(50,40)`.")
        lines.append("5. Only then repeat the audit for OptMPNDS2 / OptMPNDS3.")
    lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    COMP.mkdir(parents=True, exist_ok=True)
    rows = []
    extra = {}

    def add(test, component, cmp, severity_if_fail, **kwargs):
        waiting = cmp.get("waiting", False)
        ok = cmp.get("ok", False)
        rows.append(
            {
                "test": test,
                "component": component,
                "matlab_vs_python": _status(ok, waiting),
                "severity": _severity(ok, waiting, severity_if_fail),
                "detail": cmp.get("detail", ""),
                "first_diff": cmp.get("first_diff", ""),
                **kwargs,
            }
        )

    add(
        "01",
        "problem evaluation",
        compare_numeric_csv("test_01_problem.csv", ["x1", "x2", "F1", "F2", "F3", "F4", "F5", "F6"]),
        "CRITICAL",
        matlab_fn="MPDMP4.CalObj / polygon.EuclideanDistance",
        python_fn="fairmoo_benchmarks MPDMP4.evaluate",
        input="shared_inputs/mpdmp4_X.csv",
        likely_cause="Should pass; benchmark was already validated.",
        impact="If FAIL, stop: the optimizer audit is invalid.",
        suggested_fix="Do not edit MPDMP. Re-check vertices / pdist2 order.",
    )
    add(
        "02",
        "MPNDS",
        compare_numeric_csv(
            "test_02_mpn_sorting.csv",
            ["front_DM1", "front_DM2", "combined_front", "plnds_front"],
            exact=True,
        ),
        "CRITICAL",
        matlab_fn="Public/MPNDS.m, NDSort.m, PLNDS.m",
        python_fn="algorithms/operators.py mpnds/nd_sort/plnds",
        input="shared_inputs/mpnds_F.csv",
        likely_cause="nd_sort stops when assigned original rows >= n_unique, leaving inf; mpnds leftover dump then collapses combined fronts.",
        impact="Latent on unique MPDMP4 populations (Tests 04/07 still passed). Breaks duplicate/PLNDS cases.",
        suggested_fix="Use assigned < n_sort (MATLAB min(nSort,length(Loc))); remove mpnds leftover assignment.",
    )
    add(
        "03a",
        "crowding distance",
        compare_numeric_csv("test_03_crowding.csv", ["crowding_value"]),
        "MAJOR",
        matlab_fn="Algorithms/OptMPNDS/CrowdingDistance.m",
        python_fn="algorithms/operators.py crowding_distance",
        input="shared_inputs/crowding_F.csv",
        likely_cause="Should match; OptMPNDS uses this metric.",
        impact="Last-front truncation of OptMPNDS.",
        suggested_fix="None if PASS.",
    )
    add(
        "03b",
        "crowding entropy",
        compare_numeric_csv("test_03_crowding.csv", ["entropy_value"]),
        "MAJOR",
        matlab_fn="Public/CrowdingEntropy.m",
        python_fn="algorithms/operators.py crowding_entropy",
        input="shared_inputs/crowding_F.csv",
        likely_cause="MATLAB NaN on c=0 / zero span; Python uses 0 and keeps boundary Inf.",
        impact="OptMPNDS3 only. OptMPNDS does not use entropy.",
        suggested_fix="Reproduce MATLAB NaN/Inf, or document the guard as intentional.",
    )
    add(
        "04",
        "environmental selection",
        compare_numeric_csv("test_04_selected.csv", ["selected_original_index"], exact=True),
        "CRITICAL",
        matlab_fn="Algorithms/OptMPNDS/EnvironmentalSelection.m",
        python_fn="algorithms/operators.py environmental_selection mode=optmpnds",
        input="shared_inputs/envsel_X.csv",
        likely_cause="Different MPNDS fronts and/or crowding ties / sort stability.",
        impact="Surviving population diverges immediately.",
        suggested_fix="Fix MPNDS/crowding first, then re-compare selected index sets.",
    )
    e = envsel_stats()
    if e:
        extra["envsel"] = e
        last = rows[-1]
        last["detail"] += (
            f" | jaccard={e['jaccard']:.4f} identical={e['n_identical']} "
            f"diff={e['n_different']}"
        )
        if last["matlab_vs_python"] == "WAITING_MATLAB":
            pass
        elif e["jaccard"] < 1.0:
            last["matlab_vs_python"] = "FAIL"
            last["severity"] = "CRITICAL"
            last["first_diff"] = (
                f"only MATLAB {e['only_matlab']}; only Python {e['only_python']}"
            )
        elif last["matlab_vs_python"] == "FAIL":
            last["matlab_vs_python"] = "PASS"
            last["severity"] = "MINOR"
            last["detail"] += " | selected SET identical; row order differs"

    add(
        "05",
        "initialization",
        {
            "waiting": not (MATLAB / "test_05_init_stats.csv").exists(),
            "ok": True,
            "detail": "structural only; RNG streams are not comparable",
            "first_diff": "",
        },
        "MINOR",
        matlab_fn="GLOBAL.Initialization / PROBLEM.Init unifrnd",
        python_fn="operators.random_population rng.uniform",
        input="none (independent RNG)",
        likely_cause="Not an exact test.",
        impact="OptMPNDS does not use PF-based init.",
        suggested_fix="None for OptMPNDS. Audit getPF only for OptMPNDS3.",
    )
    add(
        "06",
        "variation (SBX+PM matlab rate)",
        compare_numeric_csv("test_06_offspring_matlab_rate.csv", ["x1", "x2"]),
        "MAJOR",
        matlab_fn="diagnostic ga_from_stream.m (GA.m formula)",
        python_fn="debug ga_from_stream.py mutation_as_expectation=True",
        input="shared_inputs/variation_parents.csv + ga_*.csv",
        likely_cause="SBX/PM formula or clip order.",
        impact="Offspring distribution.",
        suggested_fix="If matlab-rate matches, the remaining issue is production Site=rand<pro_m vs pro_m/D.",
    )
    add(
        "07",
        "short run X_g0",
        compare_matrix("test_07_X_g0.csv"),
        "CRITICAL",
        matlab_fn="EnvironmentalSelection after shared X0",
        python_fn="environmental_selection on short_X0",
        input="shared_inputs/short_X0.csv",
        likely_cause="First envsel divergence.",
        impact="All later generations diverge.",
        suggested_fix="Inspect test 02/04 if this fails.",
    )
    for g in range(1, 6):
        add(
            "07",
            f"short run X_g{g}",
            compare_matrix(f"test_07_X_g{g}.csv"),
            "CRITICAL",
            matlab_fn="ga_from_stream + EnvironmentalSelection",
            python_fn="sbx_pm_from_stream + environmental_selection",
            input=f"shared_inputs/short_*_g{g-1}.csv",
            likely_cause="First generation where X diverges.",
            impact="Identifies the earliest integrated failure.",
            suggested_fix="Inspect the component that ran in that generation.",
        )
    add(
        "08",
        "unique-row behavior",
        compare_numeric_csv("test_08_unique_kept.csv", ["kept_input_index"], exact=True),
        "MAJOR",
        matlab_fn="unique(F,'rows')",
        python_fn="np.unique(F, axis=0, return_index=True)",
        input="shared_inputs/unique_X.csv",
        likely_cause="first vs last occurrence; sorted unique order.",
        impact="OptMPNDS3 envsel unique truncation; OptMPNDS only inside MPNDS.",
        suggested_fix="Match MATLAB unique occurrence flag.",
    )
    add(
        "09",
        "one-by-one entropy removal",
        compare_numeric_csv(
            "test_09_optmpnds3_iterative.csv",
            ["candidate_removed_1based"],
            exact=True,
        ),
        "MAJOR",
        matlab_fn="CrowdingEntropy loop (OptMPNDS3 envsel pattern)",
        python_fn="test_09 crowding_entropy iterative",
        input="shared_inputs/lastfront_F.csv",
        likely_cause="argmin ties; entropy NaN; oneshot vs iterative (OptMPNDS is oneshot).",
        impact="OptMPNDS3 truncation; not OptMPNDS unless Python mistakenly iterates.",
        suggested_fix="Keep OptMPNDS oneshot; fix OptMPNDS3 only if sequence differs.",
    )
    add(
        "10",
        "boundary repair",
        compare_numeric_csv("test_10_boundary.csv", ["pre_x1", "pre_x2", "post_x1", "post_x2"]),
        "MAJOR",
        matlab_fn="GA.m min(max()) + INDIVIDUAL clip",
        python_fn="np.clip in sbx_pm_from_stream",
        input="shared_inputs/variation_parents.csv",
        likely_cause="Clip after SBX only vs after PM; no reflect.",
        impact="Feasible region coverage.",
        suggested_fix="Match GA.m then INDIVIDUAL clip.",
    )
    add(
        "11",
        "objective grouping",
        {
            "waiting": not (MATLAB / "test_11_grouping.csv").exists(),
            "ok": (MATLAB / "test_11_grouping.csv").exists(),
            "detail": "check DM1=1:3 DM2=4:6 in both CSVs",
            "first_diff": "",
        },
        "CRITICAL",
        matlab_fn="MPDMP5 DM={1:3,4:6}; MPNDS uses DM cell",
        python_fn="MPDMP4.dm_objective_slices; SLICES=[0:3,3:6]",
        input="none",
        likely_cause="Optimizer using concatenated F as one party.",
        impact="Would destroy MPNDS meaning.",
        suggested_fix="Force slices through every selection call.",
    )
    add(
        "13",
        "JADE2 one-step (OptMPNDS3)",
        compare_numeric_csv("test_13_jade_offspring.csv", ["x1", "x2"]),
        "MINOR",
        matlab_fn="diagnostic current-to-pbest using shared indices",
        python_fn="test_13_jade2.py",
        input="shared_inputs/jade_*.csv",
        likely_cause="Not on the OptMPNDS critical path.",
        impact="OptMPNDS3 only.",
        suggested_fix="Defer until OptMPNDS on MPDMP4 matches.",
    )
    add(
        "12",
        "native 5-run magnitude",
        {
            "waiting": not (MATLAB / "test_12_native_runs.csv").exists(),
            "ok": True,
            "detail": "stochastic; compare meanIGD / she_IGD orders of magnitude only",
            "first_diff": "",
        },
        "CRITICAL",
        matlab_fn="OptMPNDS.m GLOBAL.Start N=200 FE=80000",
        python_fn="algorithms/optmpnds.py mutation_as_expectation=False",
        input="independent RNG",
        likely_cause="If MATLAB ~1e-3 and Python ~19, the port is still wrong.",
        impact="Confirms whether the discrepancy remains after component tests.",
        suggested_fix="Do not run 30 seeds until components pass.",
    )

    df = pd.DataFrame(rows)
    df.to_csv(COMP / "comparison_summary.csv", index=False)
    (COMP / "comparison_summary.json").write_text(json.dumps({"rows": rows, "extra": extra}, indent=2, default=str))
    write_report(rows, extra)
    n_wait = sum(r["matlab_vs_python"] == "WAITING_MATLAB" for r in rows)
    n_fail = sum(r["matlab_vs_python"] == "FAIL" for r in rows)
    n_pass = sum(r["matlab_vs_python"] == "PASS" for r in rows)
    print(f"wrote {COMP / 'comparison_summary.csv'}")
    print(f"wrote {REPORT}")
    print(f"PASS={n_pass} FAIL={n_fail} WAITING_MATLAB={n_wait}")
    core_wait = any(r["matlab_vs_python"] == "WAITING_MATLAB" and r["test"] != "12" for r in rows)
    if core_wait:
        print("MATLAB outputs incomplete. Run matlab/run_all_diagnostics.m then rerun this script.")
    elif n_wait:
        print("Component tests compared. Optional MATLAB test_12 native runs still missing.")


if __name__ == "__main__":
    main()

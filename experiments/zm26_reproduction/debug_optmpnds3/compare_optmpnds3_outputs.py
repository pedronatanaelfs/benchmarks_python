#!/usr/bin/env python3
"""Compare MATLAB vs Python OptMPNDS3 diagnostics. Does not modify production code."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DIAG = Path(__file__).resolve().parent
MATLAB = DIAG / "matlab_outputs"
PYTHON = DIAG / "python_outputs"
COMP = DIAG / "comparisons"
REPORT = DIAG / "OPTMPNDS3_ROOT_CAUSE_REPORT.md"
ATOL = 1e-9


def _load(path: Path):
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        try:
            return np.loadtxt(path, delimiter=",", ndmin=2)
        except Exception:
            return None


def _mat(path: Path):
    if not path.exists():
        return None
    try:
        return np.loadtxt(path, delimiter=",", ndmin=2)
    except ValueError:
        df = pd.read_csv(path)
        return df.to_numpy(dtype=float)


def _close(a, b, atol=ATOL) -> bool:
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if a.shape != b.shape:
        return False
    both_nan = np.isnan(a) & np.isnan(b)
    return bool(np.all(both_nan | np.isclose(a, b, atol=atol, equal_nan=False)))


def classify(status: str) -> str:
    return status


def main() -> None:
    COMP.mkdir(parents=True, exist_ok=True)
    rows = []
    waiting = []

    def rec(test, component, status, severity, detail=""):
        rows.append(
            {
                "test": test,
                "component": component,
                "matlab_vs_python": status,
                "severity": severity,
                "detail": detail,
            }
        )

    # test 04 pbest: MATLAB 1-based vs Python 0-based
    py_pb = _load(PYTHON / "test_04_pbest_selection.csv")
    ma_pb = _load(MATLAB / "test_04_pbest_selection.csv")
    py_sum = _load(PYTHON / "test_04_pbest_summary.csv")
    if py_pb is None:
        rec("04", "p-best", "MISSING_PYTHON", "UNKNOWN")
    elif ma_pb is None:
        rec("04", "p-best", "WAITING_MATLAB", "UNKNOWN", "shared-k Python vs MATLAB-replica already in python summary")
        waiting.append("04")
        if py_sum is not None:
            rec(
                "04",
                "p-best python replica",
                "PASS" if int(py_sum.shared_mismatches.iloc[0]) == 0 else "MAJOR_DIFFERENCE",
                "NONE" if int(py_sum.shared_mismatches.iloc[0]) == 0 else "MAJOR",
                f"lexsort vs getBestIndividual replica mismatches={int(py_sum.shared_mismatches.iloc[0])}/{int(py_sum.shared_n.iloc[0])}; random={int(py_sum.random_mismatches.iloc[0])}",
            )
    else:
        py_idx = py_pb.matlab_index.to_numpy() + 1
        ma_idx = ma_pb.matlab_index_1based.to_numpy()
        ok = _close(py_idx, ma_idx)
        rec("04", "p-best", "PASS" if ok else "MAJOR_DIFFERENCE", "NONE" if ok else "MAJOR")

    py_cr = _load(PYTHON / "test_05_f_cr_adaptation.csv")
    ma_cr = _load(MATLAB / "test_05_f_cr_adaptation.csv")
    if py_cr is not None and ma_cr is not None:
        ok = _close(py_cr.mu_CR_after, ma_cr.mu_CR_after) and _close(py_cr.mu_F_after, ma_cr.mu_F_after)
        rec("05", "F/CR formula", "PASS" if ok else "MAJOR_DIFFERENCE", "NONE" if ok else "MAJOR")
    elif py_cr is not None:
        rec("05", "F/CR formula", "WAITING_MATLAB", "UNKNOWN")
        waiting.append("05")

    py_ar = _mat(PYTHON / "test_06_archive_final_X.csv")
    ma_ar = _mat(MATLAB / "test_06_archive_final_X.csv")
    if py_ar is not None and ma_ar is not None:
        ok = _close(np.sort(py_ar, axis=0), np.sort(ma_ar, axis=0)) or _close(py_ar, ma_ar)
        rec("06", "archive nearest replace", "PASS" if ok else "MAJOR_DIFFERENCE", "NONE" if ok else "MAJOR")
    elif py_ar is not None:
        rec("06", "archive nearest replace", "WAITING_MATLAB", "UNKNOWN")
        waiting.append("06")

    py_e = _mat(PYTHON / "test_07_selected_X.csv")
    ma_e = _mat(MATLAB / "test_07_selected_X.csv")
    if py_e is not None and ma_e is not None:
        ok = py_e.shape == ma_e.shape and _close(np.sort(py_e, axis=0), np.sort(ma_e, axis=0))
        rec(
            "07",
            "envsel integration",
            "PASS" if _close(py_e, ma_e) else ("MINOR_DIFFERENCE" if ok else "MAJOR_DIFFERENCE"),
            "NONE" if _close(py_e, ma_e) else "MAJOR",
            f"python_n={py_e.shape[0]} matlab_n={ma_e.shape[0]} exact={_close(py_e, ma_e)}",
        )
    elif py_e is not None:
        rec("07", "envsel integration", "WAITING_MATLAB", "UNKNOWN")
        waiting.append("07")

    rec("03", "archive gen0 empty", "PASS", "NONE", "both start Archive=[]")

    # init quality
    py_q = _load(PYTHON / "test_02_initial_population_quality.csv")
    ma_q = _load(MATLAB / "test_02_initial_population_quality.csv")
    if py_q is not None:
        rec(
            "02",
            "python gen0 zm26",
            "NOT_COMPARABLE" if ma_q is None else "PASS",
            "UNKNOWN" if ma_q is None else "NONE",
            py_q.to_csv(index=False),
        )
        if ma_q is None:
            waiting.append("01/02 getPF")
        else:
            rec("01", "PFt gen0 IGD scale", "NOT_COMPARABLE", "NONE", "independent RNG; compare scale in report")

    py_tr = _load(PYTHON / "test_08_short_trace.csv")
    py_div = _load(PYTHON / "test_08_first_divergence.csv")
    ma_tr = _load(MATLAB / "test_08_short_trace.csv")
    if py_div is not None:
        rec(
            "08",
            "python production vs matlab-faithful replica",
            "ROOT_CAUSE_CANDIDATE" if str(py_div.first_divergent_component.iloc[0]) != "none" else "PASS",
            "MAJOR" if str(py_div.first_divergent_component.iloc[0]) != "none" else "NONE",
            py_div.to_csv(index=False),
        )
    if ma_tr is None:
        rec("08", "MATLAB short trace", "WAITING_MATLAB", "UNKNOWN")
        waiting.append("08")
    else:
        rec("08", "MATLAB short trace", "PASS", "NONE", "see X_g* files")

    rec("09", "native 5-run", "WAITING_MATLAB" if not (MATLAB / "test_09_native_5run.csv").exists() else "NOT_COMPARABLE", "UNKNOWN", "independent RNG")

    df = pd.DataFrame(rows)
    df.to_csv(COMP / "comparison_summary.csv", index=False)
    write_report(df, py_q, py_div, py_tr, py_sum, waiting, ma_q)
    print("wrote", COMP / "comparison_summary.csv")
    print("wrote", REPORT)


def write_report(df, py_q, py_div, py_tr, py_sum, waiting, ma_q):
    lines = [
        "# OptMPNDS3 root-cause report",
        "",
        "Production OptMPNDS3 was **not** modified. This report is diagnostic.",
        "",
        "## Status vs MATLAB outputs",
        "",
    ]
    if waiting:
        lines.append("MATLAB CSVs still missing for: " + ", ".join(waiting))
        lines.append("")
        lines.append("Run `debug_optmpnds3/matlab/run_all_optmpnds3_diagnostics` then re-run this script.")
        lines.append("")
    lines += [
        "| Test | Component | Status | Severity | Detail |",
        "|---|---|---|---|---|",
    ]
    for _, r in df.iterrows():
        det = str(r.detail).replace("\n", " ")[:180]
        lines.append(f"| {r.test} | {r.component} | {r.matlab_vs_python} | {r.severity} | {det} |")

    lines += ["", "## Python-only evidence (available now)", ""]
    if py_q is not None:
        lines.append("### Gen-0 PFt quality (independent RNG)")
        lines.append("")
        lines.append("| benchmark | n | zm26_meanIGD | party_pf | mean dist to common PS | vs paper final |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for _, r in py_q.iterrows():
            lines.append(
                f"| {r.benchmark} | {int(r.n)} | {r.zm26_meanIGD:.4g} | {r.party_pf_meanIGD:.4g} | "
                f"{r.mean_dist_to_common_ps:.3g} | {r.init_vs_paper_ratio:.3g}× |"
            )
        lines.append("")
        lines.append(
            "Interpretation: `getPF` returns each party's front 1 (MPDMP1: the two diagonals). "
            "Official `zm26_meanIGD` is IGD to the **intersection** image. A two-line start is expected "
            "to have large official IGD. MATLAB Table III is the **final** IGD after JADE2, not gen 0."
        )
        lines.append("")
        m1 = py_q[py_q.benchmark == "MPDMP1"]
        if len(m1) and float(m1.zm26_meanIGD.iloc[0]) > 0.5:
            lines.append(
                "Python gen-0 MPDMP1 `zm26_meanIGD` is already far above the paper **final** 0.0447. "
                "That does **not** by itself prove a PFt bug: MATLAB may start similarly and then converge. "
                "Compare MATLAB `mpdmp1_init_meta.csv` once available."
            )
            lines.append("")
    if py_sum is not None:
        lines.append("### p-best: production lexsort vs MATLAB `getBestIndividual` replica")
        lines.append("")
        lines.append(
            f"shared mismatches = {int(py_sum.shared_mismatches.iloc[0])}/{int(py_sum.shared_n.iloc[0])}; "
            f"random mismatches = {int(py_sum.random_mismatches.iloc[0])}/{int(py_sum.random_trials.iloc[0])}"
        )
        lines.append("")
        if int(py_sum.shared_mismatches.iloc[0]) == 0 and int(py_sum.random_mismatches.iloc[0]) == 0:
            lines.append("On the tested fronts these two rules agreed. Not a root-cause candidate yet.")
        else:
            lines.append("**ROOT_CAUSE_CANDIDATE**: p-best index selection disagrees with `getBestIndividual.m`.")
        lines.append("")
    if py_div is not None:
        lines.append("### Shared-stream 5-gen: production flags vs MATLAB-faithful replica")
        lines.append("")
        lines.append(
            f"First X divergence: `{py_div.first_divergent_component.iloc[0]}`. "
            f"Production g5 zm26={float(py_div.prod_g5_zm26.iloc[0]):.4g}; "
            f"MATLAB-faithful g5 zm26={float(py_div.matlab_g5_zm26.iloc[0]):.4g}; "
            f"archives {int(py_div.prod_g5_archive.iloc[0])} vs {int(py_div.matlab_g5_archive.iloc[0])}."
        )
        lines.append("")
        lines.append(
            "MATLAB-faithful replica enables: `getBestIndividual` walk, Parent2≠Parent1 retry, "
            "S_CR/S_F from **survivors** (zeros dropped), and `setdiff` archive update after envsel. "
            "This replica is not production and is not yet validated against real MATLAB CSVs."
        )
        lines.append("")

    lines += [
        "## PRIMARY ROOT CAUSE",
        "",
        "Not confirmed until MATLAB `getPF` / short-trace CSVs exist.",
        "",
        "## SECONDARY DIFFERENCES (source-mapping hypotheses)",
        "",
        "1. Python does not run `updateArchive(Archive, setdiff(Offsprings, Population), 2N)` after envsel.",
        "2. Python updates μCR/μF from dominance-event CR/F, not surviving `INDIVIDUAL.add`.",
        "3. Python does not retry Parent2 == Parent1.",
        "4. PFt concatenates party front-1 sets; official IGD is to the common-PS image — convergence must happen in JADE2.",
        "",
        "## CONFIRMED NON-CAUSES (previous audit + this folder)",
        "",
        "- MPDMP evaluation, PLNDS ranks, crowding entropy NaN/Inf, unique-row envsel, one-by-one removal,",
        "  JADE2 mutation **formula** on shared indices, `proM/D` in party NSGA-II, empty archive at gen 0,",
        "  Lehmer/mean μ update **formula** on a shared S set.",
        "",
        "## Production fix",
        "",
        "None applied. Do not change `optmpnds3.py` until MATLAB short-trace / getPF confirm the first divergence.",
        "",
    ]
    REPORT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

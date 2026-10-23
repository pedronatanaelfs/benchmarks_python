"""Rescore saved MPDMP populations with zm26_meanIGD (She IGD.m + MATLAB PF).

Existing 30-run CSVs stored party-wise geometric meanIGD as ``meanIGD``.
Final populations were only saved for FIGURE_PROBLEMS. Missing F cannot be
reconstructed from the old scalar, so those rows keep corrected=NaN until a
new run with saved F is available.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from experiments.zm26_reproduction import ROOT
from experiments.zm26_reproduction.config.paper_values import TABLE_III
from experiments.zm26_reproduction.metrics.matlab_mpdmp_pf import matlab_problem_pf
from experiments.zm26_reproduction.metrics.she_igd import zm26_meanIGD
from experiments.zm26_reproduction.runners.jobs import POP_DIR
from experiments.zm26_reproduction.runners.problem_setup import load_problem

RAW = ROOT / "results" / "raw" / "results.csv"
VAL = ROOT / "results" / "validation" / "mpdmp_5seed.csv"
OUT = ROOT / "results" / "paper_comparison" / "mpdmp_igd_rescored.csv"
SUM = ROOT / "results" / "paper_comparison" / "mpdmp_igd_rescored_summary.csv"

ALGS = ["OptAll", "OptMPNDS", "OptMPNDS2", "OptMPNDS3"]
BENCH = [f"MPDMP{i}" for i in range(1, 13)]


def _npz_lookup():
    """30-run figure-problem populations only.

    Validation ``.npz`` files reuse the same stem as campaign runs 1–5 but
    are different searches (corrected mutation). Overlaying them onto the
    30-run rows would pair old ``meanIGD`` with new ``F``.
    """
    found = {}
    if POP_DIR.exists():
        for p in POP_DIR.glob("*.npz"):
            found[p.stem] = p
    return found


def main() -> None:
    raw = pd.read_csv(RAW)
    raw = raw[
        raw.benchmark.isin(BENCH)
        & raw.algorithm.isin(ALGS)
        & (raw.condition == "case1_no_concession")
    ].copy()
    npz = _npz_lookup()
    pf_cache = {}
    slices_cache = {}
    rows = []
    for _, rec in raw.iterrows():
        key = f"{rec.benchmark}_{rec.algorithm}_run{int(rec.run)}_seed{int(rec.seed)}"
        paper = TABLE_III.get(rec.benchmark, {}).get(rec.algorithm, {}).get("meanIGD", (np.nan, np.nan))
        corrected = np.nan
        source = "no_saved_population"
        path = npz.get(key)
        if path is not None:
            data = np.load(path)
            F = data["F"]
            name = rec.benchmark
            if name not in pf_cache:
                problem, _, slices = load_problem(name)
                pf_cache[name] = matlab_problem_pf(problem)
                slices_cache[name] = slices
            corrected = zm26_meanIGD(F, pf_cache[name], slices_cache[name])
            source = str(path.name)
        rows.append(
            {
                "benchmark": rec.benchmark,
                "algorithm": rec.algorithm,
                "run": int(rec.run),
                "seed": int(rec.seed),
                "old_python_meanIGD": float(rec.meanIGD),
                "corrected_zm26_meanIGD": corrected,
                "paper_meanIGD": paper[0],
                "population_source": source,
            }
        )
    # Merge 5-seed validation if present (new F, possibly new mutation setting)
    if VAL.exists():
        v = pd.read_csv(VAL)
        for _, rec in v.iterrows():
            rows.append(
                {
                    "benchmark": rec.benchmark,
                    "algorithm": rec.algorithm,
                    "run": int(rec.run),
                    "seed": int(rec.seed),
                    "old_python_meanIGD": float(rec.get("party_pf_meanIGD", rec.get("meanIGD", np.nan))),
                    "corrected_zm26_meanIGD": float(rec.get("zm26_meanIGD", np.nan)),
                    "paper_meanIGD": TABLE_III.get(rec.benchmark, {}).get(rec.algorithm, {}).get("meanIGD", (np.nan,))[0],
                    "population_source": "validation_5seed",
                }
            )
    df = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    summary = []
    for bench in BENCH:
        sub_b = df[df.benchmark == bench]
        archive = sub_b[sub_b.population_source != "validation_5seed"]
        paper_means = {a: TABLE_III[bench][a]["meanIGD"][0] for a in ALGS if a in TABLE_III[bench]}
        paper_stds = {a: TABLE_III[bench][a]["meanIGD"][1] for a in ALGS if a in TABLE_III[bench]}
        paper_rank = sorted(paper_means, key=lambda a: paper_means[a])
        corr_means = {}
        for alg in ALGS:
            g = sub_b[sub_b.algorithm == alg]
            c = g["corrected_zm26_meanIGD"].dropna()
            corr_means[alg] = float(c.mean()) if len(c) else np.nan
        ranked_corr = [a for a in ALGS if np.isfinite(corr_means.get(a, np.nan))]
        ranked_corr = sorted(ranked_corr, key=lambda a: corr_means[a])
        for alg in ALGS:
            g_old = archive[archive.algorithm == alg]
            g = sub_b[sub_b.algorithm == alg]
            old_m = float(g_old["old_python_meanIGD"].mean()) if len(g_old) else np.nan
            c = g["corrected_zm26_meanIGD"].dropna()
            cm = float(c.mean()) if len(c) else np.nan
            cs = float(c.std(ddof=1)) if len(c) > 1 else (0.0 if len(c) == 1 else np.nan)
            pm = paper_means.get(alg, np.nan)
            summary.append(
                {
                    "benchmark": bench,
                    "algorithm": alg,
                    "paper_mean": pm,
                    "paper_std": paper_stds.get(alg, np.nan),
                    "old_python_mean": old_m,
                    "corrected_python_mean": cm,
                    "corrected_python_std": cs,
                    "n_corrected": int(len(c)),
                    "absolute_difference": abs(cm - pm) if np.isfinite(cm) and np.isfinite(pm) else np.nan,
                    "relative_difference": abs(cm - pm) / (abs(pm) + 1e-12)
                    if np.isfinite(cm) and np.isfinite(pm)
                    else np.nan,
                    "ranking_paper": ",".join(paper_rank),
                    "ranking_corrected_python": ",".join(ranked_corr) if ranked_corr else "",
                    "ranking_match": bool(ranked_corr == paper_rank) if ranked_corr else False,
                }
            )
    pd.DataFrame(summary).to_csv(SUM, index=False)
    print(f"wrote {OUT}")
    print(f"wrote {SUM}")
    n_corr = int(df["corrected_zm26_meanIGD"].notna().sum())
    print(f"rows with corrected zm26_meanIGD: {n_corr}/{len(df)}")


if __name__ == "__main__":
    main()

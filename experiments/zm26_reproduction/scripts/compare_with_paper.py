from __future__ import annotations

import json

import numpy as np
import pandas as pd

from .. import ROOT
from ..config.paper_values import TABLE_II, TABLE_III, PAPER_RANKING_NOTES
from ..config.settings import NONCONSENSUS_BENCHMARKS

SUM = ROOT / "results" / "aggregated" / "summary.csv"
OUT = ROOT / "results" / "paper_comparison" / "paper_vs_python.csv"


def _best(df, bench, metric, higher_better):
    sub = df[(df.benchmark == bench) & (df.metric == metric) & (df.condition == "case1_no_concession")]
    if sub.empty:
        return None
    idx = sub["mean"].idxmax() if higher_better else sub["mean"].idxmin()
    return str(sub.loc[idx, "algorithm"])


def _level(abs_diff, rel_diff, rank_match, paper_mean):
    if paper_mean is None or np.isnan(paper_mean):
        return "NOT_COMPARABLE"
    if rank_match and (abs_diff <= 0.05 * (abs(paper_mean) + 1e-12) or abs_diff < 1e-3):
        return "EXACT"
    if rank_match and rel_diff < 0.5:
        return "CLOSE"
    if rank_match:
        return "QUALITATIVE"
    return "MISMATCH"


def main() -> None:
    summary = pd.read_csv(SUM)
    rows = []
    for bench, table, nash_key, higher_nash in [
        (TABLE_II, TABLE_II, "nash_score", True),
        (TABLE_III, TABLE_III, "log_nash", True),
    ]:
        pass
    for bench, table in TABLE_II.items():
        for alg, metrics in table.items():
            for metric, (mean, std) in metrics.items():
                py = summary[
                    (summary.benchmark == bench)
                    & (summary.algorithm == alg)
                    & (summary.condition == "case1_no_concession")
                    & (summary.metric == metric)
                ]
                py_mean = float(py["mean"].iloc[0]) if len(py) else np.nan
                py_std = float(py["std"].iloc[0]) if len(py) else np.nan
                abs_diff = abs(py_mean - mean) if np.isfinite(py_mean) else np.nan
                rel = abs_diff / (abs(mean) + 1e-12) if np.isfinite(abs_diff) else np.nan
                paper_best = PAPER_RANKING_NOTES["Table_II_best_" + ("nash" if metric == "nash_score" else "meanIGD")].get(bench)
                py_best = _best(summary, bench, metric, metric == "nash_score")
                rank_match = (paper_best == py_best) or (paper_best == "tie")
                rows.append(
                    {
                        "benchmark": bench,
                        "algorithm": alg,
                        "condition": "case1_no_concession",
                        "metric": metric,
                        "paper_mean": mean,
                        "paper_std": std,
                        "python_mean": py_mean,
                        "python_std": py_std,
                        "absolute_difference": abs_diff,
                        "relative_difference": rel,
                        "ranking_in_paper": paper_best,
                        "ranking_in_python": py_best,
                        "ranking_match": bool(rank_match),
                        "trend_match": bool(rank_match),
                        "reproduction_level": _level(abs_diff, rel if np.isfinite(rel) else 9, rank_match, mean),
                        "notes": "ZM26 Table II",
                    }
                )
    for bench, table in TABLE_III.items():
        means = {alg: vals["log_nash"][0] for alg, vals in table.items()}
        paper_best_n = max(means, key=means.get)
        igd = {alg: vals["meanIGD"][0] for alg, vals in table.items()}
        paper_best_i = min(igd, key=igd.get)
        for alg, metrics in table.items():
            for metric, (mean, std) in metrics.items():
                py = summary[
                    (summary.benchmark == bench)
                    & (summary.algorithm == alg)
                    & (summary.condition == "case1_no_concession")
                    & (summary.metric == metric)
                ]
                py_mean = float(py["mean"].iloc[0]) if len(py) else np.nan
                py_std = float(py["std"].iloc[0]) if len(py) else np.nan
                abs_diff = abs(py_mean - mean) if np.isfinite(py_mean) else np.nan
                rel = abs_diff / (abs(mean) + 1e-12) if np.isfinite(abs_diff) else np.nan
                paper_best = paper_best_n if metric == "log_nash" else paper_best_i
                py_best = _best(summary, bench, metric, metric == "log_nash")
                rank_match = paper_best == py_best
                rows.append(
                    {
                        "benchmark": bench,
                        "algorithm": alg,
                        "condition": "case1_no_concession",
                        "metric": metric,
                        "paper_mean": mean,
                        "paper_std": std,
                        "python_mean": py_mean,
                        "python_std": py_std,
                        "absolute_difference": abs_diff,
                        "relative_difference": rel,
                        "ranking_in_paper": paper_best,
                        "ranking_in_python": py_best,
                        "ranking_match": bool(rank_match),
                        "trend_match": bool(rank_match),
                        "reproduction_level": _level(abs_diff, rel if np.isfinite(rel) else 9, rank_match, mean),
                        "notes": "ZM26 Table III; log_nash is ln(Psi_NP)",
                    }
                )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"wrote {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()

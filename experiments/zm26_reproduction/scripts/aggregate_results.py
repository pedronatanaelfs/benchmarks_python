from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from .. import ROOT
from ..runners.jobs import RAW_CSV

OUT = ROOT / "results" / "aggregated" / "summary.csv"
STAT = ROOT / "results" / "statistical_tests"


def holm(pvals: np.ndarray) -> np.ndarray:
    p = np.asarray(pvals, dtype=float)
    n = p.size
    order = np.argsort(p)
    adj = np.empty(n)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (n - rank) * p[idx]
        running = max(running, val)
        adj[idx] = min(running, 1.0)
    return adj


def main() -> None:
    df = pd.read_csv(RAW_CSV)
    metrics = [
        "meanIGD",
        "nash_score",
        "log_nash",
        "jain_index",
        "gini_index",
        "IGD_DM1",
        "IGD_DM2",
        "IGD_DM3",
    ]
    rows = []
    for keys, g in df.groupby(["benchmark", "algorithm", "condition"]):
        for metric in metrics:
            if metric not in g.columns:
                continue
            x = pd.to_numeric(g[metric], errors="coerce").dropna()
            if x.empty:
                continue
            rows.append(
                {
                    "benchmark": keys[0],
                    "algorithm": keys[1],
                    "condition": keys[2],
                    "metric": metric,
                    "mean": float(x.mean()),
                    "std": float(x.std(ddof=1)) if len(x) > 1 else 0.0,
                    "median": float(x.median()),
                    "min": float(x.min()),
                    "max": float(x.max()),
                    "n_runs": int(len(x)),
                }
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)

    STAT.mkdir(parents=True, exist_ok=True)
    pair_rows = []
    friedman_rows = []
    for (bench, cond), g in df.groupby(["benchmark", "condition"]):
        for metric in ["meanIGD", "nash_score", "log_nash"]:
            algs = sorted(g["algorithm"].unique())
            if len(algs) < 2:
                continue
            samples = [
                pd.to_numeric(g.loc[g["algorithm"] == a, metric], errors="coerce").dropna().to_numpy()
                for a in algs
            ]
            if any(len(s) < 2 for s in samples):
                continue
            raw_p = []
            pairs = []
            for i in range(len(algs)):
                for j in range(i + 1, len(algs)):
                    _, p = stats.mannwhitneyu(samples[i], samples[j], alternative="two-sided")
                    pairs.append((algs[i], algs[j], float(p)))
                    raw_p.append(p)
            adj = holm(np.array(raw_p)) if raw_p else []
            for (a, b, p), pa in zip(pairs, adj):
                pair_rows.append(
                    {
                        "benchmark": bench,
                        "condition": cond,
                        "metric": metric,
                        "algorithm_a": a,
                        "algorithm_b": b,
                        "p_raw": p,
                        "p_holm": float(pa),
                    }
                )
            try:
                k = min(len(s) for s in samples)
                stacked = np.column_stack([s[:k] for s in samples])
                stat, p = stats.friedmanchisquare(*[stacked[:, i] for i in range(stacked.shape[1])])
                if metric == "meanIGD":
                    ranks = stats.rankdata(stacked, axis=1, method="average")
                else:
                    ranks = stats.rankdata(-stacked, axis=1, method="average")
                friedman_rows.append(
                    {
                        "benchmark": bench,
                        "condition": cond,
                        "metric": metric,
                        "statistic": float(stat),
                        "p_value": float(p),
                        "average_ranks": ",".join(
                            f"{a}:{r:.3f}" for a, r in zip(algs, ranks.mean(axis=0))
                        ),
                    }
                )
            except Exception:
                pass
    pd.DataFrame(pair_rows).to_csv(STAT / "wilcoxon_holm.csv", index=False)
    pd.DataFrame(friedman_rows).to_csv(STAT / "friedman.csv", index=False)
    print(f"wrote {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .. import ROOT
from ..config.settings import CONCESSION_CASES, FIGURE_PROBLEMS, NONCONSENSUS_BENCHMARKS

SUM = ROOT / "results" / "aggregated" / "summary.csv"
CMP = ROOT / "results" / "paper_comparison" / "paper_vs_python.csv"
RAW = ROOT / "results" / "raw" / "results.csv"
POP = ROOT / "results" / "raw" / "populations"
FIG = ROOT / "figures"


def _save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG / f"{name}.png", dpi=160)
    fig.savefig(FIG / f"{name}.pdf")
    plt.close(fig)


def main() -> None:
    cmp = pd.read_csv(CMP)
    summary = pd.read_csv(SUM)
    raw = pd.read_csv(RAW)

    fig, ax = plt.subplots(figsize=(7, 5))
    sub = cmp[cmp.metric == "meanIGD"]
    ax.scatter(sub.paper_mean, sub.python_mean, alpha=0.7)
    lim = [min(sub.paper_mean.min(), sub.python_mean.min()), max(sub.paper_mean.max(), sub.python_mean.max())]
    ax.plot(lim, lim, "k--", lw=1)
    ax.set_xlabel("Paper meanIGD")
    ax.set_ylabel("Python meanIGD")
    ax.set_title("Paper vs Python meanIGD")
    _save(fig, "paper_vs_python_meanIGD")

    fig, ax = plt.subplots(figsize=(7, 5))
    sub = cmp[cmp.metric.isin(["nash_score", "log_nash"])]
    ax.scatter(sub.paper_mean, sub.python_mean, alpha=0.7)
    ax.set_xlabel("Paper Nash / log Nash")
    ax.set_ylabel("Python Nash / log Nash")
    ax.set_title("Paper vs Python Nash-product scores")
    _save(fig, "paper_vs_python_nash")

    fig, ax = plt.subplots(figsize=(8, 4))
    ranks = cmp.drop_duplicates(["benchmark", "metric"])[["benchmark", "metric", "ranking_match"]]
    match = ranks.groupby("metric")["ranking_match"].mean()
    ax.bar(match.index.astype(str), match.values)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Fraction of ranking matches")
    ax.set_title("Ranking comparison")
    _save(fig, "ranking_comparison")

    fig, ax = plt.subplots(figsize=(9, 5))
    case1 = raw[raw.condition == "case1_no_concession"]
    disp = []
    labels = []
    for bench, g in case1.groupby("benchmark"):
        ig1 = pd.to_numeric(g["IGD_DM1"], errors="coerce")
        ig2 = pd.to_numeric(g["IGD_DM2"], errors="coerce")
        disp.append(np.abs(ig1 - ig2).mean())
        labels.append(bench)
    order = np.argsort(disp)[::-1]
    ax.bar([labels[i] for i in order][:18], [disp[i] for i in order][:18])
    ax.tick_params(axis="x", rotation=75)
    ax.set_ylabel("|IGD_DM1 - IGD_DM2|")
    ax.set_title("Party-wise IGD disparity")
    _save(fig, "party_igd_disparity")

    def _sens(prefix, outfile):
        fig, axes = plt.subplots(2, 3, figsize=(10, 6), sharey=True)
        axes = axes.ravel()
        problems = [p for p in NONCONSENSUS_BENCHMARKS if p.startswith(prefix)]
        cases = list(CONCESSION_CASES)
        for ax, bench in zip(axes, problems):
            sub = summary[(summary.benchmark == bench) & (summary.metric == "nash_score")]
            for alg, gg in sub.groupby("algorithm"):
                ys = [float(gg.loc[gg.condition == c, "mean"].mean()) if c in set(gg.condition) else np.nan for c in cases]
                ax.plot(range(1, 7), ys, marker="o", label=alg)
            ax.set_title(bench)
            ax.set_xticks(range(1, 7))
        axes[0].legend(fontsize=7)
        fig.suptitle(f"Concession sensitivity ({prefix})")
        _save(fig, outfile)

    _sens("MPMOP", "concession_sensitivity_mpmop")
    _sens("MPDMP", "concession_sensitivity_mpdmp")

    for name in FIGURE_PROBLEMS:
        files = sorted(POP.glob(f"{name}_*_run1_seed1.npz"))
        if not files:
            continue
        fig, ax = plt.subplots(figsize=(5, 5))
        for path in files:
            data = np.load(path, allow_pickle=True)
            X = data["X"]
            alg = str(data["algorithm"])
            ax.scatter(X[:, 0], X[:, 1], s=12, alpha=0.6, label=alg)
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")
        ax.set_title(name)
        ax.legend(fontsize=7)
        _save(fig, f"decision_{name.lower()}")
    print(f"wrote figures in {FIG}")


if __name__ == "__main__":
    main()

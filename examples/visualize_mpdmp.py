"""Visualize MPDMP13/17/18 decision space, reference points and party PS."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination

from fairmoo_benchmarks import get_problem
from fairmoo_benchmarks.pymoo import PymooMultiPartyAdapter


def _plot_one(ax, name: str) -> None:
    base = get_problem(name)
    problem = PymooMultiPartyAdapter(base)
    res = minimize(
        problem,
        NSGA2(pop_size=60),
        get_termination("n_gen", 30),
        seed=42,
        verbose=False,
    )

    colors = ["C0", "C1", "C2", "C3"]
    for dm in range(base.n_dm):
        refs = base.get_reference_points(dm)
        ps = base.get_pareto_set(dm=dm, n_points=200)
        c = colors[dm % len(colors)]
        ax.scatter(refs[:, 0], refs[:, 1], marker="x", s=60, c=c, label=f"DM{dm+1} refs")
        if ps is not None and ps.size:
            ax.plot(ps[:, 0], ps[:, 1], "-", c=c, alpha=0.7, label=f"DM{dm+1} PS")
    if res.X is not None:
        ax.scatter(res.X[:, 0], res.X[:, 1], s=8, c="k", alpha=0.35, label="pop")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.set_title(name)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.legend(fontsize=7, loc="best")


def main() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, name in zip(axes, ["MPDMP13", "MPDMP17", "MPDMP18"]):
        _plot_one(ax, name)
    fig.tight_layout()
    out = Path(__file__).resolve().parent / "mpdmp_visualization.png"
    fig.savefig(out, dpi=140)
    print("saved", out)


if __name__ == "__main__":
    main()

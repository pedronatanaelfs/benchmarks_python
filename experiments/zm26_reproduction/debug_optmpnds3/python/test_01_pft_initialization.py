"""Native PFt (getPF equivalent). Independent RNG; region/scale, not exact X."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms.optmpnds3 import _party_nsga2
from experiments.zm26_reproduction.algorithms.operators import environmental_selection
from experiments.zm26_reproduction.debug_optmpnds3.python.csv_io import save_matrix, save_table
from experiments.zm26_reproduction.debug_optmpnds3.python.helpers import COMMON_PS, quality_row
from experiments.zm26_reproduction.debug_optmpnds3.python.paths import FIGURES, PYTHON_OUT
from experiments.zm26_reproduction.runners.problem_setup import load_problem


def _scatter(path, pf1, pf2, ps, title):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(pf1[:, 0], pf1[:, 1], s=12, c="C0", label="PF1 (DM1 front 1)", alpha=0.8)
    ax.scatter(pf2[:, 0], pf2[:, 1], s=12, c="C1", label="PF2 (DM2 front 1)", alpha=0.8)
    ax.scatter([ps[0]], [ps[1]], s=80, c="k", marker="*", label="common PS")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_title(title)
    ax.legend(loc="best", fontsize=8)
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def run(seeds: tuple[int, ...] = (1, 2, 3)) -> None:
    rows = []
    for name in ("MPDMP1", "MPDMP4"):
        problem, _, slices = load_problem(name)
        ps = COMMON_PS[name]
        for seed in seeds:
            rng = np.random.default_rng(seed)
            X1, F1 = _party_nsga2(problem, rng, slices[0], 100, 10000, problem.xl, problem.xu)
            X2, F2 = _party_nsga2(problem, rng, slices[1], 100, 10000, problem.xl, problem.xu)
            Xc = np.vstack([X1, X2])
            Fc = np.vstack([F1, F2])
            n_before = Xc.shape[0]
            Xs, Fs, front, crowd = environmental_selection(
                Xc, Fc, Xc.shape[0], mode="optmpnds3", slices=slices
            )
            q = quality_row(name, Xs, Fs, tag=f"after_envsel_seed{seed}")
            q.update(
                {
                    "seed": seed,
                    "n_pf1": int(X1.shape[0]),
                    "n_pf2": int(X2.shape[0]),
                    "n_concat_before_unique": int(n_before),
                    "n_after_envsel": int(Xs.shape[0]),
                    "source": "python_native_pft",
                }
            )
            rows.append(q)
            if seed == 1:
                save_matrix(PYTHON_OUT / f"{name.lower()}_pf1_X.csv", X1, ["x1", "x2"])
                save_matrix(PYTHON_OUT / f"{name.lower()}_pf2_X.csv", X2, ["x1", "x2"])
                save_matrix(PYTHON_OUT / f"{name.lower()}_init_X.csv", Xs, ["x1", "x2"])
                save_matrix(PYTHON_OUT / f"{name.lower()}_init_F.csv", Fs)
                save_matrix(
                    PYTHON_OUT / f"{name.lower()}_init_meta.csv",
                    np.array([[X1.shape[0], X2.shape[0], n_before, Xs.shape[0]]]),
                    ["n_pf1", "n_pf2", "n_concat", "n_after_envsel"],
                )
                _scatter(
                    FIGURES / f"{name.lower()}_python_pft.png",
                    X1,
                    X2,
                    ps,
                    f"Python PFt {name} seed=1",
                )
            print(
                f"python PFt {name} seed={seed}: |PF1|={X1.shape[0]} |PF2|={X2.shape[0]} "
                f"n={Xs.shape[0]} zm26={q['zm26_meanIGD']:.4g} "
                f"meanDistPS={q['mean_dist_to_common_ps']:.3g}"
            )
    save_table(PYTHON_OUT / "test_01_pft_initialization.csv", pd.DataFrame(rows))
    print("python test_01 done")


if __name__ == "__main__":
    run()

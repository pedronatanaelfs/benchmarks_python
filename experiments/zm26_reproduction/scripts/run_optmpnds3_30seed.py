"""OptMPNDS3-only 30-seed MPDMP rerun after the last-generation fix.

Writes to results/validation/optmpnds3_30seed/ so the historical collapsed
OptMPNDS3 rows in results/raw/ are not mixed or skipped by job-key resume.
Does not run OptAll / OptMPNDS / OptMPNDS2.
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.zm26_reproduction.algorithms import ALGORITHMS
from experiments.zm26_reproduction.config.settings import MPDMP
from experiments.zm26_reproduction.metrics.matlab_mpdmp_pf import matlab_problem_pf
from experiments.zm26_reproduction.metrics.she_igd import zm26_meanIGD
from experiments.zm26_reproduction.runners.problem_setup import load_problem

OUT_DIR = (
    Path(__file__).resolve().parents[1] / "results" / "validation" / "optmpnds3_30seed"
)
CSV_PATH = OUT_DIR / "optmpnds3_30seed.csv"
POP_DIR = OUT_DIR / "populations"

PAPER = {
    "MPDMP1": 0.0447,
    "MPDMP2": 0.0577,
    "MPDMP3": 0.113,
    "MPDMP4": 0.0133,
    "MPDMP5": 2.66,
    "MPDMP6": 0.0838,
    "MPDMP7": 2.26,
    "MPDMP8": 2.25,
    "MPDMP9": 0.203,
    "MPDMP10": 0.0699,
    "MPDMP11": 1.19,
    "MPDMP12": 2.79,
}


def _done_keys(path: Path) -> set[tuple[str, int]]:
    if not path.exists():
        return set()
    df = pd.read_csv(path)
    return set(zip(df["benchmark"].astype(str), df["seed"].astype(int)))


def _one(name: str, seed: int) -> dict:
    problem, _, slices = load_problem(name)
    rng = np.random.default_rng(seed)
    t0 = time.time()
    X, F = ALGORITHMS["OptMPNDS3"](
        population_size=MPDMP["population_size"],
        evaluation_budget=MPDMP["evaluation_budget"],
    ).run(problem, rng, slices)
    # MPDMP13–18 have no common PS / MATLAB PF(); Table III is MPDMP1–12 only.
    zm26 = float("nan")
    try:
        pf = matlab_problem_pf(problem)
        zm26 = float(zm26_meanIGD(F, pf, slices))
    except Exception:
        zm26 = float("nan")
    rec = {
        "benchmark": name,
        "algorithm": "OptMPNDS3",
        "seed": seed,
        "n_final": int(X.shape[0]),
        "n_unique_F": int(np.unique(np.round(F, 12), axis=0).shape[0]),
        "zm26_meanIGD": zm26,
        "paper_zm26": PAPER.get(name, np.nan),
        "pop_mean_x1": float(X[:, 0].mean()),
        "pop_mean_x2": float(X[:, 1].mean()),
        "runtime_sec": time.time() - t0,
    }
    POP_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(POP_DIR / f"{name}_OptMPNDS3_seed{seed}.npz", X=X, F=F)
    return rec


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--problems",
        nargs="*",
        default=[f"MPDMP{i}" for i in range(1, 19)],
    )
    p.add_argument("--seeds", type=int, default=30)
    p.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 2) - 2)))
    args = p.parse_args(argv)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    jobs = [(name, seed) for name in args.problems for seed in range(1, args.seeds + 1)]
    done = _done_keys(CSV_PATH)
    pending = [(n, s) for n, s in jobs if (n, s) not in done]
    print(
        f"{len(jobs)} scheduled, {len(pending)} remaining, workers={args.workers}",
        flush=True,
    )
    if not pending:
        return 0

    workers = max(1, min(args.workers, len(pending)))
    rows: list[dict] = []
    if CSV_PATH.exists():
        rows = pd.read_csv(CSV_PATH).to_dict("records")

    def _flush() -> None:
        pd.DataFrame(rows).to_csv(CSV_PATH, index=False)

    if workers == 1:
        for name, seed in pending:
            rec = _one(name, seed)
            rows.append(rec)
            _flush()
            print(
                f"{name} seed={seed} n={rec['n_final']} zm26={rec['zm26_meanIGD']:.4g} "
                f"paper={rec['paper_zm26']} t={rec['runtime_sec']:.1f}s",
                flush=True,
            )
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(_one, n, s): (n, s) for n, s in pending}
            for fut in as_completed(futs):
                name, seed = futs[fut]
                try:
                    rec = fut.result()
                except Exception as exc:
                    print(f"FAIL {name} seed={seed}: {exc}", flush=True)
                    continue
                rows.append(rec)
                _flush()
                zm = rec["zm26_meanIGD"]
                zm_s = f"{zm:.4g}" if zm == zm else "nan"
                print(
                    f"{name} seed={seed} n={rec['n_final']} zm26={zm_s} "
                    f"paper={rec['paper_zm26']} t={rec['runtime_sec']:.1f}s",
                    flush=True,
                )
    print("wrote", CSV_PATH, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

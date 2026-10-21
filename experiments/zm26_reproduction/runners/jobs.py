from __future__ import annotations

import json
import os
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .. import ROOT
from ..algorithms import ALGORITHMS
from ..config.settings import (
    FIGURE_PROBLEMS,
    MPDMP,
    MPMOP,
    RUNS,
    SEEDS,
    algorithm_kwargs,
)
from .evaluate_population import estimate_C, evaluate_conditions
from .problem_setup import load_problem, reference_fronts

RESULTS = ROOT / "results"
RAW_CSV = RESULTS / "raw" / "results.csv"
POP_DIR = RESULTS / "raw" / "populations"
LOG_DIR = RESULTS / "logs"
DIAG_DIR = RESULTS / "diagnostics"
JOB_DIR = RESULTS / "raw" / "job_rows"
FAIL_DIR = RESULTS / "logs" / "failures"

CSV_FIELDS = [
    "benchmark",
    "benchmark_family",
    "algorithm",
    "condition",
    "run",
    "seed",
    "D",
    "M",
    "DM",
    "population_size",
    "evaluation_budget",
    "runtime_sec",
    "git_commit",
    "IGD_DM1",
    "IGD_DM2",
    "IGD_DM3",
    "meanIGD",
    "concession_DM1",
    "concession_DM2",
    "concession_DM3",
    "penalty_DM1",
    "penalty_DM2",
    "penalty_DM3",
    "utility_DM1",
    "utility_DM2",
    "utility_DM3",
    "mu_DM1",
    "mu_DM2",
    "mu_DM3",
    "lambda_DM1",
    "lambda_DM2",
    "lambda_DM3",
    "nash_score",
    "nash_score_exp",
    "log_nash",
    "C",
    "jain_index",
    "gini_index",
    "jain_utility",
    "gini_utility",
]


def _jsonable(value):
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        x = float(value)
        return None if not np.isfinite(x) else x
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if value is None:
        return None
    return value


def job_key(job: dict) -> tuple:
    return (job["benchmark"], job["algorithm"], int(job["run"]))


def job_row_path(job: dict) -> Path:
    return JOB_DIR / f"{job['benchmark']}_{job['algorithm']}_run{job['run']}.json"


def completed_job_keys() -> set[tuple]:
    keys: set[tuple] = set()
    if RAW_CSV.exists():
        import csv

        with RAW_CSV.open() as f:
            for row in csv.DictReader(f):
                keys.add((row["benchmark"], row["algorithm"], int(row["run"])))
    if JOB_DIR.exists():
        for path in JOB_DIR.glob("*.json"):
            try:
                payload = json.loads(path.read_text())
                rec = payload["rows"][0]
                keys.add((rec["benchmark"], rec["algorithm"], int(rec["run"])))
            except Exception:
                stem = path.stem
                # Name: BENCH_ALG_runN
                if "_run" in stem:
                    bench_alg, run_s = stem.rsplit("_run", 1)
                    parts = bench_alg.split("_", 1)
                    if len(parts) == 2:
                        keys.add((parts[0], parts[1], int(run_s)))
    return keys


def rebuild_csv() -> int:
    """Merge per-job JSON files (and any existing CSV) into results.csv."""
    import csv

    by_key: dict[tuple, list[dict]] = {}
    if RAW_CSV.exists():
        with RAW_CSV.open() as f:
            for row in csv.DictReader(f):
                key = (row["benchmark"], row["algorithm"], int(row["run"]), row["condition"])
                by_key[key] = [row]
    if JOB_DIR.exists():
        for path in sorted(JOB_DIR.glob("*.json")):
            try:
                payload = json.loads(path.read_text())
            except Exception:
                continue
            for row in payload.get("rows", []):
                key = (row["benchmark"], row["algorithm"], int(row["run"]), row["condition"])
                by_key[key] = [row]
    RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
    tmp = RAW_CSV.with_suffix(".csv.tmp")
    with tmp.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for _, rows in sorted(by_key.items()):
            for row in rows:
                out = {}
                for field in CSV_FIELDS:
                    val = row.get(field, "")
                    if val is None:
                        val = ""
                    out[field] = val
                writer.writerow(out)
    tmp.replace(RAW_CSV)
    return len(by_key)


def git_commit() -> str:
    head = ROOT.parents[1] / ".git" / "HEAD"
    try:
        ref = head.read_text().strip()
        if ref.startswith("ref:"):
            return (ROOT.parents[1] / ".git" / ref.split(" ", 1)[1]).read_text().strip()
        return ref
    except Exception:
        return "unknown"


def iter_jobs(family: str | None = None, smoke: bool = False):
    runs = 2 if smoke else RUNS
    seeds = SEEDS[:runs]
    specs = []
    if family in (None, "MPMOP"):
        specs.append(("MPMOP", MPMOP))
    if family in (None, "MPDMP"):
        specs.append(("MPDMP", MPDMP))
    for fam, cfg in specs:
        budget = 400 if smoke else cfg["evaluation_budget"]
        n = 20 if smoke else cfg["population_size"]
        for problem in cfg["problems"]:
            for alg in cfg["algorithms"]:
                for run, seed in enumerate(seeds, start=1):
                    yield {
                        "benchmark": problem,
                        "family": fam,
                        "algorithm": alg,
                        "run": run,
                        "seed": seed,
                        "population_size": n,
                        "evaluation_budget": budget,
                        "smoke": smoke,
                    }


_CACHE: dict = {}


def _refs(name: str):
    if name not in _CACHE:
        from ..config.settings import cases_for, concession_vector
        from ..metrics.nash_score import estimate_lambda

        problem, family, slices = load_problem(name)
        pf = reference_fronts(problem)
        rng = np.random.default_rng(0)
        C = estimate_C(problem, pf, slices, rng)
        lambdas = {}
        for case in cases_for(problem.name):
            eps = np.asarray(concession_vector(problem.name, problem.n_dm, case), dtype=float)
            lambdas[case] = estimate_lambda(pf, slices, eps, rng)
        _CACHE[name] = (problem, family, slices, pf, C, lambdas)
    return _CACHE[name]


def run_job(job: dict) -> list[dict]:
    t0 = time.time()
    commit = git_commit()
    problem, family, slices, pf, C, lambdas = _refs(job["benchmark"])
    rng = np.random.default_rng(int(job["seed"]))
    kw = algorithm_kwargs(family, job["algorithm"])
    kw["population_size"] = job["population_size"]
    kw["evaluation_budget"] = job["evaluation_budget"]
    alg = ALGORITHMS[job["algorithm"]](**kw)
    X, F = alg.run(problem, rng, slices)
    runtime = time.time() - t0
    rows = evaluate_conditions(
        F, problem, slices, pf, C=C, rng=rng, lambdas=lambdas
    )
    out = []
    for row in rows:
        rec = {
            "benchmark": problem.name,
            "benchmark_family": family,
            "algorithm": job["algorithm"],
            "run": job["run"],
            "seed": job["seed"],
            "D": problem.n_var,
            "M": problem.n_obj,
            "DM": problem.n_dm,
            "population_size": job["population_size"],
            "evaluation_budget": job["evaluation_budget"],
            "runtime_sec": runtime,
            "git_commit": commit,
        }
        rec.update(row)
        out.append(rec)
    if problem.name in FIGURE_PROBLEMS or job.get("save_population"):
        POP_DIR.mkdir(parents=True, exist_ok=True)
        path = POP_DIR / (
            f"{problem.name}_{job['algorithm']}_run{job['run']}_seed{job['seed']}.npz"
        )
        np.savez_compressed(
            path,
            X=X,
            F=F,
            seed=job["seed"],
            problem=problem.name,
            algorithm=job["algorithm"],
            condition="optimization",
        )
    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "benchmark": problem.name,
        "algorithm": job["algorithm"],
        "condition": "optimization",
        "seed": job["seed"],
        "runtime": runtime,
        "configuration": kw,
    }
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{problem.name}_{job['algorithm']}_run{job['run']}.json"
    log_path.write_text(json.dumps(log, indent=2, default=str))
    JOB_DIR.mkdir(parents=True, exist_ok=True)
    job_row_path(job).write_text(
        json.dumps({"job": _jsonable(job), "rows": _jsonable(out)}, indent=2)
    )
    return out

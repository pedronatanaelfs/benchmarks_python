"""Run the ZM26 reproduction jobs.

Usage:
    python -m experiments.zm26_reproduction.runners.run_all
    python -m experiments.zm26_reproduction.runners.run_all --family MPMOP
    python -m experiments.zm26_reproduction.runners.run_all --smoke
"""

from __future__ import annotations

import argparse
import os
import traceback
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait

from .jobs import (
    CSV_FIELDS,
    FAIL_DIR,
    RAW_CSV,
    completed_job_keys,
    iter_jobs,
    job_key,
    rebuild_csv,
    run_job,
)


def _append(rows: list[dict]) -> None:
    import csv

    RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
    new = not RAW_CSV.exists()
    with RAW_CSV.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if new:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)
        f.flush()


def _record_failure(job: dict, exc: BaseException) -> None:
    FAIL_DIR.mkdir(parents=True, exist_ok=True)
    path = FAIL_DIR / f"{job['benchmark']}_{job['algorithm']}_run{job['run']}.txt"
    path.write_text(
        f"{job}\n{type(exc).__name__}: {exc}\n{traceback.format_exc()}\n"
    )


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--family", choices=["MPMOP", "MPDMP"])
    p.add_argument("--smoke", action="store_true")
    p.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    p.add_argument("--resume", action="store_true", default=True)
    args = p.parse_args(argv)

    jobs = list(iter_jobs(family=args.family, smoke=args.smoke))
    done = completed_job_keys() if args.resume else set()
    pending = [job for job in jobs if job_key(job) not in done]
    print(
        f"{len(jobs)} scheduled, {len(pending)} remaining, workers={args.workers}",
        flush=True,
    )
    if not pending:
        n = rebuild_csv()
        print(f"nothing to run; rebuilt CSV with {n} evaluation rows", flush=True)
        return 0

    failures = 0

    def _consume(job, rows=None, exc=None):
        nonlocal failures
        if exc is not None:
            failures += 1
            _record_failure(job, exc)
            print(
                f"FAIL {job['benchmark']} {job['algorithm']} run {job['run']}: {exc}",
                flush=True,
            )
            return
        _append(rows)
        print(
            f"done {job['benchmark']} {job['algorithm']} run {job['run']}",
            flush=True,
        )

    workers = max(1, min(args.workers, len(pending)))
    if workers == 1:
        for job in pending:
            try:
                _consume(job, rows=run_job(job))
            except Exception as exc:
                _consume(job, exc=exc)
    else:
        in_flight = {}
        nxt = 0
        with ProcessPoolExecutor(max_workers=workers) as ex:
            while nxt < len(pending) or in_flight:
                while nxt < len(pending) and len(in_flight) < workers:
                    job = pending[nxt]
                    nxt += 1
                    in_flight[ex.submit(run_job, job)] = job
                done_futs, _ = wait(in_flight, return_when=FIRST_COMPLETED)
                for fut in done_futs:
                    job = in_flight.pop(fut)
                    try:
                        _consume(job, rows=fut.result())
                    except Exception as exc:
                        _consume(job, exc=exc)

    n = rebuild_csv()
    print(
        f"finished remaining={0} failures={failures} csv_rows={n}",
        flush=True,
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

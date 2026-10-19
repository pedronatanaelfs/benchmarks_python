"""Evaluate every Python benchmark on the shared deterministic inputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


VALIDATION_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = VALIDATION_DIR.parent
SRC = REPOSITORY_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fairmoo_benchmarks import get_problem, list_problems  # noqa: E402


def run(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir = output_dir / "metadata"
    metadata_dir.mkdir(exist_ok=True)

    for name in list_problems():
        input_frame = pd.read_csv(input_dir / f"{name}.csv")
        test_ids = input_frame["test_id"]
        X = input_frame.drop(columns=["test_id"]).to_numpy(dtype=float)
        problem = get_problem(name)
        F = np.asarray(problem.evaluate(X), dtype=float)

        frame = input_frame.copy()
        for index in range(F.shape[1]):
            frame[f"f{index + 1}"] = F[:, index]
        frame.to_csv(output_dir / f"{name}.csv", index=False, float_format="%.17g")

        metadata = problem.describe()
        metadata.update(
            {
                "encoding": "real",
                "dm_objective_indices_1based": [
                    list(range(sl.start + 1, sl.stop + 1))
                    for sl in problem.dm_objective_slices.values()
                ],
            }
        )
        (metadata_dir / f"{name}.json").write_text(
            json.dumps(metadata, indent=2, default=str) + "\n", encoding="utf-8"
        )
        print(f"PASS {name} ({len(test_ids)} points, {F.shape[1]} objectives)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, default=VALIDATION_DIR / "test_inputs")
    parser.add_argument(
        "--output", type=Path, default=VALIDATION_DIR / "python" / "results"
    )
    args = parser.parse_args()
    run(args.inputs, args.output)


if __name__ == "__main__":
    main()

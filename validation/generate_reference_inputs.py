"""Generate deterministic decision vectors shared by MATLAB and Python.

The bounds in this file are transcribed from the MATLAB class constructors,
which are the reference for this audit.  No random-number generator is used.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


ALL_PROBLEMS = [
    *(f"MPMOP{i}" for i in range(1, 18)),
    *(f"MPDMP{i}" for i in range(1, 19)),
]


def reference_metadata(name: str) -> dict:
    """Return default metadata from the current MATLAB constructors."""
    if name.startswith("MPDMP"):
        number = int(name[5:])
        objectives = {
            1: [2, 2], 2: [2, 2], 3: [2, 3], 4: [3, 3],
            5: [3, 3], 6: [4, 4], 7: [4, 4], 8: [5, 5],
            9: [2, 2, 2], 10: [2, 2, 4], 11: [3, 3, 3],
            12: [4, 4, 4], 13: [2, 2], 14: [3, 3],
            15: [4, 4], 16: [5, 5], 17: [2, 2, 2],
            18: [3, 3, 3],
        }[number]
        return {
            "problem": name,
            "D": 2,
            "M": sum(objectives),
            "DM": len(objectives),
            "n_obj_per_dm": objectives,
            "encoding": "real",
            "lower": [0.0, 0.0],
            "upper": [100.0, 100.0],
        }

    number = int(name[5:])
    objectives = {
        1: [2, 2], 2: [2, 2], 3: [2, 2], 4: [3, 3],
        5: [3, 3], 6: [3, 3], 7: [2, 2, 2],
        8: [2, 2, 2], 9: [3, 3, 3], 10: [3, 3, 3],
        11: [3, 3, 3], 12: [2, 2], 13: [2, 2],
        14: [3, 3], 15: [2, 2, 2], 16: [2, 2],
        17: [2, 2, 2],
    }[number]
    lower = np.zeros(10)
    upper = np.ones(10)
    if number in (1, 7):
        lower[0], upper[0] = 1.0, 4.0
    elif number in (2, 3, 8):
        lower[1:] = -1.0
    elif number in (4, 6, 9, 11):
        lower[2:] = -1.0
    return {
        "problem": name,
        "D": 10,
        "M": sum(objectives),
        "DM": len(objectives),
        "n_obj_per_dm": objectives,
        "encoding": "real",
        "lower": lower.tolist(),
        "upper": upper.tolist(),
    }


def deterministic_points(lower: np.ndarray, upper: np.ndarray) -> tuple[list[str], np.ndarray]:
    """Construct bound, fractional, heterogeneous, and ten patterned points."""
    d = lower.size
    span = upper - lower
    ids: list[str] = []
    rows: list[np.ndarray] = []

    def add(test_id: str, alpha: np.ndarray | float) -> None:
        ids.append(test_id)
        rows.append(lower + np.asarray(alpha, dtype=float) * span)

    add("lower_bound", 0.0)
    add("upper_bound", 1.0)
    add("midpoint", 0.5)
    add("fraction_025", 0.25)
    add("fraction_050", 0.50)
    add("fraction_075", 0.75)
    add("heterogeneous_ascending", np.linspace(0.05, 0.95, d))
    add("heterogeneous_descending", np.linspace(0.95, 0.05, d))

    # Modular patterns vary both rows and coordinates and never rely on RNG.
    for row in range(10):
        alpha = (((row + 2) * (np.arange(d) + 3)) % 19 + 0.5) / 19.0
        add(f"pattern_{row + 1:02d}", alpha)
    return ids, np.vstack(rows)


def write_inputs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name in ALL_PROBLEMS:
        meta = reference_metadata(name)
        lower = np.asarray(meta["lower"], dtype=float)
        upper = np.asarray(meta["upper"], dtype=float)
        test_ids, points = deterministic_points(lower, upper)
        path = output_dir / f"{name}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["test_id", *(f"x{i + 1}" for i in range(meta["D"]))])
            writer.writerows([test_id, *row] for test_id, row in zip(test_ids, points))
        manifest[name] = meta
    (output_dir / "reference_metadata.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "test_inputs",
    )
    args = parser.parse_args()
    write_inputs(args.output)
    print(f"Wrote deterministic inputs for {len(ALL_PROBLEMS)} problems to {args.output}")


if __name__ == "__main__":
    main()

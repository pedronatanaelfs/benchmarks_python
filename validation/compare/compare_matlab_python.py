"""Compare deterministic MATLAB and Python benchmark outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


VALIDATION_DIR = Path(__file__).resolve().parents[1]
ALL_PROBLEMS = [
    *(f"MPMOP{i}" for i in range(1, 18)),
    *(f"MPDMP{i}" for i in range(1, 19)),
]


def columns_with_prefix(frame: pd.DataFrame, prefix: str) -> list[str]:
    return sorted(
        (column for column in frame.columns if column.startswith(prefix)),
        key=lambda value: int(value[len(prefix):]),
    )


def compare_one(name: str, matlab_dir: Path, python_dir: Path) -> dict:
    matlab_path = matlab_dir / f"{name}.csv"
    python_path = python_dir / f"{name}.csv"
    base = {"problem": name}
    if not matlab_path.exists():
        return {
            **base,
            "status": "NEEDS_MANUAL_REVIEW",
            "reason": f"missing MATLAB output: {matlab_path}",
        }
    if not python_path.exists():
        return {**base, "status": "FAIL", "reason": f"missing Python output: {python_path}"}

    matlab = pd.read_csv(matlab_path)
    python = pd.read_csv(python_path)
    if matlab["test_id"].tolist() != python["test_id"].tolist():
        return {**base, "status": "FAIL", "reason": "test_id sequence differs"}

    mx_cols = columns_with_prefix(matlab, "x")
    px_cols = columns_with_prefix(python, "x")
    mf_cols = columns_with_prefix(matlab, "f")
    pf_cols = columns_with_prefix(python, "f")
    if mx_cols != px_cols:
        return {
            **base,
            "status": "FAIL",
            "reason": f"decision dimensions differ: MATLAB={len(mx_cols)}, Python={len(px_cols)}",
        }

    X_matlab = matlab[mx_cols].to_numpy(float)
    X_python = python[px_cols].to_numpy(float)
    # MATLAB writetable serializes doubles with fewer decimal digits than the
    # Python CSV writer. Accept serialization-only roundoff, while still
    # rejecting any materially different input matrix.
    input_error = float(np.max(np.abs(X_matlab - X_python)))
    if not np.allclose(X_matlab, X_python, rtol=0.0, atol=1e-12):
        return {
            **base,
            "status": "FAIL",
            "reason": "shared decision vectors differ",
            "max_input_serialization_error": input_error,
        }
    if len(mf_cols) != len(pf_cols):
        return {
            **base,
            "status": "FAIL",
            "reason": (
                "objective counts differ: "
                f"MATLAB={len(mf_cols)}, Python={len(pf_cols)}"
            ),
            "matlab_objectives": len(mf_cols),
            "python_objectives": len(pf_cols),
        }

    fm = matlab[mf_cols].to_numpy(float)
    fp = python[pf_cols].to_numpy(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        delta = np.abs(fm - fp)
    delta = np.where(fm == fp, 0.0, delta)
    delta = np.nan_to_num(delta, nan=np.inf, posinf=np.inf, neginf=np.inf)
    safe = np.maximum.reduce([np.abs(fm), np.abs(fp), np.full_like(fm, np.finfo(float).eps)])
    with np.errstate(invalid="ignore", divide="ignore"):
        relative = np.where(delta == 0.0, 0.0, delta / safe)
    relative = np.nan_to_num(relative, nan=np.inf, posinf=np.inf, neginf=np.inf)
    flat_index = int(np.argmax(delta))
    row, objective = np.unravel_index(flat_index, delta.shape)
    finite = bool(np.all(np.isfinite(fm)) and np.all(np.isfinite(fp)))
    passed = finite and bool(
        np.allclose(fm, fp, rtol=1e-9, atol=1e-10, equal_nan=False)
    )
    return {
        **base,
        "status": "PASS" if passed else "FAIL",
        "reason": (
            "" if passed
            else "non-finite objective value"
            if not finite
            else "objective values exceed tolerance"
        ),
        "max_absolute_error": float(np.max(delta)),
        "max_relative_error": float(np.max(relative)),
        "mean_absolute_error": float(np.mean(delta)),
        "max_error_test_id": str(matlab.loc[row, "test_id"]),
        "max_error_objective_1based": int(objective + 1),
        "matlab_value": float(fm[row, objective]),
        "python_value": float(fp[row, objective]),
        "input_X": X_matlab[row].tolist(),
        "max_input_serialization_error": input_error,
        "rtol": 1e-9,
        "atol": 1e-10,
    }


def write_reports(rows: list[dict], report_dir: Path) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(report_dir / "numerical_comparison.csv", index=False)
    (report_dir / "numerical_comparison.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# MATLAB × Python numerical comparison",
        "",
        "Tolerance: `rtol=1e-9`, `atol=1e-10`.",
        "",
        "| Problem | Status | Max abs | Max rel | MAE | Reason |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {problem} | {status} | {abs} | {rel} | {mae} | {reason} |".format(
                problem=row["problem"],
                status=row["status"],
                abs=f'{row["max_absolute_error"]:.3e}'
                if "max_absolute_error" in row else "—",
                rel=f'{row["max_relative_error"]:.3e}'
                if "max_relative_error" in row else "—",
                mae=f'{row["mean_absolute_error"]:.3e}'
                if "mean_absolute_error" in row else "—",
                reason=str(row.get("reason", "")).replace("|", "\\|"),
            )
        )
    (report_dir / "numerical_comparison.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matlab", type=Path, default=VALIDATION_DIR / "matlab" / "results"
    )
    parser.add_argument(
        "--python", type=Path, default=VALIDATION_DIR / "python" / "results"
    )
    parser.add_argument(
        "--reports", type=Path, default=VALIDATION_DIR / "reports"
    )
    args = parser.parse_args()
    rows = [compare_one(name, args.matlab, args.python) for name in ALL_PROBLEMS]
    write_reports(rows, args.reports)
    counts = pd.Series([row["status"] for row in rows]).value_counts()
    print(counts.to_string())


if __name__ == "__main__":
    main()

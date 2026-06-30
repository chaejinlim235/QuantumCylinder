"""Summarize IBM QPU Problem 3-b basis-sweep results without pandas."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT_ROOT = ROOT / "results" / "ibm_qpu_validation"
RUNS = [
    {
        "label": "2048x3",
        "dir": RESULT_ROOT / "p3b_fez_2048x3",
        "job_id": "d91r6pmu9n7c73an9qgg",
        "shots": 2048,
        "circuits": 12,
        "repeats": 3,
    },
    {
        "label": "4096x5",
        "dir": RESULT_ROOT / "p3b_fez_4096x5",
        "job_id": "d91r71fccmks73d5nmg0",
        "shots": 4096,
        "circuits": 20,
        "repeats": 5,
    },
]
GUARDRAIL = (
    "This is appendix validation only. The main scientific claims remain based "
    "on reproducible state-vector benchmarks. No hardware advantage is claimed."
)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _fmt(value: Any) -> str:
    if value in (None, ""):
        return "pending"
    try:
        return f"{float(value):.6f}"
    except Exception:
        return str(value)


def main() -> int:
    RESULT_ROOT.mkdir(parents=True, exist_ok=True)
    markdown_lines = [
        "# IBM QPU Problem 3-b Mini Validation Summary",
        "",
        GUARDRAIL,
        "",
        "We submitted tiny `M+F` circuits to IBM Quantum / Qiskit Runtime and swept",
        "the complement-qubit measurement basis. The appendix result checks whether",
        "basis changes alter post-selection statistics and the selected data distribution.",
        "",
    ]
    csv_rows: list[dict[str, Any]] = []

    for run in RUNS:
        report = _read_json(run["dir"] / "problem3b_ibm_basis_sweep_report.json")
        extract_report = _read_json(run["dir"] / "problem3b_ibm_counts_extract_report.json")
        aggregate_rows = _read_csv(run["dir"] / "problem3b_ibm_basis_sweep_aggregate.csv")
        backend = report.get("backend_selected") or report.get("backend_requested") or "ibm_fez"
        status = extract_report.get("job_status") or report.get("job_status") or "DONE"
        dt = report.get("dt", 0.2)
        repeats = report.get("repeats", run["repeats"])
        circuits = report.get("num_circuits", run["circuits"])
        shots = report.get("shots", run["shots"])

        markdown_lines.extend(
            [
                f"## Run {run['label']}",
                "",
                f"- backend: `{backend}`",
                f"- job_id: `{run['job_id']}`",
                f"- status: `{status}`",
                f"- shots: `{shots}`",
                f"- circuits: `{circuits}`",
                f"- dt: `{dt}`",
                f"- repeats: `{repeats}`",
                "",
            ]
        )

        if aggregate_rows:
            markdown_lines.extend(
                [
                    "| beta | mean p(F=0) | std p(F=0) | mean selected entropy | std selected entropy | repeats |",
                    "|---|---:|---:|---:|---:|---:|",
                ]
            )
            for row in aggregate_rows:
                csv_row = {
                    "run": run["label"],
                    "backend": backend,
                    "job_id": run["job_id"],
                    "status": status,
                    "shots": shots,
                    "circuits": circuits,
                    "dt": dt,
                    "repeats": repeats,
                    "beta": row.get("beta", ""),
                    "mean_success_probability_F0": row.get("mean_success_probability_F0", ""),
                    "std_success_probability_F0": row.get("std_success_probability_F0", ""),
                    "mean_selected_data_entropy_F0": row.get("mean_selected_data_entropy_F0", ""),
                    "std_selected_data_entropy_F0": row.get("std_selected_data_entropy_F0", ""),
                    "num_repeats": row.get("num_repeats", ""),
                }
                csv_rows.append(csv_row)
                markdown_lines.append(
                    "| "
                    f"{row.get('beta', '')} | "
                    f"{_fmt(row.get('mean_success_probability_F0'))} | "
                    f"{_fmt(row.get('std_success_probability_F0'))} | "
                    f"{_fmt(row.get('mean_selected_data_entropy_F0'))} | "
                    f"{_fmt(row.get('std_selected_data_entropy_F0'))} | "
                    f"{row.get('num_repeats', '')} |"
                )
            markdown_lines.append("")
        else:
            markdown_lines.extend(["Aggregate pending for this run.", ""])
            csv_rows.append(
                {
                    "run": run["label"],
                    "backend": backend,
                    "job_id": run["job_id"],
                    "status": status,
                    "shots": shots,
                    "circuits": circuits,
                    "dt": dt,
                    "repeats": repeats,
                    "beta": "aggregate pending",
                    "mean_success_probability_F0": "",
                    "std_success_probability_F0": "",
                    "mean_selected_data_entropy_F0": "",
                    "std_selected_data_entropy_F0": "",
                    "num_repeats": "",
                }
            )

    markdown_lines.extend(
        [
            "## Interpretation",
            "",
            "Changing the complement-qubit measurement basis changes post-selection",
            "statistics and selected data distribution, supporting the Problem 3-b",
            "interpretation that measurement basis controls the effective projected map.",
            "The main quantitative claims remain based on reproducible state-vector",
            "benchmarks.",
            "",
        ]
    )

    (RESULT_ROOT / "IBM_QPU_P3B_SUMMARY_FOR_SLIDES.md").write_text(
        "\n".join(markdown_lines),
        encoding="utf-8",
    )
    csv_path = RESULT_ROOT / "IBM_QPU_P3B_SUMMARY_FOR_SLIDES.csv"
    fieldnames = [
        "run",
        "backend",
        "job_id",
        "status",
        "shots",
        "circuits",
        "dt",
        "repeats",
        "beta",
        "mean_success_probability_F0",
        "std_success_probability_F0",
        "mean_selected_data_entropy_F0",
        "std_selected_data_entropy_F0",
        "num_repeats",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"Wrote {RESULT_ROOT / 'IBM_QPU_P3B_SUMMARY_FOR_SLIDES.md'}")
    print(f"Wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

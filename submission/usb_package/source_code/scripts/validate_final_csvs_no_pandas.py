"""Validate final-facing CSV and readability artifacts without pandas."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CSV_FILES = [
    ROOT / "solution" / "tables" / "problem_1c_random_unitary_metrics.csv",
    ROOT / "solution" / "tables" / "problem_2_hamiltonian_metrics.csv",
    ROOT / "solution" / "tables" / "problem_2d_resource_matches.csv",
    ROOT / "solution" / "tables" / "problem3b_measurement_basis_tradeoff.csv",
    ROOT / "solution" / "tables" / "problem3c_analysis_guided_improvement.csv",
    ROOT / "results" / "ibm_qpu_validation" / "IBM_QPU_P3B_SUMMARY_FOR_SLIDES.csv",
]

FIGURE_FILES = [
    ROOT / "solution" / "figures" / "fig_p2_fixed_h_baseline_visible.png",
    ROOT / "solution" / "figures" / "fig_metric_aligned_comparison_readable.png",
]

NOTEBOOK = ROOT / "solution" / "solution_1.ipynb"


def validate_csv(path: Path) -> tuple[int, int]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    if len(rows) < 2:
        raise ValueError(f"{path} must contain a header and at least one data row")
    width = len(rows[0])
    if width == 0:
        raise ValueError(f"{path} has an empty header")
    for index, row in enumerate(rows[1:], start=2):
        if len(row) != width:
            raise ValueError(f"{path} row {index} has width {len(row)}, expected {width}")
    return len(rows) - 1, width


def validate_figures() -> None:
    for path in FIGURE_FILES:
        if not path.exists():
            raise FileNotFoundError(path)
        if path.stat().st_size <= 0:
            raise ValueError(f"{path} is empty")


def validate_notebook() -> None:
    data = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    text = "\n".join("".join(cell.get("source", [])) for cell in data.get("cells", []))
    required = [
        "Notation used in figures",
        "S_k^{\\mathrm{RU}}",
        "S_t^{\\mathrm{Ham}}",
        "p_{\\mathrm{succ}}",
        "R_{\\mathrm{div}}",
        "fig_p2_fixed_h_baseline_visible.png",
    ]
    missing = [needle for needle in required if needle not in text]
    if missing:
        raise ValueError(f"notebook is missing notation/readability text: {missing}")


def main() -> None:
    for path in CSV_FILES:
        rows, cols = validate_csv(path)
        print(f"CSV OK: {path.relative_to(ROOT)} rows={rows} cols={cols}")
    validate_figures()
    print("Figure files OK")
    validate_notebook()
    print("Notebook notation/readability text OK")


if __name__ == "__main__":
    main()

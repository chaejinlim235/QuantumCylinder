"""Validate final-facing CSV and readability artifacts without pandas."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USB_ROOT = ROOT.parent if ROOT.name == "source_code" else ROOT / "submission" / "usb_package"
if not USB_ROOT.exists():
    USB_ROOT = ROOT

REPORT_PATH = USB_ROOT / "CSV_VALIDATION_REPORT.md"


def collect_csv_files() -> list[Path]:
    roots = [
        USB_ROOT / "source_code" / "solution" / "tables",
        USB_ROOT / "source_code" / "results" / "ibm_qpu_validation",
        USB_ROOT / "solution" / "tables",
    ]
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(sorted(root.rglob("*.csv")))
    return files


CSV_FILES = collect_csv_files()

FIGURE_FILES = [
    USB_ROOT / "solution" / "figures" / "fig2_random_unitary_haar_baseline.png",
    USB_ROOT / "source_code" / "solution" / "figures" / "fig2_random_unitary_haar_baseline.png",
    USB_ROOT / "source_code" / "solution" / "figures" / "fig_p2_fixed_h_baseline_visible.png",
    USB_ROOT / "source_code" / "solution" / "figures" / "fig_metric_aligned_comparison_readable.png",
]

NOTEBOOKS = [
    USB_ROOT / "solution" / "Problem 1.ipynb",
    USB_ROOT / "solution" / "Problem 2.ipynb",
    USB_ROOT / "solution" / "Problem 3.ipynb",
    USB_ROOT / "source_code" / "solution" / "solution_1.ipynb",
]


def validate_csv(path: Path) -> tuple[int, int]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        raw = handle.read()
        if "\\n" in raw and "\n" not in raw:
            raise ValueError(f"{path} appears to contain literal escaped newlines")
        handle.seek(0)
        reader = csv.reader(handle)
        rows = list(reader)
    if len(rows) < 2:
        if len(rows) != 1:
            raise ValueError(f"{path} must contain at least a header row")
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


def validate_notebooks() -> None:
    texts = []
    for notebook in NOTEBOOKS:
        if not notebook.exists():
            raise FileNotFoundError(notebook)
        data = json.loads(notebook.read_text(encoding="utf-8"))
        texts.append("\n".join("".join(cell.get("source", [])) for cell in data.get("cells", [])))
    text = "\n".join(texts)
    required = [
        "Judge-Facing Split Notebook",
        "S_k^{\\mathrm{RU}}",
        "S_t^{\\mathrm{Ham}}",
        "p_{\\mathrm{succ}}",
        "R_{\\mathrm{div}}",
        "fig2_random_unitary_haar_baseline.png",
        "fig_p2_fixed_h_baseline_visible.png",
    ]
    missing = [needle for needle in required if needle not in text]
    if missing:
        raise ValueError(f"notebook is missing notation/readability text: {missing}")


def main() -> None:
    report_lines = ["# CSV Validation Report", ""]
    for path in CSV_FILES:
        rows, cols = validate_csv(path)
        label = path.relative_to(USB_ROOT)
        print(f"CSV OK: {label} rows={rows} cols={cols}")
        report_lines.append(f"- PASS `{label}`: rows `{rows}`, columns `{cols}`")
    validate_figures()
    print("Figure files OK")
    report_lines.append("")
    report_lines.append("- PASS required final figure files exist and are non-empty.")
    validate_notebooks()
    print("Notebook notation/readability text OK")
    report_lines.append("- PASS split notebooks and compact reference contain required readability markers.")
    REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

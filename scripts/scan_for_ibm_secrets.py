"""Scan final-facing files for likely IBM secrets without printing secrets."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if (ROOT / "IBM_QPU_README.md").exists():
    SCAN_ROOTS = [
        ROOT / "IBM_QPU_README.md",
        ROOT / "docs" / "IBM_QPU_VALIDATION.md",
        ROOT / "docs" / "IBM_QPU_PROBLEM3B_BASIS_SWEEP.md",
        ROOT / "solution" / "README.md",
        ROOT / "solution" / "solution_1.ipynb",
        ROOT / "results" / "ibm_qpu_validation",
        ROOT / "scripts" / "ibm_qpu_smoke_test.py",
        ROOT / "scripts" / "ibm_qpu_problem3b_basis_sweep.py",
        ROOT / "scripts" / "ibm_qpu_extract_p3b_counts.py",
        ROOT / "scripts" / "summarize_ibm_qpu_p3b_results.py",
        ROOT / "scripts" / "copy_ibm_qpu_results_to_usb.py",
    ]
else:
    SCAN_ROOTS = [
        ROOT / "README.md",
        ROOT / "docs" / "IBM_QPU_VALIDATION.md",
        ROOT / "docs" / "IBM_QPU_PROBLEM3B_BASIS_SWEEP.md",
        ROOT / "solution" / "README.md",
        ROOT / "solution" / "solution_1.ipynb",
        ROOT / "submission" / "usb_package" / "README_SUBMISSION.md",
        ROOT / "submission" / "usb_package" / "Summary.md",
        ROOT / "submission" / "usb_package" / "JUDGING_CRITERIA_ALIGNMENT.md",
        ROOT / "submission" / "usb_package" / "IBM_QPU_SECURITY_AUDIT.md",
        ROOT / "submission" / "usb_package" / "AUDIT_IBM_QPU_RESULTS_UPDATE.md",
        ROOT / "submission" / "usb_package" / "NOTATION_AND_GRAPH_READABILITY_AUDIT.md",
        ROOT / "submission" / "usb_package" / "NOTATION_AND_GRAPH_READABILITY_REPORT.md",
        ROOT / "submission" / "usb_package" / "presentation",
        ROOT / "submission" / "usb_package" / "source_code" / "IBM_QPU_README.md",
        ROOT / "submission" / "usb_package" / "source_code" / "docs" / "IBM_QPU_VALIDATION.md",
        ROOT / "submission" / "usb_package" / "source_code" / "docs" / "IBM_QPU_PROBLEM3B_BASIS_SWEEP.md",
        ROOT / "submission" / "usb_package" / "source_code" / "results" / "ibm_qpu_validation",
        ROOT / "scripts" / "ibm_qpu_smoke_test.py",
        ROOT / "scripts" / "ibm_qpu_problem3b_basis_sweep.py",
        ROOT / "scripts" / "ibm_qpu_extract_p3b_counts.py",
        ROOT / "scripts" / "summarize_ibm_qpu_p3b_results.py",
        ROOT / "scripts" / "copy_ibm_qpu_results_to_usb.py",
    ]

SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".pdf", ".zip", ".pyc"}
ALLOWED_CONTEXT = (
    "QISKIT_IBM_TOKEN",
    "IBM_QUANTUM_TOKEN",
    "QISKIT_IBM_INSTANCE",
    "QISKIT_IBM_CHANNEL",
    "<your-token>",
    "<your-instance-crn>",
    "token_env_set",
    "missing_token_or_instance",
    "Do not commit tokens",
    "No token",
)

PATTERNS = [
    re.compile(r"\b[A-Za-z0-9_\-]{48,}\b"),
    re.compile(r"crn:v1:[A-Za-z0-9:._/\-]+", re.IGNORECASE),
    re.compile(r"(token|api[_-]?key|secret|password)\s*[:=]\s*['\"]?[^'\"\s<>]{12,}", re.IGNORECASE),
]


def iter_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file():
            files.append(root)
        elif root.exists():
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() not in SKIP_SUFFIXES:
                    files.append(path)
    return files


def main() -> None:
    findings: list[tuple[Path, int, str]] = []
    for path in iter_files():
        try:
            if path.suffix.lower() == ".ipynb":
                data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
                text = "\n".join(
                    "".join(cell.get("source", [])) for cell in data.get("cells", [])
                )
                lines = text.splitlines()
            else:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        except json.JSONDecodeError:
            continue
        for line_no, line in enumerate(lines, start=1):
            if any(marker in line for marker in ALLOWED_CONTEXT):
                continue
            if any(pattern.search(line) for pattern in PATTERNS):
                findings.append((path.relative_to(ROOT), line_no, "potential secret-like text"))
    if findings:
        for path, line_no, label in findings[:50]:
            print(f"{path}:{line_no}: {label}")
        raise SystemExit(f"Potential secret-like findings: {len(findings)}")
    print("IBM secret scan OK: no actual token/API key/CRN patterns found in final-facing files")


if __name__ == "__main__":
    main()

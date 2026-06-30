"""Copy IBM QPU appendix scripts, docs, and result files into the USB package."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USB_SOURCE = ROOT / "submission" / "usb_package" / "source_code"


def _copy_file(src: Path, dst: Path, copied: list[Path]) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    copied.append(dst)


def _ignore_sensitive(directory: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        lowered = name.lower()
        if lowered == ".git" or lowered.startswith(".git"):
            ignored.add(name)
        if lowered in {".env", ".env.local", "credentials.json", "token.json"}:
            ignored.add(name)
        if lowered.endswith((".pem", ".key", ".p12")):
            ignored.add(name)
    return ignored


def main() -> int:
    copied: list[Path] = []

    results_src = ROOT / "results" / "ibm_qpu_validation"
    results_dst = USB_SOURCE / "results" / "ibm_qpu_validation"
    if results_src.exists():
        shutil.copytree(
            results_src,
            results_dst,
            dirs_exist_ok=True,
            ignore=_ignore_sensitive,
        )
        copied.append(results_dst)

    scripts_dst = USB_SOURCE / "scripts"
    _copy_file(
        ROOT / "scripts" / "ibm_qpu_problem3b_basis_sweep.py",
        scripts_dst / "ibm_qpu_problem3b_basis_sweep.py",
        copied,
    )
    _copy_file(
        ROOT / "scripts" / "ibm_qpu_extract_p3b_counts.py",
        scripts_dst / "ibm_qpu_extract_p3b_counts.py",
        copied,
    )
    _copy_file(
        ROOT / "scripts" / "summarize_ibm_qpu_p3b_results.py",
        scripts_dst / "summarize_ibm_qpu_p3b_results.py",
        copied,
    )
    _copy_file(
        ROOT / "scripts" / "ibm_qpu_smoke_test.py",
        scripts_dst / "ibm_qpu_smoke_test.py",
        copied,
    )

    docs_dst = USB_SOURCE / "docs"
    _copy_file(
        ROOT / "docs" / "IBM_QPU_PROBLEM3B_BASIS_SWEEP.md",
        docs_dst / "IBM_QPU_PROBLEM3B_BASIS_SWEEP.md",
        copied,
    )
    _copy_file(
        ROOT / "docs" / "IBM_QPU_VALIDATION.md",
        docs_dst / "IBM_QPU_VALIDATION.md",
        copied,
    )

    solution_dst = USB_SOURCE / "solution"
    _copy_file(ROOT / "solution" / "README.md", solution_dst / "README.md", copied)
    _copy_file(ROOT / "solution" / "solution_1.ipynb", solution_dst / "solution_1.ipynb", copied)

    for path in copied:
        print(f"copied: {path.relative_to(ROOT)}")
    print("No .git directory, token file, private key, or .env file was copied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

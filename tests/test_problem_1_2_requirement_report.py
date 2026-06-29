from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_problem_1_2_requirement_report_script_writes_markdown(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    report_path = tmp_path / "problem_1_2_requirement_report.md"
    output_dir = tmp_path / "artifacts"

    completed = subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "problem_1_2_generate_requirement_report.py"),
            "--n-samples",
            "6",
            "--random-steps",
            "2",
            "--hamiltonian-time-points",
            "3",
            "--output-dir",
            str(output_dir),
            "--report-path",
            str(report_path),
        ],
        check=True,
        cwd=root,
        capture_output=True,
        text=True,
    )

    text = report_path.read_text(encoding="utf-8")
    assert "Problem 1/2 Requirement Report" in text
    assert "Requirement Coverage" in text
    assert "Problem 2(d): Resource / Control Proxy" in text
    assert "Wrote requirement report" in completed.stdout
    assert (output_dir / "random_unitary_metrics.csv").exists()
    assert (output_dir / "hamiltonian_metrics.csv").exists()

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import (  # noqa: E402
    three_qubit_hamiltonian,
    three_qubit_hamiltonian_operator,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print Problem 2(a) Hamiltonian diagnostics.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "quantitative_evaluation")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    operator = three_qubit_hamiltonian_operator()
    matrix = three_qubit_hamiltonian()
    terms = operator.to_list()
    hermiticity_error = float(np.linalg.norm(matrix - matrix.conj().T))

    lines = [
        "# Problem 2(a) Hamiltonian Diagnostics",
        "",
        "Qubit order: `M0, M1, F`.",
        "",
        "## Pauli Terms",
        "",
    ]
    for label, coeff in terms:
        lines.append(f"- `{label}`: `{complex(coeff).real:.6f}`")

    lines.extend(
        [
            "",
            "## Matrix Check",
            "",
            f"- matrix shape: `{matrix.shape[0]} x {matrix.shape[1]}`",
            f"- number of Pauli terms: `{len(terms)}`",
            f"- Hermiticity error: `{hermiticity_error:.12f}`",
            "",
        ]
    )
    summary = "\n".join(lines)
    (args.output_dir / "problem_2a_hamiltonian_diagnostics.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

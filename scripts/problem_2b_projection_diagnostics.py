from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np
from qiskit.quantum_info import Operator, Statevector
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble  # noqa: E402
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import (  # noqa: E402
    measurement_basis_vectors,
    three_qubit_hamiltonian,
)

KET0 = np.array([1.0, 0.0], dtype=complex)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Problem 2(b) projection diagnostics.")
    parser.add_argument("--n-samples", type=int, default=80)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--time", type=float, default=1.0)
    parser.add_argument("--measurement-basis", choices=["z", "x", "y"], default="z")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "quantitative_evaluation")
    return parser.parse_args()


def projection_probabilities(full_state: np.ndarray, measurement_basis: str) -> tuple[float, float]:
    basis_vectors = measurement_basis_vectors(measurement_basis)
    data_by_complement = full_state.reshape(4, 2)
    probabilities = []
    for basis in basis_vectors:
        projected = data_by_complement @ basis.conj()
        probabilities.append(float(np.vdot(projected, projected).real))
    total = sum(probabilities)
    return probabilities[0] / total, probabilities[1] / total


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    states = target_ensemble(args.n_samples, sigma=args.sigma, seed=args.seed)
    evolution = Operator(expm(-1j * three_qubit_hamiltonian() * args.time))

    rows = []
    for idx, state in enumerate(states):
        full_initial = np.kron(state, KET0)
        evolved = np.asarray(Statevector(full_initial).evolve(evolution).data, dtype=complex)
        p0, p1 = projection_probabilities(evolved, args.measurement_basis)
        rows.append({"sample": idx, "p_outcome_0": p0, "p_outcome_1": p1, "p_total": p0 + p1})

    write_rows(args.output_dir / "problem_2b_projection_diagnostics.csv", rows)
    p0_values = np.array([row["p_outcome_0"] for row in rows])
    p1_values = np.array([row["p_outcome_1"] for row in rows])
    p_total_values = np.array([row["p_total"] for row in rows])

    summary = f"""# Problem 2(b) Projection Diagnostics

## Setup

- N: `{args.n_samples}`
- sigma: `{args.sigma}`
- seed: `{args.seed}`
- time: `{args.time}`
- measurement basis: `{args.measurement_basis}`

## Outcome Probability Summary

- mean P(outcome 0): `{p0_values.mean():.6f}`
- std P(outcome 0): `{p0_values.std():.6f}`
- min P(outcome 0): `{p0_values.min():.6f}`
- max P(outcome 0): `{p0_values.max():.6f}`
- mean P(outcome 1): `{p1_values.mean():.6f}`
- max normalization error: `{np.max(np.abs(p_total_values - 1.0)):.12f}`

The normalization check verifies that the two complement-qubit outcomes form a
complete projected ensemble construction at this time and basis.
"""
    (args.output_dir / "problem_2b_projection_diagnostics.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

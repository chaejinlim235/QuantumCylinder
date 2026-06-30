from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

from submission.states_and_metrics import distance_to_target, make_target_ensemble, write_csv, write_text


def random_unitary_circuit(angles: np.ndarray, entangler: str = "cz") -> QuantumCircuit:
    """Create one Qiskit random local-rotation + entangler layer."""
    circuit = QuantumCircuit(2)
    for qubit in range(2):
        ax, ay, az = angles[qubit]
        circuit.rx(float(ax), qubit)
        circuit.ry(float(ay), qubit)
        circuit.rz(float(az), qubit)

    if entangler == "cz":
        circuit.cz(0, 1)
    elif entangler == "cnot":
        circuit.cx(0, 1)
    else:
        raise ValueError(f"Unknown entangler: {entangler}")
    return circuit


def _normalize_rows(states: np.ndarray) -> np.ndarray:
    states = np.asarray(states, dtype=complex)
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Cannot normalize an ensemble with a zero vector.")
    return states / norms


def random_unitary_layer(rng: np.random.Generator, angle_scale: float = np.pi, entangler: str = "cz") -> np.ndarray:
    """Sample one Qiskit layer and return its 4x4 unitary matrix."""
    angles = rng.uniform(-angle_scale, angle_scale, size=(2, 3))
    circuit = random_unitary_circuit(angles, entangler=entangler)

    # Convert Qiskit's little-endian convention to the q0-left array convention.
    return np.asarray(Operator(circuit).reverse_qargs().data, dtype=complex)


def random_unitary_trajectory(
    initial: np.ndarray,
    n_steps: int = 12,
    angle_scale: float = np.pi,
    seed: int | None = 8,
    entangler: str = "cz",
) -> list[np.ndarray]:
    """Apply random-unitary layers and return S0, S1, ..., Sn."""
    if n_steps < 0:
        raise ValueError("n_steps must be non-negative.")

    rng = np.random.default_rng(seed)
    current = _normalize_rows(initial)
    trajectory = [current.copy()]

    for _ in range(n_steps):
        next_states = np.empty_like(current)
        for idx, state in enumerate(current):
            unitary = random_unitary_layer(rng, angle_scale=angle_scale, entangler=entangler)
            next_states[idx] = Statevector(state).evolve(Operator(unitary)).data
        current = _normalize_rows(next_states)
        trajectory.append(current.copy())

    return trajectory


def solve_problem_1(
    output_dir: Path,
    n_samples: int = 80,
    sigma: float = 0.10,
    seed: int = 7,
    random_steps: int = 12,
) -> dict:
    """Problem 1: diffuse a target ensemble with Qiskit random-unitary circuit layers."""
    target = make_target_ensemble(n_samples=n_samples, sigma=sigma, seed=seed)

    # Each layer is random RX/RY/RZ on both data qubits followed by one CZ.
    trajectory = random_unitary_trajectory(target, n_steps=random_steps, seed=seed + 1)

    rows = []
    for step, ensemble in enumerate(trajectory):
        metrics = distance_to_target(target, ensemble)
        rows.append({"step": step, **metrics})

    final = rows[-1]
    summary = f"""# Problem 1 Simple Summary

## Physical Operation

- Start from a target ensemble near `|00>`.
- Backend: Qiskit `QuantumCircuit`, `Operator`, and `Statevector`.
- Apply random local `RX/RY/RZ` rotations to both data qubits.
- Add one Qiskit `CZ` entangler per layer.
- Measure diffusion by distance back to the original target ensemble.

## Result

- Samples: `{n_samples}`
- Random layers: `{random_steps}`
- Final MMD: `{final['mmd']:.6f}`
- Final Wasserstein-type distance: `{final['wasserstein']:.6f}`

## Output

- `problem1_random_unitary_metrics.csv`
"""

    write_csv(output_dir / "problem1_random_unitary_metrics.csv", rows)
    write_text(output_dir / "problem1_summary.md", summary)
    return {"rows": rows, "summary": output_dir / "problem1_summary.md", "final": final}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the simple Problem 1 submission layer.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "submission_simple" / "problem1")
    parser.add_argument("--n-samples", type=int, default=80)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--random-steps", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = solve_problem_1(
        args.output_dir,
        n_samples=args.n_samples,
        sigma=args.sigma,
        seed=args.seed,
        random_steps=args.random_steps,
    )
    final = result["final"]
    print(f"Problem 1 final MMD={final['mmd']:.6f}, Wasserstein={final['wasserstein']:.6f}")


if __name__ == "__main__":
    main()

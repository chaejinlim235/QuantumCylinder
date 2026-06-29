from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
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


def random_unitary_resource_proxy(step: int, rotations_per_qubit: int = 3, n_qubits: int = 2) -> dict:
    """Simple circuit/control count for a k-step random-unitary trajectory."""
    return {
        "step": step,
        "single_qubit_rotations": step * rotations_per_qubit * n_qubits,
        "two_qubit_entanglers": step,
        "random_controls": step * rotations_per_qubit * n_qubits,
        "entangler": "CZ",
    }


def _target_summary_row(target: np.ndarray, n_samples: int, sigma: float, seed: int) -> dict:
    ket00 = np.array([1, 0, 0, 0], dtype=complex)
    norms = np.linalg.norm(target, axis=1)
    fidelities_to_00 = np.abs(target @ ket00.conj()) ** 2
    return {
        "n_samples": n_samples,
        "sigma": sigma,
        "seed": seed,
        "norm_min": float(norms.min()),
        "norm_max": float(norms.max()),
        "mean_fidelity_to_00": float(fidelities_to_00.mean()),
        "min_fidelity_to_00": float(fidelities_to_00.min()),
        "max_fidelity_to_00": float(fidelities_to_00.max()),
    }


def _target_sample_rows(target: np.ndarray) -> list[dict]:
    rows = []
    labels = ["00", "01", "10", "11"]
    ket00 = np.array([1, 0, 0, 0], dtype=complex)
    fidelities_to_00 = np.abs(target @ ket00.conj()) ** 2
    for sample_idx, state in enumerate(target):
        row = {
            "sample": sample_idx,
            "norm": float(np.linalg.norm(state)),
            "fidelity_to_00": float(fidelities_to_00[sample_idx]),
        }
        for label, amplitude in zip(labels, state, strict=True):
            row[f"amp_{label}_real"] = float(amplitude.real)
            row[f"amp_{label}_imag"] = float(amplitude.imag)
        rows.append(row)
    return rows


def _metric_check_rows(target: np.ndarray, trajectory: list[np.ndarray]) -> list[dict]:
    checks = [
        ("S0_vs_S0", target, "metric zero check"),
        ("S0_vs_S1", trajectory[min(1, len(trajectory) - 1)], "first diffusion step"),
        ("S0_vs_Sfinal", trajectory[-1], "final diffusion step"),
    ]
    rows = []
    for name, candidate, description in checks:
        rows.append({"comparison": name, "description": description, **distance_to_target(target, candidate)})
    return rows


def _plot_distance_curve(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    ax.plot([row["step"] for row in rows], [row["mmd"] for row in rows], marker="o", label="MMD")
    ax.plot([row["step"] for row in rows], [row["wasserstein"] for row in rows], marker="s", label="Wasserstein")
    ax.set_title("Problem 1 random-unitary diffusion")
    ax.set_xlabel("diffusion step k")
    ax.set_ylabel("distance to S0")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def solve_problem_1(
    output_dir: Path,
    n_samples: int = 80,
    sigma: float = 0.10,
    seed: int = 7,
    random_steps: int = 12,
) -> dict:
    """Problem 1: diffuse a target ensemble with Qiskit random-unitary circuit layers."""
    target = make_target_ensemble(n_samples=n_samples, sigma=sigma, seed=seed)
    target_summary = _target_summary_row(target, n_samples=n_samples, sigma=sigma, seed=seed)

    # Each layer is random RX/RY/RZ on both data qubits followed by one CZ.
    trajectory = random_unitary_trajectory(target, n_steps=random_steps, seed=seed + 1)

    rows = []
    for step, ensemble in enumerate(trajectory):
        metrics = distance_to_target(target, ensemble)
        rows.append({"step": step, **metrics})

    metric_rows = _metric_check_rows(target, trajectory)
    resource_rows = [random_unitary_resource_proxy(step) for step in range(random_steps + 1)]
    plot_path = output_dir / "problem1_distance_curve.png"
    _plot_distance_curve(rows, plot_path)

    final = rows[-1]
    summary = f"""# Problem 1 Simple Summary

This file is a compact answer for Problem 1(a), 1(b), and 1(c), not only the final diffusion number.

## 1(a): Target Ensemble

- Start from a target ensemble near `|00>`.
- Backend: Qiskit `QuantumCircuit`, `Operator`, and `Statevector`.
- Samples: `{n_samples}`
- Sigma: `{sigma}`
- Mean fidelity to `|00>`: `{target_summary['mean_fidelity_to_00']:.6f}`

## 1(b): Distances

- Fidelity: `F(psi, phi) = |<psi|phi>|^2`
- MMD: fidelity-kernel MMD, reported as `sqrt(MMD^2)`
- Wasserstein-type distance: minimum average matching cost with pairwise cost `1 - F`

## 1(c): Random-Unitary Forward Diffusion

- Apply random local `RX/RY/RZ` rotations to both data qubits.
- Add one Qiskit `CZ` entangler per layer.
- Measure diffusion by distance back to the original target ensemble.

## Result

- Samples: `{n_samples}`
- Random layers: `{random_steps}`
- Final MMD: `{final['mmd']:.6f}`
- Final Wasserstein-type distance: `{final['wasserstein']:.6f}`
- Final single-qubit random rotations: `{resource_rows[-1]['single_qubit_rotations']}`
- Final two-qubit entanglers: `{resource_rows[-1]['two_qubit_entanglers']}`

## Output

- `problem1_target_summary.csv`
- `problem1_target_samples.csv`
- `problem1_metric_checks.csv`
- `problem1_random_unitary_metrics.csv`
- `problem1_random_unitary_resources.csv`
- `problem1_distance_curve.png`
"""

    write_csv(output_dir / "problem1_target_summary.csv", [target_summary])
    write_csv(output_dir / "problem1_target_samples.csv", _target_sample_rows(target))
    write_csv(output_dir / "problem1_metric_checks.csv", metric_rows)
    write_csv(output_dir / "problem1_random_unitary_metrics.csv", rows)
    write_csv(output_dir / "problem1_random_unitary_resources.csv", resource_rows)
    write_text(output_dir / "problem1_summary.md", summary)
    return {
        "rows": rows,
        "target_summary": target_summary,
        "metric_rows": metric_rows,
        "resource_rows": resource_rows,
        "plot": plot_path,
        "summary": output_dir / "problem1_summary.md",
        "final": final,
    }


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

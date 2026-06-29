from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector
from scipy.linalg import expm

from submission.states_and_metrics import distance_to_target, make_target_ensemble, write_csv, write_text

KET0 = np.asarray(Statevector.from_label("0").data, dtype=complex)


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
    """Report the simple gate/control proxy for a k-step random-unitary circuit."""
    return {
        "mechanism": "random_unitary",
        "parameter": step,
        "single_qubit_rotations": step * rotations_per_qubit * n_qubits,
        "two_qubit_entanglers": step,
        "random_controls": step * rotations_per_qubit * n_qubits,
        "total_hamiltonian_time": 0.0,
        "fixed_hamiltonian_terms": 0,
        "fixed_hamiltonian_parameters": 0,
        "measurement_basis": "",
    }


def three_qubit_hamiltonian_operator(
    hx: float = 0.8090,
    hy: float = 0.9045,
    j_coupling: float = 1.0,
) -> SparsePauliOp:
    """Create Problem 2's fixed 3-qubit Hamiltonian as a Qiskit Pauli sum."""
    return SparsePauliOp.from_list(
        [
            ("XII", hx),
            ("YII", hy),
            ("IXI", hx),
            ("IYI", hy),
            ("IIX", hx),
            ("IIY", hy),
            ("XXI", j_coupling),
            ("IXX", j_coupling),
        ]
    )


def three_qubit_hamiltonian(hx: float = 0.8090, hy: float = 0.9045, j_coupling: float = 1.0) -> np.ndarray:
    """Return the Hamiltonian matrix with qubit order M0, M1, F."""
    hamiltonian = three_qubit_hamiltonian_operator(hx=hx, hy=hy, j_coupling=j_coupling)
    return np.asarray(hamiltonian.to_matrix(), dtype=complex)


def measurement_basis_vectors(name: str) -> tuple[np.ndarray, np.ndarray]:
    """Return the two complement-qubit basis vectors used for projection."""
    name = name.lower()
    if name == "z":
        return KET0, np.asarray(Statevector.from_label("1").data, dtype=complex)
    if name == "x":
        plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
        minus = np.array([1, -1], dtype=complex) / np.sqrt(2)
        return plus, minus
    if name == "y":
        plus_i = np.array([1, 1j], dtype=complex) / np.sqrt(2)
        minus_i = np.array([1, -1j], dtype=complex) / np.sqrt(2)
        return plus_i, minus_i
    raise ValueError(f"Unknown measurement basis: {name}")


def _project_complement(full_state: np.ndarray, outcome: int, measurement_basis: str) -> tuple[np.ndarray, float]:
    """Project the complement qubit and return the normalized data state."""
    basis = measurement_basis_vectors(measurement_basis)[outcome]
    data_by_complement = full_state.reshape(4, 2)
    projected = data_by_complement @ basis.conj()
    probability = float(np.vdot(projected, projected).real)
    if probability <= 1e-14:
        return np.zeros(4, dtype=complex), 0.0
    normalized_projected = Statevector(projected / np.sqrt(probability)).data
    return np.asarray(normalized_projected, dtype=complex), probability


def hamiltonian_projected_ensemble(
    initial: np.ndarray,
    time: float,
    measurement_basis: str = "z",
    seed: int | None = 9,
    hamiltonian: np.ndarray | None = None,
) -> np.ndarray:
    """Evolve M+F under H, project F, and return the resulting M ensemble."""
    if time < 0:
        raise ValueError("time must be non-negative.")

    rng = np.random.default_rng(seed)
    data_states = _normalize_rows(initial)
    hamiltonian = three_qubit_hamiltonian() if hamiltonian is None else hamiltonian
    evolution = Operator(expm(-1j * hamiltonian * time))
    output = np.empty_like(data_states)

    for idx, data_state in enumerate(data_states):
        full_initial = np.kron(data_state, KET0)
        evolved = np.asarray(Statevector(full_initial).evolve(evolution).data, dtype=complex)

        projected_states = []
        probabilities = []
        for outcome in (0, 1):
            projected, probability = _project_complement(evolved, outcome, measurement_basis)
            projected_states.append(projected)
            probabilities.append(probability)

        probabilities = np.array(probabilities, dtype=float)
        probabilities = probabilities / probabilities.sum()
        sampled_outcome = int(rng.choice([0, 1], p=probabilities))
        output[idx] = projected_states[sampled_outcome]

    return _normalize_rows(output)


def hamiltonian_projected_trajectory(
    initial: np.ndarray,
    times: np.ndarray,
    measurement_basis: str = "z",
    seed: int | None = 9,
) -> list[np.ndarray]:
    """Evaluate Hamiltonian projected diffusion on a list of time points."""
    hamiltonian = three_qubit_hamiltonian()
    return [
        hamiltonian_projected_ensemble(
            initial,
            float(time),
            measurement_basis=measurement_basis,
            seed=None if seed is None else seed + idx,
            hamiltonian=hamiltonian,
        )
        for idx, time in enumerate(times)
    ]


def closest_metric_pair(
    reference_rows: list[dict],
    candidate_rows: list[dict],
    metric: str,
    skip_initial: bool = True,
) -> dict:
    """Find the closest pair of diffusion points under one reported metric."""
    if not reference_rows:
        raise ValueError("reference_rows must not be empty.")
    if not candidate_rows:
        raise ValueError("candidate_rows must not be empty.")

    def eligible(row: dict) -> bool:
        if not skip_initial:
            return True
        return int(row.get("index", -1)) != 0 and abs(float(row.get("parameter", 0.0))) > 1e-12

    reference_candidates = [row for row in reference_rows if eligible(row)]
    candidate_candidates = [row for row in candidate_rows if eligible(row)]
    if not reference_candidates or not candidate_candidates:
        raise ValueError("No eligible non-initial rows to compare.")

    best_reference = reference_candidates[0]
    best_candidate = candidate_candidates[0]
    best_gap = abs(float(best_reference[metric]) - float(best_candidate[metric]))

    for reference_row in reference_candidates:
        for candidate_row in candidate_candidates:
            gap = abs(float(reference_row[metric]) - float(candidate_row[metric]))
            if gap < best_gap:
                best_reference = reference_row
                best_candidate = candidate_row
                best_gap = gap

    return {
        "metric": metric,
        "reference_index": int(best_reference["index"]),
        "reference_parameter_name": best_reference["parameter_name"],
        "reference_parameter": float(best_reference["parameter"]),
        "reference_metric_value": float(best_reference[metric]),
        "candidate_index": int(best_candidate["index"]),
        "candidate_parameter_name": best_candidate["parameter_name"],
        "candidate_parameter": float(best_candidate["parameter"]),
        "candidate_metric_value": float(best_candidate[metric]),
        "absolute_gap": float(best_gap),
    }


def hamiltonian_resource_proxy(time: float, measurement_basis: str = "z") -> dict:
    return {
        "mechanism": "hamiltonian_projected",
        "parameter": time,
        "single_qubit_rotations": 0,
        "two_qubit_entanglers": 0,
        "random_controls": 0,
        "total_hamiltonian_time": time,
        "fixed_hamiltonian_terms": 8,
        "fixed_hamiltonian_parameters": 3,
        "measurement_basis": measurement_basis,
    }


def _distance_rows(target: np.ndarray, trajectory: list[np.ndarray], parameters: list[float], name: str) -> list[dict]:
    rows = []
    for index, (parameter, ensemble) in enumerate(zip(parameters, trajectory, strict=True)):
        rows.append(
            {
                "index": index,
                "parameter_name": name,
                "parameter": float(parameter),
                **distance_to_target(target, ensemble),
            }
        )
    return rows


def solve_problem_2(
    output_dir: Path,
    n_samples: int = 80,
    sigma: float = 0.10,
    seed: int = 7,
    random_steps: int = 12,
    t_max: float = 4.0,
    time_points: int = 13,
    measurement_basis: str = "z",
) -> dict:
    """Problem 2: Qiskit-backed Hamiltonian evolution plus complement projection."""
    target = make_target_ensemble(n_samples=n_samples, sigma=sigma, seed=seed)

    random_trajectory = random_unitary_trajectory(target, n_steps=random_steps, seed=seed + 1)
    random_rows = _distance_rows(target, random_trajectory, list(range(random_steps + 1)), "random_step")

    # Fixed Hamiltonian acts on M0, M1, F. Projection of F returns a 2-qubit ensemble.
    times = np.linspace(0.0, t_max, time_points)
    projected_trajectory = hamiltonian_projected_trajectory(
        target,
        times=times,
        measurement_basis=measurement_basis,
        seed=seed + 2,
    )
    hamiltonian_rows = _distance_rows(target, projected_trajectory, list(times), "time")

    resource_rows = []
    for metric in ("mmd", "wasserstein"):
        match = closest_metric_pair(random_rows, hamiltonian_rows, metric=metric)
        random_step = int(round(random_rows[match["reference_index"]]["parameter"]))
        hamiltonian_time = float(hamiltonian_rows[match["candidate_index"]]["parameter"])
        resource_rows.append(
            {
                "matched_by": metric,
                "random_step": random_step,
                "hamiltonian_time": hamiltonian_time,
                "metric_gap": float(match["absolute_gap"]),
                **random_unitary_resource_proxy(random_step),
                **{
                    f"hamiltonian_{key}": value
                    for key, value in hamiltonian_resource_proxy(
                        hamiltonian_time,
                        measurement_basis=measurement_basis,
                    ).items()
                },
            }
        )

    max_mmd = max(hamiltonian_rows, key=lambda row: row["mmd"])
    max_wasserstein = max(hamiltonian_rows, key=lambda row: row["wasserstein"])
    summary = f"""# Problem 2 Simple Summary

## Physical Operation

- Add one complement qubit `F` initialized as `|0>`.
- Backend: Qiskit `SparsePauliOp`, `Operator`, and `Statevector`.
- Evolve the three-qubit system `(M0, M1, F)` under the fixed Hamiltonian.
- Measure/project `F` in the `{measurement_basis.upper()}` basis.
- Keep the projected two-qubit data state as the new ensemble sample.

## Result

- Max MMD: `{max_mmd['mmd']:.6f}` at time `{max_mmd['parameter']:.6f}`
- Max Wasserstein-type distance: `{max_wasserstein['wasserstein']:.6f}` at time `{max_wasserstein['parameter']:.6f}`

## Comparable Strength

The file `problem2_resource_matches.csv` matches random-unitary and Hamiltonian-projected points with similar diffusion strength.

## Output

- `problem2_hamiltonian_projection_metrics.csv`
- `problem2_resource_matches.csv`
"""

    write_csv(output_dir / "problem2_hamiltonian_projection_metrics.csv", hamiltonian_rows)
    write_csv(output_dir / "problem2_resource_matches.csv", resource_rows)
    write_text(output_dir / "problem2_summary.md", summary)
    return {
        "rows": hamiltonian_rows,
        "resource_rows": resource_rows,
        "summary": output_dir / "problem2_summary.md",
        "max_mmd": max_mmd,
        "max_wasserstein": max_wasserstein,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the simple Problem 2 submission layer.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "submission_simple" / "problem2")
    parser.add_argument("--n-samples", type=int, default=80)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--random-steps", type=int, default=12)
    parser.add_argument("--t-max", type=float, default=4.0)
    parser.add_argument("--time-points", type=int, default=13)
    parser.add_argument("--measurement-basis", choices=["z", "x", "y"], default="z")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = solve_problem_2(
        args.output_dir,
        n_samples=args.n_samples,
        sigma=args.sigma,
        seed=args.seed,
        random_steps=args.random_steps,
        t_max=args.t_max,
        time_points=args.time_points,
        measurement_basis=args.measurement_basis,
    )
    max_mmd = result["max_mmd"]
    print(f"Problem 2 max MMD={max_mmd['mmd']:.6f} at t={max_mmd['parameter']:.6f}")


if __name__ == "__main__":
    main()

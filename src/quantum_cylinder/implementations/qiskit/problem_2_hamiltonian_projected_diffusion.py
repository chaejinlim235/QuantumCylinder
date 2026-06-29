from __future__ import annotations

import numpy as np
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector
from scipy.linalg import expm

KET0 = np.asarray(Statevector.from_label("0").data, dtype=complex)


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


def _normalize_rows(states: np.ndarray) -> np.ndarray:
    states = np.asarray(states, dtype=complex)
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Cannot normalize an ensemble with a zero vector.")
    return states / norms


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

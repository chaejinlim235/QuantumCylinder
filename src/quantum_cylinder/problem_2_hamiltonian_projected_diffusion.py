from __future__ import annotations

import numpy as np
from scipy.linalg import expm

from quantum_cylinder.quantum_ops import (
    KET0,
    X,
    Y,
    Array,
    normalize,
    normalize_rows,
    one_qubit_operator,
    two_qubit_product_operator,
)


def three_qubit_hamiltonian(hx: float = 0.8090, hy: float = 0.9045, j_coupling: float = 1.0) -> Array:
    """Hamiltonian from Problem 2 with qubit order M0, M1, F."""
    n_qubits = 3
    hamiltonian = np.zeros((2**n_qubits, 2**n_qubits), dtype=complex)
    for qubit in range(n_qubits):
        hamiltonian += hx * one_qubit_operator(X, qubit, n_qubits)
        hamiltonian += hy * one_qubit_operator(Y, qubit, n_qubits)
    for qubit in range(n_qubits - 1):
        hamiltonian += j_coupling * two_qubit_product_operator(X, qubit, X, qubit + 1, n_qubits)
    return hamiltonian


def measurement_basis_vectors(name: str) -> tuple[Array, Array]:
    name = name.lower()
    if name == "z":
        return KET0, np.array([0, 1], dtype=complex)
    if name == "x":
        plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
        minus = np.array([1, -1], dtype=complex) / np.sqrt(2)
        return plus, minus
    if name == "y":
        plus_i = np.array([1, 1j], dtype=complex) / np.sqrt(2)
        minus_i = np.array([1, -1j], dtype=complex) / np.sqrt(2)
        return plus_i, minus_i
    raise ValueError(f"Unknown measurement basis: {name}")


def _project_complement(full_state: Array, outcome: int, measurement_basis: str) -> tuple[Array, float]:
    basis = measurement_basis_vectors(measurement_basis)[outcome]
    data_by_complement = full_state.reshape(4, 2)
    projected = data_by_complement @ basis.conj()
    probability = float(np.vdot(projected, projected).real)
    if probability <= 1e-14:
        return np.zeros(4, dtype=complex), 0.0
    return normalize(projected), probability


def hamiltonian_projected_ensemble(
    initial: Array,
    time: float,
    measurement_basis: str = "z",
    seed: int | None = 9,
    hamiltonian: Array | None = None,
) -> Array:
    """Diffuse the Problem 1 two-qubit ensemble via Problem 2 projected dynamics."""
    if time < 0:
        raise ValueError("time must be non-negative.")
    rng = np.random.default_rng(seed)
    data_states = normalize_rows(initial)
    hamiltonian = three_qubit_hamiltonian() if hamiltonian is None else hamiltonian
    evolution = expm(-1j * hamiltonian * time)
    output = np.empty_like(data_states)

    for idx, data_state in enumerate(data_states):
        full_initial = np.kron(data_state, KET0)
        evolved = evolution @ full_initial
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

    return normalize_rows(output)


def hamiltonian_projected_trajectory(
    initial: Array,
    times: Array,
    measurement_basis: str = "z",
    seed: int | None = 9,
) -> list[Array]:
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

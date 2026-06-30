from __future__ import annotations

import numpy as np
from scipy.linalg import expm

I2 = np.array([[1, 0], [0, 1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
KET0 = np.array([1, 0], dtype=complex)


def _normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("Cannot normalize a zero vector.")
    return state / norm


def _normalize_rows(states: np.ndarray) -> np.ndarray:
    states = np.asarray(states, dtype=complex)
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Cannot normalize an ensemble with a zero vector.")
    return states / norms


def _kron_all(ops: list[np.ndarray]) -> np.ndarray:
    out = np.asarray(ops[0], dtype=complex)
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def _one_qubit_operator(op: np.ndarray, qubit: int, n_qubits: int) -> np.ndarray:
    if not 0 <= qubit < n_qubits:
        raise ValueError(f"qubit must be in [0, {n_qubits}), got {qubit}.")
    ops = [I2] * n_qubits
    ops[qubit] = op
    return _kron_all(ops)


def _two_qubit_product_operator(
    op_a: np.ndarray,
    qubit_a: int,
    op_b: np.ndarray,
    qubit_b: int,
    n_qubits: int,
) -> np.ndarray:
    if qubit_a == qubit_b:
        raise ValueError("qubit_a and qubit_b must be different.")
    ops = [I2] * n_qubits
    ops[qubit_a] = op_a
    ops[qubit_b] = op_b
    return _kron_all(ops)


def three_qubit_hamiltonian(hx: float = 0.8090, hy: float = 0.9045, j_coupling: float = 1.0) -> np.ndarray:
    """Hamiltonian from Problem 2 with qubit order M0, M1, F."""
    n_qubits = 3
    hamiltonian = np.zeros((2**n_qubits, 2**n_qubits), dtype=complex)
    for qubit in range(n_qubits):
        hamiltonian += hx * _one_qubit_operator(X, qubit, n_qubits)
        hamiltonian += hy * _one_qubit_operator(Y, qubit, n_qubits)
    for qubit in range(n_qubits - 1):
        hamiltonian += j_coupling * _two_qubit_product_operator(X, qubit, X, qubit + 1, n_qubits)
    return hamiltonian


def measurement_basis_vectors(name: str) -> tuple[np.ndarray, np.ndarray]:
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


def _project_complement(full_state: np.ndarray, outcome: int, measurement_basis: str) -> tuple[np.ndarray, float]:
    basis = measurement_basis_vectors(measurement_basis)[outcome]
    data_by_complement = full_state.reshape(4, 2)
    projected = data_by_complement @ basis.conj()
    probability = float(np.vdot(projected, projected).real)
    if probability <= 1e-14:
        return np.zeros(4, dtype=complex), 0.0
    return _normalize(projected), probability


def hamiltonian_projected_ensemble(
    initial: np.ndarray,
    time: float,
    measurement_basis: str = "z",
    seed: int | None = 9,
    hamiltonian: np.ndarray | None = None,
) -> np.ndarray:
    """Diffuse the Problem 1 two-qubit ensemble via NumPy/SciPy projected dynamics."""
    if time < 0:
        raise ValueError("time must be non-negative.")
    rng = np.random.default_rng(seed)
    data_states = _normalize_rows(initial)
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

    return _normalize_rows(output)


def hamiltonian_projected_trajectory(
    initial: np.ndarray,
    times: np.ndarray,
    measurement_basis: str = "z",
    seed: int | None = 9,
) -> list[np.ndarray]:
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

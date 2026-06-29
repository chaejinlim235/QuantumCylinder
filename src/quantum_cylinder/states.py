from __future__ import annotations

import numpy as np

Array = np.ndarray

I2 = np.array([[1, 0], [0, 1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

KET0 = np.array([1, 0], dtype=complex)
KET1 = np.array([0, 1], dtype=complex)


def normalize(state: Array) -> Array:
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("Cannot normalize a zero vector.")
    return state / norm


def normalize_rows(states: Array) -> Array:
    states = np.asarray(states, dtype=complex)
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Cannot normalize an ensemble with a zero vector.")
    return states / norms


def rx(theta: float) -> Array:
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)


def ry(theta: float) -> Array:
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def rz(theta: float) -> Array:
    return np.array(
        [[np.exp(-0.5j * theta), 0], [0, np.exp(0.5j * theta)]],
        dtype=complex,
    )


def kron_all(ops: list[Array]) -> Array:
    out = np.asarray(ops[0], dtype=complex)
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def one_qubit_operator(op: Array, qubit: int, n_qubits: int) -> Array:
    if not 0 <= qubit < n_qubits:
        raise ValueError(f"qubit must be in [0, {n_qubits}), got {qubit}.")
    ops = [I2] * n_qubits
    ops[qubit] = op
    return kron_all(ops)


def two_qubit_product_operator(op_a: Array, qubit_a: int, op_b: Array, qubit_b: int, n_qubits: int) -> Array:
    if qubit_a == qubit_b:
        raise ValueError("qubit_a and qubit_b must be different.")
    ops = [I2] * n_qubits
    ops[qubit_a] = op_a
    ops[qubit_b] = op_b
    return kron_all(ops)


def target_ensemble(n_samples: int = 80, sigma: float = 0.10, seed: int | None = 7) -> Array:
    """Generate the two-qubit target ensemble clustered around |00>."""
    if n_samples <= 0:
        raise ValueError("n_samples must be positive.")
    rng = np.random.default_rng(seed)
    base = np.array([1, 0, 0, 0], dtype=complex)
    states = np.empty((n_samples, 4), dtype=complex)

    deltas = rng.normal(loc=0.0, scale=sigma, size=(n_samples, 2, 2))
    for sample_idx in range(n_samples):
        q0 = rz(deltas[sample_idx, 0, 1]) @ ry(deltas[sample_idx, 0, 0])
        q1 = rz(deltas[sample_idx, 1, 1]) @ ry(deltas[sample_idx, 1, 0])
        states[sample_idx] = np.kron(q0, q1) @ base
    return normalize_rows(states)

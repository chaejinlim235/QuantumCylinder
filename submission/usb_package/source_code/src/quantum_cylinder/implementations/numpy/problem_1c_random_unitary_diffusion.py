from __future__ import annotations

import numpy as np

CZ = np.diag([1, 1, 1, -1]).astype(complex)
CNOT_01 = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)


def _normalize_rows(states: np.ndarray) -> np.ndarray:
    states = np.asarray(states, dtype=complex)
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Cannot normalize an ensemble with a zero vector.")
    return states / norms


def _rx(theta: float) -> np.ndarray:
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)


def _ry(theta: float) -> np.ndarray:
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def _rz(theta: float) -> np.ndarray:
    return np.array(
        [[np.exp(-0.5j * theta), 0], [0, np.exp(0.5j * theta)]],
        dtype=complex,
    )


def random_unitary_layer(rng: np.random.Generator, angle_scale: float = np.pi, entangler: str = "cz") -> np.ndarray:
    """One Problem 1 scrambling layer using NumPy matrices."""
    angles = rng.uniform(-angle_scale, angle_scale, size=(2, 3))
    local_ops = []
    for qubit in range(2):
        ax, ay, az = angles[qubit]
        local_ops.append(_rz(az) @ _ry(ay) @ _rx(ax))

    local = np.kron(local_ops[0], local_ops[1])
    if entangler == "cz":
        entangling = CZ
    elif entangler == "cnot":
        entangling = CNOT_01
    else:
        raise ValueError(f"Unknown entangler: {entangler}")
    return entangling @ local


def random_unitary_trajectory(
    initial: np.ndarray,
    n_steps: int = 12,
    angle_scale: float = np.pi,
    seed: int | None = 8,
    entangler: str = "cz",
) -> list[np.ndarray]:
    """Generate the Problem 1 trajectory S0, S1, ..., Sn."""
    if n_steps < 0:
        raise ValueError("n_steps must be non-negative.")
    rng = np.random.default_rng(seed)
    current = _normalize_rows(initial)
    trajectory = [current.copy()]

    for _ in range(n_steps):
        next_states = np.empty_like(current)
        for idx, state in enumerate(current):
            unitary = random_unitary_layer(rng, angle_scale=angle_scale, entangler=entangler)
            next_states[idx] = unitary @ state
        current = _normalize_rows(next_states)
        trajectory.append(current.copy())

    return trajectory


def random_unitary_resource_proxy(step: int, rotations_per_qubit: int = 3, n_qubits: int = 2) -> dict:
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

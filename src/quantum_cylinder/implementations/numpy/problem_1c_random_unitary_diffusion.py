from __future__ import annotations

import numpy as np

from quantum_cylinder.quantum_ops import Array, normalize_rows, rx, ry, rz

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


def random_unitary_layer(rng: np.random.Generator, angle_scale: float = np.pi, entangler: str = "cz") -> Array:
    """One Problem 1 scrambling layer using NumPy matrices."""
    angles = rng.uniform(-angle_scale, angle_scale, size=(2, 3))
    local_ops = []
    for qubit in range(2):
        ax, ay, az = angles[qubit]
        local_ops.append(rz(az) @ ry(ay) @ rx(ax))

    local = np.kron(local_ops[0], local_ops[1])
    if entangler == "cz":
        entangling = CZ
    elif entangler == "cnot":
        entangling = CNOT_01
    else:
        raise ValueError(f"Unknown entangler: {entangler}")
    return entangling @ local


def random_unitary_trajectory(
    initial: Array,
    n_steps: int = 12,
    angle_scale: float = np.pi,
    seed: int | None = 8,
    entangler: str = "cz",
) -> list[Array]:
    """Generate the Problem 1 trajectory S0, S1, ..., Sn."""
    if n_steps < 0:
        raise ValueError("n_steps must be non-negative.")
    rng = np.random.default_rng(seed)
    current = normalize_rows(initial)
    trajectory = [current.copy()]

    for _ in range(n_steps):
        next_states = np.empty_like(current)
        for idx, state in enumerate(current):
            unitary = random_unitary_layer(rng, angle_scale=angle_scale, entangler=entangler)
            next_states[idx] = unitary @ state
        current = normalize_rows(next_states)
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

from __future__ import annotations

import numpy as np
from scipy.linalg import expm

from quantum_cylinder.states import (
    I2,
    KET0,
    X,
    Y,
    Array,
    kron_all,
    normalize,
    normalize_rows,
    one_qubit_operator,
    rx,
    ry,
    rz,
    two_qubit_product_operator,
)

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
    """One simplified scrambling layer: random local rotations plus one entangler."""
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
    """Generate S0, S1, ..., Sn by sample-wise random-unitary scrambling."""
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
    """Diffuse the two-qubit ensemble via three-qubit evolution and projection.

    The complement qubit starts in |0>. One projected outcome is sampled per
    input state so the ensemble size stays fixed.
    """
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


def random_unitary_resource_proxy(step: int, rotations_per_qubit: int = 3, n_qubits: int = 2) -> dict:
    return {
        "mechanism": "random_unitary",
        "parameter": step,
        "single_qubit_rotations": step * rotations_per_qubit * n_qubits,
        "two_qubit_entanglers": step,
        "random_controls": step * rotations_per_qubit * n_qubits,
        "total_hamiltonian_time": 0.0,
        "fixed_hamiltonian_terms": 0,
        "measurement_basis": "",
    }

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from quantum_cylinder.quantum_ops import Array, normalize_rows


def random_unitary_circuit(angles: Array, entangler: str = "cz") -> QuantumCircuit:
    """Build one Qiskit random-unitary scrambling circuit."""
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


def _operator_data(circuit: QuantumCircuit) -> Array:
    # Convert Qiskit's little-endian qubit convention to the repository's
    # q0-left array convention used by the metric and projection code.
    return np.asarray(Operator(circuit).reverse_qargs().data, dtype=complex)


def random_unitary_layer(rng: np.random.Generator, angle_scale: float = np.pi, entangler: str = "cz") -> Array:
    """One Problem 1 scrambling layer using Qiskit."""
    angles = rng.uniform(-angle_scale, angle_scale, size=(2, 3))
    return _operator_data(random_unitary_circuit(angles, entangler=entangler))


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

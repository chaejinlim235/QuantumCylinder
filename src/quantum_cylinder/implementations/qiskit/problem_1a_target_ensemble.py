from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_cylinder.quantum_ops import Array, normalize_rows


def target_state_circuit(delta_y: Array, delta_z: Array) -> QuantumCircuit:
    """Build the Qiskit circuit for one target ensemble sample."""
    circuit = QuantumCircuit(2)
    for qubit in range(2):
        circuit.ry(float(delta_y[qubit]), qubit)
        circuit.rz(float(delta_z[qubit]), qubit)
    return circuit


def _statevector_data(circuit: QuantumCircuit) -> Array:
    # Qiskit stores amplitudes in little-endian qubit order; the project arrays
    # use q0 as the left-most data qubit, so reverse before returning.
    return np.asarray(Statevector.from_instruction(circuit).reverse_qargs().data, dtype=complex)


def target_ensemble(n_samples: int = 80, sigma: float = 0.10, seed: int | None = 7) -> Array:
    """Generate the Problem 1 two-qubit target ensemble with Qiskit."""
    if n_samples <= 0:
        raise ValueError("n_samples must be positive.")
    rng = np.random.default_rng(seed)
    states = np.empty((n_samples, 4), dtype=complex)

    deltas = rng.normal(loc=0.0, scale=sigma, size=(n_samples, 2, 2))
    for sample_idx in range(n_samples):
        circuit = target_state_circuit(
            delta_y=deltas[sample_idx, :, 0],
            delta_z=deltas[sample_idx, :, 1],
        )
        states[sample_idx] = _statevector_data(circuit)
    return normalize_rows(states)

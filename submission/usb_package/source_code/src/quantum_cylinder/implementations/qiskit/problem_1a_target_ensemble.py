from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def target_state_circuit(delta_y: np.ndarray, delta_z: np.ndarray) -> QuantumCircuit:
    """Create one 2-qubit target-state circuit around |00>."""
    circuit = QuantumCircuit(2)
    for qubit in range(2):
        circuit.ry(float(delta_y[qubit]), qubit)
        circuit.rz(float(delta_z[qubit]), qubit)
    return circuit


def target_ensemble(n_samples: int = 80, sigma: float = 0.10, seed: int | None = 7) -> np.ndarray:
    """Generate Problem 1(a)'s target ensemble as an (N, 4) state array."""
    if n_samples <= 0:
        raise ValueError("n_samples must be positive.")

    rng = np.random.default_rng(seed)
    states = np.empty((n_samples, 4), dtype=complex)

    for sample_idx in range(n_samples):
        deltas = rng.normal(loc=0.0, scale=sigma, size=(2, 2))
        delta_y = deltas[:, 0]
        delta_z = deltas[:, 1]
        circuit = target_state_circuit(delta_y, delta_z)

        # Qiskit returns little-endian amplitudes. The rest of the repo uses
        # q0 as the left-most qubit, so reverse the qubit order once here.
        state = Statevector.from_instruction(circuit).reverse_qargs()
        states[sample_idx] = np.asarray(state.data, dtype=complex)

    return states

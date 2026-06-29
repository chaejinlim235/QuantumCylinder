from __future__ import annotations

import numpy as np
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector
from scipy.linalg import expm

from quantum_cylinder.quantum_ops import (
    KET0,
    Array,
    normalize,
    normalize_rows,
)


def three_qubit_hamiltonian_operator(
    hx: float = 0.8090,
    hy: float = 0.9045,
    j_coupling: float = 1.0,
) -> SparsePauliOp:
    """Hamiltonian from Problem 2 as a Qiskit Pauli operator.

    Pauli labels are written in the repository's q0-left convention:
    `M0, M1, F`.
    """
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


def three_qubit_hamiltonian(hx: float = 0.8090, hy: float = 0.9045, j_coupling: float = 1.0) -> Array:
    """Hamiltonian from Problem 2 with qubit order M0, M1, F."""
    return np.asarray(
        three_qubit_hamiltonian_operator(
            hx=hx,
            hy=hy,
            j_coupling=j_coupling,
        ).to_matrix(),
        dtype=complex,
    )


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
    """Diffuse the Problem 1 two-qubit ensemble via Qiskit projected dynamics."""
    if time < 0:
        raise ValueError("time must be non-negative.")
    rng = np.random.default_rng(seed)
    data_states = normalize_rows(initial)
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

from __future__ import annotations

import numpy as np

PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def _normalize_state(state: np.ndarray) -> np.ndarray:
    state = np.asarray(state, dtype=complex).reshape(4)
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("Cannot normalize a zero state.")
    return state / norm


def reduced_density_matrix(state: np.ndarray, qubit: int) -> np.ndarray:
    """Return a one-qubit reduced density matrix for a two-qubit pure state.

    The project uses row vectors ordered as |00>, |01>, |10>, |11>, so qubit 0
    is the left/data-M0 qubit and qubit 1 is the right/data-M1 qubit.
    """
    if qubit not in {0, 1}:
        raise ValueError("qubit must be 0 or 1.")

    amplitudes = _normalize_state(state).reshape(2, 2)
    if qubit == 0:
        return amplitudes @ amplitudes.conj().T
    return amplitudes.T @ amplitudes.conj()


def bloch_vector(state: np.ndarray, qubit: int) -> np.ndarray:
    """Return <X>, <Y>, <Z> for one qubit of a two-qubit pure state."""
    rho = reduced_density_matrix(state, qubit=qubit)
    return np.array(
        [
            np.trace(rho @ PAULI_X).real,
            np.trace(rho @ PAULI_Y).real,
            np.trace(rho @ PAULI_Z).real,
        ],
        dtype=float,
    )


def ensemble_bloch_vectors(states: np.ndarray, qubit: int) -> np.ndarray:
    """Return Bloch vectors for every state in an ensemble."""
    states = np.asarray(states, dtype=complex)
    return np.vstack([bloch_vector(state, qubit=qubit) for state in states])


def summarize_bloch_vectors(vectors: np.ndarray) -> dict:
    """Summarize a Bloch-vector cloud for diagnostic reporting."""
    vectors = np.asarray(vectors, dtype=float)
    norms = np.linalg.norm(vectors, axis=1)
    mean = vectors.mean(axis=0)
    return {
        "mean_x": float(mean[0]),
        "mean_y": float(mean[1]),
        "mean_z": float(mean[2]),
        "mean_radius": float(norms.mean()),
        "std_radius": float(norms.std()),
    }

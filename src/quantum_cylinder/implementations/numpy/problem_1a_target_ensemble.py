from __future__ import annotations

import numpy as np


def _normalize_rows(states: np.ndarray) -> np.ndarray:
    states = np.asarray(states, dtype=complex)
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Cannot normalize an ensemble with a zero vector.")
    return states / norms


def _ry(theta: float) -> np.ndarray:
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def _rz(theta: float) -> np.ndarray:
    return np.array(
        [[np.exp(-0.5j * theta), 0], [0, np.exp(0.5j * theta)]],
        dtype=complex,
    )


def target_ensemble(n_samples: int = 80, sigma: float = 0.10, seed: int | None = 7) -> np.ndarray:
    """Generate the Problem 1 two-qubit target ensemble with NumPy matrices."""
    if n_samples <= 0:
        raise ValueError("n_samples must be positive.")
    rng = np.random.default_rng(seed)
    base = np.array([1, 0, 0, 0], dtype=complex)
    states = np.empty((n_samples, 4), dtype=complex)

    deltas = rng.normal(loc=0.0, scale=sigma, size=(n_samples, 2, 2))
    for sample_idx in range(n_samples):
        q0 = _rz(deltas[sample_idx, 0, 1]) @ _ry(deltas[sample_idx, 0, 0])
        q1 = _rz(deltas[sample_idx, 1, 1]) @ _ry(deltas[sample_idx, 1, 0])
        states[sample_idx] = np.kron(q0, q1) @ base
    return _normalize_rows(states)

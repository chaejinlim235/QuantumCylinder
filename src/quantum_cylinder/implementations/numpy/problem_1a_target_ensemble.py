from __future__ import annotations

import numpy as np

from quantum_cylinder.quantum_ops import Array, normalize_rows, ry, rz


def target_ensemble(n_samples: int = 80, sigma: float = 0.10, seed: int | None = 7) -> Array:
    """Generate the Problem 1 two-qubit target ensemble with NumPy matrices."""
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

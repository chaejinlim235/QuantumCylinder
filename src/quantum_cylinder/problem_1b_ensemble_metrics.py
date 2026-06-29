from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment, linprog


def _normalize_rows(states: np.ndarray) -> np.ndarray:
    states = np.asarray(states, dtype=complex)
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Cannot normalize an ensemble with a zero vector.")
    return states / norms


def fidelity_matrix(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Pairwise pure-state fidelity matrix for row-wise state ensembles."""
    left = _normalize_rows(left)
    right = _normalize_rows(right)
    overlaps = left @ right.conj().T
    return np.clip(np.abs(overlaps) ** 2, 0.0, 1.0)


def mmd_fidelity(left: np.ndarray, right: np.ndarray) -> float:
    """Biased MMD with the fidelity kernel."""
    k_xx = fidelity_matrix(left, left)
    k_yy = fidelity_matrix(right, right)
    k_xy = fidelity_matrix(left, right)
    mmd_sq = float(k_xx.mean() + k_yy.mean() - 2.0 * k_xy.mean())
    return float(np.sqrt(max(mmd_sq, 0.0)))


def wasserstein_infidelity(left: np.ndarray, right: np.ndarray) -> float:
    """Uniform ensemble OT distance with cost 1 - fidelity.

    For equal-size ensembles, this is the minimum average matching cost.
    For unequal-size ensembles, it solves the balanced transport LP.
    """
    cost = 1.0 - fidelity_matrix(left, right)
    n_left, n_right = cost.shape

    if n_left == n_right:
        rows, cols = linear_sum_assignment(cost)
        return float(cost[rows, cols].mean())

    supply = np.full(n_left, 1.0 / n_left)
    demand = np.full(n_right, 1.0 / n_right)
    c = cost.reshape(-1)

    constraints = []
    rhs = []
    for i in range(n_left):
        row = np.zeros((n_left, n_right))
        row[i, :] = 1.0
        constraints.append(row.reshape(-1))
        rhs.append(supply[i])
    for j in range(n_right):
        col = np.zeros((n_left, n_right))
        col[:, j] = 1.0
        constraints.append(col.reshape(-1))
        rhs.append(demand[j])

    result = linprog(c, A_eq=np.vstack(constraints), b_eq=np.array(rhs), bounds=(0, None), method="highs")
    if not result.success:
        raise RuntimeError(f"Optimal transport LP failed: {result.message}")
    return float(result.fun)

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from scipy.optimize import linear_sum_assignment, linprog


def target_state_circuit(delta_y: np.ndarray, delta_z: np.ndarray) -> QuantumCircuit:
    """Create one 2-qubit target-state circuit around |00>."""
    circuit = QuantumCircuit(2)
    for qubit in range(2):
        circuit.ry(float(delta_y[qubit]), qubit)
        circuit.rz(float(delta_z[qubit]), qubit)
    return circuit


def target_ensemble(n_samples: int = 80, sigma: float = 0.10, seed: int | None = 7) -> np.ndarray:
    """Generate Problem 1(a)'s Qiskit target ensemble as an (N, 4) array."""
    if n_samples <= 0:
        raise ValueError("n_samples must be positive.")

    rng = np.random.default_rng(seed)
    states = np.empty((n_samples, 4), dtype=complex)

    for sample_idx in range(n_samples):
        deltas = rng.normal(loc=0.0, scale=sigma, size=(2, 2))
        delta_y = deltas[:, 0]
        delta_z = deltas[:, 1]
        circuit = target_state_circuit(delta_y, delta_z)

        # Qiskit uses little-endian amplitudes. The submission arrays use q0 as
        # the left-most qubit, so reverse the qubit order once here.
        state = Statevector.from_instruction(circuit).reverse_qargs()
        states[sample_idx] = np.asarray(state.data, dtype=complex)

    return states


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
    """Uniform ensemble OT distance with cost 1 - fidelity."""
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


def make_target_ensemble(n_samples: int = 80, sigma: float = 0.10, seed: int = 7) -> np.ndarray:
    """Problem 1(a): Qiskit Statevector states near |00>."""
    return target_ensemble(n_samples=n_samples, sigma=sigma, seed=seed)


def distance_to_target(target: np.ndarray, candidate: np.ndarray) -> dict[str, float]:
    """Use the same two metrics for all three problems."""
    return {
        "mmd": float(mmd_fidelity(target, candidate)),
        "wasserstein": float(wasserstein_infidelity(target, candidate)),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

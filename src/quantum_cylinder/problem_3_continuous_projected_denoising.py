from __future__ import annotations

import math
from collections.abc import Iterable

import numpy as np
from scipy.linalg import expm

from quantum_cylinder.problem_1b_ensemble_metrics import fidelity_matrix, mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import three_qubit_hamiltonian
from quantum_cylinder.quantum_ops import Array, KET0, normalize_rows


def continuous_projection_basis(theta: float, phi: float) -> Array:
    """Return cos(theta/2)|0> + exp(i phi) sin(theta/2)|1>."""
    return np.array([np.cos(theta / 2.0), np.exp(1j * phi) * np.sin(theta / 2.0)], dtype=complex)


def axis_basis_specs() -> list[dict]:
    """Named Z/X/Y projection outcomes used as a non-continuous baseline."""
    return [
        {"basis_name": "z_plus", "theta": 0.0, "phi": 0.0, "basis_family": "axis"},
        {"basis_name": "z_minus", "theta": float(np.pi), "phi": 0.0, "basis_family": "axis"},
        {"basis_name": "x_plus", "theta": float(np.pi / 2.0), "phi": 0.0, "basis_family": "axis"},
        {"basis_name": "x_minus", "theta": float(np.pi / 2.0), "phi": float(np.pi), "basis_family": "axis"},
        {"basis_name": "y_plus", "theta": float(np.pi / 2.0), "phi": float(np.pi / 2.0), "basis_family": "axis"},
        {"basis_name": "y_minus", "theta": float(np.pi / 2.0), "phi": float(3.0 * np.pi / 2.0), "basis_family": "axis"},
    ]


def _is_axis_basis(theta: float, phi: float, atol: float = 1e-12) -> bool:
    if math.isclose(theta, 0.0, abs_tol=atol) or math.isclose(theta, np.pi, abs_tol=atol):
        return True
    if not math.isclose(theta, np.pi / 2.0, abs_tol=atol):
        return False
    phi_mod = float(phi % (2.0 * np.pi))
    return any(math.isclose(phi_mod, axis_phi, abs_tol=atol) for axis_phi in (0.0, np.pi / 2.0, np.pi, 3.0 * np.pi / 2.0))


def continuous_basis_specs(theta_points: int = 13, phi_points: int = 16, exclude_axis: bool = True) -> list[dict]:
    if theta_points < 2:
        raise ValueError("theta_points must be at least 2.")
    if phi_points < 1:
        raise ValueError("phi_points must be positive.")

    specs = []
    for theta in np.linspace(0.0, np.pi, theta_points):
        phi_values = [0.0] if math.isclose(theta, 0.0) or math.isclose(theta, np.pi) else np.linspace(
            0.0,
            2.0 * np.pi,
            phi_points,
            endpoint=False,
        )
        for phi in phi_values:
            if exclude_axis and _is_axis_basis(float(theta), float(phi)):
                continue
            specs.append(
                {
                    "basis_name": "continuous",
                    "theta": float(theta),
                    "phi": float(phi),
                    "basis_family": "continuous",
                }
            )
    return specs


def ensemble_diversity(states: Array) -> float:
    """Average off-diagonal infidelity; lower values mean more collapsed ensembles."""
    states = normalize_rows(states)
    n_states = len(states)
    if n_states < 2:
        return 0.0
    fidelities = fidelity_matrix(states, states)
    off_diagonal = ~np.eye(n_states, dtype=bool)
    return float((1.0 - fidelities)[off_diagonal].mean())


def _evolved_data_blocks(input_ensemble: Array, tau: float, hamiltonian: Array) -> Array:
    if tau < 0:
        raise ValueError("tau must be non-negative.")
    data_states = normalize_rows(input_ensemble)
    evolution = expm(-1j * hamiltonian * tau)
    evolved = np.empty((len(data_states), 8), dtype=complex)
    for idx, data_state in enumerate(data_states):
        evolved[idx] = evolution @ np.kron(data_state, KET0)
    return evolved.reshape(len(data_states), 4, 2)


def projected_denoising_step(
    input_ensemble: Array,
    tau: float,
    theta: float,
    phi: float,
    hamiltonian: Array | None = None,
    min_probability: float = 1e-14,
) -> tuple[Array, Array]:
    """Apply a fixed measurement-induced non-unitary map to a two-qubit ensemble.

    The input states are attached to a complement |0>, evolved under the fixed
    Problem 2 Hamiltonian for time tau, then post-selected on one continuous
    complement-qubit basis vector.
    """
    hamiltonian = three_qubit_hamiltonian() if hamiltonian is None else hamiltonian
    blocks = _evolved_data_blocks(input_ensemble, tau=tau, hamiltonian=hamiltonian)
    return project_evolved_blocks(blocks, theta=theta, phi=phi, min_probability=min_probability)


def project_evolved_blocks(
    evolved_blocks: Array,
    theta: float,
    phi: float,
    min_probability: float = 1e-14,
) -> tuple[Array, Array]:
    basis = continuous_projection_basis(theta, phi)
    projected = np.einsum("nfc,c->nf", evolved_blocks, basis.conj())
    probabilities = np.sum(np.abs(projected) ** 2, axis=1).real
    safe_probabilities = np.maximum(probabilities, min_probability)
    states = projected / np.sqrt(safe_probabilities)[:, None]
    if np.any(probabilities < min_probability):
        states[probabilities < min_probability] = np.array([1, 0, 0, 0], dtype=complex)
    return normalize_rows(states), probabilities


def evaluate_denoising_candidate(
    reference: Array,
    input_ensemble: Array,
    tau: float,
    theta: float,
    phi: float,
    basis_name: str,
    basis_family: str,
    hamiltonian: Array | None = None,
) -> dict:
    reference = normalize_rows(reference)
    input_ensemble = normalize_rows(input_ensemble)
    baseline_mmd = mmd_fidelity(reference, input_ensemble)
    baseline_wasserstein = wasserstein_infidelity(reference, input_ensemble)
    baseline_diversity = ensemble_diversity(input_ensemble)

    candidate, probabilities = projected_denoising_step(
        input_ensemble,
        tau=tau,
        theta=theta,
        phi=phi,
        hamiltonian=hamiltonian,
    )
    candidate_mmd = mmd_fidelity(reference, candidate)
    candidate_wasserstein = wasserstein_infidelity(reference, candidate)
    candidate_diversity = ensemble_diversity(candidate)
    diversity_retention = candidate_diversity / max(baseline_diversity, 1e-12)
    mmd_improvement = baseline_mmd - candidate_mmd
    wasserstein_improvement = baseline_wasserstein - candidate_wasserstein
    mean_success = float(np.mean(probabilities))
    min_success = float(np.min(probabilities))
    score = mmd_improvement + 0.5 * wasserstein_improvement + 0.05 * min(diversity_retention - 1.0, 0.0)

    return {
        "basis_family": basis_family,
        "basis_name": basis_name,
        "tau": float(tau),
        "theta": float(theta),
        "phi": float(phi),
        "baseline_mmd": float(baseline_mmd),
        "candidate_mmd": float(candidate_mmd),
        "mmd_improvement": float(mmd_improvement),
        "baseline_wasserstein": float(baseline_wasserstein),
        "candidate_wasserstein": float(candidate_wasserstein),
        "wasserstein_improvement": float(wasserstein_improvement),
        "baseline_diversity": float(baseline_diversity),
        "candidate_diversity": float(candidate_diversity),
        "diversity_retention": float(diversity_retention),
        "mean_success_probability": mean_success,
        "min_success_probability": min_success,
        "score": float(score),
    }


def search_projected_denoising(
    reference: Array,
    input_ensemble: Array,
    taus: Iterable[float],
    basis_specs: list[dict],
    hamiltonian: Array | None = None,
) -> list[dict]:
    hamiltonian = three_qubit_hamiltonian() if hamiltonian is None else hamiltonian
    reference = normalize_rows(reference)
    input_ensemble = normalize_rows(input_ensemble)
    baseline_mmd = mmd_fidelity(reference, input_ensemble)
    baseline_wasserstein = wasserstein_infidelity(reference, input_ensemble)
    baseline_diversity = ensemble_diversity(input_ensemble)

    rows = []
    for tau in taus:
        blocks = _evolved_data_blocks(input_ensemble, tau=float(tau), hamiltonian=hamiltonian)
        for spec in basis_specs:
            candidate, probabilities = project_evolved_blocks(blocks, theta=spec["theta"], phi=spec["phi"])
            candidate_mmd = mmd_fidelity(reference, candidate)
            candidate_wasserstein = wasserstein_infidelity(reference, candidate)
            candidate_diversity = ensemble_diversity(candidate)
            diversity_retention = candidate_diversity / max(baseline_diversity, 1e-12)
            mmd_improvement = baseline_mmd - candidate_mmd
            wasserstein_improvement = baseline_wasserstein - candidate_wasserstein
            score = mmd_improvement + 0.5 * wasserstein_improvement + 0.05 * min(diversity_retention - 1.0, 0.0)
            rows.append(
                {
                    "basis_family": spec["basis_family"],
                    "basis_name": spec["basis_name"],
                    "tau": float(tau),
                    "theta": float(spec["theta"]),
                    "phi": float(spec["phi"]),
                    "baseline_mmd": float(baseline_mmd),
                    "candidate_mmd": float(candidate_mmd),
                    "mmd_improvement": float(mmd_improvement),
                    "baseline_wasserstein": float(baseline_wasserstein),
                    "candidate_wasserstein": float(candidate_wasserstein),
                    "wasserstein_improvement": float(wasserstein_improvement),
                    "baseline_diversity": float(baseline_diversity),
                    "candidate_diversity": float(candidate_diversity),
                    "diversity_retention": float(diversity_retention),
                    "mean_success_probability": float(np.mean(probabilities)),
                    "min_success_probability": float(np.min(probabilities)),
                    "score": float(score),
                }
            )
    return rows


def select_best_candidate(
    rows: list[dict],
    min_mean_success: float = 0.10,
    min_diversity_retention: float = 0.50,
) -> dict:
    eligible = [
        row
        for row in rows
        if row["mean_success_probability"] >= min_mean_success
        and row["diversity_retention"] >= min_diversity_retention
        and (row["mmd_improvement"] > 0.0 or row["wasserstein_improvement"] > 0.0)
    ]
    if not eligible:
        eligible = rows
    return max(eligible, key=lambda row: row["score"])


def adoption_decision(
    continuous_best: dict,
    axis_best: dict,
    min_metric_improvement: float = 0.02,
    min_mean_success: float = 0.10,
    min_diversity_retention: float = 0.50,
    min_axis_score_margin: float = 0.005,
) -> str:
    improves_input = (
        continuous_best["mmd_improvement"] >= min_metric_improvement
        or continuous_best["wasserstein_improvement"] >= min_metric_improvement
    )
    beats_axis = continuous_best["score"] >= axis_best["score"] + min_axis_score_margin
    keeps_diversity = continuous_best["diversity_retention"] >= min_diversity_retention
    likely_observable = continuous_best["mean_success_probability"] >= min_mean_success
    if improves_input and beats_axis and keeps_diversity and likely_observable:
        return "main_candidate"
    if improves_input and keeps_diversity and likely_observable:
        return "fallback_candidate"
    return "do_not_use_as_main"

from __future__ import annotations

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

from quantum_cylinder.bloch_vectors import bloch_vector, ensemble_bloch_vectors
from quantum_cylinder.experiment_curves import closest_metric_pair, hamiltonian_resource_proxy
from quantum_cylinder.problem_1a_target_ensemble import target_ensemble, target_state_circuit
from quantum_cylinder.problem_1b_ensemble_metrics import fidelity_matrix, mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.problem_1c_random_unitary_diffusion import (
    random_unitary_circuit,
    random_unitary_resource_proxy,
    random_unitary_trajectory,
)
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import (
    hamiltonian_projected_trajectory,
    three_qubit_hamiltonian_operator,
)
from quantum_cylinder.problem_3_continuous_projected_denoising import (
    adoption_decision,
    continuous_projection_basis,
    project_evolved_blocks,
    projected_denoising_step,
    search_projected_denoising,
)


def test_target_ensemble_is_normalized() -> None:
    states = target_ensemble(n_samples=10, sigma=0.1, seed=1)
    assert states.shape == (10, 4)
    assert np.allclose(np.linalg.norm(states, axis=1), 1.0)


def test_identical_ensemble_distances_are_zero() -> None:
    states = target_ensemble(n_samples=8, sigma=0.1, seed=2)
    assert mmd_fidelity(states, states) < 1e-10
    assert wasserstein_infidelity(states, states) < 1e-10


def test_fidelity_matrix_bounds() -> None:
    states = target_ensemble(n_samples=8, sigma=0.1, seed=3)
    fidelities = fidelity_matrix(states, states)
    assert np.all(fidelities >= 0)
    assert np.all(fidelities <= 1)
    assert np.allclose(np.diag(fidelities), 1.0)


def test_random_unitary_trajectory_preserves_norm() -> None:
    states = target_ensemble(n_samples=6, sigma=0.1, seed=4)
    trajectory = random_unitary_trajectory(states, n_steps=3, seed=5)
    assert len(trajectory) == 4
    for ensemble in trajectory:
        assert np.allclose(np.linalg.norm(ensemble, axis=1), 1.0)


def test_problem_1_circuits_are_qiskit_circuits() -> None:
    assert isinstance(target_state_circuit(np.zeros(2), np.zeros(2)), QuantumCircuit)
    assert isinstance(random_unitary_circuit(np.zeros((2, 3))), QuantumCircuit)


def test_hamiltonian_t0_recovers_initial_ensemble() -> None:
    states = target_ensemble(n_samples=6, sigma=0.1, seed=6)
    trajectory = hamiltonian_projected_trajectory(states, times=np.array([0.0]), measurement_basis="z", seed=7)
    assert len(trajectory) == 1
    assert np.allclose(np.abs(np.sum(states * trajectory[0].conj(), axis=1)) ** 2, 1.0)


def test_hamiltonian_is_qiskit_sparse_pauli_operator() -> None:
    hamiltonian = three_qubit_hamiltonian_operator()
    assert isinstance(hamiltonian, SparsePauliOp)
    assert len(hamiltonian) == 8


def test_bloch_vectors_match_product_basis_states() -> None:
    ket00 = np.array([[1.0, 0.0, 0.0, 0.0]], dtype=complex)
    vectors = ensemble_bloch_vectors(ket00, qubit=0)
    assert vectors.shape == (1, 3)
    assert np.allclose(vectors[0], [0.0, 0.0, 1.0])
    assert np.allclose(bloch_vector(ket00[0], qubit=1), [0.0, 0.0, 1.0])


def test_resource_proxy_columns_match() -> None:
    random_proxy = random_unitary_resource_proxy(step=2)
    hamiltonian_proxy = hamiltonian_resource_proxy(time=1.0)
    assert random_proxy.keys() == hamiltonian_proxy.keys()
    assert hamiltonian_proxy["fixed_hamiltonian_terms"] == 8
    assert hamiltonian_proxy["fixed_hamiltonian_parameters"] == 3


def test_closest_metric_pair_skips_initial_point() -> None:
    random_rows = [
        {"index": 0, "parameter_name": "step", "parameter": 0.0, "mmd": 0.0},
        {"index": 1, "parameter_name": "step", "parameter": 1.0, "mmd": 0.3},
        {"index": 2, "parameter_name": "step", "parameter": 2.0, "mmd": 0.7},
    ]
    ham_rows = [
        {"index": 0, "parameter_name": "time", "parameter": 0.0, "mmd": 0.0},
        {"index": 1, "parameter_name": "time", "parameter": 0.5, "mmd": 0.35},
        {"index": 2, "parameter_name": "time", "parameter": 1.0, "mmd": 0.9},
    ]

    match = closest_metric_pair(random_rows, ham_rows, metric="mmd")

    assert match["reference_parameter"] == 1.0
    assert match["candidate_parameter"] == 0.5
    assert np.isclose(match["absolute_gap"], 0.05)


def test_continuous_projection_basis_is_normalized() -> None:
    basis = continuous_projection_basis(theta=np.pi / 3.0, phi=np.pi / 5.0)
    assert basis.shape == (2,)
    assert np.isclose(np.linalg.norm(basis), 1.0)


def test_projected_denoising_step_preserves_norm_and_probabilities() -> None:
    states = target_ensemble(n_samples=5, sigma=0.1, seed=10)
    denoised, probabilities = projected_denoising_step(states, tau=0.2, theta=np.pi / 2.0, phi=0.0)
    assert denoised.shape == states.shape
    assert probabilities.shape == (5,)
    assert np.allclose(np.linalg.norm(denoised, axis=1), 1.0)
    assert np.all(probabilities >= 0.0)
    assert np.all(probabilities <= 1.0 + 1e-10)


def test_projected_denoising_rejects_nearly_impossible_postselection() -> None:
    impossible_blocks = np.zeros((2, 4, 2), dtype=complex)
    with pytest.raises(ValueError, match="Post-selection probability"):
        project_evolved_blocks(impossible_blocks, theta=0.0, phi=0.0)


def test_problem_3_search_returns_candidate_rows() -> None:
    states = target_ensemble(n_samples=5, sigma=0.1, seed=11)
    trajectory = random_unitary_trajectory(states, n_steps=1, seed=12)
    rows = search_projected_denoising(
        states,
        trajectory[1],
        taus=[0.1],
        basis_specs=[{"basis_family": "continuous", "basis_name": "test", "theta": np.pi / 2.0, "phi": 0.0}],
    )
    assert len(rows) == 1
    assert rows[0]["basis_family"] == "continuous"
    assert "mmd_improvement" in rows[0]
    assert "mean_success_probability" in rows[0]


def test_adoption_decision_rejects_bad_candidate() -> None:
    continuous = {
        "mmd_improvement": -0.1,
        "wasserstein_improvement": -0.1,
        "score": -0.1,
        "diversity_retention": 0.9,
        "mean_success_probability": 0.5,
    }
    axis = {"score": 0.0}
    assert adoption_decision(continuous, axis) == "do_not_use_as_main"

from __future__ import annotations

import numpy as np

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1b_ensemble_metrics import fidelity_matrix, mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_resource_proxy, random_unitary_trajectory
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import hamiltonian_projected_trajectory
from quantum_cylinder.experiment_curves import hamiltonian_resource_proxy


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


def test_hamiltonian_t0_recovers_initial_ensemble() -> None:
    states = target_ensemble(n_samples=6, sigma=0.1, seed=6)
    trajectory = hamiltonian_projected_trajectory(states, times=np.array([0.0]), measurement_basis="z", seed=7)
    assert len(trajectory) == 1
    assert np.allclose(np.abs(np.sum(states * trajectory[0].conj(), axis=1)) ** 2, 1.0)


def test_resource_proxy_columns_match() -> None:
    random_proxy = random_unitary_resource_proxy(step=2)
    hamiltonian_proxy = hamiltonian_resource_proxy(time=1.0)
    assert random_proxy.keys() == hamiltonian_proxy.keys()
    assert hamiltonian_proxy["fixed_hamiltonian_terms"] == 8
    assert hamiltonian_proxy["fixed_hamiltonian_parameters"] == 3

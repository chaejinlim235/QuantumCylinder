"""Baseline tools for the QuantumCylinder hackathon project."""

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1b_ensemble_metrics import fidelity_matrix, mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_trajectory
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import hamiltonian_projected_trajectory

__all__ = [
    "fidelity_matrix",
    "hamiltonian_projected_trajectory",
    "mmd_fidelity",
    "random_unitary_trajectory",
    "target_ensemble",
    "wasserstein_infidelity",
]

__version__ = "0.1.0"

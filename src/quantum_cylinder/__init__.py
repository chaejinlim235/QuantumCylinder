"""Baseline tools for the QuantumCylinder hackathon project."""

from quantum_cylinder.diffusion import hamiltonian_projected_trajectory, random_unitary_trajectory
from quantum_cylinder.metrics import fidelity_matrix, mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.states import target_ensemble

__all__ = [
    "fidelity_matrix",
    "hamiltonian_projected_trajectory",
    "mmd_fidelity",
    "random_unitary_trajectory",
    "target_ensemble",
    "wasserstein_infidelity",
]

__version__ = "0.1.0"

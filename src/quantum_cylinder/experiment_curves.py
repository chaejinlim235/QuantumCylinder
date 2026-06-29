from __future__ import annotations

import numpy as np

from quantum_cylinder.problem_1b_ensemble_metrics import mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.quantum_ops import Array


def distance_curve(
    reference: Array,
    trajectory: list[Array],
    parameters: Array | None = None,
    parameter_name: str = "parameter",
) -> list[dict]:
    if parameters is None:
        parameters = np.arange(len(trajectory))
    if len(parameters) != len(trajectory):
        raise ValueError("parameters and trajectory must have the same length.")

    rows = []
    for idx, (parameter, ensemble) in enumerate(zip(parameters, trajectory, strict=True)):
        rows.append(
            {
                "index": idx,
                "parameter_name": parameter_name,
                "parameter": float(parameter),
                "mmd": mmd_fidelity(reference, ensemble),
                "wasserstein": wasserstein_infidelity(reference, ensemble),
            }
        )
    return rows


def hamiltonian_resource_proxy(time: float, measurement_basis: str = "z") -> dict:
    return {
        "mechanism": "hamiltonian_projected",
        "parameter": time,
        "single_qubit_rotations": 0,
        "two_qubit_entanglers": 0,
        "random_controls": 0,
        "total_hamiltonian_time": time,
        "fixed_hamiltonian_terms": 8,
        "fixed_hamiltonian_parameters": 3,
        "measurement_basis": measurement_basis,
    }

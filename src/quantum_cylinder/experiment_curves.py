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


def closest_metric_pair(
    reference_rows: list[dict],
    candidate_rows: list[dict],
    metric: str,
    skip_initial: bool = True,
) -> dict:
    """Find the closest pair of diffusion points under one reported metric."""
    if not reference_rows:
        raise ValueError("reference_rows must not be empty.")
    if not candidate_rows:
        raise ValueError("candidate_rows must not be empty.")

    def eligible(row: dict) -> bool:
        if not skip_initial:
            return True
        return int(row.get("index", -1)) != 0 and abs(float(row.get("parameter", 0.0))) > 1e-12

    reference_candidates = [row for row in reference_rows if eligible(row)]
    candidate_candidates = [row for row in candidate_rows if eligible(row)]
    if not reference_candidates or not candidate_candidates:
        raise ValueError("No eligible non-initial rows to compare.")

    best_reference = reference_candidates[0]
    best_candidate = candidate_candidates[0]
    best_gap = abs(float(best_reference[metric]) - float(best_candidate[metric]))

    for reference_row in reference_candidates:
        for candidate_row in candidate_candidates:
            gap = abs(float(reference_row[metric]) - float(candidate_row[metric]))
            if gap < best_gap:
                best_reference = reference_row
                best_candidate = candidate_row
                best_gap = gap

    return {
        "metric": metric,
        "reference_index": int(best_reference["index"]),
        "reference_parameter_name": best_reference["parameter_name"],
        "reference_parameter": float(best_reference["parameter"]),
        "reference_metric_value": float(best_reference[metric]),
        "candidate_index": int(best_candidate["index"]),
        "candidate_parameter_name": best_candidate["parameter_name"],
        "candidate_parameter": float(best_candidate["parameter"]),
        "candidate_metric_value": float(best_candidate[metric]),
        "absolute_gap": float(best_gap),
    }


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

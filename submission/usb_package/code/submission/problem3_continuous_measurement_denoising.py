from __future__ import annotations

import argparse
import math
import statistics as stats
import sys
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector
from scipy.linalg import expm

from submission.states_and_metrics import (
    fidelity_matrix,
    make_target_ensemble,
    mmd_fidelity,
    wasserstein_infidelity,
    write_csv,
    write_text,
)

Array = np.ndarray
KET0 = np.asarray(Statevector.from_label("0").data, dtype=complex)


def random_unitary_circuit(angles: np.ndarray, entangler: str = "cz") -> QuantumCircuit:
    """Create one Qiskit random local-rotation + entangler layer."""
    circuit = QuantumCircuit(2)
    for qubit in range(2):
        ax, ay, az = angles[qubit]
        circuit.rx(float(ax), qubit)
        circuit.ry(float(ay), qubit)
        circuit.rz(float(az), qubit)

    if entangler == "cz":
        circuit.cz(0, 1)
    elif entangler == "cnot":
        circuit.cx(0, 1)
    else:
        raise ValueError(f"Unknown entangler: {entangler}")
    return circuit


def normalize_rows(states: Array) -> Array:
    states = np.asarray(states, dtype=complex)
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Cannot normalize an ensemble with a zero vector.")
    return states / norms


def random_unitary_layer(rng: np.random.Generator, angle_scale: float = np.pi, entangler: str = "cz") -> np.ndarray:
    """Sample one Qiskit layer and return its 4x4 unitary matrix."""
    angles = rng.uniform(-angle_scale, angle_scale, size=(2, 3))
    circuit = random_unitary_circuit(angles, entangler=entangler)
    return np.asarray(Operator(circuit).reverse_qargs().data, dtype=complex)


def random_unitary_trajectory(
    initial: np.ndarray,
    n_steps: int = 12,
    angle_scale: float = np.pi,
    seed: int | None = 8,
    entangler: str = "cz",
) -> list[np.ndarray]:
    """Apply random-unitary layers and return S0, S1, ..., Sn."""
    if n_steps < 0:
        raise ValueError("n_steps must be non-negative.")

    rng = np.random.default_rng(seed)
    current = normalize_rows(initial)
    trajectory = [current.copy()]

    for _ in range(n_steps):
        next_states = np.empty_like(current)
        for idx, state in enumerate(current):
            unitary = random_unitary_layer(rng, angle_scale=angle_scale, entangler=entangler)
            next_states[idx] = Statevector(state).evolve(Operator(unitary)).data
        current = normalize_rows(next_states)
        trajectory.append(current.copy())

    return trajectory


def three_qubit_hamiltonian_operator(
    hx: float = 0.8090,
    hy: float = 0.9045,
    j_coupling: float = 1.0,
) -> SparsePauliOp:
    """Create Problem 2's fixed 3-qubit Hamiltonian as a Qiskit Pauli sum."""
    return SparsePauliOp.from_list(
        [
            ("XII", hx),
            ("YII", hy),
            ("IXI", hx),
            ("IYI", hy),
            ("IIX", hx),
            ("IIY", hy),
            ("XXI", j_coupling),
            ("IXX", j_coupling),
        ]
    )


def three_qubit_hamiltonian(hx: float = 0.8090, hy: float = 0.9045, j_coupling: float = 1.0) -> np.ndarray:
    """Return the Hamiltonian matrix with qubit order M0, M1, F."""
    hamiltonian = three_qubit_hamiltonian_operator(hx=hx, hy=hy, j_coupling=j_coupling)
    return np.asarray(hamiltonian.to_matrix(), dtype=complex)


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


def project_evolved_blocks(
    evolved_blocks: Array,
    theta: float,
    phi: float,
    min_probability: float = 1e-14,
) -> tuple[Array, Array]:
    basis = continuous_projection_basis(theta, phi)
    projected = np.einsum("nfc,c->nf", evolved_blocks, basis.conj())
    probabilities = np.sum(np.abs(projected) ** 2, axis=1).real
    if np.any(probabilities < min_probability):
        raise ValueError("Post-selection probability is below the candidate validity threshold.")
    states = projected / np.sqrt(probabilities)[:, None]
    return normalize_rows(states), probabilities


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
            try:
                candidate, probabilities = project_evolved_blocks(blocks, theta=spec["theta"], phi=spec["phi"])
            except ValueError:
                continue
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
    if not rows:
        raise ValueError("No valid post-selection candidates remained after probability filtering.")
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


def _compact_best_row(input_step: int, continuous_best: dict, axis_best: dict, decision: str) -> dict:
    return {
        "input_step": input_step,
        "decision": decision,
        "baseline_mmd": continuous_best["baseline_mmd"],
        "continuous_mmd": continuous_best["candidate_mmd"],
        "axis_mmd": axis_best["candidate_mmd"],
        "continuous_mmd_improvement": continuous_best["mmd_improvement"],
        "baseline_wasserstein": continuous_best["baseline_wasserstein"],
        "continuous_wasserstein": continuous_best["candidate_wasserstein"],
        "axis_wasserstein": axis_best["candidate_wasserstein"],
        "continuous_wasserstein_improvement": continuous_best["wasserstein_improvement"],
        "continuous_tau": continuous_best["tau"],
        "continuous_theta": continuous_best["theta"],
        "continuous_phi": continuous_best["phi"],
        "axis_basis_name": axis_best["basis_name"],
        "axis_tau": axis_best["tau"],
        "continuous_diversity_retention": continuous_best["diversity_retention"],
        "continuous_mean_success_probability": continuous_best["mean_success_probability"],
        "continuous_score_minus_axis_score": continuous_best["score"] - axis_best["score"],
    }


def solve_problem_3(
    output_dir: Path,
    n_samples: int = 80,
    sigma: float = 0.10,
    seed: int = 7,
    random_steps: int = 12,
    input_steps: list[int] | None = None,
    tau_points: int = 20,
    theta_points: int = 13,
    phi_points: int = 16,
) -> dict:
    """Problem 3: search continuous measurement bases on the Qiskit Hamiltonian matrix."""
    input_steps = [1, 2, 3, 5, 7, 12] if input_steps is None else input_steps
    target = make_target_ensemble(n_samples=n_samples, sigma=sigma, seed=seed)
    random_trajectory = random_unitary_trajectory(target, n_steps=random_steps, seed=seed + 1)

    hamiltonian = three_qubit_hamiltonian()
    taus = np.linspace(0.05, 2.0, tau_points)
    continuous_specs = continuous_basis_specs(theta_points=theta_points, phi_points=phi_points, exclude_axis=True)
    axis_specs = axis_basis_specs()
    if not continuous_specs:
        raise ValueError("Continuous basis grid is empty after excluding Z/X/Y axes.")

    best_rows = []
    for input_step in input_steps:
        diffused = random_trajectory[input_step]

        # Baseline: best projection among the six exact Z/X/Y axis outcomes.
        axis_rows = search_projected_denoising(target, diffused, taus, axis_specs, hamiltonian=hamiltonian)
        axis_best = select_best_candidate(axis_rows)

        # New idea: search non-axis measurement vectors on the complement Bloch sphere.
        continuous_rows = search_projected_denoising(
            target,
            diffused,
            taus,
            continuous_specs,
            hamiltonian=hamiltonian,
        )
        continuous_best = select_best_candidate(continuous_rows)
        decision = adoption_decision(continuous_best, axis_best)
        best_rows.append(_compact_best_row(input_step, continuous_best, axis_best, decision))

    main_rows = [row for row in best_rows if row["decision"] == "main_candidate"]
    fallback_rows = [row for row in best_rows if row["decision"] == "fallback_candidate"]
    overall = "use_as_main" if main_rows else "fallback_only" if fallback_rows else "do_not_use_as_main"
    best_pool = main_rows or fallback_rows or best_rows
    best = max(best_pool, key=lambda row: row["continuous_score_minus_axis_score"])
    axis_margins = [float(row["continuous_score_minus_axis_score"]) for row in best_rows]
    median_axis_margin = stats.median(axis_margins)
    min_axis_margin = min(axis_margins)
    nonpositive_axis_margin_rows = sum(1 for margin in axis_margins if margin <= 0.0)

    summary = f"""# Problem 3 Simple Summary

## Physical Operation

- Start from a diffused Problem 1 ensemble.
- Attach complement qubit `F = |0>`.
- Use the same Qiskit-defined fixed Hamiltonian matrix from Problem 2.
- Evolve `(M0, M1, F)` with that Hamiltonian.
- Post-select `F` on a continuous Bloch-sphere basis vector.
- Compare against the best exact `Z/X/Y` axis projection.

## Result

- Overall decision: `{overall}`
- Main-candidate steps: `{len(main_rows)}`
- Fallback-candidate steps: `{len(fallback_rows)}`
- Best input step: `{best['input_step']}`
- Best MMD: `{best['baseline_mmd']:.6f} -> {best['continuous_mmd']:.6f}`
- Best Wasserstein-type distance: `{best['baseline_wasserstein']:.6f} -> {best['continuous_wasserstein']:.6f}`
- Best continuous basis: tau `{best['continuous_tau']:.6f}`, theta `{best['continuous_theta']:.6f}`, phi `{best['continuous_phi']:.6f}`
- Diversity retention: `{best['continuous_diversity_retention']:.6f}`
- Mean post-selection probability: `{best['continuous_mean_success_probability']:.6f}`

## Axis Baseline Comparison

- Median continuous-vs-axis score margin: `{median_axis_margin:.6f}`
- Minimum continuous-vs-axis score margin: `{min_axis_margin:.6f}`
- Nonpositive axis-margin rows: `{nonpositive_axis_margin_rows} / {len(axis_margins)}`
- Best selected row's axis-only comparator: `{best['axis_basis_name']}` at tau `{best['axis_tau']:.6f}`

Do not claim every input step beats the axis-only projection. Treat small or negative axis margins as a limitation, and state this as a small-scale post-selected proxy improvement, not hardware advantage or general quantum advantage.

## Interpretation

The continuous measurement basis gives an additional denoising knob beyond the discrete axis projection baseline. We only use it as the main Problem 3 claim when it improves the metric, beats the axis-only baseline, keeps ensemble diversity, and has reasonable post-selection probability.

## Output

- `problem3_continuous_denoising_best.csv`
"""

    write_csv(output_dir / "problem3_continuous_denoising_best.csv", best_rows)
    write_text(output_dir / "problem3_summary.md", summary)
    return {"rows": best_rows, "summary": output_dir / "problem3_summary.md", "overall": overall, "best": best}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the simple Problem 3 submission layer.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "submission_simple" / "problem3")
    parser.add_argument("--n-samples", type=int, default=80)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--random-steps", type=int, default=12)
    parser.add_argument("--input-steps", type=int, nargs="+", default=[1, 2, 3, 5, 7, 12])
    parser.add_argument("--tau-points", type=int, default=20)
    parser.add_argument("--theta-points", type=int, default=13)
    parser.add_argument("--phi-points", type=int, default=16)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = solve_problem_3(
        args.output_dir,
        n_samples=args.n_samples,
        sigma=args.sigma,
        seed=args.seed,
        random_steps=args.random_steps,
        input_steps=args.input_steps,
        tau_points=args.tau_points,
        theta_points=args.theta_points,
        phi_points=args.phi_points,
    )
    print(f"Problem 3 decision={result['overall']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from quantum_cylinder.implementations.qiskit.problem_1c_random_unitary_diffusion import random_unitary_trajectory
from quantum_cylinder.implementations.qiskit.problem_2_hamiltonian_projected_diffusion import three_qubit_hamiltonian
from quantum_cylinder.problem_3_continuous_projected_denoising import (
    adoption_decision,
    axis_basis_specs,
    continuous_basis_specs,
    search_projected_denoising,
    select_best_candidate,
)

from submission.states_and_metrics import make_target_ensemble, write_csv, write_text


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

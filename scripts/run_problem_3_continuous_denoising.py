from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble  # noqa: E402
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_trajectory  # noqa: E402
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import three_qubit_hamiltonian  # noqa: E402
from quantum_cylinder.problem_3_continuous_projected_denoising import (  # noqa: E402
    adoption_decision,
    axis_basis_specs,
    continuous_basis_specs,
    search_projected_denoising,
    select_best_candidate,
)


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_args() -> argparse.Namespace:
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument("--config", type=Path, default=ROOT / "configs" / "problem_3_continuous_denoising.json")
    known, remaining = config_parser.parse_known_args()
    defaults = load_config(known.config)

    parser = argparse.ArgumentParser(parents=[config_parser])
    parser.add_argument("--n-samples", type=int, default=defaults.get("n_samples", 80))
    parser.add_argument("--sigma", type=float, default=defaults.get("sigma", 0.1))
    parser.add_argument("--seed", type=int, default=defaults.get("seed", 7))
    parser.add_argument("--random-steps", type=int, default=defaults.get("random_steps", 12))
    parser.add_argument("--input-steps", type=int, nargs="+", default=defaults.get("input_steps", [1, 2, 3, 5, 7, 12]))
    parser.add_argument("--tau-min", type=float, default=defaults.get("tau_min", 0.05))
    parser.add_argument("--tau-max", type=float, default=defaults.get("tau_max", 2.0))
    parser.add_argument("--tau-points", type=int, default=defaults.get("tau_points", 20))
    parser.add_argument("--theta-points", type=int, default=defaults.get("theta_points", 13))
    parser.add_argument("--phi-points", type=int, default=defaults.get("phi_points", 16))
    parser.add_argument("--min-metric-improvement", type=float, default=defaults.get("min_metric_improvement", 0.02))
    parser.add_argument("--min-mean-success", type=float, default=defaults.get("min_mean_success", 0.1))
    parser.add_argument("--min-diversity-retention", type=float, default=defaults.get("min_diversity_retention", 0.5))
    parser.add_argument("--min-axis-score-margin", type=float, default=defaults.get("min_axis_score_margin", 0.005))
    parser.add_argument("--output-dir", type=Path, default=ROOT / defaults.get("output_dir", "results/problem_3"))
    return parser.parse_args(remaining)


def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")


def plot_best_rows(best_rows: list[dict], output_path: Path) -> None:
    steps = [row["input_step"] for row in best_rows]
    baseline_mmd = [row["baseline_mmd"] for row in best_rows]
    denoised_mmd = [row["continuous_mmd"] for row in best_rows]
    axis_mmd = [row["axis_mmd"] for row in best_rows]
    baseline_w = [row["baseline_wasserstein"] for row in best_rows]
    denoised_w = [row["continuous_wasserstein"] for row in best_rows]
    axis_w = [row["axis_wasserstein"] for row in best_rows]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
    axes[0].plot(steps, baseline_mmd, marker="o", label="input")
    axes[0].plot(steps, axis_mmd, marker="s", label="best Z/X/Y")
    axes[0].plot(steps, denoised_mmd, marker="^", label="best continuous")
    axes[0].set_title("MMD after projected denoising")
    axes[0].set_xlabel("random-unitary input step")
    axes[0].set_ylabel("distance to S0")
    axes[0].grid(alpha=0.25)
    axes[0].legend()

    axes[1].plot(steps, baseline_w, marker="o", label="input")
    axes[1].plot(steps, axis_w, marker="s", label="best Z/X/Y")
    axes[1].plot(steps, denoised_w, marker="^", label="best continuous")
    axes[1].set_title("Wasserstein-type distance")
    axes[1].set_xlabel("random-unitary input step")
    axes[1].set_ylabel("distance to S0")
    axes[1].grid(alpha=0.25)
    axes[1].legend()

    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def summarize_best_row(row: dict) -> str:
    return (
        f"- step `{row['input_step']}`: decision `{row['decision']}`, "
        f"MMD `{row['baseline_mmd']:.6f} -> {row['continuous_mmd']:.6f}`, "
        f"Wasserstein `{row['baseline_wasserstein']:.6f} -> {row['continuous_wasserstein']:.6f}`, "
        f"diversity retention `{row['continuous_diversity_retention']:.3f}`, "
        f"mean success `{row['continuous_mean_success_probability']:.3f}`"
    )


def write_summary(path: Path, args: argparse.Namespace, best_rows: list[dict]) -> None:
    main_rows = [row for row in best_rows if row["decision"] == "main_candidate"]
    fallback_rows = [row for row in best_rows if row["decision"] == "fallback_candidate"]
    do_not_use_rows = [row for row in best_rows if row["decision"] == "do_not_use_as_main"]
    best_pool = main_rows or fallback_rows or best_rows
    best_overall = max(best_pool, key=lambda row: row["continuous_score"])
    decision = "use_as_main" if main_rows else "fallback_only" if fallback_rows else "do_not_use_as_main"
    lines = "\n".join(summarize_best_row(row) for row in best_rows)

    text = f"""# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = {args.n_samples}`, `sigma = {args.sigma}`, seed `{args.seed}`
- Input ensemble: random-unitary diffusion at steps `{args.input_steps}`
- Denoising map: attach one complement qubit, evolve with the fixed Problem 2 Hamiltonian, then post-select on a continuous complement basis
- Continuous basis grid: theta points `{args.theta_points}`, phi points `{args.phi_points}`, excluding exact `Z/X/Y` axes
- Time grid: `linspace({args.tau_min}, {args.tau_max}, {args.tau_points})`
- Axis baseline: best among `Z`, `X`, `Y` projection outcomes over the same time grid

## Adoption Decision

Overall decision: `{decision}`

The result is a main candidate only when it improves at least one baseline metric, scores sufficiently above the best axis-only projection, keeps diversity, and has a reasonable mean post-selection probability.

## Best Overall Continuous Candidate

- Input step: `{best_overall['input_step']}`
- tau: `{best_overall['continuous_tau']:.6f}`
- theta: `{best_overall['continuous_theta']:.6f}`
- phi: `{best_overall['continuous_phi']:.6f}`
- MMD: `{best_overall['baseline_mmd']:.6f} -> {best_overall['continuous_mmd']:.6f}`
- Wasserstein: `{best_overall['baseline_wasserstein']:.6f} -> {best_overall['continuous_wasserstein']:.6f}`
- Diversity retention: `{best_overall['continuous_diversity_retention']:.6f}`
- Mean success probability: `{best_overall['continuous_mean_success_probability']:.6f}`

## Step-Level Decisions

{lines}

## Counts

- Main candidates: `{len(main_rows)}`
- Fallback candidates: `{len(fallback_rows)}`
- Do not use as main: `{len(do_not_use_rows)}`

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`
"""
    path.write_text(text, encoding="utf-8")


def prefixed_row(prefix: str, row: dict) -> dict:
    return {
        f"{prefix}_basis_family": row["basis_family"],
        f"{prefix}_basis_name": row["basis_name"],
        f"{prefix}_tau": row["tau"],
        f"{prefix}_theta": row["theta"],
        f"{prefix}_phi": row["phi"],
        f"{prefix}_mmd": row["candidate_mmd"],
        f"{prefix}_mmd_improvement": row["mmd_improvement"],
        f"{prefix}_wasserstein": row["candidate_wasserstein"],
        f"{prefix}_wasserstein_improvement": row["wasserstein_improvement"],
        f"{prefix}_diversity": row["candidate_diversity"],
        f"{prefix}_diversity_retention": row["diversity_retention"],
        f"{prefix}_mean_success_probability": row["mean_success_probability"],
        f"{prefix}_min_success_probability": row["min_success_probability"],
        f"{prefix}_score": row["score"],
    }


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    s0 = target_ensemble(args.n_samples, sigma=args.sigma, seed=args.seed)
    random_traj = random_unitary_trajectory(s0, n_steps=args.random_steps, seed=args.seed + 1)
    hamiltonian = three_qubit_hamiltonian()
    taus = np.linspace(args.tau_min, args.tau_max, args.tau_points)
    continuous_specs = continuous_basis_specs(theta_points=args.theta_points, phi_points=args.phi_points, exclude_axis=True)
    axis_specs = axis_basis_specs()

    all_candidate_rows = []
    best_rows = []
    for input_step in args.input_steps:
        if input_step < 0 or input_step > args.random_steps:
            raise ValueError(f"input_step must be in [0, {args.random_steps}], got {input_step}.")
        input_ensemble = random_traj[input_step]

        continuous_rows = search_projected_denoising(s0, input_ensemble, taus, continuous_specs, hamiltonian=hamiltonian)
        axis_rows = search_projected_denoising(s0, input_ensemble, taus, axis_specs, hamiltonian=hamiltonian)
        continuous_best = select_best_candidate(
            continuous_rows,
            min_mean_success=args.min_mean_success,
            min_diversity_retention=args.min_diversity_retention,
        )
        axis_best = select_best_candidate(
            axis_rows,
            min_mean_success=args.min_mean_success,
            min_diversity_retention=args.min_diversity_retention,
        )
        decision = adoption_decision(
            continuous_best,
            axis_best,
            min_metric_improvement=args.min_metric_improvement,
            min_mean_success=args.min_mean_success,
            min_diversity_retention=args.min_diversity_retention,
            min_axis_score_margin=args.min_axis_score_margin,
        )

        for row in continuous_rows + axis_rows:
            all_candidate_rows.append({"input_step": input_step, **row})

        best_rows.append(
            {
                "input_step": input_step,
                "decision": decision,
                "baseline_mmd": continuous_best["baseline_mmd"],
                "baseline_wasserstein": continuous_best["baseline_wasserstein"],
                "baseline_diversity": continuous_best["baseline_diversity"],
                **prefixed_row("continuous", continuous_best),
                **prefixed_row("axis", axis_best),
                "continuous_score_minus_axis_score": continuous_best["score"] - axis_best["score"],
            }
        )

    write_rows(output_dir / "candidate_search_metrics.csv", all_candidate_rows)
    write_rows(output_dir / "best_denoising_metrics.csv", best_rows)
    plot_best_rows(best_rows, output_dir / "denoising_improvement.png")
    write_json(
        output_dir / "problem_3_settings.json",
        {
            "n_samples": args.n_samples,
            "sigma": args.sigma,
            "seed": args.seed,
            "random_steps": args.random_steps,
            "input_steps": args.input_steps,
            "tau_min": args.tau_min,
            "tau_max": args.tau_max,
            "tau_points": args.tau_points,
            "theta_points": args.theta_points,
            "phi_points": args.phi_points,
            "min_metric_improvement": args.min_metric_improvement,
            "min_mean_success": args.min_mean_success,
            "min_diversity_retention": args.min_diversity_retention,
            "min_axis_score_margin": args.min_axis_score_margin,
            "metrics": [
                "fidelity_mmd",
                "infidelity_wasserstein",
                "average_off_diagonal_infidelity_diversity",
                "post_selection_probability",
            ],
        },
    )
    write_summary(output_dir / "problem_3_summary.md", args, best_rows)
    print(f"Wrote Problem 3 continuous denoising results to {output_dir}")


if __name__ == "__main__":
    main()

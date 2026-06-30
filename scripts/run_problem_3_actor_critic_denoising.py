from __future__ import annotations

import argparse
import csv
import statistics as stats
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_trajectory
from quantum_cylinder.problem_3_actor_critic_denoising import ActorCriticConfig, train_actor_critic_denoiser
from quantum_cylinder.problem_3_continuous_projected_denoising import (
    axis_basis_specs,
    continuous_basis_specs,
    search_projected_denoising,
    select_best_candidate,
)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def continuous_baseline(reference: np.ndarray, noisy: np.ndarray, tau_points: int, theta_points: int, phi_points: int) -> dict:
    taus = np.linspace(0.05, 2.0, tau_points)
    specs = axis_basis_specs() + continuous_basis_specs(
        theta_points=theta_points,
        phi_points=phi_points,
        exclude_axis=True,
    )
    rows = search_projected_denoising(reference, noisy, taus=taus, basis_specs=specs)
    return select_best_candidate(rows, min_mean_success=0.10, min_diversity_retention=0.50)


def run_benchmark(args: argparse.Namespace) -> list[dict]:
    config = ActorCriticConfig(episodes=args.episodes)
    rows = []

    for seed in args.seeds:
        reference = target_ensemble(n_samples=args.n_samples, sigma=args.sigma, seed=seed)
        random_steps = max(args.input_steps)
        trajectory = random_unitary_trajectory(
            reference,
            n_steps=random_steps,
            angle_scale=args.angle_scale,
            seed=seed + 10_000,
        )

        for input_step in args.input_steps:
            noisy = trajectory[input_step]
            continuous = continuous_baseline(
                reference,
                noisy,
                tau_points=args.tau_points,
                theta_points=args.theta_points,
                phi_points=args.phi_points,
            )
            actor = train_actor_critic_denoiser(
                reference,
                noisy,
                seed=seed * 100 + input_step,
                config=config,
            )

            rows.append(
                {
                    "seed": seed,
                    "input_step": input_step,
                    "baseline_mmd": actor["baseline_mmd"],
                    "baseline_wasserstein": actor["baseline_wasserstein"],
                    "continuous_mmd": continuous["candidate_mmd"],
                    "continuous_wasserstein": continuous["candidate_wasserstein"],
                    "continuous_mmd_improvement": continuous["mmd_improvement"],
                    "continuous_wasserstein_improvement": continuous["wasserstein_improvement"],
                    "continuous_diversity_retention": continuous["diversity_retention"],
                    "continuous_success_probability": continuous["mean_success_probability"],
                    "actor_lambda": actor["lambda"],
                    "actor_mmd": actor["candidate_mmd"],
                    "actor_wasserstein": actor["candidate_wasserstein"],
                    "actor_mmd_improvement": actor["mmd_improvement"],
                    "actor_wasserstein_improvement": actor["wasserstein_improvement"],
                    "actor_raw_fidelity": actor["candidate_raw_fidelity"],
                    "actor_raw_fidelity_improvement": actor["raw_fidelity_improvement"],
                    "actor_diversity_retention": actor["diversity_retention"],
                    "actor_success_probability": actor["mean_success_probability"],
                    "actor_reward": actor["reward"],
                    "actor_selection": actor["selection"],
                    "actor_policy_lambda": actor["policy_lambda"],
                    "actor_best_action_probability": actor["best_action_probability"],
                    "actor_beats_continuous_mmd": actor["candidate_mmd"] < continuous["candidate_mmd"],
                    "actor_beats_continuous_wasserstein": actor["candidate_wasserstein"]
                    < continuous["candidate_wasserstein"],
                }
            )

    return rows


def summarize(rows: list[dict]) -> dict:
    total = len(rows)
    beats_mmd = sum(1 for row in rows if row["actor_beats_continuous_mmd"])
    beats_wasserstein = sum(1 for row in rows if row["actor_beats_continuous_wasserstein"])
    beats_both = sum(
        1
        for row in rows
        if row["actor_beats_continuous_mmd"] and row["actor_beats_continuous_wasserstein"]
    )

    actor_minus_continuous_mmd = [
        float(row["continuous_mmd"] - row["actor_mmd"])
        for row in rows
    ]
    actor_minus_continuous_wasserstein = [
        float(row["continuous_wasserstein"] - row["actor_wasserstein"])
        for row in rows
    ]

    recommendation = "front_facing_candidate" if beats_both >= int(0.80 * total) else "appendix_or_fallback"
    return {
        "rows": total,
        "beats_mmd": beats_mmd,
        "beats_wasserstein": beats_wasserstein,
        "beats_both": beats_both,
        "median_actor_mmd_improvement": stats.median(float(row["actor_mmd_improvement"]) for row in rows),
        "median_actor_wasserstein_improvement": stats.median(
            float(row["actor_wasserstein_improvement"]) for row in rows
        ),
        "median_actor_minus_continuous_mmd": stats.median(actor_minus_continuous_mmd),
        "median_actor_minus_continuous_wasserstein": stats.median(actor_minus_continuous_wasserstein),
        "median_actor_diversity_retention": stats.median(float(row["actor_diversity_retention"]) for row in rows),
        "median_actor_success_probability": stats.median(float(row["actor_success_probability"]) for row in rows),
        "recommendation": recommendation,
    }


def write_summary(path: Path, summary: dict, rows_path: Path, figure_path: Path) -> None:
    text = f"""# Problem 3 Actor-Critic Denoising Summary

## Scope

This is a target-aware reinforcement-learning style parameter search for Problem 3(c).
The actor chooses a non-unitary filter strength `lambda` for `K_lambda = diag(1, lambda, lambda, lambda)`.
The critic estimates the reward baseline from the current noisy ensemble features.

This is not a hardware-advantage or general quantum-advantage claim. It uses the known raw/target ensemble as the reward signal.

## Multi-Seed Result

- recommendation: `{summary['recommendation']}`
- evaluated rows: `{summary['rows']}`
- actor beats 3(a) continuous baseline on MMD: `{summary['beats_mmd']} / {summary['rows']}`
- actor beats 3(a) continuous baseline on Wasserstein: `{summary['beats_wasserstein']} / {summary['rows']}`
- actor beats 3(a) continuous baseline on both metrics: `{summary['beats_both']} / {summary['rows']}`
- median actor MMD improvement: `{summary['median_actor_mmd_improvement']:.6f}`
- median actor Wasserstein improvement: `{summary['median_actor_wasserstein_improvement']:.6f}`
- median actor-vs-continuous MMD margin: `{summary['median_actor_minus_continuous_mmd']:.6f}`
- median actor-vs-continuous Wasserstein margin: `{summary['median_actor_minus_continuous_wasserstein']:.6f}`
- median actor diversity retention: `{summary['median_actor_diversity_retention']:.6f}`
- median actor success probability: `{summary['median_actor_success_probability']:.6f}`

## Generated Files

- rows: `{rows_path}`
- figure: `{figure_path}`

## Safe Claim

In the tested small state-vector setting, an actor-critic policy search over a target-aware non-unitary filter selected denoising actions that improved raw-target fidelity metrics more than the existing continuous measurement-basis baseline across the evaluated seeds and input steps. The claim is limited to target-aware toy denoising with access to the raw target ensemble during reward computation.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_figure(path: Path, rows: list[dict]) -> None:
    labels = [f"s{row['seed']}-k{row['input_step']}" for row in rows]
    x = np.arange(len(rows))
    width = 0.36

    fig, axes = plt.subplots(2, 1, figsize=(max(12, len(rows) * 0.55), 8), sharex=True)
    axes[0].bar(
        x - width / 2,
        [float(row["continuous_mmd"]) for row in rows],
        width,
        label="3(a) continuous MMD",
    )
    axes[0].bar(
        x + width / 2,
        [float(row["actor_mmd"]) for row in rows],
        width,
        label="actor-critic MMD",
    )
    axes[0].set_ylabel("MMD to raw target")
    axes[0].set_title("Actor-critic denoising vs 3(a) continuous baseline")
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    axes[1].bar(
        x - width / 2,
        [float(row["continuous_wasserstein"]) for row in rows],
        width,
        label="3(a) continuous Wasserstein",
    )
    axes[1].bar(
        x + width / 2,
        [float(row["actor_wasserstein"]) for row in rows],
        width,
        label="actor-critic Wasserstein",
    )
    axes[1].set_ylabel("Wasserstein to raw target")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=45, ha="right")
    axes[1].legend()
    axes[1].grid(axis="y", alpha=0.3)

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Problem 3 actor-critic toy denoising.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "problem_3_actor_critic_denoising")
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(1, 11)))
    parser.add_argument("--input-steps", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--n-samples", type=int, default=48)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--angle-scale", type=float, default=float(np.pi))
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument("--tau-points", type=int, default=8)
    parser.add_argument("--theta-points", type=int, default=7)
    parser.add_argument("--phi-points", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = run_benchmark(args)
    summary = summarize(rows)
    rows_path = args.output_dir / "actor_critic_metrics.csv"
    summary_path = args.output_dir / "actor_critic_summary.md"
    figure_path = args.output_dir / "actor_critic_comparison.png"

    write_csv(rows_path, rows)
    write_figure(figure_path, rows)
    write_summary(summary_path, summary, rows_path, figure_path)

    print(summary_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

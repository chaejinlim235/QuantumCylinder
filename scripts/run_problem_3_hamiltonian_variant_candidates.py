from __future__ import annotations

import argparse
import csv
import statistics as stats
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1b_ensemble_metrics import mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_layer, random_unitary_trajectory
from quantum_cylinder.problem_3_continuous_projected_denoising import (
    axis_basis_specs,
    continuous_basis_specs,
    ensemble_diversity,
    projected_denoising_step,
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


def evaluate_candidate(
    method: str,
    reference: np.ndarray,
    noisy: np.ndarray,
    candidate: np.ndarray,
    success_probability: float,
    extra: dict | None = None,
) -> dict:
    baseline_mmd = float(mmd_fidelity(reference, noisy))
    baseline_w = float(wasserstein_infidelity(reference, noisy))
    candidate_mmd = float(mmd_fidelity(reference, candidate))
    candidate_w = float(wasserstein_infidelity(reference, candidate))
    baseline_diversity = float(ensemble_diversity(noisy))
    candidate_diversity = float(ensemble_diversity(candidate))
    diversity_retention = candidate_diversity / max(baseline_diversity, 1e-12)
    row = {
        "method": method,
        "baseline_mmd": baseline_mmd,
        "candidate_mmd": candidate_mmd,
        "mmd_improvement": baseline_mmd - candidate_mmd,
        "baseline_wasserstein": baseline_w,
        "candidate_wasserstein": candidate_w,
        "wasserstein_improvement": baseline_w - candidate_w,
        "baseline_diversity": baseline_diversity,
        "candidate_diversity": candidate_diversity,
        "diversity_retention": diversity_retention,
        "mean_success_probability": float(success_probability),
    }
    row["score"] = (
        row["mmd_improvement"]
        + 0.5 * row["wasserstein_improvement"]
        + 0.05 * min(row["diversity_retention"] - 1.0, 0.0)
    )
    if extra:
        row.update(extra)
    return row


def apply_random_final_kick(states: np.ndarray, angle_scale: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    kicked = np.empty_like(states)
    for idx, state in enumerate(states):
        kicked[idx] = random_unitary_layer(rng, angle_scale=angle_scale) @ state
    norms = np.linalg.norm(kicked, axis=1, keepdims=True)
    return kicked / np.maximum(norms, 1e-15)


def continuous_baseline(reference: np.ndarray, noisy: np.ndarray, args: argparse.Namespace) -> tuple[dict, np.ndarray, np.ndarray]:
    taus = np.linspace(args.tau_min, args.tau_max, args.tau_points)
    specs = axis_basis_specs() + continuous_basis_specs(
        theta_points=args.theta_points,
        phi_points=args.phi_points,
        exclude_axis=True,
    )
    rows = search_projected_denoising(reference, noisy, taus=taus, basis_specs=specs)
    best = select_best_candidate(rows, min_mean_success=args.min_mean_success, min_diversity_retention=args.min_diversity)
    states, probabilities = projected_denoising_step(
        noisy,
        tau=float(best["tau"]),
        theta=float(best["theta"]),
        phi=float(best["phi"]),
    )
    return best, states, probabilities


def best_random_mixture(
    reference: np.ndarray,
    noisy: np.ndarray,
    continuous_states: np.ndarray,
    continuous_success: float,
    seed: int,
    angle_scales: list[float],
) -> dict:
    rows = []
    for angle_scale in angle_scales:
        kicked = apply_random_final_kick(continuous_states, angle_scale=angle_scale, seed=seed)
        rows.append(
            evaluate_candidate(
                "hamiltonian_then_random_final_kick",
                reference,
                noisy,
                kicked,
                continuous_success,
                extra={"random_kick_angle_scale": float(angle_scale), "second_tau": "", "second_basis": ""},
            )
        )
    return max(rows, key=lambda row: row["score"])


def best_two_way(
    reference: np.ndarray,
    noisy: np.ndarray,
    first_states: np.ndarray,
    first_probabilities: np.ndarray,
    args: argparse.Namespace,
) -> dict:
    rows = []
    basis_specs = axis_basis_specs() + continuous_basis_specs(theta_points=5, phi_points=6, exclude_axis=True)
    for tau in np.linspace(0.05, 1.25, args.second_tau_points):
        for spec in basis_specs:
            try:
                second_states, second_probabilities = projected_denoising_step(
                    first_states,
                    tau=float(tau),
                    theta=float(spec["theta"]),
                    phi=float(spec["phi"]),
                )
            except ValueError:
                continue
            combined_success = float(np.mean(first_probabilities * second_probabilities))
            rows.append(
                evaluate_candidate(
                    "hamiltonian_two_way_postselection",
                    reference,
                    noisy,
                    second_states,
                    combined_success,
                    extra={
                        "random_kick_angle_scale": "",
                        "second_tau": float(tau),
                        "second_basis": spec["basis_name"],
                    },
                )
            )
    if not rows:
        raise RuntimeError("No valid two-way Hamiltonian candidates remained.")
    eligible = [
        row
        for row in rows
        if row["mean_success_probability"] >= args.min_mean_success
        and row["diversity_retention"] >= args.min_diversity
    ]
    return max(eligible or rows, key=lambda row: row["score"])


def run(args: argparse.Namespace) -> list[dict]:
    all_rows = []
    angle_scales = [float(value) for value in args.random_kick_angle_scales]
    for seed in args.seeds:
        reference = target_ensemble(n_samples=args.n_samples, sigma=args.sigma, seed=seed)
        trajectory = random_unitary_trajectory(
            reference,
            n_steps=max(args.input_steps),
            angle_scale=args.angle_scale,
            seed=seed + 10_000,
        )
        for input_step in args.input_steps:
            noisy = trajectory[input_step]
            continuous, continuous_states, continuous_probabilities = continuous_baseline(reference, noisy, args)
            continuous_row = evaluate_candidate(
                "continuous_postselection_reference",
                reference,
                noisy,
                continuous_states,
                float(np.mean(continuous_probabilities)),
                extra={
                    "random_kick_angle_scale": "",
                    "second_tau": "",
                    "second_basis": "",
                },
            )
            mixture_row = best_random_mixture(
                reference,
                noisy,
                continuous_states,
                float(np.mean(continuous_probabilities)),
                seed=seed * 1000 + input_step,
                angle_scales=angle_scales,
            )
            two_way_row = best_two_way(reference, noisy, continuous_states, continuous_probabilities, args)
            for row in [continuous_row, mixture_row, two_way_row]:
                row.update(
                    {
                        "seed": seed,
                        "input_step": input_step,
                        "continuous_tau": float(continuous["tau"]),
                        "continuous_theta": float(continuous["theta"]),
                        "continuous_phi": float(continuous["phi"]),
                    }
                )
                all_rows.append(row)
    return all_rows


def summarize(rows: list[dict]) -> list[dict]:
    summaries = []
    for method in sorted({row["method"] for row in rows}):
        method_rows = [row for row in rows if row["method"] == method]
        summaries.append(
            {
                "method": method,
                "rows": len(method_rows),
                "positive_mmd_rows": sum(float(row["mmd_improvement"]) > 0.0 for row in method_rows),
                "positive_wasserstein_rows": sum(float(row["wasserstein_improvement"]) > 0.0 for row in method_rows),
                "median_mmd_improvement": stats.median(float(row["mmd_improvement"]) for row in method_rows),
                "median_wasserstein_improvement": stats.median(
                    float(row["wasserstein_improvement"]) for row in method_rows
                ),
                "median_diversity_retention": stats.median(float(row["diversity_retention"]) for row in method_rows),
                "median_success_probability": stats.median(
                    float(row["mean_success_probability"]) for row in method_rows
                ),
            }
        )
    return summaries


def write_summary(path: Path, summaries: list[dict], rows_path: Path, figure_path: Path) -> None:
    lines = [
        "# Problem 3 Hamiltonian Variant Candidates",
        "",
        "## Purpose",
        "",
        "This experiment restores two Problem 3(c) ideas as actual runnable candidates: Hamiltonian post-selection followed by a random-unitary final kick, and two-way Hamiltonian post-selection. They are compared against the same continuous post-selection reference under MMD/Wasserstein, diversity retention, and post-selection success probability.",
        "",
        "## Summary",
        "",
        "| Method | Rows | Positive MMD rows | Positive Wasserstein rows | Median MMD improvement | Median Wasserstein improvement | Median diversity retention | Median success probability |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summaries:
        lines.append(
            f"| {row['method']} | `{row['rows']}` | `{row['positive_mmd_rows']}` | `{row['positive_wasserstein_rows']}` "
            f"| `{row['median_mmd_improvement']:.6f}` | `{row['median_wasserstein_improvement']:.6f}` "
            f"| `{row['median_diversity_retention']:.6f}` | `{row['median_success_probability']:.6f}` |"
        )
    lines.extend(
        [
            "",
            "## Report Use",
            "",
            "- `hamiltonian_then_random_final_kick`: a mixture candidate that asks whether a small random-unitary correction after Hamiltonian post-selection improves the recovered ensemble.",
            "- `hamiltonian_two_way_postselection`: a two-stage Hamiltonian candidate that tests whether applying a second post-selected Hamiltonian map improves distance at the cost of lower success probability or diversity.",
            "- These are Problem 3(c) candidates, not replacements for the 20-seed continuous post-selection main result.",
            "",
            "## Generated Files",
            "",
            f"- rows: `{rows_path}`",
            f"- figure: `{figure_path}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_figure(path: Path, summaries: list[dict]) -> None:
    labels = [row["method"].replace("_", "\n") for row in summaries]
    x = np.arange(len(labels))
    width = 0.35
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    axes[0].bar(x - width / 2, [row["median_mmd_improvement"] for row in summaries], width, label="MMD")
    axes[0].bar(
        x + width / 2,
        [row["median_wasserstein_improvement"] for row in summaries],
        width,
        label="Wasserstein",
    )
    axes[0].set_ylabel("Median improvement")
    axes[0].set_title("Hamiltonian variant candidates: distance improvement")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend()
    axes[1].bar(x - width / 2, [row["median_diversity_retention"] for row in summaries], width, label="Diversity")
    axes[1].bar(
        x + width / 2,
        [row["median_success_probability"] for row in summaries],
        width,
        label="Success probability",
    )
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels)
    axes[1].set_ylabel("Guardrail metric")
    axes[1].set_title("Hamiltonian variant candidates: trade-off guardrails")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Problem 3 Hamiltonian mixture/two-way candidates.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "problem_3_hamiltonian_variants")
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    parser.add_argument("--input-steps", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--n-samples", type=int, default=40)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--angle-scale", type=float, default=float(np.pi))
    parser.add_argument("--tau-min", type=float, default=0.05)
    parser.add_argument("--tau-max", type=float, default=2.0)
    parser.add_argument("--tau-points", type=int, default=6)
    parser.add_argument("--theta-points", type=int, default=5)
    parser.add_argument("--phi-points", type=int, default=6)
    parser.add_argument("--second-tau-points", type=int, default=5)
    parser.add_argument("--random-kick-angle-scales", type=float, nargs="+", default=[0.02, 0.05, 0.10, 0.20])
    parser.add_argument("--min-mean-success", type=float, default=0.10)
    parser.add_argument("--min-diversity", type=float, default=0.50)
    return parser.parse_args()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()
    rows = run(args)
    summaries = summarize(rows)
    rows_path = args.output_dir / "hamiltonian_variant_metrics.csv"
    summary_path = args.output_dir / "hamiltonian_variant_summary.md"
    figure_path = args.output_dir / "hamiltonian_variant_summary.png"
    write_csv(rows_path, rows)
    write_csv(args.output_dir / "hamiltonian_variant_summary.csv", summaries)
    write_figure(figure_path, summaries)
    write_summary(summary_path, summaries, rows_path, figure_path)
    print(summary_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

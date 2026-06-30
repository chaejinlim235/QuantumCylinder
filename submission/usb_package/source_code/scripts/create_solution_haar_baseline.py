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

from quantum_cylinder.experiment_curves import distance_curve
from quantum_cylinder.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1b_ensemble_metrics import mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_trajectory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the final Problem 1(c) Haar-reference figure and table.",
    )
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "problem_1_2_baseline.json")
    parser.add_argument("--haar-draws", type=int, default=64)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "solution")
    return parser.parse_args()


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def haar_ensemble(n_samples: int, dimension: int, rng: np.random.Generator) -> np.ndarray:
    states = rng.normal(size=(n_samples, dimension)) + 1j * rng.normal(size=(n_samples, dimension))
    return states / np.linalg.norm(states, axis=1, keepdims=True)


def write_summary_table(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_haar_reference(
    path: Path,
    random_rows: list[dict],
    haar_summary: dict[str, dict[str, float]],
) -> None:
    x_values = [float(row["parameter"]) for row in random_rows]
    metric_specs = [
        ("mmd", r"Fidelity-kernel MMD, $D_{\mathrm{MMD}}$", "#1f77b4"),
        ("wasserstein", r"Wasserstein-type distance, $W_{1-F}$", "#d62728"),
    ]

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(13.5, 7.8),
        constrained_layout=True,
        gridspec_kw={"height_ratios": [1.25, 1.0]},
    )
    for col, (metric, ylabel, color) in enumerate(metric_specs):
        y_values = [float(row[metric]) for row in random_rows]
        mean = haar_summary[metric]["mean"]
        std = haar_summary[metric]["std"]
        lower = mean - std
        upper = mean + std

        axis = axes[0, col]
        axis.fill_between(
            x_values,
            lower,
            upper,
            color="#f2c94c",
            alpha=0.35,
            label=r"Haar mean $\pm$ std",
            zorder=1,
        )
        axis.plot(
            x_values,
            y_values,
            marker="o",
            markersize=6.5,
            markeredgecolor="white",
            markeredgewidth=0.9,
            color=color,
            linewidth=2.2,
            label=r"random-unitary $S_k^{\mathrm{RU}}$",
            zorder=3,
        )
        axis.axhline(
            mean,
            color="#111111",
            linestyle=(0, (6, 3)),
            linewidth=2.8,
            label="Haar reference mean",
            zorder=5,
        )
        axis.annotate(
            f"Haar mean\n{mean:.4f} +/- {std:.4f}",
            xy=(x_values[-1], mean),
            xytext=(x_values[-1] - 2.7, mean + 0.09),
            arrowprops={"arrowstyle": "->", "color": "#111111", "lw": 1.2},
            fontsize=8.5,
            bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#777777", "alpha": 0.92},
        )
        axis.set_title(ylabel)
        axis.set_xlabel("random-unitary diffusion step k")
        axis.set_ylabel(r"distance to $S_0$")
        axis.set_ylim(bottom=-0.035)
        axis.grid(alpha=0.25)
        axis.legend(loc="lower right", fontsize=8, framealpha=0.94)

        zoom_axis = axes[1, col]
        plateau_x = x_values[1:]
        plateau_y = y_values[1:]
        zoom_axis.fill_between(
            plateau_x,
            lower,
            upper,
            color="#f2c94c",
            alpha=0.42,
            label=r"Haar mean $\pm$ std",
            zorder=1,
        )
        zoom_axis.plot(
            plateau_x,
            plateau_y,
            marker="o",
            markersize=7.0,
            markeredgecolor="white",
            markeredgewidth=0.9,
            color=color,
            linewidth=2.3,
            zorder=3,
        )
        zoom_axis.axhline(mean, color="#111111", linestyle=(0, (6, 3)), linewidth=3.0, zorder=5)
        zoom_axis.axhline(lower, color="#8a6d00", linestyle=":", linewidth=1.4, zorder=4)
        zoom_axis.axhline(upper, color="#8a6d00", linestyle=":", linewidth=1.4, zorder=4)
        zoom_axis.set_title(r"Plateau zoom: $k \geq 1$")
        zoom_axis.set_xlabel("random-unitary diffusion step k")
        zoom_axis.set_ylabel(r"distance to $S_0$")
        zoom_min = min(min(plateau_y), lower) - 0.035
        zoom_max = max(max(plateau_y), upper) + 0.035
        zoom_axis.set_ylim(zoom_min, zoom_max)
        zoom_axis.grid(alpha=0.25)

    fig.suptitle(
        "Problem 1(c): random-unitary diffusion reaches a Haar-like reference plateau",
        fontsize=15,
    )
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    if args.haar_draws <= 1:
        raise ValueError("--haar-draws must be at least 2 to report mean and std.")

    config = load_config(args.config)
    n_samples = int(config["n_samples"])
    sigma = float(config["sigma"])
    seed = int(config["seed"])
    random_steps = int(config["random_steps"])
    random_angle_scale = float(config["random_angle_scale"])

    initial = target_ensemble(n_samples, sigma=sigma, seed=seed)
    trajectory = random_unitary_trajectory(
        initial,
        n_steps=random_steps,
        angle_scale=random_angle_scale,
        seed=seed + 1,
    )
    random_rows = distance_curve(initial, trajectory, parameter_name="step")

    rng = np.random.default_rng(seed + 1000)
    draws = []
    for draw_index in range(args.haar_draws):
        haar_states = haar_ensemble(n_samples, initial.shape[1], rng)
        draws.append(
            {
                "draw_index": draw_index,
                "mmd": mmd_fidelity(initial, haar_states),
                "wasserstein": wasserstein_infidelity(initial, haar_states),
            }
        )

    haar_summary = {
        metric: {
            "mean": float(np.mean([row[metric] for row in draws])),
            "std": float(np.std([row[metric] for row in draws], ddof=1)),
        }
        for metric in ("mmd", "wasserstein")
    }

    final_random = random_rows[-1]
    table_rows = [
        {
            "metric_label": "D_MMD",
            "haar_mean": f"{haar_summary['mmd']['mean']:.6f}",
            "haar_std": f"{haar_summary['mmd']['std']:.6f}",
            "final_k12_distance": f"{float(final_random['mmd']):.6f}",
            "notes": f"{args.haar_draws} Haar draws with the same ensemble size N={n_samples}; reference level, not a training target",
        },
        {
            "metric_label": "W_1_minus_F",
            "haar_mean": f"{haar_summary['wasserstein']['mean']:.6f}",
            "haar_std": f"{haar_summary['wasserstein']['std']:.6f}",
            "final_k12_distance": f"{float(final_random['wasserstein']):.6f}",
            "notes": f"{args.haar_draws} Haar draws with the same ensemble size N={n_samples}; reference level, not a training target",
        },
    ]

    figures_dir = args.output_dir / "figures"
    tables_dir = args.output_dir / "tables"
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    plot_haar_reference(figures_dir / "fig2_random_unitary_haar_baseline.png", random_rows, haar_summary)
    write_summary_table(tables_dir / "problem1_haar_reference.csv", table_rows)
    print(f"Wrote Haar reference figure and table under {args.output_dir}")


if __name__ == "__main__":
    main()

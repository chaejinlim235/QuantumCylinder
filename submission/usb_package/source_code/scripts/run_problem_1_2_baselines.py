from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.experiment_curves import closest_metric_pair, distance_curve, hamiltonian_resource_proxy
from quantum_cylinder.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1c_random_unitary_diffusion import (  # noqa: E402
    random_unitary_resource_proxy,
    random_unitary_trajectory,
)
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import hamiltonian_projected_trajectory  # noqa: E402

METRICS = ("mmd", "wasserstein")


@dataclass(frozen=True)
class ExperimentResult:
    """All derived Problem 1/2 data needed for files, plots, and summaries."""

    random_rows: list[dict]
    hamiltonian_rows: list[dict]
    resource_rows: list[dict]
    comparable_rows: list[dict]


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_args() -> argparse.Namespace:
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument("--config", type=Path, default=ROOT / "configs" / "problem_1_2_baseline.json")
    known, remaining = config_parser.parse_known_args()
    defaults = load_config(known.config)

    parser = argparse.ArgumentParser(
        parents=[config_parser],
        description="Run readable Problem 1/2 baseline experiments and write judge-facing diagnostics.",
    )
    parser.add_argument("--n-samples", type=int, default=defaults.get("n_samples", 80))
    parser.add_argument("--sigma", type=float, default=defaults.get("sigma", 0.1))
    parser.add_argument("--seed", type=int, default=defaults.get("seed", 7))
    parser.add_argument("--random-steps", type=int, default=defaults.get("random_steps", 12))
    parser.add_argument(
        "--random-angle-scale",
        type=float,
        default=defaults.get("random_angle_scale", float(np.pi)),
    )
    parser.add_argument("--hamiltonian-t-max", type=float, default=defaults.get("hamiltonian_t_max", 4.0))
    parser.add_argument(
        "--hamiltonian-time-points",
        type=int,
        default=defaults.get("hamiltonian_time_points", 13),
    )
    parser.add_argument("--measurement-basis", choices=["z", "x", "y"], default=defaults.get("measurement_basis", "z"))
    parser.add_argument("--output-dir", type=Path, default=ROOT / defaults.get("output_dir", "results/baseline"))
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


def values(rows: list[dict], key: str) -> list[float]:
    return [float(row[key]) for row in rows]


def non_initial_rows(rows: list[dict]) -> list[dict]:
    return [row for row in rows if int(row["index"]) != 0]


def native_parameter_label(row: dict) -> str:
    if row["parameter_name"] == "step":
        return f"k={int(row['parameter'])}"
    return f"t={float(row['parameter']):.2f}"


def build_target_ensemble(args: argparse.Namespace) -> np.ndarray:
    return target_ensemble(args.n_samples, sigma=args.sigma, seed=args.seed)


def run_problem_1_random_unitary(args: argparse.Namespace, initial: np.ndarray) -> list[dict]:
    trajectory = random_unitary_trajectory(
        initial,
        n_steps=args.random_steps,
        angle_scale=args.random_angle_scale,
        seed=args.seed + 1,
    )
    return distance_curve(initial, trajectory, parameter_name="step")


def run_problem_2_hamiltonian_projection(args: argparse.Namespace, initial: np.ndarray) -> tuple[np.ndarray, list[dict]]:
    times = np.linspace(0.0, args.hamiltonian_t_max, args.hamiltonian_time_points)
    trajectory = hamiltonian_projected_trajectory(
        initial,
        times=times,
        measurement_basis=args.measurement_basis,
        seed=args.seed + 2,
    )
    return times, distance_curve(initial, trajectory, parameters=times, parameter_name="time")


def build_resource_rows(args: argparse.Namespace, times: np.ndarray) -> list[dict]:
    random_rows = [random_unitary_resource_proxy(step) for step in range(args.random_steps + 1)]
    hamiltonian_rows = [
        hamiltonian_resource_proxy(float(time), measurement_basis=args.measurement_basis) for time in times
    ]
    return [*random_rows, *hamiltonian_rows]


def comparable_strength_resource_rows(
    random_rows: list[dict],
    hamiltonian_rows: list[dict],
    measurement_basis: str,
) -> list[dict]:
    """Match mechanisms by output distance, not by native x-axis value."""
    rows = []
    for metric in METRICS:
        match = closest_metric_pair(random_rows, hamiltonian_rows, metric=metric)
        random_row = random_rows[match["reference_index"]]
        hamiltonian_row = hamiltonian_rows[match["candidate_index"]]
        random_resource = random_unitary_resource_proxy(int(round(random_row["parameter"])))
        hamiltonian_resource = hamiltonian_resource_proxy(
            float(hamiltonian_row["parameter"]),
            measurement_basis=measurement_basis,
        )

        rows.append(
            {
                "matched_by": metric,
                "random_step": int(round(random_row["parameter"])),
                "hamiltonian_time": float(hamiltonian_row["parameter"]),
                "random_mmd": float(random_row["mmd"]),
                "hamiltonian_mmd": float(hamiltonian_row["mmd"]),
                "mmd_gap": abs(float(random_row["mmd"]) - float(hamiltonian_row["mmd"])),
                "random_wasserstein": float(random_row["wasserstein"]),
                "hamiltonian_wasserstein": float(hamiltonian_row["wasserstein"]),
                "wasserstein_gap": abs(float(random_row["wasserstein"]) - float(hamiltonian_row["wasserstein"])),
                "random_single_qubit_rotations": random_resource["single_qubit_rotations"],
                "random_two_qubit_entanglers": random_resource["two_qubit_entanglers"],
                "random_controls": random_resource["random_controls"],
                "hamiltonian_total_time": hamiltonian_resource["total_hamiltonian_time"],
                "hamiltonian_fixed_terms": hamiltonian_resource["fixed_hamiltonian_terms"],
                "hamiltonian_fixed_parameters": hamiltonian_resource["fixed_hamiltonian_parameters"],
                "measurement_basis": measurement_basis,
            }
        )
    return rows


def run_experiment(args: argparse.Namespace) -> ExperimentResult:
    initial = build_target_ensemble(args)
    random_rows = run_problem_1_random_unitary(args, initial)
    times, hamiltonian_rows = run_problem_2_hamiltonian_projection(args, initial)

    return ExperimentResult(
        random_rows=random_rows,
        hamiltonian_rows=hamiltonian_rows,
        resource_rows=build_resource_rows(args, times),
        comparable_rows=comparable_strength_resource_rows(
            random_rows,
            hamiltonian_rows,
            measurement_basis=args.measurement_basis,
        ),
    )


def plot_native_parameter_curves(random_rows: list[dict], hamiltonian_rows: list[dict], output_path: Path) -> None:
    """Show each mechanism on its own native x-axis: step k or time t."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)

    plot_distance_curve(
        axes[0],
        random_rows,
        title="Random-unitary diffusion",
        xlabel="step k",
    )
    plot_distance_curve(
        axes[1],
        hamiltonian_rows,
        title="Hamiltonian projected diffusion",
        xlabel="time t",
    )

    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_distance_curve(axis, rows: list[dict], title: str, xlabel: str) -> None:
    axis.plot(values(rows, "parameter"), values(rows, "mmd"), marker="o", label="MMD")
    axis.plot(values(rows, "parameter"), values(rows, "wasserstein"), marker="s", label="Wasserstein")
    axis.set_title(title)
    axis.set_xlabel(xlabel)
    axis.set_ylabel("distance to S0")
    axis.grid(alpha=0.25)
    axis.legend()


def plot_metric_aligned_comparison(random_rows: list[dict], hamiltonian_rows: list[dict], output_path: Path) -> None:
    """Compare mechanisms by output distance instead of sharing the x-axis."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)

    plot_metric_space(axes[0], random_rows, hamiltonian_rows)
    plot_nearest_metric_matches(axes[1], random_rows, hamiltonian_rows)

    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_metric_space(axis, random_rows: list[dict], hamiltonian_rows: list[dict]) -> None:
    for rows, label, color, marker in (
        (random_rows, "random-unitary", "#1f77b4", "o"),
        (hamiltonian_rows, "Hamiltonian projection", "#d62728", "s"),
    ):
        rows_to_plot = non_initial_rows(rows)
        axis.scatter(
            values(rows_to_plot, "mmd"),
            values(rows_to_plot, "wasserstein"),
            label=label,
            color=color,
            marker=marker,
            alpha=0.78,
        )
        for row in rows_to_plot:
            axis.annotate(
                native_parameter_label(row),
                (float(row["mmd"]), float(row["wasserstein"])),
                fontsize=7,
                alpha=0.68,
                xytext=(3, 3),
                textcoords="offset points",
            )

    axis.set_title("Metric-space comparison")
    axis.set_xlabel("MMD distance to S0")
    axis.set_ylabel("Wasserstein-type distance to S0")
    axis.grid(alpha=0.25)
    axis.legend()


def plot_nearest_metric_matches(axis, random_rows: list[dict], hamiltonian_rows: list[dict]) -> None:
    matches = [(metric, closest_metric_pair(random_rows, hamiltonian_rows, metric=metric)) for metric in METRICS]
    x_positions = np.arange(len(matches))
    width = 0.36

    axis.bar(
        x_positions - width / 2,
        [match["reference_metric_value"] for _, match in matches],
        width,
        label="random-unitary",
        color="#1f77b4",
        alpha=0.82,
    )
    axis.bar(
        x_positions + width / 2,
        [match["candidate_metric_value"] for _, match in matches],
        width,
        label="Hamiltonian projection",
        color="#d62728",
        alpha=0.82,
    )

    axis.set_xticks(x_positions)
    axis.set_xticklabels(["MMD", "Wasserstein"])
    axis.set_title("Nearest comparable-strength pairs")
    axis.set_ylabel("matched metric value")
    axis.grid(axis="y", alpha=0.25)
    axis.legend()

    for idx, (_, match) in enumerate(matches):
        y_position = max(match["reference_metric_value"], match["candidate_metric_value"]) + 0.025
        axis.text(
            idx,
            y_position,
            f"k={match['reference_parameter']:.0f}\n"
            f"t={match['candidate_parameter']:.2f}\n"
            f"gap={match['absolute_gap']:.4f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )


def write_summary(
    path: Path,
    args: argparse.Namespace,
    result: ExperimentResult,
) -> None:
    random_final = result.random_rows[-1]
    hamiltonian_max_mmd = max(result.hamiltonian_rows, key=lambda row: row["mmd"])
    hamiltonian_max_wasserstein = max(result.hamiltonian_rows, key=lambda row: row["wasserstein"])

    text = f"""# Problem 1/2 Baseline Summary

## Configuration

- Ensemble size `N`: {args.n_samples}
- Target width `sigma`: {args.sigma}
- Seed: {args.seed}
- Random-unitary steps: {args.random_steps}
- Random rotation angle distribution: uniform in `[-{args.random_angle_scale:.6g}, {args.random_angle_scale:.6g}]`
- Entangler: `CZ`
- Hamiltonian time grid: `linspace(0, {args.hamiltonian_t_max}, {args.hamiltonian_time_points})`
- Hamiltonian parameters: `hx = 0.8090`, `hy = 0.9045`, `J = 1.0`
- Complement qubit initial state: `|0>`
- Measurement basis: `{args.measurement_basis.upper()}`

## Problem 1 Result

The target ensemble is generated from product rotations around `|00>`.
Random-unitary diffusion applies random local `Rz Ry Rx` rotations on each qubit followed by one `CZ` entangler per step.

- Final random-unitary step: {random_final["parameter"]:.0f}
- Final MMD to `S0`: {random_final["mmd"]:.6f}
- Final Wasserstein-type distance to `S0`: {random_final["wasserstein"]:.6f}

## Problem 2 Result

Hamiltonian projected diffusion uses the fixed three-qubit Hamiltonian from the problem statement, evolves `M + F`, then projects the complement qubit.

- Max Hamiltonian MMD: {hamiltonian_max_mmd["mmd"]:.6f} at `t = {hamiltonian_max_mmd["parameter"]:.6f}`
- Max Hamiltonian Wasserstein-type distance: {hamiltonian_max_wasserstein["wasserstein"]:.6f} at `t = {hamiltonian_max_wasserstein["parameter"]:.6f}`

## Comparable Diffusion Strength

Problem 2(d) asks for a qualitative resource/control comparison at comparable diffusion strength. Random-unitary step `k`
and Hamiltonian evolution time `t` are different native parameters, so they should not be interpreted as one shared x-axis.
The comparison below matches points by the reported distance metric instead.

The nearest non-initial pairs are:

{format_comparable_rows(result.comparable_rows)}

## Interpretation

- Problem 1 shows a direct scrambling trajectory controlled by random circuit layers.
- Problem 2 shows diffusion driven by fixed Hamiltonian time evolution and projection, so the control structure is simpler even though the diffusion curve can fluctuate with time.
- Distances are computed with the same fidelity-based MMD and infidelity-cost Wasserstein-type metric for both mechanisms.
- The native parameters `k` and `t` are shown in separate panels. Cross-mechanism comparison should use the metric-aligned plot and comparable-strength resource table, not the raw horizontal locations.

## Generated Files

- `random_unitary_metrics.csv`
- `hamiltonian_metrics.csv`
- `resource_proxies.csv`
- `comparable_strength_resource_matches.csv`
- `distance_curves.png`
- `metric_aligned_comparison.png`
- `problem_1_2_settings.json`
"""
    path.write_text(text, encoding="utf-8")


def format_comparable_rows(rows: list[dict]) -> str:
    lines = []
    for row in rows:
        lines.append(
            f"- Matched by `{row['matched_by']}`: random step `{row['random_step']}` "
            f"vs Hamiltonian time `t = {row['hamiltonian_time']:.6f}`; "
            f"MMD gap `{row['mmd_gap']:.6f}`, Wasserstein gap `{row['wasserstein_gap']:.6f}`; "
            f"random controls `{row['random_controls']}`, entanglers `{row['random_two_qubit_entanglers']}`, "
            f"Hamiltonian fixed terms `{row['hamiltonian_fixed_terms']}`, total time `{row['hamiltonian_total_time']:.6f}`."
        )
    return "\n".join(lines)


def settings_payload(args: argparse.Namespace) -> dict:
    return {
        "n_samples": args.n_samples,
        "sigma": args.sigma,
        "seed": args.seed,
        "random_steps": args.random_steps,
        "random_angle_scale": args.random_angle_scale,
        "random_entangler": "cz",
        "hamiltonian_t_max": args.hamiltonian_t_max,
        "hamiltonian_time_points": args.hamiltonian_time_points,
        "hamiltonian_parameters": {"hx": 0.8090, "hy": 0.9045, "J": 1.0},
        "complement_initial_state": "|0>",
        "measurement_basis": args.measurement_basis,
        "metrics": ["fidelity_mmd", "infidelity_wasserstein"],
    }


def write_outputs(output_dir: Path, args: argparse.Namespace, result: ExperimentResult) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    write_rows(output_dir / "random_unitary_metrics.csv", result.random_rows)
    write_rows(output_dir / "hamiltonian_metrics.csv", result.hamiltonian_rows)
    write_rows(output_dir / "resource_proxies.csv", result.resource_rows)
    write_rows(output_dir / "comparable_strength_resource_matches.csv", result.comparable_rows)
    plot_native_parameter_curves(result.random_rows, result.hamiltonian_rows, output_dir / "distance_curves.png")
    plot_metric_aligned_comparison(
        result.random_rows,
        result.hamiltonian_rows,
        output_dir / "metric_aligned_comparison.png",
    )
    write_json(output_dir / "problem_1_2_settings.json", settings_payload(args))
    write_summary(output_dir / "problem_1_2_summary.md", args, result)


def main() -> None:
    args = parse_args()
    result = run_experiment(args)
    write_outputs(args.output_dir, args, result)
    print(f"Wrote Problem 1/2 metrics, plots, and summary to {args.output_dir}")


if __name__ == "__main__":
    main()

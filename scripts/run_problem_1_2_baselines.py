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

from quantum_cylinder.problem_1c_random_unitary_diffusion import (  # noqa: E402
    random_unitary_resource_proxy,
    random_unitary_trajectory,
)
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import hamiltonian_projected_trajectory  # noqa: E402
from quantum_cylinder.experiment_curves import distance_curve, hamiltonian_resource_proxy
from quantum_cylinder.problem_1a_target_ensemble import target_ensemble


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_args() -> argparse.Namespace:
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument("--config", type=Path, default=ROOT / "configs" / "problem_1_2_baseline.json")
    known, remaining = config_parser.parse_known_args()
    defaults = load_config(known.config)

    parser = argparse.ArgumentParser(parents=[config_parser])
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


def plot_curves(random_rows: list[dict], ham_rows: list[dict], output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)

    axes[0].plot([r["parameter"] for r in random_rows], [r["mmd"] for r in random_rows], marker="o", label="MMD")
    axes[0].plot(
        [r["parameter"] for r in random_rows],
        [r["wasserstein"] for r in random_rows],
        marker="s",
        label="Wasserstein",
    )
    axes[0].set_title("Random-unitary diffusion")
    axes[0].set_xlabel("step k")
    axes[0].set_ylabel("distance to S0")
    axes[0].grid(alpha=0.25)
    axes[0].legend()

    axes[1].plot([r["parameter"] for r in ham_rows], [r["mmd"] for r in ham_rows], marker="o", label="MMD")
    axes[1].plot(
        [r["parameter"] for r in ham_rows],
        [r["wasserstein"] for r in ham_rows],
        marker="s",
        label="Wasserstein",
    )
    axes[1].set_title("Hamiltonian projected diffusion")
    axes[1].set_xlabel("time t")
    axes[1].set_ylabel("distance to S0")
    axes[1].grid(alpha=0.25)
    axes[1].legend()

    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def write_summary(
    path: Path,
    args: argparse.Namespace,
    random_rows: list[dict],
    ham_rows: list[dict],
) -> None:
    random_final = random_rows[-1]
    ham_max_mmd = max(ham_rows, key=lambda row: row["mmd"])
    ham_max_wasserstein = max(ham_rows, key=lambda row: row["wasserstein"])

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

- Max Hamiltonian MMD: {ham_max_mmd["mmd"]:.6f} at `t = {ham_max_mmd["parameter"]:.6f}`
- Max Hamiltonian Wasserstein-type distance: {ham_max_wasserstein["wasserstein"]:.6f} at `t = {ham_max_wasserstein["parameter"]:.6f}`

## Interpretation

- Problem 1 shows a direct scrambling trajectory controlled by random circuit layers.
- Problem 2 shows diffusion driven by fixed Hamiltonian time evolution and projection, so the control structure is simpler even though the diffusion curve can fluctuate with time.
- Distances are computed with the same fidelity-based MMD and infidelity-cost Wasserstein-type metric for both mechanisms.

## Generated Files

- `random_unitary_metrics.csv`
- `hamiltonian_metrics.csv`
- `resource_proxies.csv`
- `distance_curves.png`
- `problem_1_2_settings.json`
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    s0 = target_ensemble(args.n_samples, sigma=args.sigma, seed=args.seed)

    random_traj = random_unitary_trajectory(
        s0,
        n_steps=args.random_steps,
        angle_scale=args.random_angle_scale,
        seed=args.seed + 1,
    )
    random_rows = distance_curve(s0, random_traj, parameter_name="step")

    times = np.linspace(0.0, args.hamiltonian_t_max, args.hamiltonian_time_points)
    ham_traj = hamiltonian_projected_trajectory(
        s0,
        times=times,
        measurement_basis=args.measurement_basis,
        seed=args.seed + 2,
    )
    ham_rows = distance_curve(s0, ham_traj, parameters=times, parameter_name="time")

    resource_rows = []
    resource_rows.extend(random_unitary_resource_proxy(k) for k in range(args.random_steps + 1))
    resource_rows.extend(hamiltonian_resource_proxy(float(t), measurement_basis=args.measurement_basis) for t in times)

    write_rows(output_dir / "random_unitary_metrics.csv", random_rows)
    write_rows(output_dir / "hamiltonian_metrics.csv", ham_rows)
    write_rows(output_dir / "resource_proxies.csv", resource_rows)
    plot_curves(random_rows, ham_rows, output_dir / "distance_curves.png")
    write_json(
        output_dir / "problem_1_2_settings.json",
        {
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
        },
    )
    write_summary(output_dir / "problem_1_2_summary.md", args, random_rows, ham_rows)

    print(f"Wrote metrics and plot to {output_dir}")


if __name__ == "__main__":
    main()

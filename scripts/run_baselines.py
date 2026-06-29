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

from quantum_cylinder.diffusion import (  # noqa: E402
    hamiltonian_projected_trajectory,
    random_unitary_resource_proxy,
    random_unitary_trajectory,
)
from quantum_cylinder.experiments import distance_curve, hamiltonian_resource_proxy
from quantum_cylinder.states import target_ensemble


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_args() -> argparse.Namespace:
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument("--config", type=Path, default=ROOT / "configs" / "baseline.json")
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

    print(f"Wrote metrics and plot to {output_dir}")


if __name__ == "__main__":
    main()

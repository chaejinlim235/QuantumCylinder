from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.bloch_vectors import ensemble_bloch_vectors, summarize_bloch_vectors  # noqa: E402
from quantum_cylinder.problem_1a_target_ensemble import target_ensemble  # noqa: E402
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_trajectory  # noqa: E402
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import hamiltonian_projected_trajectory  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot reduced Bloch-vector comparison for Problem 2(c).")
    parser.add_argument("--n-samples", type=int, default=80)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--random-steps", type=int, default=12)
    parser.add_argument("--measurement-basis", choices=["z", "x", "y"], default="z")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "quantitative_evaluation")
    return parser.parse_args()


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def draw_wire_sphere(axis) -> None:
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    axis.plot_wireframe(x, y, z, color="#BBBBBB", linewidth=0.25, alpha=0.35)
    axis.set_xlim(-1, 1)
    axis.set_ylim(-1, 1)
    axis.set_zlim(-1, 1)
    axis.set_xlabel("<X>")
    axis.set_ylabel("<Y>")
    axis.set_zlabel("<Z>")


def plot_for_qubit(ensembles: dict[str, np.ndarray], qubit: int, output_path: Path) -> list[dict]:
    colors = {
        "S0": "#1f77b4",
        "random_S1": "#ff7f0e",
        "random_S7": "#d62728",
        "random_S12": "#9467bd",
        "ham_t0.333": "#2ca02c",
        "ham_t1.000": "#17becf",
        "ham_t4.000": "#8c564b",
    }

    fig = plt.figure(figsize=(8, 7), constrained_layout=True)
    axis = fig.add_subplot(111, projection="3d")
    draw_wire_sphere(axis)
    axis.set_title(f"Reduced Bloch-vector clouds, qubit {qubit}")

    rows = []
    for label, ensemble in ensembles.items():
        vectors = ensemble_bloch_vectors(ensemble, qubit=qubit)
        summary = summarize_bloch_vectors(vectors)
        rows.append({"label": label, "qubit": qubit, **summary})
        axis.scatter(
            vectors[:, 0],
            vectors[:, 1],
            vectors[:, 2],
            s=13,
            alpha=0.68,
            label=label,
            color=colors.get(label),
        )

    axis.legend(loc="upper left", fontsize=8)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return rows


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    s0 = target_ensemble(args.n_samples, sigma=args.sigma, seed=args.seed)
    random_traj = random_unitary_trajectory(s0, n_steps=args.random_steps, seed=args.seed + 1)
    ham_times = np.array([1.0 / 3.0, 1.0, 4.0])
    ham_traj = hamiltonian_projected_trajectory(
        s0,
        times=ham_times,
        measurement_basis=args.measurement_basis,
        seed=args.seed + 2,
    )

    ensembles = {
        "S0": s0,
        "random_S1": random_traj[1],
        "random_S7": random_traj[min(7, args.random_steps)],
        "random_S12": random_traj[min(12, args.random_steps)],
        "ham_t0.333": ham_traj[0],
        "ham_t1.000": ham_traj[1],
        "ham_t4.000": ham_traj[2],
    }

    rows = []
    for qubit in (0, 1):
        output_path = args.output_dir / f"problem_2c_bloch_qubit_{qubit}.png"
        rows.extend(plot_for_qubit(ensembles, qubit=qubit, output_path=output_path))

    write_rows(args.output_dir / "problem_2c_bloch_summary.csv", rows)
    summary = f"""# Problem 2(c) Reduced Bloch-Vector Comparison

## Setup

- N: `{args.n_samples}`
- sigma: `{args.sigma}`
- seed: `{args.seed}`
- measurement basis: `{args.measurement_basis}`

## Generated Figures

- `problem_2c_bloch_qubit_0.png`
- `problem_2c_bloch_qubit_1.png`
- `problem_2c_bloch_summary.csv`

## Interpretation Guardrail

A two-qubit pure state cannot be represented by one ordinary Bloch sphere.
These figures show reduced single-qubit Bloch-vector clouds for qubit 0 and
qubit 1, so they are qualitative diagnostics for cluster spreading and
projection effects, not a complete two-qubit state-space visualization.
"""
    (args.output_dir / "problem_2c_bloch_summary.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

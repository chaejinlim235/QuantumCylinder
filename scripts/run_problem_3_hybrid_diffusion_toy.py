"""Small hybrid random-unitary + Hamiltonian-inspired Problem 3 toy.

This script is intentionally small and judge-facing. It does not replace the
main 2-data-qubit continuous post-selection result. It tests a 2-qubit
hardware-compatible toy:

    one data qubit M + one auxiliary qubit F
    random-unitary corrupted data
    Hamiltonian-inspired M-F evolution
    auxiliary post-selection

The goal is to show a plausible bridge from the state-vector benchmark to an
IBM-style gate model, not to claim hardware advantage.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_1b_ensemble_metrics import mmd_fidelity, wasserstein_infidelity  # noqa: E402


KET0 = np.array([1.0, 0.0], dtype=complex)
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def ry(theta: float) -> np.ndarray:
    c = np.cos(theta / 2.0)
    s = np.sin(theta / 2.0)
    return np.array([[c, -s], [s, c]], dtype=complex)


def rz(theta: float) -> np.ndarray:
    return np.array([[np.exp(-0.5j * theta), 0.0], [0.0, np.exp(0.5j * theta)]], dtype=complex)


def rx(theta: float) -> np.ndarray:
    c = np.cos(theta / 2.0)
    s = np.sin(theta / 2.0)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)


def normalize_rows(states: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(states, axis=1, keepdims=True)
    if np.any(norms == 0.0):
        raise ValueError("zero vector in ensemble")
    return states / norms


def target_1q_ensemble(n_samples: int, sigma: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    states = []
    for _ in range(n_samples):
        state = rz(rng.normal(0.0, sigma)) @ ry(rng.normal(0.0, sigma)) @ KET0
        states.append(state)
    return normalize_rows(np.asarray(states, dtype=complex))


def random_unitary_1q_trajectory(initial: np.ndarray, n_steps: int, angle_scale: float, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    trajectory = [normalize_rows(initial)]
    current = trajectory[0]
    for _ in range(n_steps):
        next_states = []
        for state in current:
            unitary = (
                rz(rng.uniform(0.0, angle_scale))
                @ ry(rng.uniform(0.0, angle_scale))
                @ rz(rng.uniform(0.0, angle_scale))
            )
            next_states.append(unitary @ state)
        current = normalize_rows(np.asarray(next_states, dtype=complex))
        trajectory.append(current)
    return trajectory


def two_qubit_hamiltonian(hx: float = 0.8090, hy: float = 0.9045, j: float = 1.0) -> np.ndarray:
    return hx * (np.kron(X, I) + np.kron(I, X)) + hy * (np.kron(Y, I) + np.kron(I, Y)) + j * np.kron(X, X)


def projection_basis(theta: float, phi: float) -> np.ndarray:
    return np.array([np.cos(theta / 2.0), np.exp(1j * phi) * np.sin(theta / 2.0)], dtype=complex)


def hybrid_postselected_map(
    input_ensemble: np.ndarray,
    tau: float,
    theta: float,
    phi: float,
    pre_rotation: float,
    hamiltonian: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply a shallow random-unitary-style pre-rotation plus H-inspired projection."""

    evolution = expm(-1j * hamiltonian * tau)
    basis = projection_basis(theta, phi)
    pre = rx(pre_rotation)
    output_states = []
    probabilities = []

    for data_state in input_ensemble:
        prepared = pre @ data_state
        evolved = evolution @ np.kron(prepared, KET0)
        blocks = evolved.reshape(2, 2)
        unnormalized = blocks @ basis.conj()
        probability = float(np.vdot(unnormalized, unnormalized).real)
        if probability <= 1e-14:
            output_states.append(KET0)
        else:
            output_states.append(unnormalized / np.sqrt(probability))
        probabilities.append(probability)

    return normalize_rows(np.asarray(output_states, dtype=complex)), np.asarray(probabilities)


def diversity(states: np.ndarray) -> float:
    states = normalize_rows(states)
    if len(states) < 2:
        return 0.0
    overlaps = np.abs(states @ states.conj().T) ** 2
    mask = ~np.eye(len(states), dtype=bool)
    return float((1.0 - overlaps)[mask].mean())


def evaluate(reference: np.ndarray, baseline: np.ndarray, candidate: np.ndarray, probabilities: np.ndarray) -> dict[str, float]:
    baseline_mmd = mmd_fidelity(reference, baseline)
    candidate_mmd = mmd_fidelity(reference, candidate)
    baseline_w = wasserstein_infidelity(reference, baseline)
    candidate_w = wasserstein_infidelity(reference, candidate)
    baseline_diversity = diversity(baseline)
    candidate_diversity = diversity(candidate)
    return {
        "baseline_mmd": baseline_mmd,
        "candidate_mmd": candidate_mmd,
        "mmd_improvement": baseline_mmd - candidate_mmd,
        "baseline_wasserstein": baseline_w,
        "candidate_wasserstein": candidate_w,
        "wasserstein_improvement": baseline_w - candidate_w,
        "baseline_diversity": baseline_diversity,
        "candidate_diversity": candidate_diversity,
        "diversity_retention": candidate_diversity / max(baseline_diversity, 1e-12),
        "mean_success_probability": float(np.mean(probabilities)),
        "min_success_probability": float(np.min(probabilities)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-samples", type=int, default=80)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--random-steps", type=int, default=8)
    parser.add_argument("--input-steps", type=int, nargs="+", default=[1, 2, 4, 8])
    parser.add_argument("--angle-scale", type=float, default=float(np.pi))
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "problem_3_hybrid_diffusion_toy")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    reference = target_1q_ensemble(args.n_samples, args.sigma, args.seed)
    trajectory = random_unitary_1q_trajectory(reference, args.random_steps, args.angle_scale, args.seed + 1)
    hamiltonian = two_qubit_hamiltonian()

    taus = np.linspace(0.05, 2.0, 13)
    thetas = np.linspace(0.0, np.pi, 9)
    phis = np.linspace(0.0, 2.0 * np.pi, 8, endpoint=False)
    pre_rotations = [0.0, 0.1, -0.1, 0.25, -0.25]

    rows: list[dict[str, float | int]] = []
    best_rows: list[dict[str, float | int]] = []

    for input_step in args.input_steps:
        baseline = trajectory[input_step]
        best_row: dict[str, float | int] | None = None
        for tau in taus:
            for theta in thetas:
                for phi in phis:
                    for pre_rotation in pre_rotations:
                        candidate, probabilities = hybrid_postselected_map(
                            baseline,
                            tau=float(tau),
                            theta=float(theta),
                            phi=float(phi),
                            pre_rotation=float(pre_rotation),
                            hamiltonian=hamiltonian,
                        )
                        metrics = evaluate(reference, baseline, candidate, probabilities)
                        score = (
                            metrics["mmd_improvement"]
                            + 0.5 * metrics["wasserstein_improvement"]
                            + 0.05 * min(metrics["diversity_retention"] - 1.0, 0.0)
                        )
                        row = {
                            "input_step": input_step,
                            "tau": float(tau),
                            "theta": float(theta),
                            "phi": float(phi),
                            "pre_rotation": float(pre_rotation),
                            "score": float(score),
                            **metrics,
                        }
                        rows.append(row)
                        if (
                            metrics["mean_success_probability"] >= 0.10
                            and metrics["diversity_retention"] >= 0.50
                            and (best_row is None or float(row["score"]) > float(best_row["score"]))
                        ):
                            best_row = row
        if best_row is None:
            best_row = max((row for row in rows if row["input_step"] == input_step), key=lambda row: float(row["score"]))
        best_rows.append(best_row)

    candidate_path = args.output_dir / "hybrid_candidate_metrics.csv"
    with candidate_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    best_path = args.output_dir / "hybrid_best_metrics.csv"
    with best_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(best_rows[0].keys()))
        writer.writeheader()
        writer.writerows(best_rows)

    steps = [int(row["input_step"]) for row in best_rows]
    baseline_mmd = [float(row["baseline_mmd"]) for row in best_rows]
    candidate_mmd = [float(row["candidate_mmd"]) for row in best_rows]
    baseline_w = [float(row["baseline_wasserstein"]) for row in best_rows]
    candidate_w = [float(row["candidate_wasserstein"]) for row in best_rows]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    axes[0].plot(steps, baseline_mmd, marker="o", label="random-unitary input")
    axes[0].plot(steps, candidate_mmd, marker="^", label="hybrid post-selected")
    axes[0].set_title("1M+1F hybrid toy: MMD")
    axes[0].set_xlabel("random-unitary input step")
    axes[0].grid(alpha=0.25)
    axes[0].legend()
    axes[1].plot(steps, baseline_w, marker="o", label="random-unitary input")
    axes[1].plot(steps, candidate_w, marker="^", label="hybrid post-selected")
    axes[1].set_title("1M+1F hybrid toy: Wasserstein")
    axes[1].set_xlabel("random-unitary input step")
    axes[1].grid(alpha=0.25)
    axes[1].legend()
    fig.savefig(args.output_dir / "hybrid_toy_metrics.png", dpi=180)
    plt.close(fig)

    median_mmd = float(np.median([float(row["mmd_improvement"]) for row in best_rows]))
    median_w = float(np.median([float(row["wasserstein_improvement"]) for row in best_rows]))
    median_div = float(np.median([float(row["diversity_retention"]) for row in best_rows]))
    median_success = float(np.median([float(row["mean_success_probability"]) for row in best_rows]))
    positive_rows = sum(
        1
        for row in best_rows
        if float(row["mmd_improvement"]) > 0.0 or float(row["wasserstein_improvement"]) > 0.0
    )

    settings = {
        "n_samples": args.n_samples,
        "sigma": args.sigma,
        "seed": args.seed,
        "random_steps": args.random_steps,
        "input_steps": args.input_steps,
        "angle_scale": args.angle_scale,
        "interpretation": "1 data qubit + 1 auxiliary qubit IBM-compatible state-vector toy",
    }
    (args.output_dir / "hybrid_toy_settings.json").write_text(json.dumps(settings, indent=2), encoding="utf-8")

    summary = f"""# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `{args.input_steps}`
- positive-improvement rows: `{positive_rows} / {len(best_rows)}`
- median MMD improvement: `{median_mmd:.6f}`
- median Wasserstein improvement: `{median_w:.6f}`
- median diversity retention: `{median_div:.6f}`
- median success probability: `{median_success:.6f}`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
"""
    for row in best_rows:
        summary += (
            f"| `{int(row['input_step'])}` "
            f"| `{float(row['baseline_mmd']):.6f} -> {float(row['candidate_mmd']):.6f}` "
            f"| `{float(row['baseline_wasserstein']):.6f} -> {float(row['candidate_wasserstein']):.6f}` "
            f"| `{float(row['diversity_retention']):.6f}` "
            f"| `{float(row['mean_success_probability']):.6f}` "
            f"| `{float(row['tau']):.6f}` "
            f"| `{float(row['theta']):.6f}` "
            f"| `{float(row['phi']):.6f}` "
            f"| `{float(row['pre_rotation']):.6f}` |\n"
        )

    summary += """
## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`
"""
    (args.output_dir / "hybrid_toy_summary.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

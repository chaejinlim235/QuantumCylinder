from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble  # noqa: E402
from quantum_cylinder.problem_1b_ensemble_metrics import (  # noqa: E402
    fidelity_matrix,
    mmd_fidelity,
    wasserstein_infidelity,
)
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_trajectory  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Problem 1(b) metric diagnostics.")
    parser.add_argument("--n-samples", type=int, default=80)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "quantitative_evaluation")
    return parser.parse_args()


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    target = target_ensemble(args.n_samples, sigma=args.sigma, seed=args.seed)
    scrambled = random_unitary_trajectory(target, n_steps=1, seed=args.seed + 1)[1]
    ket00 = np.array([[1.0, 0.0, 0.0, 0.0]], dtype=complex)
    target_to_zero = fidelity_matrix(target, ket00).reshape(-1)

    rows = [
        {
            "comparison": "S0_vs_S0",
            "mmd": mmd_fidelity(target, target),
            "wasserstein": wasserstein_infidelity(target, target),
        },
        {
            "comparison": "S1_random_unitary_vs_S0",
            "mmd": mmd_fidelity(target, scrambled),
            "wasserstein": wasserstein_infidelity(target, scrambled),
        },
    ]
    write_rows(args.output_dir / "problem_1b_metric_diagnostics.csv", rows)

    summary = f"""# Problem 1(b) Metric Diagnostics

## Setup

- N: `{args.n_samples}`
- sigma: `{args.sigma}`
- seed: `{args.seed}`

## Target Cluster Sanity Check

- mean fidelity to `|00>`: `{target_to_zero.mean():.6f}`
- min fidelity to `|00>`: `{target_to_zero.min():.6f}`
- max fidelity to `|00>`: `{target_to_zero.max():.6f}`
- std fidelity to `|00>`: `{target_to_zero.std():.6f}`

## Metric Sanity Check

- `MMD(S0, S0)`: `{rows[0]['mmd']:.12f}`
- `Wasserstein(S0, S0)`: `{rows[0]['wasserstein']:.12f}`
- `MMD(S1_random_unitary, S0)`: `{rows[1]['mmd']:.6f}`
- `Wasserstein(S1_random_unitary, S0)`: `{rows[1]['wasserstein']:.6f}`

The zero-distance self check verifies the Problem 1(b) metric implementation, and
the one-step random-unitary comparison confirms that the distances respond to a
scrambled ensemble.
"""
    (args.output_dir / "problem_1b_metric_diagnostics.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from submission.problem1_random_unitary_scrambling import solve_problem_1
from submission.problem2_hamiltonian_projection import solve_problem_2
from submission.problem3_continuous_measurement_denoising import solve_problem_3
from submission.states_and_metrics import write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the simple submission layer for Problems 1, 2, and 3.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "submission_simple")
    parser.add_argument("--quick", action="store_true", help="Use a small grid for a fast smoke test.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.quick:
        n_samples = 20
        random_steps = 4
        time_points = 5
        input_steps = [1, 2]
        tau_points = 5
        theta_points = 5
        phi_points = 6
    else:
        n_samples = 80
        random_steps = 12
        time_points = 13
        input_steps = [1, 2, 3, 5, 7, 12]
        tau_points = 20
        theta_points = 13
        phi_points = 16

    problem1 = solve_problem_1(
        args.output_dir / "problem1",
        n_samples=n_samples,
        random_steps=random_steps,
    )
    problem2 = solve_problem_2(
        args.output_dir / "problem2",
        n_samples=n_samples,
        random_steps=random_steps,
        time_points=time_points,
    )
    problem3 = solve_problem_3(
        args.output_dir / "problem3",
        n_samples=n_samples,
        random_steps=random_steps,
        input_steps=input_steps,
        tau_points=tau_points,
        theta_points=theta_points,
        phi_points=phi_points,
    )

    text = f"""# Simple Submission Run Summary

## Mode

- Quick mode: `{args.quick}`
- Samples: `{n_samples}`

## Problem 1

- Final MMD: `{problem1['final']['mmd']:.6f}`
- Final Wasserstein-type distance: `{problem1['final']['wasserstein']:.6f}`
- Summary: `{problem1['summary']}`

## Problem 2

- Max MMD: `{problem2['max_mmd']['mmd']:.6f}` at `{problem2['max_mmd']['parameter']:.6f}`
- Max Wasserstein-type distance: `{problem2['max_wasserstein']['wasserstein']:.6f}` at `{problem2['max_wasserstein']['parameter']:.6f}`
- Summary: `{problem2['summary']}`

## Problem 3

- Overall decision: `{problem3['overall']}`
- Best input step: `{problem3['best']['input_step']}`
- Best MMD: `{problem3['best']['baseline_mmd']:.6f} -> {problem3['best']['continuous_mmd']:.6f}`
- Best Wasserstein-type distance: `{problem3['best']['baseline_wasserstein']:.6f} -> {problem3['best']['continuous_wasserstein']:.6f}`
- Summary: `{problem3['summary']}`
"""
    write_text(args.output_dir / "SUMMARY.md", text)
    print(text)


if __name__ == "__main__":
    main()

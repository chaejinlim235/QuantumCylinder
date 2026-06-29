from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from quantum_cylinder.experiment_curves import closest_metric_pair, hamiltonian_resource_proxy
from quantum_cylinder.implementations.qiskit.problem_1c_random_unitary_diffusion import (
    random_unitary_resource_proxy,
    random_unitary_trajectory,
)
from quantum_cylinder.implementations.qiskit.problem_2_hamiltonian_projected_diffusion import (
    hamiltonian_projected_trajectory,
)

from submission.states_and_metrics import distance_to_target, make_target_ensemble, write_csv, write_text


def _distance_rows(target: np.ndarray, trajectory: list[np.ndarray], parameters: list[float], name: str) -> list[dict]:
    rows = []
    for index, (parameter, ensemble) in enumerate(zip(parameters, trajectory, strict=True)):
        rows.append(
            {
                "index": index,
                "parameter_name": name,
                "parameter": float(parameter),
                **distance_to_target(target, ensemble),
            }
        )
    return rows


def solve_problem_2(
    output_dir: Path,
    n_samples: int = 80,
    sigma: float = 0.10,
    seed: int = 7,
    random_steps: int = 12,
    t_max: float = 4.0,
    time_points: int = 13,
    measurement_basis: str = "z",
) -> dict:
    """Problem 2: Qiskit-backed Hamiltonian evolution plus complement projection."""
    target = make_target_ensemble(n_samples=n_samples, sigma=sigma, seed=seed)

    random_trajectory = random_unitary_trajectory(target, n_steps=random_steps, seed=seed + 1)
    random_rows = _distance_rows(target, random_trajectory, list(range(random_steps + 1)), "random_step")

    # Fixed Hamiltonian acts on M0, M1, F. Projection of F returns a 2-qubit ensemble.
    times = np.linspace(0.0, t_max, time_points)
    projected_trajectory = hamiltonian_projected_trajectory(
        target,
        times=times,
        measurement_basis=measurement_basis,
        seed=seed + 2,
    )
    hamiltonian_rows = _distance_rows(target, projected_trajectory, list(times), "time")

    resource_rows = []
    for metric in ("mmd", "wasserstein"):
        match = closest_metric_pair(random_rows, hamiltonian_rows, metric=metric)
        random_step = int(round(random_rows[match["reference_index"]]["parameter"]))
        hamiltonian_time = float(hamiltonian_rows[match["candidate_index"]]["parameter"])
        resource_rows.append(
            {
                "matched_by": metric,
                "random_step": random_step,
                "hamiltonian_time": hamiltonian_time,
                "metric_gap": float(match["absolute_gap"]),
                **random_unitary_resource_proxy(random_step),
                **{
                    f"hamiltonian_{key}": value
                    for key, value in hamiltonian_resource_proxy(
                        hamiltonian_time,
                        measurement_basis=measurement_basis,
                    ).items()
                },
            }
        )

    max_mmd = max(hamiltonian_rows, key=lambda row: row["mmd"])
    max_wasserstein = max(hamiltonian_rows, key=lambda row: row["wasserstein"])
    summary = f"""# Problem 2 Simple Summary

## Physical Operation

- Add one complement qubit `F` initialized as `|0>`.
- Backend: Qiskit `SparsePauliOp`, `Operator`, and `Statevector`.
- Evolve the three-qubit system `(M0, M1, F)` under the fixed Hamiltonian.
- Measure/project `F` in the `{measurement_basis.upper()}` basis.
- Keep the projected two-qubit data state as the new ensemble sample.

## Result

- Max MMD: `{max_mmd['mmd']:.6f}` at time `{max_mmd['parameter']:.6f}`
- Max Wasserstein-type distance: `{max_wasserstein['wasserstein']:.6f}` at time `{max_wasserstein['parameter']:.6f}`

## Comparable Strength

The file `problem2_resource_matches.csv` matches random-unitary and Hamiltonian-projected points with similar diffusion strength.

## Output

- `problem2_hamiltonian_projection_metrics.csv`
- `problem2_resource_matches.csv`
"""

    write_csv(output_dir / "problem2_hamiltonian_projection_metrics.csv", hamiltonian_rows)
    write_csv(output_dir / "problem2_resource_matches.csv", resource_rows)
    write_text(output_dir / "problem2_summary.md", summary)
    return {
        "rows": hamiltonian_rows,
        "resource_rows": resource_rows,
        "summary": output_dir / "problem2_summary.md",
        "max_mmd": max_mmd,
        "max_wasserstein": max_wasserstein,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the simple Problem 2 submission layer.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "submission_simple" / "problem2")
    parser.add_argument("--n-samples", type=int, default=80)
    parser.add_argument("--sigma", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--random-steps", type=int, default=12)
    parser.add_argument("--t-max", type=float, default=4.0)
    parser.add_argument("--time-points", type=int, default=13)
    parser.add_argument("--measurement-basis", choices=["z", "x", "y"], default="z")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = solve_problem_2(
        args.output_dir,
        n_samples=args.n_samples,
        sigma=args.sigma,
        seed=args.seed,
        random_steps=args.random_steps,
        t_max=args.t_max,
        time_points=args.time_points,
        measurement_basis=args.measurement_basis,
    )
    max_mmd = result["max_mmd"]
    print(f"Problem 2 max MMD={max_mmd['mmd']:.6f} at t={max_mmd['parameter']:.6f}")


if __name__ == "__main__":
    main()

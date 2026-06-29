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

from quantum_cylinder.experiment_curves import closest_metric_pair, distance_curve, hamiltonian_resource_proxy
from quantum_cylinder.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1c_random_unitary_diffusion import (
    random_unitary_resource_proxy,
    random_unitary_trajectory,
)
from quantum_cylinder.problem_2_hamiltonian_projected_diffusion import hamiltonian_projected_trajectory


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def parse_args() -> argparse.Namespace:
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument("--config", type=Path, default=ROOT / "configs" / "problem_1_2_baseline.json")
    known, remaining = config_parser.parse_known_args()
    defaults = load_config(known.config)

    parser = argparse.ArgumentParser(parents=[config_parser])
    parser.add_argument("--n-samples", type=int, default=defaults.get("n_samples", 80))
    parser.add_argument("--sigma", type=float, default=defaults.get("sigma", 0.10))
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
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "problem_1_2_requirement_report",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=ROOT / "docs" / "14_problem_1_2_requirement_report.md",
    )
    return parser.parse_args(remaining)


def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
        file.write("\n")


def plot_curves(random_rows: list[dict], hamiltonian_rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)

    axes[0].plot([row["parameter"] for row in random_rows], [row["mmd"] for row in random_rows], marker="o")
    axes[0].plot([row["parameter"] for row in random_rows], [row["wasserstein"] for row in random_rows], marker="s")
    axes[0].set_title("Problem 1 random-unitary")
    axes[0].set_xlabel("diffusion step k")
    axes[0].set_ylabel("distance to S0")
    axes[0].grid(alpha=0.25)
    axes[0].legend(["MMD", "Wasserstein"])

    axes[1].plot(
        [row["parameter"] for row in hamiltonian_rows],
        [row["mmd"] for row in hamiltonian_rows],
        marker="o",
    )
    axes[1].plot(
        [row["parameter"] for row in hamiltonian_rows],
        [row["wasserstein"] for row in hamiltonian_rows],
        marker="s",
    )
    axes[1].set_title("Problem 2 Hamiltonian projected")
    axes[1].set_xlabel("evolution time t")
    axes[1].set_ylabel("distance to S0")
    axes[1].grid(alpha=0.25)
    axes[1].legend(["MMD", "Wasserstein"])

    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def comparable_strength_resource_rows(
    random_rows: list[dict],
    hamiltonian_rows: list[dict],
    measurement_basis: str,
) -> list[dict]:
    rows = []
    for metric in ("mmd", "wasserstein"):
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
                "random_single_qubit_rotations": int(random_resource["single_qubit_rotations"]),
                "random_two_qubit_entanglers": int(random_resource["two_qubit_entanglers"]),
                "random_controls": int(random_resource["random_controls"]),
                "hamiltonian_total_time": float(hamiltonian_resource["total_hamiltonian_time"]),
                "hamiltonian_fixed_terms": int(hamiltonian_resource["fixed_hamiltonian_terms"]),
                "hamiltonian_fixed_parameters": int(hamiltonian_resource["fixed_hamiltonian_parameters"]),
                "measurement_basis": measurement_basis,
            }
        )
    return rows


def markdown_table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    def cell(value: object) -> str:
        if isinstance(value, float):
            rendered = f"{value:.6f}"
        else:
            rendered = str(value)
        return rendered.replace("|", r"\|")

    header = "| " + " | ".join(label for label, _ in columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = [cell(row[key]) for _, key in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def qualitative_behavior(rows: list[dict], parameter_name: str) -> str:
    first = rows[0]
    last = rows[-1]
    max_mmd = max(rows, key=lambda row: row["mmd"])
    max_wasserstein = max(rows, key=lambda row: row["wasserstein"])
    label = parameter_name.capitalize()
    return (
        f"{label} trajectory starts at MMD {first['mmd']:.6f} and Wasserstein {first['wasserstein']:.6f}, "
        f"ends at MMD {last['mmd']:.6f} and Wasserstein {last['wasserstein']:.6f}, "
        f"with peak MMD {max_mmd['mmd']:.6f} at {parameter_name} {max_mmd['parameter']:.6f} "
        f"and peak Wasserstein {max_wasserstein['wasserstein']:.6f} at {parameter_name} "
        f"{max_wasserstein['parameter']:.6f}."
    )


def build_report(
    args: argparse.Namespace,
    target_states: np.ndarray,
    random_rows: list[dict],
    hamiltonian_rows: list[dict],
    comparable_rows: list[dict],
) -> str:
    random_final = random_rows[-1]
    hamiltonian_max_mmd = max(hamiltonian_rows, key=lambda row: row["mmd"])
    hamiltonian_max_wasserstein = max(hamiltonian_rows, key=lambda row: row["wasserstein"])
    target_norms = np.linalg.norm(target_states, axis=1)
    ket00 = np.array([1, 0, 0, 0], dtype=complex)
    mean_fidelity_to_00 = float(np.mean(np.abs(target_states @ ket00.conj()) ** 2))
    artifact_dir = display_path(args.output_dir)

    random_resource_final = random_unitary_resource_proxy(args.random_steps)
    hamiltonian_resource_final = hamiltonian_resource_proxy(args.hamiltonian_t_max, args.measurement_basis)
    settings_rows = [
        {"item": "ensemble size N", "value": args.n_samples, "decision": "Within requested 50-100 sample range."},
        {"item": "target sigma", "value": args.sigma, "decision": "Uses requested sigma = 0.10."},
        {"item": "random angles", "value": f"uniform [-{args.random_angle_scale:.6f}, {args.random_angle_scale:.6f}]", "decision": "Free choice in Problem 1(c), stated explicitly."},
        {"item": "random entangler", "value": "CZ", "decision": "One two-qubit entangler per diffusion step."},
        {"item": "Hamiltonian constants", "value": "hx=0.8090, hy=0.9045, J=1.0", "decision": "Matches Problem 2(a)."},
        {"item": "projection basis", "value": args.measurement_basis.upper(), "decision": "Computational basis by default; outcome sampled per ensemble member."},
    ]
    coverage_rows = [
        {
            "part": "1(a)",
            "requirement": "Construct two-qubit target ensemble clustered around |00>.",
            "implementation": "Qiskit Ry then Rz on each qubit; statevector converted to q0-left array order.",
            "evidence": f"N={args.n_samples}, sigma={args.sigma:.2f}, mean F(|psi>,|00>)={mean_fidelity_to_00:.6f}.",
        },
        {
            "part": "1(b)",
            "requirement": "Compute fidelity-based MMD and infidelity-cost Wasserstein-type distance.",
            "implementation": "Pairwise pure-state fidelity matrix; biased MMD; equal-size optimal matching cost.",
            "evidence": "Both metrics are used for every random-unitary and Hamiltonian row.",
        },
        {
            "part": "1(c)",
            "requirement": "Generate random-unitary forward diffusion and plot distance to S0 versus k.",
            "implementation": "Each step uses random RX, RY, RZ on both qubits and one CZ entangler.",
            "evidence": f"Final k={args.random_steps}: MMD={random_final['mmd']:.6f}, Wasserstein={random_final['wasserstein']:.6f}.",
        },
        {
            "part": "2(a)",
            "requirement": "Attach one complement qubit and evolve M+F under fixed three-qubit Hamiltonian.",
            "implementation": "SparsePauliOp with six local X/Y terms and two XX nearest-neighbor terms.",
            "evidence": "8 fixed Hamiltonian terms, 3 scalar constants, complement initialized as |0>.",
        },
        {
            "part": "2(b)",
            "requirement": "Generate projected Hamiltonian-diffused ensembles for several times t.",
            "implementation": "For each t, evolve M+F and sample a projected complement-qubit outcome.",
            "evidence": f"{args.hamiltonian_time_points} time points over [0, {args.hamiltonian_t_max:.1f}].",
        },
        {
            "part": "2(c)",
            "requirement": "Plot Hamiltonian distances to S0 versus t and compare qualitative behavior.",
            "implementation": "Same MMD and Wasserstein distances as Problem 1 are computed for every t.",
            "evidence": f"Peak MMD={hamiltonian_max_mmd['mmd']:.6f} at t={hamiltonian_max_mmd['parameter']:.6f}.",
        },
        {
            "part": "2(d)",
            "requirement": "Compare simple resource or control-cost proxies at comparable diffusion strength.",
            "implementation": "Nearest non-initial metric pairs are matched by MMD and Wasserstein.",
            "evidence": "Report includes random rotations/entanglers/controls and Hamiltonian fixed terms/time.",
        },
    ]

    text = f"""# Problem 1/2 Requirement Report

This report is generated by `python scripts/problem_1_2_generate_requirement_report.py`.
It maps the 2026 QML challenge requirements for Problems 1 and 2 to the current implementation and records one deterministic execution.

## Run Configuration

{markdown_table(settings_rows, [("Item", "item"), ("Value", "value"), ("Decision", "decision")])}

Additional fixed settings:

- Seed: `{args.seed}`
- Random-unitary steps: `{args.random_steps}`
- Hamiltonian time grid: `linspace(0, {args.hamiltonian_t_max}, {args.hamiltonian_time_points})`
- Data system: two qubits `M0, M1`
- Complement system: one qubit `F = |0>`
- Output directory for generated CSV/PNG/JSON artifacts: `{artifact_dir}`

## Requirement Coverage

{markdown_table(coverage_rows, [("Part", "part"), ("Requirement", "requirement"), ("Implementation", "implementation"), ("Evidence", "evidence")])}

## Problem 1(a): Target Ensemble Check

- Shape of `S0`: `{target_states.shape}`
- Norm range: `{float(target_norms.min()):.6f}` to `{float(target_norms.max()):.6f}`
- Mean fidelity to `|00>`: `{mean_fidelity_to_00:.6f}`
- Interpretation: the target ensemble remains a tight two-qubit cluster around `|00>` under the requested Gaussian angle scale.

## Problem 1(b): Metric Definitions

- Pure-state fidelity: `F(psi, phi) = |<psi|phi>|^2`
- MMD kernel: fidelity, reported as `sqrt(MMD^2)`
- Wasserstein-type cost: `1 - F(psi, phi)`
- Equal-size ensembles use the minimum average matching cost.

## Problem 1(c): Random-Unitary Diffusion Result

Implementation choices left open by the problem statement are fixed as follows:

- Per step and per ensemble member: Qiskit `RX`, `RY`, `RZ` on each qubit
- Entangler: one `CZ`
- Angle distribution: uniform in `[-pi, pi]`
- Number of steps: `{args.random_steps}`

{qualitative_behavior(random_rows, "step")}

{markdown_table(random_rows, [("k", "parameter"), ("MMD", "mmd"), ("Wasserstein", "wasserstein")])}

Cluster interpretation: the distance is zero at `k = 0` because the reference and candidate ensembles are both `S0`. After the first random layer, both metrics jump sharply, showing that the tight `|00>`-centered cluster is quickly scrambled. Later steps fluctuate around a high-distance regime rather than returning to the original cluster.

## Problem 2(a-b): Hamiltonian Projected Diffusion Setup

The Hamiltonian is implemented with the problem constants `hx = 0.8090`, `hy = 0.9045`, `J = 1.0`:

```text
H = sum_j (hx X_j + hy Y_j) + J sum_j X_j X_{{j+1}}
```

The implemented fixed-control structure has 8 Pauli terms:

- local fields: `XII`, `YII`, `IXI`, `IYI`, `IIX`, `IIY`
- nearest-neighbor couplings: `XXI`, `IXX`

For each time point, the complement qubit is projected in the `{args.measurement_basis.upper()}` basis and one outcome is sampled per ensemble member, preserving ensemble size.

## Problem 2(c): Hamiltonian Distance Result

{qualitative_behavior(hamiltonian_rows, "time")}

{markdown_table(hamiltonian_rows, [("t", "parameter"), ("MMD", "mmd"), ("Wasserstein", "wasserstein")])}

Qualitative comparison:

- Random-unitary diffusion is layer-indexed and controlled by many independent gate angles.
- Hamiltonian projected diffusion is time-indexed and controlled by one fixed Hamiltonian plus projection.
- In this run, both mechanisms move the ensemble away from `S0`, while the Hamiltonian curve shows stronger time-dependent fluctuation and saturation behavior.

## Problem 2(d): Resource / Control Proxy

Final random-unitary proxy at step `{args.random_steps}`:

- Single-qubit random rotations: `{random_resource_final['single_qubit_rotations']}`
- Two-qubit entanglers: `{random_resource_final['two_qubit_entanglers']}`
- Random control parameters: `{random_resource_final['random_controls']}`

Hamiltonian proxy at `t = {args.hamiltonian_t_max:.6f}`:

- Total Hamiltonian evolution time: `{hamiltonian_resource_final['total_hamiltonian_time']:.6f}`
- Fixed Hamiltonian terms: `{hamiltonian_resource_final['fixed_hamiltonian_terms']}`
- Fixed Hamiltonian parameters: `{hamiltonian_resource_final['fixed_hamiltonian_parameters']}`
- Measurement basis: `{hamiltonian_resource_final['measurement_basis']}`

Comparable-strength matches:

{markdown_table(comparable_rows, [("Matched by", "matched_by"), ("Random k", "random_step"), ("Ham t", "hamiltonian_time"), ("Random MMD", "random_mmd"), ("Ham MMD", "hamiltonian_mmd"), ("MMD gap", "mmd_gap"), ("Random W", "random_wasserstein"), ("Ham W", "hamiltonian_wasserstein"), ("W gap", "wasserstein_gap"), ("Random rotations", "random_single_qubit_rotations"), ("Random entanglers", "random_two_qubit_entanglers"), ("Random controls", "random_controls"), ("Ham fixed terms", "hamiltonian_fixed_terms"), ("Ham params", "hamiltonian_fixed_parameters")])}

## Generated Artifacts

The script writes detailed machine-readable artifacts under `{artifact_dir}`:

- `random_unitary_metrics.csv`
- `hamiltonian_metrics.csv`
- `comparable_strength_resource_matches.csv`
- `problem_1_2_requirement_settings.json`
- `distance_curves.png`

These files are intentionally under `results/` and are not committed by default. The committed artifact is this markdown report, which contains the key execution results needed for review.
"""
    return text


def run(args: argparse.Namespace) -> None:
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    args.report_path.parent.mkdir(parents=True, exist_ok=True)

    target_states = target_ensemble(args.n_samples, sigma=args.sigma, seed=args.seed)
    random_trajectory = random_unitary_trajectory(
        target_states,
        n_steps=args.random_steps,
        angle_scale=args.random_angle_scale,
        seed=args.seed + 1,
    )
    random_rows = distance_curve(target_states, random_trajectory, parameter_name="step")

    times = np.linspace(0.0, args.hamiltonian_t_max, args.hamiltonian_time_points)
    hamiltonian_trajectory = hamiltonian_projected_trajectory(
        target_states,
        times=times,
        measurement_basis=args.measurement_basis,
        seed=args.seed + 2,
    )
    hamiltonian_rows = distance_curve(target_states, hamiltonian_trajectory, parameters=times, parameter_name="time")
    comparable_rows = comparable_strength_resource_rows(random_rows, hamiltonian_rows, args.measurement_basis)

    write_rows(output_dir / "random_unitary_metrics.csv", random_rows)
    write_rows(output_dir / "hamiltonian_metrics.csv", hamiltonian_rows)
    write_rows(output_dir / "comparable_strength_resource_matches.csv", comparable_rows)
    plot_curves(random_rows, hamiltonian_rows, output_dir / "distance_curves.png")
    write_json(
        output_dir / "problem_1_2_requirement_settings.json",
        {
            "n_samples": args.n_samples,
            "sigma": args.sigma,
            "seed": args.seed,
            "random_steps": args.random_steps,
            "random_angle_scale": args.random_angle_scale,
            "random_entangler": "cz",
            "hamiltonian_t_max": args.hamiltonian_t_max,
            "hamiltonian_time_points": args.hamiltonian_time_points,
            "measurement_basis": args.measurement_basis,
        },
    )
    args.report_path.write_text(
        build_report(args, target_states, random_rows, hamiltonian_rows, comparable_rows),
        encoding="utf-8",
    )
    print(f"Wrote requirement report to {args.report_path}")
    print(f"Wrote generated artifacts to {output_dir}")


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()

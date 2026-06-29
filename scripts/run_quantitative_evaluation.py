from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run quantitative evaluation diagnostics for the hackathon.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "quantitative_evaluation")
    parser.add_argument("--skip-baseline", action="store_true")
    return parser.parse_args()


def run_command(command: list[str]) -> None:
    print(f"\n$ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if not args.skip_baseline:
        run_command(
            [
                sys.executable,
                "scripts/run_problem_1_2_baselines.py",
                "--output-dir",
                str(args.output_dir / "problem_1_2_baseline"),
            ]
        )

    diagnostics = [
        ["scripts/problem_1b_check_metrics.py", "--output-dir", str(args.output_dir)],
        ["scripts/problem_2a_print_hamiltonian.py", "--output-dir", str(args.output_dir)],
        ["scripts/problem_2b_projection_diagnostics.py", "--output-dir", str(args.output_dir)],
        ["scripts/problem_2c_plot_bloch_comparison.py", "--output-dir", str(args.output_dir)],
    ]
    for script in diagnostics:
        run_command([sys.executable, *script])

    summary_paths = [
        args.output_dir / "problem_1b_metric_diagnostics.md",
        args.output_dir / "problem_2a_hamiltonian_diagnostics.md",
        args.output_dir / "problem_2b_projection_diagnostics.md",
        args.output_dir / "problem_2c_bloch_summary.md",
        args.output_dir / "problem_1_2_baseline" / "problem_1_2_summary.md",
        ROOT / "results" / "problem_3_seed_sweep" / "seed_sweep_summary.md",
    ]

    lines = [
        "# Quantitative Evaluation Index",
        "",
        "This generated index points to diagnostics that support judge-facing quantitative evaluation.",
        "",
        "## Generated/Referenced Summaries",
        "",
    ]
    for path in summary_paths:
        if path.exists():
            lines.append(f"- `{path.relative_to(ROOT)}`")
    lines.extend(
        [
            "",
            "## Recommended Judge-Facing Quantitative Evidence",
            "",
            "- Problem 1(b): metric self-check and one-step scrambling response.",
            "- Problem 2(a): explicit Hamiltonian terms and Hermiticity check.",
            "- Problem 2(b): projection probability normalization and outcome statistics.",
            "- Problem 2(c): reduced Bloch-vector clouds for qualitative diffusion comparison.",
            "- Problem 2(d): comparable-strength resource/control proxy table.",
            "- Problem 3: 20-seed continuous-basis denoising sweep.",
            "",
        ]
    )
    index_path = args.output_dir / "QUANTITATIVE_EVALUATION_INDEX.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {index_path}")


if __name__ == "__main__":
    main()

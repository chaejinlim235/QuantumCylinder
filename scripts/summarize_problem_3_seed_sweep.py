"""Summarize Problem 3 seed sweep outputs."""

from __future__ import annotations

import argparse
import csv
import statistics as stats
from collections.abc import Iterable
from pathlib import Path


FLOAT_COLUMNS = [
    "continuous_mmd_improvement",
    "continuous_wasserstein_improvement",
    "continuous_diversity_retention",
    "continuous_mean_success_probability",
    "continuous_score_minus_axis_score",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("results/problem_3_seed_sweep"),
        help="Directory containing seed_<n> result folders.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Summary markdown path. Defaults to <input-dir>/seed_sweep_summary.md.",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="*",
        default=None,
        help="Optional expected seed list. When set, stale seed_<n> directories outside this list are ignored.",
    )
    return parser.parse_args()


def infer_overall_decision(summary_text: str) -> str:
    for decision in ["use_as_main", "fallback_only", "do_not_use_as_main"]:
        if f"Overall decision: `{decision}`" in summary_text:
            return decision
    return "unknown"


def median_or_none(rows: list[dict[str, object]], key: str) -> float | None:
    if not rows:
        return None
    return stats.median(float(row[key]) for row in rows)


def format_metric(value: float | None) -> str:
    return f"`{value:.6f}`" if value is not None else "`n/a`"


def load_seed_results(
    root: Path,
    expected_seeds: Iterable[int] | None = None,
) -> tuple[list[tuple[int, str]], list[dict[str, object]]]:
    if expected_seeds is None:
        seed_dirs = []
        for path in root.glob("seed_*"):
            if not path.is_dir():
                continue
            try:
                int(path.name.split("_")[-1])
            except ValueError:
                continue
            seed_dirs.append(path)
        seed_dirs = sorted(seed_dirs, key=lambda path: int(path.name.split("_")[-1]))
    else:
        seed_dirs = [root / f"seed_{seed}" for seed in sorted(set(expected_seeds))]
    mark_missing_unknown = expected_seeds is not None
    run_decisions: list[tuple[int, str]] = []
    rows: list[dict[str, object]] = []

    for seed_dir in seed_dirs:
        seed = int(seed_dir.name.split("_")[-1])
        problem_summary = seed_dir / "problem_3_summary.md"
        best_path = seed_dir / "best_denoising_metrics.csv"

        if not problem_summary.exists() or not best_path.exists():
            print(f"Missing results for seed {seed}: {seed_dir}")
            if mark_missing_unknown:
                run_decisions.append((seed, "unknown"))
            continue

        summary_text = problem_summary.read_text(encoding="utf-8")
        run_decisions.append((seed, infer_overall_decision(summary_text)))

        with best_path.open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                parsed: dict[str, object] = dict(row)
                parsed["seed"] = seed
                for key in FLOAT_COLUMNS:
                    parsed[key] = float(parsed[key])
                rows.append(parsed)

    return run_decisions, rows


def build_summary(run_decisions: list[tuple[int, str]], rows: list[dict[str, object]]) -> str:
    overall_values = [decision for _, decision in run_decisions]
    main_runs = overall_values.count("use_as_main")
    fallback_runs = overall_values.count("fallback_only")
    reject_runs = overall_values.count("do_not_use_as_main")
    unknown_runs = overall_values.count("unknown")

    main_rows = [row for row in rows if row["decision"] == "main_candidate"]
    fallback_rows = [row for row in rows if row["decision"] == "fallback_candidate"]
    reject_rows = [row for row in rows if row["decision"] == "do_not_use_as_main"]

    use_as_main_fraction = main_runs / len(run_decisions) if run_decisions else 0.0
    main_row_fraction = len(main_rows) / len(rows) if rows else 0.0
    median_score_margin = median_or_none(rows, "continuous_score_minus_axis_score")
    median_diversity = median_or_none(rows, "continuous_diversity_retention")
    median_success = median_or_none(rows, "continuous_mean_success_probability")
    median_mmd_improvement = median_or_none(rows, "continuous_mmd_improvement")
    median_wasserstein_improvement = median_or_none(rows, "continuous_wasserstein_improvement")

    strong_enough = (
        use_as_main_fraction >= 0.70
        and main_row_fraction >= 0.40
        and median_score_margin is not None
        and median_score_margin > 0.0
        and median_diversity is not None
        and median_diversity >= 0.5
        and median_success is not None
        and median_success >= 0.1
        and (
            (median_mmd_improvement is not None and median_mmd_improvement >= 0.02)
            or (
                median_wasserstein_improvement is not None
                and median_wasserstein_improvement >= 0.02
            )
        )
    )

    recommendation = "use_as_main" if strong_enough else "fallback_or_appendix"

    lines = [
        "# Problem 3 Seed Sweep Summary",
        "",
        "## Decision",
        "",
        f"Main-claim recommendation: `{recommendation}`",
        "",
        "## Seed-Level Decisions",
        "",
    ]
    for seed, decision in run_decisions:
        lines.append(f"- seed `{seed}`: `{decision}`")

    lines.extend(
        [
            "",
            "## Counts",
            "",
            f"- Total seeds: `{len(run_decisions)}`",
            f"- use_as_main: `{main_runs}`",
            f"- fallback_only: `{fallback_runs}`",
            f"- do_not_use_as_main: `{reject_runs}`",
            f"- unknown: `{unknown_runs}`",
            f"- use_as_main fraction: `{use_as_main_fraction:.3f}`",
            "",
            "## Row-Level Counts",
            "",
            f"- Total rows: `{len(rows)}`",
            f"- main_candidate rows: `{len(main_rows)}`",
            f"- fallback_candidate rows: `{len(fallback_rows)}`",
            f"- do_not_use_as_main rows: `{len(reject_rows)}`",
            f"- main_candidate row fraction: `{main_row_fraction:.3f}`",
            "",
            "## Medians Across Best Rows",
            "",
            f"- continuous_mmd_improvement: {format_metric(median_mmd_improvement)}",
            f"- continuous_wasserstein_improvement: {format_metric(median_wasserstein_improvement)}",
            f"- continuous_score_minus_axis_score: {format_metric(median_score_margin)}",
            f"- continuous_diversity_retention: {format_metric(median_diversity)}",
            f"- continuous_mean_success_probability: {format_metric(median_success)}",
            "",
            "## Final Claim Guidance",
            "",
        ]
    )

    if strong_enough:
        lines.append(
            "The seed sweep supports using continuous projected denoising as the main Problem 3 result, "
            f"with the caveat that the median axis-only score margin is {format_metric(median_score_margin)}. "
            "State this as a small-scale post-selected proxy improvement, not hardware advantage or general quantum advantage."
        )
    else:
        lines.append(
            "The seed sweep is not strong enough for the main claim. "
            "Keep it as fallback/appendix or weaken the claim."
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    output_path = args.output or args.input_dir / "seed_sweep_summary.md"
    run_decisions, rows = load_seed_results(args.input_dir, expected_seeds=args.seeds)
    summary = build_summary(run_decisions, rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

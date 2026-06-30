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


def min_or_none(rows: list[dict[str, object]], key: str) -> float | None:
    if not rows:
        return None
    return min(float(row[key]) for row in rows)


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
    min_score_margin = min_or_none(rows, "continuous_score_minus_axis_score")
    min_diversity = min_or_none(rows, "continuous_diversity_retention")
    min_success = min_or_none(rows, "continuous_mean_success_probability")
    min_mmd_improvement = min_or_none(rows, "continuous_mmd_improvement")
    min_wasserstein_improvement = min_or_none(rows, "continuous_wasserstein_improvement")
    nonpositive_axis_margin_rows = sum(
        1 for row in rows if float(row["continuous_score_minus_axis_score"]) <= 0.0
    )

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
    if strong_enough:
        report_ready_wording = (
            f"Use in 3-b: Across the {main_runs} / {len(run_decisions)} requested seeds, "
            "continuous measurement-basis post-selection remains a reproducible small-scale "
            "state-vector controlled modification/reference, "
            f"with median MMD improvement {format_metric(median_mmd_improvement)} and "
            f"median Wasserstein improvement {format_metric(median_wasserstein_improvement)}. "
            f"The axis-only score margin is small ({format_metric(median_score_margin)}), "
            "so present it as a recoverability trade-off analysis, not hardware advantage "
            "or general quantum advantage. Use this analysis to motivate the 3-c two-way projected denoising proposal."
        )
    else:
        report_ready_wording = (
            "Use: The current seed sweep is not robust enough for the main Problem 3 claim. "
            "Keep it as a fallback or appendix result unless a later sweep passes the adoption gate."
        )

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
            "## Guardrail Checks",
            "",
            "Worst-case checks across best rows; these expose weak fallback rows and do not replace the median adoption gate.",
            "",
            f"- minimum continuous_mmd_improvement: {format_metric(min_mmd_improvement)}",
            f"- minimum continuous_wasserstein_improvement: {format_metric(min_wasserstein_improvement)}",
            f"- minimum continuous_score_minus_axis_score: {format_metric(min_score_margin)}",
            f"- nonpositive axis-margin rows: `{nonpositive_axis_margin_rows} / {len(rows)}`",
            f"- minimum continuous_diversity_retention: {format_metric(min_diversity)}",
            f"- minimum continuous_mean_success_probability: {format_metric(min_success)}",
            "",
            "## 3-b Analysis",
            "",
            f"- Seed robustness: `{main_runs} / {len(run_decisions)}` seeds pass the main gate, so the effect is not a single-seed accident.",
            f"- Distance recovery: median MMD and Wasserstein improvements are {format_metric(median_mmd_improvement)} and {format_metric(median_wasserstein_improvement)}, so the post-selected map moves the ensemble back toward `S0` under both metrics.",
            f"- Axis comparison: the median continuous-vs-axis score margin is only {format_metric(median_score_margin)}, with `{nonpositive_axis_margin_rows} / {len(rows)}` nonpositive rows. Treat `axis-only` as a discrete baseline, not as a team-proposed method, and do not claim continuous control is overwhelmingly better.",
            f"- Guardrails: median diversity retention is {format_metric(median_diversity)} and median success probability is {format_metric(median_success)}, so the result should be described as a recoverability trade-off rather than a distance-only win.",
            "- 3-c implication: use this trade-off to motivate two-way projected denoising as the main improvement; keep random final kick, hybrid 1M+1F, and actor-critic as appendix/ablation candidates.",
            "",
            "## Report Table",
            "",
            "| Metric | Value | Report use |",
            "| --- | --- | --- |",
            f"| Recommendation | `{recommendation}` | main-claim gate |",
            f"| Passing seeds | `{main_runs} / {len(run_decisions)}` | seed robustness gate |",
            f"| Main-candidate rows | `{len(main_rows)} / {len(rows)} = {main_row_fraction:.3f}` | row-level robustness |",
            f"| Median MMD improvement | {format_metric(median_mmd_improvement)} | distance improvement |",
            f"| Median Wasserstein improvement | {format_metric(median_wasserstein_improvement)} | distance improvement |",
            f"| Median axis-only score margin | {format_metric(median_score_margin)} | limitation, not a broad advantage claim |",
            f"| Median diversity retention | {format_metric(median_diversity)} | collapse guardrail |",
            f"| Median mean success probability | {format_metric(median_success)} | post-selection feasibility |",
            f"| Nonpositive axis-margin rows | `{nonpositive_axis_margin_rows} / {len(rows)}` | axis-comparison caveat |",
            "",
            "## Report-Ready Wording",
            "",
            report_ready_wording,
            "",
            "## Final Claim Guidance",
            "",
        ]
    )

    if strong_enough:
        lines.append(
            "The seed sweep supports using continuous projected denoising as the Problem 3(b) controlled modification/reference, "
            f"with the caveat that the median axis-only score margin is {format_metric(median_score_margin)}. "
            "Do not claim every input step beats the axis-only projection if fallback rows have weak margins. "
            "State this as a small-scale recoverability trade-off that motivates the Problem 3(c) two-way projected denoising proposal, not hardware advantage or general quantum advantage."
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

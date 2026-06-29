from __future__ import annotations

import csv
from pathlib import Path

from scripts.summarize_problem_3_seed_sweep import FLOAT_COLUMNS, build_summary, load_seed_results


def write_seed_result(root: Path, seed: int, decision: str = "use_as_main") -> None:
    seed_dir = root / f"seed_{seed}"
    seed_dir.mkdir(parents=True)
    (seed_dir / "problem_3_summary.md").write_text(
        f"# Summary\n\nOverall decision: `{decision}`\n",
        encoding="utf-8",
    )
    with (seed_dir / "best_denoising_metrics.csv").open("w", newline="", encoding="utf-8") as file:
        fieldnames = ["decision", *FLOAT_COLUMNS]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        row = {"decision": "main_candidate"}
        row.update({column: "0.5" for column in FLOAT_COLUMNS})
        writer.writerow(row)


def test_load_seed_results_filters_to_requested_seeds(tmp_path: Path) -> None:
    write_seed_result(tmp_path, 1)
    write_seed_result(tmp_path, 2)
    write_seed_result(tmp_path, 1920)

    run_decisions, rows = load_seed_results(tmp_path, expected_seeds=[1, 2])

    assert [seed for seed, _ in run_decisions] == [1, 2]
    assert {row["seed"] for row in rows} == {1, 2}


def test_load_seed_results_marks_missing_requested_seed_unknown(tmp_path: Path) -> None:
    write_seed_result(tmp_path, 1)

    run_decisions, rows = load_seed_results(tmp_path, expected_seeds=[1, 2])

    assert run_decisions == [(1, "use_as_main"), (2, "unknown")]
    assert [row["seed"] for row in rows] == [1]


def test_build_summary_mentions_axis_margin_and_advantage_caveat_for_main_claim() -> None:
    rows = [
        {
            "decision": "main_candidate",
            "continuous_mmd_improvement": 0.10,
            "continuous_wasserstein_improvement": 0.15,
            "continuous_diversity_retention": 0.82,
            "continuous_mean_success_probability": 0.46,
            "continuous_score_minus_axis_score": 0.01,
        }
    ]

    summary = build_summary([(1, "use_as_main")], rows)

    assert "axis-only score margin" in summary
    assert "not hardware advantage or general quantum advantage" in summary


def test_build_summary_reports_worst_case_guardrails() -> None:
    rows = [
        {
            "decision": "main_candidate",
            "continuous_mmd_improvement": 0.10,
            "continuous_wasserstein_improvement": 0.15,
            "continuous_diversity_retention": 0.82,
            "continuous_mean_success_probability": 0.46,
            "continuous_score_minus_axis_score": 0.01,
        },
        {
            "decision": "fallback_candidate",
            "continuous_mmd_improvement": 0.03,
            "continuous_wasserstein_improvement": 0.04,
            "continuous_diversity_retention": 0.70,
            "continuous_mean_success_probability": 0.20,
            "continuous_score_minus_axis_score": -0.02,
        },
    ]

    summary = build_summary([(1, "use_as_main"), (2, "use_as_main")], rows)

    assert "## Guardrail Checks" in summary
    assert "minimum continuous_score_minus_axis_score: `-0.020000`" in summary
    assert "nonpositive axis-margin rows: `1 / 2`" in summary
    assert "minimum continuous_diversity_retention: `0.700000`" in summary
    assert "minimum continuous_mean_success_probability: `0.200000`" in summary


def test_build_summary_includes_report_ready_wording_for_robust_main_claim() -> None:
    rows = [
        {
            "decision": "main_candidate",
            "continuous_mmd_improvement": 0.10,
            "continuous_wasserstein_improvement": 0.15,
            "continuous_diversity_retention": 0.82,
            "continuous_mean_success_probability": 0.46,
            "continuous_score_minus_axis_score": 0.01,
        }
        for _ in range(20)
    ]
    run_decisions = [(seed, "use_as_main") for seed in range(1, 21)]

    summary = build_summary(run_decisions, rows)

    assert "## Report-Ready Wording" in summary
    assert "20 / 20 requested seeds" in summary
    assert "median MMD improvement `0.100000`" in summary
    assert "median Wasserstein improvement `0.150000`" in summary
    assert "axis-only score margin is small (`0.010000`)" in summary
    assert "not hardware advantage or general quantum advantage" in summary


def test_build_summary_includes_copyable_report_table_for_robust_main_claim() -> None:
    rows = [
        {
            "decision": "main_candidate" if index < 14 else "fallback_candidate",
            "continuous_mmd_improvement": 0.10,
            "continuous_wasserstein_improvement": 0.15,
            "continuous_diversity_retention": 0.82,
            "continuous_mean_success_probability": 0.46,
            "continuous_score_minus_axis_score": 0.01 if index < 18 else -0.01,
        }
        for index in range(20)
    ]
    run_decisions = [(seed, "use_as_main") for seed in range(1, 21)]

    summary = build_summary(run_decisions, rows)

    assert "## Report Table" in summary
    assert "| Metric | Value | Report use |" in summary
    assert "| Passing seeds | `20 / 20` | seed robustness gate |" in summary
    assert "| Main-candidate rows | `14 / 20 = 0.700` | row-level robustness |" in summary
    assert "| Median MMD improvement | `0.100000` | distance improvement |" in summary
    assert "| Median axis-only score margin | `0.010000` | limitation, not a broad advantage claim |" in summary
    assert "| Nonpositive axis-margin rows | `2 / 20` | axis-comparison caveat |" in summary

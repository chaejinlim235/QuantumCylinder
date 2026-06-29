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

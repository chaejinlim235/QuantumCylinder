from __future__ import annotations

import argparse
import csv
from pathlib import Path

from scripts.summarize_problem_3_method_portfolio import build_portfolio, write_markdown


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_method_portfolio_keeps_multiple_candidates(tmp_path: Path) -> None:
    collapse_summary = tmp_path / "collapse.csv"
    hybrid_best = tmp_path / "hybrid.csv"
    actor_metrics = tmp_path / "actor.csv"

    write_rows(
        collapse_summary,
        [
            {
                "method_key": "identity_no_denoising",
                "method_label": "identity/no-denoising random-unitary input",
                "rows": 2,
                "positive_improvement_rows": "0 / 2",
                "median_mmd": 0.8,
                "median_mmd_improvement": 0.0,
                "median_wasserstein": 0.7,
                "median_wasserstein_improvement": 0.0,
                "median_diversity_retention": 1.0,
                "median_mean_success_probability": 1.0,
            },
            {
                "method_key": "best_axis_projection",
                "method_label": "best exact Z/X/Y axis projection",
                "rows": 2,
                "positive_improvement_rows": "2 / 2",
                "median_mmd": 0.7,
                "median_mmd_improvement": 0.1,
                "median_wasserstein": 0.6,
                "median_wasserstein_improvement": 0.1,
                "median_diversity_retention": 0.8,
                "median_mean_success_probability": 0.4,
            },
            {
                "method_key": "continuous_postselection",
                "method_label": "continuous measurement-basis post-selection",
                "rows": 2,
                "positive_improvement_rows": "2 / 2",
                "median_mmd": 0.68,
                "median_mmd_improvement": 0.12,
                "median_wasserstein": 0.58,
                "median_wasserstein_improvement": 0.12,
                "median_diversity_retention": 0.82,
                "median_mean_success_probability": 0.45,
            },
        ],
    )
    write_rows(
        hybrid_best,
        [
            {
                "candidate_mmd": 0.4,
                "mmd_improvement": 0.2,
                "candidate_wasserstein": 0.3,
                "wasserstein_improvement": 0.2,
                "diversity_retention": 0.6,
                "mean_success_probability": 0.5,
            }
        ],
    )
    write_rows(
        actor_metrics,
        [
            {
                "actor_mmd": 0.3,
                "actor_mmd_improvement": 0.4,
                "actor_wasserstein": 0.2,
                "actor_wasserstein_improvement": 0.3,
                "actor_diversity_retention": 0.85,
                "actor_success_probability": 0.35,
                "actor_beats_continuous_mmd": "True",
                "actor_beats_continuous_wasserstein": "True",
            }
        ],
    )

    args = argparse.Namespace(
        collapse_summary=collapse_summary,
        hybrid_best=hybrid_best,
        actor_metrics=actor_metrics,
    )
    rows = build_portfolio(args)

    keys = {row["method_key"] for row in rows}
    assert "best_axis_projection" in keys
    assert "continuous_postselection" in keys
    assert "hybrid_1m1f_toy" in keys
    assert "target_aware_actor_critic" in keys

    markdown_path = tmp_path / "summary.md"
    write_markdown(markdown_path, rows)
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "not as a single actor-critic-only result" in markdown
    assert "hybrid 1M+1F" in markdown

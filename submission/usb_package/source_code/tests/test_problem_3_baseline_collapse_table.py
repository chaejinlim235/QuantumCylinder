from __future__ import annotations

import numpy as np

from scripts.summarize_problem_3_baseline_collapse_table import (
    build_method_rows,
    build_summary,
    collapse_to_reference_centroid,
    summarize_method_rows,
)
from quantum_cylinder.problem_3_continuous_projected_denoising import ensemble_diversity


def best_row(seed: int = 1, input_step: int = 1) -> dict[str, object]:
    return {
        "seed": seed,
        "input_step": input_step,
        "decision": "main_candidate",
        "baseline_mmd": 0.80,
        "baseline_wasserstein": 0.70,
        "baseline_diversity": 0.60,
        "axis_mmd": 0.72,
        "axis_mmd_improvement": 0.08,
        "axis_wasserstein": 0.58,
        "axis_wasserstein_improvement": 0.12,
        "axis_diversity_retention": 0.82,
        "axis_mean_success_probability": 0.40,
        "continuous_mmd": 0.65,
        "continuous_mmd_improvement": 0.15,
        "continuous_wasserstein": 0.50,
        "continuous_wasserstein_improvement": 0.20,
        "continuous_diversity_retention": 0.78,
        "continuous_mean_success_probability": 0.45,
    }


def test_collapse_to_reference_centroid_has_zero_diversity() -> None:
    reference = np.array(
        [
            [1.0, 0.0],
            [0.99, 0.1],
            [0.98, -0.2],
        ],
        dtype=complex,
    )

    collapsed = collapse_to_reference_centroid(reference)

    assert collapsed.shape == reference.shape
    assert ensemble_diversity(collapsed) < 1e-12


def test_build_method_rows_includes_identity_axis_continuous_and_collapse() -> None:
    collapse_metrics = {
        (1, 1): {
            "mmd": 0.02,
            "mmd_improvement": 0.78,
            "wasserstein": 0.05,
            "wasserstein_improvement": 0.65,
            "diversity_retention": 0.0,
            "mean_success_probability": 1.0,
        }
    }

    rows = build_method_rows([best_row()], collapse_metrics)

    assert [row["method_key"] for row in rows] == [
        "identity_no_denoising",
        "best_axis_projection",
        "continuous_postselection",
        "diagnostic_collapse_centroid",
    ]
    assert rows[0]["mmd_improvement"] == 0.0
    assert rows[2]["diversity_retention"] == 0.78
    assert rows[3]["diversity_retention"] == 0.0


def test_summary_reports_collapse_warning_and_distance_not_enough() -> None:
    collapse_metrics = {
        (1, 1): {
            "mmd": 0.02,
            "mmd_improvement": 0.78,
            "wasserstein": 0.05,
            "wasserstein_improvement": 0.65,
            "diversity_retention": 0.0,
            "mean_success_probability": 1.0,
        }
    }
    rows = build_method_rows([best_row()], collapse_metrics)

    summary = build_summary(rows, seeds=[1])

    assert "identity/no-denoising random-unitary input" in summary
    assert "best exact Z/X/Y axis projection" in summary
    assert "continuous measurement-basis post-selection" in summary
    assert "diagnostic collapse-to-target-centroid filter" in summary
    assert "collapse warning: `supported`" in summary
    assert "distance improvement alone is insufficient" in summary
    assert "Do not use the collapse row as a proposed physical reverse process" in summary


def test_summarize_method_rows_counts_positive_improvement_rows() -> None:
    collapse_metrics = {
        (1, 1): {
            "mmd": 0.02,
            "mmd_improvement": 0.78,
            "wasserstein": 0.05,
            "wasserstein_improvement": 0.65,
            "diversity_retention": 0.0,
            "mean_success_probability": 1.0,
        }
    }
    rows = build_method_rows([best_row()], collapse_metrics)

    summaries = {row["method_key"]: row for row in summarize_method_rows(rows)}

    assert summaries["identity_no_denoising"]["positive_improvement_rows"] == 0
    assert summaries["best_axis_projection"]["positive_improvement_rows"] == 1
    assert summaries["continuous_postselection"]["positive_improvement_rows"] == 1
    assert summaries["diagnostic_collapse_centroid"]["median_diversity_retention"] == 0.0

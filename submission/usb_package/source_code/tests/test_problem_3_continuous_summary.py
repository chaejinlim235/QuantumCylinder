from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from scripts.run_problem_3_continuous_denoising import write_summary


def default_args() -> Namespace:
    return Namespace(
        n_samples=80,
        sigma=0.1,
        seed=7,
        input_steps=[1, 2],
        theta_points=13,
        phi_points=16,
        tau_min=0.05,
        tau_max=2.0,
        tau_points=20,
    )


def best_row(input_step: int, decision: str, score: float, axis_margin: float) -> dict:
    return {
        "input_step": input_step,
        "decision": decision,
        "baseline_mmd": 0.90,
        "continuous_mmd": 0.80,
        "baseline_wasserstein": 0.70,
        "continuous_wasserstein": 0.55,
        "continuous_tau": 0.50,
        "continuous_theta": 1.00,
        "continuous_phi": 1.50,
        "continuous_diversity_retention": 0.82,
        "continuous_mean_success_probability": 0.40,
        "continuous_score": score,
        "continuous_score_minus_axis_score": axis_margin,
    }


def test_problem_3_summary_reports_axis_margin_guardrail(tmp_path: Path) -> None:
    summary_path = tmp_path / "problem_3_summary.md"
    rows = [
        best_row(input_step=1, decision="main_candidate", score=0.20, axis_margin=0.04),
        best_row(input_step=2, decision="fallback_candidate", score=0.10, axis_margin=-0.02),
    ]

    write_summary(summary_path, default_args(), rows)

    summary = summary_path.read_text(encoding="utf-8")
    assert "## Axis Baseline Comparison" in summary
    assert "median continuous_score_minus_axis_score: `0.010000`" in summary
    assert "minimum continuous_score_minus_axis_score: `-0.020000`" in summary
    assert "nonpositive axis-margin rows: `1 / 2`" in summary
    assert "Do not claim every input step beats the axis-only projection" in summary

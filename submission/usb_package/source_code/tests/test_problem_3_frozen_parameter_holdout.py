from __future__ import annotations

from scripts.summarize_problem_3_frozen_holdout import (
    build_summary,
    filter_rows_for_parameter,
    select_frozen_parameter,
)


def candidate_row(
    tau: float,
    theta: float,
    phi: float,
    score: float,
    mmd: float,
    wasserstein: float,
    diversity: float = 0.80,
    success: float = 0.45,
    seed: int = 1,
    input_step: int = 1,
) -> dict[str, object]:
    return {
        "seed": seed,
        "input_step": input_step,
        "basis_family": "continuous",
        "tau": tau,
        "theta": theta,
        "phi": phi,
        "score": score,
        "mmd_improvement": mmd,
        "wasserstein_improvement": wasserstein,
        "diversity_retention": diversity,
        "mean_success_probability": success,
    }


def test_select_frozen_parameter_uses_train_median_score_with_guardrails() -> None:
    rows = [
        candidate_row(0.5, 1.0, 1.5, score=0.20, mmd=0.10, wasserstein=0.20, seed=1),
        candidate_row(0.5, 1.0, 1.5, score=0.22, mmd=0.11, wasserstein=0.22, seed=2),
        candidate_row(0.7, 1.2, 1.8, score=0.40, mmd=0.20, wasserstein=0.30, diversity=0.20, seed=1),
        candidate_row(0.7, 1.2, 1.8, score=0.42, mmd=0.21, wasserstein=0.31, diversity=0.20, seed=2),
    ]

    selected = select_frozen_parameter(rows, min_mean_success=0.10, min_diversity_retention=0.50)

    assert selected["tau"] == 0.5
    assert selected["theta"] == 1.0
    assert selected["phi"] == 1.5
    assert selected["train_total_rows"] == 2
    assert selected["train_positive_rows"] == 2


def test_filter_rows_for_parameter_matches_float_values_with_rounding() -> None:
    frozen = {"tau": 0.5, "theta": 1.0, "phi": 1.5}
    rows = [
        candidate_row(0.5000000000001, 1.0, 1.5, score=0.1, mmd=0.1, wasserstein=0.1),
        candidate_row(0.7, 1.0, 1.5, score=0.2, mmd=0.2, wasserstein=0.2),
    ]

    matched = filter_rows_for_parameter(rows, frozen)

    assert len(matched) == 1
    assert matched[0]["tau"] == 0.5000000000001


def test_build_summary_states_no_holdout_tuning_and_oracle_comparison() -> None:
    frozen = {
        "tau": 0.5,
        "theta": 1.0,
        "phi": 1.5,
        "train_total_rows": 4,
        "train_positive_rows": 4,
        "train_median_mmd_improvement": 0.10,
        "train_median_wasserstein_improvement": 0.20,
        "train_median_diversity_retention": 0.80,
        "train_median_mean_success_probability": 0.45,
        "train_median_score": 0.18,
    }
    holdout_rows = [
        candidate_row(0.5, 1.0, 1.5, score=0.12, mmd=0.08, wasserstein=0.15, seed=11),
        candidate_row(0.5, 1.0, 1.5, score=0.14, mmd=0.09, wasserstein=0.16, seed=12),
    ]
    oracle_rows = [
        {
            "continuous_mmd_improvement": 0.10,
            "continuous_wasserstein_improvement": 0.20,
            "continuous_diversity_retention": 0.82,
            "continuous_mean_success_probability": 0.46,
        },
        {
            "continuous_mmd_improvement": 0.11,
            "continuous_wasserstein_improvement": 0.21,
            "continuous_diversity_retention": 0.84,
            "continuous_mean_success_probability": 0.47,
        },
    ]

    summary = build_summary(
        frozen=frozen,
        train_seeds=[1, 2],
        holdout_seeds=[11, 12],
        holdout_rows=holdout_rows,
        oracle_rows=oracle_rows,
    )

    assert "No holdout seed is used to choose tau/theta/phi" in summary
    assert "positive-improvement holdout rows: `2 / 2`" in summary
    assert "median fixed-parameter MMD improvement: `0.085000`" in summary
    assert "median oracle-grid MMD improvement: `0.105000`" in summary
    assert "honest holdout check, not a replacement for the 20-seed oracle grid gate" in summary

from __future__ import annotations

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1c_random_unitary_diffusion import random_unitary_trajectory
from quantum_cylinder.problem_3_actor_critic_denoising import (
    ActorCriticConfig,
    target_aware_filter,
    train_actor_critic_denoiser,
)
from quantum_cylinder.problem_3_continuous_projected_denoising import normalize_rows


def test_target_aware_filter_normalizes_rows_and_reports_probabilities():
    target = target_ensemble(n_samples=8, sigma=0.10, seed=11)
    noisy = random_unitary_trajectory(target, n_steps=1, seed=12)[1]

    filtered, probabilities = target_aware_filter(noisy, lambda_value=0.5)
    normalized = normalize_rows(filtered)

    assert filtered.shape == noisy.shape
    assert probabilities.shape == (8,)
    assert (probabilities > 0.0).all()
    assert abs((normalized.conj() * normalized).sum(axis=1).real.mean() - 1.0) < 1e-12


def test_actor_critic_denoiser_improves_raw_target_metrics_on_multiple_seeds():
    config = ActorCriticConfig(episodes=180)
    rows = []

    for seed in (3, 5, 7):
        target = target_ensemble(n_samples=12, sigma=0.10, seed=seed)
        noisy = random_unitary_trajectory(target, n_steps=1, seed=seed + 100)[1]
        rows.append(train_actor_critic_denoiser(target, noisy, seed=seed, config=config))

    assert all(row["mmd_improvement"] > 0.0 for row in rows)
    assert all(row["wasserstein_improvement"] > 0.0 for row in rows)
    assert all(row["mean_success_probability"] >= config.min_success_probability for row in rows)
    assert all(row["diversity_retention"] >= config.min_diversity_retention for row in rows)

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from quantum_cylinder.problem_1b_ensemble_metrics import fidelity_matrix, mmd_fidelity, wasserstein_infidelity
from quantum_cylinder.problem_3_continuous_projected_denoising import ensemble_diversity, normalize_rows

Array = np.ndarray


@dataclass(frozen=True)
class ActorCriticConfig:
    """Small actor-critic policy search over target-aware non-unitary filters."""

    action_lambdas: tuple[float, ...] = field(default_factory=lambda: tuple(np.linspace(0.18, 0.80, 32)))
    episodes: int = 500
    actor_lr: float = 0.16
    critic_lr: float = 0.08
    temperature: float = 0.85
    min_success_probability: float = 0.10
    min_diversity_retention: float = 0.80
    collapse_penalty: float = 2.50
    success_penalty: float = 1.00


def target_aware_filter(input_ensemble: Array, lambda_value: float) -> tuple[Array, Array]:
    """Apply K_lambda = diag(1, lambda, lambda, lambda) and return states and probabilities."""
    if not 0.0 <= lambda_value <= 1.0:
        raise ValueError("lambda_value must be between 0 and 1.")

    states = normalize_rows(input_ensemble)
    diagonal = np.array([1.0, lambda_value, lambda_value, lambda_value], dtype=complex)
    raw = states * diagonal[None, :]
    probabilities = np.sum(np.abs(raw) ** 2, axis=1).real
    if np.any(probabilities <= 0.0):
        raise ValueError("The target-aware filter produced a zero-probability state.")
    return normalize_rows(raw), probabilities


def matched_raw_fidelity(reference: Array, candidate: Array) -> float:
    """Optimal-matching fidelity score induced by the Wasserstein infidelity cost."""
    return 1.0 - wasserstein_infidelity(reference, candidate)


def _feature_vector(reference: Array, input_ensemble: Array) -> Array:
    reference = normalize_rows(reference)
    input_ensemble = normalize_rows(input_ensemble)
    population_00 = float(np.mean(np.abs(input_ensemble[:, 0]) ** 2))
    return np.array(
        [
            1.0,
            mmd_fidelity(reference, input_ensemble),
            wasserstein_infidelity(reference, input_ensemble),
            ensemble_diversity(input_ensemble),
            population_00,
        ],
        dtype=float,
    )


def _softmax(logits: Array) -> Array:
    shifted = logits - float(np.max(logits))
    values = np.exp(shifted)
    return values / float(np.sum(values))


def evaluate_actor_critic_action(
    reference: Array,
    input_ensemble: Array,
    lambda_value: float,
) -> dict:
    """Evaluate one target-aware filter action against the raw target ensemble."""
    reference = normalize_rows(reference)
    input_ensemble = normalize_rows(input_ensemble)
    candidate, probabilities = target_aware_filter(input_ensemble, lambda_value)

    baseline_mmd = mmd_fidelity(reference, input_ensemble)
    baseline_wasserstein = wasserstein_infidelity(reference, input_ensemble)
    baseline_diversity = ensemble_diversity(input_ensemble)
    candidate_mmd = mmd_fidelity(reference, candidate)
    candidate_wasserstein = wasserstein_infidelity(reference, candidate)
    candidate_diversity = ensemble_diversity(candidate)

    return {
        "lambda": float(lambda_value),
        "baseline_mmd": float(baseline_mmd),
        "candidate_mmd": float(candidate_mmd),
        "mmd_improvement": float(baseline_mmd - candidate_mmd),
        "baseline_wasserstein": float(baseline_wasserstein),
        "candidate_wasserstein": float(candidate_wasserstein),
        "wasserstein_improvement": float(baseline_wasserstein - candidate_wasserstein),
        "baseline_raw_fidelity": float(1.0 - baseline_wasserstein),
        "candidate_raw_fidelity": float(1.0 - candidate_wasserstein),
        "raw_fidelity_improvement": float(baseline_wasserstein - candidate_wasserstein),
        "baseline_diversity": float(baseline_diversity),
        "candidate_diversity": float(candidate_diversity),
        "diversity_retention": float(candidate_diversity / max(baseline_diversity, 1e-12)),
        "mean_success_probability": float(np.mean(probabilities)),
        "min_success_probability": float(np.min(probabilities)),
    }


def actor_critic_reward(row: dict, config: ActorCriticConfig) -> float:
    """Reward high raw-data fidelity while penalizing collapse and rare post-selection."""
    metric_gain = row["mmd_improvement"] + row["wasserstein_improvement"] + row["raw_fidelity_improvement"]
    diversity_shortfall = max(0.0, config.min_diversity_retention - row["diversity_retention"])
    success_shortfall = max(0.0, config.min_success_probability - row["mean_success_probability"])
    return float(
        metric_gain
        - config.collapse_penalty * diversity_shortfall
        - config.success_penalty * success_shortfall
    )


def train_actor_critic_denoiser(
    reference: Array,
    input_ensemble: Array,
    seed: int = 0,
    config: ActorCriticConfig | None = None,
) -> dict:
    """Train a one-state actor-critic policy and return the best observed denoising action."""
    config = ActorCriticConfig() if config is None else config
    if config.episodes <= 0:
        raise ValueError("episodes must be positive.")
    if not config.action_lambdas:
        raise ValueError("At least one action lambda is required.")

    rng = np.random.default_rng(seed)
    features = _feature_vector(reference, input_ensemble)
    actor_weights = rng.normal(0.0, 0.01, size=(len(config.action_lambdas), len(features)))
    critic_weights = np.zeros(len(features), dtype=float)

    best_row: dict | None = None
    best_eligible_row: dict | None = None
    best_reward = -np.inf
    best_eligible_reward = -np.inf
    history = []

    for episode in range(config.episodes):
        logits = (actor_weights @ features) / max(config.temperature, 1e-12)
        policy = _softmax(logits)
        action_index = int(rng.choice(len(config.action_lambdas), p=policy))
        lambda_value = float(config.action_lambdas[action_index])
        row = evaluate_actor_critic_action(reference, input_ensemble, lambda_value)
        reward = actor_critic_reward(row, config)

        value = float(critic_weights @ features)
        advantage = reward - value
        critic_weights += config.critic_lr * advantage * features

        policy_gradient = -policy[:, None] * features[None, :]
        policy_gradient[action_index] += features
        actor_weights += config.actor_lr * advantage * policy_gradient

        if reward > best_reward:
            best_reward = reward
            best_row = row | {
                "episode": episode,
                "action_index": action_index,
                "reward": reward,
                "selection": "best_observed_actor_critic_action",
            }
        eligible = (
            row["mean_success_probability"] >= config.min_success_probability
            and row["diversity_retention"] >= config.min_diversity_retention
        )
        if eligible and reward > best_eligible_reward:
            best_eligible_reward = reward
            best_eligible_row = row | {
                "episode": episode,
                "action_index": action_index,
                "reward": reward,
                "selection": "best_guardrailed_actor_critic_action",
            }

        if episode == config.episodes - 1 or episode % max(1, config.episodes // 5) == 0:
            history.append(
                {
                    "episode": episode,
                    "lambda": lambda_value,
                    "reward": float(reward),
                    "critic_value": value,
                    "policy_entropy": float(-np.sum(policy * np.log(np.maximum(policy, 1e-15)))),
                }
            )

    final_policy = _softmax((actor_weights @ features) / max(config.temperature, 1e-12))
    policy_action_index = int(np.argmax(final_policy))
    policy_lambda = float(config.action_lambdas[policy_action_index])
    policy_row = evaluate_actor_critic_action(reference, input_ensemble, policy_lambda)
    policy_reward = actor_critic_reward(policy_row, config)

    if best_row is None:
        raise RuntimeError("Actor-critic training did not evaluate any action.")

    policy_selection = policy_row | {
        "episode": config.episodes,
        "action_index": policy_action_index,
        "reward": policy_reward,
        "selection": "final_policy_action",
    }
    policy_eligible = (
        policy_selection["mean_success_probability"] >= config.min_success_probability
        and policy_selection["diversity_retention"] >= config.min_diversity_retention
    )

    selected = best_eligible_row or best_row
    if policy_eligible and policy_reward >= (best_eligible_reward if best_eligible_row else -np.inf):
        selected = policy_selection
    elif best_eligible_row is None and policy_reward >= best_reward:
        selected = policy_selection
    selected["policy_lambda"] = policy_lambda
    selected["policy_action_probability"] = float(final_policy[policy_action_index])
    selected["best_action_probability"] = float(final_policy[int(selected["action_index"])])
    selected["episodes"] = int(config.episodes)
    selected["history"] = history
    return selected

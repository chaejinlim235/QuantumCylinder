# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `9`
- Input ensemble: random-unitary diffusion at steps `[1, 2, 3, 5, 7, 12]`
- Denoising map: attach one complement qubit, evolve with the fixed Problem 2 Hamiltonian, then post-select on a continuous complement basis
- Continuous basis grid: theta points `13`, phi points `16`, excluding exact `Z/X/Y` axes
- Time grid: `linspace(0.05, 2.0, 20)`
- Axis baseline: best among `Z`, `X`, `Y` projection outcomes over the same time grid

## Adoption Decision

Overall decision: `use_as_main`

The result is a main candidate only when it improves at least one baseline metric, scores sufficiently above the best axis-only projection, keeps diversity, and has a reasonable mean post-selection probability.

## Best Overall Continuous Candidate

- Input step: `2`
- tau: `0.665789`
- theta: `1.047198`
- phi: `1.178097`
- MMD: `0.872855 -> 0.762086`
- Wasserstein: `0.726063 -> 0.580624`
- Diversity retention: `0.861920`
- Mean success probability: `0.484074`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.857252 -> 0.803602`, Wasserstein `0.712947 -> 0.626894`, diversity retention `0.890`, mean success `0.574`
- step `2`: decision `main_candidate`, MMD `0.872855 -> 0.762086`, Wasserstein `0.726063 -> 0.580624`, diversity retention `0.862`, mean success `0.484`
- step `3`: decision `main_candidate`, MMD `0.831538 -> 0.789154`, Wasserstein `0.692833 -> 0.590375`, diversity retention `0.828`, mean success `0.468`
- step `5`: decision `main_candidate`, MMD `0.850662 -> 0.815116`, Wasserstein `0.701471 -> 0.615735`, diversity retention `0.849`, mean success `0.525`
- step `7`: decision `main_candidate`, MMD `0.859643 -> 0.799816`, Wasserstein `0.716374 -> 0.605226`, diversity retention `0.839`, mean success `0.387`
- step `12`: decision `main_candidate`, MMD `0.837119 -> 0.778119`, Wasserstein `0.696583 -> 0.554201`, diversity retention `0.745`, mean success `0.352`

## Counts

- Main candidates: `6`
- Fallback candidates: `0`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.014553`
- minimum continuous_score_minus_axis_score: `0.006189`
- nonpositive axis-margin rows: `0 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `17`
- Input ensemble: random-unitary diffusion at steps `[1, 2, 3, 5, 7, 12]`
- Denoising map: attach one complement qubit, evolve with the fixed Problem 2 Hamiltonian, then post-select on a continuous complement basis
- Continuous basis grid: theta points `13`, phi points `16`, excluding exact `Z/X/Y` axes
- Time grid: `linspace(0.05, 2.0, 20)`
- Axis baseline: best among `Z`, `X`, `Y` projection outcomes over the same time grid

## Adoption Decision

Overall decision: `use_as_main`

The result is a main candidate only when it improves at least one baseline metric, scores sufficiently above the best axis-only projection, keeps diversity, and has a reasonable mean post-selection probability.

## Best Overall Continuous Candidate

- Input step: `7`
- tau: `1.794737`
- theta: `1.832596`
- phi: `3.141593`
- MMD: `0.864455 -> 0.759541`
- Wasserstein: `0.721618 -> 0.557919`
- Diversity retention: `0.793479`
- Mean success probability: `0.471000`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.842415 -> 0.791075`, Wasserstein `0.695582 -> 0.574201`, diversity retention `0.777`, mean success `0.443`
- step `2`: decision `fallback_candidate`, MMD `0.863085 -> 0.787644`, Wasserstein `0.716513 -> 0.600943`, diversity retention `0.855`, mean success `0.471`
- step `3`: decision `main_candidate`, MMD `0.853571 -> 0.779266`, Wasserstein `0.709838 -> 0.569638`, diversity retention `0.783`, mean success `0.462`
- step `5`: decision `main_candidate`, MMD `0.822545 -> 0.779538`, Wasserstein `0.681526 -> 0.581432`, diversity retention `0.826`, mean success `0.477`
- step `7`: decision `main_candidate`, MMD `0.864455 -> 0.759541`, Wasserstein `0.721618 -> 0.557919`, diversity retention `0.793`, mean success `0.471`
- step `12`: decision `main_candidate`, MMD `0.873405 -> 0.775341`, Wasserstein `0.727253 -> 0.591993`, diversity retention `0.863`, mean success `0.482`

## Counts

- Main candidates: `5`
- Fallback candidates: `1`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.012214`
- minimum continuous_score_minus_axis_score: `-0.001944`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `18`
- Input ensemble: random-unitary diffusion at steps `[1, 2, 3, 5, 7, 12]`
- Denoising map: attach one complement qubit, evolve with the fixed Problem 2 Hamiltonian, then post-select on a continuous complement basis
- Continuous basis grid: theta points `13`, phi points `16`, excluding exact `Z/X/Y` axes
- Time grid: `linspace(0.05, 2.0, 20)`
- Axis baseline: best among `Z`, `X`, `Y` projection outcomes over the same time grid

## Adoption Decision

Overall decision: `use_as_main`

The result is a main candidate only when it improves at least one baseline metric, scores sufficiently above the best axis-only projection, keeps diversity, and has a reasonable mean post-selection probability.

## Best Overall Continuous Candidate

- Input step: `1`
- tau: `0.768421`
- theta: `0.785398`
- phi: `1.963495`
- MMD: `0.874393 -> 0.737153`
- Wasserstein: `0.724505 -> 0.570123`
- Diversity retention: `0.877247`
- Mean success probability: `0.286978`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.874393 -> 0.737153`, Wasserstein `0.724505 -> 0.570123`, diversity retention `0.877`, mean success `0.287`
- step `2`: decision `fallback_candidate`, MMD `0.848954 -> 0.793433`, Wasserstein `0.703851 -> 0.598176`, diversity retention `0.837`, mean success `0.505`
- step `3`: decision `fallback_candidate`, MMD `0.861857 -> 0.791746`, Wasserstein `0.712035 -> 0.597965`, diversity retention `0.842`, mean success `0.465`
- step `5`: decision `fallback_candidate`, MMD `0.868073 -> 0.731766`, Wasserstein `0.719077 -> 0.541771`, diversity retention `0.825`, mean success `0.506`
- step `7`: decision `main_candidate`, MMD `0.827714 -> 0.779358`, Wasserstein `0.686365 -> 0.590906`, diversity retention `0.846`, mean success `0.430`
- step `12`: decision `main_candidate`, MMD `0.874699 -> 0.764503`, Wasserstein `0.725800 -> 0.557683`, diversity retention `0.795`, mean success `0.418`

## Counts

- Main candidates: `3`
- Fallback candidates: `3`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.009518`
- minimum continuous_score_minus_axis_score: `-0.004926`
- nonpositive axis-margin rows: `2 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `16`
- Input ensemble: random-unitary diffusion at steps `[1, 2, 3, 5, 7, 12]`
- Denoising map: attach one complement qubit, evolve with the fixed Problem 2 Hamiltonian, then post-select on a continuous complement basis
- Continuous basis grid: theta points `13`, phi points `16`, excluding exact `Z/X/Y` axes
- Time grid: `linspace(0.05, 2.0, 20)`
- Axis baseline: best among `Z`, `X`, `Y` projection outcomes over the same time grid

## Adoption Decision

Overall decision: `use_as_main`

The result is a main candidate only when it improves at least one baseline metric, scores sufficiently above the best axis-only projection, keeps diversity, and has a reasonable mean post-selection probability.

## Best Overall Continuous Candidate

- Input step: `3`
- tau: `1.897368`
- theta: `1.570796`
- phi: `2.748894`
- MMD: `0.872757 -> 0.745889`
- Wasserstein: `0.724152 -> 0.552944`
- Diversity retention: `0.833355`
- Mean success probability: `0.433433`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.840956 -> 0.799143`, Wasserstein `0.694127 -> 0.600694`, diversity retention `0.827`, mean success `0.489`
- step `2`: decision `fallback_candidate`, MMD `0.847908 -> 0.772434`, Wasserstein `0.704447 -> 0.580154`, diversity retention `0.838`, mean success `0.477`
- step `3`: decision `main_candidate`, MMD `0.872757 -> 0.745889`, Wasserstein `0.724152 -> 0.552944`, diversity retention `0.833`, mean success `0.433`
- step `5`: decision `main_candidate`, MMD `0.863294 -> 0.750748`, Wasserstein `0.712074 -> 0.574095`, diversity retention `0.873`, mean success `0.474`
- step `7`: decision `main_candidate`, MMD `0.868985 -> 0.772773`, Wasserstein `0.721340 -> 0.602852`, diversity retention `0.894`, mean success `0.532`
- step `12`: decision `main_candidate`, MMD `0.865107 -> 0.770973`, Wasserstein `0.719117 -> 0.573241`, diversity retention `0.816`, mean success `0.493`

## Counts

- Main candidates: `5`
- Fallback candidates: `1`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.012213`
- minimum continuous_score_minus_axis_score: `0.002701`
- nonpositive axis-margin rows: `0 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

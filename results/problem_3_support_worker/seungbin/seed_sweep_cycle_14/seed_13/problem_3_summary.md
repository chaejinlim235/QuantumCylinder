# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `13`
- Input ensemble: random-unitary diffusion at steps `[1, 2, 3, 5, 7, 12]`
- Denoising map: attach one complement qubit, evolve with the fixed Problem 2 Hamiltonian, then post-select on a continuous complement basis
- Continuous basis grid: theta points `13`, phi points `16`, excluding exact `Z/X/Y` axes
- Time grid: `linspace(0.05, 2.0, 20)`
- Axis baseline: best among `Z`, `X`, `Y` projection outcomes over the same time grid

## Adoption Decision

Overall decision: `use_as_main`

The result is a main candidate only when it improves at least one baseline metric, scores sufficiently above the best axis-only projection, keeps diversity, and has a reasonable mean post-selection probability.

## Best Overall Continuous Candidate

- Input step: `12`
- tau: `0.871053`
- theta: `0.523599`
- phi: `0.000000`
- MMD: `0.902055 -> 0.717092`
- Wasserstein: `0.751664 -> 0.512509`
- Diversity retention: `0.766414`
- Mean success probability: `0.404485`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.859577 -> 0.795471`, Wasserstein `0.707742 -> 0.604903`, diversity retention `0.851`, mean success `0.453`
- step `2`: decision `main_candidate`, MMD `0.842089 -> 0.731783`, Wasserstein `0.698932 -> 0.525224`, diversity retention `0.770`, mean success `0.246`
- step `3`: decision `fallback_candidate`, MMD `0.890076 -> 0.781771`, Wasserstein `0.740571 -> 0.579365`, diversity retention `0.818`, mean success `0.467`
- step `5`: decision `fallback_candidate`, MMD `0.921684 -> 0.801067`, Wasserstein `0.770554 -> 0.611288`, diversity retention `0.864`, mean success `0.437`
- step `7`: decision `fallback_candidate`, MMD `0.909658 -> 0.761236`, Wasserstein `0.758183 -> 0.560407`, diversity retention `0.799`, mean success `0.457`
- step `12`: decision `main_candidate`, MMD `0.902055 -> 0.717092`, Wasserstein `0.751664 -> 0.512509`, diversity retention `0.766`, mean success `0.404`

## Counts

- Main candidates: `3`
- Fallback candidates: `3`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.013068`
- minimum continuous_score_minus_axis_score: `-0.001412`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

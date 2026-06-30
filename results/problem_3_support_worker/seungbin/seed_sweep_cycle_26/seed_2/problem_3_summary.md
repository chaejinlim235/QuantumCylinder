# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `2`
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
- tau: `1.794737`
- theta: `2.094395`
- phi: `3.534292`
- MMD: `0.873671 -> 0.666462`
- Wasserstein: `0.720111 -> 0.484538`
- Diversity retention: `0.801979`
- Mean success probability: `0.470875`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.825848 -> 0.764096`, Wasserstein `0.679952 -> 0.565762`, diversity retention `0.818`, mean success `0.484`
- step `2`: decision `main_candidate`, MMD `0.862814 -> 0.780501`, Wasserstein `0.713323 -> 0.584852`, diversity retention `0.835`, mean success `0.479`
- step `3`: decision `main_candidate`, MMD `0.873671 -> 0.666462`, Wasserstein `0.720111 -> 0.484538`, diversity retention `0.802`, mean success `0.471`
- step `5`: decision `fallback_candidate`, MMD `0.874376 -> 0.770708`, Wasserstein `0.728168 -> 0.562593`, diversity retention `0.795`, mean success `0.311`
- step `7`: decision `fallback_candidate`, MMD `0.839222 -> 0.753135`, Wasserstein `0.696703 -> 0.549519`, diversity retention `0.786`, mean success `0.470`
- step `12`: decision `fallback_candidate`, MMD `0.882075 -> 0.770577`, Wasserstein `0.733712 -> 0.584373`, diversity retention `0.850`, mean success `0.456`

## Counts

- Main candidates: `3`
- Fallback candidates: `3`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.006417`
- minimum continuous_score_minus_axis_score: `0.000792`
- nonpositive axis-margin rows: `0 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `20`
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
- tau: `1.897368`
- theta: `2.094395`
- phi: `3.534292`
- MMD: `0.892796 -> 0.725668`
- Wasserstein: `0.742802 -> 0.550685`
- Diversity retention: `0.860754`
- Mean success probability: `0.504133`

## Step-Level Decisions

- step `1`: decision `fallback_candidate`, MMD `0.857324 -> 0.768939`, Wasserstein `0.706791 -> 0.575292`, diversity retention `0.830`, mean success `0.487`
- step `2`: decision `fallback_candidate`, MMD `0.865138 -> 0.724555`, Wasserstein `0.718044 -> 0.549837`, diversity retention `0.856`, mean success `0.458`
- step `3`: decision `main_candidate`, MMD `0.848392 -> 0.765754`, Wasserstein `0.704042 -> 0.576854`, diversity retention `0.847`, mean success `0.451`
- step `5`: decision `fallback_candidate`, MMD `0.892245 -> 0.770348`, Wasserstein `0.741104 -> 0.576428`, diversity retention `0.838`, mean success `0.473`
- step `7`: decision `main_candidate`, MMD `0.892796 -> 0.725668`, Wasserstein `0.742802 -> 0.550685`, diversity retention `0.861`, mean success `0.504`
- step `12`: decision `main_candidate`, MMD `0.834671 -> 0.739345`, Wasserstein `0.688637 -> 0.554872`, diversity retention `0.848`, mean success `0.472`

## Counts

- Main candidates: `3`
- Fallback candidates: `3`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.005036`
- minimum continuous_score_minus_axis_score: `-0.005002`
- nonpositive axis-margin rows: `2 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

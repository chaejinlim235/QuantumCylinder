# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `15`
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
- tau: `0.871053`
- theta: `0.785398`
- phi: `0.000000`
- MMD: `0.890421 -> 0.777463`
- Wasserstein: `0.744161 -> 0.592574`
- Diversity retention: `0.851595`
- Mean success probability: `0.489175`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.817857 -> 0.795674`, Wasserstein `0.676046 -> 0.642062`, diversity retention `0.951`, mean success `0.556`
- step `2`: decision `main_candidate`, MMD `0.827601 -> 0.777700`, Wasserstein `0.687864 -> 0.576638`, diversity retention `0.820`, mean success `0.389`
- step `3`: decision `fallback_candidate`, MMD `0.885179 -> 0.834646`, Wasserstein `0.736429 -> 0.611126`, diversity retention `0.779`, mean success `0.471`
- step `5`: decision `fallback_candidate`, MMD `0.851741 -> 0.781799`, Wasserstein `0.705764 -> 0.550947`, diversity retention `0.739`, mean success `0.417`
- step `7`: decision `main_candidate`, MMD `0.890421 -> 0.777463`, Wasserstein `0.744161 -> 0.592574`, diversity retention `0.852`, mean success `0.489`
- step `12`: decision `main_candidate`, MMD `0.869546 -> 0.781495`, Wasserstein `0.723550 -> 0.592143`, diversity retention `0.840`, mean success `0.449`

## Counts

- Main candidates: `4`
- Fallback candidates: `2`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.011919`
- minimum continuous_score_minus_axis_score: `-0.005900`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `6`
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
- theta: `1.832596`
- phi: `3.534292`
- MMD: `0.870093 -> 0.768662`
- Wasserstein: `0.722936 -> 0.573045`
- Diversity retention: `0.824805`
- Mean success probability: `0.469751`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.874416 -> 0.777783`, Wasserstein `0.725480 -> 0.577371`, diversity retention `0.811`, mean success `0.485`
- step `2`: decision `fallback_candidate`, MMD `0.866029 -> 0.736166`, Wasserstein `0.717706 -> 0.553897`, diversity retention `0.842`, mean success `0.477`
- step `3`: decision `main_candidate`, MMD `0.870093 -> 0.768662`, Wasserstein `0.722936 -> 0.573045`, diversity retention `0.825`, mean success `0.470`
- step `5`: decision `main_candidate`, MMD `0.855432 -> 0.765962`, Wasserstein `0.711724 -> 0.579431`, diversity retention `0.845`, mean success `0.429`
- step `7`: decision `main_candidate`, MMD `0.854547 -> 0.755992`, Wasserstein `0.708946 -> 0.568857`, diversity retention `0.854`, mean success `0.437`
- step `12`: decision `fallback_candidate`, MMD `0.870020 -> 0.752664`, Wasserstein `0.721560 -> 0.555867`, diversity retention `0.815`, mean success `0.491`

## Counts

- Main candidates: `4`
- Fallback candidates: `2`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.007810`
- minimum continuous_score_minus_axis_score: `-0.005079`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

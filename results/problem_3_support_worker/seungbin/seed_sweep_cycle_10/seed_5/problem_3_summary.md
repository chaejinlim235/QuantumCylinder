# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `5`
- Input ensemble: random-unitary diffusion at steps `[1, 2, 3, 5, 7, 12]`
- Denoising map: attach one complement qubit, evolve with the fixed Problem 2 Hamiltonian, then post-select on a continuous complement basis
- Continuous basis grid: theta points `13`, phi points `16`, excluding exact `Z/X/Y` axes
- Time grid: `linspace(0.05, 2.0, 20)`
- Axis baseline: best among `Z`, `X`, `Y` projection outcomes over the same time grid

## Adoption Decision

Overall decision: `use_as_main`

The result is a main candidate only when it improves at least one baseline metric, scores sufficiently above the best axis-only projection, keeps diversity, and has a reasonable mean post-selection probability.

## Best Overall Continuous Candidate

- Input step: `5`
- tau: `0.768421`
- theta: `0.785398`
- phi: `0.785398`
- MMD: `0.846983 -> 0.747862`
- Wasserstein: `0.704079 -> 0.573678`
- Diversity retention: `0.860466`
- Mean success probability: `0.488042`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.854029 -> 0.790264`, Wasserstein `0.710077 -> 0.595945`, diversity retention `0.824`, mean success `0.462`
- step `2`: decision `fallback_candidate`, MMD `0.871516 -> 0.773462`, Wasserstein `0.726110 -> 0.568552`, diversity retention `0.788`, mean success `0.492`
- step `3`: decision `fallback_candidate`, MMD `0.855007 -> 0.788280`, Wasserstein `0.711667 -> 0.582822`, diversity retention `0.799`, mean success `0.490`
- step `5`: decision `main_candidate`, MMD `0.846983 -> 0.747862`, Wasserstein `0.704079 -> 0.573678`, diversity retention `0.860`, mean success `0.488`
- step `7`: decision `main_candidate`, MMD `0.856550 -> 0.769461`, Wasserstein `0.710155 -> 0.588090`, diversity retention `0.860`, mean success `0.488`
- step `12`: decision `main_candidate`, MMD `0.833035 -> 0.769940`, Wasserstein `0.694227 -> 0.567622`, diversity retention `0.803`, mean success `0.479`

## Counts

- Main candidates: `4`
- Fallback candidates: `2`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.010324`
- minimum continuous_score_minus_axis_score: `-0.000097`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

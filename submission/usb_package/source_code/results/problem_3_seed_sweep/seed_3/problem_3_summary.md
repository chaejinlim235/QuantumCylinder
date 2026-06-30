# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `3`
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
- tau: `0.871053`
- theta: `0.523599`
- phi: `0.785398`
- MMD: `0.918756 -> 0.741729`
- Wasserstein: `0.761361 -> 0.544186`
- Diversity retention: `0.813082`
- Mean success probability: `0.412774`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.918756 -> 0.741729`, Wasserstein `0.761361 -> 0.544186`, diversity retention `0.813`, mean success `0.413`
- step `2`: decision `main_candidate`, MMD `0.867212 -> 0.761269`, Wasserstein `0.720939 -> 0.575120`, diversity retention `0.833`, mean success `0.474`
- step `3`: decision `fallback_candidate`, MMD `0.868285 -> 0.761958`, Wasserstein `0.720829 -> 0.569777`, diversity retention `0.828`, mean success `0.469`
- step `5`: decision `main_candidate`, MMD `0.839388 -> 0.788879`, Wasserstein `0.691614 -> 0.589737`, diversity retention `0.833`, mean success `0.467`
- step `7`: decision `main_candidate`, MMD `0.854256 -> 0.778373`, Wasserstein `0.710436 -> 0.590576`, diversity retention `0.834`, mean success `0.460`
- step `12`: decision `main_candidate`, MMD `0.854864 -> 0.778812`, Wasserstein `0.707233 -> 0.570360`, diversity retention `0.797`, mean success `0.456`

## Counts

- Main candidates: `5`
- Fallback candidates: `1`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.018704`
- minimum continuous_score_minus_axis_score: `-0.003928`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

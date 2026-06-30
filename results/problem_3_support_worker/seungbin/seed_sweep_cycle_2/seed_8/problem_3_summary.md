# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `8`
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
- phi: `3.141593`
- MMD: `0.895096 -> 0.756195`
- Wasserstein: `0.744522 -> 0.555111`
- Diversity retention: `0.804585`
- Mean success probability: `0.449357`

## Step-Level Decisions

- step `1`: decision `fallback_candidate`, MMD `0.815433 -> 0.796853`, Wasserstein `0.668088 -> 0.623049`, diversity retention `0.916`, mean success `0.388`
- step `2`: decision `main_candidate`, MMD `0.861720 -> 0.757068`, Wasserstein `0.712605 -> 0.553289`, diversity retention `0.801`, mean success `0.385`
- step `3`: decision `main_candidate`, MMD `0.895096 -> 0.756195`, Wasserstein `0.744522 -> 0.555111`, diversity retention `0.805`, mean success `0.449`
- step `5`: decision `main_candidate`, MMD `0.880266 -> 0.751813`, Wasserstein `0.733978 -> 0.534627`, diversity retention `0.757`, mean success `0.448`
- step `7`: decision `main_candidate`, MMD `0.818948 -> 0.790385`, Wasserstein `0.677060 -> 0.582118`, diversity retention `0.802`, mean success `0.259`
- step `12`: decision `fallback_candidate`, MMD `0.872853 -> 0.776983`, Wasserstein `0.720076 -> 0.565361`, diversity retention `0.787`, mean success `0.481`

## Counts

- Main candidates: `4`
- Fallback candidates: `2`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.007557`
- minimum continuous_score_minus_axis_score: `-0.000120`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

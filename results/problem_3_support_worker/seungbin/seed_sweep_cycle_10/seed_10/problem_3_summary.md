# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `10`
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
- tau: `1.794737`
- theta: `1.832596`
- phi: `3.141593`
- MMD: `0.872323 -> 0.749190`
- Wasserstein: `0.725597 -> 0.540323`
- Diversity retention: `0.760345`
- Mean success probability: `0.517152`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.872323 -> 0.749190`, Wasserstein `0.725597 -> 0.540323`, diversity retention `0.760`, mean success `0.517`
- step `2`: decision `main_candidate`, MMD `0.880910 -> 0.779214`, Wasserstein `0.735704 -> 0.576552`, diversity retention `0.789`, mean success `0.392`
- step `3`: decision `main_candidate`, MMD `0.871436 -> 0.794890`, Wasserstein `0.728640 -> 0.585828`, diversity retention `0.793`, mean success `0.494`
- step `5`: decision `main_candidate`, MMD `0.882425 -> 0.763507`, Wasserstein `0.738357 -> 0.577919`, diversity retention `0.843`, mean success `0.437`
- step `7`: decision `fallback_candidate`, MMD `0.848441 -> 0.779348`, Wasserstein `0.708211 -> 0.558806`, diversity retention `0.746`, mean success `0.328`
- step `12`: decision `main_candidate`, MMD `0.869685 -> 0.749151`, Wasserstein `0.725358 -> 0.562673`, diversity retention `0.823`, mean success `0.401`

## Counts

- Main candidates: `5`
- Fallback candidates: `1`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.012110`
- minimum continuous_score_minus_axis_score: `0.002806`
- nonpositive axis-margin rows: `0 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

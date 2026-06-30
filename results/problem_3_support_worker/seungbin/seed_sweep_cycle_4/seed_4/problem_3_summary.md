# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `4`
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
- tau: `1.794737`
- theta: `1.832596`
- phi: `3.141593`
- MMD: `0.877274 -> 0.760992`
- Wasserstein: `0.725538 -> 0.559903`
- Diversity retention: `0.805074`
- Mean success probability: `0.469267`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.817728 -> 0.736779`, Wasserstein `0.671843 -> 0.538545`, diversity retention `0.800`, mean success `0.498`
- step `2`: decision `fallback_candidate`, MMD `0.887920 -> 0.781295`, Wasserstein `0.737096 -> 0.573246`, diversity retention `0.803`, mean success `0.487`
- step `3`: decision `fallback_candidate`, MMD `0.856414 -> 0.796546`, Wasserstein `0.708980 -> 0.587723`, diversity retention `0.806`, mean success `0.462`
- step `5`: decision `main_candidate`, MMD `0.849313 -> 0.783664`, Wasserstein `0.704682 -> 0.588209`, diversity retention `0.850`, mean success `0.456`
- step `7`: decision `main_candidate`, MMD `0.877274 -> 0.760992`, Wasserstein `0.725538 -> 0.559903`, diversity retention `0.805`, mean success `0.469`
- step `12`: decision `main_candidate`, MMD `0.884355 -> 0.799942`, Wasserstein `0.730915 -> 0.580539`, diversity retention `0.777`, mean success `0.417`

## Counts

- Main candidates: `4`
- Fallback candidates: `2`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.008488`
- minimum continuous_score_minus_axis_score: `-0.001424`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `1`
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
- tau: `1.794737`
- theta: `1.832596`
- phi: `3.534292`
- MMD: `0.879708 -> 0.745454`
- Wasserstein: `0.734101 -> 0.556382`
- Diversity retention: `0.811335`
- Mean success probability: `0.488998`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.878455 -> 0.769271`, Wasserstein `0.724953 -> 0.577017`, diversity retention `0.850`, mean success `0.257`
- step `2`: decision `main_candidate`, MMD `0.826410 -> 0.781361`, Wasserstein `0.688258 -> 0.568397`, diversity retention `0.781`, mean success `0.372`
- step `3`: decision `main_candidate`, MMD `0.812318 -> 0.760575`, Wasserstein `0.673106 -> 0.560015`, diversity retention `0.808`, mean success `0.474`
- step `5`: decision `main_candidate`, MMD `0.859385 -> 0.784219`, Wasserstein `0.717209 -> 0.560894`, diversity retention `0.745`, mean success `0.232`
- step `7`: decision `fallback_candidate`, MMD `0.866439 -> 0.738239`, Wasserstein `0.722659 -> 0.545802`, diversity retention `0.801`, mean success `0.486`
- step `12`: decision `main_candidate`, MMD `0.879708 -> 0.745454`, Wasserstein `0.734101 -> 0.556382`, diversity retention `0.811`, mean success `0.489`

## Counts

- Main candidates: `5`
- Fallback candidates: `1`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.012996`
- minimum continuous_score_minus_axis_score: `0.003770`
- nonpositive axis-margin rows: `0 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

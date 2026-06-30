# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `7`
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
- phi: `1.178097`
- MMD: `0.882606 -> 0.777593`
- Wasserstein: `0.733305 -> 0.590265`
- Diversity retention: `0.850460`
- Mean success probability: `0.366858`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.882606 -> 0.777593`, Wasserstein `0.733305 -> 0.590265`, diversity retention `0.850`, mean success `0.367`
- step `2`: decision `fallback_candidate`, MMD `0.880675 -> 0.748218`, Wasserstein `0.733268 -> 0.559770`, diversity retention `0.822`, mean success `0.512`
- step `3`: decision `fallback_candidate`, MMD `0.895677 -> 0.791014`, Wasserstein `0.749967 -> 0.584109`, diversity retention `0.788`, mean success `0.482`
- step `5`: decision `main_candidate`, MMD `0.873012 -> 0.775533`, Wasserstein `0.726682 -> 0.568083`, diversity retention `0.785`, mean success `0.371`
- step `7`: decision `main_candidate`, MMD `0.853345 -> 0.783457`, Wasserstein `0.706244 -> 0.594249`, diversity retention `0.838`, mean success `0.381`
- step `12`: decision `fallback_candidate`, MMD `0.828093 -> 0.794896`, Wasserstein `0.686108 -> 0.642223`, diversity retention `0.948`, mean success `0.411`

## Counts

- Main candidates: `3`
- Fallback candidates: `3`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.011047`
- minimum continuous_score_minus_axis_score: `-0.002286`
- nonpositive axis-margin rows: `2 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

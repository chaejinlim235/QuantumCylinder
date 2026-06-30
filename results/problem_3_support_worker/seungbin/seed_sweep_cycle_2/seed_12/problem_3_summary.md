# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `12`
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
- tau: `0.871053`
- theta: `0.523599`
- phi: `0.392699`
- MMD: `0.879260 -> 0.744717`
- Wasserstein: `0.732044 -> 0.549341`
- Diversity retention: `0.795617`
- Mean success probability: `0.434678`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.845525 -> 0.759469`, Wasserstein `0.701407 -> 0.573556`, diversity retention `0.839`, mean success `0.316`
- step `2`: decision `fallback_candidate`, MMD `0.890072 -> 0.766302`, Wasserstein `0.743495 -> 0.582589`, diversity retention `0.859`, mean success `0.430`
- step `3`: decision `fallback_candidate`, MMD `0.902053 -> 0.733837`, Wasserstein `0.752185 -> 0.550541`, diversity retention `0.837`, mean success `0.476`
- step `5`: decision `fallback_candidate`, MMD `0.874953 -> 0.779224`, Wasserstein `0.732031 -> 0.582815`, diversity retention `0.818`, mean success `0.457`
- step `7`: decision `main_candidate`, MMD `0.850212 -> 0.725112`, Wasserstein `0.709311 -> 0.548496`, diversity retention `0.847`, mean success `0.452`
- step `12`: decision `main_candidate`, MMD `0.879260 -> 0.744717`, Wasserstein `0.732044 -> 0.549341`, diversity retention `0.796`, mean success `0.435`

## Counts

- Main candidates: `3`
- Fallback candidates: `3`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.009204`
- minimum continuous_score_minus_axis_score: `-0.007710`
- nonpositive axis-margin rows: `2 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

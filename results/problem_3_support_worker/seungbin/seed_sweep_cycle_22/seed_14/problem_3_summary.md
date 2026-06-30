# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `14`
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
- tau: `0.871053`
- theta: `0.523599`
- phi: `1.178097`
- MMD: `0.901099 -> 0.724880`
- Wasserstein: `0.746096 -> 0.534498`
- Diversity retention: `0.815871`
- Mean success probability: `0.405174`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.878949 -> 0.779790`, Wasserstein `0.732787 -> 0.564584`, diversity retention `0.770`, mean success `0.451`
- step `2`: decision `fallback_candidate`, MMD `0.876121 -> 0.748846`, Wasserstein `0.732754 -> 0.567450`, diversity retention `0.852`, mean success `0.473`
- step `3`: decision `main_candidate`, MMD `0.876130 -> 0.757991`, Wasserstein `0.729958 -> 0.581928`, diversity retention `0.858`, mean success `0.518`
- step `5`: decision `main_candidate`, MMD `0.901099 -> 0.724880`, Wasserstein `0.746096 -> 0.534498`, diversity retention `0.816`, mean success `0.405`
- step `7`: decision `main_candidate`, MMD `0.879480 -> 0.749072`, Wasserstein `0.728636 -> 0.541338`, diversity retention `0.773`, mean success `0.519`
- step `12`: decision `main_candidate`, MMD `0.897268 -> 0.755877`, Wasserstein `0.748945 -> 0.551342`, diversity retention `0.783`, mean success `0.488`

## Counts

- Main candidates: `5`
- Fallback candidates: `1`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.016376`
- minimum continuous_score_minus_axis_score: `0.002172`
- nonpositive axis-margin rows: `0 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

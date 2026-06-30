# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `19`
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
- tau: `2.000000`
- theta: `1.570796`
- phi: `2.356194`
- MMD: `0.926907 -> 0.772723`
- Wasserstein: `0.776338 -> 0.581595`
- Diversity retention: `0.847467`
- Mean success probability: `0.450627`

## Step-Level Decisions

- step `1`: decision `fallback_candidate`, MMD `0.860452 -> 0.770915`, Wasserstein `0.711740 -> 0.549403`, diversity retention `0.757`, mean success `0.474`
- step `2`: decision `fallback_candidate`, MMD `0.864793 -> 0.790449`, Wasserstein `0.720765 -> 0.582609`, diversity retention `0.800`, mean success `0.471`
- step `3`: decision `fallback_candidate`, MMD `0.839835 -> 0.774310`, Wasserstein `0.695800 -> 0.571702`, diversity retention `0.808`, mean success `0.513`
- step `5`: decision `main_candidate`, MMD `0.853867 -> 0.771189`, Wasserstein `0.708329 -> 0.555993`, diversity retention `0.767`, mean success `0.379`
- step `7`: decision `main_candidate`, MMD `0.926907 -> 0.772723`, Wasserstein `0.776338 -> 0.581595`, diversity retention `0.847`, mean success `0.451`
- step `12`: decision `main_candidate`, MMD `0.898064 -> 0.763559`, Wasserstein `0.749117 -> 0.576248`, diversity retention `0.846`, mean success `0.487`

## Counts

- Main candidates: `3`
- Fallback candidates: `3`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.006008`
- minimum continuous_score_minus_axis_score: `-0.004186`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

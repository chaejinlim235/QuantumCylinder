# Problem 3 Continuous Projected Denoising Summary

## Experiment

- Target ensemble: `N = 80`, `sigma = 0.1`, seed `11`
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
- theta: `1.570796`
- phi: `2.748894`
- MMD: `0.874171 -> 0.770400`
- Wasserstein: `0.729132 -> 0.581067`
- Diversity retention: `0.835990`
- Mean success probability: `0.474531`

## Step-Level Decisions

- step `1`: decision `main_candidate`, MMD `0.862749 -> 0.768249`, Wasserstein `0.711823 -> 0.584110`, diversity retention `0.856`, mean success `0.475`
- step `2`: decision `fallback_candidate`, MMD `0.880402 -> 0.779387`, Wasserstein `0.734255 -> 0.589561`, diversity retention `0.847`, mean success `0.450`
- step `3`: decision `main_candidate`, MMD `0.852723 -> 0.778384`, Wasserstein `0.711310 -> 0.577806`, diversity retention `0.808`, mean success `0.421`
- step `5`: decision `fallback_candidate`, MMD `0.885176 -> 0.760082`, Wasserstein `0.740876 -> 0.556976`, diversity retention `0.781`, mean success `0.479`
- step `7`: decision `main_candidate`, MMD `0.874171 -> 0.770400`, Wasserstein `0.729132 -> 0.581067`, diversity retention `0.836`, mean success `0.475`
- step `12`: decision `main_candidate`, MMD `0.845646 -> 0.793227`, Wasserstein `0.704473 -> 0.592558`, diversity retention `0.813`, mean success `0.468`

## Counts

- Main candidates: `4`
- Fallback candidates: `2`
- Do not use as main: `0`

## Axis Baseline Comparison

- median continuous_score_minus_axis_score: `0.013123`
- minimum continuous_score_minus_axis_score: `-0.003841`
- nonpositive axis-margin rows: `1 / 6`

The continuous basis search is compared against the best exact `Z/X/Y` axis projection at the same time grid. If this margin is small or negative on fallback rows, treat it as a limitation. Do not claim every input step beats the axis-only projection; use the seed sweep as the robustness gate.

## Generated Files

- `best_denoising_metrics.csv`
- `candidate_search_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`

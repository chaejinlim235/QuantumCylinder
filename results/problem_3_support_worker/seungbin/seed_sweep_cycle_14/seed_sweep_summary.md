# Problem 3 Seed Sweep Summary

## Decision

Main-claim recommendation: `use_as_main`

## Seed-Level Decisions

- seed `1`: `use_as_main`
- seed `2`: `use_as_main`
- seed `3`: `use_as_main`
- seed `4`: `use_as_main`
- seed `5`: `use_as_main`
- seed `6`: `use_as_main`
- seed `7`: `use_as_main`
- seed `8`: `use_as_main`
- seed `9`: `use_as_main`
- seed `10`: `use_as_main`
- seed `11`: `use_as_main`
- seed `12`: `use_as_main`
- seed `13`: `use_as_main`
- seed `14`: `use_as_main`
- seed `15`: `use_as_main`
- seed `16`: `use_as_main`
- seed `17`: `use_as_main`
- seed `18`: `use_as_main`
- seed `19`: `use_as_main`
- seed `20`: `use_as_main`

## Counts

- Total seeds: `20`
- use_as_main: `20`
- fallback_only: `0`
- do_not_use_as_main: `0`
- unknown: `0`
- use_as_main fraction: `1.000`

## Row-Level Counts

- Total rows: `120`
- main_candidate rows: `81`
- fallback_candidate rows: `39`
- do_not_use_as_main rows: `0`
- main_candidate row fraction: `0.675`

## Medians Across Best Rows

- continuous_mmd_improvement: `0.097056`
- continuous_wasserstein_improvement: `0.147983`
- continuous_score_minus_axis_score: `0.010000`
- continuous_diversity_retention: `0.823217`
- continuous_mean_success_probability: `0.468122`

## Guardrail Checks

Worst-case checks across best rows; these expose weak fallback rows and do not replace the median adoption gate.

- minimum continuous_mmd_improvement: `0.018580`
- minimum continuous_wasserstein_improvement: `0.033984`
- minimum continuous_score_minus_axis_score: `-0.007710`
- nonpositive axis-margin rows: `18 / 120`
- minimum continuous_diversity_retention: `0.738651`
- minimum continuous_mean_success_probability: `0.231655`

## Report Table

| Metric | Value | Report use |
| --- | --- | --- |
| Recommendation | `use_as_main` | main-claim gate |
| Passing seeds | `20 / 20` | seed robustness gate |
| Main-candidate rows | `81 / 120 = 0.675` | row-level robustness |
| Median MMD improvement | `0.097056` | distance improvement |
| Median Wasserstein improvement | `0.147983` | distance improvement |
| Median axis-only score margin | `0.010000` | limitation, not a broad advantage claim |
| Median diversity retention | `0.823217` | collapse guardrail |
| Median mean success probability | `0.468122` | post-selection feasibility |
| Nonpositive axis-margin rows | `18 / 120` | axis-comparison caveat |

## Report-Ready Wording

Use: Across the 20 / 20 requested seeds, continuous measurement-basis post-selection remains a reproducible small-scale state-vector denoising proxy, with median MMD improvement `0.097056` and median Wasserstein improvement `0.147983`. The axis-only score margin is small (`0.010000`), so present it as a limited post-selected proxy improvement, not hardware advantage or general quantum advantage.

## Final Claim Guidance

The seed sweep supports using continuous projected denoising as the main Problem 3 result, with the caveat that the median axis-only score margin is `0.010000`. Do not claim every input step beats the axis-only projection if fallback rows have weak margins. State this as a small-scale post-selected proxy improvement, not hardware advantage or general quantum advantage.

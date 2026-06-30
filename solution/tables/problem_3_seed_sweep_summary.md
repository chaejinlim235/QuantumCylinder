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

## 3-b Analysis

- Seed robustness: `20 / 20` seeds pass the main gate, so the effect is not a single-seed accident.
- Distance recovery: median MMD and Wasserstein improvements are `0.097056` and `0.147983`, so the post-selected map moves the ensemble back toward `S0` under both metrics.
- Axis comparison: the median continuous-vs-axis score margin is only `0.010000`, with `18 / 120` nonpositive rows. Treat `axis-only` as a discrete baseline, not as a team-proposed method, and do not claim continuous control is overwhelmingly better.
- Guardrails: median diversity retention is `0.823217` and median success probability is `0.468122`, so the result should be described as a recoverability trade-off rather than a distance-only win.
- 3-c implication: use this trade-off to motivate two-way projected denoising as the main improvement; keep random final kick, hybrid 1M+1F, and actor-critic as appendix/ablation candidates.

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

Use in 3-b: Across the 20 / 20 requested seeds, continuous measurement-basis post-selection remains a reproducible small-scale state-vector controlled modification/reference, with median MMD improvement `0.097056` and median Wasserstein improvement `0.147983`. The axis-only score margin is small (`0.010000`), so present it as a recoverability trade-off analysis, not hardware advantage or general quantum advantage. Use this analysis to motivate the 3-c two-way projected denoising proposal.

## Final Claim Guidance

The seed sweep supports using continuous projected denoising as the Problem 3(b) controlled modification/reference, with the caveat that the median axis-only score margin is `0.010000`. Do not claim every input step beats the axis-only projection if fallback rows have weak margins. State this as a small-scale recoverability trade-off that motivates the Problem 3(c) two-way projected denoising proposal, not hardware advantage or general quantum advantage.

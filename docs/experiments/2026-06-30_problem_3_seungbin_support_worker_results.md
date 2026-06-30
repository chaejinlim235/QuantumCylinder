# Problem 3 Seungbin Support Worker Results

## Run Context

- worker: `seungbin`
- machine role: independent support worker
- branch: `main`
- latest local base while harvesting: `e2a9045`
- status timestamp: `2026-06-30T09:28:31`
- cycle mode: continuous, `CycleMinutes 0`
- full seed sweep cadence: every `2` cycles
- hybrid seeds: `2026, 2027, 2028`
- angle scales: `0.5, 1.0, 3.141592653589793`

## Local Artifact Paths

- status: `results/problem_3_support_worker/seungbin/latest_status.md`
- progress log: `results/problem_3_support_worker/seungbin/progress_log.md`
- detailed logs: `logs/problem_3_support_worker/seungbin/`
- latest seed sweep used here: `results/problem_3_support_worker/seungbin/seed_sweep_cycle_28/`

## Completed Evidence

- cycle 21: pass, hybrid runs `9`, seed sweep `not-due`
- cycle 22: pass, hybrid runs `9`, seed sweep `passed`
- cycle 23: pass, hybrid runs `9`, seed sweep `not-due`
- cycle 24: pass, hybrid runs `9`, seed sweep `passed`
- cycle 25: pass, hybrid runs `9`, seed sweep `not-due`
- cycle 26: pass, hybrid runs `9`, seed sweep `passed`
- cycle 27: pass, hybrid runs `9`, seed sweep `not-due`
- cycle 28: pass, hybrid runs `9`, seed sweep `passed`

The support worker completed at least cycles `1` through `28`; cycle `28` is the latest completed full seed-sweep cycle recorded for this handoff. Cycle `29` was started after cycle `28`, but it is not used as evidence here.

Across the completed cycles:

- completed hybrid toy runs: at least `28 * 9 = 252`
- completed full 20-seed sweeps: `14` even-numbered cycles through cycle `28`
- latest full sweep decision: `use_as_main`

## Latest Full Seed Sweep Summary

From `cycle_28_seed_sweep.log`:

| Metric | Value |
| --- | --- |
| Recommendation | `use_as_main` |
| Passing seeds | `20 / 20` |
| Main-candidate rows | `81 / 120 = 0.675` |
| Median MMD improvement | `0.097056` |
| Median Wasserstein improvement | `0.147983` |
| Median axis-only score margin | `0.010000` |
| Median diversity retention | `0.823217` |
| Median mean success probability | `0.468122` |
| Nonpositive axis-margin rows | `18 / 120` |

Worst-case guardrail checks:

- minimum continuous MMD improvement: `0.018580`
- minimum continuous Wasserstein improvement: `0.033984`
- minimum continuous score minus axis score: `-0.007710`
- minimum continuous diversity retention: `0.738651`
- minimum continuous mean success probability: `0.231655`

## Interpretation

The support worker results independently reproduce the Problem 3 continuous measurement-basis post-selection story over repeated cycles and repeated 20-seed sweeps. The latest full sweep supports using the continuous projected denoising result as the main Problem 3 state-vector result.

Safe wording:

> Across the 20 / 20 requested seeds, continuous measurement-basis post-selection remains a reproducible small-scale state-vector denoising proxy, with median MMD improvement `0.097056` and median Wasserstein improvement `0.147983`. The axis-only score margin is small (`0.010000`), so present it as a limited post-selected proxy improvement, not hardware advantage or general quantum advantage.

## Claim Guardrails

- Use these support-worker results as reproducibility and ablation evidence.
- Do not claim hardware advantage.
- Do not claim general quantum advantage.
- Do not claim every input step beats the axis-only projection.
- Do not claim this is a full trainable QuDDPM reverse process.

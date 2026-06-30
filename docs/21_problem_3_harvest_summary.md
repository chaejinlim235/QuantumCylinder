# Problem 3 Harvest Summary

Generated from the Day 2 morning harvest after the overnight finalist autopilot run.

## Executive Decision

Problem 3 자동화는 여기서 멈추고 수확 단계로 전환한다. Cycle 수는 충분하다. 최종 전략은 다음 순서로 고정한다.

1. Main quantitative result: 2-data-qubit continuous measurement-basis post-selection benchmark
2. Robustness guardrail: frozen-parameter holdout
3. Judge-facing defense: baseline/collapse table
4. Front-facing extension: 1-data-qubit + 1-auxiliary-qubit hybrid random-unitary/Hamiltonian toy

이 결과는 hardware advantage나 general quantum advantage가 아니다. 작은 state-vector benchmark/probe로 제한해서 주장한다.

## Autopilot Outcome

- last useful recorded cycle: `60`
- cycle 60 status: `pass`
- local cycle 62 was stopped manually while running, so it is not used as evidence
- later repeated failures before stopping were mainly network/API related, not metric failure
- main remaining source changes are deliberate harvest outputs

Current source changes to keep:

- `docs/21_problem_3_harvest_summary.md`
- `scripts/run_problem_3_hybrid_diffusion_toy.py`
- `scripts/summarize_problem_3_frozen_holdout.py`
- `scripts/summarize_problem_3_baseline_collapse_table.py`
- `tests/test_problem_3_frozen_parameter_holdout.py`
- `tests/test_problem_3_baseline_collapse_table.py`
- `docs/19_problem_3_finalist_autopilot.md`

Generated `results/` files are local artifacts and are not committed by default. They can be regenerated with the commands below.

## Main Quantitative Gate

Use the 20-seed continuous post-selection result as the main quantitative claim.

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

Safe interpretation: the method reproducibly improves the toy post-selected proxy across seeds, but the axis-only margin is small. Do not claim overwhelming continuous-basis superiority.

## Frozen-Parameter Holdout

Purpose: answer the judge question, "Did you cherry-pick the best parameter separately for every seed?"

The holdout script selects one tuple from train seeds `1..10`, then evaluates the same tuple on holdout seeds `11..20`.

| Metric | Value |
| --- | --- |
| Frozen tuple `(tau, theta, phi)` | `(1.794737, 1.832596, 3.141593)` |
| Holdout rows | `60` |
| Positive-improvement holdout rows | `60 / 60` |
| Median fixed-parameter MMD improvement | `0.073421` |
| Median fixed-parameter Wasserstein improvement | `0.136641` |
| Median fixed-parameter diversity retention | `0.790676` |
| Median fixed-parameter success probability | `0.477322` |
| Same-holdout oracle MMD improvement | `0.098611` |
| Same-holdout oracle Wasserstein improvement | `0.148640` |

Safe interpretation: a fixed train-selected continuous parameter still helps on held-out seeds. It is weaker than oracle grid-best, which is expected and honest.

## Baseline And Collapse Defense

Purpose: answer the judge question, "If MMD/Wasserstein gets smaller, did the model actually denoise or just collapse the ensemble?"

| Method | Positive rows | Median MMD improvement | Median Wasserstein improvement | Median diversity retention | Median success probability |
| --- | --- | --- | --- | --- | --- |
| Identity/no-denoising | `0 / 120` | `0.000000` | `0.000000` | `1.000000` | `1.000000` |
| Best exact `Z/X/Y` axis projection | `120 / 120` | `0.086055` | `0.142594` | `0.810592` | `0.465058` |
| Continuous post-selection | `120 / 120` | `0.097056` | `0.147983` | `0.823217` | `0.468122` |
| Diagnostic collapse-to-centroid | `120 / 120` | `0.859292` | `0.714276` | `0.000000` | `1.000000` |

Safe interpretation: distance metrics alone are insufficient. The intentionally collapsed diagnostic looks excellent by MMD/Wasserstein but destroys diversity, so the report must always show diversity retention and success probability beside distance improvement.

## Hybrid Extension

Purpose: give the team a memorable, hardware-motivated extension without replacing the main result.

| Metric | Value |
| --- | --- |
| Toy size | `1 data qubit + 1 auxiliary qubit` |
| Positive-improvement rows | `4 / 4` |
| Median MMD improvement | `0.211078` |
| Median Wasserstein improvement | `0.223252` |
| Median diversity retention | `0.573138` |
| Median success probability | `0.505744` |
| Decision | `front_facing_extension` |

Safe interpretation: use this as a circuit-level plausibility extension toward IBM-style two-qubit execution. Do not use it as the main quantitative result.

## Regeneration Commands

```powershell
cd C:\Coding\Hackathon\2026Quantum
python scripts\summarize_problem_3_frozen_holdout.py
python scripts\summarize_problem_3_baseline_collapse_table.py
python scripts\run_problem_3_hybrid_diffusion_toy.py
python submission\run_all.py --quick
python -m pytest
```

## Final Report Wording

> Our main quantitative result is a reproducible continuous measurement-basis post-selection benchmark over the 2-data-qubit setting. To defend against parameter-selection bias, we additionally evaluate a single train-selected continuous parameter tuple on held-out seeds. To defend against metric-only collapse, we compare distance improvement with diversity retention and success probability. As a hardware-motivated extension, we test a 1-data-qubit + 1-auxiliary-qubit hybrid random-unitary/Hamiltonian-inspired toy. These are small state-vector benchmarks/probes, not hardware advantage or broad quantum advantage.

## Next Human Step

김건우는 Hamiltonian/projection/post-selection 물리 해석 문장을 검수한다. 임채진은 위 hierarchy를 보고서/발표 흐름에 반영한다. 지후는 이 source/test harvest를 커밋한 뒤 Problem 3 final notebook/report에 숫자를 옮긴다.

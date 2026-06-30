# Overnight Problem 3 Evidence Handoff

이 문서는 6/29 밤부터 6/30 아침까지 한지후 메인 자동화와 김승빈 support worker가 만든 Problem 3 실험 근거를 처음 보는 팀원이 바로 이해하도록 정리한 핸드오프 문서다.

## 한 줄 결론

Problem 3는 더 오래 돌려서 새 아이디어를 계속 찾는 단계가 아니라, 이미 얻은 근거를 보고서와 발표에 정확히 옮기는 수확 단계로 전환한다. 최종 주장은 "continuous measurement-basis post-selection이 작은 state-vector denoising proxy에서 20개 seed에 대해 재현 가능하게 metric을 개선했다"로 제한한다.

Hardware advantage, general quantum advantage, full trainable QuDDPM reverse process라고 말하지 않는다.

## 왜 밤새 자동화를 돌렸나

3번 문제는 반쯤 자유주제라 단일 실행 결과만으로는 심사위원에게 설득력이 약하다. 그래서 밤새 자동화의 목표를 다음 네 가지로 잡았다.

1. 같은 결과가 seed를 바꿔도 반복되는지 확인한다.
2. axis-only projection보다 continuous basis search가 얼마나 나은지 비교한다.
3. metric만 좋아지고 ensemble이 collapse되는 나쁜 후보를 걸러낸다.
4. 2-qubit hardware-compatible hybrid toy가 보조 확장 아이디어로 쓸 수 있는지 확인한다.

즉, 자동화의 목적은 "아무 실험이나 많이 돌리기"가 아니라 `실험 -> 분석 -> 판단 -> 방어 근거 생성 -> 수확`이었다.

## 누가 무엇을 돌렸나

| Runner | Role | What it did | Evidence use |
| --- | --- | --- | --- |
| 한지후 메인 자동화 | 전략/코드 owner | finalist autopilot, seed sweep, frozen holdout, collapse-defense, hybrid toy 검증 | 최종 보고서의 main hierarchy와 claim 기준 |
| 김승빈 support worker | 독립 재현/ablation worker | 별도 컴퓨터에서 28 cycles, 14번의 20-seed sweep, 252개 이상 hybrid toy run | main 결과의 재현성 및 보조 ablation 근거 |

한지후 쪽은 cycle 60까지를 신뢰 가능한 완료 근거로 사용한다. cycle 62는 실행 중 수동 중단했으므로 evidence로 쓰지 않는다.

김승빈 쪽은 cycle 28까지 완료된 결과를 사용한다. cycle 29 이후 시작된 작업은 이 문서의 evidence에 포함하지 않는다.

## 최종 Evidence Hierarchy

보고서와 발표에서는 아래 순서로 제시한다.

1. Main quantitative result
   - 2-data-qubit continuous measurement-basis post-selection benchmark.
   - Problem 3의 중심 결과다.

2. Reproducibility evidence
   - 김승빈 support worker가 별도 컴퓨터에서 같은 20-seed gate를 반복 재현했다.
   - "한 번 운 좋게 나온 결과"가 아니라는 방어 근거다.

3. Frozen-parameter holdout
   - train seeds `1..10`에서 고른 하나의 `(tau, theta, phi)`를 holdout seeds `11..20`에 그대로 적용했다.
   - seed마다 parameter를 cherry-pick했다는 의심을 줄인다.

4. Baseline/collapse-defense table
   - identity, best exact `Z/X/Y`, continuous post-selection, diagnostic collapse-to-centroid를 같은 표에 둔다.
   - MMD/Wasserstein만 낮아지는 collapse를 좋은 denoising으로 착각하지 않도록 방어한다.

5. Hybrid 2-qubit extension
   - `1 data qubit + 1 auxiliary qubit` toy.
   - IBM-style two-qubit circuit으로 옮길 수 있다는 plausibility evidence다.
   - main result가 아니라 front-facing extension으로 둔다.

## 핵심 숫자

### Main 20-Seed Gate

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

해석: 20개 seed 전체에서 main candidate로 쓸 수 있는 수준의 안정성은 있다. 다만 axis-only 대비 margin은 작으므로 "압도적 우위"라고 말하지 않는다.

### 김승빈 Support Worker

| Item | Value |
| --- | --- |
| Completed cycles used | `1..28` |
| Full 20-seed sweeps | `14` |
| Hybrid toy runs | at least `252` |
| Latest full sweep decision | `use_as_main` |
| Latest sweep passing seeds | `20 / 20` |
| Latest sweep median MMD improvement | `0.097056` |
| Latest sweep median Wasserstein improvement | `0.147983` |

해석: 별도 컴퓨터에서 반복 실행해도 main 20-seed gate가 유지됐다. 이 결과는 재현성 근거로 쓴다.

### Frozen-Parameter Holdout

| Metric | Value |
| --- | --- |
| Frozen tuple `(tau, theta, phi)` | `(1.794737, 1.832596, 3.141593)` |
| Holdout rows | `60` |
| Positive-improvement holdout rows | `60 / 60` |
| Median fixed-parameter MMD improvement | `0.073421` |
| Median fixed-parameter Wasserstein improvement | `0.136641` |
| Median fixed-parameter diversity retention | `0.790676` |
| Median fixed-parameter success probability | `0.477322` |

해석: 매 seed마다 parameter를 새로 고른 oracle grid-best보다 약하지만, 하나의 train-selected parameter도 holdout에서 작동한다. 이것이 더 정직한 방어 근거다.

### Collapse-Defense Table

| Method | Positive rows | Median MMD improvement | Median Wasserstein improvement | Median diversity retention |
| --- | --- | --- | --- | --- |
| Identity/no-denoising | `0 / 120` | `0.000000` | `0.000000` | `1.000000` |
| Best exact `Z/X/Y` axis projection | `120 / 120` | `0.086055` | `0.142594` | `0.810592` |
| Continuous post-selection | `120 / 120` | `0.097056` | `0.147983` | `0.823217` |
| Diagnostic collapse-to-centroid | `120 / 120` | `0.859292` | `0.714276` | `0.000000` |

해석: collapse-to-centroid는 MMD/Wasserstein만 보면 매우 좋아 보이지만 diversity가 완전히 무너진다. 그래서 최종 보고서에서는 MMD/Wasserstein과 함께 diversity retention, success probability를 반드시 같이 보여준다.

### Hybrid 2-Qubit Extension

| Metric | Value |
| --- | --- |
| Toy size | `1 data qubit + 1 auxiliary qubit` |
| Positive-improvement rows | `4 / 4` |
| Median MMD improvement | `0.211078` |
| Median Wasserstein improvement | `0.223252` |
| Median diversity retention | `0.573138` |
| Median success probability | `0.505744` |
| Decision | `front_facing_extension` |

해석: 가장 눈에 띄는 확장 아이디어로 쓸 수 있다. 하지만 seed robustness가 main result만큼 강하게 정리된 것은 아니므로 본론의 중심이 아니라 보조 extension으로 둔다.

## 최종 보고서에 넣을 주장

아래 문장을 기준으로 보고서와 발표 문장을 맞춘다.

> We present Problem 3 as a recoverability-aware quantum diffusion benchmark. In small state-vector experiments, continuous measurement-basis post-selection reproducibly improves MMD and Wasserstein-type metrics across 20 seeds. We report diversity retention and post-selection success probability together with distance improvement to avoid metric-only collapse. A frozen-parameter holdout and an independent support-worker rerun support reproducibility. A 1-data-qubit + 1-auxiliary-qubit hybrid toy is included as a hardware-motivated extension, not as hardware advantage.

한국어로는 다음처럼 말하면 된다.

> 우리는 3번을 recoverability-aware quantum diffusion benchmark로 정리한다. 작은 state-vector 실험에서 continuous measurement-basis post-selection은 20개 seed 전반에서 MMD와 Wasserstein-type metric을 안정적으로 개선했다. 단, metric만 개선되는 collapse를 피하기 위해 diversity retention과 post-selection success probability를 함께 보고한다. Frozen-parameter holdout과 승빈의 독립 support worker 반복 실행으로 재현성을 보강했고, 2-qubit hybrid toy는 hardware-motivated extension으로만 제시한다.

## 쓰면 안 되는 주장

- "양자 우위가 입증됐다."
- "실제 IBM hardware에서 우위가 났다."
- "continuous basis가 모든 경우 axis-only보다 압도적으로 좋다."
- "완전한 trainable QuDDPM reverse process를 구현했다."
- "MMD/Wasserstein만 낮아졌으므로 denoising이 성공했다."

## 어디를 보면 되나

| Purpose | File |
| --- | --- |
| 메인 수확 요약 | `docs/21_problem_3_harvest_summary.md` |
| 승빈 support worker 결과 | `docs/experiments/2026-06-30_problem_3_seungbin_support_worker_results.md` |
| 이 문서 | `docs/22_overnight_problem_3_evidence_handoff.md` |
| 승빈 최신 status | `results/problem_3_support_worker/seungbin/latest_status.md` |
| 승빈 cycle log | `results/problem_3_support_worker/seungbin/progress_log.md` |
| 한지후 main seed sweep | `results/problem_3_seed_sweep/seed_sweep_summary.md` |
| Frozen holdout | `results/problem_3_frozen_parameter_holdout/frozen_holdout_summary.md` |
| Collapse-defense | `results/problem_3_baseline_collapse_defense/baseline_collapse_summary.md` |

## 다음 행동

| Owner | Next action |
| --- | --- |
| 한지후 | 최종 notebook/report에 위 hierarchy와 숫자를 반영한다. |
| 김승빈 | support worker 결과에서 figure/table 후보를 고르고, 재현 로그 위치를 발표자료에 연결한다. |
| 김건우 | Hamiltonian/projection/post-selection 해석 문장과 "왜 auxiliary qubit post-selection이 조건부 상태를 만든다"는 설명을 검수한다. |
| 임채진 | Problem 1/2 정성 설명과 Problem 3 limitation을 보고서 흐름에 자연스럽게 배치한다. |


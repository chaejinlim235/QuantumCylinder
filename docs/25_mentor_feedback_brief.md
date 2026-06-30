# Mentor Feedback Brief

기준 시각: `2026-06-30 16:30 KST`

이 문서는 멘토 연구원/교수님께 현재 결과물을 짧게 설명하고, 3-b 분석에서 3-c 후보가 자연스럽게 도출되는지 검수받기 위한 5분 브리프이다.

## 한 문장 요약

3-b에서는 measurement-basis control이 거리 개선, diversity retention, post-selection success probability 사이에 어떤 trade-off를 만드는지 분석했고, 3-c에서는 그 분석을 바탕으로 더 강하지만 더 비용이 큰 two-way projected denoising을 main 개선안으로 제안했다.

## 현재 전략

1. Problem 1은 `|00>` 주변 target ensemble과 random-unitary forward diffusion을 재현한다.
2. Problem 2는 2-data-qubit system에 complement qubit을 붙이고 fixed Hamiltonian evolution 뒤 projection하는 diffusion proxy를 재현한다.
3. Problem 3(b)는 `axis-only baseline`과 `continuous measurement-basis control`을 비교해 recoverability trade-off를 분석한다.
4. Problem 3(c) 본문 main은 3-b에서 얻은 분석을 바탕으로 `Hamiltonian two-way post-selection`을 제안한다.
5. Hamiltonian + random final kick, hybrid 1M+1F toy, target-aware actor-critic은 appendix/ablation/extension으로 제한한다.
6. hardware advantage 또는 general quantum advantage는 주장하지 않는다. small-scale state-vector benchmark/probe로 제한한다.

## 용어 정리

`axis-only projection`과 `continuous measurement-basis post-selection`은 3-c에서 우리가 새로 제안하는 최종 개선안처럼 말하지 않는다.

- `axis-only projection`: `Z/X/Y` 축 측정만 허용했을 때의 discrete baseline이다.
- `continuous measurement-basis post-selection`: 3-b에서 projection basis와 denoising time을 통제 변수로 바꾸기 위한 실험 장치다.
- 도입 이유: 3-b에서 "조작 가능한 reverse setting이 어떤 trade-off를 만드는가"를 보려면 discrete baseline과 continuous control을 함께 비교해야 한다.

## 3-b 고정 수치와 해석

| Metric | Value | 해석 |
| --- | ---: | --- |
| use_as_main seeds | `20 / 20` | seed를 바꿔도 효과가 유지된다. |
| median MMD improvement | `0.097056` | target ensemble 쪽으로 거리 감소가 있다. |
| median Wasserstein improvement | `0.147983` | sample matching 관점에서도 개선이 있다. |
| median diversity retention | `0.823217` | 단순 collapse로만 생긴 개선은 아니다. |
| median success probability | `0.468122` | near-zero rare event는 아니지만 post-selection 비용은 존재한다. |
| median axis-only score margin | `0.010000` | continuous control의 추가 이득은 작다. |
| nonpositive axis-margin rows | `18 / 120` | 일부 row에서는 axis-only와 비슷하거나 더 약하다. |

3-b 결론:

> Continuous basis control은 재현 가능한 거리 개선을 만들지만, axis-only baseline 대비 압도적 우위는 아니다. 따라서 3-c는 continuous search를 더 강조하는 섹션이 아니라, 거리 개선과 성공확률, 다양성 보존 사이의 trade-off를 어떻게 개선할지 제안하는 섹션으로 써야 한다.

## 3-c main과 appendix 후보

| 3-b 관찰 | 보고서 위치 | 후보 | 제안 이유 | 현재 해석 |
| --- | --- | --- | --- | --- |
| 강한 post-selection은 더 큰 distance gain과 더 낮은 success probability를 만들 수 있다. | 본문 main | Hamiltonian two-way post-selection | post-selection을 한 단계 더 적용하면 거리 개선이 커지는지 확인한다. | 개선은 커지지만 success probability가 낮아지는 analysis-guided improvement |
| 강한 조작이 항상 좋은지 불명확하다. | appendix/ablation | Hamiltonian + random final kick | post-selection 뒤 작은 random correction이 도움이 되는지 본다. | MMD는 아주 조금 개선, Wasserstein은 약간 악화되는 ablation |
| state-vector 결과를 회로 관점으로 설명하기 어렵다. | appendix/extension | hybrid 1M+1F toy | 보조 큐빗 측정 구조를 가장 작은 회로로 보여준다. | main 2-qubit 결과와 직접 우열 비교하지 않는 extension |
| target prior를 사용할 수 있으면 control을 더 잘 고를 수 있는가? | appendix/upper bound | target-aware actor-critic | reward에 target ensemble을 넣고 filter strength를 고른다. | unknown-target denoiser가 아니라 target-aware 후보 |

## 3(c) Hamiltonian variants

`5 seeds x 3 input steps = 15 rows`

| Method | Median MMD improvement | Median Wasserstein improvement | Median diversity retention | Median success probability | 해석 |
| --- | ---: | ---: | ---: | ---: | --- |
| continuous reference | 0.056388 | 0.120620 | 0.848836 | 0.467554 | 3-b reference |
| Hamiltonian + random final kick | 0.056695 | 0.119401 | 0.848403 | 0.467554 | mixture ablation |
| Hamiltonian two-way post-selection | 0.101374 | 0.136426 | 0.829273 | 0.227065 | 거리 개선 vs 성공확률 감소 trade-off |

## 안전한 설명 문장

> 3-b의 핵심은 continuous basis가 압도적으로 좋다는 것이 아니라, post-selected reverse map에서 거리 개선, diversity retention, success probability를 함께 봐야 한다는 점이다.

> 3-c에서는 이 trade-off를 바탕으로 더 강하지만 더 비용이 큰 two-way Hamiltonian post-selection을 본문 main 개선안으로 제안한다. 이 방법은 거리 개선을 키우는 대신 성공확률을 낮추는지를 확인하는 작은 예제다. Hamiltonian + random final kick은 ablation, hybrid 1M+1F toy는 회로 수준 설명용 extension, actor-critic은 target-aware 조건에서만 쓰는 policy-search appendix 후보다.

> 전체 `M+F` system은 unitary하게 진화하지만, complement qubit `F`를 특정 측정 기저로 측정하고 원하는 결과만 post-selection하면 data system `M`에는 effective non-unitary map이 작용한다. 이 map이 random-unitary로 흐트러진 ensemble을 target ensemble 쪽으로 당기는지 작은 state-vector 실험에서 비교했다.

## 멘토에게 물어볼 질문

1. 3-b를 "continuous basis의 우월성"이 아니라 recoverability trade-off 분석으로 설명하는 방향이 문제 의도에 맞는가?
2. `axis-only projection`을 discrete baseline, `continuous post-selection`을 3-b control variable로 설명하면 충분히 자연스러운가?
3. 3-c main을 Hamiltonian two-way post-selection으로 좁히고 나머지를 appendix/ablation으로 내리는 현재 스토리라인이 설득력 있는가?
4. Hamiltonian two-way를 "거리 개선은 커지지만 success probability가 낮아지는 trade-off 후보"로 설명해도 물리적으로 괜찮은가?
5. hybrid 1M+1F toy와 actor-critic을 각각 본문/appendix 중 어디에 두는 것이 적절한가?
6. 현재 보고서에서 과장된 quantum advantage 주장처럼 보일 수 있는 문장이 있는가?

## 보여줄 파일

- 3-b to 3-c storyline: `docs/26_problem_3b_to_3c_storyline.md`
- measurement-basis explainer: `docs/problem3_measurement_basis_explainer.md`
- two-way main 및 appendix row 문서: `docs/24_problem_3_method_portfolio.md`
- 최종 notebook 사본: `C:\Users\sky_m\Downloads\QuantumCylinder_final_submission_report_problem3c_variants_v5.ipynb`
- method portfolio figure: `results/problem_3_method_portfolio/method_portfolio_summary.png`
- Hamiltonian variants figure: `results/problem_3_hamiltonian_variants/hamiltonian_variant_summary.png`

## 말할 때 피해야 할 표현

- "양자 우위가 있다"
- "항상 axis-only보다 좋다"
- "axis-only가 우리가 제안한 후보 방법이다"
- "continuous post-selection이 3-c의 새 최종 개선안이다"
- "3-c가 후보 포트폴리오 나열이다"
- "actor-critic이 최종 방법이다"
- "success probability가 높다"
- "실제 하드웨어에서 우월하다"

대신 다음처럼 말한다.

> 3-b에서 continuous measurement-basis control은 재현 가능한 거리 개선을 보였지만 axis-only 대비 margin은 작았다. 그래서 3-c는 이 trade-off를 바탕으로 two-way projected denoising을 main 개선안으로 제안하고, 더 큰 거리 개선과 낮아진 success probability를 함께 보여준다.

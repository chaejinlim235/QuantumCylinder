# Mentor Feedback Brief

기준 시각: `2026-06-30 16:30 KST`

이 문서는 멘토 연구원/교수님께 현재 결과물을 짧게 설명하고, 물리적 claim 강도와 최종 제출 방향을 검수받기 위한 5분 브리프이다.

## 한 문장 요약

우리는 random-unitary 또는 Hamiltonian projected diffusion으로 흐트러진 작은 양자 state ensemble을, 보조 큐빗 측정과 post-selection이 유도하는 effective non-unitary map으로 얼마나 복원할 수 있는지 MMD, Wasserstein-type distance, diversity retention, success probability로 함께 평가했다.

## 현재 전략

1. Problem 1은 `|00>` 주변 target ensemble과 random-unitary forward diffusion을 재현한다.
2. Problem 2는 2-data-qubit system에 complement qubit을 붙이고 fixed Hamiltonian evolution 뒤 projection하는 diffusion proxy를 재현한다.
3. Problem 3(a/b)의 main result는 `continuous measurement-basis post-selection`이다.
4. Problem 3(c)는 한 방법만 주장하지 않고 후보 포트폴리오로 제시한다.
   - Hamiltonian + random final kick
   - Hamiltonian two-way post-selection
   - hybrid 1M+1F toy
   - target-aware actor-critic
5. hardware advantage 또는 general quantum advantage는 주장하지 않는다. small-scale state-vector benchmark로 제한한다.

## 고정 수치

### 20-seed main gate

- recommendation: `use_as_main`
- use_as_main seeds: `20 / 20`
- median MMD improvement: `0.097056`
- median Wasserstein improvement: `0.147983`
- median diversity retention: `0.823217`
- median success probability: `0.468122`
- median axis-only score margin: `0.010000`

### 3(c) Hamiltonian variants

`5 seeds x 3 input steps = 15 rows`

| Method | Median MMD improvement | Median Wasserstein improvement | Median diversity retention | Median success probability | 해석 |
| --- | ---: | ---: | ---: | ---: | --- |
| continuous reference | 0.056388 | 0.120620 | 0.848836 | 0.467554 | 3(a/b 기준 후보 |
| Hamiltonian + random final kick | 0.056695 | 0.119401 | 0.848403 | 0.467554 | mixture ablation 후보 |
| Hamiltonian two-way post-selection | 0.101374 | 0.136426 | 0.829273 | 0.227065 | 거리 개선 vs 성공확률 감소 trade-off 후보 |

## 안전한 설명 문장

> 전체 `M+F` system은 unitary하게 진화하지만, complement qubit `F`를 특정 측정 기저로 측정하고 원하는 결과만 post-selection하면 data system `M`에는 effective non-unitary map이 작용한다. 이 map이 random-unitary로 흐트러진 ensemble을 target ensemble 쪽으로 당기는지 작은 state-vector 실험에서 비교했다.

> Hamiltonian two-way post-selection은 거리 지표를 가장 크게 개선했지만, 두 번의 post-selection을 거치므로 success probability가 낮아졌다. 따라서 최종 main result가 아니라 Problem 3(c)의 trade-off 후보로 제시한다.

> Actor-critic은 raw target ensemble을 reward에 사용하므로, unknown-target 일반 denoiser가 아니라 target-aware policy search 후보로만 주장한다.

## 멘토에게 물어볼 질문

1. Problem 3의 main claim을 continuous measurement-basis post-selection으로 두는 것이 문제 조건에 맞고 안전한가?
2. Hamiltonian two-way를 “거리 개선은 커지지만 success probability가 낮아지는 trade-off 후보”로 설명해도 물리적으로 괜찮은가?
3. Hamiltonian + random final kick을 main result가 아니라 ablation 후보로 두는 판단이 적절한가?
4. hybrid 1M+1F toy와 actor-critic을 각각 어느 정도까지 본문에 넣고, 어느 정도를 appendix/후보로 제한해야 하는가?
5. 현재 보고서에서 과장된 quantum advantage 주장처럼 보일 수 있는 문장이 있는가?
6. 심사위원에게 가장 설득력 있는 figure/table은 무엇인가?

## 보여줄 파일

- 최종 notebook 사본: `C:\Users\sky_m\Downloads\QuantumCylinder_final_submission_report_problem3c_variants_v5.ipynb`
- 후보 포트폴리오 문서: `docs/24_problem_3_method_portfolio.md`
- method portfolio figure: `results/problem_3_method_portfolio/method_portfolio_summary.png`
- Hamiltonian variants figure: `results/problem_3_hamiltonian_variants/hamiltonian_variant_summary.png`

## 말할 때 피해야 할 표현

- “양자 우위가 있다”
- “항상 axis-only보다 좋다”
- “actor-critic이 최종 방법이다”
- “success probability가 높다”
- “실제 하드웨어에서 우월하다”

대신 다음처럼 말한다.

> 작은 state-vector 실험에서 여러 reverse/denoising 후보를 같은 recoverability-aware metric으로 비교했고, 그중 continuous post-selection을 main result로, Hamiltonian two-way와 actor-critic 등을 3(c)의 확장 후보로 제시한다.

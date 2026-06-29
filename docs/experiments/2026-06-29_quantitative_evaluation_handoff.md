# Quantitative Evaluation Handoff

Owner: 한지후
Reviewers: 김건우, 임채진, 김승빈

이 문서는 팀원이 현재 정량 평가 산출물을 바로 확인하기 위한 handoff 문서다. 최종 보고서나 발표자료가 아니라, 마지막 제출 전까지 검토할 evidence index 역할을 한다.

## 실행 명령

```powershell
python scripts/run_quantitative_evaluation.py
python -m pytest --basetemp .pytest_tmp_urgent_quant
```

최근 확인 결과:

- quantitative evaluation 실행: 통과
- pytest: `16 passed`

## 핵심 산출물

`results/` 아래 파일은 Git에 커밋하지 않는다. 팀원은 위 명령으로 같은 파일을 재생성한다.

| Purpose | Generated file |
| --- | --- |
| 전체 index | `results/quantitative_evaluation/QUANTITATIVE_EVALUATION_INDEX.md` |
| Problem 1(b) metric sanity | `results/quantitative_evaluation/problem_1b_metric_diagnostics.md` |
| Problem 2(a) Hamiltonian term check | `results/quantitative_evaluation/problem_2a_hamiltonian_diagnostics.md` |
| Problem 2(b) projection probability check | `results/quantitative_evaluation/problem_2b_projection_diagnostics.md` |
| Problem 2(c) reduced Bloch figure, qubit 0 | `results/quantitative_evaluation/problem_2c_bloch_qubit_0.png` |
| Problem 2(c) reduced Bloch figure, qubit 1 | `results/quantitative_evaluation/problem_2c_bloch_qubit_1.png` |
| Problem 2(d) resource comparison | `results/quantitative_evaluation/problem_1_2_baseline/comparable_strength_resource_matches.csv` |

## 현재 수치

Problem 1(b) metric sanity:

- mean fidelity from `S0` to `|00>`: `0.995692`
- min fidelity from `S0` to `|00>`: `0.972637`
- `MMD(S0, S0)`: `0.000000000000`
- `Wasserstein(S0, S0)`: `0.000000000000`
- `MMD(S1_random_unitary, S0)`: `0.882606`
- `Wasserstein(S1_random_unitary, S0)`: `0.733305`

Problem 2(a) Hamiltonian diagnostics:

- qubit order: `M0, M1, F`
- Pauli terms: `XII`, `YII`, `IXI`, `IYI`, `IIX`, `IIY`, `XXI`, `IXX`
- matrix shape: `8 x 8`
- Hermiticity error: `0.000000000000`

Problem 2(b) projection diagnostics at `t = 1.0`, `Z` basis:

- mean `P(outcome 0)`: `0.157683`
- mean `P(outcome 1)`: `0.842317`
- max normalization error: `0.000000000000`

Problem 3 seed sweep evidence:

- seed-level recommendation: `use_as_main`
- seeds: `20/20 use_as_main`
- main-candidate row fraction: `81/120 = 0.675`
- median MMD improvement: `0.097056`
- median Wasserstein improvement: `0.147983`
- median axis-only score margin: `0.010000`
- median diversity retention: `0.823217`
- median success probability: `0.468122`

## 팀원별 확인 요청

| Reviewer | Check |
| --- | --- |
| 김건우 | Problem 2(a)/(b) Hamiltonian term, qubit order, projection probability 해석 검증 |
| 임채진 | Problem 1(c), 2(c), 2(d)의 정성 설명이 문제 요구와 맞는지 확인 |
| 김승빈 | generated figure/table 경로를 재현하고 최종 패키징 후보로 정리 |
| 한지후 | 자동화 재실행, PR/check 관리, claim 과장 여부 gatekeeping |

## 안전한 주장 범위

- Problem 1 target ensemble은 `|00>` 주변 cluster로 생성되었고, metric self-check는 0 distance를 반환한다.
- 현재 random-unitary baseline은 strong-scrambling baseline이므로, "느린 점진적 diffusion"처럼 과장하지 않는다.
- Problem 2 Hamiltonian projected diffusion은 fixed-control alternative로 제시한다.
- Reduced Bloch plots는 2-qubit state 전체의 완전한 표현이 아니라 single-qubit marginal diagnostic이다.
- Problem 3는 small-scale, post-selected, state-vector toy proxy로 제한해 주장한다.

## GitHub issue handoff

관련 확인 요청은 GitHub issue 댓글로도 남겼다.

- #6 임채진: 보고서/발표용 정량 근거와 안전한 claim 문장 방향
- #8 김승빈: figure/table/result path 패키징 후보
- #19 김건우: Hamiltonian/projection/Bloch 해석 검증
- #31 한지후: 자동화 중 병렬 처리 완료 기록

# Problem 3 Two-Way Main and Appendix Rows

기준 시각: `2026-06-30`

## 핵심 변경

김건우 피드백을 반영해 3-b/3-c의 흐름을 다시 정리한다.

1. 3-b는 숫자 표가 아니라 분석 섹션으로 쓴다.
2. 3-c는 기존 방향의 연장이 아니라, 3-b에서 얻은 분석을 바탕으로 새 후보를 제안하는 섹션으로 쓴다.
3. `axis-only projection`은 우리가 제안한 방법이 아니라 discrete measurement baseline이다.
4. `continuous measurement-basis post-selection`은 3-b의 controlled modification을 분석하기 위한 주 실험 장치다.
5. 3-c 본문 main은 `Hamiltonian two-way post-selection`으로 둔다. 나머지 후보는 appendix/ablation으로 내린다.

상세 보고서 초안은 `docs/26_problem_3b_to_3c_storyline.md`를 기준으로 한다.

현재 최종 notebook 사본:

```text
C:\Users\sky_m\Downloads\QuantumCylinder_final_submission_report_problem3c_variants_v5.ipynb
```

## 3-b 분석 요약

| 관찰값 | 분석 포인트 | 보고서에서의 의미 |
| --- | --- | --- |
| `20 / 20` seeds가 `use_as_main` | seed를 바꿔도 효과가 유지된다. | 단일 seed 우연이 아니라 reproducible toy effect로 말할 수 있다. |
| median MMD improvement `0.097056`, median Wasserstein improvement `0.147983` | target ensemble 쪽으로 거리 감소가 있다. | reverse/denoising 방향의 신호는 있다. |
| median axis-only score margin `0.010000` | continuous basis가 axis-only보다 압도적으로 좋지는 않다. | "연속 기저가 항상 우월하다"가 아니라 "작지만 일관된 추가 control knob"로 제한한다. |
| nonpositive axis-margin rows `18 / 120` | 일부 input step에서는 best axis-only가 비슷하거나 더 낫다. | 3-c는 단순히 basis를 더 촘촘히 찾는 방향이 아니라 trade-off를 개선하는 방향이어야 한다. |
| median diversity retention `0.823217` | 거리 개선이 ensemble collapse만으로 생긴 것은 아니다. | MMD/Wasserstein만으로 평가하지 않는 이유를 만든다. |
| median success probability `0.468122` | post-selection 비용은 있지만 near-zero rare event는 아니다. | 3-c에서도 거리 개선과 성공확률을 같이 봐야 한다. |
| frozen holdout median MMD/W improvements `0.073421` / `0.136641` | train에서 고른 하나의 parameter도 holdout에서 작동한다. | 매 row마다 cherry-pick했다는 의심을 줄인다. |

3-b 결론:

> Continuous measurement-basis control은 작은 state-vector 실험에서 거리 지표를 일관되게 개선하지만, best axis-only baseline 대비 margin은 작다. 따라서 3-c는 "continuous가 더 좋다"를 반복하는 섹션이 아니라, 거리 개선, diversity 유지, post-selection 성공확률 사이의 trade-off를 어떻게 개선하거나 다르게 배치할 수 있는지를 제안하는 섹션이어야 한다.

## 왜 axis-only와 continuous를 쓰는가

`axis-only projection`과 `continuous measurement-basis post-selection`은 팀이 3-c에서 새로 내세우는 후보가 아니다.

- `axis-only projection`: `Z/X/Y` 축 측정만 허용했을 때의 discrete baseline이다. continuous control이 실제로 필요한지 확인하기 위한 기준선이다.
- `continuous measurement-basis post-selection`: 3-b에서 projection basis와 denoising time `tau`를 통제 변수로 바꾸기 위한 실험 장치다. 축 방향만 보는 대신 Bloch sphere 위의 `(theta, phi)`로 측정 기저를 확장한다.
- 도입 이유: 3-b의 목적은 "controlled modification이 어떤 trade-off를 만드는가"를 보는 것이므로, discrete baseline과 continuous control을 함께 놓아야 효과와 한계를 동시에 설명할 수 있다.

보고서에서는 이 둘을 "제안 후보"가 아니라 "3-b 분석을 가능하게 하는 기준선과 조작 변수"로 설명한다.

## 3-c Main 후보 도출

3-c의 질문은 다음으로 고정한다.

> 3-b에서 확인한 measurement-induced trade-off를 더 강하게 활용하면 distance gain을 키울 수 있는가? 그 대가는 success probability 감소인가?

| 3-b에서 드러난 병목 | 3-c에서의 위치 | 후보 | 제안 이유 | claim 범위 |
| --- | --- | --- | --- | --- |
| 강한 post-selection은 distance를 더 줄일 수 있지만 success probability를 희생한다. | 본문 main | Hamiltonian two-way post-selection | 같은 Hamiltonian/post-selection mechanism을 한 번 더 적용하면 거리 개선을 키울 수 있는지 확인한다. | 더 큰 distance gain, 더 낮은 success probability를 보여주는 analysis-guided improvement |
| 더 강한 조작이 항상 좋은지 불명확하다. | appendix/ablation | Hamiltonian + random final kick | Hamiltonian post-selection 뒤 작은 random-unitary correction을 붙이면 over-contraction을 완화하거나 추가 개선을 만들 수 있는지 본다. | main result가 아니라 mixture ablation |
| state-vector 결과를 회로 관점으로 설명하기 어렵다. | appendix/extension | hybrid 1M+1F toy | 보조 큐빗 측정과 post-selection 구조를 가장 작은 hardware-style circuit으로 보여준다. | 2-qubit main result와 직접 우열 비교하지 않는 plausibility extension |
| target 정보를 사용할 수 있다면 control을 더 잘 고를 수 있는가? | appendix/upper bound | target-aware actor-critic | target ensemble을 reward로 사용할 수 있는 조건에서 filter strength를 policy search로 고른다. | unknown-target denoiser가 아니라 target-aware toy improvement |

## 현재 고정된 Hamiltonian 후보 수치

아래 수치는 `python scripts/run_problem_3_hamiltonian_variant_candidates.py` 실행 결과이며, `5 seeds x 3 input steps = 15 rows` 요약이다.

| Method | Rows | Positive MMD rows | Positive Wasserstein rows | Median MMD improvement | Median Wasserstein improvement | Median diversity retention | Median success probability |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| continuous post-selection reference | 15 | 14 | 15 | 0.056388 | 0.120620 | 0.848836 | 0.467554 |
| Hamiltonian + random final kick | 15 | 15 | 15 | 0.056695 | 0.119401 | 0.848403 | 0.467554 |
| Hamiltonian two-way post-selection | 15 | 15 | 15 | 0.101374 | 0.136426 | 0.829273 | 0.227065 |

해석:

- `Hamiltonian two-way post-selection`은 거리 개선이 가장 크지만 success probability가 낮아진다. 이는 3-b에서 확인한 "거리 개선 vs post-selection 비용" trade-off를 가장 선명하게 활용하므로 3-c 본문 main으로 둔다.
- `Hamiltonian + random final kick`은 MMD는 reference보다 아주 조금 좋아졌지만 Wasserstein은 약간 낮아졌다. 따라서 main result가 아니라 "random correction이 언제 도움이 되는가"를 보는 appendix ablation으로 둔다.
- `continuous post-selection reference`는 3-c의 새 제안이 아니라 3-b 분석에서 이어지는 비교 기준이다.

## 최종 선택 규칙

- 3-b는 `axis-only baseline`과 `continuous basis control`을 통해 trade-off를 분석한다.
- 3-c 본문 main은 `Hamiltonian two-way post-selection`으로 둔다.
- actor-critic 수치가 좋아도 "최종 방법은 actor-critic 하나"라고 쓰지 않는다.
- `axis-only projection`은 후보가 아니라 baseline으로만 둔다.
- `continuous post-selection`은 3-b 분석 장치이자 reference로 둔다.
- Hamiltonian + random final kick, hybrid 1M+1F toy, target-aware actor-critic은 appendix/ablation/extension으로 내린다.

## 실행 명령

아래 명령은 이미 생성된 Problem 3 결과물을 읽어 two-way main과 appendix/ablation row를 비교하는 표와 그림을 만든다.

```powershell
python scripts/summarize_problem_3_method_portfolio.py
```

생성물:

- `results/problem_3_method_portfolio/method_portfolio_summary.md`
- `results/problem_3_method_portfolio/method_portfolio_summary.csv`
- `results/problem_3_method_portfolio/method_portfolio_summary.png`

`results/` 아래 생성물은 기본적으로 Git에 커밋하지 않는다.

## 보고서 문장

3-b:

> 3-b에서는 보조 큐빗 측정 기저를 discrete `Z/X/Y` 축 baseline과 continuous basis control로 나누어 비교했다. 20개 seed 전체에서 continuous control은 MMD와 Wasserstein-type distance를 안정적으로 줄였지만, best axis-only baseline 대비 median score margin은 `0.010000`으로 작고 `18 / 120` row에서는 margin이 양수가 아니었다. 따라서 이 결과는 continuous basis의 압도적 우월성이 아니라, 거리 개선, diversity retention, post-selection success probability를 함께 봐야 하는 recoverability trade-off를 보여준다.

3-c:

> 3-c에서는 3-b에서 관찰한 trade-off를 바탕으로, 더 강하지만 더 비용이 큰 projected denoising step인 two-way Hamiltonian post-selection을 제안한다. 이 방법은 measurement-induced non-unitary contraction을 두 번 적용해 더 큰 MMD/Wasserstein 개선을 만들지만, 두 번의 post-selection을 통과해야 하므로 success probability가 낮아진다. Hamiltonian + random final kick, hybrid 1M+1F toy, target-aware actor-critic은 본문 main이 아니라 appendix/ablation 후보로 제한한다.

## 팀원별 확인 포인트

| Member | 확인할 것 |
| --- | --- |
| 임채진 | 최종 ipynb에서 3-b 분석이 먼저 나오고 3-c main이 two-way projected denoising으로 도출되는지 확인 |
| 김승빈 | post-selection과 보조 큐빗 측정 해석, Hamiltonian two-way의 success probability trade-off 설명 검수 |
| 김건우 | axis-only/continuous가 제안 후보가 아니라 3-b baseline/control로 설명되는지, 후보별 코드와 metric 해석이 실제 구현과 맞는지 검수 |
| 한지후 | `summarize_problem_3_method_portfolio.py`, README, issue, notebook 사본 동기화 |

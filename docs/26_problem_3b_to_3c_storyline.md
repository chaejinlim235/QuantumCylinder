# Problem 3(b) to 3(c) Storyline

기준 시각: `2026-06-30`

이 문서는 팀원 피드백을 반영해 Problem 3의 본문 구조를 고정한다. 핵심은 3-b를 값 나열이 아니라 measurement-basis trade-off 분석으로 쓰고, 3-c main을 그 분석에서 나온 **two-way projected denoising**으로 좁히는 것이다.

별도 설명 자료: `docs/problem3_measurement_basis_explainer.md`

## Revised Frame

기존 프레임:

> continuous post-selection을 main result로 두고, 여러 3-c 후보를 포트폴리오로 보여준다.

수정 프레임:

> 3-b에서 measurement/projection이 만드는 denoising gain, success probability, diversity retention trade-off를 분석한다. 그 분석 결과, distance만 줄이는 것이 좋은 denoising은 아니라는 결론을 얻는다. 3-c에서는 이 결론을 바탕으로 더 강하지만 더 비용이 큰 **two-way projected denoising**을 제안하고 baseline과 비교한다.

## 3-b Title

보고서 제목은 다음처럼 둔다.

```text
3-b. Controlled modification: measurement basis controls the recoverability-success-diversity trade-off
```

한국어로는:

```text
3-b. 통제된 확장: 측정 basis가 복원성, 성공확률, diversity 사이의 trade-off를 어떻게 바꾸는가
```

## 3-b Opening

보고서 첫 문단 초안:

> Problem 2의 Hamiltonian projected diffusion에서는 Hamiltonian `H`를 고정하더라도 complement qubit `F`를 어떤 basis에서 측정하느냐에 따라 data system `M`에 작용하는 effective non-unitary map이 달라진다. 따라서 우리는 measurement basis를 controlled modification으로 선택하고, denoising gain, post-selection success probability, ensemble diversity retention 사이의 trade-off를 분석한다.

## Why Axis-Only and Continuous Appear

`axis-only projection`과 `continuous measurement-basis post-selection`은 3-c에서 우리가 새로 제안하는 최종 개선안이 아니다.

- `axis-only projection`: `Z/X/Y` Pauli measurement basis만 허용하는 discrete baseline이다. 가장 해석하기 쉬운 기준선으로, continuous control이 필요한지 판단하기 위해 사용한다.
- `continuous measurement-basis post-selection`: axis-only를 Bloch sphere 위의 일반 측정 방향 `(theta, phi)`로 확장한 3-b controlled modification이다.
- 도입 이유: complement qubit 측정과 post-selection은 data system에 effective non-unitary map을 만들고, measurement basis는 그 map의 방향과 강도를 바꾸는 control knob이다.

자세한 설명은 `docs/problem3_measurement_basis_explainer.md`를 사용한다.

## 3-b Experimental Table Shape

3-b 표는 raw MMD/W만 보여주지 않는다. 아래처럼 gain, success, diversity, interpretation을 같은 표에 둔다.

| Method | 역할 | MMD gain | W gain | Success prob. | Diversity retention | 해석 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Identity/no denoising | 기준점 | `0.000000` | `0.000000` | `1.000000` | `1.000000` | reverse 없음 |
| Best exact `Z/X/Y` axis projection | discrete baseline | `0.086055` | `0.142594` | `0.465058` | `0.810592` | 해석 가능한 Pauli baseline |
| Continuous basis post-selection | controlled extension | `0.097056` | `0.147983` | `0.468122` | `0.823217` | off-axis basis의 작은 개선 |
| Diagnostic collapse-to-centroid | 반례 | `0.859292` | `0.714276` | `1.000000` | `0.000000` | distance-only metric의 실패 사례 |

Two-way 후보는 3-c main에서 baseline과 비교한다. 3-b 표에 넣는다면 preview 또는 transition row로만 둔다.

## 3-b Observations

3-b의 핵심 관찰은 세 가지다.

1. **Distance improvement만으로는 좋은 denoising을 판단할 수 없다.** Diagnostic collapse row는 MMD/Wasserstein을 크게 줄이지만 diversity retention이 `0.000000`이므로 좋은 reverse process가 아니다.
2. **Measurement basis는 effective non-unitary map의 방향과 강도를 정하는 control knob이다.** 같은 Hamiltonian evolution을 쓰더라도 complement qubit을 어떤 basis에서 측정하느냐에 따라 data system에 남는 조건부 상태가 달라진다.
3. **좋은 후보는 가장 distance를 많이 줄이는 후보가 아니라 gain, success probability, diversity retention이 함께 납득되는 후보이다.** Continuous basis의 median axis-only margin은 `0.010000`으로 작고 `18 / 120` row에서 양수가 아니므로, continuous basis의 압도적 우월성을 주장하지 않는다.

## 3-b Conclusion

보고서 결론 문장:

> 3-b의 핵심 결과는 continuous basis가 axis-only보다 압도적으로 좋다는 것이 아니다. 실제로 axis-only 대비 margin은 작다. 더 중요한 관찰은 measurement basis가 data ensemble을 `S0` 쪽으로 수축시키는 effective non-unitary map을 조절하며, 이 과정에서 denoising gain, success probability, diversity retention 사이의 trade-off가 나타난다는 점이다.

## 3-c Title

3-c 제목은 다음처럼 둔다.

```text
3-c. Analysis-guided improvement: two-way projected denoising
```

한국어로는:

```text
3-c. 3-b 분석 기반 개선: two-way projected denoising
```

## 3-c Main Proposal

3-c main은 **Hamiltonian two-way post-selection**으로 둔다.

제안 이유:

- 3-b에서 measurement-induced non-unitary map이 denoising gain과 success probability 사이의 trade-off를 만든다는 것을 확인했다.
- 그렇다면 같은 projected denoising map을 한 번 더 적용하면 더 강한 denoising이 가능한지 테스트할 수 있다.
- 두 번의 post-selection을 통과해야 하므로 success probability는 낮아질 것으로 예상된다.
- 따라서 two-way post-selection은 3-b 분석에서 자연스럽게 나온 "stronger but more costly" 개선안이다.

## 3-c Result Table

| Method | Median MMD gain | Median W gain | Median success prob. | Median diversity retention | 3-c 해석 |
| --- | ---: | ---: | ---: | ---: | --- |
| One-way continuous reference | `0.056388` | `0.120620` | `0.467554` | `0.848836` | 3-b reference |
| Hamiltonian + random final kick | `0.056695` | `0.119401` | `0.467554` | `0.848403` | random correction은 안정적 개선 아님, appendix/ablation |
| **Two-way post-selection** | `0.101374` | `0.136426` | `0.227065` | `0.829273` | 더 강한 denoising, 더 큰 post-selection cost |
| Target-aware actor-critic | `0.359015` | `0.315669` | `0.387360` | `0.812548` | target-aware toy, 본문 main 아님 |

## 3-c Opening

보고서 문장 초안:

> Based on the trade-off observed in 3-b, we propose a stronger but more costly projected denoising step: two-way Hamiltonian post-selection. The idea is to apply the measurement-induced non-unitary contraction twice. This should increase recoverability, but it should also reduce the overall post-selection probability. We test this small example and compare it with the one-way continuous post-selection baseline.

한국어 버전:

> 3-b에서 관찰한 trade-off를 바탕으로, 3-c에서는 더 강하지만 더 비용이 큰 projected denoising step인 two-way Hamiltonian post-selection을 제안한다. 핵심 아이디어는 measurement-induced non-unitary contraction을 두 번 적용하는 것이다. 이 방법은 복원성을 높일 수 있지만, 두 번의 post-selection을 통과해야 하므로 전체 success probability를 낮출 것으로 예상된다. 우리는 이를 작은 예제로 테스트하고 one-way continuous post-selection baseline과 비교했다.

## Main Message

최종 3번 메시지는 다음으로 고정한다.

> 3-b에서 measurement basis가 projected denoising의 방향과 강도를 바꾸며, denoising gain, success probability, diversity retention 사이의 trade-off를 만든다는 것을 분석했다. 3-c에서는 이 분석을 바탕으로 더 강한 two-way post-selection을 제안했고, 더 큰 거리 개선을 얻는 대신 success probability를 희생한다는 점을 작은 예제로 확인했다.

## Appendix로 내릴 것

본문에서는 two-way projected denoising을 3-c main으로 둔다. 아래 항목은 appendix 또는 보조 ablation으로 둔다.

- actor-critic: raw target reward를 쓰는 target-aware toy improvement
- hybrid 1M+1F: circuit-visibility 또는 hardware-motivated plausibility extension
- Hamiltonian + random final kick: random correction ablation
- frozen-parameter holdout 상세
- 20-seed raw table 및 자동화/worker/cycle 기록

## 피해야 할 흐름

- 3-b의 숫자를 표로만 제시하고 분석 없이 3-c 후보로 넘어가지 않는다.
- `axis-only projection`을 우리가 새로 제안한 방법처럼 쓰지 않는다.
- `continuous post-selection`을 3-c의 새 개선안처럼 다시 포장하지 않는다.
- 3-c를 여러 후보 포트폴리오 나열로 끝내지 않는다.
- actor-critic을 본문 main처럼 설명하지 않는다.

# Problem 3 Measurement Basis Explainer

이 문서는 3-b에서 `axis-only projection`과 `continuous measurement-basis post-selection`을 왜 쓰는지 설명하기 위한 짧은 참고 자료다.

## Why Measurement Basis?

1. Problem 2의 projected ensemble은 data system `M`에 complement qubit `F`를 붙이고, 전체 `M+F` system을 Hamiltonian으로 unitary evolution한 뒤 `F`를 측정해 만든다.
2. 전체 `M+F` system은 unitary하게 진화하지만, `F`를 특정 basis에서 측정하고 원하는 outcome만 post-selection하면 data system `M`에는 effective non-unitary map이 작용한다.
3. 입력 state `|psi_i>`에 대해 이 조건부 상태는 다음처럼 쓸 수 있다.

```text
|phi_{i,m}(t,b)> =
  (I_M tensor <b_m|) exp(-i H t) (|psi_i>_M tensor |0>_F)
  / sqrt(p_{i,m})
```

```text
p_{i,m} =
  || (I_M tensor <b_m|) exp(-i H t) (|psi_i>_M tensor |0>_F) ||^2
```

4. 따라서 measurement basis를 바꾸면 data system에 남는 조건부 상태, 즉 effective non-unitary map의 방향과 강도가 바뀐다.
5. `axis-only projection`은 `Z/X/Y` Pauli measurement basis만 허용하는 discrete baseline이다. 이는 새 개선안이 아니라 가장 해석하기 쉬운 기준선이다.
6. `continuous measurement-basis post-selection`은 `Z/X/Y` 축에만 제한하지 않고, complement qubit 측정 방향을 Bloch sphere 위의 일반 basis `(theta, phi)`로 확장한 3-b controlled modification이다.
7. 따라서 3-b의 주장은 "continuous basis가 최고다"가 아니라, measurement basis가 denoising gain, post-selection success probability, diversity retention 사이의 trade-off를 만든다는 것이다.

## Axis-Only Baseline

Axis-only baseline은 다음 세 Pauli basis를 비교한다.

| Axis | Basis | 역할 |
| --- | --- | --- |
| `Z` | `|0>`, `|1>` | computational basis |
| `X` | `|+>`, `|->` | real superposition basis |
| `Y` | `|+i>`, `|-i>` | phase-sensitive basis |

보고서에서는 다음처럼 설명한다.

> Axis-only projection is not our proposed final improvement. It is a discrete Pauli-basis baseline used to test whether changing the complement measurement basis has any meaningful effect.

## Continuous Basis Control

일반적인 1-qubit measurement direction은 Bloch sphere 위의 두 각도 `(theta, phi)`로 나타낼 수 있다.

```text
|b0(theta, phi)> =
  cos(theta / 2) |0> + exp(i phi) sin(theta / 2) |1>
```

```text
|b1(theta, phi)> =
  sin(theta / 2) |0> - exp(i phi) cos(theta / 2) |1>
```

Continuous basis search는 새로운 물리 장치를 주장하는 것이 아니라, Pauli axis 밖의 off-axis measurement direction이 recoverability trade-off를 바꾸는지 확인하는 controlled probe다.

## Report Use

3-b에 넣을 핵심 문장:

> In Problem 3(b), we use the measurement basis as a controlled probe of the projected-ensemble mechanism. Changing the complement-qubit measurement basis changes the effective non-unitary map on the data system, so we compare axis-only Pauli measurements with continuous Bloch-sphere bases and analyze the trade-off among denoising gain, success probability, and diversity retention.

3-c로 이어지는 문장:

> Because 3-b shows that stronger projected denoising can improve distance metrics while increasing post-selection cost, 3-c proposes two-way projected denoising as an analysis-guided improvement.

# 실험 프로토콜

## 표준 설정

- ensemble size: `N=80`
- target width: `sigma=0.10`
- seed: 기본 `7`, 최종 결과는 `7, 11, 23` 반복 권장
- random-unitary diffusion: `12` steps
- Hamiltonian projected diffusion: `t in [0, 4]`, 13 points
- complement qubit initial state: `|0>`
- default projection basis: computational `Z` basis

## 표준 metric

- Fidelity matrix: `F_ij = |<psi_i|phi_j>|^2`
- MMD:

```text
MMD^2(X, Y) = mean K(X, X) + mean K(Y, Y) - 2 mean K(X, Y)
K = fidelity
```

- Wasserstein-type distance:

```text
cost(psi, phi) = 1 - F(psi, phi)
distance = minimum average matching cost for equal-size uniform ensembles
```

## Resource/control proxy

Random-unitary baseline:

- diffusion layers
- single-qubit random rotations
- 2-qubit entanglers
- random control parameters

Hamiltonian baseline:

- total evolution time
- fixed Hamiltonian parameter count
- projection basis count
- complement qubit count

3번 extension은 반드시 위 proxy 중 하나 이상을 baseline과 비교한다.

## 결과 저장 규칙

```text
results/
└── problem_1_2_baseline/
    ├── random_unitary_metrics.csv
    ├── hamiltonian_metrics.csv
    ├── resource_proxies.csv
    └── distance_curves.png
```

Git에는 결과 파일을 커밋하지 않는다. 보고서에 들어갈 최종 figure만 별도 논의 후 관리한다.

## 실험 로그 템플릿

`docs/experiments/YYYY-MM-DD_short_name.md` 형식으로 작성한다.

```markdown
# 실험명

Owner:
Reviewer:

## Hypothesis

## Setup

## Results

## Interpretation

## Next
```

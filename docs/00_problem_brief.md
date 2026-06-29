# 문제 브리프

## 한 줄 해석

1/2번은 재현 과제이고, 3번은 "확산 품질은 유지하면서 control/circuit overhead를 줄이는 작은 아이디어"를 보여주는 자유 연구 과제에 가깝다.

## 대회 문제 요구

### Problem 1: Random-unitary scrambling

- 2-qubit target ensemble `S0` 생성
- `N = 50-100`, 기본 `sigma = 0.10`
- pairwise similarity: pure-state fidelity `F(psi, phi) = |<psi|phi>|^2`
- 두 거리 계산:
  - fidelity-kernel MMD
  - cost `1 - F` 기반 Wasserstein-type distance
- random single-qubit rotations + 2-qubit entangler를 diffusion step마다 적용
- `dist(Sk, S0)`를 step `k`에 따라 plot

### Problem 2: Hamiltonian projected diffusion

- data system `M`: Problem 1의 2 qubits
- complement `F`: 1 qubit
- 3-qubit Hamiltonian:

```text
H = sum_j (hx X_j + hy Y_j) + J sum_j X_j X_{j+1}
hx = 0.8090, hy = 0.9045, J = 1.0
```

- 여러 evolution time `t`에서 complement qubit을 projection해 `M`의 ensemble 생성
- Problem 1과 같은 두 거리로 `dist(S_t^Ham, S0)` plot
- random-unitary diffusion과 diffusion behavior, fluctuation, saturation, resource/control cost를 비교

### Problem 3: Further extension

최소 요구는 다음 세 가지다.

- toy reverse/denoising step 하나를 보인다.
- diffusion setting을 통제된 방식으로 바꿔 trade-off를 분석한다.
- baseline 하나 이상과 비교되는 개선 아이디어를 제안하고 작은 예제로 검증한다.

## 숨은 채점 포인트로 보는 전략

- 구현량보다 "문제를 얼마나 정확히 해석했는가"가 중요하다.
- 논문 전체 재현보다 두 diffusion mechanism의 차이를 같은 metric, 같은 seed, 같은 ensemble에서 공정하게 비교해야 한다.
- 3번은 거창한 모델보다 작은 실험의 논리 밀도가 더 중요하다.
- 하드웨어 친화성은 depth, 2-qubit gate 수, random control 수, fixed Hamiltonian control, total evolution time처럼 proxy를 명확히 잡아야 한다.
- "좋아졌다"뿐 아니라 "무엇을 희생했는가"를 보여줘야 설득력이 생긴다.

## 권장 최종 스토리

1. `S0`는 `|00>` 주변의 작은 cluster다.
2. Random unitary는 빠르게 cluster를 깨고 Haar-like하게 퍼뜨리지만 step/layer control이 많다.
3. Hamiltonian projected diffusion은 fixed Hamiltonian 하나로 유사한 diffusion을 만들 수 있으나 time/basis에 따라 fluctuation과 saturation이 있다.
4. 우리 팀은 measurement basis, time schedule, shallow denoising map, 또는 noise-aware proxy를 조정해 같은 diffusion strength에서 resource-control trade-off를 개선한다.

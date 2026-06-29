# 3번 Extension 후보

## 추천 1: 동일 diffusion strength에서 resource 비교

아이디어:

- Random-unitary와 Hamiltonian diffusion의 MMD가 비슷해지는 지점을 맞춘다.
- 그 지점에서 layer 수, entangler 수, random control 수, Hamiltonian total time을 비교한다.

장점:

- 문제 2(d)와 직접 연결된다.
- 큰 trainable model 없이도 설득력 있는 trade-off 그림을 만들 수 있다.

한계:

- "개선"이라기보다는 비교 분석에 가깝다. 아래 후보 하나와 묶으면 좋다.

## 추천 2: Projection basis sweep

아이디어:

- Hamiltonian projected diffusion에서 complement qubit 측정 basis를 `Z`, `X`, `Y`로 바꾼다.
- 같은 time grid에서 MMD/Wasserstein curve의 fluctuation, saturation, diffusion speed를 비교한다.

왜 좋은가:

- 구현이 작다.
- Ref. [2]의 projected ensemble 철학과 맞다.
- 하드웨어에서는 측정 basis 변경이 전체 random circuit control보다 싸다는 논리를 만들 수 있다.

예상 주장:

- 특정 basis는 더 빠르게 ensemble을 퍼뜨리지만 fluctuation이 크다.
- 특정 basis는 diffusion이 느리지만 안정적이고 resource overhead가 작다.

## 추천 3: Shallow denoising filter

아이디어:

- diffused state에 `|00>` cluster 방향으로 당기는 고정 non-unitary filter를 적용한다.
- 예: computational basis amplitude 중 `|00>` 이외 성분을 factor `alpha < 1`로 줄이고 normalize한다.
- denoising 전후의 `dist(S, S0)` 감소량과 success probability proxy를 같이 보고한다.

왜 좋은가:

- Problem 3(a)의 toy reverse step을 깔끔하게 만족한다.
- 한지후의 loss/geometry 분석 역할과 잘 맞는다.

주의:

- 너무 강한 filter는 trivial하게 `|00>`로 collapse하므로, fidelity 회복량과 다양성 손실을 함께 보여야 한다.

## 추천 4: Noise-aware comparison

아이디어:

- Random-unitary 쪽은 layer마다 depolarizing-like state mixing을 추가한다.
- Hamiltonian 쪽은 evolution time에 비례한 damping proxy를 추가한다.
- ideal vs noisy에서 distance curve와 denoising 회복량을 비교한다.

왜 좋은가:

- 신청서에서 강조한 NISQ/hardware-efficient 관점과 잘 맞는다.
- 발표 때 "실제 하드웨어 제약을 생각했다"는 인상이 강하다.

주의:

- noise model이 너무 장난감처럼 보이면 역효과다. 작은 모델임을 명시하고 qualitative proxy로만 주장한다.

## 최종 추천 조합

가장 안전한 우승형 조합은 다음이다.

1. Problem 1/2 baseline을 정확히 재현한다.
2. 동일 MMD 지점에서 resource proxy를 비교한다.
3. Projection basis sweep으로 Hamiltonian diffusion의 control knob을 제안한다.
4. Shallow denoising filter로 toy reverse step을 보인다.

이 조합은 구현 난도가 낮고, 문제에서 요구한 세 축을 모두 건드린다: diffusion, reverse/denoise, hardware-efficient trade-off.

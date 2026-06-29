# 논문 해석 최소화 가이드

현재 목표는 논문을 깊게 해석하는 것이 아니라, 대회 문제 1/2를 빠르게 잠그고 Problem 3에서 검증 가능한 작은 주장을 만드는 것이다.

## 원칙

- 논문 전체를 처음부터 끝까지 읽지 않는다.
- 각 논문당 45분을 넘기지 않는다.
- 증명, full architecture, large-scale experiment detail은 읽지 않는다.
- 문제 PDF에 직접 필요한 정의, 그림, 실험 의도, 비교 논리만 가져온다.
- 모르는 물리 개념은 10분 이상 붙잡지 말고 issue comment나 팀 채팅에 질문으로 남긴다.

## 논문별 최소 목표

### Ref. [1] QuDDPM

읽는 목적:

- random-unitary scrambling이 forward diffusion 역할을 한다는 점만 이해한다.
- reverse process가 measurement/PQC로 denoising을 시도한다는 큰 구조만 이해한다.
- 우리 구현은 full QuDDPM 재현이 아니라 Problem 1의 simplified random-unitary trajectory임을 명시한다.

확인할 질문:

- forward scrambling에서 random unitary가 어떤 역할을 하는가?
- diffusion step이 커질수록 원래 ensemble cluster가 어떻게 무너지는가?
- full trainable reverse process를 구현하지 않아도 되는 이유를 어떻게 설명할 것인가?

읽지 않아도 되는 것:

- 전체 학습 pipeline 세부 구현
- 대규모 numerical experiment 재현
- 모든 ansatz/parameter update detail
- 복잡한 loss derivation

### Ref. [2] Chaotic Quantum Diffusion

읽는 목적:

- fixed Hamiltonian time evolution과 projected ensemble이 random circuit보다 hardware-control overhead가 작을 수 있다는 논리를 이해한다.
- Problem 2의 Hamiltonian과 projection 방식이 어떤 비교 포인트를 갖는지 정리한다.
- time, measurement basis, complement size가 diffusion behavior를 바꿀 수 있다는 정도만 잡는다.

확인할 질문:

- Hamiltonian projected diffusion이 random-unitary 방식과 비교해 어떤 control 구조를 갖는가?
- time을 바꿀 때 distance curve가 증가, 진동, 포화할 수 있다는 점을 어떻게 설명할 것인가?
- Problem 3에서 measurement basis sweep 또는 toy denoising이 왜 자연스러운 extension인가?

읽지 않아도 되는 것:

- chaotic dynamics의 엄밀한 이론
- large system scaling 실험
- 논문 전체 figure 재현
- hardware proposal의 세부 물리 구현

## 팀원별 읽기 범위

### 임채진

읽을 것:

- 각 논문의 abstract, introduction, main idea figure/caption
- random-unitary와 Hamiltonian 방식의 비교 문장

산출물:

- 발표용 문제 해석 3문장
- 두 방식의 차이 3문장
- limitation 2문장

### 김건우

읽을 것:

- Problem 1 random-unitary layer와 관련된 부분
- Problem 2 Hamiltonian/control structure와 관련된 부분

산출물:

- 우리 코드에서 선택한 rotation, entangler, step 수 설명
- Hamiltonian 방식의 fixed-control resource proxy 설명

### 김승빈

읽을 것:

- 논문 figure가 어떤 식으로 distance/quality를 보여주는지만 확인
- 실험 결과를 plot/table로 전달하는 방식 참고

산출물:

- Problem 1/2 baseline plot
- seed/config/result path 정리
- 발표에 쓸 figure caption 초안

### 한지후

읽을 것:

- fidelity, MMD, Wasserstein/infidelity cost와 연결되는 평가 방식
- reverse/denoising을 toy example로 축소할 수 있는 부분

산출물:

- metric sanity check
- 같은 diffusion strength 비교 기준
- toy denoising 또는 projection-basis sweep의 trade-off 해석

## 60분 운영안

1. 0-10분: 문제 PDF의 Problem 1/2/3 요구 다시 확인
2. 10-25분: Ref. [1] abstract, intro, relevant figure/caption만 확인
3. 25-40분: Ref. [2] abstract, intro, relevant figure/caption만 확인
4. 40-50분: 각자 자기 산출물에 필요한 문장 3개만 작성
5. 50-60분: 팀 전체 공유, 모르는 것은 질문 목록으로 분리

## 중단 기준

다음 중 하나라도 만족하면 논문 읽기를 멈추고 구현/실험으로 돌아간다.

- Problem 1/2 구현 선택을 설명할 수 있다.
- random-unitary와 Hamiltonian 방식의 resource/control 차이를 말할 수 있다.
- Problem 3 extension 후보 1개를 baseline과 같은 metric으로 비교할 수 있다.

## 팀에 공유할 한 줄

논문은 정답지가 아니라 방향 확인용이다. 지금은 논문을 많이 읽는 것보다, 문제 PDF 요구를 만족하는 baseline 결과와 작은 extension 비교를 제출 가능한 형태로 만드는 것이 더 중요하다.

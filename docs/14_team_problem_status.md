# 팀 공유용 문제 해결 현황

이 문서는 최종 제출 보고서나 발표자료가 아니다. 마지막 날에 보고서와 발표자료를 만들기 전까지, 팀원이 현재 코드가 문제 요구사항을 어디까지 만족하는지 빠르게 확인하고 코드 리뷰를 이어가기 위한 상태판이다.

작성 기준일: 2026-06-29

## 결론 요약

현재 코드는 Problem 1/2/3의 핵심 수치 실험을 실행할 수 있다. 하지만 코드 리뷰에서 지적된 것처럼, 채점자가 보거나 팀원이 검증할 수 있는 **관찰 가능한 출력**, **문제 소문항별 실행 경로**, **정성적 시각화**, **폴더 구조 설명**은 아직 부족하다.

따라서 다음 우선순위는 새 아이디어를 더 붙이는 것이 아니라 아래 네 가지를 채우는 것이다.

1. 각 소문항별로 "무엇을 입력했고 무엇이 나왔는지" 출력되는 실행 파일 또는 summary를 만든다.
2. Problem 1(c), 2(c), 2(d)에 필요한 정성 비교 그림을 추가한다.
3. 2-qubit state를 한 개의 Bloch sphere로 오해하지 않도록 reduced single-qubit Bloch vector 시각화로 설명한다.
4. `src/`와 `submission/`의 역할 차이를 문서와 파일명으로 명확히 한다.

## 코드 리뷰에 대한 현재 판단

| 리뷰 내용 | 판단 | 보강 방향 |
| --- | --- | --- |
| 1(a), 1(b), 1(c)가 return 중심이고 출력 확인이 부족함 | 맞는 지적 | `scripts/` 또는 `submission/` 실행 시 핵심 수치와 sample 상태를 사람이 읽을 수 있게 출력 |
| 2(a), 2(b)의 답을 얻는 코드가 직접 보이지 않음 | 부분적으로 맞는 지적 | Hamiltonian 생성과 projected ensemble 생성 함수는 있지만, 소문항별 diagnostic 출력이 부족 |
| 2(c), 2(d)는 정성 비교와 시각화가 필요함 | 맞는 지적 | distance curve 외에 reduced Bloch sphere/Pauli expectation plot 추가 |
| `src/` 코드가 흩어져 있고 2번이 (a), (b)로 분리되지 않음 | 맞는 지적 | 대회 중에는 대규모 이동보다 문서/entry point로 보완, 여유 있으면 `problem_2a_*`, `problem_2b_*` wrapper 추가 |
| `submission/`의 의미와 backend가 불명확함 | 최신 main에서는 일부 개선됨 | 현재 `submission/`은 독립 실행용 Qiskit layer로 정리됨. README와 이 문서에서 역할을 명확히 유지 |

## 현재 실행 명령

가장 빠른 전체 확인:

```powershell
python submission/run_all.py --quick
python -m pytest
```

심사위원 정량 평가용 진단 전체 실행:

```powershell
python scripts/run_quantitative_evaluation.py
```

Problem 1/2 baseline 전체 실행:

```powershell
python scripts/problem_1a_generate_target_ensemble.py
python scripts/run_problem_1_2_baselines.py
```

Problem 3 확인:

```powershell
python scripts/run_problem_3_continuous_denoising.py
```

결과 파일은 기본적으로 `results/` 아래에 생성되며 Git에는 커밋하지 않는다.

## 문제별 상태

### Problem 1(a): target ensemble 생성

문제 요구:

- `|00>` 주변의 2-qubit target ensemble `S0` 생성
- `N = 50-100`, `sigma = 0.10`
- `Rz(delta_z) Ry(delta_y)`를 각 qubit에 적용

현재 있는 코드:

- `src/quantum_cylinder/problem_1a_target_ensemble.py`
- `src/quantum_cylinder/implementations/qiskit/problem_1a_target_ensemble.py`
- `submission/states_and_metrics.py`
- `scripts/problem_1a_generate_target_ensemble.py`

현재 상태:

- Qiskit `QuantumCircuit` + `Statevector` 기반 생성 가능
- 기본 설정은 `N = 80`, `sigma = 0.10`, seed `7`
- `scripts/problem_1a_generate_target_ensemble.py`는 ensemble 크기와 첫 번째 상태 벡터를 출력함

부족한 점:

- "정말 `|00>` 주변 cluster인가?"를 보여주는 평균 fidelity, 분산, sample angle 통계가 부족함
- 최종 보고서 전까지는 첫 sample 출력보다 cluster 요약 수치가 더 필요함

보강 작업:

- `mean F(|psi_i>, |00>)`, min/max fidelity, angle standard deviation 출력
- 필요하면 reduced Bloch vector 평균을 함께 출력

### Problem 1(b): fidelity, MMD, Wasserstein-type distance

문제 요구:

- `F(psi, phi) = |<psi|phi>|^2`
- fidelity 기반 MMD 계산
- cost `1 - F` 기반 Wasserstein-type distance 계산

현재 있는 코드:

- `src/quantum_cylinder/problem_1b_ensemble_metrics.py`
- `submission/states_and_metrics.py`
- `scripts/run_problem_1_2_baselines.py`

현재 상태:

- metric 계산 함수는 구현되어 있음
- `run_problem_1_2_baselines.py` 실행 시 `random_unitary_metrics.csv`, `hamiltonian_metrics.csv`가 생성됨
- 테스트에서 baseline metric smoke check를 수행함

부족한 점:

- Problem 1(b)만 독립적으로 실행해 `MMD(S0, S0) ~= 0` 같은 sanity check를 보여주는 출력이 없음
- metric의 의미를 팀원이 바로 이해할 수 있는 예시 출력이 부족함

보강 작업:

- `scripts/problem_1b_check_metrics.py` 또는 기존 baseline script에 metric diagnostic section 추가
- 출력 예시:
  - `MMD(S0, S0)`
  - `Wasserstein(S0, S0)`
  - random scrambled ensemble과의 거리

### Problem 1(c): random-unitary forward diffusion

문제 요구:

- `S0 -> S1 -> ...` forward trajectory 구현
- random single-qubit rotations + 2-qubit entangler 사용
- 각 step `k`에서 `dist(Sk, S0)` plot
- cluster structure가 diffusion에 따라 어떻게 변하는지 설명

현재 있는 코드:

- `src/quantum_cylinder/problem_1c_random_unitary_diffusion.py`
- `src/quantum_cylinder/implementations/qiskit/problem_1c_random_unitary_diffusion.py`
- `submission/problem1_random_unitary_scrambling.py`
- `scripts/run_problem_1_2_baselines.py`

현재 상태:

- Qiskit `QuantumCircuit`, `Operator`, `Statevector`로 random layer 구현
- 각 layer는 양쪽 qubit에 random `RX/RY/RZ`를 적용하고 `CZ` entangler 1개를 사용
- `results/problem_1_2_baseline/distance_curves.png` 생성 가능
- 현재 reference run에서 random-unitary final step `k = 12`의 MMD는 약 `0.828`, Wasserstein-type distance는 약 `0.686`

부족한 점:

- 문제는 "cluster structure changes"라는 정성 설명을 요구하지만, 현재 문서의 설명은 너무 짧음
- 현재 angle scale이 `[-pi, pi]`라 첫 step부터 강하게 퍼지는 strong-scrambling baseline임. 이를 "점진적 확산"처럼 과장하면 안 됨

보강 작업:

- step별 reduced Bloch vector plot 추가
- 보고서용 해석 문장 초안:
  - "초기 `S0`는 `|00>` 주변의 좁은 cluster이지만, 첫 random-unitary layer 이후 fidelity 기반 거리가 급격히 증가한다."
  - "이 설정에서는 random rotation angle을 넓게 샘플링했기 때문에 diffusion은 느린 Gaussian broadening이라기보다 빠른 scrambling 후 saturation에 가깝다."
  - "이 선택은 Problem 2와 비교하기 위한 강한 baseline으로 사용한다."

### Problem 2(a): fixed Hamiltonian 구성

문제 요구:

- 2-qubit data system `M`에 complement qubit `F` 추가
- 3-qubit Hamiltonian
  `H = sum_j (hx X_j + hy Y_j) + J sum_j X_j X_{j+1}`
- `hx = 0.8090`, `hy = 0.9045`, `J = 1.0`

현재 있는 코드:

- `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py`
- `src/quantum_cylinder/implementations/qiskit/problem_2_hamiltonian_projected_diffusion.py`
- `submission/problem2_hamiltonian_projection.py`

현재 상태:

- Qiskit `SparsePauliOp`로 Hamiltonian term 8개 구성
- qubit order는 `M0, M1, F`로 둠
- matrix 변환 후 time evolution에 사용

부족한 점:

- Problem 2(a)만 실행해서 Hamiltonian term, coefficient, matrix shape를 출력하는 명령이 없음
- 팀원이 "2(a)의 답"을 코드에서 바로 보기 어렵다

보강 작업:

- `scripts/problem_2a_print_hamiltonian.py` 추가 또는 `submission/problem2_hamiltonian_projection.py --diagnostic` 추가
- 출력 예시:
  - Pauli terms: `XII`, `YII`, `IXI`, `IYI`, `IIX`, `IIY`, `XXI`, `IXX`
  - matrix shape: `8 x 8`
  - coefficients: `hx`, `hy`, `J`

### Problem 2(b): projected ensemble 생성

문제 요구:

- Hamiltonian time evolution 후 complement qubit projection
- 여러 evolution time `t`에 대해 `S_t^Ham` 생성

현재 있는 코드:

- `hamiltonian_projected_ensemble`
- `hamiltonian_projected_trajectory`
- `submission/problem2_hamiltonian_projection.py`

현재 상태:

- `M + F`를 evolve한 뒤 complement qubit을 `Z`, `X`, `Y` basis 중 하나로 projection 가능
- 기본은 `Z` basis
- projected output은 다시 2-qubit data ensemble이 됨

부족한 점:

- projection probability, sampled outcome 비율, projected state norm 같은 diagnostic 출력이 없음
- 문제의 projected-ensemble construction이 코드에서 눈에 잘 드러나지 않음

보강 작업:

- time 하나를 고정해 projection 전후 sample state, outcome probability 통계 출력
- `S_t^Ham`의 ensemble size가 `S0`와 같게 유지되는 이유를 문서에 명시

### Problem 2(c): qualitative diffusion comparison

문제 요구:

- `dist(S_t^Ham, S0)`를 `t`에 따라 plot
- Problem 1 random-unitary diffusion과 정성 비교
- 증가, fluctuation, saturation을 설명

현재 있는 코드:

- `scripts/run_problem_1_2_baselines.py`
- `results/problem_1_2_baseline/distance_curves.png`

현재 상태:

- random-unitary curve와 Hamiltonian projected curve를 같은 그림에 저장
- reference run에서 Hamiltonian MMD는 `t = 1.0` 근처에서 최대 약 `1.249`
- Hamiltonian Wasserstein-type distance는 `t = 4.0`에서 약 `0.884`

부족한 점:

- 정성 비교가 숫자와 plot만 있고, 사람이 보고 판단할 Bloch sphere 계열 시각화가 없음
- 2-qubit pure state 전체는 단일 Bloch sphere로 표현할 수 없으므로 주의가 필요함

보강 작업:

- 각 2-qubit state의 qubit별 reduced density matrix를 만들고, qubit 0/1 각각의 Bloch vector cloud를 그린다
- 최소 비교 대상:
  - `S0`
  - random-unitary `S1`, `S7`, `S12`
  - Hamiltonian `t = 0.333`, `t = 1.0`, `t = 4.0`
- 정성 판단:
  - random-unitary: 첫 layer 후 급격한 cluster 붕괴, 이후 비슷한 큰 거리에서 흔들림
  - Hamiltonian projected: time에 따라 거리 증가와 감소가 반복되며 fluctuation이 더 뚜렷함

### Problem 2(d): resource/control-cost proxy

문제 요구:

- 비슷한 diffusion strength에서 resource/control-cost proxy 비교
- random-unitary layer 수, entangling operation 수
- Hamiltonian total evolution time, fixed-control structure

현재 있는 코드:

- `results/problem_1_2_baseline/resource_proxies.csv`
- `results/problem_1_2_baseline/comparable_strength_resource_matches.csv`
- `submission/problem2_hamiltonian_projection.py`

현재 상태:

- MMD 기준 comparable pair:
  - random step `1` vs Hamiltonian `t = 0.333333`
  - MMD gap 약 `0.002259`
  - random controls `6`, entanglers `1`
  - Hamiltonian fixed terms `8`, fixed parameters `3`
- Wasserstein 기준 comparable pair:
  - random step `7` vs Hamiltonian `t = 3.333333`
  - Wasserstein gap 약 `0.001220`
  - random controls `42`, entanglers `7`
  - Hamiltonian fixed terms `8`, fixed parameters `3`

부족한 점:

- 이 표를 해석하는 문장이 아직 충분하지 않음
- "Hamiltonian이 무조건 더 좋다"가 아니라 cost 종류가 다르다는 식으로 써야 안전함

보고서용 해석 문장 초안:

- "MMD 기준으로는 아주 짧은 Hamiltonian evolution time에서도 random-unitary 1 step과 비슷한 거리 변화가 관찰된다."
- "Wasserstein 기준으로 맞추면 random-unitary는 7개의 entangler와 42개의 random local controls를 사용하지만, Hamiltonian baseline은 같은 fixed Hamiltonian coefficient 3개와 longer evolution time으로 비슷한 matching cost를 만든다."
- "따라서 이 비교는 어느 쪽이 절대적으로 우월하다는 주장이 아니라, layer-wise random control을 줄이는 대신 time/projection schedule 선택이 중요해지는 trade-off를 보여준다."

### Problem 3: further extension

문제 요구:

- toy reverse/denoising step
- diffusion setting의 controlled modification
- baseline과 비교한 improvement/trade-off

현재 있는 코드:

- `src/quantum_cylinder/problem_3_continuous_projected_denoising.py`
- `submission/problem3_continuous_measurement_denoising.py`
- `scripts/run_problem_3_continuous_denoising.py`
- `scripts/run_problem_3_seed_sweep_visible.ps1`

현재 상태:

- complement measurement basis를 `Z/X/Y` 축에 고정하지 않고 Bloch sphere 위 continuous basis로 탐색
- fixed Hamiltonian + post-selection을 toy non-unitary denoising map으로 사용
- 20-seed sweep에서 `20/20 use_as_main`
- median MMD improvement 약 `0.097056`
- median Wasserstein improvement 약 `0.147983`
- median diversity retention 약 `0.823217`
- median success probability 약 `0.468122`

부족한 점:

- axis-only 대비 median score margin이 약 `0.010000`으로 작으므로 과장하면 위험함
- physical interpretation은 "small-scale post-selected toy proxy"로 제한해야 함

보강 작업:

- 최종 발표 전에는 Problem 3를 새로 크게 바꾸기보다 limitation 문장을 단단히 만든다
- Bloch basis 변화가 왜 controlled modification인지 그림으로 보여준다

## `src/`와 `submission/` 구조 정리

현재 구조는 두 목적이 섞여 보여서 코드 리뷰가 어렵다.

### `src/quantum_cylinder/`

역할:

- 개발용 source of truth
- 테스트와 재사용을 위한 library-style 함수
- return 중심 API가 자연스러움

문제:

- 소문항별 폴더가 아니라 `problem_1a_*.py`, `problem_1b_*.py` 식의 flat 파일 구조
- Problem 2는 `2(a)`, `2(b)`가 한 파일 안에 묶여 있음
- Qiskit backend와 NumPy backend가 함께 있어 처음 보는 팀원이 헷갈릴 수 있음

대회 중 권장 대응:

- 큰 refactor는 위험하므로 지금은 유지
- 대신 README와 이 문서의 code map을 source of truth로 사용
- 필요하면 얇은 wrapper 파일만 추가:
  - `scripts/problem_2a_print_hamiltonian.py`
  - `scripts/problem_2b_generate_projected_ensemble.py`
  - `scripts/problem_2c_plot_bloch_comparison.py`

### `submission/`

역할:

- 심사자/팀원이 바로 읽고 실행하는 독립 실행용 layer
- 최신 main 기준으로 필요한 Qiskit 구현과 metric logic을 내부에 직접 포함
- `src/`를 import하지 않아도 실행 흐름을 따라갈 수 있게 하는 목적

주의:

- `submission/`은 최종 제출 친화적 entry point이지, 개발 중 모든 실험의 source of truth는 아님
- 같은 기능이 `src/`와 중복되어 보일 수 있으나, 목적은 "읽기 쉬움"과 "실행 독립성"이다

## 다음 작업 체크리스트

### 바로 해야 할 것

- [x] Problem 1(b) metric diagnostic 출력 추가: `scripts/problem_1b_check_metrics.py`
- [x] Problem 2(a) Hamiltonian term 출력 추가: `scripts/problem_2a_print_hamiltonian.py`
- [x] Problem 2(b) projection probability/outcome diagnostic 추가: `scripts/problem_2b_projection_diagnostics.py`
- [x] Problem 2(c) reduced Bloch vector visualization 추가: `scripts/problem_2c_plot_bloch_comparison.py`
- [x] Problem 2(d) comparable-strength resource table 해석 문장 보강: `docs/15_quantitative_evaluation_plan.md`
- [ ] 생성된 `results/quantitative_evaluation/` 파일을 팀원이 직접 보고 정성 판단 기록

### 해도 되지만 조심할 것

- [ ] `src/` 폴더를 소문항별 하위 폴더로 재구성
- [ ] Problem 1 random angle scale을 더 작은 값으로 바꿔 gradual diffusion curve 추가

위 두 작업은 기존 결과와 테스트를 흔들 수 있으므로, 시간이 부족하면 최종 제출 전에는 문서와 diagnostic script 보강을 우선한다.

## 팀원별 확인 포인트

| 담당 | 확인할 것 |
| --- | --- |
| 한지후 | diagnostic script와 visualization을 최소 변경으로 추가 |
| 김건우 | Qiskit Hamiltonian term, qubit order, projection basis 설명 검증 |
| 임채진 | Problem 1/2 정성 설명이 문제 요구와 맞는지 확인 |
| 김승빈 | 실행 명령을 따라 결과 파일이 생성되는지 확인하고 screenshot/log 정리 |

## 새 정량 평가 산출물

아래 명령으로 생성한다.

```powershell
python scripts/run_quantitative_evaluation.py
```

확인할 파일:

- `results/quantitative_evaluation/problem_1b_metric_diagnostics.md`
- `results/quantitative_evaluation/problem_2a_hamiltonian_diagnostics.md`
- `results/quantitative_evaluation/problem_2b_projection_diagnostics.md`
- `results/quantitative_evaluation/problem_2c_bloch_qubit_0.png`
- `results/quantitative_evaluation/problem_2c_bloch_qubit_1.png`
- `results/quantitative_evaluation/QUANTITATIVE_EVALUATION_INDEX.md`

## 현재 안전한 주장 범위

- Problem 1/2는 같은 `S0`, 같은 fidelity metric 위에서 두 diffusion mechanism을 비교하는 baseline으로 동작한다.
- Problem 1 random-unitary baseline은 현재 설정에서 빠르게 cluster를 흩뜨리는 strong-scrambling baseline이다.
- Problem 2 Hamiltonian projected diffusion은 fixed Hamiltonian과 complement projection만으로 distance curve를 만들며, time에 따른 fluctuation이 있다.
- Problem 2(d)의 핵심은 "절대 성능 우위"가 아니라 "random control cost와 fixed-control/time-schedule cost의 trade-off"이다.
- Problem 3는 continuous measurement basis search가 toy denoising proxy에서 안정적으로 개선을 보인다는 수준까지 주장할 수 있다.

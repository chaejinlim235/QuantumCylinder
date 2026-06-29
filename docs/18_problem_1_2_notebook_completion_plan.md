# Problem 1/2 Notebook Completion Plan

작성 기준: `2026-06-29 22:31 KST`

오늘의 목표는 Problem 1과 Problem 2를 코드, 결과, 해석이 서로 맞는 상태로 완전히 닫는 것이다. Problem 3 자동화는 별도 루프로 유지하되, 팀원이 직접 읽고 제출물로 다듬을 노트북은 우선 Problem 1/2 완성도를 기준으로 정리한다.

## 입력 노트북

- 원본: `C:\Users\sky_m\Downloads\양자정보경진대회.ipynb`
- 원칙: 원본 파일은 직접 덮어쓰지 않는다.
- 저장 규칙: 수정본은 같은 작업 위치 또는 공유 드라이브 제출 폴더에 `양자정보경진대회_v1.ipynb`, `양자정보경진대회_v2.ipynb`, `양자정보경진대회_v3.ipynb` 순서로 저장한다.
- 각 버전은 실행 결과가 포함된 상태로 저장한다.

## 반드시 직접 리뷰할 코드

노트북을 고치기 전에 아래 코드는 최소 한 번 직접 열어 보고, 노트북의 설명이 실제 구현과 어긋나지 않는지 확인한다.

| Problem | File | 확인할 점 |
| --- | --- | --- |
| 1(a) | `src/quantum_cylinder/implementations/qiskit/problem_1a_target_ensemble.py` | `N=80`, `sigma=0.10`, `Rz(delta_z) Ry(delta_y)`가 `|00>` 주변 ensemble을 만드는지 |
| 1(b) | `src/quantum_cylinder/problem_1b_ensemble_metrics.py` | fidelity, MMD, infidelity-cost Wasserstein-type distance 정의 |
| 1(c) | `src/quantum_cylinder/implementations/qiskit/problem_1c_random_unitary_diffusion.py` | random `RX/RY/RZ` layer와 `CZ` entangler, 12-step trajectory |
| 2(a)(b) | `src/quantum_cylinder/implementations/qiskit/problem_2_hamiltonian_projected_diffusion.py` | fixed Hamiltonian term, qubit order `M0, M1, F`, projection construction |
| 2(c)(d) | `scripts/run_problem_1_2_baselines.py` | distance curve, metric-aligned comparison, comparable-strength resource table |
| diagnostics | `scripts/run_quantitative_evaluation.py` | Problem 1/2 진단 파일을 한 번에 생성하는 경로 |

## 노트북 구성

노트북은 문제 소문항 순서와 동일하게 구성한다. 코드 셀은 새 구현을 복붙하기보다 repo의 검증된 함수와 스크립트 결과를 읽는 방식으로 둔다.

1. Problem 1(a): target ensemble
   - `N=80`, `sigma=0.10`, seed 값을 명시한다.
   - `mean fidelity to |00> = 0.995692`, `min fidelity = 0.972637`을 보여준다.
   - 초기 ensemble이 `|00>` 주변 cluster라는 한 문단 설명을 넣는다.

2. Problem 1(b): metrics
   - fidelity `F(psi, phi)=|<psi|phi>|^2`를 적는다.
   - MMD와 Wasserstein-type distance가 같은 fidelity에서 나온다는 점을 설명한다.
   - `MMD(S0,S0)=0`, `Wasserstein(S0,S0)=0` sanity check를 보여준다.

3. Problem 1(c): random-unitary diffusion
   - random local `RX/RY/RZ` rotations와 `CZ` entangler를 사용한다고 명시한다.
   - `distance_curves.png` 또는 equivalent plot을 넣는다.
   - 현재 설정은 gradual broadening이 아니라 strong scrambling baseline이라는 점을 쓴다.

4. Problem 2(a): fixed Hamiltonian
   - `hx=0.8090`, `hy=0.9045`, `J=1.0`을 명시한다.
   - Pauli terms `XII`, `YII`, `IXI`, `IYI`, `IIX`, `IIY`, `XXI`, `IXX`를 보여준다.
   - Hermiticity error가 0임을 적는다.

5. Problem 2(b): projected ensemble
   - `M`은 Problem 1의 2-qubit data system, `F`는 complement qubit임을 적는다.
   - projection probability normalization diagnostic을 보여준다.
   - projected output이 다시 2-qubit ensemble이라는 점을 설명한다.

6. Problem 2(c): qualitative comparison
   - random-unitary는 step `k`, Hamiltonian projection은 time `t`가 native parameter라 같은 x축으로 직접 비교하지 않는다고 명시한다.
   - native distance curve와 metric-aligned comparison을 함께 보여준다.
   - reduced Bloch-vector plot은 2-qubit state 전체가 아니라 single-qubit marginal diagnostic이라는 guardrail을 넣는다.

7. Problem 2(d): resource/control proxy
   - MMD 기준 comparable pair와 Wasserstein 기준 comparable pair를 표로 보여준다.
   - random-unitary의 layer/entangler/random control 수와 Hamiltonian의 fixed terms/fixed parameters/evolution time을 구분한다.
   - 어느 방식이 절대적으로 우월하다는 주장이 아니라 control-cost trade-off라고 정리한다.

## 실행 명령

노트북 수정 전후에 아래 명령을 실행해 숫자와 그림을 최신으로 맞춘다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
python scripts/run_quantitative_evaluation.py
python scripts/run_problem_1_2_baselines.py
python submission/run_all.py --quick
python -m pytest
```

확인할 결과:

- `results/problem_1_2_baseline/problem_1_2_summary.md`
- `results/problem_1_2_baseline/distance_curves.png`
- `results/problem_1_2_baseline/metric_aligned_comparison.png`
- `results/problem_1_2_baseline/comparable_strength_resource_matches.csv`
- `results/quantitative_evaluation/problem_1b_metric_diagnostics.md`
- `results/quantitative_evaluation/problem_2a_hamiltonian_diagnostics.md`
- `results/quantitative_evaluation/problem_2b_projection_diagnostics.md`
- `results/quantitative_evaluation/problem_2c_bloch_qubit_0.png`
- `results/quantitative_evaluation/problem_2c_bloch_qubit_1.png`

## 완료 기준

- 노트북이 Problem 1(a), 1(b), 1(c), 2(a), 2(b), 2(c), 2(d)를 모두 별도 heading으로 가진다.
- 각 heading에는 코드 실행 결과 또는 생성된 result path가 있다.
- 각 plot/table에는 2-4문장의 해석이 붙어 있다.
- `k`와 `t`를 같은 x축 값처럼 비교하지 않는다.
- reduced Bloch-vector plot을 완전한 2-qubit Bloch sphere라고 쓰지 않는다.
- 수정본은 `v1`, `v2`, `v3` 규칙으로 저장되어 원본을 덮어쓰지 않는다.


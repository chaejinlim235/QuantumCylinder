# Submission Layer

이 폴더는 심사자와 팀원이 먼저 읽을 수 있는 단순 제출용 코드입니다.

기존 `src/`, `scripts/`, `tests/`는 검증과 자동화에 유리한 개발용 구조입니다. 이 폴더는 제출자가 바로 읽고 실행할 수 있도록 필요한 Qiskit 구현을 폴더 안에 복사해 둔 독립 실행용 코드입니다.

## Files

| File | Purpose |
| --- | --- |
| `states_and_metrics.py` | Qiskit target ensemble, MMD, Wasserstein 거리 계산 |
| `problem1_random_unitary_scrambling.py` | Problem 1: Qiskit random local rotations + entangler diffusion |
| `problem2_hamiltonian_projection.py` | Problem 2: Qiskit random-unitary 비교, Hamiltonian evolution, projection, resource matching |
| `problem3_continuous_measurement_denoising.py` | Problem 3: Qiskit-generated diffusion, fixed Hamiltonian, continuous complement-basis post-selection denoising |
| `run_all.py` | Problem 1, 2, 3을 한 번에 실행 |

## Quick Smoke Test

짧게 구조만 확인합니다.

```powershell
python submission/run_all.py --quick
```

## Full Run

제출용 기본 설정으로 실행합니다.

```powershell
python submission/run_all.py
```

결과는 기본적으로 `results/submission_simple/`에 생성됩니다.

## Physical Story

1. Problem 1은 `|00>` 근처의 작은 target ensemble을 만들고, random local rotations와 `CZ` layer로 ensemble을 퍼뜨립니다.
2. Problem 2는 2-qubit data system에 complement qubit `F`를 붙이고, 고정 3-qubit Hamiltonian으로 진화시킨 뒤 `F`를 측정해 projected ensemble을 만듭니다.
3. Problem 3은 Problem 2의 Hamiltonian projection을 denoising step으로 다시 사용합니다. 단, `Z/X/Y` axis projection만 쓰지 않고 Bloch sphere 위의 continuous complement basis를 탐색합니다.

## Qiskit Boundary

- Problem 1(a): Qiskit `QuantumCircuit` + `Statevector`로 target state를 생성합니다.
- Problem 1(c): Qiskit `QuantumCircuit`, `Operator`, `Statevector`로 random unitary layer를 적용합니다.
- Problem 2: Qiskit `SparsePauliOp`로 fixed Hamiltonian을 정의하고 `Statevector` projection을 사용합니다.
- Problem 3: Problem 2의 Qiskit Hamiltonian matrix를 재사용하고, continuous measurement basis 후보 탐색은 수치 grid search로 수행합니다.

## Problem 1 Outputs

Problem 1은 하나의 최종 숫자만 내는 코드가 아닙니다. 실행하면 1(a) target ensemble 확인, 1(b) metric sanity check, 1(c) diffusion curve와 resource proxy가 각각 별도 파일로 생성됩니다.

- `problem1_target_summary.csv`
- `problem1_target_samples.csv`
- `problem1_metric_checks.csv`
- `problem1_random_unitary_metrics.csv`
- `problem1_random_unitary_resources.csv`
- `problem1_distance_curve.png`
- `problem1_summary.md`

## Rule

이 폴더는 읽기 쉬운 제출용 layer입니다. `submission/` 안의 코드는 개발용 패키지를 import하지 않고, 필요한 Qiskit/metric/search 로직을 직접 포함합니다. 개발용 source of truth는 여전히 `src/`에 있지만, 제출 폴더만 보아도 실행 흐름을 따라갈 수 있습니다.

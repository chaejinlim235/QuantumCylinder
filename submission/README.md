# Submission Layer

이 폴더는 심사자와 팀원이 먼저 읽을 수 있는 단순 제출용 코드입니다.

기존 `src/`, `scripts/`, `tests/`는 검증과 자동화에 유리한 개발용 구조입니다. 이 폴더는 같은 구현을 더 얇게 묶어, 문제별 물리 흐름이 바로 보이도록 정리합니다.

## Files

| File | Purpose |
| --- | --- |
| `states_and_metrics.py` | target ensemble, MMD, Wasserstein 거리 계산 |
| `problem1_random_unitary_scrambling.py` | Problem 1: random local rotations + entangler diffusion |
| `problem2_hamiltonian_projection.py` | Problem 2: data + complement Hamiltonian evolution and projection |
| `problem3_continuous_measurement_denoising.py` | Problem 3: continuous complement-basis post-selection denoising |
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

## Rule

이 폴더는 읽기 쉬운 제출용 layer입니다. 물리적 세부 구현의 source of truth는 여전히 `src/quantum_cylinder/`입니다.

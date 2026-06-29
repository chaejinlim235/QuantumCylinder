# Problem 1/2 코드 읽는 순서

이 문서는 Problem 1/2 baseline 코드를 처음 읽는 팀원을 위한 짧은 안내서다.

## 먼저 볼 파일

- 실행 파일: `scripts/run_problem_1_2_baselines.py`
- Problem 1(a): `src/quantum_cylinder/problem_1a_target_ensemble.py`
- Problem 1(b): `src/quantum_cylinder/problem_1b_ensemble_metrics.py`
- Problem 1(c): `src/quantum_cylinder/problem_1c_random_unitary_diffusion.py`
- Problem 2: `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py`

## 실행 파일 읽는 순서

`scripts/run_problem_1_2_baselines.py`는 아래 순서로 읽으면 된다.

1. `parse_args`
   - config와 command line option을 읽는다.
2. `run_experiment`
   - 전체 실험 흐름이다.
   - `S0` 생성, Problem 1 random-unitary 실행, Problem 2 Hamiltonian projection 실행, comparable-strength table 생성을 순서대로 호출한다.
3. `run_problem_1_random_unitary`
   - Problem 1(c)의 random circuit diffusion curve를 만든다.
4. `run_problem_2_hamiltonian_projection`
   - Problem 2의 Hamiltonian time evolution/projection curve를 만든다.
5. `comparable_strength_resource_rows`
   - `k`와 `t`를 같은 x축으로 비교하지 않고, MMD/Wasserstein 값이 가까운 지점을 matching한다.
6. `write_outputs`
   - CSV, PNG, JSON, Markdown summary를 저장한다.

## 중요한 비교 기준

Random-unitary의 `k`와 Hamiltonian projection의 `t`는 같은 단위가 아니다.

따라서 보고서와 발표에서는 다음처럼 설명한다.

- native parameter curve:
  - random-unitary는 `step k`
  - Hamiltonian projection은 `time t`
- cross-mechanism comparison:
  - 같은 x축 위치가 아니라 MMD/Wasserstein 값이 가까운 comparable-strength pair를 비교한다.

## 생성되는 핵심 파일

- `results/problem_1_2_baseline/distance_curves.png`
  - 각 mechanism의 native parameter curve
- `results/problem_1_2_baseline/metric_aligned_comparison.png`
  - metric-space comparison
- `results/problem_1_2_baseline/comparable_strength_resource_matches.csv`
  - Problem 2(d)에 사용할 comparable-strength pair
- `results/problem_1_2_baseline/problem_1_2_summary.md`
  - 보고서용 요약 수치와 해석 guardrail


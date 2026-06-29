# Quantitative Evaluation Plan

이 문서는 최종 보고서가 아니라, 심사위원에게 정량적으로 설득력 있는 결과를 만들기 위해 남은 시간 동안 실행할 평가 계획이다.

## 목표

Problem 1/2/3의 결과를 다음 기준으로 강화한다.

1. **Correctness diagnostics**: 구현이 문제 정의를 직접 만족하는지 보인다.
2. **Robustness**: seed 하나의 우연이 아님을 보인다.
3. **Fair comparison**: 같은 `S0`, 같은 metric, 비슷한 diffusion strength에서 비교한다.
4. **Resource/control proxy**: random-unitary와 Hamiltonian projected diffusion의 비용 종류를 분리해 보여준다.
5. **Qualitative visibility**: distance curve만이 아니라 reduced Bloch-vector cloud로 사람이 볼 수 있게 만든다.

## One-command Evaluation

```powershell
python scripts/run_quantitative_evaluation.py
```

주요 출력:

- `results/quantitative_evaluation/problem_1b_metric_diagnostics.md`
- `results/quantitative_evaluation/problem_2a_hamiltonian_diagnostics.md`
- `results/quantitative_evaluation/problem_2b_projection_diagnostics.md`
- `results/quantitative_evaluation/problem_2c_bloch_qubit_0.png`
- `results/quantitative_evaluation/problem_2c_bloch_qubit_1.png`
- `results/quantitative_evaluation/QUANTITATIVE_EVALUATION_INDEX.md`

`results/` 아래 파일은 기본적으로 commit하지 않는다.

## 문제별 정량 증거

| Problem | Evidence | Purpose |
| --- | --- | --- |
| 1(a) | fidelity to `|00>` summary | target ensemble이 cluster인지 확인 |
| 1(b) | `MMD(S0,S0)`, `W(S0,S0)`, one-step scrambled distance | metric sanity check |
| 1(c) | distance curve, reduced Bloch clouds | cluster structure 변화 설명 |
| 2(a) | Pauli terms, matrix shape, Hermiticity error | Hamiltonian 구현 검증 |
| 2(b) | projection probability normalization | projected ensemble construction 검증 |
| 2(c) | random vs Hamiltonian distance/Bloch comparison | 증가, fluctuation, saturation 정성 비교 |
| 2(d) | comparable-strength resource table | control/resource trade-off 설명 |
| 3 | 20-seed sweep, axis-only comparison, diversity/success gates | extension claim 안정성 |

## 우선순위

1. `python scripts/run_quantitative_evaluation.py`를 실행해 Problem 1/2의 diagnostic output을 확보한다.
2. `.\scripts\run_problem_3_seed_sweep_visible.ps1` 또는 Hermes `final-sync-fix`로 Problem 3 seed sweep을 유지한다.
3. 김건우는 Problem 2(a)/(b)의 Qiskit Hamiltonian, qubit order, projection basis 설명을 검증한다.
4. 임채진은 Problem 1(c), 2(c), 2(d)의 정성 해석 문장을 검토한다.
5. 김승빈은 생성된 `results/quantitative_evaluation/` 파일을 같은 명령으로 재현되는지 확인한다.

## Claim Guardrails

- `random-unitary`는 현재 설정에서 strong-scrambling baseline이다.
- Hamiltonian projected diffusion은 fixed-control alternative이지 무조건 더 좋은 방법이라고 주장하지 않는다.
- Reduced Bloch-vector plot은 2-qubit state 전체의 완전한 표현이 아니라 single-qubit marginal diagnostic이다.
- Problem 3는 small-scale, post-selected, state-vector toy proxy로 제한해 주장한다.

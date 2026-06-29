# Qiskit 검증 레이어

현재 Problem 1/2의 기준 구현은 NumPy/SciPy state-vector 방식이다. 2-qubit, 3-qubit 문제에서는 이 방식이 가장 직접적이고 빠르다.

Qiskit은 필수 구현 도구가 아니라 다음 용도의 보조 레이어로 사용한다.

- Problem 1 random-unitary layer를 회로 형태로 설명
- depth, 1-qubit rotation 수, 2-qubit entangler 수 확인
- 발표/보고서에서 circuit resource proxy를 직관적으로 보여주기

## 설치

기본 개발 환경에는 Qiskit을 설치하지 않는다. 필요한 팀원만 아래 extra를 설치한다.

```powershell
pip install -e ".[qiskit]"
```

기본 테스트 환경과 CI는 Qiskit 없이도 실행된다.

## 실행

```powershell
python scripts/problem_1_qiskit_resource_check.py
```

회로 텍스트 그림을 저장하려면:

```powershell
python scripts/problem_1_qiskit_resource_check.py --draw results/problem_1_qiskit_circuit.txt
```

## 해석

기본 설정 `steps = 12`, `entangler = CZ`에서 기대되는 proxy는 다음과 같다.

- single-qubit rotations: `12 * 2 * 3 = 72`
- two-qubit entanglers: `12`
- random controls: `72`

이 값은 `results/problem_1_2_baseline/resource_proxies.csv`의 random-unitary resource proxy와 같은 논리로 해석한다.

## 팀 내 결론

Qiskit으로 전체 baseline을 갈아엎지 않는다.

대신 NumPy/SciPy 구현을 metric과 state-vector truth로 유지하고, Qiskit은 회로 표현과 gate/depth 설명을 보강하는 데 사용한다. 이 방식이 3일 해커톤 일정에서 가장 안전하다.

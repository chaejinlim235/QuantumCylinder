# LLM 개발 가이드

이 문서는 팀원이 Codex, ChatGPT, Claude 등 LLM을 사용할 때 바로 붙여 넣을 수 있는 프롬프트와 작업 규칙을 정리한다.

## 공통 규칙

- 먼저 `README.md`, `docs/05_hackathon_execution_plan.md`, `docs/07_problem_1_2_solution.md`를 읽고 현재 구현을 기준으로 답한다.
- Problem 1/2 baseline을 깨지 않는다.
- Problem 3 아이디어는 반드시 baseline과 같은 metric으로 비교한다.
- 브랜치명에는 개인 이름이나 GitHub username을 넣지 않는다.
- PR 본문은 가능하면 영어/ASCII로 작성해 GitHub 한글 깨짐을 피한다.
- 문서 본문은 UTF-8 한글로 작성해도 된다.
- 코드 변경 후에는 `python -m pytest`를 실행한다.
- 물리 해석을 모르면 단정하지 말고 "검증 필요"로 표시한다.
- 논문 전체를 번역하지 말고 figure, metric, 실험 설정, 우리 주장에 필요한 문장만 추출한다.

## 공통 시작 프롬프트

```text
너는 QuantumCylinder 팀의 2026 양자정보경진대회 작업을 돕는 LLM 개발 파트너다.

반드시 먼저 아래 파일의 역할을 기준으로 작업해라.
- README.md
- docs/05_hackathon_execution_plan.md
- docs/07_problem_1_2_solution.md
- docs/09_qiskit_validation_layer.md

현재 운영 원칙:
- 한지후가 핵심 코드 구현과 최종 통합을 담당한다.
- 김건우는 Qiskit/resource 검증과 논문 확인을 담당한다.
- 임채진은 지정문제/논문 해석과 보고서 흐름을 담당한다.
- 김승빈은 Python 환경 복구, 실행 재현, 결과 정리를 담당한다.

작업 원칙:
1. Problem 1/2 baseline을 깨지 마라.
2. Problem 3 제안은 baseline과 같은 MMD/Wasserstein-type metric으로 비교하라.
3. 브랜치명에는 개인 이름이나 GitHub username을 넣지 마라.
4. 코드 변경 후에는 `python -m pytest`를 실행하라.
5. 확실하지 않은 물리 해석은 단정하지 말고 검증 질문으로 남겨라.
6. 최종 답변에는 변경 파일, 실행 명령, 확인 결과를 짧게 적어라.
```

## 한지후용 프롬프트

```text
나는 QuantumCylinder 팀의 핵심 구현과 통합을 맡은 한지후다.

목표:
- Problem 1/2 baseline을 안정적으로 유지한다.
- Problem 3 extension을 가장 작은 구현으로 시작한다.
- 팀원 PR을 검증하고 충돌 없이 merge 가능한 상태로 만든다.

현재 코드 기준으로 다음을 도와줘.
1. 변경 범위를 작게 나눠라.
2. 문제별 파일명 규칙 `problem_<n><subproblem>_<topic>.py`를 지켜라.
3. 새 실험은 `configs/`, `scripts/`, `src/quantum_cylinder/`, `tests/` 중 필요한 곳만 수정하라.
4. baseline과 같은 metric으로 비교할 수 없는 아이디어는 우선순위를 낮춰라.
5. 결과 해석에는 개선점과 trade-off를 함께 적어라.
6. 마지막에 실행할 명령을 제시하라.
```

## 김건우용 프롬프트

```text
나는 QuantumCylinder 팀에서 Qiskit 적용, 회로/resource 검증, 논문 확인을 맡은 김건우다.

목표:
- NumPy/SciPy baseline을 Qiskit으로 갈아엎지 않는다.
- Qiskit은 회로 표현, depth, gate count, resource proxy를 설명하는 보조 레이어로 쓴다.
- Problem 1/2 구현이 지정문제 조건과 맞는지 확인한다.

현재 코드 기준으로 다음을 도와줘.
1. `scripts/problem_1_qiskit_resource_check.py`를 기준으로 회로 depth, rotation 수, entangler 수를 정리하라.
2. Qiskit 구현이 baseline metric과 직접 연결되지 않는다면 resource 설명으로 분리하라.
3. 논문에서 필요한 부분은 metric, circuit/resource, 실험 조건 위주로만 요약하라.
4. 한지후가 바로 반영할 수 있게 파일명, 함수명, 표 형태로 제안하라.
5. 불확실한 해석은 "검증 필요"로 표시하라.
```

## 임채진용 프롬프트

```text
나는 QuantumCylinder 팀에서 지정문제 해석, 논문 핵심 추출, 최종 보고서 흐름을 맡은 임채진이다.

목표:
- 문제를 과장 없이 정확히 해석한다.
- 논문 전체 번역이 아니라 발표와 보고서에 필요한 핵심만 뽑는다.
- Problem 1/2 baseline 결과와 Problem 3 claim을 하나의 이야기로 묶는다.

현재 자료 기준으로 다음을 도와줘.
1. 지정문제에서 요구하는 입력, 출력, 평가 기준을 짧게 정리하라.
2. 논문에서 우리에게 필요한 metric, 실험 설정, figure 해석만 추출하라.
3. Problem 1과 Problem 2의 차이를 발표 문장으로 바꿔라.
4. "우리가 실제로 구현한 것"과 "논문에서 가져온 아이디어"를 구분하라.
5. 확실하지 않은 물리적 주장은 검증 질문으로 남겨라.
6. 보고서 목차와 각 장의 핵심 문장을 제안하라.
```

## 김승빈용 프롬프트

```text
나는 QuantumCylinder 팀에서 Python 환경 복구, 실행 재현, 결과 정리를 맡은 김승빈이다.

목표:
- 로컬 Python 환경을 복구한다.
- baseline 실행 명령이 통과하는지 확인한다.
- 결과 파일이 어디에 생성되는지 정리한다.

현재 저장소 기준으로 다음을 도와줘.
1. Windows PowerShell 기준으로 가상환경 생성, 활성화, 설치, 실행 명령을 단계별로 알려줘.
2. `pip install -e ".[dev]"`, `python scripts/run_problem_1_2_baselines.py`, `python -m pytest`가 통과하는지 확인하게 해줘.
3. 오류가 나면 오류 메시지의 핵심 원인과 다음 명령을 제안해줘.
4. 논문 리딩은 전체 번역이 아니라 figure, metric, 실험 조건만 요약하게 해줘.
5. 결과 파일 목록과 발표에 쓸 수 있는 figure/table 후보를 정리하게 해줘.
```

## 환경 복구용 짧은 프롬프트

```text
Windows PowerShell에서 Python 개발 환경이 꼬였다.
현재 저장소는 QuantumCylinder이고, 목표는 아래 명령이 통과하는 것이다.

pip install -e ".[dev]"
python scripts/run_problem_1_2_baselines.py
python -m pytest

내가 붙여 넣는 오류 메시지를 보고 원인 후보를 2개 이하로 줄이고, 다음에 실행할 명령만 순서대로 알려줘.
설명은 짧게 하고, 위험한 삭제 명령은 먼저 이유를 설명해줘.
```

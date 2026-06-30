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
- 역할, issue, 파일 구조, 진행도가 바뀌면 `README.md`, `docs/github_issue_plan.json`, 실제 GitHub issue를 같은 변경 안에서 동기화한다.

## 공통 시작 프롬프트

```text
너는 QuantumCylinder 팀의 2026 양자정보경진대회 작업을 돕는 LLM 개발 파트너다.

반드시 먼저 아래 파일의 역할을 기준으로 작업해라.
- README.md
- docs/05_hackathon_execution_plan.md
- docs/07_problem_1_2_solution.md
- docs/09_qiskit_validation_layer.md
- docs/22_overnight_problem_3_evidence_handoff.md

현재 운영 원칙:
- 한지후가 핵심 코드 구현, 통합, README/issue 동기화, 최종 gatekeeping을 담당한다.
- 김건우는 코드/Qiskit 구현 해석, conditional state 설명, resource/control-cost consistency 검수를 담당한다.
- 임채진은 ipynb 최종 보고서 작성, 1/2번 형식 유지, 3번 소문항별 답변 추가를 담당한다.
- 김승빈은 물리적 해석, figure/table 패키징, support worker 재현 로그 정리를 담당한다.

작업 원칙:
1. Problem 1/2 baseline을 깨지 마라.
2. Problem 3 제안은 baseline과 같은 MMD/Wasserstein-type metric으로 비교하라.
3. 브랜치명에는 개인 이름이나 GitHub username을 넣지 마라.
4. 코드 변경 후에는 `python -m pytest`를 실행하라.
5. 확실하지 않은 물리 해석은 단정하지 말고 검증 질문으로 남겨라.
6. 역할, issue, 파일 구조, 진행도가 바뀌면 README, issue plan, 실제 GitHub issue를 함께 갱신하라.
7. 최종 답변에는 변경 파일, 실행 명령, 확인 결과를 짧게 적어라.
```

## 한지후용 프롬프트

```text
나는 QuantumCylinder 팀의 핵심 구현과 통합을 맡은 한지후다.

목표:
- Problem 1/2 baseline을 안정적으로 유지한다.
- Problem 3 최종 claim 숫자와 limitation을 gatekeeping한다.
- 팀원 PR을 검증하고 충돌 없이 merge 가능한 상태로 만든다.
- README, issue plan, 실제 GitHub issue를 항상 같은 상태로 유지한다.

현재 코드 기준으로 다음을 도와줘.
1. 변경 범위를 작게 나눠라.
2. 문제별 파일명 규칙 `problem_<n><subproblem>_<topic>.py`를 지켜라.
3. 새 실험은 `configs/`, `scripts/`, `src/quantum_cylinder/`, `tests/` 중 필요한 곳만 수정하라.
4. baseline과 같은 metric으로 비교할 수 없는 아이디어는 우선순위를 낮춰라.
5. 결과 해석에는 개선점과 trade-off를 함께 적어라.
6. 역할/issue/파일 구조가 바뀌면 `README.md`, `docs/github_issue_plan.json`, 실제 GitHub issue를 갱신하라.
7. 마지막에 실행할 명령을 제시하라.
```

## 김건우용 프롬프트

```text
나는 QuantumCylinder 팀에서 코드/Qiskit 구현 해석과 consistency 검수를 맡은 김건우다.

목표:
- notebook 설명이 실제 `submission/`, `src/quantum_cylinder/`, Qiskit/backend 구현과 충돌하지 않는지 확인한다.
- Problem 2(b)의 auxiliary/complement qubit 설명이 normalized conditional post-measurement state를 정확히 말하는지 검수한다.
- resource/control-cost proxy가 주관 점수가 아니라 구현에서 나온 count/time proxy로 설명되도록 확인한다.

현재 코드 기준으로 다음을 도와줘.
1. README의 Code Map을 기준으로 Problem 1/2/3 entry point를 읽어라.
2. Problem 2(b)가 단순 append가 아니라 projection outcome에 따른 normalized conditional state임을 코드와 수식 관점에서 설명하라.
3. Problem 2(c)의 random step `k`와 Hamiltonian time `t`가 같은 x축 물리량으로 오해되지 않도록 문장을 제안하라.
4. Qiskit 구현이 baseline metric과 직접 연결되지 않는다면 resource 설명으로 분리하라.
5. 한지후와 임채진이 바로 반영할 수 있게 파일명, 함수명, 표 형태로 제안하라.
6. 불확실한 해석은 "검증 필요"로 표시하라.
```

## 임채진용 프롬프트

```text
나는 QuantumCylinder 팀에서 ipynb 최종 보고서 작성과 storyline 정리를 맡은 임채진이다.

목표:
- 현재 1/2번 notebook 형식을 유지한다.
- Problem 3 소문항별 답변을 같은 톤으로 추가한다.
- Problem 1/2 baseline 결과와 Problem 3 claim을 하나의 이야기로 묶는다.

현재 자료 기준으로 다음을 도와줘.
1. 지정문제에서 요구하는 입력, 출력, 평가 기준을 짧게 정리하라.
2. 논문에서 우리에게 필요한 metric, 실험 설정, figure 해석만 추출하라.
3. Problem 1과 Problem 2의 차이를 발표 문장으로 바꿔라.
4. "우리가 실제로 구현한 것"과 "논문에서 가져온 아이디어"를 구분하라.
5. Problem 3 claim은 `20/20 use_as_main`, median MMD/Wasserstein improvement, axis-only margin limitation을 같은 숫자로 맞춰라.
6. 확실하지 않은 물리적 주장은 검증 질문으로 남겨라.
7. 보고서 목차와 각 장의 핵심 문장을 제안하라.
```

## 김승빈용 프롬프트

```text
나는 QuantumCylinder 팀에서 Problem 3 물리적 해석, figure/table 패키징, 재현 로그 정리를 맡은 김승빈이다.

목표:
- measurement-induced denoising proxy와 hybrid extension의 물리적 의미를 설명한다.
- support worker 결과와 seed sweep 결과에서 최종 보고서에 넣을 표/그림 후보를 고른다.
- 결과 파일이 어디에 생성되는지 정리한다.

현재 저장소 기준으로 다음을 도와줘.
1. `docs/22_overnight_problem_3_evidence_handoff.md`와 support worker 결과를 기준으로 핵심 수치를 정리하게 해줘.
2. continuous measurement-basis post-selection이 왜 denoising proxy인지 과장 없이 설명하게 해줘.
3. hybrid toy는 hardware-motivated plausibility evidence로만 쓰고 hardware advantage로 과장하지 않게 해줘.
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

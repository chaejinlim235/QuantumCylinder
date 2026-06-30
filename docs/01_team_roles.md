# 팀 역할

개인정보가 담긴 신청서 원문은 저장소에 두지 않는다. 이 문서는 대회 중 협업을 위한 이름, GitHub 계정, 역할만 기록한다.

## 현재 운영 원칙

- 한지후가 코드 구현의 대부분과 최종 통합을 담당한다.
- 임채진은 ipynb 최종 보고서와 storyline에 집중한다.
- 김건우는 코드/Qiskit 구현 해석과 notebook 설명의 consistency 검수에 집중한다.
- 김승빈은 Problem 3의 물리적 해석, figure/table 패키징, 재현 로그 정리에 집중한다.
- 팀원별 브랜치는 따로 두되, 브랜치명에는 개인 이름이나 GitHub username을 넣지 않는다.
- 첫 해커톤인 팀원이 많으므로 작업 단위를 작게 유지하고, PR에는 실행 명령과 확인 결과를 반드시 남긴다.
- 역할, issue, 파일 구조, 진행도가 바뀌면 `README.md`, `docs/github_issue_plan.json`, 실제 GitHub issue를 같은 변경 안에서 동기화한다.

## 핵심 역할

| 팀원 | GitHub | 주 담당 | 현재 상태 | 첫 산출물 | 리뷰 파트너 |
| --- | --- | --- | --- | --- | --- |
| 한지후 | `caffeine-fighter` | 핵심 코드 구현, 통합, gatekeeping, README/issue 동기화 | Problem 1/2 baseline과 Problem 3 main candidate를 안정화함 | main branch 안정화, 최종 claim 숫자 관리, metadata sync | 임채진, 김건우 |
| 김건우 | `koi312500` | 코드/Qiskit 구현 해석 및 consistency 검수 | notebook 설명과 실제 Qiskit/backend 구현의 충돌 여부를 검수 중 | conditional state 설명, x축 비교 주의, resource/control-cost 문장 | 한지후 |
| 임채진 | `chaejinlim235` | ipynb 최종 보고서 작성 및 storyline 정리 | 1/2번 notebook 형식을 유지하며 3번 소문항 답변을 추가 중 | 최종 ipynb 보고서, claim/limitation/발표 흐름 | 한지후, 김승빈 |
| 김승빈 | `dreamerghost77` | 물리적 해석, figure/table 패키징, 재현 로그 정리 | support worker 결과와 Problem 3 물리 해석을 정리 중 | measurement-induced denoising 해석, 표/그림 후보, 재현 로그 | 김건우 |

## 팀원별 지금 할 일

### 한지후

- `main`의 Problem 1/2 baseline을 안정적으로 유지한다.
- Problem 3의 최종 claim 숫자가 seed sweep summary와 충돌하지 않게 gatekeeping한다.
- README, `docs/github_issue_plan.json`, 실제 GitHub issue를 같은 상태로 유지한다.
- 팀원 PR을 받아 CI, 테스트, 충돌 여부를 확인하고 merge한다.
- 코드 변경은 작게 나누어 실험 실패 시에도 되돌리기 쉽게 만든다.

### 김건우

- notebook 설명이 실제 `submission/`, `src/quantum_cylinder/`, Qiskit/backend 구현과 충돌하지 않는지 확인한다.
- Problem 2(b)의 auxiliary/complement qubit 설명이 normalized conditional post-measurement state를 정확히 말하는지 검수한다.
- Problem 2(c)의 random step `k`와 Hamiltonian time `t`가 같은 물리량처럼 보이지 않도록 문장을 검수한다.
- 산출물은 코드 위치, 함수명, 짧은 검수 문장 중심으로 남긴다.

### 임채진

- 현재 1/2번 notebook 형식을 유지하고, Problem 3 소문항별 답변을 같은 톤으로 추가한다.
- Problem 1/2 baseline 결과가 무엇을 보여주는지 과장 없이 설명한다.
- Problem 3 claim, limitation, figure/table caption이 seed sweep summary와 같은 숫자를 가리키도록 정리한다.
- Codex나 GitHub 작업이 다시 막히면 문서 초안을 로컬 파일로 먼저 저장하고, 커밋은 한지후에게 넘긴다.

### 김승빈

- Problem 3의 물리적 해석을 정리하고, support worker 결과에서 최종 보고서에 넣을 표/그림 후보를 고른다.
- 재현이 필요하면 아래 세 명령이 통과하는지 확인한다.

```powershell
pip install -e ".[dev]"
python scripts/run_problem_1_2_baselines.py
python -m pytest
```

- 실행 결과가 생기면 result path와 caption 후보를 함께 기록한다.
- 논문 리딩은 전체 번역보다 Problem 3 claim에 필요한 물리 해석, metric, 실험 설정 위주로 줄인다.

## 협업 규칙

- 실험 PR은 반드시 owner와 reviewer를 둔다.
- 한 사람이 만든 figure는 다른 한 사람이 수치와 caption을 확인한다.
- failed experiment도 짧게 남긴다. 실패의 이유가 Problem 3 discussion 재료가 될 수 있다.
- 최종 발표에서는 팀원별 구현물을 나열하기보다 하나의 질문으로 묶는다: "양자 확산 품질과 control/resource cost 사이의 trade-off는 어떻게 달라지는가?"

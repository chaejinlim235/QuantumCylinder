# 팀 역할

개인정보가 담긴 신청서 원문은 저장소에 두지 않는다. 이 문서는 대회 중 협업을 위한 이름, GitHub 계정, 역할만 기록한다.

## 현재 운영 원칙

- 한지후가 코드 구현의 대부분과 최종 통합을 담당한다.
- 나머지 팀원은 구현 자체보다 해석, 검증, 환경 안정화, 실행 재현, 발표 자료화에 집중한다.
- 팀원별 브랜치는 따로 두되, 브랜치명에는 개인 이름이나 GitHub username을 넣지 않는다.
- 첫 해커톤인 팀원이 많으므로 작업 단위를 작게 유지하고, PR에는 실행 명령과 확인 결과를 반드시 남긴다.

## 핵심 역할

| 팀원 | GitHub | 주 담당 | 현재 상태 | 첫 산출물 | 리뷰 파트너 |
| --- | --- | --- | --- | --- | --- |
| 한지후 | `caffeine-fighter` | 핵심 코드 구현, 통합, Problem 3 extension | Problem 1/2 baseline과 테스트 환경을 주도적으로 구축 | Problem 3 최소 구현, metric 비교표, merge 관리 | 임채진, 김건우 |
| 김건우 | `koi312500` | Qiskit 적용, 회로/resource 검증, 논문 확인 | Qiskit 코드 적용과 논문 리딩을 병행 중 | gate/depth/resource proxy 표, NumPy baseline과 Qiskit 회로 관점 비교 | 한지후 |
| 임채진 | `chaejinlim235` | 지정문제 해석, 논문 핵심 추출, 발표 흐름 | 문제/논문 해석 중이며 Codex 작업 커밋이 지연 중 | 문제 정의 1페이지, baseline 결과 해석, 보고서 목차 | 한지후 |
| 김승빈 | `dreamerghost77` | Python 환경 복구, 실행 재현, 결과 정리 | Python 설치 문제 해결 중이며 논문을 GPT와 함께 읽는 중 | 로컬 실행 성공 로그, 결과 파일 체크리스트, figure/table 후보 | 김건우 |

## 팀원별 지금 할 일

### 한지후

- `main`의 Problem 1/2 baseline을 안정적으로 유지한다.
- Problem 3 후보를 하나로 줄이고 최소 구현을 시작한다.
- 팀원 PR을 받아 CI, 테스트, 충돌 여부를 확인하고 merge한다.
- 코드 변경은 작게 나누어 실험 실패 시에도 되돌리기 쉽게 만든다.

### 김건우

- `scripts/problem_1_qiskit_resource_check.py`를 실행해 Qiskit 회로 관점의 resource proxy를 정리한다.
- Problem 1/2 구현이 문제 조건과 어긋나지 않는지 PDF/논문 기준으로 확인한다.
- Qiskit으로 전체 baseline을 갈아엎기보다, 회로 설명과 resource 검증에 필요한 부분만 보강한다.
- 산출물은 표와 짧은 해석 문장 중심으로 남긴다.

### 임채진

- 지정문제와 논문에서 발표에 반드시 필요한 정의, 가정, 평가 기준만 추출한다.
- Problem 1/2 baseline 결과가 무엇을 보여주는지 과장 없이 설명한다.
- 최종 보고서의 목차와 스토리라인을 만든다.
- Codex나 GitHub 작업이 무한 로딩이면 문서 초안을 로컬 파일로 먼저 저장하고, 커밋은 한지후에게 넘긴다.

### 김승빈

- Python 환경 문제 해결을 최우선으로 한다.
- 환경이 복구되면 아래 세 명령이 통과하는지 확인한다.

```powershell
pip install -e ".[dev]"
python scripts/run_problem_1_2_baselines.py
python -m pytest
```

- 실행 결과가 생기면 `results/problem_1_2_baseline/`에 어떤 파일이 생성되는지 확인한다.
- 논문 리딩은 전체 번역보다 figure, metric, 실험 설정 위주로 줄인다.

## 협업 규칙

- 실험 PR은 반드시 owner와 reviewer를 둔다.
- 한 사람이 만든 figure는 다른 한 사람이 수치와 caption을 확인한다.
- failed experiment도 짧게 남긴다. 실패의 이유가 Problem 3 discussion 재료가 될 수 있다.
- 최종 발표에서는 팀원별 구현물을 나열하기보다 하나의 질문으로 묶는다: "양자 확산 품질과 control/resource cost 사이의 trade-off는 어떻게 달라지는가?"

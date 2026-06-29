# 3일 해커톤 실행 계획

제출 목표 시각: **3일차 09:00**
내부 완료 목표 시각: **3일차 08:00**
코드/실험 동결 목표 시각: **3일차 07:30**

## 현재 상황

| 항목 | 상태 | 담당 | 판단 |
| --- | --- | --- | --- |
| Problem 1 baseline | 잠금 | 한지후 | 3번 extension의 비교 기준으로 유지 |
| Problem 2 baseline | 잠금 | 한지후 | comparable-strength resource match 표까지 생성 |
| Qiskit 설치/검증 | 로컬 검증 완료 | 김건우 | 전체 구현 교체가 아니라 resource 설명 보강에 사용 |
| 테스트 환경 | 구축 완료 | 한지후 | `python -m pytest` 기준으로 PR 검증 |
| 지정문제/논문 해석 | 진행 중 | 임채진, 김건우, 김승빈 | 전체 번역보다 claim에 필요한 정의와 figure만 추출 |
| Python 환경 복구 | 진행 중 | 김승빈 | 환경 복구 전에는 코드 구현을 맡기지 않음 |
| Problem 3 extension | 착수 가능 | 한지후 | measurement-basis sweep 또는 shallow denoising 중 최소 구현 선택 |
| 최종 보고서/발표 | 스토리라인 초안 있음 | 임채진 | baseline 결과와 Problem 3 claim에 맞춰 보강 |

## 운영 전제

- 한지후가 코드 구현의 대부분과 최종 통합을 담당한다.
- 김건우는 Qiskit 적용, 회로/resource proxy, 논문 기준 검증을 담당한다.
- 임채진은 지정문제 해석, 논문 핵심 추출, 최종 보고서 흐름을 담당한다.
- 김승빈은 Python 환경 복구, 실행 재현, 결과 파일 확인을 담당한다.
- 팀원들은 개발 경험은 충분하지만 첫 해커톤이므로, 작업 단위는 작게 만들고 완료 기준을 명확히 둔다.
- 논문 해석은 `docs/06_paper_triage.md` 기준으로 제한한다.
- 모든 작업은 1인 1주 브랜치를 쓰되, 브랜치명에는 개인 이름을 넣지 않는다.

## Branch And Owner Map

| Owner | Branch | Scope |
| --- | --- | --- |
| 한지후 | `exp/problem-3-denoising-extension` | 핵심 구현, Problem 3 extension, 최종 통합 |
| 김건우 | `feat/problem-1-2-circuit-validation` | Qiskit 적용, circuit/resource 검증 |
| 임채진 | `docs/final-report-storyline` | 문제 해석, 논문 핵심, 보고서/발표 흐름 |
| 김승빈 | `exp/problem-1-2-result-pipeline` | 환경 복구, baseline 실행 재현, 결과 파일 확인 |

## Timeline

### Day 1: Problem 1/2 고정과 역할 안정화

목표: Problem 1/2는 더 이상 큰 구조를 바꾸지 않고, Problem 3 후보를 하나로 좁힌다.

- 한지후: Problem 1/2 baseline과 테스트를 유지하고 Problem 3 후보를 구현 난도 기준으로 정리한다.
- 김건우: Qiskit resource check를 실행하고 random-unitary 회로의 depth, rotation 수, entangler 수를 표로 만든다.
- 임채진: 지정문제에서 요구하는 입력, 출력, 평가 기준을 짧게 정리한다.
- 김승빈: Python 환경을 복구하고 baseline 실행 명령이 통과하는지 확인한다.

완료 기준:

- `python scripts/run_problem_1_2_baselines.py` 실행 가능
- `python -m pytest` 통과
- Qiskit resource proxy 표 초안 확보
- Problem 3 후보 1개와 backup 1개 선택

### Day 1 저녁: Problem 3 최소 구현 시작

목표: 새 아이디어를 늘리지 않고 최소 실험 코드를 만든다.

- 한지후: 선택한 Problem 3 extension의 최소 구현을 시작한다.
- 김건우: extension이 기존 resource proxy와 어떻게 비교되는지 정리한다.
- 임채진: main claim이 발표 가능한 문장인지 확인한다.
- 김승빈: 환경이 복구되었으면 실행 로그와 결과 저장 경로를 확인한다. 환경이 여전히 깨져 있으면 더 이상 코드를 맡지 않고 문서/체크리스트로 지원한다.

완료 기준:

- 실패해도 설명 가능한 main claim 1개
- baseline과 같은 metric으로 비교할 계획
- 결과 폴더와 config 이름 확정

### Day 2 오전: Extension 구현과 첫 결과

목표: Problem 3의 첫 숫자를 만든다.

- 한지후: extension을 실행 가능한 상태로 만들고 baseline과 같은 MMD/Wasserstein-type metric을 계산한다.
- 김건우: Qiskit/resource 관점에서 추가 비용을 설명한다.
- 임채진: baseline 대비 무엇이 좋아졌고 무엇이 나빠졌는지 문장으로 정리한다.
- 김승빈: 실행 재현과 결과 파일 목록을 확인한다.

완료 기준:

- baseline 대비 비교 가능한 숫자 1세트
- main figure 후보 1장
- resource/trade-off 표 초안

### Day 2 오후: Seed Sweep And Ablation

목표: 결과를 보강하되 실험 범위를 넓히지 않는다.

- seed는 최소 3개만 반복한다.
- ablation은 measurement basis, denoising strength, time grid 중 하나만 선택한다.
- 새 모델이나 새 metric을 추가하지 않는다.

완료 기준:

- main figure 후보 1장 확정
- appendix figure 후보 1-2장
- 실패/한계 해석 메모

### Day 2 저녁: Report Draft Freeze

목표: 새 실험보다 제출 가능한 스토리를 우선한다.

- 임채진: 보고서 목차, 실험 설명, 결론 초안을 작성한다.
- 한지후: 코드 실행법, metric 정의, limitation을 정리한다.
- 김건우: Qiskit/resource proxy 설명을 넣는다.
- 김승빈: figure/table 파일명과 결과 재현 명령을 확인한다.

완료 기준:

- 보고서/발표 초안 80% 이상
- 새 실험 추가 금지 여부 결정
- 남은 작업을 오탈자, figure 교체, 결과 확인으로 제한

### Day 3 06:00-07:30: Final Verification

목표: 제출 직전 깨진 링크, 깨진 실행, 누락 파일을 없앤다.

- `python scripts/run_problem_1_2_baselines.py`
- `python -m pytest`
- 제출 figure/table 파일 열림 확인
- README 실행법 확인
- 압축 파일 또는 제출 링크 확인

완료 기준:

- 코드/실험 동결
- 제출물 패키지 확정

### Day 3 07:30-09:00: Submission Buffer

목표: 업로드와 최종 확인만 한다.

- 파일명, 링크, 열림 여부 확인
- 제출 플랫폼 업로드
- 최종 제출

## Risk Control

- Day 2 오전까지 Problem 3 결과가 불안정하면 extension 범위를 줄인다.
- Day 2 저녁 이후에는 새 아이디어를 추가하지 않는다.
- 수치가 기대와 다르면 실패를 숨기지 않고 trade-off로 정리한다.
- 양자물리 설명은 과장하지 않고, 작은 예제에서 확인한 사실만 주장한다.
- 팀원이 환경 문제로 막히면 코드를 맡기기보다 해석, 검증, 체크리스트로 역할을 전환한다.

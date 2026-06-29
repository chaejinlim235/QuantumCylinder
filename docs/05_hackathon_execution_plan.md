# 3일 해커톤 실행 계획

현재 시각 기준: **1일차 15:30**  
제출 목표 시각: **3일차 09:00**  
내부 완료 목표 시각: **3일차 08:00**

## 운영 전제

- 나를 제외한 팀원들은 개발 경험은 충분하지만 첫 해커톤이다.
- 한지후는 MVP 개발 해커톤 경험은 있으나 양자물리 배경은 거의 없는 상태다.
- 따라서 초반에는 이론 완성보다 baseline 재현, 결과물 동결, 발표 논리 정리를 우선한다.
- 논문 해석은 `docs/06_paper_triage.md` 기준으로 제한한다.
- 모든 작업은 1인 1주 브랜치를 쓰되, 브랜치명에는 개인 이름을 넣지 않는다.
- GitHub issue assignee를 모르는 경우 issue 본문에 `Owner`를 명시한다.

## Branch And Owner Map

| Owner | Branch | Scope |
| --- | --- | --- |
| 임채진 | `docs/final-report-storyline` | 문제 해석, 결과 해석, 최종 보고서/발표 흐름 |
| 김건우 | `feat/problem-1-2-circuit-validation` | Problem 1/2 구현 검증, 회로/resource proxy |
| 김승빈 | `exp/problem-1-2-result-pipeline` | 실험 실행, seed sweep, CSV/plot, 결과 패키징 |
| 한지후 | `exp/problem-3-denoising-extension` | metric 검증, 동일 diffusion strength 비교, toy denoising extension |

## Timeline

### Day 1 15:30-18:30: Baseline Lock

- 전원: `python scripts/run_problem_1_2_baselines.py` 실행 확인
- 김건우: Problem 1/2 구현이 문제 PDF 조건과 맞는지 점검
- 김승빈: 결과 CSV/plot 생성 경로와 재현 절차 정리
- 한지후: MMD/Wasserstein 값이 정상 범위인지 sanity check
- 임채진: 문제 해석과 최종 발표 질문 1문장 정리

완료 기준:

- baseline 실행 성공
- Problem 1/2 결과 plot 확보
- 최소 1개 resource proxy table 초안 확보

### Day 1 18:30-23:00: Extension Choice

- 후보 2개 이하로 축소
- 추천 기본 조합:
  - projection basis sweep
  - shallow denoising filter
- 한지후: denoising filter metric 설계
- 김건우: resource proxy와 구현 난도 평가
- 김승빈: 실험 batch 실행 방식 정리
- 임채진: 발표에서 주장 가능한 형태인지 검토

완료 기준:

- Problem 3에서 밀고 갈 main claim 1개 선택
- 실패해도 발표 가능한 backup claim 1개 확보

### Day 2 09:00-12:00: Extension Implementation

- Problem 3 extension 최소 구현
- baseline과 같은 metric으로 비교
- result directory와 config naming 고정

완료 기준:

- baseline 대비 비교 가능한 숫자 1세트
- plot 1장 이상

### Day 2 12:00-18:00: Seed Sweep And Ablation

- seed 최소 3개 반복
- measurement basis, denoising strength, time grid 중 하나만 주요 ablation으로 선택
- 지나친 실험 확장은 금지

완료 기준:

- main figure 후보 1장
- appendix figure 후보 2장
- 실패/한계 해석 메모

### Day 2 18:00-23:30: Report Draft Freeze

- 임채진: story line과 conclusion 초안
- 김승빈: figure/table 정리
- 김건우: resource/control-cost 설명
- 한지후: metric/denoising 해석과 limitation 정리

완료 기준:

- 보고서/발표 초안 80% 이상
- 새 실험 추가 금지 여부 결정

### Day 3 06:00-08:00: Final Package

- 코드 실행 확인
- final plot/table 파일 확인
- README 실행법 확인
- 제출 파일명과 압축 파일 확인

완료 기준:

- 제출물 동결
- 08:00 이후에는 오탈자/포맷만 수정

### Day 3 08:00-09:00: Submission Buffer

- 업로드, 링크, 파일 열림 여부 확인
- 최종 제출

## Task Ownership

### 임채진

- Problem 1/2 결과의 물리적 의미를 설명한다.
- random-unitary와 Hamiltonian projected diffusion의 차이를 발표 문장으로 정리한다.
- 최종 보고서 목차와 결론을 관리한다.

### 김건우

- Problem 1/2 구현이 문제 조건과 맞는지 확인한다.
- random-unitary layer 수, rotation 수, entangler 수를 resource proxy로 정리한다.
- Hamiltonian projected diffusion의 fixed-control 구조와 비교한다.

### 김승빈

- 실험 실행 명령, config, 결과 저장 경로를 관리한다.
- seed sweep과 plot 생성을 담당한다.
- 발표에 쓸 figure/table 후보를 정리한다.

### 한지후

- fidelity, MMD, Wasserstein-type distance sanity check를 맡는다.
- 같은 diffusion strength 기준에서 resource 비교 방법을 정한다.
- toy denoising 또는 Problem 3 extension의 metric 해석을 담당한다.

## Risk Control

- Day 2 12:00까지 Problem 3 결과가 불안정하면 extension 범위를 줄인다.
- Day 2 18:00 이후에는 새 아이디어를 추가하지 않는다.
- 수치가 기대와 다르면 실패를 숨기지 않고 trade-off로 정리한다.
- 양자물리 설명은 과장하지 않고, 작은 예제에서 확인한 사실만 주장한다.

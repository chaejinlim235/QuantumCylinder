# 3일 로드맵 및 현재 진행도

작성 기준: 2026-06-29  
대회 운영 시간대: KST  
범위: 2026-06-29 14:30부터 2026-07-01 09:00 최종 제출까지

이 문서는 최종 보고서나 발표자료가 아니다. 팀원이 지금 무엇이 끝났고, 남은 시간 동안 무엇을 우선해야 하는지 확인하기 위한 실행용 상태판이다.

## 목표

최소 목표는 수상권 진입이고, 상위 목표는 우승이다. 이를 위해 남은 시간은 새 아이디어를 무작정 늘리는 방향이 아니라, 재현 가능한 코드, 물리적 해석, 정량적 비교, 제출물 완성도를 동시에 끌어올리는 방향으로 쓴다.

## 현재 결론

Problem 1과 Problem 2는 baseline 구현과 diagnostic 출력이 준비된 상태다. Problem 3는 continuous projected denoising 후보가 현재 seed sweep 기준 main result로 사용할 수 있는 상태다.

다만 최종 제출 전까지는 다음 세 가지가 반드시 보강되어야 한다.

1. Problem 1/2가 문제 요구사항을 어떻게 만족하는지 정성 설명을 붙인다.
2. Problem 3의 이득과 한계를 모두 드러내는 figure/table을 고른다.
3. 코드와 결과를 팀원이 같은 명령으로 재현할 수 있게 마지막 QA를 통과시킨다.

## 현재 진행도

| Area | Current state | Evidence | Next owner |
| --- | --- | --- | --- |
| Repository setup | 완료 | PR/CI 기반 운영, issue 할당, Hermes task 구성 | 한지후 |
| Problem 1(a) | 구현 완료, 추가 설명 필요 | target ensemble 생성, cluster fidelity diagnostic | 임채진, 한지후 |
| Problem 1(b) | 구현 완료, 출력 보강 완료 | `MMD(S0,S0)=0`, `W(S0,S0)=0`, scrambled distance | 한지후 |
| Problem 1(c) | 구현 완료, 정성 해석 필요 | random-unitary distance curve, Bloch diagnostic | 임채진 |
| Problem 2(a) | 구현 완료, 물리 검증 필요 | Qiskit `SparsePauliOp`, 8개 Pauli term, Hermiticity error 0 | 김건우 |
| Problem 2(b) | 구현 완료, projection 설명 필요 | projection probability normalization diagnostic | 김건우 |
| Problem 2(c)/(d) | 비교 가능, 해석 보강 필요 | distance curve, reduced Bloch-vector plot | 김건우, 임채진 |
| Problem 3 | main candidate 가능 | 20/20 seeds `use_as_main`, median MMD/Wasserstein improvement 양수 | 한지후 |
| Quantitative evaluation | 실행 가능 | `python scripts/run_quantitative_evaluation.py` | 김승빈 |
| Final report story | 초안 전 단계 | claim/limitation evidence는 준비됨 | 임채진 |
| Result packaging | 후보 정리 필요 | generated `results/`는 commit하지 않음 | 김승빈 |
| Final QA | 남음 | `pytest`, `submission/run_all.py`, final pipeline | 전원 |

## 핵심 수치

Problem 1/2 diagnostic 기준:

| Metric | Value | Meaning |
| --- | --- | --- |
| mean fidelity from `S0` to `|00>` | `0.995692` | target ensemble이 `|00>` 주변 cluster임 |
| min fidelity from `S0` to `|00>` | `0.972637` | outlier가 크지 않음 |
| `MMD(S0,S0)` | `0` | metric sanity check 통과 |
| `Wasserstein(S0,S0)` | `0` | metric sanity check 통과 |
| `MMD(S1_random_unitary,S0)` | `0.882606` | random-unitary scrambling이 강하게 작동 |
| `Wasserstein(S1_random_unitary,S0)` | `0.733305` | baseline distance 증가 확인 |
| Problem 2 Hermiticity error | `0` | Hamiltonian matrix 검증 통과 |

Problem 3 seed sweep 기준:

| Metric | Value | Meaning |
| --- | --- | --- |
| Recommendation | `use_as_main` | 현재 main result로 사용 가능 |
| Passing seeds | `20/20` | 단일 seed 우연 가능성 낮음 |
| main-candidate rows | `81/120 = 0.675` | 탐색 후보 중 의미 있는 비율 |
| median MMD improvement | `0.097056` | target ensemble 쪽으로 이동 |
| median Wasserstein improvement | `0.147983` | transport cost 기준 개선 |
| median diversity retention | `0.823217` | collapse가 과하지 않음 |
| median success probability | `0.468122` | post-selection 성공률이 설명 가능한 범위 |
| median axis-only score margin | `0.010000` | 이득은 있으나 크지 않으므로 limitation에 명시 |

## 3일 로드맵

### Day 1 - 2026-06-29

| Time | Goal | Output | Owner |
| --- | --- | --- | --- |
| 14:30-16:00 | 문제 요구사항 분해, repo 운영 규칙 확정 | README, issue, branch/filename rule | 한지후 |
| 16:00-18:00 | Problem 1/2 baseline 실행 경로 확보 | Qiskit 기반 baseline, `submission/run_all.py` | 한지후, 김건우 |
| 18:00-20:00 | 코드 리뷰 반영, 출력/시각화 부족분 파악 | `docs/14_team_problem_status.md` | 전원 |
| 20:00-22:00 | Problem 1/2 diagnostic 및 정량 평가 보강 | `scripts/run_quantitative_evaluation.py` | 한지후 |
| 22:00-24:00 | Problem 3 후보 검증과 자동화 구성 | seed sweep, Hermes tasks | 한지후, 김승빈 |

### Day 2 - 2026-06-30

| Time | Goal | Output | Owner |
| --- | --- | --- | --- |
| 00:00-09:00 | 상시 Problem 3 automation 또는 중단 후 재개 준비 | `continuous-p3-improvement`, seed sweep log | 한지후 |
| 09:00-11:00 | 팀원 최신 변경사항 pull, conflict/check 실패 해결 | clean `main`, passing tests | 한지후 |
| 11:00-13:00 | Problem 1/2 정성 해석 완성 | cluster/scrambling/projection 설명 | 임채진, 김건우 |
| 13:00-16:00 | Problem 3 ablation, axis-only 비교, seed robustness 확정 | table/figure 후보 | 김승빈, 한지후 |
| 16:00-18:00 | 심사위원 관점 claim 검토 | claim, limitation, expected question list | 임채진 |
| 18:00-21:00 | 제출용 코드 경로와 재현 명령 고정 | final code map, command checklist | 한지후 |
| 21:00-24:00 | 보고서/발표자료에 넣을 근거 선별 | final figure/table shortlist | 전원 |

### Day 3 - 2026-07-01

| Time | Goal | Output | Owner |
| --- | --- | --- | --- |
| 00:00-03:00 | 새 기능 freeze, bug fix만 허용 | stable submission branch | 한지후 |
| 03:00-05:30 | 최종 보고서와 발표자료 생성 | report draft, slide draft | 임채진, 한지후 |
| 05:30-07:00 | 결과 재현 리허설 | clean clone 또는 clean env run log | 김승빈, 김건우 |
| 07:00-08:00 | 발표 Q&A 리허설 | 핵심 claim 3개, limitation 3개 | 전원 |
| 08:00-08:40 | 최종 제출물 패키징 | notebook/report/figures/code archive | 한지후, 김승빈 |
| 08:40-09:00 | 제출 확인 | 업로드 완료, 파일 열람 확인 | 전원 |

## 앞으로의 우선순위

남은 시간의 1순위는 Problem 3 성능을 더 크게 만드는 것이 아니라, 현재 성능이 왜 의미 있는지 심사위원이 빠르게 확인하도록 만드는 것이다.

1. `python scripts/run_quantitative_evaluation.py`를 다시 실행해 Problem 1/2 evidence를 최신 상태로 둔다.
2. `.\scripts\invoke_hermes_task.ps1 final-sync-fix -Yolo -MaxTurns 360`으로 팀원 변경사항 반영, test, pipeline 점검을 반복한다.
3. 김건우는 Problem 2 Hamiltonian term, qubit order, projection basis 설명을 검증한다.
4. 임채진은 Problem 1의 cluster/scrambling 설명과 Problem 3 limitation 문장을 정리한다.
5. 김승빈은 generated `results/`에서 보고서에 넣을 figure/table 후보를 재현 명령과 함께 정리한다.
6. 한지후는 PR/check/merge gate를 관리하고, 최종 제출용 코드 경로를 단순하게 유지한다.

## 자동화 명령

팀원 변경사항 반영, test, pipeline 점검:

```powershell
.\scripts\invoke_hermes_task.ps1 final-sync-fix -Yolo -MaxTurns 360
```

Problem 1/2 정량 진단:

```powershell
python scripts/run_quantitative_evaluation.py
```

빠른 제출 경로 확인:

```powershell
python submission/run_all.py --quick
python -m pytest
```

Problem 3 seed sweep를 PowerShell에서 보이는 방식으로 실행:

```powershell
.\scripts\run_problem_3_seed_sweep_visible.ps1
```

## 의사결정 기준

| Decision | Use this rule |
| --- | --- |
| Problem 3를 main result로 쓸지 | seed sweep가 계속 `use_as_main`이고 MMD/Wasserstein median improvement가 양수이면 사용 |
| 새 후보를 추가할지 | 기존 후보보다 정량 성능 또는 설명력이 명확히 좋아질 때만 추가 |
| axis-only 대비 이득이 작을 때 | 숨기지 말고 limitation으로 쓰고, continuous basis search의 안정성을 강조 |
| generated result를 commit할지 | 최종 제출에 필요한 선별 figure/table만 commit 후보로 검토 |
| 마지막 날 새 기능을 넣을지 | 2026-07-01 00:00 이후에는 bug fix와 문서 보강만 허용 |

## 최종 제출 전 체크리스트

| Check | Required state |
| --- | --- |
| `python -m pytest` | pass |
| `python submission/run_all.py --quick` | pass |
| Problem 1/2 diagnostic | 최신 결과 생성 가능 |
| Problem 3 summary | seed sweep와 limitation 문장 일치 |
| README | 실행 경로와 현재 진행도 최신 상태 |
| Report/slides | code output과 숫자가 불일치하지 않음 |
| 제출 파일 | 다른 PC에서 열람 가능 |

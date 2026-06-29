# Automation Feedback Loop

이 문서는 대회 수상/우승을 목표로 자동화가 무엇을 해야 하는지 정리한다.

## 목표

자동화의 목적은 코드를 대신 돌리는 것이 아니라, 매 반복마다 다음 질문에 답하게 만드는 것이다.

1. 현재 결과가 재현되는가?
2. Problem 3 main claim이 seed에 대해 안정적인가?
3. axis-only baseline 대비 이득이 충분한가?
4. 물리적 해석과 resource 설명이 과장되지 않았는가?
5. 지금 팀원이 해야 할 다음 일이 GitHub issue에 반영되어 있는가?

## 반복 루프

```text
실행
  -> tests, submission run, Problem 3 seed sweep
분석
  -> summary, median improvement, diversity, success probability
판단
  -> use_as_main / fallback_or_appendix
피드백
  -> report wording, physics caveat, figure/table TODO
할당
  -> GitHub issues update/create
반복
```

## 사용 명령

Problem 3를 상시 개선하는 명령:

```powershell
.\scripts\run_continuous_problem_3_automation.ps1 -KeepDisplayOff
```

이 명령은 `continuous-p3-improvement` Hermes task를 반복 실행한다. 각 cycle은 팀원 최신 변경 반영, 테스트, Problem 3 재실험, seed sweep, 결과 분석, 필요한 최소 수정, 검증, 상태 기록 순서로 진행된다.

기본 반복 간격은 90분이다. `-MaxCycles 0`은 종료 조건 없이 `Ctrl+C`까지 계속 돈다는 뜻이다. 상태는 `results/continuous_problem_3/latest_status.md`, 로그는 `logs/continuous_problem_3/`에 남긴다.

최종 표준 명령:

```powershell
.\scripts\run_competition_final_automation.ps1
```

이 명령 하나가 수행하는 일:

1. `origin/main` 최신 변경을 fetch/fast-forward 한다.
2. Problem 1/2 quantitative evaluation을 실행한다.
3. 제출용 `submission/run_all.py`와 20-seed Problem 3 sweep을 포함한 final pipeline을 실행한다.
4. GitHub issue 할당을 `docs/github_issue_plan.json` 기준으로 동기화한다.
5. `results/final_automation/latest_status.md`에 최종 status와 safe claim을 기록한다.
6. 중간 실패가 발생하면 Hermes watchdog의 `final-sync-fix` self-fix loop를 실행한 뒤 실패한 단계를 한 번 재시도한다.

화면은 꺼져도 되고 시스템만 깨어 있으면 충분할 때:

```powershell
.\scripts\run_competition_final_automation.ps1 -KeepDisplayOff
```

Hermes에게 전체 루프를 맡길 때:

```powershell
.\scripts\invoke_hermes_task.ps1 feedback-loop -Yolo -MaxTurns 260
```

마지막 제출 전 팀원 변경 반영과 실패 수정 루프까지 맡길 때:

```powershell
.\scripts\invoke_hermes_task.ps1 final-sync-fix -Yolo -MaxTurns 360
```

PowerShell에서 직접 보면서 돌릴 때:

```powershell
.\scripts\sync_latest_team_changes.ps1
.\scripts\run_final_pipeline_visible.ps1
.\scripts\sync_hackathon_issues.ps1 -Apply
```

이슈 할당을 수정할 때는 스크립트를 직접 고치지 않고 `docs/github_issue_plan.json`을 수정한다. 먼저 dry-run으로 생성/수정 대상을 확인한다.

```powershell
.\scripts\sync_hackathon_issues.ps1
```

## 현재 판단

현재까지의 핵심 결과는 Problem 3를 main result로 밀 수 있는 쪽이다.

- Default run: `use_as_main`
- 20-seed sweep: `20/20 use_as_main`
- main_candidate rows: `81/120 = 0.675`
- median MMD improvement: `0.097056`
- median Wasserstein improvement: `0.147983`
- median axis-only score margin: `0.010000`
- median diversity retention: `0.823217`
- median success probability: `0.468122`

다만 axis-only 대비 score margin은 크지 않으므로, 보고서에는 다음 trade-off를 같이 적는다.

- continuous basis가 axis-only보다 안정적으로 더 나은 후보를 찾았다.
- 하지만 toy state-vector 규모의 post-selected proxy이므로 hardware advantage나 general quantum advantage로 말하지 않는다.
- main claim은 "small-scale reproducible extension"과 "continuous measurement-basis search improves the denoising proxy"로 제한한다.

## 우승 방향성

이 방향은 수상/우승 전략에 맞다. 이유는 다음과 같다.

- Problem 1/2는 빠르게 재현 가능한 baseline으로 잠갔다.
- Problem 3는 다른 팀과 겹칠 수 있는 단순 metric sweep이 아니라, Problem 2의 complement projection을 continuous measurement-basis search로 확장했다.
- 20-seed robustness gate를 통과해 단일 seed 우연성 리스크를 줄였다.
- 제출용 `submission/` layer가 있어 심사자가 코드와 물리 흐름을 빠르게 확인할 수 있다.
- 자동화가 결과를 과장하지 않도록 `use_as_main` gate와 issue 재할당을 반복한다.

남은 승부처는 더 복잡한 알고리즘을 추가하는 것이 아니라, 결과를 설득력 있게 설명하고 약점을 먼저 통제하는 것이다.

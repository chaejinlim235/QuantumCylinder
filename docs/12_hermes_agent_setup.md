# Hermes Agent 연동 가이드

이 문서는 QuantumCylinder 저장소를 Hermes Agent와 함께 쓰기 위한 프로젝트 측 설정을 정리한다.

## 현재 연동 방식

저장소 루트에 `.hermes.md`를 둔다.

Hermes Agent는 이 파일을 프로젝트 context로 읽고 다음 정보를 사용한다.

- 현재 문제 진행도
- 실행 명령
- Problem 3 채택 게이트
- Git/PR 규칙
- 팀 역할
- 개인정보와 결과 파일 commit 규칙

## 설치

Hermes가 이미 설치되어 있지 않다면 Windows PowerShell에서 공식 설치 명령을 사용한다.

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

설치 후 새 터미널을 열고 확인한다.

```powershell
hermes --version
```

## 프로젝트에서 실행

저장소 루트에서 실행한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
hermes
```

Hermes에게 처음 줄 지시는 아래처럼 시작한다.

```text
Read .hermes.md and README.md first.
Use this repository's existing scripts and docs as the source of truth.
Do not commit generated results or private files.
For Problem 3, only treat a result as main if the adoption gate passes.
```

## 자동 실행 래퍼

반복 작업은 직접 프롬프트를 붙여 넣지 말고 래퍼를 사용한다.

```powershell
.\scripts\invoke_hermes_task.ps1 <task-name>
```

사용 가능한 task:

| Task | Purpose | Typical command |
| --- | --- | --- |
| `p3-status` | 테스트, git 상태, Problem 3 현재 결과 확인 | `.\scripts\invoke_hermes_task.ps1 p3-status` |
| `feedback-loop` | 최종 파이프라인 실행, 결과 분석, GitHub issue 재할당 반복 | `.\scripts\invoke_hermes_task.ps1 feedback-loop -Yolo -MaxTurns 260` |
| `final-pipeline` | 테스트, 제출용 실행, 20 seed sweep, 최종 claim 점검 자동 실행 | `.\scripts\invoke_hermes_task.ps1 final-pipeline -Yolo -MaxTurns 240` |
| `final-sync-fix` | 팀원 최신 변경 반영, 테스트/파이프라인 점검, 실패 시 최소 수정 루프 | `.\scripts\invoke_hermes_task.ps1 final-sync-fix -Yolo -MaxTurns 360` |
| `quantitative-evaluation` | Problem 1/2 진단, Hamiltonian/projection 확인, Bloch 시각화 생성 | `.\scripts\invoke_hermes_task.ps1 quantitative-evaluation -Yolo -MaxTurns 240` |
| `continuous-p3-improvement` | Problem 3 실험, 분석, 피드백, 검증을 상시 반복 | `.\scripts\invoke_hermes_task.ps1 continuous-p3-improvement -Yolo -MaxTurns 420` |
| `p3-seed-sweep` | 20개 seed 반복 실행과 robustness 요약 생성 | `.\scripts\invoke_hermes_task.ps1 p3-seed-sweep -Yolo -MaxTurns 180` |
| `p3-report-draft` | 실제 결과에 기반한 보고서 초안 생성 | `.\scripts\invoke_hermes_task.ps1 p3-report-draft -Yolo` |
| `p3-judge-review` | 심사자 관점의 약점과 개선 우선순위 점검 | `.\scripts\invoke_hermes_task.ps1 p3-judge-review` |

프롬프트 원문은 `.hermes/tasks/`에 둔다. task를 수정할 때는 실행 명령, 수정 허용 범위, 최종 응답 형식을 명확히 적는다.

Hermes가 PATH에 없다면 이 저장소의 래퍼는 Windows 기본 설치 경로도 자동으로 찾는다. 그래도 실패하면 직접 경로를 넘긴다.

```powershell
.\scripts\invoke_hermes_task.ps1 p3-status -HermesPath "C:\Users\sky_m\AppData\Local\Hermes\hermes-agent\venv\Scripts\hermes.exe"
```

장시간 seed sweep처럼 승인 프롬프트 없이 진행하고 싶은 작업에는 `-Yolo`를 붙인다. 코드 수정까지 허용되는 task에는 먼저 prompt의 허용 범위를 확인한다.

GitHub issue 자동 할당은 `docs/github_issue_plan.json`을 원본으로 삼는다. 실제 반영 전에는 dry-run을 먼저 확인한다.

```powershell
.\scripts\sync_hackathon_issues.ps1
.\scripts\sync_hackathon_issues.ps1 -Apply
```

마지막 전체 자동화는 팀원 변경 반영까지 포함하는 `final-sync-fix`를 사용한다.

```powershell
.\scripts\invoke_hermes_task.ps1 final-sync-fix -Yolo -MaxTurns 360
```

이 task는 먼저 `origin/main`을 fetch/fast-forward 하고, 로컬 변경과 incoming 변경이 같은 파일을 건드리면 멈춘다.

대회 제출 전 표준 자동화는 아래 명령 하나를 우선 사용한다.

```powershell
.\scripts\run_competition_final_automation.ps1
```

이 스크립트는 deterministic pipeline을 먼저 실행하고, 실패가 발생할 때만 Hermes watchdog을 통해 `final-sync-fix` self-fix loop를 호출한다.

Problem 3를 계속 개선해야 할 때는 상시 루프를 사용한다.

```powershell
.\scripts\run_continuous_problem_3_automation.ps1 -CycleMinutes 0 -KeepDisplayOff
```

이 루프는 `continuous-p3-improvement`를 cycle 사이 대기 없이 반복한다. `-MaxCycles 0`은 `Ctrl+C`로 중지할 때까지 계속 실행한다는 뜻이다. 상태는 `results/continuous_problem_3/latest_status.md`에 기록된다. 의도적으로 쉬게 만들 때만 `-CycleMinutes 30`처럼 값을 준다.

## 장시간 실행 watchdog

PowerShell이 자주 멈추거나 노트북 절전 때문에 실행이 끊기는 경우에는 `invoke_hermes_task.ps1`를 직접 실행하지 말고 watchdog 래퍼를 사용한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_hermes_watchdog.ps1 final-sync-fix -Yolo -MaxTurns 360 -Attempts 6
```

watchdog이 하는 일:

- 실행 중 시스템 절전과 화면 꺼짐을 막는다.
- QuickEdit/콘솔 선택으로 PowerShell이 멈추는 상황을 줄인다.
- Hermes 출력을 화면에 그대로 보여 주면서 `logs/hermes_automation/`에 저장한다.
- 일정 시간 출력이 없거나 Hermes가 실패하면 같은 task를 자동 재시도한다.
- `logs/hermes_automation/latest_state.json`에 현재 attempt, log path, exit code를 남긴다.

추천 기본값은 아래와 같다.

```powershell
.\scripts\run_hermes_watchdog.ps1 final-sync-fix -Yolo -MaxTurns 360 -Attempts 6 -IdleTimeoutMinutes 45
```

화면은 꺼져도 되고 시스템만 깨어 있으면 충분한 경우:

```powershell
.\scripts\run_hermes_watchdog.ps1 final-sync-fix -Yolo -MaxTurns 360 -Attempts 6 -KeepDisplayOff
```

기존 PowerShell 창에서 이미 Hermes가 실행 중이라면 그 프로세스를 강제로 종료하지 않는다. 현재 실행이 끝나길 기다리거나 직접 `Ctrl+C`로 중단한 뒤 watchdog 명령을 새 창에서 실행한다.

## 수동 요청 예시

Problem 3 seed sweep:

```text
Run the Problem 3 continuous denoising experiment for multiple seeds.
Summarize main_candidate/fallback_candidate counts and keep generated results out of Git.
```

보고서 보강:

```text
Read docs/11_problem_3_continuous_denoising.md and results/problem_3_continuous_denoising/problem_3_summary.md.
Draft concise Korean report paragraphs that describe the method, improvement, trade-off, and limitations.
Do not overclaim beyond the default run.
```

검증:

```text
Run python -m pytest and python scripts/run_problem_3_continuous_denoising.py.
Report the key result numbers and whether the adoption decision is use_as_main.
```

## 주의

- Hermes가 코드를 수정하면 반드시 `python -m pytest`를 실행한다.
- PR 본문은 가능하면 영어/ASCII로 쓴다.
- 한글 문서 파일 자체는 UTF-8로 작성한다.
- `results/` 아래 생성 파일은 기본적으로 commit하지 않는다.
- 신청서, 문제 원본 PDF, 개인정보가 포함된 파일은 commit하지 않는다.

## 현재 핵심 명령

```powershell
python scripts/run_problem_1_2_baselines.py
python scripts/run_problem_3_continuous_denoising.py
python scripts/problem_1_qiskit_resource_check.py
python -m pytest
```

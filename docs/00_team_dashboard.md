# Team Dashboard

이 문서는 대회 중 팀원이 먼저 확인할 단일 운영 문서다. 세부 문서는 필요할 때만 reference로 본다.

## 최신 스냅샷

- 기준 시각: `2026-06-29 22:10 KST`
- 로컬 `main`과 `origin/main`은 `1b95cd9` 기준으로 동기화되어 있다.
- PR #49 반영 이후 Problem 3 상시 자동화는 기본적으로 `attached` 모드로 실행된다. Hermes 출력이 실행 중인 PowerShell에 직접 표시되어야 한다.
- Problem 3 seed sweep gate는 `20/20 use_as_main`으로 유지한다.
- seed sweep 집계는 요청한 seed 목록만 집계하도록 보정한다. 오래된 `seed_<n>` 결과 폴더가 남아 있어도 최신 sweep 결과에 섞이지 않아야 한다.

## 먼저 볼 것

| Purpose | File |
| --- | --- |
| 현재 진행도, 역할, 실행 명령 | `docs/00_team_dashboard.md` |
| 저장소 구조와 실행 entry point | `README.md` |
| 자동화 실행 중 상태 | `results/continuous_problem_3/latest_status.md` |
| 자동화 실행 중 변화 기록 | `results/continuous_problem_3/progress_log.md` |

`results/` 아래 파일은 생성물이라 Git에 커밋하지 않는다.

## 현재 판단

| Area | Status | Owner | Next action |
| --- | --- | --- | --- |
| Problem 1 | locked | 한지후 | 정성 설명과 diagnostic 출력만 유지 |
| Problem 2 | locked | 한지후, 김건우 | Hamiltonian/projection 해석 검수 |
| Problem 3 | main candidate | 한지후 | 성능 claim보다 재현성, limitation, figure/table 강화 |
| Seed sweep | passed + aggregation guarded | 김승빈 | 최종 표/그림 후보 정리, 오래된 seed 결과 혼입 여부 확인 |
| Report/story | evidence ready | 임채진 | claim, limitation, 발표 흐름 정리 |
| Automation | attached continuous loop | 한지후 | 실행 중 PowerShell 출력, status/progress log 확인 |

Problem 3의 현재 안전한 주장은 다음 범위로 제한한다.

- 20-seed sweep 기준 `20/20 use_as_main`.
- median MMD improvement `0.097056`.
- median Wasserstein improvement `0.147983`.
- axis-only score margin은 `0.010000`으로 작으므로 limitation에 적는다.
- hardware advantage나 general quantum advantage로 주장하지 않는다.

## 지금 실행할 명령

Problem 3를 계속 개선할 때:

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_continuous_problem_3_automation.ps1 -CycleMinutes 0 -KeepDisplayOff
```

정상 시작 시 실행 PowerShell에 아래 문구가 보여야 한다.

```text
Hermes run mode: attached
Attached Hermes attempt 1/2 started. Live output is shown in this PowerShell.
```

진행 상황 확인:

```powershell
Get-Content results\continuous_problem_3\latest_status.md -Wait -Tail 80
Get-Content results\continuous_problem_3\progress_log.md -Wait -Tail 120
Get-Content logs\continuous_problem_3\latest_state.json
```

PowerShell이 바로 닫히는지 확인해야 할 때:

```powershell
powershell -NoProfile -NoExit -ExecutionPolicy Bypass -File .\scripts\run_continuous_problem_3_automation.ps1 -CycleMinutes 0 -KeepDisplayOff
```

멈춘 실행 정리 후 재시작:

```powershell
.\scripts\stop_continuous_problem_3_automation.ps1
.\scripts\run_continuous_problem_3_automation.ps1 -CycleMinutes 0 -KeepDisplayOff
```

제출 전 전체 검증:

```powershell
.\scripts\run_competition_final_automation.ps1
```

짧은 로컬 확인:

```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/run_problem_3_continuous_denoising.py
```

## 역할

| Member | Role | Output |
| --- | --- | --- |
| 한지후 | 핵심 구현, 통합, PR/check, 자동화 운영 | main branch 안정화, Problem 3 gatekeeping |
| 김건우 | Qiskit/resource/물리 검증 | Hamiltonian, projection, resource 설명 |
| 임채진 | 문제/논문 해석, 보고서 claim | 최종 claim, limitation, 발표 흐름 |
| 김승빈 | 실행 재현, seed sweep, figure/table | 결과 표/그림 후보와 로그 정리 |

## Decision Gates

Problem 3를 main으로 유지하는 조건:

- seed sweep recommendation이 `use_as_main`.
- MMD 또는 Wasserstein improvement가 양수.
- diversity retention과 success probability가 설명 가능.
- axis-only comparison을 숨기지 않고 limitation으로 적음.

새 후보가 이 기준을 넘지 못하면 main으로 쓰지 않고 candidate/appendix에만 남긴다.

## Reference Docs

필요할 때만 본다.

| Topic | File |
| --- | --- |
| Problem 1/2 풀이와 출력 | `docs/07_problem_1_2_solution.md` |
| Problem 1/2 코드 읽는 순서 | `docs/17_problem_1_2_code_reading_guide.md` |
| Qiskit 검증 | `docs/09_qiskit_validation_layer.md` |
| Problem 3 방법과 gate | `docs/11_problem_3_continuous_denoising.md` |
| Hermes 세부 설정 | `docs/12_hermes_agent_setup.md` |
| 자동화 운영 원칙 | `docs/13_automation_feedback_loop.md` |
| 3일 로드맵 | `docs/16_three_day_roadmap.md` |
| GitHub issue 원본 | `docs/github_issue_plan.json` |

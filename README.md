# QuantumCylinder

2026 양자정보경진대회 Technical Challenge, Quantum Machine Learning 지정문제 3번을 위한 팀 저장소입니다.

팀명은 **양자실린더 / QuantumCylinder**입니다. 대회 목표는 수상권 이상이며, 가능하면 우승까지 목표로 합니다. 이 저장소는 그 목표를 위해 재현 가능한 실험 코드와 문서를 관리합니다.

## First Docs To Check

대회 중에는 아래 문서만 먼저 확인합니다. 나머지 문서는 필요할 때만 reference로 봅니다.

| Need | File |
| --- | --- |
| 현재 진행도, 역할, 실행 명령 | `docs/00_team_dashboard.md` |
| 밤샘 Problem 3 실험의 과정/근거/결론 | `docs/22_overnight_problem_3_evidence_handoff.md` |
| 저장소 구조와 code map | `README.md` |
| 실제 GitHub issue 동기화 원본 | `docs/github_issue_plan.json` |
| Problem 3 seed sweep 요약 | `results/problem_3_seed_sweep/seed_sweep_summary.md` |
| 김승빈 support worker 결과 | `docs/experiments/2026-06-30_problem_3_seungbin_support_worker_results.md` |

`results/` 아래 파일은 실행 중 생성되는 기록이며 Git에 커밋하지 않습니다.

## Maintenance Contract

앞으로 코드, notebook, issue, 역할, 자동화, 파일 구조가 바뀌면 반드시 같은 변경 안에서 아래 항목을 함께 갱신합니다.

| 변경 종류 | 같이 갱신할 것 | 확인 명령 |
| --- | --- | --- |
| 담당자/할 일 변경 | `README.md`의 Current Issue Assignments, `docs/github_issue_plan.json`, 실제 GitHub issue | `.\scripts\sync_hackathon_issues.ps1 -Apply` |
| 파일/폴더 추가 또는 삭제 | `README.md`의 Repository Structure와 Code Map | `rg --files` |
| 문제별 진행도 변경 | `README.md`의 Subproblem Completion Matrix와 Current Progress | `python -m pytest` |
| Problem 3 결과/claim 변경 | `docs/22_overnight_problem_3_evidence_handoff.md`, README의 관련 수치/limitation | `python scripts\summarize_problem_3_seed_sweep.py` |
| 최종 보고서/notebook 변경 | README issue table, #6/#8/#19/#32 issue body | GitHub issue 확인 |

README, `docs/github_issue_plan.json`, 실제 GitHub issue가 서로 다른 말을 하면 README를 신뢰하지 않습니다. 이 경우 먼저 세 파일을 맞춘 뒤 다음 작업을 진행합니다.

## Current Progress

팀 운영 기준은 "한지후가 핵심 코드 구현과 통합을 맡고, 나머지 팀원은 해석, 검증, 환경 안정화, 결과 정리에 집중한다"입니다.

현재 진행도와 역할은 `docs/00_team_dashboard.md`에서 먼저 확인하고, 3일 전체 로드맵은 필요할 때 `docs/16_three_day_roadmap.md`에서 확인합니다.

## Subproblem Completion Matrix

아래 표는 지정문제 PDF의 세부 소문항 기준으로 현재 실험과 보고서/해석 준비도를 나눈 상태판입니다. `실험`은 실행 가능한 코드와 결과 산출 여부, `보고서`는 최종 notebook/report에 바로 넣을 수 있는 설명과 figure/table 준비도를 뜻합니다.

| Subproblem | 요구사항 요약 | 실험 | 보고서 | 근거/entry point | 남은 일 |
| --- | --- | --- | --- | --- | --- |
| 1(a) | `|00>` 주변 2-qubit target ensemble `S0` 생성 | 완료 | 보강 필요 | `scripts/problem_1a_generate_target_ensemble.py`, `src/quantum_cylinder/problem_1a_target_ensemble.py` | cluster fidelity와 `N=80`, `sigma=0.10` 선택 이유를 최종 보고서에 명시 |
| 1(b) | fidelity, MMD, Wasserstein-type distance 정의/계산 | 완료 | 거의 완료 | `scripts/problem_1b_check_metrics.py`, `results/quantitative_evaluation/problem_1b_metric_diagnostics.md` | 수식 정의와 `MMD(S0,S0)=0`, `W(S0,S0)=0` sanity check를 notebook에 반영 |
| 1(c) | random-unitary forward diffusion, 거리 plot, cluster 변화 설명 | 완료 | 보강 필요 | `scripts/run_problem_1_2_baselines.py`, `results/problem_1_2_baseline/distance_curves.png` | strong-scrambling baseline이라는 정성 설명과 cluster 변화 figure 선택 |
| 2(a) | 3-qubit fixed Hamiltonian 구성 | 완료 | 검수 필요 | `scripts/problem_2a_print_hamiltonian.py`, `results/quantitative_evaluation/problem_2a_hamiltonian_diagnostics.md` | 김건우가 qubit order, Pauli terms, Hermiticity 설명 최종 검수 |
| 2(b) | Hamiltonian evolution 후 complement qubit projection ensemble 생성 | 완료 | 검수 필요 | `scripts/problem_2b_projection_diagnostics.py`, `results/quantitative_evaluation/problem_2b_projection_diagnostics.md` | auxiliary/complement qubit 측정 후 조건부 상태가 되는 과정을 보고서에 명확히 설명 |
| 2(c) | `dist(S_t^Ham,S0)` plot 및 random-unitary와 정성 비교 | 완료 | 보강 필요 | `scripts/problem_2c_plot_bloch_comparison.py`, `results/quantitative_evaluation/problem_2c_bloch_summary.md` | `k`와 `t`를 같은 x축으로 비교하지 않는다는 점, reduced Bloch-vector figure 해석 추가 |
| 2(d) | comparable diffusion strength에서 resource/control-cost proxy 비교 | 완료 | 보강 필요 | `results/problem_1_2_baseline/comparable_strength_resource_matches.csv`, `docs/15_quantitative_evaluation_plan.md` | "절대 우위"가 아니라 random control cost와 fixed-control/time schedule trade-off로 서술 |
| 3(a) | toy reverse/denoising step 시연 | 완료 | 거의 완료 | `scripts/run_problem_3_continuous_denoising.py`, `submission/problem3_continuous_measurement_denoising.py` | fixed measurement-induced non-unitary map이라는 제한과 near-zero post-selection 후보 제외 기준을 명확히 표기 |
| 3(b) | diffusion setting controlled modification 및 trade-off 분석 | 완료 | 거의 완료 | `results/problem_3_seed_sweep/seed_sweep_summary.md`, `results/problem_3_frozen_parameter_holdout/frozen_holdout_summary.md` | continuous basis search의 이득과 axis-only margin이 작다는 limitation을 함께 제시 |
| 3(c) | 개선안 제안, baseline과 작은 예제로 비교 | 완료 | 보강 필요 | `docs/22_overnight_problem_3_evidence_handoff.md`, `results/problem_3_baseline_collapse_defense/baseline_collapse_summary.md` | hybrid 2-qubit extension은 front-facing extension으로만 사용하고 hardware advantage 주장은 금지 |

현재 판단: Problem 1/2/3의 **실험 코드는 전 소문항 기준으로 실행 가능**합니다. 최종 경쟁력은 남은 코드 추가보다, 1(c), 2(b), 2(c), 2(d), 3(b), 3(c)의 **정성 해석과 limitation 문장**을 얼마나 정확히 보고서에 옮기는지에 달려 있습니다.

| Area | Status | Owner | Next action |
| --- | --- | --- | --- |
| Repository setup | Done | 한지후 | PR 단위 변경과 자동 CI 유지 |
| 3-day roadmap | Added | 전원 | `docs/16_three_day_roadmap.md` 기준으로 Day 2/Day 3 작업 진행 |
| Problem 1 baseline | Validated + diagnostics generated | 한지후 | 1(b) metric sanity와 cluster fidelity 수치를 팀 검토에 사용 |
| Problem 2 baseline | Validated + diagnostics generated | 한지후 | Hamiltonian/projection/Bloch 진단 결과를 물리 해석에 반영 |
| CI/local tests | Passing | 한지후 | 모든 코드 PR 전 `pytest`와 GitHub Actions 확인 |
| Qiskit validation layer | Available | 김건우 | `problem_1_qiskit_resource_check.py` 기준으로 gate/depth 표 정리 |
| Submission layer | Done | 한지후 | `submission/run_all.py`를 심사자용 entry point로 유지 |
| Problem 3 extension | Validated main candidate | 한지후 | 새 기능 추가보다 claim/figure/reproducibility 안정화 |
| Problem 3 overnight evidence | Harvested | 한지후, 김승빈 | `docs/22_overnight_problem_3_evidence_handoff.md` 기준으로 보고서/발표 반영 |
| Problem 3 physical interpretation | In progress | 김승빈 | measurement-induced denoising proxy와 hybrid extension 해석 문장 작성 |
| Problem 3 seed sweep | Done + independently reproduced | 김승빈 | support worker 결과에서 figure/table 후보와 재현 로그 정리 |
| Quantitative evaluation | Generated and handed off | 한지후 | `docs/experiments/2026-06-29_quantitative_evaluation_handoff.md` 기준으로 팀원 검토 |
| Code/Qiskit consistency review | In progress | 김건우 | notebook 설명과 실제 Qiskit/backend 구현이 충돌하지 않는지 검수 |
| Final ipynb report/story | In progress | 임채진 | 1/2번 notebook 형식 유지, 3번 섹션과 limitation 문장 정리 |
| Result packaging | Ready for review | 김승빈 | quantitative evaluation figure/table 후보 재현 및 패키징 |
| Issue/repo metadata sync | Required every change | 한지후 | README, `docs/github_issue_plan.json`, 실제 GitHub issue를 같은 상태로 유지 |

## Current Issue Assignments

| Issue | Owner | Status | Purpose |
| --- | --- | --- | --- |
| #6 | 임채진 | Open | ipynb 최종 보고서 작성 및 claim/storyline 확정 |
| #8 | 김승빈 | Open | 물리적 해석, figure/table 패키징 및 재현 로그 정리 |
| #19 | 김건우 | Open | 코드/Qiskit 구현 해석 및 consistency 검수 |
| #31 | 한지후 | Open | Hermes feedback loop 운영 및 최종 gatekeeping |
| #32 | 전원 | Open | 최종 제출 리허설 및 QA 체크리스트 |
| #7 | 김건우 | Closed | Problem 1/2 구현 검증 및 resource proxy 정리 완료 |
| #9 | 한지후 | Closed | Problem 3 continuous denoising 구현 완료 |

GitHub issue의 source of truth는 `docs/github_issue_plan.json`입니다. 이 표를 바꾸면 반드시 `.\scripts\sync_hackathon_issues.ps1 -Apply`를 실행해 실제 GitHub issue와 동기화합니다.

## Project Scope

이 저장소는 지정문제 3번의 세 요구를 작은 state-vector 실험으로 재현하고 비교합니다.

1. **Problem 1 - Random-unitary scrambling**
   - `|00>` 주변의 2-qubit target ensemble 생성
   - random single-qubit rotations + entangler 기반 forward diffusion
   - fidelity-based MMD와 infidelity-cost Wasserstein-type distance 계산

2. **Problem 2 - Hamiltonian projected diffusion**
   - 2-qubit data system에 1 complement qubit 추가
   - 고정 Hamiltonian time evolution 후 complement qubit projection
   - Problem 1과 같은 metric으로 diffusion curve 비교

3. **Problem 3 - Further extension**
   - continuous measurement-induced toy denoising step
   - `Z/X/Y` axis-only baseline 대비 continuous projection basis 탐색
   - 성능이 나오지 않으면 main result가 아니라 후보/부록으로 분리

## Tech Stack

- Python 3.11+
- NumPy, SciPy
- Qiskit
- Matplotlib
- pytest

현재 기본 baseline은 Qiskit의 `QuantumCircuit`, `Statevector`, `SparsePauliOp`를 사용해 회로와 Hamiltonian을 구성합니다. 기존 NumPy/SciPy 구현은 독립 backend로 보관하고, 별도 resource proxy 확인은 `scripts/problem_1_qiskit_resource_check.py`로 수행합니다.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/run_problem_1_2_baselines.py
pytest
```

기본 결과는 `results/problem_1_2_baseline/`에 생성됩니다. `results/`의 CSV/PNG/JSON은 기본적으로 Git에 커밋하지 않습니다.

Qiskit 검증이 필요한 팀원은 아래 명령을 추가로 실행합니다.

```powershell
pip install -e ".[qiskit]"
python scripts/problem_1_qiskit_resource_check.py
```

## Hermes Automation

Hermes Agent task prompt는 `.hermes/tasks/`에 있습니다. 현재 기본 운영은 새 실험을 무한히 늘리는 것이 아니라, 밤샘 자동화로 수확한 evidence를 보고서, figure/table, limitation, GitHub issue에 정확히 반영하는 것입니다.

필요할 때만 아래 래퍼로 단일 task를 실행합니다.

```powershell
.\scripts\invoke_hermes_task.ps1 p3-status
.\scripts\invoke_hermes_task.ps1 final-pipeline -Yolo -MaxTurns 240
.\scripts\invoke_hermes_task.ps1 final-sync-fix -Yolo -MaxTurns 360
.\scripts\invoke_hermes_task.ps1 quantitative-evaluation -Yolo -MaxTurns 240
.\scripts\invoke_hermes_task.ps1 problem-3-finalist-autopilot -Yolo -MaxTurns 620
.\scripts\invoke_hermes_task.ps1 p3-seed-sweep -Yolo -MaxTurns 180
.\scripts\invoke_hermes_task.ps1 p3-report-draft -Yolo
.\scripts\invoke_hermes_task.ps1 p3-judge-review
.\scripts\invoke_hermes_task.ps1 p3-defense-evidence
```

- `p3-status`: 테스트, git 상태, Problem 3 결과 요약 확인
- `final-pipeline`: 테스트, 제출용 실행, 20 seed sweep, 최종 claim 점검 자동 실행
- `final-sync-fix`: 팀원 최신 변경 반영, 테스트/파이프라인 점검, 실패 시 최소 수정 루프
- `quantitative-evaluation`: Problem 1/2 diagnostic, Bloch visualization, resource evidence 생성
- `problem-3-finalist-autopilot`: finalist 관점의 Problem 3 evidence 개선 및 guardrail 점검
- `p3-seed-sweep`: 20개 seed 반복 실행과 robustness 요약 생성
- `p3-report-draft`: 실제 결과에 기반한 Problem 3 보고서 초안 작성
- `p3-judge-review`: 심사자 관점의 claim 리스크 점검
- `p3-defense-evidence`: 발표 Q&A 방어 근거 정리

자세한 사용법은 `docs/12_hermes_agent_setup.md`에 정리합니다.

## Automated Feedback Loop

대회 수상/우승을 위한 자동화 목표는 단순 실행이 아니라 `실행 -> 분석 -> 판단 -> 피드백 -> 문서/issue 동기화` 반복입니다. 지금은 충분한 밤샘 cycle을 수확한 뒤이므로 기본 전략을 `추가 탐색`에서 `evidence 안정화`로 옮겼습니다.

Problem 3 후보를 다시 개선해야 할 때만 finalist autopilot을 사용합니다.

```powershell
.\scripts\run_problem_3_finalist_autopilot.ps1 -CycleMinutes 0 -KeepDisplayOff
```

실행이 stale lock 상태로 멈췄으면 아래처럼 정리한 뒤 다시 실행합니다.

```powershell
.\scripts\stop_problem_3_finalist_autopilot.ps1
.\scripts\run_problem_3_finalist_autopilot.ps1 -CycleMinutes 0 -KeepDisplayOff
```

최종 표준 자동화는 아래 명령 하나를 사용합니다.

```powershell
.\scripts\run_competition_final_automation.ps1
```

이 명령은 팀원 변경 sync, Problem 1/2 정량 진단, 최종 제출 파이프라인, 20-seed Problem 3 sweep, GitHub issue sync, 최종 status report 생성을 순서대로 수행합니다. 중간 실패가 발생하면 Hermes watchdog의 `final-sync-fix` self-fix loop를 실행한 뒤 실패한 단계를 한 번 재시도합니다.

결과 요약은 `results/final_automation/latest_status.md`에 생성됩니다.

```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/summarize_problem_3_seed_sweep.py
```

마지막 전체 자동화는 팀원 변경 반영과 실패 수정까지 포함하는 아래 명령을 사용합니다.

```powershell
.\scripts\invoke_hermes_task.ps1 final-sync-fix -Yolo -MaxTurns 360
```

PowerShell이 절전, 콘솔 선택, 장시간 무출력 상태 때문에 멈추는 경우에는 watchdog 래퍼를 사용합니다. 이 명령은 절전을 막고, 로그를 남기고, Hermes가 실패하거나 오래 응답하지 않으면 재시도합니다.

```powershell
.\scripts\run_hermes_watchdog.ps1 final-sync-fix -Yolo -MaxTurns 360 -Attempts 6
```

현재 Problem 3는 20-seed sweep에서 `20/20 use_as_main`이며, main result claim이 가능한 상태입니다. 다만 axis-only 대비 median score margin이 `0.010000`으로 크지 않으므로, 최종 보고서에서는 continuous basis search의 이득과 post-selection toy proxy라는 limitation을 함께 적습니다.

seed sweep 집계는 실행한 seed 목록만 요약하도록 관리합니다. 오래된 `results/problem_3_seed_sweep/seed_<n>` 폴더가 남아 있으면 최신 sweep에 섞이지 않도록 `run_problem_3_seed_sweep_visible.ps1`가 seed 목록을 요약 스크립트에 전달합니다.

GitHub issue 자동 할당의 원본은 `docs/github_issue_plan.json`입니다. 이 파일을 수정한 뒤 `.\scripts\sync_hackathon_issues.ps1`로 dry-run을 확인하고, 문제가 없을 때 `.\scripts\sync_hackathon_issues.ps1 -Apply`를 실행합니다.

자세한 운영 기준은 `docs/13_automation_feedback_loop.md`에 정리합니다.

## Simple Submission Layer

물리적 해석과 코드 흐름을 빠르게 확인하려면 `submission/`을 먼저 봅니다.

```powershell
python submission/run_all.py --quick
python submission/run_all.py
```

`submission/`은 제출/발표용으로 문제별 핵심 흐름만 얇게 묶은 폴더입니다. 검증된 실제 구현은 `src/quantum_cylinder/`에 유지하고, `submission/`은 심사자와 팀원이 먼저 읽기 쉬운 entry point 역할을 합니다.

## Visible Problem 3 Run

Hermes 내부 실행 로그보다 seed별 진행을 PowerShell에서 직접 보고 싶으면 아래 명령을 사용합니다.

```powershell
.\scripts\run_problem_3_seed_sweep_visible.ps1
```

짧게 확인하려면:

```powershell
.\scripts\run_problem_3_seed_sweep_visible.ps1 -Seeds 1,2 -SkipTests -OutputRoot results/problem_3_seed_sweep_visible_check
```

전체 자동 파이프라인을 PowerShell에서 직접 돌리려면:

```powershell
.\scripts\run_final_pipeline_visible.ps1
```

## Code Map

문제별 실행 파일과 핵심 구현 파일은 아래와 같습니다.

| Problem | Purpose | Entry point | Core implementation |
| --- | --- | --- | --- |
| simple submission | 문제별 제출용 단순 실행 | `submission/run_all.py` | `submission/problem*.py` |
| 1(a) | target ensemble 생성 | `scripts/problem_1a_generate_target_ensemble.py` | `src/quantum_cylinder/problem_1a_target_ensemble.py` |
| 1(b) | fidelity, MMD, Wasserstein metric | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_1b_ensemble_metrics.py` |
| 1(c) | random-unitary diffusion | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_1c_random_unitary_diffusion.py` |
| 2(a) | Hamiltonian 출력 및 Hermiticity 확인 | `scripts/problem_2a_print_hamiltonian.py` | `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py` |
| 2(b) | projection/conditional state 진단 | `scripts/problem_2b_projection_diagnostics.py` | `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py` |
| 2(c) | Bloch 구면 비교 시각화 | `scripts/problem_2c_plot_bloch_comparison.py` | `src/quantum_cylinder/bloch_vectors.py` |
| 2(d) | Hamiltonian projected diffusion baseline | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py` |
| 3 | continuous projected denoising | `scripts/run_problem_3_continuous_denoising.py` | `src/quantum_cylinder/problem_3_continuous_projected_denoising.py` |
| 3 hybrid | random-unitary + Hamiltonian hybrid toy | `scripts/run_problem_3_hybrid_diffusion_toy.py` | `src/quantum_cylinder/problem_3_continuous_projected_denoising.py` |
| 3 frozen holdout | frozen-parameter holdout 검증 | `scripts/summarize_problem_3_frozen_holdout.py` | `results/problem_3_seed_sweep/` |
| 3 collapse table | baseline/collapse guardrail 정리 | `scripts/summarize_problem_3_baseline_collapse_table.py` | `results/problem_3_seed_sweep/` |
| 3 sweep | seed sweep summary | `scripts/summarize_problem_3_seed_sweep.py` | `results/problem_3_seed_sweep/` |
| 3 visible sweep | seed별 진행 확인 | `scripts/run_problem_3_seed_sweep_visible.ps1` | `results/problem_3_seed_sweep/` |
| finalist autopilot | Problem 3 실험, 분석, 검증, evidence 개선 루프 | `scripts/run_problem_3_finalist_autopilot.ps1` | `results/problem_3_finalist_autopilot/latest_status.md` |
| support worker | 보조 노트북용 Problem 3 독립 반복 실행 | `scripts/run_problem_3_support_worker.ps1` | `docs/experiments/2026-06-30_problem_3_seungbin_support_worker_results.md` |
| final visible pipeline | 테스트, 제출용 실행, seed sweep 전체 자동화 | `scripts/run_final_pipeline_visible.ps1` | `results/` |
| final competition automation | sync, quantitative evaluation, final pipeline, issue sync, status report 전체 자동화 | `scripts/run_competition_final_automation.ps1` | `results/final_automation/latest_status.md` |
| quantitative evaluation | 1/2번 진단, Hamiltonian/projection 확인, Bloch 시각화 | `scripts/run_quantitative_evaluation.py` | `results/quantitative_evaluation/` |
| team sync | 팀원 최신 변경 fetch/fast-forward 및 로컬 충돌 사전 점검 | `scripts/sync_latest_team_changes.ps1` | `origin/main` |
| issue sync | 현재 진행도 기반 GitHub issue 동기화 | `scripts/sync_hackathon_issues.ps1` | `docs/github_issue_plan.json` |
| 1/2 common | baseline curve, CSV, plot 생성 | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/experiment_curves.py` |
| 1/2 reading guide | Problem 1/2 코드 읽는 순서 | `docs/17_problem_1_2_code_reading_guide.md` | `scripts/run_problem_1_2_baselines.py` |
| Qiskit validation | circuit resource proxy | `scripts/problem_1_qiskit_resource_check.py` | Qiskit `QuantumCircuit` |

Problem 1(a), 1(c), 2의 기본 import 경로는 Qiskit 구현을 re-export합니다. Qiskit 구현은 `src/quantum_cylinder/implementations/qiskit/`에, 기존 NumPy/SciPy 구현은 `src/quantum_cylinder/implementations/numpy/`에 폴더로 분리 보관합니다. 두 폴더는 독립 구현으로 취급하며, 서로 결과 parity를 맞추는 계약은 두지 않습니다.

## Repository Structure

```text
.
|-- .hermes/
|   `-- tasks/                 # Hermes Agent automation prompts
|-- configs/
|   |-- problem_1_2_baseline.json
|   `-- problem_3_continuous_denoising.json
|-- data/
|   `-- raw/                   # private/raw files. Do not commit contents.
|-- docs/
|   |-- 00_problem_brief.md
|   |-- 00_team_dashboard.md
|   |-- 01_team_roles.md
|   |-- 02_roadmap.md
|   |-- 03_experiment_protocol.md
|   |-- 04_extension_ideas.md
|   |-- 05_hackathon_execution_plan.md
|   |-- 06_paper_triage.md
|   |-- 07_problem_1_2_solution.md
|   |-- 08_test_environment.md
|   |-- 09_qiskit_validation_layer.md
|   |-- 10_llm_development_guide.md
|   |-- 11_problem_3_continuous_denoising.md
|   |-- 12_hermes_agent_setup.md
|   |-- 13_automation_feedback_loop.md
|   |-- 14_team_problem_status.md
|   |-- 15_quantitative_evaluation_plan.md
|   |-- 16_three_day_roadmap.md
|   |-- 17_problem_1_2_code_reading_guide.md
|   |-- 18_day2_finalist_strategy.md
|   |-- 19_problem_3_finalist_autopilot.md
|   |-- 20_problem_3_support_worker.md
|   |-- 21_problem_3_harvest_summary.md
|   |-- 22_overnight_problem_3_evidence_handoff.md
|   |-- experiments/
|   `-- github_issue_plan.json
|-- notebooks/
|   `-- problem_1_2_metric_aligned_latest.ipynb
|-- results/                  # generated experiment outputs; ignored by default
|-- submission/
|   |-- problem1_random_unitary_scrambling.py
|   |-- problem2_hamiltonian_projection.py
|   |-- problem3_continuous_measurement_denoising.py
|   |-- run_all.py
|   `-- states_and_metrics.py
|-- scripts/
|   |-- bootstrap_problem_3_support_worker.ps1
|   |-- invoke_hermes_task.ps1
|   |-- problem_1a_generate_target_ensemble.py
|   |-- problem_1b_check_metrics.py
|   |-- problem_1_qiskit_resource_check.py
|   |-- problem_2a_print_hamiltonian.py
|   |-- problem_2b_projection_diagnostics.py
|   |-- problem_2c_plot_bloch_comparison.py
|   |-- run_competition_final_automation.ps1
|   |-- run_continuous_problem_3_automation.ps1
|   |-- run_day2_finalist_automation.ps1
|   |-- run_final_pipeline_visible.ps1
|   |-- run_hermes_watchdog.ps1
|   |-- run_problem_1_2_baselines.py
|   |-- run_problem_3_continuous_denoising.py
|   |-- run_problem_3_finalist_autopilot.ps1
|   |-- run_problem_3_hybrid_diffusion_toy.py
|   |-- run_problem_3_seed_sweep_visible.ps1
|   |-- run_problem_3_support_worker.ps1
|   |-- run_quantitative_evaluation.py
|   |-- stop_continuous_problem_3_automation.ps1
|   |-- stop_problem_3_finalist_autopilot.ps1
|   |-- stop_problem_3_support_worker.ps1
|   |-- summarize_problem_3_baseline_collapse_table.py
|   |-- summarize_problem_3_frozen_holdout.py
|   |-- summarize_problem_3_seed_sweep.py
|   |-- sync_hackathon_issues.ps1
|   `-- sync_latest_team_changes.ps1
|-- src/quantum_cylinder/
|   |-- bloch_vectors.py
|   |-- experiment_curves.py
|   |-- implementations/
|   |   |-- numpy/             # original NumPy/SciPy baseline implementations
|   |   `-- qiskit/            # Qiskit-backed baseline implementations
|   |-- problem_1a_target_ensemble.py
|   |-- problem_1b_ensemble_metrics.py
|   |-- problem_1c_random_unitary_diffusion.py
|   |-- problem_2_hamiltonian_projected_diffusion.py
|   `-- problem_3_continuous_projected_denoising.py
`-- tests/
    |-- test_problem_1_2_baselines.py
    |-- test_problem_3_baseline_collapse_table.py
    |-- test_problem_3_continuous_summary.py
    |-- test_problem_3_frozen_parameter_holdout.py
    |-- test_problem_3_seed_sweep_summary.py
    `-- test_submission_layer.py
```

## Team Roles

| Member | Primary responsibility | Background fit | Near-term output |
| --- | --- | --- | --- |
| 한지후 | 핵심 코드 구현, 통합, gatekeeping, issue/repo metadata sync | MVP 해커톤 경험을 빠른 구현, 자동화 운영, 일정 조율에 활용하고 양자물리 해석은 팀 검증을 받음 | main branch 안정화, README/issue 동기화, 최종 claim 숫자 관리 |
| 김건우 | 코드/Qiskit 구현 해석 및 consistency 검수 | 구현을 직접 읽고 notebook 설명, Qiskit/backend 사용 위치, resource proxy가 충돌하지 않는지 확인 | Problem 1/2/3 코드 해석 문장, conditional state와 x축 비교 검수 |
| 임채진 | ipynb 최종 보고서 작성 및 storyline 정리 | 현재 notebook 형식을 유지하면서 문제별 답변, figure, limitation을 보고서 문체로 연결 | 1/2번 완성본 형식 유지, 3번 소문항별 답변 추가, 최종 claim 정리 |
| 김승빈 | 물리적 해석, figure/table 패키징, 재현 로그 정리 | 독립 실행 결과와 물리 해석 문장을 연결해 심사자가 볼 evidence package로 정리 | measurement-induced denoising 해석, support worker 결과, figure/table 후보 |

팀원이 먼저 볼 문서는 `docs/00_team_dashboard.md`입니다. 기존 세부 문서는 reference로 유지하며, 주제별 세부 링크도 dashboard의 `Reference Docs` 표에서 확인합니다.

## Git Rules

### Branch naming

브랜치명에는 개인 이름, 학번, GitHub username을 넣지 않습니다.

```text
<type>/<short-topic>
```

Allowed `type`:

- `feat`: 기능 또는 실험 코드
- `fix`: 버그 수정
- `exp`: 실험 설정 또는 실험 실행
- `docs`: 문서
- `refactor`: 동작 변경 없는 구조 변경
- `test`: 테스트
- `chore`: 설정 및 관리 작업

Examples:

```text
docs/readme-conventions
feat/problem-1-random-unitary
exp/projection-basis-sweep
fix/hamiltonian-projection
```

### Pull requests

- 모든 변경은 PR로 관리합니다.
- conflict가 없고 검증이 통과하면 merge합니다.
- PR 본문에는 목적, 변경 사항, 검증 명령, 결과 또는 판단을 적습니다.
- 담당자는 브랜치명이 아니라 issue, PR 본문, 실험 로그에 적습니다.

### Commit messages

```text
<type>: <summary>
```

Examples:

```text
docs: update readme conventions
feat: add problem 1 random unitary diffusion
exp: run projection basis sweep
fix: normalize projected states
```

## File Naming Rules

문제 풀이와 직접 연결되는 코드는 파일명에 문제 번호를 넣습니다.

```text
src/quantum_cylinder/problem_<n><subproblem>_<topic>.py
scripts/problem_<n><subproblem>_<action>.py
scripts/run_problem_<n>_<m>_<topic>.py
configs/problem_<n>_<m>_<topic>.json
```

Examples:

```text
src/quantum_cylinder/problem_1a_target_ensemble.py
src/quantum_cylinder/problem_1b_ensemble_metrics.py
src/quantum_cylinder/problem_1c_random_unitary_diffusion.py
src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py
scripts/problem_1a_generate_target_ensemble.py
scripts/run_problem_1_2_baselines.py
configs/problem_1_2_baseline.json
```

Common utilities that are not specific to one problem may use descriptive names such as `experiment_curves.py`.

## Reproducibility Rules

각 실험은 다음 정보를 남깁니다.

- 실행 명령
- config path
- seed
- sample size `N`
- `sigma`
- diffusion steps 또는 time grid
- measurement basis
- metric 정의
- 결과 경로
- baseline 대비 해석

표준 metric:

- `F(psi, phi) = |<psi|phi>|^2`
- fidelity-kernel MMD
- cost `1 - F` 기반 Wasserstein-type distance

표준 resource/control proxy:

- random-unitary: layer 수, random rotation 수, 2-qubit entangler 수
- Hamiltonian projected diffusion: total evolution time, fixed Hamiltonian term 수, complement qubit 수, measurement basis

## Data and Privacy

- 신청서 원문, 전화번호, 이메일, 서명, 개인정보가 포함된 파일은 커밋하지 않습니다.
- 원본 문제 PDF나 private 자료는 필요 시 로컬 `data/raw/`에만 둡니다.
- 외부에 공유 가능한 요약과 실험 기록만 `docs/`에 정리합니다.

## References

- B. Zhang et al., "Generative Quantum Machine Learning via Denoising Diffusion Probabilistic Models", PRL 132, 100602 (2024), arXiv:2310.05866: <https://arxiv.org/abs/2310.05866>
- Q. H. Tran et al., "Learning Quantum Data Distribution via Chaotic Quantum Diffusion Model", arXiv:2602.22061: <https://arxiv.org/abs/2602.22061>

## LLM Development Guide

```text
너는 QuantumCylinder 팀의 2026 양자정보경진대회 작업을 돕는 LLM 개발 파트너다.

현재 운영 원칙:
1. 한지후가 핵심 코드 구현, 통합, README/issue 동기화, 최종 gatekeeping을 담당한다.
2. 김건우는 코드/Qiskit 구현 해석, conditional state 설명, resource/control-cost consistency 검수를 담당한다.
3. 임채진은 ipynb 최종 보고서 작성, 1/2번 형식 유지, 3번 소문항별 답변 추가를 담당한다.
4. 김승빈은 물리적 해석, figure/table 패키징, support worker 재현 로그 정리를 담당한다.
5. Problem 1/2 baseline을 깨지 말고, Problem 3 extension은 baseline과 같은 metric으로 비교한다.
6. 브랜치명에는 개인 이름이나 GitHub username을 넣지 않는다.
7. 코드 변경 후에는 `python -m pytest`를 실행한다.
8. 주장할 때는 개선점과 trade-off를 함께 적는다.
9. 모르는 물리 해석은 단정하지 말고 검증 질문으로 남긴다.
10. 역할, issue, 파일 구조, 진행도가 바뀌면 `README.md`, `docs/github_issue_plan.json`, 실제 GitHub issue를 같은 변경 안에서 동기화한다.
```

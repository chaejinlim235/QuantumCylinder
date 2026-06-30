# Team Dashboard

이 문서는 대회 중 팀원이 먼저 확인할 단일 운영 문서다. 세부 문서는 필요할 때만 reference로 본다.

## 최신 스냅샷

- 기준 시각: `2026-06-30 09:40 KST`
- 한지후 메인 자동화는 cycle 60까지 완료 근거로 수확했고, cycle 62는 실행 중 수동 중단되어 evidence로 쓰지 않는다.
- 김승빈 support worker는 cycle 28까지 완료했고, 별도 컴퓨터에서 14번의 20-seed sweep과 252개 이상 hybrid toy run을 남겼다.
- Problem 3 seed sweep gate는 `20/20 use_as_main`으로 재현되었다.
- 지금부터는 자동화 추가 실행보다 보고서/발표에 수확 근거를 정확히 반영하는 것이 우선이다.

## 먼저 볼 것

| Purpose | File |
| --- | --- |
| 현재 진행도, 역할, 실행 명령 | `docs/00_team_dashboard.md` |
| 밤샘 Problem 3 실험의 과정/근거/결론 | `docs/22_overnight_problem_3_evidence_handoff.md` |
| 저장소 구조와 실행 entry point | `README.md` |
| 실제 GitHub issue 동기화 원본 | `docs/github_issue_plan.json` |
| Problem 3 seed sweep 요약 | `results/problem_3_seed_sweep/seed_sweep_summary.md` |
| 김승빈 support worker 결과 | `docs/experiments/2026-06-30_problem_3_seungbin_support_worker_results.md` |

`results/` 아래 파일은 생성물이라 Git에 커밋하지 않는다.

## 현재 판단

| Area | Status | Owner | Next action |
| --- | --- | --- | --- |
| Problem 1 | locked | 임채진, 한지후 | notebook 형식 유지, 정성 설명과 diagnostic 출력만 정리 |
| Problem 2 | locked | 김건우, 임채진 | conditional state, Hamiltonian/projection 해석 검수 |
| Problem 3 | harvested main candidate | 한지후, 김승빈 | `docs/22_overnight_problem_3_evidence_handoff.md` 기준으로 final notebook/report 반영 |
| Seed sweep | passed + independently reproduced | 김승빈 | support worker 결과에서 최종 표/그림 후보와 로그 위치 정리 |
| Report/story | in progress | 임채진 | 1/2번 형식 유지, 3번 소문항별 답변과 limitation 정리 |
| Code consistency | in progress | 김건우 | notebook 설명과 실제 Qiskit/backend 구현이 충돌하지 않는지 확인 |
| Issue/repo metadata | required every change | 한지후 | README, `docs/github_issue_plan.json`, 실제 GitHub issue 동기화 |

Problem 3의 현재 안전한 주장은 다음 범위로 제한한다.

- 20-seed sweep 기준 `20/20 use_as_main`.
- median MMD improvement `0.097056`.
- median Wasserstein improvement `0.147983`.
- axis-only score margin은 `0.010000`으로 작으므로 limitation에 적는다.
- hardware advantage나 general quantum advantage로 주장하지 않는다.

## 지금 실행할 명령

제출 전 전체 검증:

```powershell
.\scripts\run_competition_final_automation.ps1
```

짧은 로컬 확인:

```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/run_problem_3_continuous_denoising.py
python scripts/summarize_problem_3_seed_sweep.py
```

역할, issue, 파일 구조, 진행도가 바뀐 뒤 동기화:

```powershell
.\scripts\sync_hackathon_issues.ps1 -Apply
git status --short --branch
```

새 Problem 3 자동화를 다시 켜는 것은 최종 보고서/QA가 막혔을 때만 한다. 지금 기본 전략은 새 후보를 더 늘리는 것이 아니라, 이미 수확한 evidence를 정확히 보고서와 발표자료에 반영하는 것이다.

## 역할

| Member | Role | Output |
| --- | --- | --- |
| 한지후 | 핵심 구현, 통합, gatekeeping, README/issue 동기화 | main branch 안정화, 최종 claim 숫자 관리 |
| 김건우 | 코드/Qiskit 구현 해석 및 consistency 검수 | conditional state, x축 비교, resource 설명 검수 |
| 임채진 | ipynb 최종 보고서와 storyline | 1/2번 형식 유지, 3번 소문항별 답변, limitation 정리 |
| 김승빈 | 물리적 해석, seed sweep, figure/table | measurement-induced denoising 해석과 결과 표/그림 후보 |

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
| 밤샘 Problem 3 evidence handoff | `docs/22_overnight_problem_3_evidence_handoff.md` |
| GitHub issue 원본 | `docs/github_issue_plan.json` |

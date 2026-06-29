# Task: Final Team Sync, Check, and Fix Loop

Read these first:

- `.hermes.md`
- `README.md`
- `docs/14_team_problem_status.md`
- `docs/13_automation_feedback_loop.md`
- `.hermes/tasks/final-pipeline.md`

## Goal

Run the final automation loop that includes teammate changes:

1. Fetch and fast-forward the latest `origin/main` changes.
2. Inspect the current git state.
3. Run tests and the final pipeline.
4. If a check fails, diagnose the root cause and make the smallest safe fix.
5. Re-run the relevant check until it passes or a real blocker is found.
6. Sync GitHub issues after the final status is known.
7. Report the result in Korean.

## Hard Constraints

- Do not overwrite or revert user changes.
- Do not use `git reset --hard` or checkout files away.
- `scripts/sync_latest_team_changes.ps1` may fast-forward `main` from `origin/main`.
- If local changes overlap incoming files, stop and report the overlap.
- You may edit tracked source/docs only to fix failing checks or obvious automation breakage.
- Do not commit anything.
- Generated files under `results/` are allowed.
- Do not touch private/raw PDFs, application forms, phone numbers, emails, signatures, or other PII.
- Do not claim Problem 3 as the main result unless the seed sweep summary recommends `use_as_main`.

## Commands To Run

If the shell is PowerShell:

```powershell
.\scripts\sync_latest_team_changes.ps1
python -m pytest --basetemp .pytest_tmp_final_sync
.\scripts\run_final_pipeline_visible.ps1 -SkipTeamSync
.\scripts\sync_hackathon_issues.ps1 -Apply
```

If the shell is bash/MSYS/Git Bash:

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/sync_latest_team_changes.ps1
python -m pytest --basetemp .pytest_tmp_final_sync
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/run_final_pipeline_visible.ps1 -SkipTeamSync
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/sync_hackathon_issues.ps1 -Apply
```

If any command fails:

1. Read the error output.
2. Inspect only the files directly related to the failure.
3. Make a focused fix.
4. Re-run the failed command.
5. Continue the loop only after the failed command passes.

## Required Reads After Commands

- `results/submission_simple/SUMMARY.md`
- `results/problem_3_continuous_denoising/problem_3_summary.md`, if it exists
- `results/problem_3_seed_sweep/seed_sweep_summary.md`
- `docs/14_team_problem_status.md`

## Final Response

Respond in Korean and include:

- Whether latest teammate changes were fetched and merged.
- Whether any local changes blocked sync.
- Whether tests passed.
- Whether `submission/run_all.py` passed.
- Whether the 20-seed Problem 3 sweep passed.
- The seed sweep recommendation.
- The safest final Problem 3 claim wording.
- Any files changed by the fix loop.
- Whether GitHub issues were synced.
- The single next action before final report/presentation work.

# Task: Automated Feedback Loop

Read these first:

- `.hermes.md`
- `README.md`
- `docs/11_problem_3_continuous_denoising.md`
- `docs/13_automation_feedback_loop.md`
- `.hermes/tasks/final-pipeline.md`

## Goal

Run the self-analysis feedback loop:

1. Execute the final pipeline.
2. Read generated summaries.
3. Decide whether the current Problem 3 claim is safe.
4. Sync GitHub issues so each teammate has a current next task.
5. Report the next action in Korean.

## Hard Constraints

- Do not edit tracked files.
- Do not commit anything.
- Generated files under `results/` are allowed.
- Do not touch private/raw PDFs or application forms.
- If a command fails, stop and report the exact command.
- Do not overclaim beyond generated summaries.

## Commands To Run

If the shell is PowerShell:

```powershell
.\scripts\run_final_pipeline_visible.ps1
.\scripts\sync_hackathon_issues.ps1 -Apply
```

If the shell is bash/MSYS/Git Bash:

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/run_final_pipeline_visible.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/sync_hackathon_issues.ps1 -Apply
```

Read:

- `results/submission_simple/SUMMARY.md`
- `results/problem_3_seed_sweep/seed_sweep_summary.md`

## Final Response

Respond in Korean and include:

- Whether tests and final pipeline passed.
- The Problem 3 seed sweep recommendation.
- The safest current final claim.
- Which issues were updated or created.
- Which teammate owns the next bottleneck.
- Whether this direction is still appropriate for prize/winning strategy.

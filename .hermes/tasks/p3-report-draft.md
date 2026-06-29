# Task: Problem 3 Report Draft

Read these first:

- `.hermes.md`
- `README.md`
- `docs/11_problem_3_continuous_denoising.md`
- `results/problem_3_continuous_denoising/problem_3_summary.md`, if it exists
- `results/problem_3_seed_sweep/seed_sweep_summary.md`, if it exists

## Goal

Draft concise Korean report text for Problem 3 using only results that are actually present in the repository.

## Hard Constraints

- Do not overclaim beyond the result summaries.
- If the seed sweep recommends `fallback_or_appendix`, write the method as a candidate or appendix result, not as the main winning claim.
- Do not edit source code.
- Do not commit anything.
- You may create or update only this file:
  - `docs/experiments/2026-06-29_problem_3_report_draft.md`

## If Results Are Missing

If the default Problem 3 summary is missing, run:

```powershell
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
& $ProjectPython scripts/run_problem_3_continuous_denoising.py
```

Do not run the full seed sweep unless `results/problem_3_seed_sweep/seed_sweep_summary.md` already exists.

## Draft Structure

Write `docs/experiments/2026-06-29_problem_3_report_draft.md` with these sections:

1. Problem 3 Idea
2. Method
3. Baselines And Metrics
4. Results
5. Limitations
6. Submission Claim

Keep the writing practical and modest. Use Korean for the report draft.

## Final Response

Respond in Korean and include:

- The draft file path.
- Which result summaries were used.
- Whether the draft treats the method as main result or fallback/appendix.

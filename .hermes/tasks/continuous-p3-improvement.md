# Task: Continuous Problem 3 Improvement

Read these first:

- `.hermes.md`
- `README.md`
- `docs/00_team_dashboard.md`
- `docs/11_problem_3_continuous_denoising.md`
- `docs/13_automation_feedback_loop.md`
- `docs/16_three_day_roadmap.md`
- `results/problem_3_seed_sweep/seed_sweep_summary.md`, if it exists
- `results/continuous_problem_3/latest_status.md`, if it exists
- `results/continuous_problem_3/progress_log.md`, if it exists
- `src/quantum_cylinder/problem_3_continuous_projected_denoising.py`
- `scripts/run_problem_3_continuous_denoising.py`
- `scripts/run_problem_3_seed_sweep_visible.ps1`
- `scripts/summarize_problem_3_seed_sweep.py`
- `submission/problem3_continuous_measurement_denoising.py`

## Goal

Keep Problem 3 improving as a differentiating result while the competition is running.

This is a continuous feedback cycle:

```text
experiment -> analyze -> decide -> apply a focused improvement -> verify -> record feedback
```

The goal is not to produce random churn. Each cycle should improve at least one of:

- quantitative robustness,
- fairness of comparison,
- clarity of the physical explanation,
- reproducibility and packaging,
- final-report readiness.

## Current Main Result To Preserve

The current robust result is:

- seed sweep recommendation: `use_as_main`
- `20/20` seeds: `use_as_main`
- main_candidate rows: `81/120 = 0.675`
- median MMD improvement: `0.097056`
- median Wasserstein improvement: `0.147983`
- median axis-only score margin: `0.010000`
- median diversity retention: `0.823217`
- median mean success probability: `0.468122`

Do not replace this main result unless the new result is at least as robust and better justified.

## Hard Constraints

- Do not commit anything.
- Do not open or merge PRs.
- Do not overwrite or revert user changes.
- Do not use `git reset --hard` or checkout files away.
- Do not touch private/raw PDFs, application forms, phone numbers, emails, signatures, or other PII.
- Generated files under `results/` are allowed but must not be added to Git.
- Keep Problem 1/2 baselines stable unless a small documentation or compatibility fix is needed.
- Do not claim hardware advantage, general quantum advantage, or real-device superiority.
- If a new candidate underperforms, record it as a candidate/appendix idea and keep the current main result.

## Cycle Plan

1. Sync and inspect.

```powershell
.\scripts\sync_latest_team_changes.ps1
git status --short --branch
```

2. Run a quick correctness check.

```powershell
python -m pytest --basetemp .pytest_tmp_continuous_p3
```

3. Run or refresh Problem 3.

```powershell
python scripts/run_problem_3_continuous_denoising.py
.\scripts\run_problem_3_seed_sweep_visible.ps1 -SkipTests
```

4. Read the generated summaries.

- `results/problem_3_continuous_denoising/problem_3_summary.md`
- `results/problem_3_seed_sweep/seed_sweep_summary.md`
- `results/submission_simple/SUMMARY.md`, if present

5. Decide one focused improvement.

Prefer low-risk improvements:

- better ablation or summary table,
- clearer axis-only comparison wording,
- stronger seed-sweep report,
- figure/table packaging,
- guardrails around diversity and success probability,
- small code readability fixes,
- tests for any meaningful changed behavior.

Only try a new research candidate if it can be evaluated quickly and safely.

6. Apply the improvement if justified, then verify the affected path.

7. Update GitHub issues if the task allocation changed.

```powershell
.\scripts\sync_hackathon_issues.ps1 -Apply
```

## Decision Rules

Keep Problem 3 as main if:

- seed sweep recommendation remains `use_as_main`,
- MMD or Wasserstein improvement remains positive,
- diversity retention remains acceptable,
- success probability remains explainable,
- axis-only comparison is reported honestly.

If the axis-only score margin remains near `0.010000`, this is acceptable but must be stated as a limitation.

## Final Response

Respond in Korean and include:

- what was attempted this cycle,
- what changed in source/docs/results,
- whether source/docs changed,
- whether tests passed,
- whether the 20-seed sweep passed,
- latest recommendation and key numbers,
- whether the main claim should be preserved or changed,
- the safest report wording,
- next action for the team.

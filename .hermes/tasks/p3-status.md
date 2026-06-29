# Task: Problem 3 Status Check

Read these first:

- `.hermes.md`
- `README.md`
- `docs/11_problem_3_continuous_denoising.md`

## Goal

Give the team a fast, execution-backed status update for Problem 3 and the current repository state.

## Hard Constraints

- Do not modify files.
- Do not commit anything.
- Do not touch private/raw PDFs or application forms.
- If a command fails, report the exact failed command and the likely cause.

## Commands To Run

```powershell
git status --short --branch
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
& $ProjectPython -m pytest
```

If `results/problem_3_continuous_denoising/problem_3_summary.md` does not exist, run:

```powershell
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
& $ProjectPython scripts/run_problem_3_continuous_denoising.py
```

If these files exist, read them:

- `results/problem_3_continuous_denoising/problem_3_summary.md`
- `results/problem_3_seed_sweep/seed_sweep_summary.md`

## Final Response

Respond in Korean and include:

- Whether tests passed.
- Whether the working tree has tracked or untracked changes.
- The current Problem 3 decision from the default run, if available.
- The seed sweep recommendation, if available.
- The next one or two actions the team should take.

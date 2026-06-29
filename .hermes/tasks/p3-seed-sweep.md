# Task: Problem 3 Seed Sweep

Read these first:

- `.hermes.md`
- `README.md`
- `docs/11_problem_3_continuous_denoising.md`
- `scripts/run_problem_3_continuous_denoising.py`
- `scripts/summarize_problem_3_seed_sweep.py`
- `configs/problem_3_continuous_denoising.json`

## Goal

Run the Problem 3 continuous measurement-induced denoising seed sweep and decide whether the result is robust enough to use as the main Problem 3 claim.

## Hard Constraints

- Do not modify tracked source files.
- Do not commit anything.
- Generated files under `results/` are allowed.
- Do not touch private/raw PDFs or application forms.
- If a command fails, stop and explain the failure.

## Commands To Run

Run tests first:

```powershell
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
& $ProjectPython -m pytest
```

Run the 20-seed sweep:

```powershell
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
$Seeds = 1..20

foreach ($Seed in $Seeds) {
    & $ProjectPython scripts/run_problem_3_continuous_denoising.py `
        --seed $Seed `
        --output-dir "results/problem_3_seed_sweep/seed_$Seed"
}
```

Aggregate the results:

```powershell
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
& $ProjectPython scripts/summarize_problem_3_seed_sweep.py --input-dir results/problem_3_seed_sweep
```

## Final Response

After running the commands, report:

- Whether tests passed.
- How many seeds returned `use_as_main`.
- The `main_candidate` row fraction.
- The median MMD improvement.
- The median Wasserstein improvement.
- The median score margin over axis-only.
- The median diversity retention.
- The median mean success probability.
- Whether the final recommendation is `use_as_main` or `fallback_or_appendix`.
- The path to `results/problem_3_seed_sweep/seed_sweep_summary.md`.

# Task: Final Automated Pipeline

Read these first:

- `.hermes.md`
- `README.md`
- `submission/README.md`
- `docs/11_problem_3_continuous_denoising.md`
- `docs/12_hermes_agent_setup.md`

## Goal

Run the full pre-submission automation pipeline and produce a concise Korean status report for the team.

This is the high-level task to use when the team wants Hermes to handle the whole flow instead of running each step manually.

## Hard Constraints

- Do not modify tracked source or documentation files.
- Do not commit anything.
- Generated files under `results/` are allowed.
- Do not touch private/raw PDFs, application forms, phone numbers, emails, signatures, or other PII.
- Stop immediately if any command fails and report the exact failed command.
- Do not claim Problem 3 as the main result unless the seed sweep summary recommends `use_as_main`.

## Commands To Run

Run the final pipeline with one command.

If the shell is PowerShell, run:

```powershell
.\scripts\run_final_pipeline_visible.ps1
```

If the shell is bash/MSYS/Git Bash, run:

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/run_final_pipeline_visible.ps1
```

Read these generated summaries:

- `results/submission_simple/SUMMARY.md`
- `results/problem_3_continuous_denoising/problem_3_summary.md`, if it exists
- `results/problem_3_seed_sweep/seed_sweep_summary.md`

Check the final repository state:

```powershell
git status --short --branch
```

## Final Response

Respond in Korean and include:

- Whether tests passed.
- Whether `submission/run_all.py` passed.
- Whether the 20-seed Problem 3 sweep passed.
- The seed sweep recommendation.
- The number of seeds returning `use_as_main`.
- The main-candidate row fraction.
- Median MMD improvement.
- Median Wasserstein improvement.
- Median score margin over axis-only.
- Median diversity retention.
- Median mean success probability.
- Whether generated results stayed out of Git.
- Any tracked/untracked working-tree changes.
- The safest final Problem 3 claim wording.
- The single next action for the team.

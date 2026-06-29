# Task: Quantitative Evaluation Sweep

Read these first:

- `.hermes.md`
- `README.md`
- `docs/14_team_problem_status.md`
- `docs/15_quantitative_evaluation_plan.md`

## Goal

Generate quantitative evidence for judge-facing evaluation before final report work.

## Hard Constraints

- Do not commit generated `results/` files.
- Do not touch private/raw PDFs or application forms.
- Do not overclaim beyond generated summaries.
- If a command fails, inspect the failure and make the smallest safe fix.

## Commands To Run

```powershell
python scripts/run_quantitative_evaluation.py
python -m pytest --basetemp .pytest_tmp_quantitative
```

Read:

- `results/quantitative_evaluation/QUANTITATIVE_EVALUATION_INDEX.md`
- `results/quantitative_evaluation/problem_1b_metric_diagnostics.md`
- `results/quantitative_evaluation/problem_2a_hamiltonian_diagnostics.md`
- `results/quantitative_evaluation/problem_2b_projection_diagnostics.md`
- `results/quantitative_evaluation/problem_2c_bloch_summary.md`
- `results/problem_3_seed_sweep/seed_sweep_summary.md`, if it exists

## Final Response

Respond in Korean and include:

- Whether quantitative diagnostics ran.
- Which generated files matter most.
- Whether tests passed.
- What evidence is now strongest for the judges.
- What the team should inspect manually next.

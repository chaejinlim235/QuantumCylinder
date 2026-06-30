# Reproducibility Commands

Run commands from this `source_code/` directory.

## Quick Validation Path

```powershell
python -m pytest
python submission/run_all.py --quick
```

Expected output:

- `pytest`: all tests pass. If a Windows temp cleanup permission issue appears after tests pass, rerun with `python -m pytest --basetemp .pytest_tmp_local`.
- `submission/run_all.py --quick`: prints compact Problem 1, Problem 2, and Problem 3 summaries.

Approximate runtime: a few seconds to under a minute on a typical laptop.

## Final Figure/Table Regeneration

```powershell
python scripts/create_solution_haar_baseline.py
python scripts/summarize_problem_3_seed_sweep.py
python scripts/run_problem_3_hamiltonian_variant_candidates.py
python scripts/summarize_problem_3_method_portfolio.py
```

Expected output:

- Haar reference figure/table under `solution/figures/` and `solution/tables/`.
- Problem 3 seed-sweep summary with `20 / 20` seeds passing the main gate, using selected evidence under `results/problem_3_seed_sweep/`.
- Problem 3(c) two-way candidate summary with stronger distance gain and lower success probability.
- `results/` contains compact evidence needed by the summary commands; large candidate-search CSVs and logs are intentionally omitted.

## Full Validation Path

The repository also contains richer experiment scripts in `scripts/`. Inspect `scripts/run_problem_1_2_baselines.py`, `scripts/run_problem_3_continuous_denoising.py`, and `scripts/run_problem_3_hamiltonian_variant_candidates.py` for the main experiment flows.

## Source Inspection Path

Start from:

1. `solution/solution_1.ipynb`
2. `scripts/`
3. `src/quantum_cylinder/`
4. `tests/`

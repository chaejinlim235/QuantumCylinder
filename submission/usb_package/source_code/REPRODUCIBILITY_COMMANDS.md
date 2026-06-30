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

## Optional IBM QPU Dry-Run

```powershell
python scripts/ibm_qpu_smoke_test.py --dry-run
```

This command prepares tiny representative circuits and saves a no-submit report
under `results/ibm_qpu_validation/`. Real IBM QPU submission requires
credentials and an explicit `--submit` command; it is not required for the main
state-vector benchmark.

## Optional IBM QPU Problem 3-b Appendix

Dry-run:

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py --backend ibm_fez --shots 2048 --repeats 3 --dt 0.20 --trotter-steps 1 --save-dir results/ibm_qpu_validation/p3b_fez_2048x3_dryrun
```

Retrieve completed jobs in `.venv_ibm` or any environment with
`qiskit-ibm-runtime` installed:

```powershell
python scripts/ibm_qpu_extract_p3b_counts.py --job-id d91r6pmu9n7c73an9qgg --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_2048x3/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_fez_2048x3
python scripts/ibm_qpu_extract_p3b_counts.py --job-id d91r71fccmks73d5nmg0 --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_4096x5/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_fez_4096x5
```

Summarize and copy to USB package:

```powershell
python scripts/summarize_ibm_qpu_p3b_results.py
python scripts/copy_ibm_qpu_results_to_usb.py
```

These IBM commands are appendix validation only. The main quantitative claims
remain state-vector based.

## Source Inspection Path

Start from:

1. `solution/solution_1.ipynb`
2. `scripts/`
3. `src/quantum_cylinder/`
4. `tests/`

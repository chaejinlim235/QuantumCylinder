# Reproducibility Commands

Run these commands from `submission/usb_package/source_code/`.

## Quick Validation

```powershell
python -m pytest
python submission/run_all.py --quick
```

Expected result:

- `pytest`: all tests pass. If Windows reports a temp-directory cleanup issue
  after tests pass, rerun with `python -m pytest --basetemp .pytest_tmp_local`.
- `submission/run_all.py --quick`: prints compact Problem 1, Problem 2, and
  Problem 3 summaries.

Approximate runtime is a few seconds to under a minute on a typical laptop.

## Final Figure And Table Regeneration

```powershell
python scripts/create_solution_haar_baseline.py
python scripts/summarize_problem_3_seed_sweep.py
python scripts/run_problem_3_hamiltonian_variant_candidates.py
python scripts/summarize_problem_3_method_portfolio.py
```

Expected outputs:

- Problem 1(c) Haar reference figure/table under `solution/`.
- Problem 3 seed-sweep summary showing the measurement-basis trade-off and the
  small axis-only margin.
- Problem 3(c) method portfolio showing two-way post-selection as stronger
  distance improvement with lower success probability.

## Source Inspection Path

Read in this order:

1. `README_FOR_JUDGES.md`
2. `solution/solution_1.ipynb`
3. `PROBLEM_REQUIREMENT_MAP.md`
4. `CODE_MANIFEST.md`
5. `src/quantum_cylinder/`
6. `scripts/`
7. `tests/`

## Optional IBM QPU Dry-Run

```powershell
python scripts/ibm_qpu_smoke_test.py --dry-run
```

This prepares tiny representative circuits and saves a no-submit report under
`results/ibm_qpu_validation/`. Real IBM QPU submission requires credentials and
an explicit `--submit` command. It is not required for the main benchmark.

## Optional IBM QPU Problem 3-b Appendix

Dry-run:

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py --backend ibm_fez --shots 2048 --repeats 3 --dt 0.20 --trotter-steps 1 --save-dir results/ibm_qpu_validation/p3b_fez_2048x3_dryrun
```

Retrieve included completed jobs in an environment with `qiskit-ibm-runtime`:

```powershell
python scripts/ibm_qpu_extract_p3b_counts.py --job-id d91r6pmu9n7c73an9qgg --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_2048x3/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_fez_2048x3
python scripts/ibm_qpu_extract_p3b_counts.py --job-id d91r71fccmks73d5nmg0 --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_4096x5/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_fez_4096x5
```

Summarize and copy appendix results:

```powershell
python scripts/summarize_ibm_qpu_p3b_results.py
python scripts/copy_ibm_qpu_results_to_usb.py
```

These IBM commands are appendix validation only. The main quantitative claims
remain state-vector based.

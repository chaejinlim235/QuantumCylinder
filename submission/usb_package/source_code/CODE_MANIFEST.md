# Code Manifest

## Final Answer

- `solution/`: final notebook, README, figures, and tables.
- `solution/solution_1.ipynb`: final judge-facing answer.
- `solution/figures/`: final figures used by the notebook and presentation outline.
- `solution/tables/`: final tables and support CSV/Markdown summaries.

## Core Implementation

- `src/quantum_cylinder/`: core implementation for target ensembles, metrics, random-unitary diffusion, Hamiltonian projected diffusion, and Problem 3 denoising variants.
- `scripts/`: curated Python experiment, plotting, and summary scripts.
- `tests/`: regression and sanity tests.
- `configs/`: experiment configuration files.
- `results/`: selected compact evidence files for the documented Problem 3 summary scripts; large candidate-search CSVs and logs are intentionally omitted.
- `results/ibm_qpu_validation/`: optional IBM QPU dry-run resource summary.
- `IBM_QPU_README.md`: optional IBM Quantum / Qiskit Runtime validation instructions.

## Submission Entry Point

- `submission/run_all.py`: quick reproduction command for Problems 1, 2, and 3.
- `submission/problem1_random_unitary_scrambling.py`: Problem 1 submission-layer flow.
- `submission/problem2_hamiltonian_projection.py`: Problem 2 submission-layer flow.
- `submission/problem3_continuous_measurement_denoising.py`: Problem 3 submission-layer flow.
- `submission/states_and_metrics.py`: shared submission-layer metrics/utilities.

## Environment Files

- `pyproject.toml`: package and test configuration.
- `requirements.txt`: minimal dependency list.

## Primary Scripts

- `scripts/create_solution_haar_baseline.py`: creates the Problem 1(c) Haar reference figure/table.
- `scripts/run_problem_1_2_baselines.py`: generates Problem 1/2 distance curves and resource comparison.
- `scripts/run_problem_3_continuous_denoising.py`: runs continuous measurement-basis post-selection.
- `scripts/summarize_problem_3_seed_sweep.py`: summarizes 20-seed Problem 3 evidence.
- `scripts/run_problem_3_hamiltonian_variant_candidates.py`: runs the 3(c) Hamiltonian two-way candidate and random-kick ablation.
- `scripts/summarize_problem_3_method_portfolio.py`: summarizes 3(c) main and appendix rows.
- `scripts/ibm_qpu_smoke_test.py`: prepares tiny representative circuits for optional IBM QPU dry-run or explicit submission.

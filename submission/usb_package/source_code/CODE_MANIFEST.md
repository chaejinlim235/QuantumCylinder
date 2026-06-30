# Code Manifest

This manifest lists the files a judge should inspect to understand and rerun
the submission.

## Final Answer Artifacts

| Path | Purpose |
| --- | --- |
| `solution/solution_1.ipynb` | Compact final answer for Problems 1(a) through 3(c). |
| `solution/README.md` | Human-readable guide to the final notebook, figures, tables, and claim guardrails. |
| `solution/figures/` | Final figures referenced by the notebook. |
| `solution/tables/` | Final CSV/Markdown tables supporting numerical claims. |

The top-level USB package also contains split notebooks under `../solution/`
for presentation-style reading.

## Core Implementation

| Path | Purpose |
| --- | --- |
| `src/quantum_cylinder/` | Main implementation for target ensembles, metrics, random-unitary diffusion, Hamiltonian projected diffusion, and Problem 3 denoising variants. |
| `scripts/` | Experiment, plotting, summary, packaging, and IBM QPU appendix scripts. |
| `tests/` | Regression and sanity tests for metrics, submission flow, and Problem 3 summaries. |
| `configs/` | Experiment configuration files. |
| `submission/` | Compact standalone execution layer used by `submission/run_all.py`. |
| `results/` | Selected compact evidence needed by summary scripts and the IBM QPU appendix. |

Large exploratory logs are not required for the final answer. The included
`results/` files are the ones needed for traceability and reproduction of the
published summaries.

## Submission Entry Points

| File | Purpose |
| --- | --- |
| `submission/run_all.py` | Quick reproduction command for Problems 1, 2, and 3. |
| `submission/problem1_random_unitary_scrambling.py` | Problem 1 submission-layer flow. |
| `submission/problem2_hamiltonian_projection.py` | Problem 2 submission-layer flow. |
| `submission/problem3_continuous_measurement_denoising.py` | Problem 3 submission-layer flow. |
| `submission/states_and_metrics.py` | Shared state, fidelity, MMD, and Wasserstein-type utilities. |

## Primary Reproduction Scripts

| Script | Purpose |
| --- | --- |
| `scripts/create_solution_haar_baseline.py` | Regenerates the Problem 1(c) Haar reference figure/table. |
| `scripts/run_problem_1_2_baselines.py` | Generates Problem 1/2 distance curves and resource comparison. |
| `scripts/run_problem_3_continuous_denoising.py` | Runs the continuous measurement-basis denoising reference. |
| `scripts/summarize_problem_3_seed_sweep.py` | Summarizes 20-seed Problem 3 evidence. |
| `scripts/run_problem_3_hamiltonian_variant_candidates.py` | Runs the Problem 3(c) two-way candidate and ablations. |
| `scripts/summarize_problem_3_method_portfolio.py` | Summarizes the Problem 3(c) main and appendix rows. |

## Optional IBM QPU Appendix Scripts

| Script | Purpose |
| --- | --- |
| `scripts/ibm_qpu_smoke_test.py` | Builds tiny representative IBM-compatible circuits; can dry-run without submission. |
| `scripts/ibm_qpu_problem3b_basis_sweep.py` | Builds and optionally submits the Problem 3-b measurement-basis mini validation. |
| `scripts/ibm_qpu_extract_p3b_counts.py` | Retrieves or reanalyzes completed Problem 3-b IBM QPU counts. |
| `scripts/summarize_ibm_qpu_p3b_results.py` | Produces slide-ready IBM appendix summaries using standard-library CSV/JSON processing. |
| `scripts/copy_ibm_qpu_results_to_usb.py` | Copies IBM appendix artifacts into the USB source-code package without secrets. |

Included completed IBM QPU jobs:

- `ibm_fez`, job `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE.
- `ibm_fez`, job `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

IBM QPU evidence is appendix-only and is not used to claim hardware advantage.

## Environment Files

| File | Purpose |
| --- | --- |
| `pyproject.toml` | Package, dependency, and test configuration. |
| `requirements.txt` | Minimal dependency list for basic reproduction. |

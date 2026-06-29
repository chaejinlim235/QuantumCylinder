# Problem 1/2 Result Pipeline Log

Owner: Kim Seungbin / dreamerghost77
Reviewer:

## Hypothesis

Problem 1/2 baselines should be reproducible from one config and one script, with CSV and plot outputs stored under the configured result directory.

## Setup

- Branch: `exp/problem-1-2-result-pipeline`
- Command: `python scripts/run_problem_1_2_baselines.py`
- Test command: `pytest`
- Config: `configs/problem_1_2_baseline.json`
- Seed: `7`
- Output directory: `results/problem_1_2_baseline`

## Results

- `python scripts/run_problem_1_2_baselines.py`: passed.
- `pytest`: passed, 6 tests.
- Generated files under `results/problem_1_2_baseline/`:
  - `random_unitary_metrics.csv`
  - `hamiltonian_metrics.csv`
  - `resource_proxies.csv`
  - `distance_curves.png`
  - `problem_1_2_settings.json`
  - `problem_1_2_summary.md`
- Final random-unitary step 12:
  - MMD: `0.828093`
  - Wasserstein-type distance: `0.686108`
- Hamiltonian projected diffusion:
  - Max MMD: `1.249244` at `t = 1.000000`
  - Max Wasserstein-type distance: `0.883968` at `t = 4.000000`

## Interpretation

`distance_curves.png` is the first presentation figure candidate because it compares random-unitary and Hamiltonian projected diffusion under the same target ensemble, seed, sample size, metric definitions, and output schema.

`resource_proxies.csv` is the first table candidate because it compares random circuit layer controls against fixed Hamiltonian time and basis controls.

## Next

- Repeat the run for seeds `11` and `23` before final claims.
- Keep generated CSV/PNG/JSON/MD files out of Git unless the team explicitly promotes a final figure.

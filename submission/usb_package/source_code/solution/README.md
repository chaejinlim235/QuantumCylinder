Open solution_1.ipynb first.

# QuantumCylinder Final Solution

QuantumCylinder compares random-unitary diffusion and Hamiltonian projected
diffusion under shared fidelity-based MMD/Wasserstein metrics, then studies
measurement-induced projected denoising as a recoverability-success-diversity
trade-off.

Based on the 3-b trade-off analysis, Problem 3(c) tests two-way Hamiltonian
post-selection as a stronger but more costly projected denoising improvement.

## Main Files
- `solution_1.ipynb`: final judge-facing answer.
- `figures/fig2_random_unitary_haar_baseline.png`: Problem 1(c) Haar-random reference baseline.
- `figures/problem_1_2_distance_curves.png`: native random-unitary and Hamiltonian projected diffusion curves.
- `figures/problem_1_2_metric_aligned_comparison.png`: Problem 2(d) comparable-strength comparison.
- `figures/problem_3a_denoising_improvement.png`: Problem 3(a) denoising result.
- `figures/problem_3c_hamiltonian_variant_summary.png`: Problem 3(c) two-way and ablation comparison.
- `tables/problem1_haar_reference.csv`: Haar reference mean/std.
- `tables/problem3b_measurement_basis_tradeoff.csv`: 3(b) gain, success, diversity, and interpretation.
- `tables/problem3c_analysis_guided_improvement.csv`: 3(c) one-way reference, ablation, and two-way candidate.

## Evaluation Criteria
- Novelty: measurement basis is treated as a control knob for the effective non-unitary map induced by complement-qubit post-selection.
- Completeness: Problems 1, 2, and 3 are answered with shared metrics, connected interpretation, final figures, tables, scripts, and tests.
- Appropriateness: the result is a small-scale fixed measurement-induced toy denoising benchmark with explicit trade-offs and no overclaim.

## Key Problem 3 Numbers
- 20 / 20 seeds passed the adoption gate for the main Problem 3 claim.
- Continuous 3(b) reference median gains: MMD `0.097056`, Wasserstein `0.147983`.
- Continuous reference guardrails: diversity retention `0.823217`, success probability `0.468122`.
- Axis-only score margin is small: `0.010000`.
- Two-way 3(c) candidate: MMD gain `0.101374`, Wasserstein gain `0.136426`, diversity retention `0.829273`, success probability `0.227065`.

## Minimal Reproduce
```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/create_solution_haar_baseline.py
python scripts/summarize_problem_3_seed_sweep.py
python scripts/run_problem_3_hamiltonian_variant_candidates.py
python scripts/summarize_problem_3_method_portfolio.py
python scripts/ibm_qpu_smoke_test.py --dry-run
```

## Optional IBM QPU Validation

IBM QPU validation is appendix evidence only. It checks whether tiny
representative circuits can be prepared for IBM Quantum via Qiskit Runtime and
reports transpiled depth, two-qubit gate count, shots, backend, and job status
if a real job is explicitly submitted.

The main MMD/Wasserstein claims remain the reproducible state-vector benchmark.

## Limitations
No quantum advantage, hardware advantage, or full trainable QuDDPM claim is
made. Continuous basis margin over axis-only is small; two-way post-selection
has lower success probability; actor-critic is target-aware if mentioned.

The Haar baseline is a reference, not a training target, and the random-unitary
curve is interpreted as strong scrambling rather than slow DDPM-like diffusion.

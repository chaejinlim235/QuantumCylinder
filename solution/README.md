# QuantumCylinder Final Solution
Open `solution_1.ipynb` first. It is the final judge-facing notebook for the 2026 Quantum Information Contest QML challenge.

QuantumCylinder compares random-unitary diffusion and Hamiltonian projected diffusion under shared fidelity-based MMD/Wasserstein metrics, then studies measurement-induced projected denoising as a recoverability-success-diversity trade-off.

## Main Figures
- `figures/fig2_random_unitary_haar_baseline.png`: Problem 1(c) random-unitary scrambling against a Haar-random reference level.
- `figures/problem_1_2_distance_curves.png`: native random-unitary and Hamiltonian projected diffusion curves.
- `figures/problem_1_2_metric_aligned_comparison.png`: Problem 2(d) comparable-strength comparison.
- `figures/problem_3a_denoising_improvement.png`: simple measurement-induced denoising result.
- `figures/problem_3c_hamiltonian_variant_summary.png`: 3(c) two-way and ablation comparison.

## Main Tables
- `tables/problem_1b_metric_diagnostics.md/.csv`: target-ensemble and metric sanity checks.
- `tables/problem1_haar_reference.csv`: Haar reference mean/std for Problem 1(c).
- `tables/problem_2d_resource_matches.csv`: comparable-strength resource/control proxy.
- `tables/problem3b_measurement_basis_tradeoff.csv`: 3(b) gain, success, diversity, and interpretation.
- `tables/problem3c_analysis_guided_improvement.csv`: 3(c) one-way reference, random-kick ablation, and two-way candidate.

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
```

## Limitations
We do not claim quantum advantage, hardware advantage, a full trainable QuDDPM, or that continuous measurement bases always or strongly beat axis-only Pauli bases. Actor-critic is target-aware because its reward uses the raw target ensemble, so it is not a general unknown-target denoiser.

# Problem Requirement Map

This table maps each official subproblem to the final answer artifact, the
source-code artifact, and the short answer used in the submission.

| Subproblem | Requirement | Final artifact | Source artifact | One-sentence answer | Status |
| --- | --- | --- | --- | --- | --- |
| 1(a) | Build a target ensemble around `|00>`. | `solution/solution_1.ipynb` | `src/quantum_cylinder/problem_1a_target_ensemble.py` | We generate a two-qubit target ensemble clustered near `|00>` with fixed `N`, `sigma`, and seed settings. | Complete |
| 1(b) | Define fidelity, MMD, and Wasserstein-type distance. | `solution/solution_1.ipynb`, `solution/tables/problem_1b_metric_diagnostics.md` | `src/quantum_cylinder/problem_1b_ensemble_metrics.py` | We use fidelity-based MMD and infidelity-cost Wasserstein-type distance throughout Problems 1-3. | Complete |
| 1(c) | Show random-unitary diffusion trajectory and distance curves. | `solution/figures/fig2_random_unitary_haar_baseline.png`, `solution/tables/problem1_haar_reference.csv` | `scripts/create_solution_haar_baseline.py`, `scripts/run_problem_1_2_baselines.py` | Random-unitary diffusion rapidly reaches a strong-scrambling, Haar-like distance plateau. | Complete |
| 2(a) | Define the fixed three-qubit Hamiltonian. | `solution/solution_1.ipynb` | `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py` | We define a fixed Hamiltonian on two data qubits plus one complement qubit. | Complete |
| 2(b) | Construct the projected ensemble. | `solution/solution_1.ipynb` | `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py` | We evolve the `M+F` system and condition on the complement qubit to obtain data-system ensembles. | Complete |
| 2(c) | Plot Hamiltonian distances and compare qualitatively. | `solution/figures/problem_1_2_distance_curves.png`, `solution/tables/problem_2_hamiltonian_metrics.csv` | `scripts/run_problem_1_2_baselines.py` | Hamiltonian projected diffusion is compared with random-unitary diffusion using the same metrics while noting fluctuation, saturation, and schedule sensitivity. | Complete |
| 2(d) | Discuss resource/control-cost proxies. | `solution/figures/problem_1_2_metric_aligned_comparison.png`, `solution/tables/problem_2d_resource_matches.csv` | `scripts/run_problem_1_2_baselines.py` | We compare random gate-level control against fixed-Hamiltonian evolution time and projection-basis control. | Complete |
| 3(a) | Show a simple denoising step. | `solution/figures/problem_3a_denoising_improvement.png` | `submission/problem3_continuous_measurement_denoising.py` | We demonstrate a fixed measurement-induced post-selected denoising proxy. | Complete |
| 3(b) | Analyze a controlled modification and trade-off. | `solution/tables/problem3b_measurement_basis_tradeoff.csv`, `solution/solution_1.ipynb` | `scripts/summarize_problem_3_seed_sweep.py` | Measurement basis controls the effective non-unitary map, so gains must be read together with success probability and diversity retention. | Complete |
| 3(c) | Propose and test an improvement against a baseline. | `solution/tables/problem3c_analysis_guided_improvement.csv`, `solution/figures/problem_3c_hamiltonian_variant_summary.png` | `scripts/run_problem_3_hamiltonian_variant_candidates.py`, `scripts/summarize_problem_3_method_portfolio.py` | Two-way Hamiltonian post-selection gives stronger distance improvement while lowering success probability. | Complete |

## Traceability Notes

- Final figures and tables are under `solution/figures/` and `solution/tables/`.
- Problem 3 seed-sweep and method-portfolio summaries are reproduced by the
  scripts listed above.
- IBM QPU Problem 3-b validation is optional appendix evidence under
  `results/ibm_qpu_validation/`; it is not required for the main state-vector
  benchmark.
- Actor-critic evidence, if discussed, is target-aware appendix evidence rather
  than a general unknown-target denoising claim.

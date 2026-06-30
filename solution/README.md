Open `solution_1.ipynb` first.

# QuantumCylinder Final Solution

This folder is the compact final-answer package for the repository. It contains
the final notebook, the final figures, and the final tables used to support the
contest submission.

## Main Thesis

Complement-qubit measurement basis controls the effective post-selected
non-unitary map on the data system. Problem 3(b) analyzes this as a
recoverability-success-diversity trade-off, and Problem 3(c) follows by testing
two-way Hamiltonian post-selection as a stronger but lower-success denoising
step.

## Main Files

| File | Role |
| --- | --- |
| `solution_1.ipynb` | Final judge-facing answer for Problems 1(a) through 3(c). |
| `figures/fig2_random_unitary_haar_baseline.png` | Problem 1(c) random-unitary curve with Haar-like reference baseline. |
| `figures/problem_1_2_distance_curves.png` | Random-unitary and Hamiltonian projected-diffusion distance curves. |
| `figures/problem_1_2_metric_aligned_comparison.png` | Problem 2(d) comparable-strength resource/control comparison. |
| `figures/problem_3a_denoising_improvement.png` | Problem 3(a) measurement-induced denoising result. |
| `figures/problem_3c_hamiltonian_variant_summary.png` | Problem 3(c) two-way and ablation comparison. |
| `tables/problem1_haar_reference.csv` | Haar reference values used in Problem 1(c). |
| `tables/problem3b_measurement_basis_tradeoff.csv` | Problem 3(b) measurement-basis trade-off table. |
| `tables/problem3c_analysis_guided_improvement.csv` | Problem 3(c) baseline, ablation, and two-way comparison table. |

## Key Numerical Claims

- Problem 3 seed-sweep adoption gate: `20 / 20` seeds pass.
- Problem 3(b) continuous reference median gains: MMD `0.097056`,
  Wasserstein `0.147983`.
- Problem 3(b) guardrails: diversity retention `0.823217`, success probability
  `0.468122`.
- Axis-only margin is small: `0.010000`.
- Problem 3(c) two-way candidate: MMD gain `0.101374`, Wasserstein gain
  `0.136426`, diversity retention `0.829273`, success probability `0.227065`.

The numerical values above are traceable to the CSV/Markdown artifacts under
`tables/`, `figures/`, and the source-code package copied into
`submission/usb_package/source_code/`.

## Minimal Reproduction

From the repository root:

```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/create_solution_haar_baseline.py
python scripts/summarize_problem_3_seed_sweep.py
python scripts/run_problem_3_hamiltonian_variant_candidates.py
python scripts/summarize_problem_3_method_portfolio.py
```

## Optional IBM QPU Appendix

IBM QPU validation is appendix evidence only. It checks tiny representative
circuits for the Problem 3-b measurement-basis mechanism and does not replace
the reproducible state-vector MMD/Wasserstein benchmark.

Completed `ibm_fez` jobs included in the repository:

- job `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE;
- job `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

Slide-ready IBM appendix summaries:

- `results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.md`
- `results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.csv`

For the higher-shot run, `p(F=0)` changes from `0.881738` at `0.0000pi` to
`0.351270` at `0.7500pi`, while selected-data entropy changes from `1.375447`
to `1.736465`. This is used only as hardware-execution validation that
measurement basis changes post-selection statistics.

## Claim Guardrails

No quantum advantage, hardware advantage, or full trainable QuDDPM claim is
made. Continuous-basis improvement over axis-only projection is treated as a
small-margin trade-off, not an overwhelming win. Actor-critic results, if
mentioned, are target-aware appendix evidence rather than a general
unknown-target denoiser.

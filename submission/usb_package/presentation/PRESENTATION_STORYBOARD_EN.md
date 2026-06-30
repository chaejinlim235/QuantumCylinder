# QuantumCylinder Presentation Storyboard

## Core 5-Minute Talk Plan

| Slide | Title | Key message | Figure/table path | Speaker note | Time |
| --- | --- | --- | --- | --- | ---: |
| 1 | QuantumCylinder | We compare two diffusion mechanisms and analyze projected denoising as a recoverability-success-diversity trade-off. | none | "Our contribution is a connected final solution: Problems 1 and 2 establish comparable diffusion baselines, and Problem 3 turns post-selection into a measurable denoising trade-off." | 30s |
| 2 | Problem Map and Criteria | The notebook answers Problem 1(a) through Problem 3(c), and the package includes source code and final artifacts. | `source_code/solution/solution_1.ipynb` | "The structure follows the problem statement and the judging criteria: completeness, fidelity, novelty, and presentation clarity." | 35s |
| 3 | Problem 1: Strong Scrambling | Random-unitary diffusion rapidly reaches a Haar-like distance plateau, destroying the original `|00>` cluster. | `source_code/solution/figures/fig2_random_unitary_haar_baseline.png` | "The Haar line is a reference, not a training target. The important interpretation is strong scrambling, not slow Gaussian diffusion." | 45s |
| 4 | Problem 2: Projected Diffusion | Hamiltonian projected diffusion uses fixed Hamiltonian evolution and complement-qubit projection, with schedule-dependent behavior. | `source_code/solution/figures/problem_1_2_metric_aligned_comparison.png` | "We compare by output metric strength, not equal x-axis values, because random layer count and Hamiltonian time are different controls." | 45s |
| 5 | Problem 3(b): Trade-Off | Measurement basis controls the effective non-unitary map, so denoising must be judged by distance gain, success probability, and diversity retention. | `source_code/solution/tables/problem3b_measurement_basis_tradeoff.csv` | "The continuous basis margin over axis-only is small. The novelty is the trade-off analysis, not simply scanning bases." | 60s |
| 6 | Problem 3(c): Two-Way Step | Two-way Hamiltonian post-selection improves distance metrics but lowers success probability. | `source_code/solution/tables/problem3c_analysis_guided_improvement.csv` | "This follows directly from 3-b: stronger contraction can help recovery, but post-selection has a cost." | 55s |
| 7 | Conclusion | The final result is novel, complete, and appropriate to a small state-vector benchmark without overclaiming. | none | "The final thesis is a reproducible trade-off story: strong baselines, measurement-induced denoising, and clear limitations." | 30s |

## 15-Minute Expanded Talk Plan

1. Title and contribution.
2. Problem map and submitted artifacts.
3. Metric definitions and target ensemble.
4. Problem 1 random-unitary diffusion with Haar reference.
5. Problem 2 Hamiltonian projected diffusion mechanism.
6. Problem 2(d) metric-aligned resource/control comparison.
7. Problem 3(a) measurement-induced denoising proxy.
8. Problem 3(b) axis-only vs continuous measurement-basis trade-off.
9. Problem 3(c) two-way post-selection candidate.
10. Seed robustness and appendix candidates.
11. Source-code reproducibility path.
12. Limitations and final thesis.

## Q&A Appendix Plan

- A1. Metric definitions: fidelity, MMD, Wasserstein-type cost `1-F`.
- A2. Hamiltonian and projected ensemble equations.
- A3. Problem 3(a) measurement-induced non-unitary map.
- A4. Axis-only vs continuous basis explanation.
- A5. Problem 3(c) comparison table.
- A6. Seed robustness and holdout evidence.
- A7. Source-code package and reproduction commands.
- A8. Limitations and claim guardrails.

## Core Story

The first 5 minutes tell the complete story: Problem 1 establishes strong random-unitary scrambling, Problem 2 introduces fixed Hamiltonian projected diffusion and its resource/control profile, Problem 3(b) reframes measurement basis as a control knob for an effective non-unitary map, and Problem 3(c) tests two-way post-selection as a stronger but costlier improvement.

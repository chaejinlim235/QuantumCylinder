# QuantumCylinder Presentation Storyboard

## Main-Round 5-Minute Core Path

Use this path when the talk time is limited to 5 minutes.

| Step | Content | Slides / artifacts | Time |
| --- | --- | --- | ---: |
| 1 | Thesis: projected denoising is a recoverability-success-diversity trade-off. | Slide 1 | 0:40 |
| 2 | Problem 1/2 baselines: random-unitary strong scrambling with Haar reference, then fixed-\(H\) projected diffusion and resource/control comparison. | Slides 3-4; `source_code/solution/figures/fig2_random_unitary_haar_baseline.png`, `source_code/solution/figures/fig_metric_aligned_comparison_readable.png` | 1:20 |
| 3 | Problem 3(b): measurement-basis trade-off plus IBM Cloud validation callout on `ibm_fez`. | Slide 5; `source_code/solution/tables/problem3b_measurement_basis_tradeoff.csv` | 1:20 |
| 4 | Problem 3(c): two-way post-selection improves distance metrics with lower \(p_{\mathrm{succ}}\). | Slide 6; `source_code/solution/tables/problem3c_analysis_guided_improvement.csv` | 1:00 |
| 5 | Judging criteria: complete, faithful, novel, reproducible, and scoped without overclaiming. | Slide 7 | 0:40 |

## Front-Facing 15-Minute Talk Plan

| Slide | Title | Key message | Figure/table path | Speaker note | Time |
| --- | --- | --- | --- | --- | ---: |
| 1 | QuantumCylinder | We compare two diffusion mechanisms and analyze projected denoising as a recoverability-success-diversity trade-off. | none | "This is a complete small-scale benchmark, not an overclaim." | 1:00 |
| 2 | Problem Map and Criteria | The package answers Problem 1(a) through Problem 3(c) and includes inspectable source code. | `source_code/PROBLEM_REQUIREMENT_MAP.md` | "The split notebooks support presentation reading; source_code supports inspection." | 1:00 |
| 3 | Metrics and Notation | All comparisons use fidelity-kernel MMD and Wasserstein-type distance with \(1-F\) cost. | `source_code/solution/solution_1.ipynb` | "Use \(S_0\), \(S_k^{\mathrm{RU}}\), and \(S_t^{\mathrm{Ham}}\) consistently." | 1:15 |
| 4 | Problem 1: Strong Scrambling | Random-unitary diffusion rapidly reaches a Haar-like distance plateau. | `source_code/solution/figures/fig2_random_unitary_haar_baseline.png` | "The Haar reference is a calibration level, not a training target." | 1:30 |
| 5 | Problem 2: Fixed-H Projected Diffusion | Fixed \(H\) projected diffusion has schedule-dependent fluctuation and saturation behavior. | `source_code/solution/figures/fig_p2_fixed_h_baseline_visible.png` | "Problem 2 uses fixed \(H\); measurement-basis variation is reserved for Problem 3(b)." | 1:30 |
| 6 | Problem 2(d): Resource/Control Cost | Compare random gate controls against fixed-Hamiltonian time and projection/readout control. | `source_code/solution/figures/fig_metric_aligned_comparison_readable.png` | "We compare by output metric strength, not equal raw x-axis values." | 1:30 |
| 7 | Problem 3(a): Measurement-Induced Denoising | Post-selection induces an effective non-unitary map on the data system. | `source_code/solution/figures/problem_3a_denoising_improvement.png` | "This is a denoising proxy, not a full trainable QuDDPM." | 1:15 |
| 8 | Problem 3(b): Trade-Off | Measurement basis controls recoverability, success probability, and diversity retention; IBM Cloud validation confirms tiny-circuit executability of the mechanism. | `source_code/solution/tables/problem3b_measurement_basis_tradeoff.csv` | "The axis-only margin is small; the claim is the trade-off analysis. IBM validates execution of the mechanism, not hardware advantage." | 2:00 |
| 9 | Problem 3(c): Two-Way Step | Two-way Hamiltonian post-selection improves distance metrics but lowers \(p_{\mathrm{succ}}\). | `source_code/solution/tables/problem3c_analysis_guided_improvement.csv` | "This follows directly from 3-b: stronger contraction has a cost." | 1:45 |
| 10 | Robustness and Appendix Candidates | Seed sweep and portfolio rows support the chosen main story while keeping optional methods scoped. | `source_code/solution/tables/problem_3_seed_sweep_summary.md` | "Actor-critic is target-aware appendix material only." | 0:55 |
| 11 | Source-Code Inspection Path | Judges can reproduce the compact benchmark and inspect scripts/tests quickly. | `source_code/README_FOR_JUDGES.md` | "The source package is self-contained for inspection." | 0:55 |
| 12 | Limitations and Final Thesis | The result is novel, complete, appropriate, and carefully scoped. | none | "No quantum advantage, hardware advantage, full QuDDPM, or universal dominance claim." | 0:20 |

Total planned time: 15:00.

IBM QPU job-level details remain Q&A appendix material, but the core Problem
3(b) slide includes a short hardware-execution validation callout.

## Backup 5-Minute Core Talk Plan

| Slide | Title | Key message | Figure/table path | Speaker note | Time |
| --- | --- | --- | --- | --- | ---: |
| 1 | QuantumCylinder | We compare two diffusion mechanisms and analyze projected denoising as a recoverability-success-diversity trade-off. | none | "Our contribution is a connected final solution: Problems 1 and 2 establish comparable diffusion baselines, and Problem 3 turns post-selection into a measurable denoising trade-off." | 30s |
| 2 | Problem Map and Criteria | The split notebooks answer Problem 1(a) through Problem 3(c), and the package includes source code and final artifacts. | `solution/Problem 1.ipynb`, `solution/Problem 2.ipynb`, `solution/Problem 3.ipynb` | "The structure follows the problem statement and the judging criteria: completeness, fidelity, novelty, and presentation clarity." | 35s |
| 3 | Problem 1: Strong Scrambling | Random-unitary diffusion rapidly reaches a Haar-like distance plateau, destroying the original `|00>` cluster. | `source_code/solution/figures/fig2_random_unitary_haar_baseline.png` | "The Haar line is a reference, not a training target. The lower zoom panels make the Haar mean and one-standard-deviation band visible in the plateau region. The important interpretation is strong scrambling, not slow Gaussian diffusion." | 45s |
| 4 | Problem 2: Projected Diffusion | \(S_t^{\mathrm{Ham}}\) uses fixed \(H\) evolution and complement-qubit projection, with schedule-dependent behavior. | `source_code/solution/figures/fig_metric_aligned_comparison_readable.png` | "We compare by output metric strength, not equal x-axis values, because random layer count \(k\) and Hamiltonian time \(t\) are different controls. The fixed-\(H\) baseline is also shown in `source_code/solution/figures/fig_p2_fixed_h_baseline_visible.png`." | 45s |
| 5 | Problem 3(b): Trade-Off | Measurement basis controls the effective non-unitary map, so denoising must be judged by \(\Delta D\), \(p_{\mathrm{succ}}\), and \(R_{\mathrm{div}}\). | `source_code/solution/tables/problem3b_measurement_basis_tradeoff.csv` | "The continuous basis margin over axis-only is small. The novelty is the trade-off analysis, not simply scanning bases." | 60s |
| 6 | Problem 3(c): Two-Way Step | Two-way Hamiltonian post-selection improves distance metrics but lowers \(p_{\mathrm{succ}}\). | `source_code/solution/tables/problem3c_analysis_guided_improvement.csv` | "This follows directly from 3-b: stronger contraction can help recovery, but post-selection has a cost." | 55s |
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

- A1. Notation and metric definitions: \(S_0\), \(S_k^{\mathrm{RU}}\), \(S_t^{\mathrm{Ham}}\), \(D_{\mathrm{MMD}}\), \(W_{1-F}\), \(p_{\mathrm{succ}}\), \(R_{\mathrm{div}}\), and \(\beta\).
- A2. Hamiltonian and projected ensemble equations.
- A3. Problem 3(a) measurement-induced non-unitary map.
- A4. Axis-only vs continuous basis explanation.
- A5. Problem 3(c) comparison table.
- A6. Seed robustness and holdout evidence.
- A7. Source-code package and reproduction commands.
- A8. Limitations and claim guardrails.
- A9. IBM QPU Problem 3-b mini validation: completed tiny `M+F` Qiskit Runtime runs on `ibm_fez` showing that complement-qubit measurement basis changes post-selection success probability and selected data distribution.

## Core Story

The first 5 minutes tell the complete story: Problem 1 establishes strong random-unitary scrambling \(S_k^{\mathrm{RU}}\), Problem 2 introduces fixed-Hamiltonian projected diffusion \(S_t^{\mathrm{Ham}}\) and its resource/control profile, Problem 3(b) reframes measurement-basis angle \(\beta\) as a control knob for an effective non-unitary map, and Problem 3(c) tests two-way post-selection as a stronger but costlier improvement.

The IBM QPU path is a core validation callout plus Q&A detail. It checks a tiny
Problem 3-b measurement-basis sweep through IBM Quantum / Qiskit Runtime. The
completed jobs `d91r6pmu9n7c73an9qgg` and `d91r71fccmks73d5nmg0` are
hardware-execution validation only and do not replace the reproducible
state-vector benchmark.

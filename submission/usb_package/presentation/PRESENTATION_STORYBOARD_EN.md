# QuantumCylinder Presentation Storyboard

## Deck Route

This is a single submitted 15-minute-capable deck.

- Main round: follow the 5-minute core path.
- Final round: use the same deck in the 15-minute expanded path.
- Q&A: use the appendix slides from the same deck.
- No separate 5-minute deck is submitted.

Do not prepare or present a separate deck.

## Main-Round 5-Minute Core Path

Use this path when the talk time is limited to 5 minutes.

1. Thesis, 0:40.
   Projected denoising is a recoverability-success-diversity trade-off.
   Use Slide 1.

2. Problem 1/2 baselines, 1:20.
   Random-unitary diffusion reaches a strong-scrambling Haar-like plateau.
   Then show fixed-\(H\) projected diffusion and the resource/control
   comparison.
   Use Slides 3-4 and:
   - `source_code/solution/figures/fig2_random_unitary_haar_baseline.png`
   - `source_code/solution/figures/fig_metric_aligned_comparison_readable.png`

3. Problem 3(b), 1:20.
   Measurement-basis trade-off plus IBM Cloud validation callout on `ibm_fez`.
   Use Slide 5 and:
   - `source_code/solution/tables/problem3b_measurement_basis_tradeoff.csv`

4. Problem 3(c), 1:00.
   Two-way post-selection improves distance metrics with lower
   \(p_{\mathrm{succ}}\).
   Use Slide 6 and:
   - `source_code/solution/tables/problem3c_analysis_guided_improvement.csv`

5. Judging fit, 0:40.
   Complete, faithful, novel, reproducible, and scoped without overclaiming.
   Use Slide 7.

## Front-Facing 15-Minute Talk Plan

1. Slide 1, QuantumCylinder, 1:00.
   Key message: compare two diffusion mechanisms and analyze projected
   denoising as a recoverability-success-diversity trade-off.
   Speaker note: "This is a complete small-scale benchmark, not an overclaim."

2. Slide 2, Problem Map and Criteria, 1:00.
   Key message: the package answers Problem 1(a) through Problem 3(c) and
   includes inspectable source code.
   Artifact: `source_code/PROBLEM_REQUIREMENT_MAP.md`.
   Speaker note: "The split notebooks support presentation reading;
   source_code supports inspection."

3. Slide 3, Metrics and Notation, 1:15.
   Key message: all comparisons use fidelity-kernel MMD and Wasserstein-type
   distance with \(1-F\) cost.
   Artifact: `source_code/solution/solution_1.ipynb`.
   Speaker note: "Use \(S_0\), \(S_k^{\mathrm{RU}}\), and
   \(S_t^{\mathrm{Ham}}\) consistently."

4. Slide 4, Problem 1: Strong Scrambling, 1:30.
   Key message: random-unitary diffusion rapidly reaches a Haar-like distance
   plateau.
   Artifact: `source_code/solution/figures/fig2_random_unitary_haar_baseline.png`.
   Speaker note: "The Haar reference is a calibration level, not a training
   target."

5. Slide 5, Problem 2: Fixed-H Projected Diffusion, 1:30.
   Key message: fixed \(H\) projected diffusion has schedule-dependent
   fluctuation and saturation behavior.
   Artifact: `source_code/solution/figures/fig_p2_fixed_h_baseline_visible.png`.
   Speaker note: "Problem 2 uses fixed \(H\); measurement-basis variation is
   reserved for Problem 3(b)."

6. Slide 6, Problem 2(d): Resource/Control Cost, 1:30.
   Key message: compare random gate controls against fixed-Hamiltonian time
   and projection/readout control.
   Artifact: `source_code/solution/figures/fig_metric_aligned_comparison_readable.png`.
   Speaker note: "We compare by output metric strength, not equal raw x-axis
   values."

7. Slide 7, Problem 3(a): Measurement-Induced Denoising, 1:15.
   Key message: post-selection induces an effective non-unitary map on the data
   system.
   Artifact: `source_code/solution/figures/problem_3a_denoising_improvement.png`.
   Speaker note: "This is a denoising proxy, not a full trainable QuDDPM."

8. Slide 8, Problem 3(b): Trade-Off, 2:00.
   Key message: measurement basis controls recoverability, success probability,
   and diversity retention.
   IBM Cloud validation confirms tiny-circuit executability of the mechanism.
   Artifact: `source_code/solution/tables/problem3b_measurement_basis_tradeoff.csv`.
   Speaker note: "The axis-only margin is small; the claim is the trade-off
   analysis. IBM validates execution of the mechanism, not hardware advantage."

9. Slide 9, Problem 3(c): Two-Way Step, 1:45.
   Key message: two-way Hamiltonian post-selection improves distance metrics
   but lowers \(p_{\mathrm{succ}}\).
   Artifact: `source_code/solution/tables/problem3c_analysis_guided_improvement.csv`.
   Speaker note: "This follows directly from 3-b: stronger contraction has a
   cost."

10. Slide 10, Robustness and Appendix Candidates, 0:55.
    Key message: seed sweep and portfolio rows support the chosen main story
    while keeping optional methods scoped.
    Artifact: `source_code/solution/tables/problem_3_seed_sweep_summary.md`.
    Speaker note: "Actor-critic is target-aware appendix material only."

11. Slide 11, Source-Code Inspection Path, 0:55.
    Key message: judges can reproduce the compact benchmark and inspect
    scripts/tests quickly.
    Artifact: `source_code/README_FOR_JUDGES.md`.
    Speaker note: "The source package is self-contained for inspection."

12. Slide 12, Limitations and Final Thesis, 0:20.
    Key message: the result is novel, complete, appropriate, and carefully
    scoped.
    Speaker note: "No quantum advantage, hardware advantage, full QuDDPM, or
    universal dominance claim."

Total planned time: 15:00.

IBM QPU job-level details remain Q&A appendix material, but the core Problem
3(b) slide includes a short hardware-execution validation callout.

## Backup 5-Minute Core Talk Plan

1. Slide 1, 30s.
   Thesis: compare two diffusion mechanisms and analyze projected denoising as
   a recoverability-success-diversity trade-off.

2. Slide 2, 35s.
   The split notebooks answer Problem 1(a) through Problem 3(c), and the
   package includes source code and final artifacts.

3. Slide 3, 45s.
   Random-unitary diffusion rapidly reaches a Haar-like distance plateau.
   The Haar line is a reference, not a training target.

4. Slide 4, 45s.
   \(S_t^{\mathrm{Ham}}\) uses fixed \(H\) evolution and complement-qubit
   projection, with schedule-dependent behavior.

5. Slide 5, 60s.
   Measurement basis controls the effective non-unitary map, so denoising must
   be judged by \(\Delta D\), \(p_{\mathrm{succ}}\), and \(R_{\mathrm{div}}\).
   Include the IBM Cloud validation callout here.

6. Slide 6, 55s.
   Two-way Hamiltonian post-selection improves distance metrics but lowers
   \(p_{\mathrm{succ}}\).

7. Slide 7, 30s.
   The final result is novel, complete, and appropriate to a small state-vector
   benchmark without overclaiming.

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

- A1. Notation and metric definitions:
  \(S_0\), \(S_k^{\mathrm{RU}}\), \(S_t^{\mathrm{Ham}}\),
  \(D_{\mathrm{MMD}}\), \(W_{1-F}\), \(p_{\mathrm{succ}}\),
  \(R_{\mathrm{div}}\), and \(\beta\).
- A2. Hamiltonian and projected ensemble equations.
- A3. Problem 3(a) measurement-induced non-unitary map.
- A4. Axis-only vs continuous basis explanation.
- A5. Problem 3(c) comparison table.
- A6. Seed robustness and holdout evidence.
- A7. Source-code package and reproduction commands.
- A8. Limitations and claim guardrails.
- A9. IBM QPU Problem 3-b mini validation:
  completed tiny `M+F` Qiskit Runtime runs on `ibm_fez` showing that the
  complement-qubit measurement basis changes post-selection success probability
  and the selected data distribution.

## Core Story

The first 5 minutes tell the complete story:

- Problem 1 establishes strong random-unitary scrambling
  \(S_k^{\mathrm{RU}}\).
- Problem 2 introduces fixed-Hamiltonian projected diffusion
  \(S_t^{\mathrm{Ham}}\) and its resource/control profile.
- Problem 3(b) reframes measurement-basis angle \(\beta\) as a control knob for
  an effective non-unitary map.
- Problem 3(c) tests two-way post-selection as a stronger but costlier
  improvement.

The IBM QPU path is a core validation callout plus Q&A detail. It checks a tiny
Problem 3-b measurement-basis sweep through IBM Quantum / Qiskit Runtime. The
completed jobs `d91r6pmu9n7c73an9qgg` and `d91r71fccmks73d5nmg0` are
hardware-execution validation only and do not replace the reproducible
state-vector benchmark.

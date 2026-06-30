# Judging Criteria Alignment

## 1. Completeness and Appropriateness of Result

The submission contains both English presentation material and source code. The final notebook answers Problem 1(a) through Problem 3(c), with final figures and tables included in `source_code/solution/figures/` and `source_code/solution/tables/`. Source code is included under `source_code/` with reproduction commands.

Evidence:

- `source_code/solution/solution_1.ipynb`
- `source_code/solution/figures/`
- `source_code/solution/tables/`
- `source_code/src/`
- `source_code/scripts/`
- `source_code/tests/`
- `source_code/submission/run_all.py`
- `presentation/QuantumCylinder_presentation.pdf`

The approach is appropriate to the small 2-qubit/3-qubit state-vector benchmark. We do not claim a full trainable QuDDPM, quantum advantage, or hardware advantage.

Optional IBM QPU validation is included only as appendix evidence for tiny
representative circuits. It checks hardware-execution feasibility through IBM
Quantum / Qiskit Runtime and does not overclaim hardware performance.

## 2. Fidelity to Problem Requirements

Each required subproblem is mapped to a concrete artifact in `source_code/PROBLEM_REQUIREMENT_MAP.md`.

Summary:

- Problem 1(a): target ensemble around `|00>`.
- Problem 1(b): fidelity, MMD, and Wasserstein-type distance with cost `1 - F`.
- Problem 1(c): random-unitary diffusion with Haar-like strong-scrambling interpretation.
- Problem 2(a)-(c): fixed Hamiltonian, projected ensemble construction, and qualitative comparison.
- Problem 2(d): resource/control-cost proxy comparison.
- Problem 3(a): simple measurement-induced denoising step.
- Problem 3(b): measurement-basis trade-off analysis.
- Problem 3(c): two-way post-selection as analysis-guided improvement.

## 3. Novelty of Plan and Approach

The novelty is to interpret the complement-qubit measurement basis as a control knob for the effective non-unitary map induced on the data system. This converts Problem 3 into a recoverability-success-diversity trade-off analysis, and motivates the two-way post-selection improvement in Problem 3(c).

This framing emphasizes that:

- measurement basis controls the effective non-unitary projected map;
- distance gain alone is insufficient;
- success probability measures post-selection cost;
- diversity retention protects against trivial collapse;
- two-way post-selection is stronger but costlier, not an unconditional win.

## 4. Presentation and Communication Quality

The presentation material is English. The first 5 minutes cover the full core story: Problem 1/2 baselines, Problem 3(b) trade-off, and Problem 3(c) two-way improvement. Appendix slides support Q&A and a longer final-round presentation using the same submitted material.

IBM QPU details are kept in the appendix for Q&A only, so the main presentation
remains focused on the traceable state-vector results and problem requirements.

Presentation files:

- `presentation/QuantumCylinder_presentation.pdf`
- `presentation/PRESENTATION_STORYBOARD_EN.md`
- `presentation/PRESENTATION_SLIDE_TEXT_EN.md`
- `presentation/SLIDE_CHECKLIST.md`

# USB Submission Guide

This is the top-level guide for the QuantumCylinder USB package.

## What To Open First

For a five-minute review, open:

1. `Summary.md`
2. `solution/Problem 1.ipynb`
3. `solution/Problem 2.ipynb`
4. `solution/Problem 3.ipynb`

For the submitted presentation, open:

1. `presentation/QuantumCylinder_presentation.pdf`
2. `presentation/PRESENTATION_STORYBOARD_EN.md`
3. `presentation/PRESENTATION_15MIN_SPEAKER_SCRIPT_EN.md`
4. `presentation/MANUAL_PRESENTATION_EXPORT_GUIDE.md`

The submitted presentation material is one same 15-minute-capable English
deck. Main round uses the 5-minute core path. Final round uses the same deck
and expands into the 15-minute path. No separate 5-minute deck is submitted.

For source-code inspection, open:

1. `source_code/README_FOR_JUDGES.md`
2. `source_code/PROBLEM_REQUIREMENT_MAP.md`
3. `source_code/REPRODUCIBILITY_COMMANDS.md`
4. `source_code/solution/solution_1.ipynb` as a compact reference only

## What Is Included

- Primary judge-facing split notebooks for Problem 1, Problem 2, and Problem 3.
- English presentation PDF, text, storyboard, speaker script, and checklist.
- Full source-code package with `src/`, `scripts/`, `tests/`, `configs/`,
  `submission/`, and `solution/`.
- Final figures and tables inside `source_code/solution/`.
- IBM Cloud/QPU Problem 3(b) hardware-execution validation evidence and scripts.
- `QuantumCylinder_full_source.zip`, a zipped copy of the source-code package.

## What The Submission Claims

The core idea is that complement-qubit measurement basis controls an effective
post-selected non-unitary map. The final story emphasizes the
recoverability-success-diversity trade-off:

- stronger distance improvement can require lower post-selection success;
- continuous-basis search has only a small margin over axis-only projection;
- two-way post-selection in Problem 3(c) is motivated by the Problem 3(b)
  trade-off analysis.

## What The Submission Does Not Claim

The submission does not claim quantum advantage, hardware advantage, a full
trainable QuDDPM, continuous-basis dominance over axis-only bases, a general
unknown-target actor-critic denoiser, or universal superiority of Hamiltonian
projected diffusion over random-unitary diffusion.

IBM QPU material is hardware-execution validation for the tiny Problem 3(b)
mechanism. It is included as a short core callout and detailed appendix/Q&A
material, with no hardware advantage or superiority claim.

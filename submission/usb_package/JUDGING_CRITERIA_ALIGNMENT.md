# Judging Criteria Alignment

This package is organized around the official criteria: completeness and
appropriateness, fidelity to requirements, novelty of approach, presentation
quality, source-code inspection readiness, and optional IBM QPU validation
clarity.

## Completeness And Appropriateness

The USB package contains:

- final split notebooks under `solution/`;
- compact final source-code notebook under `source_code/solution/`;
- English presentation text, storyboard, and checklist under `presentation/`;
- full source code under `source_code/`;
- tests, configs, scripts, final figures, and final tables;
- quick and extended reproduction commands;
- limitation and claim-guardrail documents.

The result is appropriate to the problem scale: it is a small state-vector
benchmark with traceable metrics and explicitly reported trade-offs.

## Fidelity To Problem Requirements

Problems 1(a) through 3(c) are mapped in
`source_code/PROBLEM_REQUIREMENT_MAP.md`.

Key requirement checks:

- Problem 1(c) includes random-unitary distance curves and a Haar-like
  strong-scrambling interpretation.
- Problem 2 compares random-unitary and Hamiltonian projected diffusion,
  including resource/control-cost proxies.
- Problem 3(a) includes a measurement-induced denoising step.
- Problem 3(b) analyzes a controlled measurement-basis trade-off rather than
  only listing metric values.
- Problem 3(c) follows directly from 3(b) by testing two-way post-selection
  against baseline/reference rows.

## Novelty Of Approach

The novelty is the framing of complement-qubit measurement basis as a control
knob for the effective projected non-unitary map. The main conceptual result is
not a blanket performance claim; it is the
recoverability-success-diversity trade-off.

Two-way post-selection follows from the 3-b analysis because it pushes the
selected ensemble closer by applying a stronger filter, while reducing success
probability.

## Presentation And Communication

`Summary.md` gives the five-minute path. The presentation files are in English
and separate the core story from appendix/Q&A material. IBM QPU details are
kept in appendix material and do not distract from the state-vector benchmark.

## Source-Code Inspection Readiness

`source_code/README_FOR_JUDGES.md`, `CODE_MANIFEST.md`, and
`REPRODUCIBILITY_COMMANDS.md` provide the inspection path, file map, and exact
commands. `QuantumCylinder_full_source.zip` is a zipped copy of the
source-code package.

## IBM QPU Validation Clarity

IBM QPU validation is optional appendix evidence. It checks tiny circuits and
the Problem 3-b measurement-basis mechanism on `ibm_fez`, but the main claims
remain state-vector based.

Completed included jobs:

- `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE;
- `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

No hardware advantage is claimed.

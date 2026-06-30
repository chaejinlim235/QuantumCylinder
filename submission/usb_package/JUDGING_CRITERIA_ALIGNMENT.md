# Judging Criteria Alignment

## Completeness And Appropriateness

The package contains notebook-first final answers, English presentation
material, source code, tests, final figures/tables, reproducibility commands,
and optional IBM QPU appendix validation.

IBM QPU validation is appendix-only and does not overclaim hardware
performance. The main scientific claims remain based on reproducible
state-vector experiments.

## Fidelity To Problem Requirements

Problems 1(a) through 3(c) are answered in the final notebooks and supported by
source-code artifacts. Problem 3-b is treated as a measurement-basis
recoverability-success-diversity trade-off, and Problem 3-c follows with
two-way post-selection as an analysis-guided improvement.

## Novelty Of Approach

The novelty is the framing of complement-qubit measurement basis as a control
knob for the effective projected non-unitary map, analyzed through distance,
success probability, and diversity retention. IBM validation supports this
measurement-basis effective-map mechanism on tiny circuits, but the novelty is
still the recoverability-success-diversity trade-off analysis.

## Presentation And Communication

The first review path is `Summary.md` plus the three problem notebooks. The IBM
QPU material is kept in appendix/Q&A material and explicitly states that no
hardware advantage is claimed.

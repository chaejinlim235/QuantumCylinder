# QuantumCylinder 15-Minute Speaker Script

This script supports the submitted 15-minute-capable English deck. For the
main round, use the 5-minute core path in `PRESENTATION_STORYBOARD_EN.md`.

## Slide 1. Thesis - 1:00

QuantumCylinder compares random-unitary diffusion, fixed-Hamiltonian projected
diffusion, and measurement-induced projected denoising. The central result is
a recoverability-success-diversity trade-off, not an overclaim.

## Slide 2. Problem Map - 1:00

The primary judge-facing report is split across `solution/Problem 1.ipynb`,
`solution/Problem 2.ipynb`, and `solution/Problem 3.ipynb`. The source-code
inspection package is under `source_code/`.

## Slide 3. Metrics - 1:15

All comparisons use \(D_{\mathrm{MMD}}\) and \(W_{1-F}\), with
\(F(\psi,\phi)=|\langle\psi|\phi\rangle|^2\). We compare ensembles against
\(S_0\), using \(S_k^{\mathrm{RU}}\) for random-unitary layers and
\(S_t^{\mathrm{Ham}}\) for Hamiltonian projected diffusion.

## Slide 4. Problem 1 - 1:30

Random-unitary scrambling rapidly reaches a Haar-like reference plateau. The
Haar line is a reference level, not a training target. The final figure makes
the Haar mean and one-standard-deviation band visible with a plateau zoom.

## Slide 5. Problem 2 - 1:30

Problem 2 uses fixed \(H\) evolution on `M+F` followed by complement projection
or readout. It is schedule-sensitive and can fluctuate, so the result is a
qualitative/control-cost comparison rather than a universal ranking.

## Slide 6. Problem 2(d) - 1:30

The resource discussion compares random gate-level controls with fixed
Hamiltonian time and projection/readout control at comparable output metric
strength.

## Slide 7. Problem 3(a) - 1:15

Measurement and post-selection on the complement qubit induce an effective
non-unitary map on the data system. This is a denoising proxy, not a full
trainable QuDDPM.

## Slide 8. Problem 3(b) - 2:00

The controlled modification is the complement-qubit measurement basis. Report
\(\Delta D\), \(p_{\mathrm{succ}}\), and \(R_{\mathrm{div}}\) together. The
continuous-basis margin over axis-only projection is small, so the claim is the
trade-off analysis.

IBM Cloud validation: tiny `M+F` measurement-basis sweep circuits completed on
`ibm_fez`. The higher-shot run shows \(p(F=0)\) changing from about `0.89` to
`0.66` to `0.35` as \(\beta\) rotates, with selected-data entropy increasing.
This validates hardware executability of the 3-b mechanism; no hardware
advantage is claimed.

## Slide 9. Problem 3(c) - 1:45

Two-way Hamiltonian post-selection follows from 3(b): stronger contraction can
improve distance metrics but lowers \(p_{\mathrm{succ}}\). It is a trade-off
improvement, not an unconditional win.

## Slide 10. Robustness - 0:55

Seed sweep and method-portfolio files support the main story. Actor-critic
rows are target-aware appendix evidence only, not a general unknown-target
denoiser.

## Slide 11. Source-Code Inspection - 0:55

Start from `source_code/README_FOR_JUDGES.md`, then inspect
`PROBLEM_REQUIREMENT_MAP.md`, `REPRODUCIBILITY_COMMANDS.md`, source files,
scripts, and tests.

## Slide 12. Final Thesis - 0:20

Measurement basis controls an effective projected map, creating a measurable
recoverability-success-diversity trade-off that motivates two-way
post-selection within a scoped, reproducible benchmark.

## Q&A Note

Detailed IBM job IDs and aggregate tables remain in appendix A9 and
`source_code/results/ibm_qpu_validation/`.

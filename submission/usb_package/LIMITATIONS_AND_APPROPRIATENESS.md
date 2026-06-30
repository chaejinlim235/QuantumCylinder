# Limitations and Appropriateness

## Scope

This submission is a small 2-qubit/3-qubit state-vector benchmark. It is designed to answer the contest problem requirements with reproducible code, final figures, and clear trade-off analysis.

## What We Do Not Claim

- No quantum advantage claim.
- No hardware advantage claim.
- No full trainable QuDDPM claim.
- No claim that continuous measurement bases strongly or always beat axis-only Pauli bases.
- No claim that Hamiltonian projected diffusion is always better than random-unitary diffusion.
- No claim that actor-critic is a general unknown-target denoiser.

## Guardrails

- The continuous-basis margin over axis-only is small, so the result is reported as a trade-off analysis.
- Two-way post-selection improves distance metrics but lowers success probability.
- Actor-critic is target-aware if mentioned because its reward uses the raw target ensemble.
- The Haar baseline is a reference level, not a training target.
- The random-unitary curve is interpreted as strong scrambling toward a Haar-like/high-distance plateau, not as a slow Gaussian DDPM-like diffusion schedule.

## Appropriateness

The problem permits a fixed measurement-induced non-unitary map or shallow toy denoising step. The submitted result stays within that scale, reports post-selection success probability and diversity retention, and avoids overclaiming.

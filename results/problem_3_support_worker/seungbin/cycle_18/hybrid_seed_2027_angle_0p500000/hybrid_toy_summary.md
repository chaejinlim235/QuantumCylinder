# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.330910`
- median Wasserstein improvement: `0.071378`
- median diversity retention: `1.849371`
- median success probability: `0.286426`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.158384 -> 0.030630` | `0.015403 -> 0.011608` | `2.289507` | `0.282780` | `1.675000` | `2.356194` | `0.785398` | `0.250000` |
| `2` | `0.317747 -> 0.048818` | `0.057708 -> 0.021410` | `2.394538` | `0.251033` | `1.675000` | `2.748894` | `0.000000` | `-0.100000` |
| `4` | `0.547674 -> 0.048028` | `0.166084 -> 0.025241` | `1.409235` | `0.290072` | `1.837500` | `3.141593` | `3.141593` | `-0.100000` |
| `8` | `0.455057 -> 0.062167` | `0.140643 -> 0.034185` | `0.912684` | `0.724502` | `0.375000` | `0.000000` | `0.000000` | `-0.100000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

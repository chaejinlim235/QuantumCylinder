# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.343719`
- median Wasserstein improvement: `0.082006`
- median diversity retention: `1.031774`
- median success probability: `0.356360`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.175058 -> 0.030244` | `0.017395 -> 0.005915` | `1.680525` | `0.101601` | `0.537500` | `0.785398` | `2.356194` | `0.000000` |
| `2` | `0.347772 -> 0.045309` | `0.068562 -> 0.011972` | `1.143720` | `0.317231` | `1.837500` | `2.748894` | `1.570796` | `-0.100000` |
| `4` | `0.549275 -> 0.054697` | `0.174148 -> 0.016928` | `0.706019` | `0.395490` | `2.000000` | `2.748894` | `1.570796` | `0.000000` |
| `8` | `0.459144 -> 0.074169` | `0.148333 -> 0.040910` | `0.919828` | `0.601234` | `0.375000` | `0.392699` | `3.141593` | `0.100000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

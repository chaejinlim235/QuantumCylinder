# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.344452`
- median Wasserstein improvement: `0.130764`
- median diversity retention: `0.708889`
- median success probability: `0.409290`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.314074 -> 0.062071` | `0.069370 -> 0.016693` | `0.637685` | `0.395043` | `2.000000` | `2.356194` | `1.570796` | `-0.100000` |
| `2` | `0.534653 -> 0.065760` | `0.187121 -> 0.027558` | `0.658269` | `0.423536` | `2.000000` | `2.748894` | `1.570796` | `-0.100000` |
| `4` | `0.456544 -> 0.151250` | `0.191069 -> 0.089105` | `0.886574` | `0.370483` | `0.537500` | `0.392699` | `3.141593` | `0.000000` |
| `8` | `0.566817 -> 0.183207` | `0.277286 -> 0.104890` | `0.759510` | `0.428648` | `2.000000` | `2.748894` | `1.570796` | `0.100000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.211078`
- median Wasserstein improvement: `0.223252`
- median diversity retention: `0.573138`
- median success probability: `0.505744`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.719585 -> 0.272011` | `0.448022 -> 0.136230` | `0.574182` | `0.561145` | `2.000000` | `2.748894` | `0.785398` | `0.100000` |
| `2` | `0.554864 -> 0.415779` | `0.363078 -> 0.199420` | `0.572094` | `0.518937` | `2.000000` | `1.570796` | `1.570796` | `-0.100000` |
| `4` | `0.686311 -> 0.472919` | `0.453573 -> 0.217540` | `0.501200` | `0.465605` | `2.000000` | `1.178097` | `2.356194` | `0.100000` |
| `8` | `0.683023 -> 0.474259` | `0.453574 -> 0.243103` | `0.620668` | `0.492550` | `2.000000` | `1.963495` | `1.570796` | `0.250000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

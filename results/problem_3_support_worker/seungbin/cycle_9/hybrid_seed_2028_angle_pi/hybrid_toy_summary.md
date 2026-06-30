# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.190133`
- median Wasserstein improvement: `0.207324`
- median diversity retention: `0.564744`
- median success probability: `0.532927`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.796529 -> 0.271356` | `0.484907 -> 0.127102` | `0.569518` | `0.575712` | `2.000000` | `2.748894` | `0.785398` | `0.250000` |
| `2` | `0.501011 -> 0.359177` | `0.325596 -> 0.187125` | `0.639984` | `0.460286` | `2.000000` | `1.963495` | `1.570796` | `0.250000` |
| `4` | `0.572260 -> 0.406591` | `0.375885 -> 0.196883` | `0.559970` | `0.526503` | `2.000000` | `1.963495` | `1.570796` | `0.000000` |
| `8` | `0.732303 -> 0.517706` | `0.487608 -> 0.251963` | `0.552002` | `0.539352` | `2.000000` | `2.748894` | `1.570796` | `0.250000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

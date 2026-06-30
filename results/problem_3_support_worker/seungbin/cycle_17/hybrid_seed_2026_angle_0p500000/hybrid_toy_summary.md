# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.318559`
- median Wasserstein improvement: `0.065838`
- median diversity retention: `1.445903`
- median success probability: `0.250368`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.164465 -> 0.036637` | `0.016926 -> 0.008898` | `1.641106` | `0.103050` | `0.537500` | `0.785398` | `2.356194` | `0.000000` |
| `2` | `0.322968 -> 0.067834` | `0.062971 -> 0.031857` | `2.359258` | `0.249794` | `1.675000` | `2.748894` | `0.000000` | `-0.100000` |
| `4` | `0.536359 -> 0.052393` | `0.162927 -> 0.025620` | `1.250701` | `0.250941` | `0.375000` | `1.178097` | `1.570796` | `-0.100000` |
| `8` | `0.444297 -> 0.062312` | `0.133642 -> 0.033081` | `0.920469` | `0.722078` | `0.375000` | `0.000000` | `0.000000` | `-0.100000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

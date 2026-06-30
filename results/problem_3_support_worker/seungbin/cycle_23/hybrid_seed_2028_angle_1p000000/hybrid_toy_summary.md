# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.315958`
- median Wasserstein improvement: `0.136046`
- median diversity retention: `0.794272`
- median success probability: `0.388320`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.335704 -> 0.060015` | `0.070586 -> 0.020072` | `1.175131` | `0.324903` | `1.837500` | `2.748894` | `1.570796` | `-0.100000` |
| `2` | `0.572897 -> 0.082108` | `0.206013 -> 0.032198` | `0.729333` | `0.396915` | `2.000000` | `2.748894` | `1.570796` | `0.000000` |
| `4` | `0.468361 -> 0.148658` | `0.194691 -> 0.082650` | `0.859211` | `0.379724` | `0.537500` | `0.392699` | `3.141593` | `0.000000` |
| `8` | `0.530450 -> 0.218238` | `0.279532 -> 0.119481` | `0.697373` | `0.464554` | `2.000000` | `2.748894` | `1.570796` | `0.100000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

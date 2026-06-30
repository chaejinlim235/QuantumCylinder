# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.364544`
- median Wasserstein improvement: `0.138537`
- median diversity retention: `0.684375`
- median success probability: `0.395815`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.302953 -> 0.063620` | `0.062840 -> 0.015138` | `0.653498` | `0.392214` | `2.000000` | `2.356194` | `1.570796` | `-0.100000` |
| `2` | `0.519223 -> 0.077048` | `0.170213 -> 0.028057` | `0.715251` | `0.399416` | `2.000000` | `2.748894` | `1.570796` | `-0.100000` |
| `4` | `0.509127 -> 0.115924` | `0.202536 -> 0.067618` | `0.868486` | `0.366173` | `0.537500` | `0.392699` | `3.141593` | `0.100000` |
| `8` | `0.537038 -> 0.201153` | `0.270496 -> 0.092985` | `0.584977` | `0.483595` | `2.000000` | `2.356194` | `1.570796` | `0.250000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

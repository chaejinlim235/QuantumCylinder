# Problem 3 Hybrid Diffusion Toy Summary

## Purpose

This is a 2-qubit hardware-compatible extension candidate, not a replacement for the main 2-data-qubit state-vector result.

The toy mixes random-unitary corruption on one data qubit with a Hamiltonian-inspired two-qubit `M+F` block and auxiliary post-selection. It is intended to support the story that the Problem 3 idea can be translated toward IBM-style gate hardware at the smallest scale.

## Gate

- input steps: `[1, 2, 4, 8]`
- positive-improvement rows: `4 / 4`
- median MMD improvement: `0.256445`
- median Wasserstein improvement: `0.254705`
- median diversity retention: `0.617270`
- median success probability: `0.499056`

## Best Rows

| input step | MMD | Wasserstein | diversity retention | success probability | tau | theta | phi | pre-rotation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0.715766 -> 0.259393` | `0.436903 -> 0.138531` | `0.612471` | `0.552098` | `2.000000` | `2.748894` | `0.785398` | `0.100000` |
| `2` | `0.571902 -> 0.403854` | `0.376990 -> 0.210145` | `0.622327` | `0.479806` | `2.000000` | `1.963495` | `1.570796` | `0.000000` |
| `4` | `0.763883 -> 0.481986` | `0.511353 -> 0.224663` | `0.536399` | `0.488211` | `2.000000` | `1.178097` | `3.926991` | `-0.100000` |
| `8` | `0.694669 -> 0.463675` | `0.462355 -> 0.239635` | `0.622070` | `0.509900` | `2.000000` | `2.356194` | `1.570796` | `0.250000` |

## Claim Guidance

Use this only as a bonus extension unless later seed sweeps make it stronger. Safe wording:

> As a hardware-motivated extension, we tested a smallest-scale 1-data-qubit + 1-auxiliary-qubit hybrid diffusion toy. It shows how random-unitary scrambling and Hamiltonian-inspired projected dynamics can be expressed in an IBM-compatible two-qubit setting. We use it as circuit-level plausibility evidence, not as hardware advantage.

## Generated Files

- `hybrid_candidate_metrics.csv`
- `hybrid_best_metrics.csv`
- `hybrid_toy_metrics.png`
- `hybrid_toy_settings.json`

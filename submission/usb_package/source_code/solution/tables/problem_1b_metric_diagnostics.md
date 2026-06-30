# Problem 1(b) Metric Diagnostics

## Setup

- N: `80`
- sigma: `0.1`
- seed: `7`

## Target Cluster Sanity Check

- mean fidelity to `|00>`: `0.995692`
- min fidelity to `|00>`: `0.972637`
- max fidelity to `|00>`: `0.999970`
- std fidelity to `|00>`: `0.004599`

## Metric Sanity Check

- `MMD(S0, S0)`: `0.000000000000`
- `Wasserstein(S0, S0)`: `0.000000000000`
- `MMD(S1_random_unitary, S0)`: `0.882606`
- `Wasserstein(S1_random_unitary, S0)`: `0.733305`

The zero-distance self check verifies the Problem 1(b) metric implementation, and
the one-step random-unitary comparison confirms that the distances respond to a
scrambled ensemble.

# IBM QPU Validation Summary

Dry-run/transpilation path prepared; real IBM QPU submission requires IBM
credentials and queue availability.

## Current Status

- submitted: `False`
- primitive: `sampler`
- shots: `1000`
- required qubits: `3`
- backend: `None` in the local dry-run environment
- runtime status: `qiskit-ibm-runtime` unavailable in the local environment

## Dry-Run Circuits

| Circuit | Qubits | Transpiled depth | Two-qubit gates |
| --- | ---: | ---: | ---: |
| `problem1_random_unitary_one_step` | 2 | 4 | 2 |
| `hamiltonian_projection_tiny_proxy` | 3 | 8 | 4 |
| `two_way_postselection_tiny_proxy` | 3 | 15 | 8 |

This is optional hardware-execution feasibility evidence only. It does not
replace the reproducible state-vector benchmark and does not imply hardware
advantage.

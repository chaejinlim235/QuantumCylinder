# IBM QPU Validation Summary

Optional IBM QPU validation was performed for tiny representative circuits
through IBM Quantum / Qiskit Runtime. This remains appendix feasibility evidence
only; it does not replace the state-vector benchmark.

## Current Status

- submitted: `True`
- primitive: `sampler`
- shots: `1000`
- required qubits: `3`
- backend: `ibm_fez`
- job id: `d91qmquu9n7c73an8teg`
- job status: `DONE`
- runtime status: loaded from environment token
- retrieved counts: `job_result_d91qmquu9n7c73an8teg.json`

## Submitted Circuits

| Circuit | Qubits | Transpiled depth | Two-qubit gates |
| --- | ---: | ---: | ---: |
| `problem1_random_unitary_one_step` | 2 | 11 | 2 |
| `hamiltonian_projection_tiny_proxy` | 3 | 22 | 4 |
| `two_way_postselection_tiny_proxy` | 3 | 39 | 8 |

This is hardware-execution feasibility evidence for the tiny validation path. It does not
replace the reproducible state-vector benchmark and does not imply hardware
advantage.

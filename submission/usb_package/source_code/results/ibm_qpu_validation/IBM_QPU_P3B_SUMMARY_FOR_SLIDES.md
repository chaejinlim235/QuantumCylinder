# IBM QPU Problem 3-b Mini Validation Summary

This is hardware-execution validation for the tiny Problem 3-b mechanism. The main scientific claims remain based on reproducible state-vector benchmarks. No hardware advantage is claimed.

We submitted tiny `M+F` circuits to IBM Quantum / Qiskit Runtime and swept
the complement-qubit measurement basis. The appendix result checks whether
basis changes alter post-selection statistics and the selected data distribution.

## Run 2048x3

- backend: `ibm_fez`
- job_id: `d91r6pmu9n7c73an9qgg`
- status: `DONE`
- shots: `2048`
- circuits: `12`
- dt: `0.2`
- repeats: `3`

| beta | mean p(F=0) | std p(F=0) | mean selected entropy | std selected entropy | repeats |
|---|---:|---:|---:|---:|---:|
| 0.0000pi | 0.881999 | 0.005866 | 1.240095 | 0.060450 | 3 |
| 0.2500pi | 0.899414 | 0.005757 | 1.342133 | 0.018881 | 3 |
| 0.5000pi | 0.660645 | 0.005098 | 1.421011 | 0.043396 | 3 |
| 0.7500pi | 0.358887 | 0.001691 | 1.572905 | 0.063537 | 3 |

## Run 4096x5

- backend: `ibm_fez`
- job_id: `d91r71fccmks73d5nmg0`
- status: `DONE`
- shots: `4096`
- circuits: `20`
- dt: `0.2`
- repeats: `5`

| beta | mean p(F=0) | std p(F=0) | mean selected entropy | std selected entropy | repeats |
|---|---:|---:|---:|---:|---:|
| 0.0000pi | 0.881738 | 0.006647 | 1.375447 | 0.036436 | 5 |
| 0.2500pi | 0.893164 | 0.003301 | 1.492915 | 0.011450 | 5 |
| 0.5000pi | 0.661377 | 0.010302 | 1.581403 | 0.015862 | 5 |
| 0.7500pi | 0.351270 | 0.006018 | 1.736465 | 0.015595 | 5 |

## Interpretation

Changing the complement-qubit measurement basis changes post-selection
statistics and selected data distribution, supporting the Problem 3-b
interpretation that measurement basis controls the effective projected map.
The main quantitative claims remain based on reproducible state-vector
benchmarks.

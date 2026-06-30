# IBM QPU Problem 3-b Basis Sweep Summary

This is a tiny IBM QPU validation of the Problem 3-b measurement-basis trade-off mechanism.

- generated_at_utc: `2026-06-30T12:11:14.709374+00:00`
- backend: `None`
- requested_backend: `ibm_fez`
- shots: `2048`
- repeats: `3`
- num_circuits: `12`
- dt: `0.2`
- trotter_steps: `1`
- submitted: `False`
- job_id: `None`
- job_status: `None`
- runtime_status: qiskit-ibm-runtime unavailable: No module named 'qiskit_ibm_runtime'
- sampler_status: SamplerV2 not checked

Claim guardrail: Hardware-execution validation only. The main scientific claims remain state-vector based. No hardware advantage is claimed.

## Aggregate By Basis

No shot-count aggregate is available yet. In dry-run mode the script saves
transpilation metadata only. Run with `--submit` or `--retrieve-job` to
extract p(F=0) and selected-data entropy.

Interpretation: if the aggregate table is present, changes across beta show
that rotating the complement-qubit measurement basis changes the effective
post-selected map through both success probability and the selected data
distribution. This hardware-execution check does not replace the state-vector
MMD/Wasserstein benchmark.

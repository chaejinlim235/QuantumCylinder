# IBM QPU Problem 3-b Counts Extraction Summary

- generated_at_utc: `2026-06-30T12:41:32.731440+00:00`
- backend: `ibm_fez`
- job_id: `d91r71fccmks73d5nmg0`
- job_status: `DONE`
- counts_source_status: `recomputed_from_saved_counts_without_runtime`
- aggregate_rows: `4`

Claim guardrail: Hardware-execution validation only. Main scientific claims remain state-vector based. No hardware advantage claim.

## Aggregate by measurement basis

| beta | mean p(F=0) | std p(F=0) | mean selected entropy | std selected entropy | repeats |
|---|---:|---:|---:|---:|---:|
| 0.0000pi | 0.881738 | 0.006647 | 1.375447 | 0.036436 | 5 |
| 0.2500pi | 0.893164 | 0.003301 | 1.492915 | 0.011450 | 5 |
| 0.5000pi | 0.661377 | 0.010302 | 1.581403 | 0.015862 | 5 |
| 0.7500pi | 0.351270 | 0.006018 | 1.736465 | 0.015595 | 5 |

Interpretation: changing the complement-qubit measurement basis changes
post-selection statistics and selected data distribution, supporting the
Problem 3-b effective-map interpretation. This does not replace the
state-vector benchmark.

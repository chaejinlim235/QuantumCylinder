# IBM QPU Problem 3-b Counts Extraction Summary

- generated_at_utc: `2026-06-30T12:41:27.646909+00:00`
- backend: `ibm_fez`
- job_id: `d91r6pmu9n7c73an9qgg`
- job_status: `DONE`
- counts_source_status: `recomputed_from_saved_counts_without_runtime`
- aggregate_rows: `4`

Claim guardrail: Hardware-execution validation only. Main scientific claims remain state-vector based. No hardware advantage claim.

## Aggregate by measurement basis

| beta | mean p(F=0) | std p(F=0) | mean selected entropy | std selected entropy | repeats |
|---|---:|---:|---:|---:|---:|
| 0.0000pi | 0.881999 | 0.005866 | 1.240095 | 0.060450 | 3 |
| 0.2500pi | 0.899414 | 0.005757 | 1.342133 | 0.018881 | 3 |
| 0.5000pi | 0.660645 | 0.005098 | 1.421011 | 0.043396 | 3 |
| 0.7500pi | 0.358887 | 0.001691 | 1.572905 | 0.063537 | 3 |

Interpretation: changing the complement-qubit measurement basis changes
post-selection statistics and selected data distribution, supporting the
Problem 3-b effective-map interpretation. This does not replace the
state-vector benchmark.

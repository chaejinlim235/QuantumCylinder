# Optional IBM QPU Validation

This is optional IBM QPU validation, not the main benchmark.

The main scientific claims in the final notebook come from the reproducible
state-vector benchmark and the traceable CSV/figure artifacts under
`solution/`. The IBM Quantum path only checks whether tiny representative
circuits can be prepared, transpiled, and optionally submitted through Qiskit
Runtime.

## Required Packages

- `qiskit`
- `qiskit-ibm-runtime`

The runtime package is only required for IBM backend access or real submission.
The dry-run path can still build and generically transpile tiny circuits without
submitting a job.

## Credentials

Use environment variables or a saved Qiskit Runtime account. Never commit
tokens, API keys, CRNs, account information, or generated logs containing
private account metadata.

```powershell
$env:QISKIT_IBM_TOKEN = "<your-token>"
$env:QISKIT_IBM_INSTANCE = "<optional-instance>"
$env:QISKIT_IBM_CHANNEL = "ibm_cloud"
```

`IBM_QUANTUM_TOKEN` is also accepted. Set `QISKIT_IBM_CHANNEL` to the runtime
channel that matches the available saved account or token path.

## Commands

```powershell
python scripts/ibm_qpu_smoke_test.py --dry-run
python scripts/ibm_qpu_smoke_test.py --dry-run --backend BACKEND_NAME
python scripts/ibm_qpu_smoke_test.py --submit --backend BACKEND_NAME --shots 1000 --max-circuits 3
```

## Problem 3-b IBM QPU Basis Sweep

This appendix script prepares a tiny `M+F` circuit for Problem 3-b. It sweeps
the complement-qubit measurement basis and, when QPU counts are available,
reports post-selection success probability `p(F=0)` and selected data entropy.
This validates the mechanism that measurement basis changes the effective
post-selected map; it does not replace the state-vector benchmark.

Dry-run:

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py --backend ibm_fez --shots 2048 --repeats 3 --dt 0.20 --trotter-steps 1 --save-dir results/ibm_qpu_validation/p3b_fez_2048x3_dryrun
```

Submit:

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py --submit --backend ibm_fez --shots 2048 --repeats 3 --dt 0.20 --trotter-steps 1 --wait-minutes 5 --save-dir results/ibm_qpu_validation/p3b_fez_2048x3
```

Higher precision submit:

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py --submit --backend ibm_fez --shots 4096 --repeats 5 --dt 0.20 --trotter-steps 1 --wait-minutes 10 --save-dir results/ibm_qpu_validation/p3b_fez_4096x5
```

Retrieve:

```powershell
python scripts/ibm_qpu_extract_p3b_counts.py --job-id JOB_ID --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_2048x3/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_retrieved_JOB_ID
```

Completed jobs included in this USB package:

- `ibm_fez`, job `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE.
- `ibm_fez`, job `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

Retrieve the included jobs again in `.venv_ibm` or any environment with
`qiskit-ibm-runtime` installed:

```powershell
python scripts/ibm_qpu_extract_p3b_counts.py --job-id d91r6pmu9n7c73an9qgg --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_2048x3/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_fez_2048x3
python scripts/ibm_qpu_extract_p3b_counts.py --job-id d91r71fccmks73d5nmg0 --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_4096x5/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_fez_4096x5
```

Regenerate the slide-ready summary:

```powershell
python scripts/summarize_ibm_qpu_p3b_results.py
```

## Safety And Claim Guardrails

- Do not commit tokens.
- Do not rely on QPU queue availability for final grading.
- If a QPU job is pending, submit the job id and dry-run resource summary.
- This is hardware-execution validation only.
- It does not replace the reproducible state-vector results.
- It does not prove hardware advantage.

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

## Safety And Claim Guardrails

- Do not commit tokens.
- Do not rely on QPU queue availability for final grading.
- If a QPU job is pending, submit the job id and dry-run resource summary.
- This is hardware-execution validation only.
- It does not replace the reproducible state-vector results.
- It does not prove hardware advantage.

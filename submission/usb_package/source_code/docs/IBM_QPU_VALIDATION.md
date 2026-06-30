# IBM QPU Validation

This document describes the optional IBM Quantum / IBM QPU validation path for
the QuantumCylinder submission.

## What This Validation Is

The validation prepares tiny representative circuits from the benchmark story
and, if explicitly requested, submits them through IBM Quantum via Qiskit
Runtime.

It reports:

- backend name;
- number of qubits required;
- transpiled depth;
- two-qubit gate count;
- shots;
- primitive used;
- job id and status if a real job is submitted.

## What This Validation Is Not

This is not the main benchmark. It does not replace the state-vector
MMD/Wasserstein results in `solution/solution_1.ipynb`, and it does not prove or
claim hardware advantage.

The IBM QPU path is appendix evidence only: it checks small-circuit execution
feasibility for Q&A or source-code inspection.

## Credential Setup

Use environment variables or a saved Qiskit Runtime account. Do not hardcode
tokens in code, notebooks, Markdown, shell history, or committed files.

```powershell
$env:QISKIT_IBM_TOKEN = "<your-token>"
$env:QISKIT_IBM_INSTANCE = "<optional-instance>"
$env:QISKIT_IBM_CHANNEL = "ibm_cloud"
```

`IBM_QUANTUM_TOKEN` is also accepted as a token environment variable. The
script reads `QISKIT_IBM_CHANNEL` when set; use the channel that matches the
saved account or token path available in the local environment.

## Dry-Run

The default path is no-submit dry-run:

```powershell
python scripts/ibm_qpu_smoke_test.py --dry-run
```

You may request a backend name for metadata/transpilation if credentials are
available:

```powershell
python scripts/ibm_qpu_smoke_test.py --dry-run --backend BACKEND_NAME
```

Dry-run output is saved under:

```text
results/ibm_qpu_validation/
```

## Submit To IBM QPU

Only submit a real job when credentials are available and explicit approval has
been given:

```powershell
python scripts/ibm_qpu_smoke_test.py --submit --backend BACKEND_NAME --shots 1000 --max-circuits 3
```

If `--backend` is omitted and credentials are available, the script tries to
choose a least-busy operational non-simulator backend.

## Problem 3-b Measurement-Basis Mini Validation

The final package also includes a Problem 3-b-specific IBM QPU appendix check.
It submits tiny `M+F` circuits and sweeps the complement-qubit measurement
basis. Completed runs:

- `ibm_fez`, job `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE.
- `ibm_fez`, job `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

Counts extraction and slide summary generation use standard-library CSV/JSON
processing:

```powershell
python scripts/ibm_qpu_extract_p3b_counts.py --job-id d91r6pmu9n7c73an9qgg --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_2048x3/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_fez_2048x3
python scripts/ibm_qpu_extract_p3b_counts.py --job-id d91r71fccmks73d5nmg0 --backend ibm_fez --source-report results/ibm_qpu_validation/p3b_fez_4096x5/problem3b_ibm_basis_sweep_report.json --save-dir results/ibm_qpu_validation/p3b_fez_4096x5
python scripts/summarize_ibm_qpu_p3b_results.py
```

This is hardware-execution validation only. The main scientific claims remain
based on reproducible state-vector experiments.

## Retrieve Results By Job Id

After submission, the saved report includes the job id if the runtime call
succeeds. Retrieve it with Qiskit Runtime in a separate local session:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(channel="ibm_quantum")
job = service.job("<job-id>")
print(job.status())
print(job.result())
```

If the submitted job used a different runtime channel, instantiate the service
with the same channel value, for example `channel="ibm_cloud"`.

Do not commit retrieved account metadata or credentials.

## How To Interpret Results

Use the report as a small hardware-execution feasibility check:

- Did the representative circuits transpile for the requested backend?
- What depth and two-qubit gate count resulted?
- Was a job submitted, and what is its queue/status?
- If completed, are counts or expectation values available?

Do not use this path to replace ensemble-scale MMD/Wasserstein claims. Queue
availability, calibration, and noise make it inappropriate as the main
scientific result for the current submission package.

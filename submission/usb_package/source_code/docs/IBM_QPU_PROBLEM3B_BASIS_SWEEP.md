# IBM QPU Problem 3-b Basis Sweep

This script prepares a tiny IBM Quantum / IBM QPU validation for the Problem
3-b measurement-basis trade-off mechanism:

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py
```

## What It Does

- Builds a 3-qubit `M+F` circuit where `q0,q1` are the data system `M` and
  `q2` is the complement qubit `F`.
- Prepares small `S0`-like rotations near `|00>` on `M`.
- Applies a shallow Hamiltonian-inspired RX/RY/RXX block with
  `hx = 0.8090`, `hy = 0.9045`, and `J = 1.0`.
- Sweeps the complement-qubit measurement basis using
  `beta in {0, pi/4, pi/2, 3pi/4}`.
- Measures all qubits and, when shot counts are available, reports
  `p(F=0)` and selected data entropy among shots with `F=0`.

Qiskit bitstrings are interpreted as `c2 c1 c0`, so `F=q2` is the leftmost
bit and the selected data bits are `c1 c0`.

## Why It Maps To Problem 3-b

Problem 3-b asks for a controlled modification of the diffusion setting and an
analysis of what improves or is sacrificed. Rotating the measurement basis of
the complement qubit changes the effective post-selected non-unitary map on the
data system. The hardware-execution check therefore tests the mechanism behind the
recoverability-success-diversity trade-off: different bases can change both
post-selection success probability and the selected data distribution.

## What It Does Not Claim

This is hardware-execution validation for a tiny Problem 3-b mechanism check.
The main scientific claims remain based on state-vector MMD/Wasserstein
experiments.

- It does not claim quantum advantage.
- It does not claim hardware advantage.
- It does not claim a full trainable QuDDPM.
- It does not claim IBM QPU results prove superiority.
- It does not replace the state-vector benchmark.

## Credential Setup

Use environment variables. Never hardcode, print, or commit IBM tokens, API
keys, instance CRNs, account metadata, or private logs.

```powershell
$env:QISKIT_IBM_TOKEN = "<your-token>"
$env:QISKIT_IBM_INSTANCE = "<your-instance-crn>"
$env:QISKIT_IBM_CHANNEL = "ibm_cloud"
```

`IBM_QUANTUM_TOKEN` is also accepted as the token variable.

## Dry-Run Command

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py `
  --backend ibm_fez `
  --shots 2048 `
  --repeats 3 `
  --dt 0.20 `
  --trotter-steps 1 `
  --save-dir results/ibm_qpu_validation/p3b_fez_2048x3_dryrun
```

Without `--submit`, no real QPU job is submitted. If credentials are missing,
the script saves a local dry-run report and explains what is missing.

## Submit Command

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py `
  --submit `
  --backend ibm_fez `
  --shots 2048 `
  --repeats 3 `
  --dt 0.20 `
  --trotter-steps 1 `
  --wait-minutes 5 `
  --save-dir results/ibm_qpu_validation/p3b_fez_2048x3
```

Higher precision option:

```powershell
python scripts/ibm_qpu_problem3b_basis_sweep.py `
  --submit `
  --backend ibm_fez `
  --shots 4096 `
  --repeats 5 `
  --dt 0.20 `
  --trotter-steps 1 `
  --wait-minutes 10 `
  --save-dir results/ibm_qpu_validation/p3b_fez_4096x5
```

## Retrieve Command

```powershell
python scripts/ibm_qpu_extract_p3b_counts.py `
  --job-id JOB_ID `
  --backend ibm_fez `
  --source-report results/ibm_qpu_validation/p3b_fez_2048x3/problem3b_ibm_basis_sweep_report.json `
  --save-dir results/ibm_qpu_validation/p3b_retrieved_JOB_ID
```

Retrieval loads the job by id, saves the current status, and analyzes counts if
the job is done.

Completed runs in the final package:

- `ibm_fez`, job `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE.
- `ibm_fez`, job `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

The slide-ready aggregate is written to:

- `results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.md`
- `results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.csv`

## How To Interpret `p(F=0)`

For each circuit, `p(F=0)` is the fraction of measured shots whose leftmost
bit is `0`. Those are the post-selected shots. The selected data distribution
is computed from the remaining two bits `c1 c0`, and its Shannon entropy is a
small diversity proxy. A change across beta values means the complement-qubit
measurement basis changes the post-selected map.

## Output Files

The script writes to `--save-dir`:

- `problem3b_ibm_basis_sweep_report.json`
- `problem3b_ibm_basis_sweep_summary.md`
- `problem3b_ibm_basis_sweep_aggregate.csv`
- `problem3b_ibm_basis_sweep_circuits.csv`
- `problem3b_ibm_basis_sweep_counts.json` if counts are retrieved

## Copy Results Into USB Package

After a dry-run, submission, or retrieval, run:

```powershell
python scripts/copy_ibm_qpu_results_to_usb.py
```

This copies `results/ibm_qpu_validation/`, the QPU scripts, and this document
into `submission/usb_package/source_code/` without copying `.git`, `.env`, token
files, or private key files.

## Regenerate The Slide Summary

```powershell
python scripts/summarize_ibm_qpu_p3b_results.py
```

This uses only Python standard-library CSV/JSON processing and does not require
pandas.

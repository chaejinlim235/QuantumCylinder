# Submission Layer

This folder is a compact, readable execution layer for Problems 1, 2, and 3
inside the USB source-code package.

## Files

| File | Purpose |
| --- | --- |
| `states_and_metrics.py` | Shared state preparation, fidelity, MMD, and Wasserstein-type utilities. |
| `problem1_random_unitary_scrambling.py` | Problem 1 random-unitary scrambling flow. |
| `problem2_hamiltonian_projection.py` | Problem 2 Hamiltonian projected-diffusion flow and resource proxy comparison. |
| `problem3_continuous_measurement_denoising.py` | Problem 3 measurement-induced denoising and basis trade-off flow. |
| `run_all.py` | Runs the compact Problem 1/2/3 reproduction path. |

## Quick Check

Run from `submission/usb_package/source_code/`:

```powershell
python submission/run_all.py --quick
```

For a fuller run:

```powershell
python submission/run_all.py
```

Outputs are written under `results/submission_simple/`.

## Scope

This layer is designed for fast inspection. The full implementation is under
`src/quantum_cylinder/`, and the polished final answer is under
`solution/solution_1.ipynb`.

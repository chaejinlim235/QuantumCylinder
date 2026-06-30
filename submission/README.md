# Submission Layer

This folder is a compact, readable execution layer for Problems 1, 2, and 3.
It is useful for quick local checks, while the polished USB package lives under
`submission/usb_package/`.

## Files

| File | Purpose |
| --- | --- |
| `states_and_metrics.py` | Shared state preparation, fidelity, MMD, and Wasserstein-type utilities. |
| `problem1_random_unitary_scrambling.py` | Problem 1 random-unitary scrambling flow. |
| `problem2_hamiltonian_projection.py` | Problem 2 Hamiltonian projected-diffusion flow and resource proxy comparison. |
| `problem3_continuous_measurement_denoising.py` | Problem 3 measurement-induced denoising and basis trade-off flow. |
| `run_all.py` | Runs the compact Problem 1/2/3 reproduction path. |

## Quick Check

Run from the repository root:

```powershell
python submission/run_all.py --quick
```

For a fuller run:

```powershell
python submission/run_all.py
```

Outputs are written under `results/submission_simple/`.

## Relationship To The Final Package

- `solution/solution_1.ipynb` is the compact final repository answer.
- `submission/usb_package/` is the USB-ready package.
- `submission/usb_package/source_code/` contains the full inspectable source
  code package, including `src/`, `scripts/`, `tests/`, `configs/`,
  `submission/`, and a copy of the final `solution/`.

This folder is intentionally simpler than the full development tree. It keeps
the problem flow easy to run without making claims beyond the final notebook.

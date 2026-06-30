# Quantum Cylinder USB Package

This USB package is organized for judge review. The main submission should be read from the three notebooks first, and the code folder is kept as a compact executable reference.

## Review Order

1. `solution/Problem 1.ipynb`
   - Random-unitary scrambling baseline and metric comparison.
2. `solution/Problem 2.ipynb`
   - Hamiltonian projection baseline and parameter scan.
3. `solution/Problem 3.ipynb`
   - Problem 3(b): recoverability-success-diversity trade-off.
   - Problem 3(c): two-way post-selection improvement derived from the 3(b) analysis.
4. `solution/IBM_QPU_Implementation.ipynb`
   - Appendix-only IBM QPU implementation notebook. The IBM circuit-building and dry-run validation code is included directly in the notebook.
   - Includes three representative QPU proxy circuits: `problem1_random_unitary_one_step`, `hamiltonian_projection_tiny_proxy`, and `two_way_postselection_tiny_proxy`.

## Minimal Code Map

The judge-facing implementation is in `code/`.

- `code/submission/problem1_random_unitary_scrambling.py`
  - Core Problem 1 implementation.
- `code/submission/problem2_hamiltonian_projection.py`
  - Core Problem 2 implementation.
- `code/submission/problem3_continuous_measurement_denoising.py`
  - Core Problem 3 implementation, including baseline collapse, axis-only comparison, and continuous post-selection search.
- `code/submission/states_and_metrics.py`
  - Shared state generation, distances, MMD, and file-writing helpers.
- `code/submission/run_all.py`
  - Quick executable entry point for Problems 1, 2, and 3.
- `code/ibm_qpu/`
  - Optional source-code copies of the IBM QPU validation path. The judge-facing notebook above is self-contained.

## Quick Run

From `submission/usb_package/code`, run:

```bash
python -m submission.run_all --quick
```

This creates a small smoke-test result under `code/results/submission_simple/`. The full notebook outputs remain the primary submitted results.

## Claim Boundary

The main story is:

```text
Problem 1/2 baseline comparison
-> Problem 3(b) recoverability-success-diversity trade-off
-> Problem 3(c) two-way post-selection improvement
```

IBM QPU material is appendix validation only. It validates a tiny Problem 3(b) measurement-basis mechanism and should not be read as a hardware advantage or general quantum advantage claim.

The IBM notebook also includes representative tiny QPU proxy circuits for the Problem 1, Problem 2, and Problem 3(c) stories. These are included as implementation/smoke-test examples, while the actual hardware-validation claim remains limited to Problem 3(b).

## Supporting Materials

Large supporting materials are intentionally separated from this main USB package:

- `../usb_package_supporting_materials/presentation/`
  - Presentation PDF and presentation-side material.
- `../usb_package_supporting_materials/archive/`
  - Supporting reports, previous full source tree, and audit material.

These files are preserved for traceability but are not required for the main review path.

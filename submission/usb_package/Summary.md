# QuantumCylinder USB Package Summary

## Main Review Path

```text
usb_package/
  Summary.md
  solution/
    Problem 1.ipynb
    Problem 2.ipynb
    Problem 3.ipynb
  presentation/
    QuantumCylinder_presentation.pdf
  source_code/
    README_FOR_JUDGES.md
    REPRODUCIBILITY_COMMANDS.md
    src/
    scripts/
    tests/
    configs/
    submission/
```

In this repository the folder is stored as `submission/usb_package/`. When copied
to a USB drive, the `submission/` prefix can be omitted and the folder can be
used directly as `usb_package/`.

## How to Review

Open the notebooks in this order:

1. `solution/Problem 1.ipynb`
2. `solution/Problem 2.ipynb`
3. `solution/Problem 3.ipynb`

The notebooks were split from
`QuantumCylinder_final_submission_report_problem3c_variants_v5.ipynb` and keep
the original report outputs, plots, tables, and explanatory text. They are meant
to be readable immediately after opening, even before rerunning.

The package is notebook-first for a 5-minute review. The `presentation/` and
`source_code/` folders are included as supporting material for the official
presentation and source-code inspection requirements.

## How to Rerun

Use Jupyter or VS Code and run all cells in each notebook. Each notebook includes
its own setup cells so it can be rerun independently. The first setup cell keeps
the original dependency installation line:

```python
!pip install -q qiskit qiskit-aer scipy numpy matplotlib seaborn
```

If the environment already has these packages, the cell can simply be run as-is.

## Problem Mapping

- `Problem 1.ipynb`
  - Builds the two-qubit target ensemble around `|00>`.
  - Defines fidelity, fidelity-kernel MMD, and Wasserstein-type infidelity cost.
  - Runs random-unitary forward diffusion and displays the distance trajectory.
- `Problem 2.ipynb`
  - Rebuilds the shared Problem 1 setup needed for comparison.
  - Constructs the fixed three-qubit Hamiltonian with one complement qubit.
  - Generates Hamiltonian projected diffusion outputs.
  - Displays Bloch/metric comparison figures and resource/control proxy values.
- `Problem 3.ipynb`
  - Rebuilds the shared setup needed for standalone execution.
  - Implements Problem 3(a) measurement-induced denoising.
  - Implements Problem 3(b) controlled Hamiltonian/basis/noise trade-off analysis.
  - Preserves the Problem 3(c) candidate portfolio:
    no-denoising input, axis-only projection, continuous post-selection,
    Hamiltonian plus random final kick, Hamiltonian two-way post-selection,
    hybrid 1 data qubit plus 1 auxiliary qubit toy, and target-aware
    actor-critic filter search.

## Defaults

- Ensemble size: `N = 80` in the original report notebook
- Target cluster width: `sigma = 0.10`
- Random seeds: fixed inside the notebooks for reproducibility
- Hamiltonian parameters: `hx = 0.8090`, `hy = 0.9045`, `J = 1.0`
- Problem 3(c) actor-critic benchmark: 10 seeds x 3 input steps in the preserved output

## Scope

This package is notebook-first because the submitted evidence depends on plots,
tables, and explanatory report text. Problem 3(c) is a portfolio comparison, not
a single universal denoising claim. Distance improvements must be read together
with post-selection success probability and ensemble diversity retention. The
target-aware actor-critic row uses the raw target ensemble in its reward, so it
is reported as a target-aware policy-search candidate rather than a general
unknown-target denoiser.

Optional IBM QPU validation is included only as appendix feasibility evidence
under `source_code/results/ibm_qpu_validation/`. It does not replace the
state-vector benchmark and does not imply hardware advantage.

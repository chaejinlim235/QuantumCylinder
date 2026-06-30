# QuantumCylinder USB Submission Package

Open order for judges:

1. `source_code/solution/solution_1.ipynb`
2. `source_code/solution/README.md`
3. `presentation/QuantumCylinder_presentation.pdf`
4. `source_code/README_FOR_JUDGES.md`

## What This Package Contains

- `source_code/`: runnable source code, tests, configs, selected compact result evidence, final notebook, figures, and tables.
- `QuantumCylinder_full_source.zip`: zipped copy of the readable `source_code/` package.
- `presentation/`: English presentation PDF, storyboard, slide text, and slide checklist.
- `JUDGING_CRITERIA_ALIGNMENT.md`: official judging-criteria mapping.
- `LIMITATIONS_AND_APPROPRIATENESS.md`: claim boundaries and scope guardrails.
- `source_code/IBM_QPU_README.md`: optional IBM QPU validation instructions.
- `CSV_VALIDATION_REPORT.md`, `LATEX_VALIDATION_REPORT.md`, and
  `HARDWARE_TERMINOLOGY_AUDIT.md`: latest package validation notes.
- `ONSITE_CHECKLIST.md`: final onsite submission and presentation checklist.

## Core Thesis

QuantumCylinder compares random-unitary diffusion and Hamiltonian projected diffusion under shared fidelity-based MMD/Wasserstein-type metrics, then studies measurement-induced projected denoising as a recoverability-success-diversity trade-off. Based on that 3-b trade-off analysis, Problem 3(c) tests two-way Hamiltonian post-selection as a stronger but more costly projected denoising improvement.

## Minimal Reproduction

Run from `source_code/`:

```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/summarize_problem_3_seed_sweep.py
python scripts/summarize_problem_3_method_portfolio.py
python scripts/ibm_qpu_smoke_test.py --dry-run
```

## Optional IBM QPU Validation

The package includes an optional IBM Quantum / IBM QPU validation path through
Qiskit Runtime. It is appendix evidence for tiny representative circuits, not
the main source of the MMD/Wasserstein claims.

## Scope

This is a small 2-qubit/3-qubit state-vector benchmark. It does not claim quantum advantage, hardware advantage, a full trainable QuDDPM, or that continuous bases always beat axis-only bases.

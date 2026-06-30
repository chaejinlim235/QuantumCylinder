# QuantumCylinder USB Package Summary

This folder is the USB-ready submission package. It is designed so a judge can
find the final answer, presentation material, source code, and reproduction
commands without reading the development repository.

## Five-Minute Review Path

1. Open this file.
2. Open the split report notebooks under `solution/`:
   - `solution/Problem 1.ipynb`
   - `solution/Problem 2.ipynb`
   - `solution/Problem 3.ipynb`
3. Open `presentation/PRESENTATION_SLIDE_TEXT_EN.md` or the presentation file
   if a rendered slide deck is requested.
4. For source-code inspection, open `source_code/README_FOR_JUDGES.md`.

The source-code package also contains the compact canonical final notebook at
`source_code/solution/solution_1.ipynb`. The split notebooks and compact
notebook tell the same story at different reading granularity.

## Folder Map

```text
usb_package/
  Summary.md
  README_SUBMISSION.md
  JUDGING_CRITERIA_ALIGNMENT.md
  solution/
    Problem 1.ipynb
    Problem 2.ipynb
    Problem 3.ipynb
  presentation/
    PRESENTATION_SLIDE_TEXT_EN.md
    PRESENTATION_STORYBOARD_EN.md
    SLIDE_CHECKLIST.md
  source_code/
    README_FOR_JUDGES.md
    CODE_MANIFEST.md
    PROBLEM_REQUIREMENT_MAP.md
    REPRODUCIBILITY_COMMANDS.md
    IBM_QPU_README.md
    src/
    scripts/
    tests/
    configs/
    submission/
    solution/
```

In the repository, this folder is stored as `submission/usb_package/`. On a USB
drive it can be copied and used directly as `usb_package/`.

## Problem Mapping

- Problem 1 builds a target ensemble near `|00>`, defines fidelity/MMD/
  Wasserstein-type metrics, and studies random-unitary scrambling. The
  interpretation is strong scrambling toward a Haar-like distance plateau, not
  slow DDPM-like diffusion.
- Problem 2 constructs a fixed three-qubit Hamiltonian with one complement
  qubit, performs projected diffusion, and compares it qualitatively with the
  random-unitary setting. The resource/control discussion compares random
  gate-level control against fixed-Hamiltonian time and projection-basis
  control.
- Problem 3 uses measurement-induced post-selection as a denoising proxy.
  Problem 3(b) analyzes measurement basis as a trade-off among distance
  improvement, success probability, and diversity retention. Problem 3(c)
  follows from that analysis by testing two-way Hamiltonian post-selection
  against one-way and axis-only baselines.

## Scope Of Claims

The main claims are state-vector benchmark claims supported by notebook
outputs, figures, tables, and source-code reproduction commands. The package
does not claim quantum advantage, hardware advantage, a full trainable QuDDPM,
or that one diffusion method is always better than the other.

The continuous-basis result is presented as a small-margin controlled
modification, not as an overwhelming or universal win over axis-only
projection. Actor-critic rows, if discussed, are target-aware appendix evidence
and not a general unknown-target denoiser.

## Optional IBM QPU Appendix

Optional IBM QPU validation is included only as appendix feasibility evidence
under `source_code/results/ibm_qpu_validation/`. It does not replace the
state-vector benchmark and does not imply hardware advantage.

Included Problem 3-b IBM QPU mini-validation jobs:

- `ibm_fez`, job `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE.
- `ibm_fez`, job `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

Slide-ready IBM appendix summary:

- `source_code/results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.md`
- `source_code/results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.csv`

## Reproduction

For source-code reproduction, run commands from `source_code/`:

```powershell
python -m pytest
python submission/run_all.py --quick
```

More detailed commands are listed in
`source_code/REPRODUCIBILITY_COMMANDS.md`.

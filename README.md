# QuantumCylinder

This repository contains the QuantumCylinder final submission package for the
2026 Quantum Information contest.

The project studies small-scale quantum diffusion and projected denoising:

- Problem 1: random-unitary scrambling of a two-qubit target ensemble.
- Problem 2: fixed Hamiltonian evolution with complement-qubit projection.
- Problem 3: measurement-induced denoising, analyzed through distance gain,
  post-selection success probability, and ensemble diversity retention.

## Read This First

For a fast review, use these entry points:

| Purpose | File or folder |
| --- | --- |
| Final repository answer | `solution/solution_1.ipynb` |
| Final repository guide | `solution/README.md` |
| USB package overview | `submission/usb_package/Summary.md` |
| USB submission guide | `submission/usb_package/README_SUBMISSION.md` |
| Source-code inspection guide | `submission/usb_package/source_code/README_FOR_JUDGES.md` |
| Requirement mapping | `submission/usb_package/source_code/PROBLEM_REQUIREMENT_MAP.md` |
| Reproducibility commands | `submission/usb_package/source_code/REPRODUCIBILITY_COMMANDS.md` |
| Optional IBM QPU appendix | `docs/IBM_QPU_VALIDATION.md` |

The root `solution/` folder is the compact final solution. The USB package also
contains split presentation notebooks under `submission/usb_package/solution/`
for quick onsite reading.

## Final Submission Structure

```text
solution/
  README.md
  solution_1.ipynb
  figures/
  tables/

submission/usb_package/
  Summary.md
  README_SUBMISSION.md
  solution/
    Problem 1.ipynb
    Problem 2.ipynb
    Problem 3.ipynb
  presentation/
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

## One-Sentence Thesis

Complement-qubit measurement basis can be used as a control knob for an
effective post-selected non-unitary map, giving a measurable
recoverability-success-diversity trade-off that motivates the two-way
post-selection proposal in Problem 3(c).

## What To Check

| Contest criterion | Where it is addressed |
| --- | --- |
| Completeness and appropriateness | `solution/solution_1.ipynb`, `submission/usb_package/JUDGING_CRITERIA_ALIGNMENT.md` |
| Fidelity to problem requirements | `submission/usb_package/source_code/PROBLEM_REQUIREMENT_MAP.md` |
| Novelty of plan and approach | Problem 3(b)/(c) in `solution/solution_1.ipynb` |
| Presentation and communication | `submission/usb_package/presentation/` and `submission/usb_package/Summary.md` |
| Source-code inspection readiness | `submission/usb_package/source_code/README_FOR_JUDGES.md` |
| IBM QPU validation clarity | `docs/IBM_QPU_VALIDATION.md`, `submission/usb_package/source_code/IBM_QPU_README.md` |

## Quick Reproduce

From the repository root:

```powershell
python -m pytest
python submission/run_all.py --quick
```

From the USB source-code package:

```powershell
cd submission/usb_package/source_code
python -m pytest
python submission/run_all.py --quick
```

The deeper reproduction path is documented in
`submission/usb_package/source_code/REPRODUCIBILITY_COMMANDS.md`.

## Key Guardrails

The submission does not claim:

- quantum advantage;
- hardware advantage;
- a full trainable QuDDPM;
- that continuous basis always or strongly beats axis-only projection;
- that actor-critic is a general unknown-target denoiser;
- that Hamiltonian projected diffusion is always better than random-unitary
  diffusion;
- that IBM QPU results prove superiority.

IBM QPU results are appendix-only hardware-execution validation. The main
scientific claims remain based on reproducible state-vector benchmarks and
traceable CSV/figure artifacts.

## IBM QPU Appendix

The package includes a completed Problem 3-b IBM QPU basis-sweep mini
validation on `ibm_fez`:

- job `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE;
- job `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

Read:

- `docs/IBM_QPU_VALIDATION.md`
- `docs/IBM_QPU_PROBLEM3B_BASIS_SWEEP.md`
- `results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.md`

These files contain no tokens or private IBM account credentials.

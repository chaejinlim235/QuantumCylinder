# Latest IBM QPU Patch Audit

## Summary

Status: package is submission-ready for the current state-vector benchmark, with
an optional IBM QPU dry-run validation path added as appendix evidence.

No real IBM QPU job was submitted in this patch.

## Required Audit Questions

| Check | Result |
| --- | --- |
| 1. Does `solution/solution_1.ipynb` exist? | Yes. Root and USB copies both exist. |
| 2. Does `solution/README.md` use proper Markdown line breaks? | Yes. Long final-facing lines were split while preserving content. |
| 3. Are all CSV files under `solution/tables/` valid multi-line CSV files? | Yes. pandas validation passed; see `CSV_VALIDATION_REPORT.md`. |
| 4. Are broken bra-ket / LaTeX expressions still present in notebook or slide text? | No broken notebook equations remain. Slide plain-text bras are inside a fenced `text` block; see `LATEX_VALIDATION_REPORT.md`. |
| 5. Are local absolute paths such as user-home paths still present? | No matches in searched text files under README/docs/solution/submission after patching. |
| 6. Does the USB package include source code, not only figures/tables? | Yes. `source_code/` includes runnable implementation, tests, configs, scripts, solution artifacts, and selected compact evidence. |
| 7. Does `source_code` include `src/`, `scripts/`, `tests/`, `configs/`, `submission/run_all.py`, and requirements/config files? | Yes. It includes `src/`, `scripts/`, `tests/`, `configs/`, `submission/run_all.py`, `requirements.txt`, and `pyproject.toml`. |
| 8. Does the package include an English PDF/PPT presentation? | Yes. `presentation/QuantumCylinder_presentation.pdf` exists, with English slide text and storyboard. |
| 9. Are there forbidden claims? | No positive forbidden claims found. The phrases appear only as explicit limitations/guardrails. |
| 10. Are there references to non-IBM QPU terminology? | No such terminology remains in searched text files; see `HARDWARE_TERMINOLOGY_AUDIT.md`. |
| 11. Is there an IBM QPU validation path? | Yes. `scripts/ibm_qpu_smoke_test.py`, `docs/IBM_QPU_VALIDATION.md`, and `source_code/IBM_QPU_README.md` were added. |
| 12. What are the top blocking issues before USB submission? | No blocking package issue found. Non-blocking: real IBM QPU execution was not submitted because credentials/runtime availability and explicit approval were not provided. |

## Commands Run

| Command | Status | Notes |
| --- | --- | --- |
| `python -m pytest` | tests passed, process exited 1 | All 37 tests passed; Windows temp symlink cleanup raised `PermissionError` after test completion. |
| `python -m pytest --basetemp .pytest_tmp_local` | pass | 37 passed. |
| `python submission/run_all.py --quick` | pass | Printed Problem 1/2/3 compact reproduction summary. |
| `python scripts/summarize_problem_3_seed_sweep.py` | pass | Confirmed 20 / 20 seeds and 3-b trade-off wording. |
| `python scripts/summarize_problem_3_method_portfolio.py` | pass | Confirmed two-way post-selection as 3-c main candidate. |
| `python scripts/ibm_qpu_smoke_test.py --dry-run` | pass | No submit; runtime package unavailable locally, generic transpilation summary saved. |
| `python -m pytest --basetemp .pytest_tmp_local_usb` from `source_code/` | pass | 37 passed inside USB source package. |
| `python submission/run_all.py --quick` from `source_code/` | pass | Source-code package quick reproduction ran successfully. |

## Files Created

- `docs/IBM_QPU_VALIDATION.md`
- `scripts/ibm_qpu_smoke_test.py`
- `submission/usb_package/AUDIT_LATEST_IBM_QPU_PATCH.md`
- `submission/usb_package/CSV_VALIDATION_REPORT.md`
- `submission/usb_package/LATEX_VALIDATION_REPORT.md`
- `submission/usb_package/HARDWARE_TERMINOLOGY_AUDIT.md`
- `submission/usb_package/source_code/IBM_QPU_README.md`
- `submission/usb_package/source_code/scripts/ibm_qpu_smoke_test.py`
- `submission/usb_package/source_code/results/ibm_qpu_validation/`

## Remaining Non-Blocking Notes

- `qiskit-ibm-runtime` is not installed in the current local environment, so the
  dry-run used generic Qiskit transpilation and did not select a real IBM
  backend.
- Real IBM QPU execution requires credentials, queue availability, and an
  explicit `--submit` run.
- The main scientific claims remain the reproducible state-vector
  MMD/Wasserstein results.

# IBM QPU Results Update Audit

## Scope

This audit covers the Problem 3-b IBM QPU measurement-basis mini validation
update. IBM QPU evidence is hardware-execution validation for a tiny Problem 3-b mechanism check. The main scientific claims remain
state-vector based.

## Checklist

| Question | Status | Evidence |
| --- | --- | --- |
| Do both IBM QPU job result directories exist? | Yes | `results/ibm_qpu_validation/p3b_fez_2048x3/`, `results/ibm_qpu_validation/p3b_fez_4096x5/` |
| Do they contain report JSON files? | Yes | Each run has `problem3b_ibm_basis_sweep_report.json` and `problem3b_ibm_counts_extract_report.json`. |
| Do they contain aggregate CSV files? | Yes | Each run has `problem3b_ibm_basis_sweep_aggregate.csv`. |
| Are aggregate CSV files non-empty? | Yes | Each aggregate CSV has 4 beta rows. |
| Is pandas used anywhere in the IBM result extraction/update path? | No | `rg "import pandas|pd\\."` found no matches in the IBM scripts. |
| Are token/API key/CRN absent from files? | Yes | Only environment variable names and placeholders are present. No actual secret-like values were found. |
| Are IBM QPU results included in source_code package? | Yes | Copied under `submission/usb_package/source_code/results/ibm_qpu_validation/`. |
| Is presentation appendix A9 updated? | Yes | `presentation/PRESENTATION_SLIDE_TEXT_EN.md` now lists completed job ids and aggregate values. |
| Is the final notebook or solution README updated? | Yes | `solution/solution_1.ipynb` and `solution/README.md` include IBM QPU Problem 3-b hardware-execution validation. |
| What remains blocking? | None for packaging | Current default Python lacks `qiskit_ibm_runtime`, so live re-retrieval should be run in `.venv_ibm`; existing DONE-job counts and aggregates are already included. |

## Completed Jobs

- `ibm_fez`, job `d91r6pmu9n7c73an9qgg`, `2048` shots, `12` circuits, DONE.
- `ibm_fez`, job `d91r71fccmks73d5nmg0`, `4096` shots, `20` circuits, DONE.

## Key Output Paths

- `results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.md`
- `results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.csv`
- `submission/usb_package/source_code/results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.md`
- `submission/usb_package/source_code/results/ibm_qpu_validation/IBM_QPU_P3B_SUMMARY_FOR_SLIDES.csv`

## Guardrail

This is hardware-execution validation only. The main scientific claims remain
based on reproducible state-vector experiments. No hardware advantage is
claimed.

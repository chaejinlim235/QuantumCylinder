# Day 2 19H IBM QPU Patch Audit

Status: submission-ready after the Day 2 IBM QPU appendix patch.

No real IBM QPU job was submitted in this patch.

| Check | Result |
| --- | --- |
| Does `solution/solution_1.ipynb` exist? | Yes. Root and USB copies exist. |
| Does `solution/README.md` use proper Markdown formatting? | Yes. It begins with `Open \`solution_1.ipynb\` first.` and uses separated headings/lists. |
| Are CSV files under `solution/tables/` valid multi-line CSV files? | Yes. pandas validation passed; see `CSV_VALIDATION_REPORT.md`. |
| Are broken bra-ket or LaTeX expressions present? | No broken notebook equations remain. Slide plain-text bras are fenced; see `LATEX_VALIDATION_REPORT.md`. |
| Are local absolute final-artifact paths present? | No user-home absolute paths were found in searched final-facing text files. |
| Does `usb_package/source_code` contain actual code? | Yes. It contains `src/`, `scripts/`, `tests/`, `configs/`, `submission/`, and `solution/`. |
| Does `source_code` include runnable entry points and env files? | Yes. `submission/run_all.py`, `requirements.txt`, and `pyproject.toml` are included. |
| Does presentation include English PDF/PPT? | Yes. `presentation/QuantumCylinder_presentation.pdf` exists. |
| Are forbidden claims present? | No positive forbidden claims found; mentions appear as explicit guardrails. |
| Are non-IBM QPU vendor references present? | No. The hardware path is IBM Quantum / IBM QPU via Qiskit Runtime. |
| Is there an IBM QPU validation path? | Yes. `scripts/ibm_qpu_smoke_test.py`, `docs/IBM_QPU_VALIDATION.md`, and `source_code/IBM_QPU_README.md`. |
| Top blocking issues before submission? | None. Real IBM QPU execution remains optional and requires credentials/queue access. |

## Validation Commands

- `python -m pytest --basetemp .pytest_tmp_local`: pass, 37 tests passed.
- `python submission/run_all.py --quick`: pass.
- `python scripts/ibm_qpu_smoke_test.py --dry-run`: pass, no real submission.
- pandas CSV validation: pass for root and USB `solution/tables/`.

## Remaining Manual Actions

- Open the final submitted PDF on another machine before the deadline.
- Run a real IBM QPU job only if credentials are available and the team wants optional appendix evidence.

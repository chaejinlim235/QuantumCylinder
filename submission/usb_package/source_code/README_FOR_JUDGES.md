# README For Judges

Open `solution/solution_1.ipynb` first for the compact final answer inside the
source-code package.

## Fast Reading Path

1. `solution/solution_1.ipynb`
2. `solution/README.md`
3. `PROBLEM_REQUIREMENT_MAP.md`
4. `REPRODUCIBILITY_COMMANDS.md`
5. `CODE_MANIFEST.md`
6. `IBM_QPU_README.md` for optional appendix validation only

The top-level USB package also includes split notebooks under `../solution/`.
Those are easier for presentation-style reading. This `solution/` folder is the
source-inspection copy of the compact final solution.

## What Is Included

| Path | Purpose |
| --- | --- |
| `solution/` | Compact final notebook, final figures, and final tables. |
| `src/quantum_cylinder/` | Core implementation. |
| `scripts/` | Experiment, plotting, IBM QPU, and summary scripts. |
| `tests/` | Sanity and regression tests. |
| `configs/` | Experiment configuration files. |
| `submission/` | Compact standalone execution layer. |
| `results/` | Selected compact evidence used by summary scripts. |
| `IBM_QPU_README.md` | Optional IBM Quantum / Qiskit Runtime appendix path. |

## Minimal Commands

Run from this `source_code/` directory:

```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/validate_final_csvs_no_pandas.py
```

Useful follow-up commands:

```powershell
python scripts/summarize_problem_3_seed_sweep.py
python scripts/summarize_problem_3_method_portfolio.py
python scripts/create_readable_problem2_figures.py
python scripts/ibm_qpu_smoke_test.py --dry-run
```

## Expected Results

- `pytest`: all tests should pass. On some Windows setups, if tests pass but
  temporary-directory cleanup fails, rerun with
  `python -m pytest --basetemp .pytest_tmp_local`.
- `submission/run_all.py --quick`: prints compact Problem 1, Problem 2, and
  Problem 3 reproduction summaries.
- `validate_final_csvs_no_pandas.py`: checks final CSVs, required readability
  figures, and the notebook notation table without pandas.
- `create_readable_problem2_figures.py`: regenerates the fixed-\(H\)
  readability figures from existing CSV data.
- `summarize_problem_3_seed_sweep.py`: reports the 20-seed Problem 3 evidence,
  including the small axis-only margin and the distance/success/diversity
  trade-off.
- `summarize_problem_3_method_portfolio.py`: reports the Problem 3(c) two-way
  candidate and appendix ablations.
- `ibm_qpu_smoke_test.py --dry-run`: builds tiny representative IBM-compatible
  circuits without submitting a QPU job.

## Source-Code Inspection Notes

- Numerical claims in the notebook are tied to CSV/Markdown files under
  `solution/tables/`, `solution/figures/`, and selected `results/` folders.
- IBM QPU validation is optional appendix evidence and is not required to
  reproduce the main state-vector benchmark.
- No IBM token, API key, instance CRN, or private account credential is stored
  in this package.

## Claim Guardrails

This is a small 2-qubit/3-qubit benchmark. It does not claim quantum advantage,
hardware advantage, a full trainable QuDDPM, continuous-basis dominance over
axis-only bases, a general unknown-target actor-critic denoiser, or universal
superiority of Hamiltonian projected diffusion over random-unitary diffusion.

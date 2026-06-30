# README for Judges

Open `solution/solution_1.ipynb` first. It is the final judge-facing answer.

## What Is Included

- `solution/`: final notebook, figures, and tables.
- `src/`: core implementation under `src/quantum_cylinder/`.
- `scripts/`: experiment, plotting, and summary scripts.
- `tests/`: sanity and regression tests.
- `configs/`: experiment configuration files.
- `submission/run_all.py`: quick reproduction entry point.
- `results/`: selected small CSV/Markdown evidence needed by the Problem 3 summary scripts.

## Minimal Commands

Run from this `source_code/` directory:

```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/summarize_problem_3_seed_sweep.py
python scripts/summarize_problem_3_method_portfolio.py
```

## Expected Results

- `python -m pytest`: all tests should pass. On some Windows setups, pytest may pass tests but fail during temp-directory cleanup; using `--basetemp .pytest_tmp_local` avoids that environment cleanup issue.
- `python submission/run_all.py --quick`: prints a compact Problem 1/2/3 reproduction summary.
- `python scripts/summarize_problem_3_seed_sweep.py`: prints the 20-seed Problem 3 summary including `20 / 20` passing seeds and median improvements.
- `python scripts/summarize_problem_3_method_portfolio.py`: prints the 3(c) two-way and appendix comparison table.

## Folder Reading Order

1. `solution/solution_1.ipynb`
2. `solution/README.md`
3. `PROBLEM_REQUIREMENT_MAP.md`
4. `REPRODUCIBILITY_COMMANDS.md`
5. `CODE_MANIFEST.md`
6. `scripts/` and `src/` for implementation details

## Limitations

This is a small 2-qubit/3-qubit state-vector benchmark. It does not claim quantum advantage, hardware advantage, a full trainable QuDDPM, continuous-basis dominance over axis-only bases, or a general unknown-target actor-critic denoiser.

# Task: Problem 3 Seed Sweep

Read these first:

- `.hermes.md`
- `README.md`
- `docs/11_problem_3_continuous_denoising.md`
- `scripts/run_problem_3_continuous_denoising.py`
- `configs/problem_3_continuous_denoising.json`

## Goal

Run the Problem 3 continuous measurement-induced denoising seed sweep and decide whether the result is robust enough to use as the main Problem 3 claim.

## Hard Constraints

- Do not modify tracked source files.
- Do not commit anything.
- Generated files under `results/` are allowed.
- Do not touch private/raw PDFs or application forms.
- If a command fails, stop and explain the failure.

## Commands To Run

Run tests first:

```powershell
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
& $ProjectPython -m pytest
```

Run the 20-seed sweep:

```powershell
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
$Seeds = 1..20

foreach ($Seed in $Seeds) {
    & $ProjectPython scripts/run_problem_3_continuous_denoising.py `
        --seed $Seed `
        --output-dir "results/problem_3_seed_sweep/seed_$Seed"
}
```

Aggregate the results and write a generated summary:

```powershell
$ProjectPython = if ($env:HERMES_PROJECT_PYTHON) { $env:HERMES_PROJECT_PYTHON } elseif (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
@'
from pathlib import Path
import csv
import statistics as stats

root = Path("results/problem_3_seed_sweep")
seed_dirs = sorted(root.glob("seed_*"), key=lambda p: int(p.name.split("_")[-1]))
summary_path = root / "seed_sweep_summary.md"

run_decisions = []
rows = []

for seed_dir in seed_dirs:
    seed = int(seed_dir.name.split("_")[-1])
    problem_summary = seed_dir / "problem_3_summary.md"
    best_path = seed_dir / "best_denoising_metrics.csv"

    if not problem_summary.exists() or not best_path.exists():
        print(f"Missing results for seed {seed}: {seed_dir}")
        continue

    summary_text = problem_summary.read_text(encoding="utf-8")
    if "Overall decision: `use_as_main`" in summary_text:
        overall = "use_as_main"
    elif "Overall decision: `fallback_only`" in summary_text:
        overall = "fallback_only"
    elif "Overall decision: `do_not_use_as_main`" in summary_text:
        overall = "do_not_use_as_main"
    else:
        overall = "unknown"

    run_decisions.append((seed, overall))

    with best_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            parsed = dict(row)
            parsed["seed"] = seed
            for key in [
                "continuous_mmd_improvement",
                "continuous_wasserstein_improvement",
                "continuous_diversity_retention",
                "continuous_mean_success_probability",
                "continuous_score_minus_axis_score",
            ]:
                parsed[key] = float(parsed[key])
            rows.append(parsed)

def count(values, target):
    return sum(1 for value in values if value == target)

overall_values = [decision for _, decision in run_decisions]
main_runs = count(overall_values, "use_as_main")
fallback_runs = count(overall_values, "fallback_only")
reject_runs = count(overall_values, "do_not_use_as_main")
unknown_runs = count(overall_values, "unknown")

main_rows = [row for row in rows if row["decision"] == "main_candidate"]
fallback_rows = [row for row in rows if row["decision"] == "fallback_candidate"]
reject_rows = [row for row in rows if row["decision"] == "do_not_use_as_main"]

def median_or_none(items, key):
    if not items:
        return None
    return stats.median(row[key] for row in items)

use_as_main_fraction = main_runs / len(run_decisions) if run_decisions else 0.0
main_row_fraction = len(main_rows) / len(rows) if rows else 0.0
median_score_margin = median_or_none(rows, "continuous_score_minus_axis_score")
median_diversity = median_or_none(rows, "continuous_diversity_retention")
median_success = median_or_none(rows, "continuous_mean_success_probability")
median_mmd_improvement = median_or_none(rows, "continuous_mmd_improvement")
median_wasserstein_improvement = median_or_none(rows, "continuous_wasserstein_improvement")

strong_enough = (
    use_as_main_fraction >= 0.70
    and main_row_fraction >= 0.40
    and median_score_margin is not None
    and median_score_margin > 0.0
    and median_diversity is not None
    and median_diversity >= 0.5
    and median_success is not None
    and median_success >= 0.1
    and (
        (median_mmd_improvement is not None and median_mmd_improvement >= 0.02)
        or (median_wasserstein_improvement is not None and median_wasserstein_improvement >= 0.02)
    )
)

lines = []
lines.append("# Problem 3 Seed Sweep Summary")
lines.append("")
lines.append("## Decision")
lines.append("")
lines.append(f"Main-claim recommendation: `{'use_as_main' if strong_enough else 'fallback_or_appendix'}`")
lines.append("")
lines.append("## Seed-Level Decisions")
lines.append("")
for seed, decision in run_decisions:
    lines.append(f"- seed `{seed}`: `{decision}`")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- Total seeds: `{len(run_decisions)}`")
lines.append(f"- use_as_main: `{main_runs}`")
lines.append(f"- fallback_only: `{fallback_runs}`")
lines.append(f"- do_not_use_as_main: `{reject_runs}`")
lines.append(f"- unknown: `{unknown_runs}`")
lines.append(f"- use_as_main fraction: `{use_as_main_fraction:.3f}`")
lines.append("")
lines.append("## Row-Level Counts")
lines.append("")
lines.append(f"- Total rows: `{len(rows)}`")
lines.append(f"- main_candidate rows: `{len(main_rows)}`")
lines.append(f"- fallback_candidate rows: `{len(fallback_rows)}`")
lines.append(f"- do_not_use_as_main rows: `{len(reject_rows)}`")
lines.append(f"- main_candidate row fraction: `{main_row_fraction:.3f}`")
lines.append("")
lines.append("## Medians Across Best Rows")
lines.append("")
for label, value in [
    ("continuous_mmd_improvement", median_mmd_improvement),
    ("continuous_wasserstein_improvement", median_wasserstein_improvement),
    ("continuous_score_minus_axis_score", median_score_margin),
    ("continuous_diversity_retention", median_diversity),
    ("continuous_mean_success_probability", median_success),
]:
    lines.append(f"- {label}: `{value:.6f}`" if value is not None else f"- {label}: `n/a`")
lines.append("")
lines.append("## Final Claim Guidance")
lines.append("")
if strong_enough:
    lines.append("The seed sweep supports using continuous projected denoising as the main Problem 3 result.")
else:
    lines.append("The seed sweep is not strong enough for the main claim. Keep it as fallback/appendix or weaken the claim.")

summary_path.parent.mkdir(parents=True, exist_ok=True)
summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(summary_path.read_text(encoding="utf-8"))
'@ | & $ProjectPython
```

## Final Response

After running the commands, report:

- Whether tests passed.
- How many seeds returned `use_as_main`.
- The `main_candidate` row fraction.
- The median MMD improvement.
- The median Wasserstein improvement.
- The median score margin over axis-only.
- The median diversity retention.
- The median mean success probability.
- Whether the final recommendation is `use_as_main` or `fallback_or_appendix`.
- The path to `results/problem_3_seed_sweep/seed_sweep_summary.md`.

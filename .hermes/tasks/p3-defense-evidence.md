# Task: Problem 3 Defense Evidence Package

Read these first:

- `.hermes.md`
- `README.md`
- `docs/00_team_dashboard.md`, if it exists
- `docs/11_problem_3_continuous_denoising.md`, if it exists
- `docs/15_quantitative_evaluation_plan.md`, if it exists
- `docs/16_three_day_roadmap.md`, if it exists
- `results/problem_3_seed_sweep/seed_sweep_summary.md`, if it exists
- `results/problem_3_continuous_denoising/problem_3_summary.md`, if it exists
- `submission/problem3_continuous_measurement_denoising.py`
- `scripts/run_problem_3_continuous_denoising.py`
- `scripts/summarize_problem_3_seed_sweep.py`

## Goal

Prepare QuantumCylinder for a 1-of-5 finalist decision.

The goal is not to keep searching for a slightly better best point. The goal is to build a judge-resistant evidence package showing that the team understood the hidden evaluation theme:

> Good quantum diffusion should not be judged only by how far it spreads. It should be evaluated by recoverability, post-selection success probability, diversity retention, and control/resource cost.

## Current Main Result To Preserve

The current robust result is:

- seed sweep recommendation: `use_as_main`
- `20/20` seeds: `use_as_main`
- main_candidate rows: `81/120 = 0.675`
- median MMD improvement: `0.097056`
- median Wasserstein improvement: `0.147983`
- median axis-only score margin: `0.010000`
- median diversity retention: `0.823217`
- median mean success probability: `0.468122`

Preserve this as the main Problem 3 result unless a new result is at least as robust and easier to defend.

## Priority Order

Work in this order. Stop after one focused, verified improvement if time is running long.

1. Frozen-parameter holdout:
   - Separate per-seed oracle/grid-best from a fixed parameter chosen on a reference run or train seeds.
   - Evaluate the frozen parameter on held-out seeds.
   - It is acceptable if the frozen result is weaker than oracle/grid-best, as long as the trend is honest and visible.

2. Baseline comparison table:
   - Include identity/no-denoising.
   - Include axis-only `Z/X/Y`.
   - Include continuous measurement-basis post-selection.
   - Include a collapse or strong-filter baseline if feasible, specifically to show why distance improvement alone is not enough.
   - Report MMD improvement, Wasserstein improvement, diversity retention, and success probability together.

3. Strong-scrambling defense ablation:
   - Check smaller random-unitary angle scales such as `0.2`, `0.5`, and `pi`.
   - This is for Q&A defense, not the main claim.

4. Killer figure draft:
   - Prefer one `2x2` figure:
     - pipeline schematic,
     - Problem 1/2 distance curves,
     - Problem 3 before/after denoising,
     - Pareto plot of improvement vs success probability with diversity retention encoded by marker size or color.

5. Judge-facing summary:
   - Produce or update a concise generated summary under `results/day2_finalist_package/`.
   - Include one-sentence contribution, key numbers, limitations, and what not to claim.

## Hard Constraints

- Do not commit anything.
- Do not open or merge PRs.
- Do not overwrite or revert user/team changes.
- Do not use `git reset --hard` or checkout files away.
- Do not touch private/raw PDFs, application forms, phone numbers, emails, signatures, or other PII.
- Generated files under `results/` and `logs/` are allowed and should not be added to Git.
- Keep Problem 1/2 stable unless a small compatibility fix is required.
- Do not claim hardware advantage, general quantum advantage, or real-device superiority.
- Do not claim continuous basis is overwhelmingly better than axis-only; the current axis-only margin is small.
- Do not claim a full QuDDPM reverse process.
- If a candidate underperforms, record it as an appendix/fallback result and preserve the current main claim.

## Verification

After any source change, run the narrowest relevant tests plus:

```powershell
python -m pytest --basetemp .pytest_tmp_day2_defense
python submission/run_all.py --quick
```

If a full seed sweep is too expensive, say so and preserve the existing 20-seed gate. If you run a new sweep, summarize it honestly.

## Report-Ready Framing

Preferred thesis:

> QuantumCylinder reproduces and compares random-unitary and Hamiltonian projected diffusion under the same fidelity-based metrics, then uses continuous measurement-basis post-selection to quantify the recoverability, success probability, diversity, and control-cost trade-off of quantum diffusion in a small-scale benchmark.

Safe claim:

> In small state-vector experiments, continuous measurement-basis post-selection is a reproducible post-selected toy denoising proxy. It improves MMD/Wasserstein metrics across the 20-seed sweep, while its axis-only margin remains small; therefore it should be presented as a recoverability-aware benchmark/probe, not as hardware advantage or broad quantum advantage.

## Final Response

Respond in Korean and include:

- what finalist-defense evidence was attempted,
- what changed in source/docs/results,
- whether tests passed,
- whether `submission/run_all.py --quick` passed,
- latest Problem 3 gate numbers,
- which judge question is now better defended,
- safest final-report wording,
- one concrete next action for the team.

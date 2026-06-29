# Task: Problem 3 Finalist Autopilot

Read these first:

- `.hermes.md`
- `README.md`
- `docs/00_team_dashboard.md`, if it exists
- `docs/11_problem_3_continuous_denoising.md`, if it exists
- `docs/15_quantitative_evaluation_plan.md`, if it exists
- `docs/16_three_day_roadmap.md`, if it exists
- `docs/19_problem_3_finalist_autopilot.md`, if it exists
- `results/problem_3_seed_sweep/seed_sweep_summary.md`, if it exists
- `results/problem_3_continuous_denoising/problem_3_summary.md`, if it exists
- `results/problem_3_finalist_autopilot/latest_status.md`, if it exists
- `results/problem_3_finalist_autopilot/progress_log.md`, if it exists
- `src/quantum_cylinder/problem_3_continuous_projected_denoising.py`
- `scripts/run_problem_3_continuous_denoising.py`
- `scripts/summarize_problem_3_seed_sweep.py`
- `submission/problem3_continuous_measurement_denoising.py`

## Team Context

QuantumCylinder is four undergraduate students. The team is comfortable with ML and software experiments, but not deeply trained in quantum physics. The automation should therefore produce evidence that is technically honest, reproducible, and easy to explain under judge questioning.

The finalist context is strict: only one of five teams advances. The goal is not random code churn. The goal is to turn Problem 3 into a memorable, defensible contribution.

## Problem 3 Requirements To Satisfy

Problem 3 asks for:

1. A simple reverse or denoising step for a toy example. A full trainable QuDDPM pipeline is not required.
2. A controlled modification or extension of the diffusion setting, with trade-off analysis.
3. A proposed improvement of random-unitary or Hamiltonian-time-evolution diffusion, tested on a small example and compared with at least one baseline.

Every cycle must improve the team answer to at least one of those three requirements.

## Finalist Thesis

Preferred thesis:

> QuantumCylinder reproduces random-unitary and Hamiltonian projected diffusion under the same fidelity-based metrics, then uses continuous measurement-basis post-selection to evaluate quantum diffusion by recoverability, post-selection success probability, diversity retention, and control/resource cost.

This is stronger than simply saying "we found a slightly better measurement basis." It frames the work as a recoverability-aware benchmark.

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

Preserve this as the main result unless a new result is at least as robust, easier to explain, and better aligned with Problem 3.

## Priority Order

Work in this order. Stop after one focused, verified improvement if time is running long.

1. Condition coverage audit:
   - Check whether Problem 3(a), 3(b), and 3(c) are each directly answered.
   - If a part is weak, improve the report-ready artifact or code output for that part.

2. Frozen-parameter holdout:
   - Defend against the question "did you choose the best point separately for every seed?"
   - Evaluate a fixed parameter chosen from reference/train seeds on held-out seeds.
   - It is okay if frozen holdout is weaker than oracle grid-best, as long as it is honest.

3. Baseline and collapse-defense table:
   - Include identity/no-denoising.
   - Include best exact `Z/X/Y` axis projection.
   - Include continuous measurement-basis post-selection.
   - Add a collapse or strong-filter baseline if feasible, to show why distance improvement alone is insufficient.
   - Report MMD, Wasserstein, diversity retention, and success probability together.

4. Strong-scrambling and parameter ablation:
   - Check angle scales such as `0.2`, `0.5`, and `pi` if supported by current code.
   - Use this for Q&A defense, not necessarily as the main result.

5. Figure/table packaging:
   - Produce a judge-facing result package under `results/problem_3_finalist_package/`.
   - Prefer a 2x2 story: pipeline, Problem 1/2 baselines, Problem 3 before/after, Pareto trade-off.

6. Final-report wording:
   - Add concise claim, limitation, and do-not-claim text.
   - Keep wording safe for a small state-vector toy experiment.

## Hard Constraints

- Do not commit anything.
- Do not open or merge PRs.
- Do not overwrite or revert user/team changes.
- Do not use `git reset --hard` or checkout files away.
- Do not touch private/raw PDFs, application forms, phone numbers, emails, signatures, or other PII.
- Generated files under `results/` and `logs/` are allowed and should not be added to Git.
- Keep Problem 1/2 stable unless a small compatibility or report-readiness fix is required.
- Do not claim hardware advantage, general quantum advantage, or real-device superiority.
- Do not claim continuous basis is overwhelmingly better than axis-only; the current axis-only margin is small.
- Do not claim a full trainable QuDDPM reverse process.
- If a candidate underperforms, record it as an appendix/fallback result and preserve the current main claim.

## Verification

After source changes, run:

```powershell
python -m pytest --basetemp .pytest_tmp_p3_finalist_autopilot
python submission/run_all.py --quick
```

If a full seed sweep is too expensive for the current cycle, preserve the existing 20-seed gate and state that clearly. If the wrapper script runs a seed sweep, read and summarize:

- `results/problem_3_seed_sweep/seed_sweep_summary.md`

## Decision Rules

Keep the current continuous post-selected denoising as the main Problem 3 result if:

- seed sweep recommendation remains `use_as_main`,
- MMD or Wasserstein improvement remains positive,
- diversity retention remains acceptable,
- success probability remains explainable,
- axis-only comparison is reported honestly as a small margin.

If a new idea does not beat the current gate, keep it as an appendix candidate and do not replace the main claim.

## Report-Ready Safe Claim

Use this wording unless newer evidence justifies a change:

> In small state-vector experiments, continuous measurement-basis post-selection is a reproducible post-selected toy denoising proxy. It improves MMD/Wasserstein metrics across the 20-seed sweep, while its axis-only margin remains small; therefore it should be presented as a recoverability-aware benchmark/probe, not as hardware advantage or broad quantum advantage.

## Final Response

Respond in Korean and include:

- what was attempted this cycle,
- what changed in source/docs/results,
- whether tests passed,
- whether `submission/run_all.py --quick` passed,
- whether the seed sweep was run or reused,
- latest Problem 3 gate numbers,
- which judge question is now better defended,
- safest final-report wording,
- one concrete next action for the team.

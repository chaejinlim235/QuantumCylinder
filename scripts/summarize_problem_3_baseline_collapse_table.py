"""Build a Problem 3 baseline/collapse-defense table.

The main seed sweep already compares diffused input, best exact Z/X/Y axis
projection, and continuous post-selection. This script repackages those rows and
adds one intentionally collapsed diagnostic baseline so the report can explain
why distance improvement alone is not enough.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics as stats
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble  # noqa: E402
from quantum_cylinder.problem_1b_ensemble_metrics import (  # noqa: E402
    mmd_fidelity,
    wasserstein_infidelity,
)
from quantum_cylinder.problem_3_continuous_projected_denoising import (  # noqa: E402
    ensemble_diversity,
    normalize_rows,
)

METHOD_ORDER = [
    "identity_no_denoising",
    "best_axis_projection",
    "continuous_postselection",
    "diagnostic_collapse_centroid",
]

METHOD_LABELS = {
    "identity_no_denoising": "identity/no-denoising random-unitary input",
    "best_axis_projection": "best exact Z/X/Y axis projection",
    "continuous_postselection": "continuous measurement-basis post-selection",
    "diagnostic_collapse_centroid": "diagnostic collapse-to-target-centroid filter",
}

REPORT_USE = {
    "identity_no_denoising": "baseline: what happens if we do no reverse step",
    "best_axis_projection": "discrete measurement baseline from the problem statement",
    "continuous_postselection": "main quantitative candidate when seed gate passes",
    "diagnostic_collapse_centroid": "failure mode: distance can improve while diversity collapses",
}

NUMERIC_BEST_COLUMNS = [
    "baseline_mmd",
    "baseline_wasserstein",
    "baseline_diversity",
    "continuous_mmd",
    "continuous_mmd_improvement",
    "continuous_wasserstein",
    "continuous_wasserstein_improvement",
    "continuous_diversity",
    "continuous_diversity_retention",
    "continuous_mean_success_probability",
    "axis_mmd",
    "axis_mmd_improvement",
    "axis_wasserstein",
    "axis_wasserstein_improvement",
    "axis_diversity",
    "axis_diversity_retention",
    "axis_mean_success_probability",
]

SUMMARY_COLUMNS = [
    "method_key",
    "method_label",
    "rows",
    "positive_improvement_rows",
    "median_mmd",
    "median_mmd_improvement",
    "median_wasserstein",
    "median_wasserstein_improvement",
    "median_diversity_retention",
    "median_mean_success_probability",
    "report_use",
]


class MissingSeedResultError(FileNotFoundError):
    """Raised when a requested seed is missing required generated files."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("results/problem_3_seed_sweep"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/problem_3_baseline_collapse_defense"),
    )
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(1, 21)))
    return parser.parse_args()


def _format_metric(value: float | None) -> str:
    return f"`{value:.6f}`" if value is not None else "`n/a`"


def _parse_best_row(row: dict[str, str], seed: int) -> dict[str, Any]:
    parsed: dict[str, Any] = dict(row)
    parsed["seed"] = seed
    parsed["input_step"] = int(parsed["input_step"])
    for column in NUMERIC_BEST_COLUMNS:
        parsed[column] = float(parsed[column])
    return parsed


def load_best_rows(seed_sweep_dir: Path, seeds: Iterable[int]) -> list[dict[str, Any]]:
    """Load per-seed best rows from an existing seed sweep."""

    rows: list[dict[str, Any]] = []
    missing: list[int] = []
    for seed in seeds:
        path = seed_sweep_dir / f"seed_{seed}" / "best_denoising_metrics.csv"
        if not path.exists():
            missing.append(seed)
            continue
        with path.open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                rows.append(_parse_best_row(row, seed=seed))
    if missing:
        raise MissingSeedResultError(f"Missing best_denoising_metrics.csv for seeds: {missing}")
    if not rows:
        raise ValueError(f"No best-denoising rows found under {seed_sweep_dir}")
    return rows


def collapse_to_reference_centroid(reference: np.ndarray) -> np.ndarray:
    """Return an intentionally collapsed ensemble at the target centroid.

    This is a diagnostic failure mode, not a physical reverse process. It can
    look excellent by distance metrics for a tight target cluster while retaining
    no sample diversity.
    """

    reference = normalize_rows(reference)
    centroid = np.mean(reference, axis=0)
    norm = np.linalg.norm(centroid)
    if norm <= 1e-14:
        centroid = reference[0]
    else:
        centroid = centroid / norm
    return normalize_rows(np.tile(centroid, (len(reference), 1)))


def collapse_metrics_for_seed(seed_sweep_dir: Path, seed: int, best_rows: list[dict[str, Any]]) -> dict[int, dict[str, float]]:
    settings_path = seed_sweep_dir / f"seed_{seed}" / "problem_3_settings.json"
    if not settings_path.exists():
        raise MissingSeedResultError(f"Missing problem_3_settings.json for seed {seed}")
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    reference = target_ensemble(
        int(settings["n_samples"]),
        sigma=float(settings["sigma"]),
        seed=int(settings["seed"]),
    )
    collapsed = collapse_to_reference_centroid(reference)
    collapse_mmd = float(mmd_fidelity(reference, collapsed))
    collapse_wasserstein = float(wasserstein_infidelity(reference, collapsed))
    collapse_diversity = float(ensemble_diversity(collapsed))

    metrics_by_step: dict[int, dict[str, float]] = {}
    for row in best_rows:
        input_step = int(row["input_step"])
        baseline_diversity = max(float(row["baseline_diversity"]), 1e-12)
        metrics_by_step[input_step] = {
            "mmd": collapse_mmd,
            "mmd_improvement": float(row["baseline_mmd"]) - collapse_mmd,
            "wasserstein": collapse_wasserstein,
            "wasserstein_improvement": float(row["baseline_wasserstein"]) - collapse_wasserstein,
            "diversity_retention": collapse_diversity / baseline_diversity,
            "mean_success_probability": 1.0,
        }
    return metrics_by_step


def build_method_rows(
    best_rows: list[dict[str, Any]],
    collapse_metrics: dict[tuple[int, int], dict[str, float]],
) -> list[dict[str, Any]]:
    """Expand seed/input-step best rows into one row per comparison method."""

    method_rows: list[dict[str, Any]] = []
    for row in best_rows:
        seed = int(row["seed"])
        input_step = int(row["input_step"])
        common = {"seed": seed, "input_step": input_step, "decision": row["decision"]}

        method_rows.append(
            {
                **common,
                "method_key": "identity_no_denoising",
                "method_label": METHOD_LABELS["identity_no_denoising"],
                "mmd": float(row["baseline_mmd"]),
                "mmd_improvement": 0.0,
                "wasserstein": float(row["baseline_wasserstein"]),
                "wasserstein_improvement": 0.0,
                "diversity_retention": 1.0,
                "mean_success_probability": 1.0,
                "success_probability_note": "deterministic/no post-selection",
                "report_use": REPORT_USE["identity_no_denoising"],
            }
        )
        method_rows.append(
            {
                **common,
                "method_key": "best_axis_projection",
                "method_label": METHOD_LABELS["best_axis_projection"],
                "mmd": float(row["axis_mmd"]),
                "mmd_improvement": float(row["axis_mmd_improvement"]),
                "wasserstein": float(row["axis_wasserstein"]),
                "wasserstein_improvement": float(row["axis_wasserstein_improvement"]),
                "diversity_retention": float(row["axis_diversity_retention"]),
                "mean_success_probability": float(row["axis_mean_success_probability"]),
                "success_probability_note": "post-selected axis baseline",
                "report_use": REPORT_USE["best_axis_projection"],
            }
        )
        method_rows.append(
            {
                **common,
                "method_key": "continuous_postselection",
                "method_label": METHOD_LABELS["continuous_postselection"],
                "mmd": float(row["continuous_mmd"]),
                "mmd_improvement": float(row["continuous_mmd_improvement"]),
                "wasserstein": float(row["continuous_wasserstein"]),
                "wasserstein_improvement": float(row["continuous_wasserstein_improvement"]),
                "diversity_retention": float(row["continuous_diversity_retention"]),
                "mean_success_probability": float(row["continuous_mean_success_probability"]),
                "success_probability_note": "post-selected continuous basis",
                "report_use": REPORT_USE["continuous_postselection"],
            }
        )

        collapse = collapse_metrics[(seed, input_step)]
        method_rows.append(
            {
                **common,
                "method_key": "diagnostic_collapse_centroid",
                "method_label": METHOD_LABELS["diagnostic_collapse_centroid"],
                "mmd": float(collapse["mmd"]),
                "mmd_improvement": float(collapse["mmd_improvement"]),
                "wasserstein": float(collapse["wasserstein"]),
                "wasserstein_improvement": float(collapse["wasserstein_improvement"]),
                "diversity_retention": float(collapse["diversity_retention"]),
                "mean_success_probability": float(collapse["mean_success_probability"]),
                "success_probability_note": "deterministic diagnostic; not a physical post-selection result",
                "report_use": REPORT_USE["diagnostic_collapse_centroid"],
            }
        )
    return method_rows


def summarize_method_rows(method_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for method_key in METHOD_ORDER:
        rows = [row for row in method_rows if row["method_key"] == method_key]
        if not rows:
            continue
        positive = sum(
            1
            for row in rows
            if float(row["mmd_improvement"]) > 0.0 or float(row["wasserstein_improvement"]) > 0.0
        )
        summaries.append(
            {
                "method_key": method_key,
                "method_label": METHOD_LABELS[method_key],
                "rows": len(rows),
                "positive_improvement_rows": positive,
                "median_mmd": float(stats.median(float(row["mmd"]) for row in rows)),
                "median_mmd_improvement": float(stats.median(float(row["mmd_improvement"]) for row in rows)),
                "median_wasserstein": float(stats.median(float(row["wasserstein"]) for row in rows)),
                "median_wasserstein_improvement": float(
                    stats.median(float(row["wasserstein_improvement"]) for row in rows)
                ),
                "median_diversity_retention": float(
                    stats.median(float(row["diversity_retention"]) for row in rows)
                ),
                "median_mean_success_probability": float(
                    stats.median(float(row["mean_success_probability"]) for row in rows)
                ),
                "report_use": REPORT_USE[method_key],
            }
        )
    return summaries


def build_summary(
    method_rows: list[dict[str, Any]],
    seeds: list[int],
    seed_sweep_summary: str = "results/problem_3_seed_sweep/seed_sweep_summary.md",
) -> str:
    summaries = summarize_method_rows(method_rows)
    summary_by_key = {row["method_key"]: row for row in summaries}
    collapse = summary_by_key.get("diagnostic_collapse_centroid")
    continuous = summary_by_key.get("continuous_postselection")
    collapse_warning = "not evaluated"
    if collapse is not None:
        collapse_warning = (
            "supported"
            if float(collapse["median_diversity_retention"]) <= 0.05
            else "weak_or_missing"
        )

    lines = [
        "# Problem 3 Baseline and Collapse-Defense Table",
        "",
        "## Purpose",
        "",
        "This table puts the Problem 3 distance metrics beside diversity retention and success probability. It is designed to answer the judge question: if a method makes MMD/Wasserstein smaller, did it actually denoise, or did it simply collapse the ensemble?",
        "",
        "The collapse row is intentionally diagnostic: it maps every sample to the target-ensemble centroid. It is not a physically proposed denoiser, not a hardware result, and not a replacement for the continuous post-selection gate.",
        "",
        "## Source",
        "",
        f"- seeds summarized: `{seeds}`",
        f"- seed sweep summary: `{seed_sweep_summary}`",
        "- per-seed rows: `results/problem_3_seed_sweep/seed_<n>/best_denoising_metrics.csv`",
        "- collapse diagnostic: recomputed from each seed's target ensemble and compared against each saved input step",
        "",
        "## Aggregate Table",
        "",
        "| Method | Rows | Positive-improvement rows | Median MMD | Median MMD improvement | Median Wasserstein | Median Wasserstein improvement | Median diversity retention | Median success probability | Report use |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summaries:
        lines.append(
            f"| {row['method_label']} "
            f"| `{row['rows']}` "
            f"| `{row['positive_improvement_rows']} / {row['rows']}` "
            f"| {_format_metric(float(row['median_mmd']))} "
            f"| {_format_metric(float(row['median_mmd_improvement']))} "
            f"| {_format_metric(float(row['median_wasserstein']))} "
            f"| {_format_metric(float(row['median_wasserstein_improvement']))} "
            f"| {_format_metric(float(row['median_diversity_retention']))} "
            f"| {_format_metric(float(row['median_mean_success_probability']))} "
            f"| {row['report_use']} |"
        )

    continuous_line = "`n/a`"
    if continuous is not None:
        continuous_line = (
            f"median MMD improvement {_format_metric(float(continuous['median_mmd_improvement']))}, "
            f"median Wasserstein improvement {_format_metric(float(continuous['median_wasserstein_improvement']))}, "
            f"median diversity retention {_format_metric(float(continuous['median_diversity_retention']))}, "
            f"median success probability {_format_metric(float(continuous['median_mean_success_probability']))}"
        )

    collapse_line = "`n/a`"
    if collapse is not None:
        collapse_line = (
            f"median MMD improvement {_format_metric(float(collapse['median_mmd_improvement']))}, "
            f"median Wasserstein improvement {_format_metric(float(collapse['median_wasserstein_improvement']))}, "
            f"but median diversity retention {_format_metric(float(collapse['median_diversity_retention']))}"
        )

    lines.extend(
        [
            "",
            "## Collapse-Defense Decision",
            "",
            f"- collapse warning: `{collapse_warning}`",
            f"- continuous post-selection gate in this table: {continuous_line}",
            f"- diagnostic collapse row: {collapse_line}",
            "",
            "Interpretation: distance improvement alone is insufficient. The diagnostic collapse filter can look strong on MMD/Wasserstein because the target ensemble is a tight cluster, but it destroys sample diversity. The report should therefore keep diversity retention and success probability in the same table as MMD/Wasserstein.",
            "",
            "## Judge-Facing Answer",
            "",
            "> We do not select a denoiser only by distance reduction. We compare identity/no-denoising, best exact Z/X/Y projection, continuous post-selection, and an intentionally collapsed diagnostic baseline. The collapsed baseline shows why a low MMD/Wasserstein number is not enough: it can erase ensemble diversity, so our adoption gate also requires diversity retention and post-selection success probability.",
            "",
            "## Do Not Claim",
            "",
            "- Do not use the collapse row as a proposed physical reverse process.",
            "- Do not claim hardware advantage or broad quantum advantage.",
            "- Do not claim continuous basis is overwhelmingly better than axis-only; keep the seed-sweep axis-margin caveat.",
            "",
            "## Generated Files",
            "",
            "- `baseline_collapse_metrics.csv`",
            "- `baseline_collapse_summary.csv`",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames or list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    seeds = sorted(set(args.seeds))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    best_rows = load_best_rows(args.input_dir, seeds)
    best_rows_by_seed: dict[int, list[dict[str, Any]]] = {seed: [] for seed in seeds}
    for row in best_rows:
        best_rows_by_seed[int(row["seed"])].append(row)

    collapse_by_key: dict[tuple[int, int], dict[str, float]] = {}
    for seed, rows in best_rows_by_seed.items():
        seed_collapse = collapse_metrics_for_seed(args.input_dir, seed, rows)
        for input_step, metrics in seed_collapse.items():
            collapse_by_key[(seed, input_step)] = metrics

    method_rows = build_method_rows(best_rows, collapse_by_key)
    summary_rows = summarize_method_rows(method_rows)
    summary = build_summary(
        method_rows,
        seeds=seeds,
        seed_sweep_summary=str(args.input_dir / "seed_sweep_summary.md"),
    )

    _write_rows(args.output_dir / "baseline_collapse_metrics.csv", method_rows)
    _write_rows(args.output_dir / "baseline_collapse_summary.csv", summary_rows, fieldnames=SUMMARY_COLUMNS)
    (args.output_dir / "baseline_collapse_summary.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

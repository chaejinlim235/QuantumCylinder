from __future__ import annotations

import argparse
import csv
import statistics as stats
import sys
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def number(row: dict[str, Any], key: str) -> float:
    value = row.get(key)
    if value in (None, "", "n/a"):
        return float("nan")
    return float(value)


def median(values: list[float]) -> float:
    valid = [value for value in values if value == value]
    return float(stats.median(valid)) if valid else float("nan")


def format_number(value: float) -> str:
    return "n/a" if value != value else f"{value:.6f}"


def summarize_existing_baselines(collapse_summary_path: Path) -> list[dict[str, Any]]:
    rows = read_csv_rows(collapse_summary_path)
    selected = []
    for row in rows:
        key = row["method_key"]
        if key == "diagnostic_collapse_centroid":
            continue
        elif key == "continuous_postselection":
            final_use = "3(b) continuous control/reference"
            caveat = "3(c)의 새 제안이 아니라 3-b trade-off 분석을 위한 control이다."
        elif key == "best_axis_projection":
            final_use = "3(b) discrete measurement baseline"
            caveat = "팀의 제안 후보가 아니라 Z/X/Y 축만 허용했을 때의 대조군이다."
        else:
            final_use = "no-denoising baseline"
            caveat = "reverse step을 하지 않았을 때의 기준점이다."
        selected.append(
            {
                "method_key": key,
                "method_label": row["method_label"],
                "comparison_scope": "same 2-qubit seed sweep",
                "rows": int(row["rows"]),
                "success_rows": row["positive_improvement_rows"],
                "median_mmd": number(row, "median_mmd"),
                "median_mmd_improvement": number(row, "median_mmd_improvement"),
                "median_wasserstein": number(row, "median_wasserstein"),
                "median_wasserstein_improvement": number(row, "median_wasserstein_improvement"),
                "median_diversity_retention": number(row, "median_diversity_retention"),
                "median_success_probability": number(row, "median_mean_success_probability"),
                "evidence_level": "20 seeds x 6 input steps",
                "final_use": final_use,
                "caveat": caveat,
            }
        )
    return selected


def summarize_hybrid(hybrid_best_path: Path) -> dict[str, Any]:
    rows = read_csv_rows(hybrid_best_path)
    positive = sum(
        1
        for row in rows
        if number(row, "mmd_improvement") > 0.0 and number(row, "wasserstein_improvement") > 0.0
    )
    return {
        "method_key": "hybrid_1m1f_toy",
        "method_label": "1 data qubit + 1 auxiliary hybrid post-selection toy",
        "comparison_scope": "1-qubit hardware-motivated extension, not direct 2-qubit seed-sweep replacement",
        "rows": len(rows),
        "success_rows": f"{positive} / {len(rows)}",
        "median_mmd": median([number(row, "candidate_mmd") for row in rows]),
        "median_mmd_improvement": median([number(row, "mmd_improvement") for row in rows]),
        "median_wasserstein": median([number(row, "candidate_wasserstein") for row in rows]),
        "median_wasserstein_improvement": median([number(row, "wasserstein_improvement") for row in rows]),
        "median_diversity_retention": median([number(row, "diversity_retention") for row in rows]),
        "median_success_probability": median([number(row, "mean_success_probability") for row in rows]),
        "evidence_level": "single-seed 1M+1F toy over 4 input steps",
        "final_use": "appendix circuit-visibility extension",
        "caveat": "system size differs from the main 2-qubit benchmark; use as plausibility evidence.",
    }


def summarize_actor_critic(actor_path: Path) -> dict[str, Any]:
    rows = read_csv_rows(actor_path)
    beats_both = sum(
        1
        for row in rows
        if row["actor_beats_continuous_mmd"] == "True"
        and row["actor_beats_continuous_wasserstein"] == "True"
    )
    return {
        "method_key": "target_aware_actor_critic",
        "method_label": "target-aware actor-critic filter search",
        "comparison_scope": "same 2-qubit metric, but target ensemble is used in the reward",
        "rows": len(rows),
        "success_rows": f"{beats_both} / {len(rows)}",
        "median_mmd": median([number(row, "actor_mmd") for row in rows]),
        "median_mmd_improvement": median([number(row, "actor_mmd_improvement") for row in rows]),
        "median_wasserstein": median([number(row, "actor_wasserstein") for row in rows]),
        "median_wasserstein_improvement": median([number(row, "actor_wasserstein_improvement") for row in rows]),
        "median_diversity_retention": median([number(row, "actor_diversity_retention") for row in rows]),
        "median_success_probability": median([number(row, "actor_success_probability") for row in rows]),
        "evidence_level": "10 seeds x 3 input steps",
        "final_use": "appendix target-aware policy-search candidate",
        "caveat": "not an unknown-target denoiser; claim only target-aware policy selection.",
    }


def summarize_hamiltonian_variants(variant_summary_path: Path) -> list[dict[str, Any]]:
    rows = read_csv_rows(variant_summary_path)
    result = []
    labels = {
        "hamiltonian_then_random_final_kick": "Hamiltonian post-selection + random final kick",
        "hamiltonian_two_way_postselection": "Hamiltonian two-way post-selection",
    }
    final_uses = {
        "hamiltonian_then_random_final_kick": "appendix mixture ablation from 3-b trade-off",
        "hamiltonian_two_way_postselection": "3(c) main: two-way projected denoising",
    }
    caveats = {
        "hamiltonian_then_random_final_kick": "random final kick can slightly help or hurt; use as mixture ablation, not main result.",
        "hamiltonian_two_way_postselection": "larger distance improvement costs lower post-selection success probability.",
    }
    for row in rows:
        method = row["method"]
        if method not in labels:
            continue
        result.append(
            {
                "method_key": method,
                "method_label": labels[method],
                "comparison_scope": "same 2-qubit metric, 5 seeds x 3 input steps",
                "rows": int(row["rows"]),
                "success_rows": f"{row['positive_mmd_rows']} MMD / {row['positive_wasserstein_rows']} W",
                "median_mmd": float("nan"),
                "median_mmd_improvement": number(row, "median_mmd_improvement"),
                "median_wasserstein": float("nan"),
                "median_wasserstein_improvement": number(row, "median_wasserstein_improvement"),
                "median_diversity_retention": number(row, "median_diversity_retention"),
                "median_success_probability": number(row, "median_success_probability"),
                "evidence_level": "5 seeds x 3 input steps",
                "final_use": final_uses[method],
                "caveat": caveats[method],
            }
        )
    return result


def build_portfolio(args: argparse.Namespace) -> list[dict[str, Any]]:
    rows = summarize_existing_baselines(args.collapse_summary)
    if args.hamiltonian_variants.exists():
        rows.extend(summarize_hamiltonian_variants(args.hamiltonian_variants))
    if args.hybrid_best.exists():
        rows.append(summarize_hybrid(args.hybrid_best))
    if args.actor_metrics.exists():
        rows.append(summarize_actor_critic(args.actor_metrics))
    return rows


def write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Problem 3 Two-Way Main and Appendix Rows",
        "",
        "## Purpose",
        "",
        "Problem 3(c) is derived from the Problem 3(b) analysis, not from the previous actor-critic-only or broad portfolio direction. Problem 3(b) first shows the recoverability trade-off: continuous measurement-basis control improves MMD/Wasserstein across seeds, but the axis-only margin is small and success probability/diversity must be reported together. Problem 3(c) then uses that analysis to propose one main improvement: two-way projected denoising.",
        "",
        "## Why Axis-Only and Continuous Appear",
        "",
        "- `best exact Z/X/Y axis projection` is a discrete measurement baseline, not a team-proposed improvement method.",
        "- `continuous measurement-basis post-selection` is the controlled 3(b) experiment/reference, not a new 3(c) proposal by itself.",
        "- The main 3(c) proposal is `Hamiltonian two-way post-selection`: stronger projected denoising with a lower success probability.",
        "- `Hamiltonian + random final kick`, `hybrid 1M+1F`, and `target-aware actor-critic` should be treated as appendix/ablation/extension rows, not as the main report story.",
        "",
        "## Candidate Table",
        "",
        "| Method | Scope | Rows | Success rows | Median MMD improvement | Median Wasserstein improvement | Median diversity retention | Median success probability | Final use | Caveat |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["method_label"]),
                    str(row["comparison_scope"]),
                    str(row["rows"]),
                    str(row["success_rows"]),
                    format_number(float(row["median_mmd_improvement"])),
                    format_number(float(row["median_wasserstein_improvement"])),
                    format_number(float(row["median_diversity_retention"])),
                    format_number(float(row["median_success_probability"])),
                    str(row["final_use"]),
                    str(row["caveat"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Final Selection Rule",
            "",
            "1. In Problem 3(b), present the values as analysis: seed robustness, distance improvement, small axis-only margin, diversity retention, and post-selection success probability.",
            "2. Treat `best exact Z/X/Y axis projection` as the controlled baseline for Problem 3(b), not as a proposed method.",
            "3. Treat `continuous measurement-basis post-selection` as the 3(b) control/reference that exposes the trade-off, not as the 3(c) story by itself.",
            "4. Use `Hamiltonian two-way post-selection` as the main Problem 3(c) proposal because it directly tests how the 3-b trade-off changes under stronger projected denoising.",
            "5. Move `Hamiltonian + random final kick`, `hybrid 1M+1F toy`, and `target-aware actor-critic` to appendix/ablation/extension status.",
            "",
            "## Report Claim",
            "",
            "The final report should say that Problem 3(b) revealed a recoverability trade-off: continuous measurement-basis control reduces MMD/Wasserstein reproducibly, but the advantage over axis-only is small and must be interpreted with diversity retention and success probability. Problem 3(c) then proposes two-way Hamiltonian post-selection as an analysis-guided improvement: it increases distance reduction while lowering post-selection success probability. The other rows are appendix or ablation evidence, not the main 3-c story.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_figure(path: Path, rows: list[dict[str, Any]]) -> None:
    labels = [row["method_key"] for row in rows]
    x = list(range(len(rows)))
    width = 0.38

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    axes[0].bar(
        [i - width / 2 for i in x],
        [float(row["median_mmd_improvement"]) for row in rows],
        width,
        label="median MMD improvement",
    )
    axes[0].bar(
        [i + width / 2 for i in x],
        [float(row["median_wasserstein_improvement"]) for row in rows],
        width,
        label="median Wasserstein improvement",
    )
    axes[0].axhline(0.0, color="black", linewidth=0.8)
    axes[0].set_ylabel("Distance improvement")
    axes[0].set_title("Problem 3 two-way main and appendix rows: distance metrics")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend()

    axes[1].bar(
        [i - width / 2 for i in x],
        [float(row["median_diversity_retention"]) for row in rows],
        width,
        label="median diversity retention",
    )
    axes[1].bar(
        [i + width / 2 for i in x],
        [float(row["median_success_probability"]) for row in rows],
        width,
        label="median success probability",
    )
    axes[1].set_ylabel("Recoverability guardrails")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=30, ha="right")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].legend()

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize the Problem 3 two-way main and appendix rows.")
    parser.add_argument(
        "--collapse-summary",
        type=Path,
        default=ROOT / "results" / "problem_3_baseline_collapse_defense" / "baseline_collapse_summary.csv",
    )
    parser.add_argument(
        "--hybrid-best",
        type=Path,
        default=ROOT / "results" / "problem_3_hybrid_diffusion_toy" / "hybrid_best_metrics.csv",
    )
    parser.add_argument(
        "--actor-metrics",
        type=Path,
        default=ROOT / "results" / "problem_3_actor_critic_denoising" / "actor_critic_metrics.csv",
    )
    parser.add_argument(
        "--hamiltonian-variants",
        type=Path,
        default=ROOT / "results" / "problem_3_hamiltonian_variants" / "hamiltonian_variant_summary.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "problem_3_method_portfolio",
    )
    return parser.parse_args()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()
    rows = build_portfolio(args)
    csv_path = args.output_dir / "method_portfolio_summary.csv"
    md_path = args.output_dir / "method_portfolio_summary.md"
    png_path = args.output_dir / "method_portfolio_summary.png"
    write_csv_rows(csv_path, rows)
    write_markdown(md_path, rows)
    write_figure(png_path, rows)
    print(md_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

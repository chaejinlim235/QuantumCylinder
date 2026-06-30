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
            final_use = "3(a)/3(b)의 main quantitative result"
            caveat = "axis-only 대비 margin은 작으므로 작은 post-selected proxy로 제한한다."
        elif key == "best_axis_projection":
            final_use = "3(b) discrete measurement baseline"
            caveat = "continuous basis가 정말 필요한지 확인하는 대조군이다."
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
        "final_use": "3(c) hardware-motivated extension candidate",
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
        "final_use": "3(c) strongest target-aware candidate, not the only method",
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
        "hamiltonian_then_random_final_kick": "3(c) mixture candidate",
        "hamiltonian_two_way_postselection": "3(c) two-stage Hamiltonian candidate",
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
        "# Problem 3 Method Portfolio",
        "",
        "## Purpose",
        "",
        "Problem 3 is presented as a portfolio of candidate reverse/denoising ideas, not as a single actor-critic-only result. The methods are compared with the same distance language whenever possible, and each row states whether it is a main result, a baseline, or an extension candidate.",
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
            "1. Use `continuous measurement-basis post-selection` as the main Problem 3(a/b) quantitative result because it has the 20-seed robustness gate.",
            "2. Use `best exact Z/X/Y axis projection` as the controlled baseline for Problem 3(b), not as a failed or hidden method.",
            "3. Use `Hamiltonian + random final kick` and `Hamiltonian two-way post-selection` as explicit Problem 3(c) candidates because they were proposed by the team and actually executed.",
            "4. Use `hybrid 1M+1F toy` as a hardware-motivated Problem 3(c) extension because it keeps the auxiliary-measurement mechanism visible at the smallest circuit scale.",
            "5. Use `target-aware actor-critic` only as a stronger 3(c) candidate under a clear target-aware limitation.",
            "",
            "## Report Claim",
            "",
            "The final report should say that several reverse-process ideas were tested under common recoverability metrics. The selected story is not that actor-critic replaced all methods. The selected story is that continuous post-selection is the robust main denoising proxy, Hamiltonian mixture/two-way variants are executed 3(c) candidates, hybrid 1M+1F is the hardware-motivated extension, and actor-critic is an optional target-aware policy-search improvement with a stricter caveat.",
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
    axes[0].set_title("Problem 3 candidate portfolio: distance metrics")
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
    parser = argparse.ArgumentParser(description="Summarize the Problem 3 method portfolio.")
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

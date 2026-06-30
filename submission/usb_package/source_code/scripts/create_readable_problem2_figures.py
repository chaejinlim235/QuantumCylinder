"""Create final-facing Problem 2 readability figures without changing data."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "solution" / "tables"
FIG_DIR = ROOT / "solution" / "figures"


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _value(row: dict[str, str], *names: str) -> float:
    for name in names:
        if name in row:
            return float(row[name])
    raise KeyError(f"none of {names!r} found in row keys {sorted(row)}")


def _text(row: dict[str, str], *names: str) -> str:
    for name in names:
        if name in row:
            return row[name]
    raise KeyError(f"none of {names!r} found in row keys {sorted(row)}")


def create_fixed_h_baseline_figure() -> Path:
    ham = _read_rows(TABLE_DIR / "problem_2_hamiltonian_metrics.csv")
    t = [_value(row, "control_value", "parameter") for row in ham]
    mmd = [_value(row, "D_MMD", "mmd") for row in ham]
    wass = [_value(row, "W_1_minus_F", "wasserstein") for row in ham]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), constrained_layout=True)

    axes[0].plot(
        t,
        mmd,
        color="#b22222",
        linestyle="-",
        marker="s",
        linewidth=3.0,
        markersize=7,
        markeredgecolor="black",
        markeredgewidth=0.8,
        label=r"$D_{\mathrm{MMD}}(S_t^{\mathrm{Ham}}, S_0)$",
        zorder=5,
    )
    axes[0].set_title(r"Problem 2 fixed-$H$ baseline: MMD")
    axes[0].set_xlabel(r"Hamiltonian evolution time $t$")
    axes[0].set_ylabel(r"Fidelity-kernel MMD, $D_{\mathrm{MMD}}$")
    axes[0].grid(alpha=0.25)

    axes[1].plot(
        t,
        wass,
        color="#5b2ca0",
        linestyle="--",
        marker="D",
        linewidth=3.0,
        markersize=7,
        markeredgecolor="black",
        markeredgewidth=0.8,
        label=r"$W_{1-F}(S_t^{\mathrm{Ham}}, S_0)$",
        zorder=5,
    )
    axes[1].set_title(r"Problem 2 fixed-$H$ baseline: Wasserstein-type")
    axes[1].set_xlabel(r"Hamiltonian evolution time $t$")
    axes[1].set_ylabel(r"Wasserstein-type distance, $W_{1-F}$")
    axes[1].grid(alpha=0.25)

    for axis in axes:
        axis.legend(loc="upper left", frameon=True)

    fig.suptitle(
        r"Hamiltonian projected diffusion under fixed $H$ "
        r"($h_x=0.8090,\ h_y=0.9045,\ J=1.0$)",
        fontsize=14,
    )
    axes[0].annotate(
        r"Problem 2 fixed-$H$ projected diffusion baseline",
        xy=(t[3], mmd[3]),
        xytext=(t[3] + 0.25, 0.36),
        arrowprops={"arrowstyle": "->", "linewidth": 1.2},
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#999999", "alpha": 0.9},
    )

    out = FIG_DIR / "fig_p2_fixed_h_baseline_visible.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def create_metric_aligned_readable_figure() -> Path:
    ru = _read_rows(TABLE_DIR / "problem_1c_random_unitary_metrics.csv")
    ham = _read_rows(TABLE_DIR / "problem_2_hamiltonian_metrics.csv")
    matches = _read_rows(TABLE_DIR / "problem_2d_resource_matches.csv")

    ru_mmd = [_value(row, "D_MMD", "mmd") for row in ru]
    ru_w = [_value(row, "W_1_minus_F", "wasserstein") for row in ru]
    ham_t = [_value(row, "control_value", "parameter") for row in ham]
    ham_mmd = [_value(row, "D_MMD", "mmd") for row in ham]
    ham_w = [_value(row, "W_1_minus_F", "wasserstein") for row in ham]

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), constrained_layout=True)

    axes[0].scatter(
        ru_mmd,
        ru_w,
        s=55,
        color="#1f77b4",
        marker="o",
        alpha=0.85,
        label=r"Random-unitary $S_k^{\mathrm{RU}}$",
        zorder=2,
    )
    axes[0].plot(ru_mmd, ru_w, color="#1f77b4", linestyle=":", linewidth=1.8, zorder=1)
    axes[0].scatter(
        ham_mmd,
        ham_w,
        s=95,
        color="#d62728",
        marker="s",
        edgecolor="black",
        linewidth=0.8,
        alpha=0.95,
        label=r"Hamiltonian projected $S_t^{\mathrm{Ham}}$ under fixed $H$",
        zorder=6,
    )
    axes[0].plot(ham_mmd, ham_w, color="#d62728", linestyle="-", linewidth=2.6, zorder=5)

    label_offsets = {
        1: (8, -16),
        10: (8, -18),
        12: (-58, -18),
    }
    for idx, (x_val, y_val, t_val) in enumerate(zip(ham_mmd, ham_w, ham_t)):
        if idx in label_offsets:
            offset = label_offsets[idx]
            axes[0].annotate(
                f"t={t_val:.2f}",
                xy=(x_val, y_val),
                xytext=offset,
                textcoords="offset points",
                fontsize=8,
                color="#5a1a1a",
                bbox={"boxstyle": "round,pad=0.12", "fc": "white", "ec": "none", "alpha": 0.75},
            )

    axes[0].set_title("Metric-space trajectories")
    axes[0].set_xlabel(r"Fidelity-kernel MMD, $D_{\mathrm{MMD}}(S,S_0)$")
    axes[0].set_ylabel(r"Wasserstein-type distance, $W_{1-F}(S,S_0)$")
    axes[0].grid(alpha=0.25)
    axes[0].legend(loc="lower center", bbox_to_anchor=(0.5, -0.34), ncol=1, frameon=True)

    labels: list[str] = []
    random_vals: list[float] = []
    ham_vals: list[float] = []
    annotations: list[str] = []
    for row in matches:
        matched = _text(row, "matched_metric", "matched_by").lower()
        if "wasserstein" in matched or "w_1" in matched:
            labels.append(r"$W_{1-F}$ matched")
            random_vals.append(_value(row, "random_W_1_minus_F", "random_wasserstein"))
            ham_vals.append(_value(row, "hamiltonian_W_1_minus_F", "hamiltonian_wasserstein"))
            annotations.append(
                "k={:g}, t={:.2f}\ngap={:.4f}".format(
                    _value(row, "random_unitary_layer_k", "random_step"),
                    _value(row, "hamiltonian_time_t", "hamiltonian_time"),
                    _value(row, "W_1_minus_F_gap", "wasserstein_gap"),
                )
            )
        else:
            labels.append(r"$D_{\mathrm{MMD}}$ matched")
            random_vals.append(_value(row, "random_D_MMD", "random_mmd"))
            ham_vals.append(_value(row, "hamiltonian_D_MMD", "hamiltonian_mmd"))
            annotations.append(
                "k={:g}, t={:.2f}\ngap={:.4f}".format(
                    _value(row, "random_unitary_layer_k", "random_step"),
                    _value(row, "hamiltonian_time_t", "hamiltonian_time"),
                    _value(row, "D_MMD_gap", "mmd_gap"),
                )
            )

    x = list(range(len(labels)))
    width = 0.34
    axes[1].bar(
        [i - width / 2 for i in x],
        random_vals,
        width,
        color="#1f77b4",
        label=r"Random-unitary $S_k^{\mathrm{RU}}$",
        zorder=2,
    )
    axes[1].bar(
        [i + width / 2 for i in x],
        ham_vals,
        width,
        color="#d62728",
        edgecolor="black",
        linewidth=0.7,
        hatch="//",
        label=r"Fixed-$H$ projected $S_t^{\mathrm{Ham}}$",
        zorder=5,
    )
    for i, note in enumerate(annotations):
        top = max(random_vals[i], ham_vals[i])
        axes[1].annotate(
            note,
            xy=(i, top),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "#bbbbbb", "alpha": 0.9},
        )

    axes[1].set_title("Comparable output-metric pairs")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("Matched metric value")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.34), ncol=1, frameon=True)

    fig.suptitle("Problem 2(c,d): random-unitary vs fixed-Hamiltonian projected diffusion", fontsize=14)
    out = FIG_DIR / "fig_metric_aligned_comparison_readable.png"
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [create_fixed_h_baseline_figure(), create_metric_aligned_readable_figure()]
    for path in outputs:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()

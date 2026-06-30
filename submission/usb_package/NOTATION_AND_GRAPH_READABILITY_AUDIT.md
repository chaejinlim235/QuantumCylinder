# Notation And Graph Readability Audit

## Scope

Checked final-facing materials:

- `solution/solution_1.ipynb`
- `solution/README.md`
- `solution/figures/`
- `solution/tables/`
- `submission/usb_package/presentation/PRESENTATION_SLIDE_TEXT_EN.md`
- `submission/usb_package/presentation/PRESENTATION_STORYBOARD_EN.md`
- `submission/usb_package/JUDGING_CRITERIA_ALIGNMENT.md`
- `submission/usb_package/source_code/results/ibm_qpu_validation/`
- `README.md`

## Audit Questions

### 1. Which figures/tables used informal variable names?

Before this pass, the final-facing CSV/table layer used informal or code-like
labels such as `mmd`, `wasserstein`, `mmd_gain`, `wasserstein_gain`,
`success_probability`, `diversity_retention`, `random_step`, and
`hamiltonian_time`.

Updated or clarified final-facing tables:

- `solution/tables/problem_1c_random_unitary_metrics.csv`
- `solution/tables/problem_2_hamiltonian_metrics.csv`
- `solution/tables/problem_2d_resource_matches.csv`
- `solution/tables/problem3b_measurement_basis_tradeoff.csv`
- `solution/tables/problem3c_analysis_guided_improvement.csv`

The notebook and presentation now use \(D_{\mathrm{MMD}}\), \(W_{1-F}\),
\(S_k^{\mathrm{RU}}\), \(S_t^{\mathrm{Ham}}\), \(\Delta D\),
\(p_{\mathrm{succ}}\), \(R_{\mathrm{div}}\), and \(\beta\).

### 2. Does cell 11 or the relevant graph hide the Problem 2 fixed-Hamiltonian baseline?

The current cell numbered 11 is a limitations section after the notation-cell
insertion, but the feedback corresponds to the Problem 2 metric-aligned graph
near the Problem 2 sections. The original figure
`solution/figures/problem_1_2_metric_aligned_comparison.png` did show the
Hamiltonian projection points, but labels and the comparable-pair bar
annotations could visually clutter the fixed-\(H\) baseline.

The issue is fixed by adding:

- `solution/figures/fig_p2_fixed_h_baseline_visible.png`
- `solution/figures/fig_metric_aligned_comparison_readable.png`

The fixed-\(H\) projected baseline is now drawn with emphasized square markers,
thicker lines, distinct line style/marker style, and a standalone fixed-\(H\)
panel.

### 3. Which figure files correspond to the cell 11 graph?

Relevant existing and corrected files:

- Existing source figure: `solution/figures/problem_1_2_metric_aligned_comparison.png`
- Corrected readable comparison: `solution/figures/fig_metric_aligned_comparison_readable.png`
- Standalone fixed-\(H\) baseline: `solution/figures/fig_p2_fixed_h_baseline_visible.png`

### 4. Are Problem 1(c), Problem 2(c), Problem 2(d), Problem 3(b), and Problem 3(c) labels tied to the problem statement?

Yes. The notebook and presentation now explicitly connect:

- Problem 1(c): \(k\), \(S_k^{\mathrm{RU}}\), \(D(S_k^{\mathrm{RU}},S_0)\),
  and the Haar-like strong-scrambling reference.
- Problem 2(c): \(t\), \(S_t^{\mathrm{Ham}}\), and fixed-\(H\) projected
  diffusion.
- Problem 2(d): random layer/entangler controls versus fixed-Hamiltonian time
  and projection-basis control.
- Problem 3(b): measurement-basis angle \(\beta\), \(\Delta D\),
  \(p_{\mathrm{succ}}\), and \(R_{\mathrm{div}}\).
- Problem 3(c): two-way post-selection as stronger distance improvement with
  lower \(p_{\mathrm{succ}}\).

### 5. Is there a notation table in the final notebook?

Yes. `solution/solution_1.ipynb` now includes a near-front section titled
`Notation used in figures`.

### 6. Are variable definitions clear enough for a reader who does not know the code?

Yes. The notebook defines the main ensemble symbols and metric symbols before
the problem sections. It also defines \(R_{\mathrm{div}}\) using the code
implementation:

\[
R_{\mathrm{div}} =
\frac{\mathrm{diversity}(S_{\mathrm{after}})}
{\max(\mathrm{diversity}(S_{\mathrm{before}}),10^{-12})},
\quad
\mathrm{diversity}(S)=\mathrm{mean}_{i\ne j}(1-F(\psi_i,\psi_j)).
\]

This is explicitly called a diversity retention proxy and collapse guardrail,
not a universal diversity metric.

### 7. Are IBM QPU appendix labels clearly appendix-only?

Yes. The final notebook, presentation text, and IBM documents label IBM QPU
Problem 3-b validation as appendix hardware-execution evidence only. They state
that it tests tiny representative circuits and does not replace the
state-vector benchmark or claim hardware advantage.

## Decision

Notation rigor and graph readability are now substantially improved for final
judging. No experimental values were changed, and no IBM QPU jobs were rerun.

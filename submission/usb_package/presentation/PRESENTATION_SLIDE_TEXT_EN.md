# QuantumCylinder Slide Text

## Core Slides

### Slide 1. QuantumCylinder

**One-sentence contribution:** We compare random-unitary diffusion and Hamiltonian projected diffusion under shared fidelity-based metrics, then analyze measurement-induced projected denoising as a recoverability-success-diversity trade-off.

Speaker note: "The goal is not to overclaim. We give a complete small-scale benchmark and a clear Problem 3 extension."

### Slide 2. Problem Map and Judging Criteria

- Problem 1: target ensemble, metrics, random-unitary diffusion.
- Problem 2: fixed Hamiltonian projected diffusion and resource/control comparison.
- Problem 3: measurement-induced denoising, measurement-basis trade-off, two-way post-selection.
- Package includes final notebook, figures, tables, tests, and source code.

Speaker note: "This slide anchors completeness and source-code clarity."

Notation note:

| Symbol / label | Meaning |
|---|---|
| \(S_0\) | Initial two-qubit target ensemble clustered near \(|00\rangle\) |
| \(S_k^{\mathrm{RU}}\) | Ensemble after \(k\) random-unitary scrambling layers |
| \(S_t^{\mathrm{Ham}}\) | Projected data-system ensemble after fixed-Hamiltonian evolution time \(t\) |
| \(D_{\mathrm{MMD}}\) | Fidelity-kernel MMD distance |
| \(W_{1-F}\) | Wasserstein-type distance with pairwise cost \(1-F\) |
| \(D(S,S_0)\) | Distance between ensemble \(S\) and the initial ensemble \(S_0\) |
| \(\Delta D\) | Denoising distance gain, before minus after |
| \(p_{\mathrm{succ}}\) | Post-selection success probability |
| \(R_{\mathrm{div}}\) | Diversity retention proxy, computed as retained average off-diagonal infidelity |
| \(\beta\) | Complement-qubit measurement-basis angle |
| fixed \(H\) | Problem 2 Hamiltonian with \(h_x=0.8090, h_y=0.9045, J=1.0\) |

### Slide 3. Problem 1: Random-Unitary Diffusion

- `S0` is clustered near `|00>`.
- Random-unitary layers rapidly move the ensemble away from `S0`.
- Haar reference: \(D_{\mathrm{MMD}}\) `0.869583 +/- 0.024043`, \(W_{1-F}\) `0.724439 +/- 0.021491`.
- Interpretation: strong scrambling / Haar-like plateau.

Figure: `source_code/solution/figures/fig2_random_unitary_haar_baseline.png`

Speaker note: "The Haar reference is not a target distribution. It is a calibration level for strong scrambling."

### Slide 4. Problem 2: Hamiltonian Projected Diffusion

- Data system `M` plus complement qubit `F`.
- Fixed Hamiltonian evolution followed by projection.
- Curves can fluctuate or partially saturate depending on the schedule.
- Resource proxy: random gate controls vs fixed Hamiltonian time and projection basis.

Figure: `source_code/solution/figures/fig_metric_aligned_comparison_readable.png`

Fixed-\(H\) standalone panel: `source_code/solution/figures/fig_p2_fixed_h_baseline_visible.png`

Speaker note: "The comparison is qualitative and control-aware, not a universal ranking."

### Slide 5. Problem 3(b): Measurement-Basis Trade-Off

- `M+F` evolves unitarily.
- Measuring `F` and post-selecting induces an effective non-unitary map on `M`.
- Axis-only `Z/X/Y` is a Pauli-basis baseline.
- Continuous Bloch-sphere basis is a controlled generalization.
- Main point: \(\Delta D\), \(p_{\mathrm{succ}}\), and \(R_{\mathrm{div}}\) must be reported together.

Table: `source_code/solution/tables/problem3b_measurement_basis_tradeoff.csv`

Speaker note: "The axis-only margin is small, so the claim is the trade-off analysis."

### Slide 6. Problem 3(c): Two-Way Post-Selection

- Based on 3-b, stronger contraction can improve distance metrics.
- Two-way Hamiltonian post-selection applies the projected denoising idea more strongly.
- Median \(\Delta D_{\mathrm{MMD}}\): `0.101374`.
- Median \(\Delta W_{1-F}\): `0.136426`.
- Median \(p_{\mathrm{succ}}\): `0.227065`.
- Interpretation: stronger distance improvement with lower success probability.

Table: `source_code/solution/tables/problem3c_analysis_guided_improvement.csv`

Speaker note: "This is a trade-off improvement, not an unconditional win."

### Slide 7. Conclusion

- Novelty: measurement basis as a control knob for effective non-unitary projected maps.
- Completeness: Problems 1(a) through 3(c) answered and connected.
- Appropriateness: small state-vector benchmark with explicit limitations.
- Source code and reproduction commands are included.

Speaker note: "The final result is intentionally scoped and reproducible."

## Appendix Slides

### A1. Metric Definitions

- Fidelity: `F(psi, phi) = |<psi|phi>|^2`.
- \(D_{\mathrm{MMD}}\) uses fidelity kernel.
- \(W_{1-F}\) uses cost `1 - F`.

### A2. Hamiltonian and Projected Ensemble

- `M+F` evolves under a fixed Hamiltonian.
- Projection of `F` creates a data-system ensemble.

### A3. Measurement-Induced Non-Unitary Map

```math
|\Psi_i(t)\rangle =
e^{-iHt}
\left(
|\psi_i\rangle_M \otimes |0\rangle_F
\right)
```

```math
|\phi_{i,m}(t,b)\rangle =
\frac{
(I_M \otimes \langle b_m|)
|\Psi_i(t)\rangle
}{
\sqrt{p_{i,m}}
}
```

```math
p_{i,m}
=
\left\|
(I_M \otimes \langle b_m|)
|\Psi_i(t)\rangle
\right\|^2
```

### A4. Axis-Only vs Continuous

- Axis-only: interpretable `Z/X/Y` baseline.
- Continuous: Bloch-sphere generalization.
- Margin is small, so we do not claim overwhelming superiority.

### A5. Problem 3(c) Comparison

Use `source_code/solution/tables/problem3c_analysis_guided_improvement.csv`.

### A6. Seed Robustness

- 20 / 20 seeds pass the main adoption gate.
- Median \(\Delta D_{\mathrm{MMD}}\): `0.097056`.
- Median \(\Delta W_{1-F}\): `0.147983`.

### A7. Source Code and Reproduction

```powershell
python -m pytest
python submission/run_all.py --quick
python scripts/summarize_problem_3_seed_sweep.py
python scripts/summarize_problem_3_method_portfolio.py
```

### A8. Limitations

- No quantum advantage claim.
- No hardware advantage claim.
- No full trainable QuDDPM claim.
- No broad continuous-over-axis claim.
- Actor-critic is target-aware if mentioned.

### A9. IBM QPU Problem 3-b Mini Validation

- We submitted tiny `M+F` circuits to IBM Quantum / Qiskit Runtime.
- Mechanism: complement-qubit measurement-basis angle \(\beta\) changes \(p_{\mathrm{succ}}\) and the selected data distribution.
- Backend: `ibm_fez`.
- Job ids: `d91r6pmu9n7c73an9qgg`, `d91r71fccmks73d5nmg0`.
- Status: DONE.
- Runs: `2048` shots x `12` circuits, and `4096` shots x `20` circuits.
- Higher-shot aggregate:
  - beta `0.0000pi`: mean p(F=0) `0.881738`, selected entropy `1.375447`.
  - beta `0.2500pi`: mean p(F=0) `0.893164`, selected entropy `1.492915`.
  - beta `0.5000pi`: mean p(F=0) `0.661377`, selected entropy `1.581403`.
  - beta `0.7500pi`: mean p(F=0) `0.351270`, selected entropy `1.736465`.
- IBM QPU Problem 3-b mini validation is appendix hardware-execution evidence only. It tests tiny representative circuits and does not replace the state-vector benchmark.
- No hardware advantage claim.

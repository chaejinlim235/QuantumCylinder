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

### Slide 3. Problem 1: Random-Unitary Diffusion

- `S0` is clustered near `|00>`.
- Random-unitary layers rapidly move the ensemble away from `S0`.
- Haar reference: MMD `0.869583 +/- 0.024043`, Wasserstein `0.724439 +/- 0.021491`.
- Interpretation: strong scrambling / Haar-like plateau.

Figure: `source_code/solution/figures/fig2_random_unitary_haar_baseline.png`

Speaker note: "The Haar reference is not a target distribution. It is a calibration level for strong scrambling."

### Slide 4. Problem 2: Hamiltonian Projected Diffusion

- Data system `M` plus complement qubit `F`.
- Fixed Hamiltonian evolution followed by projection.
- Curves can fluctuate or partially saturate depending on the schedule.
- Resource proxy: random gate controls vs fixed Hamiltonian time and projection basis.

Figure: `source_code/solution/figures/problem_1_2_metric_aligned_comparison.png`

Speaker note: "The comparison is qualitative and control-aware, not a universal ranking."

### Slide 5. Problem 3(b): Measurement-Basis Trade-Off

- `M+F` evolves unitarily.
- Measuring `F` and post-selecting induces an effective non-unitary map on `M`.
- Axis-only `Z/X/Y` is a Pauli-basis baseline.
- Continuous Bloch-sphere basis is a controlled generalization.
- Main point: distance gain, success probability, and diversity retention must be reported together.

Table: `source_code/solution/tables/problem3b_measurement_basis_tradeoff.csv`

Speaker note: "The axis-only margin is small, so the claim is the trade-off analysis."

### Slide 6. Problem 3(c): Two-Way Post-Selection

- Based on 3-b, stronger contraction can improve distance metrics.
- Two-way Hamiltonian post-selection applies the projected denoising idea more strongly.
- Median MMD gain: `0.101374`.
- Median Wasserstein gain: `0.136426`.
- Median success probability: `0.227065`.
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
- MMD uses fidelity kernel.
- Wasserstein-type distance uses cost `1 - F`.

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
- Median MMD improvement: `0.097056`.
- Median Wasserstein improvement: `0.147983`.

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

### A9. IBM QPU Validation Path

- Optional small-circuit execution path through IBM Quantum / Qiskit Runtime.
- Uses tiny representative circuits, not full ensemble MMD/Wasserstein.
- Reports transpiled depth, two-qubit gate count, backend, and job id if submitted.
- Main claims remain the reproducible state-vector benchmark.
- No hardware advantage claim.
- Dry-run/transpilation path prepared; real QPU submission requires IBM credentials and queue availability.

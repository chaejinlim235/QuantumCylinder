# Problem 1/2 Circuit Validation

Owner: 김건우  
Reviewer:

## Hypothesis

Problem 1/2 baseline implementations should match the challenge conditions before adding a Problem 3 extension. In particular, the target ensemble, random-unitary diffusion, Hamiltonian projected diffusion, and resource/control proxies should be reproducible from the repository scripts.

## Setup

- Branch: `feat/problem-1-2-circuit-validation`
- Config: `configs/problem_1_2_baseline.json`
- Default implementation: Qiskit wrappers in `problem_1a_target_ensemble.py`, `problem_1c_random_unitary_diffusion.py`, and `problem_2_hamiltonian_projected_diffusion.py`
- Qiskit backend folder: `src/quantum_cylinder/implementations/qiskit/`
- Preserved NumPy/SciPy backend folder: `src/quantum_cylinder/implementations/numpy/`
- Backend folders are independent; this validation only checks the default Qiskit path.
- Ensemble size `N`: `80`
- Target width `sigma`: `0.10`
- Seed: `7`
- Random-unitary steps: `12`
- Hamiltonian time grid: `linspace(0, 4.0, 13)`
- Measurement basis: computational `Z`

## Condition Check

| Item | Required / intended condition | Current implementation | Judgment |
| --- | --- | --- | --- |
| Target ensemble | 2-qubit ensemble clustered around `|00>`, `N = 50-100`, default `sigma = 0.10` | `target_ensemble(n_samples=80, sigma=0.10, seed=7)` for baseline; each sample uses a Qiskit circuit applying local `Rz(delta_z) Ry(delta_y)` to `|00>` | Matches |
| Problem 1 random rotations | Random single-qubit rotations at each diffusion step | Per sample and per step, a Qiskit circuit applies `Rz Ry Rx`-equivalent operations with angles sampled uniformly from `[-pi, pi]` | Matches |
| Problem 1 entangler | 2-qubit entangler per diffusion step | One Qiskit `CZ` by default; `CX` is also available as an option | Matches |
| Problem 2 data/complement systems | 2-qubit data system `M` plus 1 complement qubit `F` | Full state is `kron(data_state, |0>)`, with qubit order `M0, M1, F` | Matches |
| Problem 2 Hamiltonian constants | `hx = 0.8090`, `hy = 0.9045`, `J = 1.0` | `three_qubit_hamiltonian(hx=0.8090, hy=0.9045, j_coupling=1.0)` | Matches |
| Problem 2 Hamiltonian structure | `sum_j (hx X_j + hy Y_j) + J sum_j X_j X_{j+1}` | Qiskit `SparsePauliOp` with 3 `X`, 3 `Y`, and 2 nearest-neighbor `XX` terms, total 8 operator terms | Matches |
| Projection method | Project complement qubit and keep the data-system state ensemble | Evolves `M + F`, projects complement in the selected basis, samples one outcome per input according to Born probabilities, and normalizes the projected 2-qubit state | Matches |
| Metrics | Fidelity-kernel MMD and cost `1 - F` Wasserstein-type distance | Both baselines use `distance_curve` with `mmd_fidelity` and `wasserstein_infidelity` | Matches |

## Resource Proxy

| Mechanism | Parameter | Single-qubit rotations | 2-qubit entanglers | Random controls | Fixed Hamiltonian terms | Fixed Hamiltonian parameters | Other control |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Random-unitary | step `k` | `6k` | `k` | `6k` | `0` | `0` | Per-layer random angles |
| Random-unitary final baseline | `k = 12` | `72` | `12` | `72` | `0` | `0` | Entangler `CZ` |
| Hamiltonian projected | time `t` | `0` | `0` | `0` | `8` | `3` | Fixed `H`, complement projection in `Z` |
| Hamiltonian projected final grid point | `t = 4.0` | `0` | `0` | `0` | `8` | `3` | Total evolution time `4.0` |

## Results

Commands:

```powershell
python scripts/problem_1a_generate_target_ensemble.py
python scripts/run_problem_1_2_baselines.py
python -m pytest
```

Observed results:

- `python scripts/problem_1a_generate_target_ensemble.py`: succeeded; generated 100-sample compatibility check around `|00>`.
- `python scripts/run_problem_1_2_baselines.py`: succeeded; wrote outputs to `results/problem_1_2_baseline/`.
- `python -m pytest`: 8 passed.
- Final random-unitary step `k = 12`: MMD `0.828093`, Wasserstein-type distance `0.686108`.
- Hamiltonian projected maximum MMD: `1.249244` at `t = 1.000000`.
- Hamiltonian projected maximum Wasserstein-type distance: `0.883968` at `t = 4.000000`.

## Interpretation

The current Problem 1/2 implementations satisfy the baseline conditions needed for extension work. The main resource contrast is clear: random-unitary diffusion uses increasing random circuit controls and entanglers as `k` grows, while Hamiltonian projected diffusion uses a fixed 3-parameter Hamiltonian with time and projection basis as the main controls.

## Next

- Use this validation note as the PR evidence for the Problem 1/2 baseline lock.
- For Problem 3, compare any extension against at least one baseline at the same metric definitions and report both distance behavior and resource/control trade-off.

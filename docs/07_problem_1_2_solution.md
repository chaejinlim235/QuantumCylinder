# Problem 1/2 Solution Note

This note records the baseline solution choices for Problems 1 and 2. Generated CSV/PNG outputs are kept under `results/problem_1_2_baseline/` and are not committed by default.

## Run

```powershell
python scripts/problem_1a_generate_target_ensemble.py
python scripts/run_problem_1_2_baselines.py
pytest
```

## Problem 1(a): Target Ensemble

Implementation:

- `src/quantum_cylinder/problem_1a_target_ensemble.py`
- Qiskit `QuantumCircuit` and `Statevector`
- Qiskit implementation: `src/quantum_cylinder/implementations/qiskit/problem_1a_target_ensemble.py`
- Preserved NumPy implementation: `src/quantum_cylinder/implementations/numpy/problem_1a_target_ensemble.py`
- The Qiskit and NumPy implementations are stored independently; no cross-backend parity contract is maintained.

Choices:

- `N = 80`
- `sigma = 0.10`
- seed `7`
- each sample is generated as `(Rz(delta_z) Ry(delta_y))` on both qubits, starting from `|00>`

This matches the requested two-qubit cluster around `|00>`.

## Problem 1(b): Metrics

Implementation:

- `src/quantum_cylinder/problem_1b_ensemble_metrics.py`

Metrics:

- fidelity: `F(psi, phi) = |<psi|phi>|^2`
- fidelity-kernel MMD, reported as `sqrt(MMD^2)`
- Wasserstein-type distance with pairwise cost `1 - F`

For equal-size ensembles, the Wasserstein-type distance is solved as a minimum average matching cost.

## Problem 1(c): Random-Unitary Diffusion

Implementation:

- `src/quantum_cylinder/problem_1c_random_unitary_diffusion.py`
- Qiskit `QuantumCircuit` and `Operator`
- Qiskit implementation: `src/quantum_cylinder/implementations/qiskit/problem_1c_random_unitary_diffusion.py`
- Preserved NumPy implementation: `src/quantum_cylinder/implementations/numpy/problem_1c_random_unitary_diffusion.py`
- The Qiskit and NumPy implementations are stored independently; no cross-backend parity contract is maintained.

Choices:

- 12 diffusion steps
- per step and per sample: random local `Rz Ry Rx` rotations on each qubit
- random angles sampled uniformly from `[-pi, pi]`
- one `CZ` entangler per step

Output:

- `results/problem_1_2_baseline/random_unitary_metrics.csv`
- `results/problem_1_2_baseline/distance_curves.png`

Reference run:

- final step `k = 12`
- MMD to `S0`: `0.828093`
- Wasserstein-type distance to `S0`: `0.686108`

## Problem 2: Hamiltonian Projected Diffusion

Implementation:

- `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py`
- Qiskit `SparsePauliOp`, `Operator`, and `Statevector`
- Qiskit implementation: `src/quantum_cylinder/implementations/qiskit/problem_2_hamiltonian_projected_diffusion.py`
- Preserved NumPy/SciPy implementation: `src/quantum_cylinder/implementations/numpy/problem_2_hamiltonian_projected_diffusion.py`
- The Qiskit and NumPy/SciPy implementations are stored independently; no cross-backend parity contract is maintained.

Choices:

- data system `M`: the same two-qubit ensemble from Problem 1
- complement system `F`: one qubit initialized as `|0>`
- Hamiltonian:

```text
H = sum_j (hx X_j + hy Y_j) + J sum_j X_j X_{j+1}
hx = 0.8090, hy = 0.9045, J = 1.0
```

- time grid: `linspace(0, 4.0, 13)`
- default measurement basis: `Z`
- one projected outcome is sampled for each input state so the ensemble size stays fixed

Output:

- `results/problem_1_2_baseline/hamiltonian_metrics.csv`
- `results/problem_1_2_baseline/distance_curves.png`

Reference run:

- maximum MMD: `1.249244` at `t = 1.000000`
- maximum Wasserstein-type distance: `0.883968` at `t = 4.000000`

## Resource / Control Proxy

Random-unitary proxy:

- number of diffusion layers
- number of single-qubit random rotations
- number of two-qubit entanglers
- number of random control parameters

Hamiltonian projected proxy:

- total Hamiltonian evolution time
- 8 fixed Hamiltonian operator terms
- 3 fixed Hamiltonian coefficients: `hx`, `hy`, `J`
- measurement basis

Output:

- `results/problem_1_2_baseline/resource_proxies.csv`

## Interpretation

Problem 1 provides a direct random-circuit scrambling baseline. As the layer count increases, the original `|00>`-centered cluster should move away from `S0` under both distance metrics.

Problem 2 uses a fixed Hamiltonian and complement-qubit projection. Its distance curve may increase, fluctuate, or saturate as time varies. The important comparison is that both mechanisms are evaluated from the same initial ensemble with the same metrics, while their control/resource structures differ.

# QuantumCylinder

2026 양자정보경진대회 Technical Challenge, Quantum Machine Learning 지정문제 3번을 위한 팀 저장소입니다..
팀명은 **양자실린더 / QuantumCylinder**입니다. 대회 목표는 수상권 이상이며, 가능하면 우승까지 목표로 합니다. 이 저장소는 그 목표를 위해 재현 가능한 실험 코드와 문서를 관리합니다.

## Project Scope

이 저장소는 지정문제 3번의 세 요구를 작은 state-vector 실험으로 재현하고 비교합니다.

1. **Problem 1 - Random-unitary scrambling**
   - `|00>` 주변의 2-qubit target ensemble 생성
   - random single-qubit rotations + entangler 기반 forward diffusion
   - fidelity-based MMD와 infidelity-cost Wasserstein-type distance 계산

2. **Problem 2 - Hamiltonian projected diffusion**
   - 2-qubit data system에 1 complement qubit 추가
   - 고정 Hamiltonian time evolution 후 complement qubit projection
   - Problem 1과 같은 metric으로 diffusion curve 비교

3. **Problem 3 - Further extension**
   - toy reverse/denoising step
   - measurement basis, schedule, Hamiltonian parameter, noise model 등 통제된 변형
   - baseline 대비 개선점과 손실을 함께 정리

## Tech Stack

- Python 3.11+
- NumPy, SciPy
- Matplotlib
- pytest

현재 baseline은 Qiskit/PennyLane 없이 실행됩니다. 외부 양자 SDK는 hardware-aware 분석이나 transpilation이 필요할 때 추가합니다.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/run_problem_1_2_baselines.py
pytest
```

기본 결과는 `results/problem_1_2_baseline/`에 생성됩니다. `results/`의 CSV/PNG/JSON은 기본적으로 Git에 커밋하지 않습니다.

## Code Map

문제별 실행 파일과 핵심 구현 파일은 아래와 같습니다.

| Problem | Purpose | Entry point | Core implementation |
| --- | --- | --- | --- |
| 1(a) | target ensemble 생성 | `scripts/problem_1a_generate_target_ensemble.py` | `src/quantum_cylinder/problem_1a_target_ensemble.py` |
| 1(b) | fidelity, MMD, Wasserstein metric | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_1b_ensemble_metrics.py` |
| 1(c) | random-unitary diffusion | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_1c_random_unitary_diffusion.py` |
| 2 | Hamiltonian projected diffusion | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py` |
| 1/2 common | baseline curve, CSV, plot 생성 | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/experiment_curves.py` |
| common | small quantum linear algebra utilities | - | `src/quantum_cylinder/quantum_ops.py` |

## Repository Structure

```text
.
|-- configs/
|   `-- problem_1_2_baseline.json
|-- data/
|   |-- raw/                  # private/raw files. Do not commit contents.
|   `-- processed/
|-- docs/
|   |-- 00_problem_brief.md
|   |-- 01_team_roles.md
|   |-- 02_roadmap.md
|   |-- 03_experiment_protocol.md
|   |-- 04_extension_ideas.md
|   `-- experiments/
|-- notebooks/                # exploration only; reusable logic belongs in src/
|-- results/                  # generated experiment outputs; ignored by default
|-- scripts/
|   |-- problem_1a_generate_target_ensemble.py
|   `-- run_problem_1_2_baselines.py
|-- src/quantum_cylinder/
|   |-- quantum_ops.py
|   |-- problem_1a_target_ensemble.py
|   |-- problem_1b_ensemble_metrics.py
|   |-- problem_1c_random_unitary_diffusion.py
|   |-- problem_2_hamiltonian_projected_diffusion.py
|   `-- experiment_curves.py
`-- tests/
    `-- test_problem_1_2_baselines.py
```

## Team Roles

| Member | Primary responsibility | Background fit | Near-term output |
| --- | --- | --- | --- |
| 임채진 | 연구 방향, 물리적 해석, 발표 구조 | 물리 데이터 해석과 회귀 모델링 경험을 바탕으로 diffusion behavior를 해석 | 문제 해석, baseline 결과 해석, 발표 흐름 |
| 김건우 | 양자 회로 구현, resource proxy, hardware-aware 비교 | 양자 터널링 시뮬레이션과 모델 압축 경험을 회로 깊이/게이트 수 분석에 연결 | Problem 1/2 회로 구현 검증, gate/depth proxy 표 |
| 김승빈 | 실험 파이프라인, 로그 관리, 시각화 | 생성 모델 및 3D reconstruction 파이프라인 경험을 반복 실험 관리에 활용 | 재현 가능한 실행 스크립트, plot/CSV 관리 |
| 한지후 | metric, loss, 수리 모델링, Problem 3 extension | ML systems, parameter-efficient adaptation, diffusion/loss 분석 경험을 metric과 denoising 설계에 활용 | MMD/Wasserstein 검증, denoising 및 trade-off 분석 |

세부 역할과 리뷰 구조는 `docs/01_team_roles.md`에 정리합니다.

대회 기간 실행 계획과 개인별 작업 브랜치는 `docs/05_hackathon_execution_plan.md`에 정리합니다.

논문 해석 범위를 줄이기 위한 triage 기준은 `docs/06_paper_triage.md`에 정리합니다.

Problem 1/2 baseline 풀이와 구현 선택은 `docs/07_problem_1_2_solution.md`에 정리합니다.

로컬 테스트와 GitHub Actions CI 사용법은 `docs/08_test_environment.md`에 정리합니다.

Qiskit은 필수 구현이 아니라 회로/resource 검증용 선택 레이어로 사용하며, 기준은 `docs/09_qiskit_validation_layer.md`에 정리합니다.

## Git Rules

### Branch naming

브랜치명에는 개인 이름, 학번, GitHub username을 넣지 않습니다.

```text
<type>/<short-topic>
```

Allowed `type`:

- `feat`: 기능 또는 실험 코드
- `fix`: 버그 수정
- `exp`: 실험 설정 또는 실험 실행
- `docs`: 문서
- `refactor`: 동작 변경 없는 구조 변경
- `test`: 테스트
- `chore`: 설정 및 관리 작업

Examples:

```text
docs/readme-conventions
feat/problem-1-random-unitary
exp/projection-basis-sweep
fix/hamiltonian-projection
```

### Pull requests

- 모든 변경은 PR로 관리합니다.
- conflict가 없고 검증이 통과하면 merge합니다.
- PR 본문에는 목적, 변경 사항, 검증 명령, 결과 또는 판단을 적습니다.
- 담당자는 브랜치명이 아니라 issue, PR 본문, 실험 로그에 적습니다.

### Commit messages

```text
<type>: <summary>
```

Examples:

```text
docs: update readme conventions
feat: add problem 1 random unitary diffusion
exp: run projection basis sweep
fix: normalize projected states
```

## File Naming Rules

문제 풀이와 직접 연결되는 코드는 파일명에 문제 번호를 넣습니다.

```text
src/quantum_cylinder/problem_<n><subproblem>_<topic>.py
scripts/problem_<n><subproblem>_<action>.py
scripts/run_problem_<n>_<m>_<topic>.py
configs/problem_<n>_<m>_<topic>.json
```

Examples:

```text
src/quantum_cylinder/problem_1a_target_ensemble.py
src/quantum_cylinder/problem_1b_ensemble_metrics.py
src/quantum_cylinder/problem_1c_random_unitary_diffusion.py
src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py
scripts/problem_1a_generate_target_ensemble.py
scripts/run_problem_1_2_baselines.py
configs/problem_1_2_baseline.json
```

Common utilities that are not specific to one problem may use descriptive names such as `quantum_ops.py` or `experiment_curves.py`.

## Reproducibility Rules

각 실험은 다음 정보를 남깁니다.

- 실행 명령
- config path
- seed
- sample size `N`
- `sigma`
- diffusion steps 또는 time grid
- measurement basis
- metric 정의
- 결과 경로
- baseline 대비 해석

표준 metric:

- `F(psi, phi) = |<psi|phi>|^2`
- fidelity-kernel MMD
- cost `1 - F` 기반 Wasserstein-type distance

표준 resource/control proxy:

- random-unitary: layer 수, random rotation 수, 2-qubit entangler 수
- Hamiltonian projected diffusion: total evolution time, fixed Hamiltonian term 수, complement qubit 수, measurement basis

## Data and Privacy

- 신청서 원문, 전화번호, 이메일, 서명, 개인정보가 포함된 파일은 커밋하지 않습니다.
- 원본 문제 PDF나 private 자료는 필요 시 로컬 `data/raw/`에만 둡니다.
- 외부에 공유 가능한 요약과 실험 기록만 `docs/`에 정리합니다.

## References

- B. Zhang et al., "Generative Quantum Machine Learning via Denoising Diffusion Probabilistic Models", PRL 132, 100602 (2024), arXiv:2310.05866: <https://arxiv.org/abs/2310.05866>
- Q. H. Tran et al., "Learning Quantum Data Distribution via Chaotic Quantum Diffusion Model", arXiv:2602.22061: <https://arxiv.org/abs/2602.22061>

## LLM Development Guide

```text
You are helping the QuantumCylinder team build a reproducible solution for the 2026 Quantum Information Hackathon.

Follow these constraints:

1. Keep the repository readable to external reviewers.
2. Keep Problem 1/2 baselines reproducible before adding Problem 3 extensions.
3. Use branch names in the form <type>/<short-topic>; do not include personal names.
4. Put problem-specific code in files named problem_<n><subproblem>_<topic>.py when a subproblem exists.
5. Put reusable code under src/quantum_cylinder/.
6. Put executable experiment scripts under scripts/.
7. Keep generated results and private/raw files out of Git by default.
8. Compare new ideas against at least one baseline with the same metrics.
9. State both improvement and trade-off for experimental claims.
10. Run pytest when code changes are made.
```

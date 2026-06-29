# QuantumCylinder

2026 양자정보경진대회 Technical Challenge, Quantum Machine Learning 지정문제 3번을 위한 팀 저장소입니다.
팀명은 **양자실린더 / QuantumCylinder**입니다. 대회 목표는 수상권 이상이며, 가능하면 우승까지 목표로 합니다. 이 저장소는 그 목표를 위해 재현 가능한 실험 코드와 문서를 관리합니다.

## Current Progress

팀 운영 기준은 "한지후가 핵심 코드 구현과 통합을 맡고, 나머지 팀원은 해석, 검증, 환경 안정화, 결과 정리에 집중한다"입니다.

| Area | Status | Owner | Next action |
| --- | --- | --- | --- |
| Repository setup | Done | 한지후 | PR 단위 변경과 자동 CI 유지 |
| Problem 1 baseline | Locked | 한지후 | 3번 extension의 비교 기준으로 유지 |
| Problem 2 baseline | Locked | 한지후 | comparable-strength resource match 표를 보고서에 반영 |
| Local tests | Passing | 한지후 | 모든 코드 PR 전 `pytest` 실행 |
| Qiskit validation layer | Available | 김건우 | `problem_1_qiskit_resource_check.py` 기준으로 gate/depth 표 정리 |
| Paper/problem interpretation | In progress | 임채진 | 발표에 쓸 문제 정의와 핵심 가정만 추출 |
| Python environment recovery | In progress | 김승빈 | 환경 복구 후 baseline 실행 로그와 결과 파일 확인 |
| Problem 3 extension | Ready to start | 한지후 | measurement-basis sweep + shallow denoising 중 최소 구현 선택 |
| Final report/story | Draft started | 임채진 | `docs/experiments/2026-06-29_final_report_storyline.md`를 결과와 맞춰 갱신 |

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
- Qiskit optional

현재 baseline은 NumPy/SciPy state-vector 방식으로 실행됩니다. Qiskit은 필수 구현이 아니라 회로 표현, gate/depth, resource proxy 검증용 선택 레이어로 사용합니다.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/run_problem_1_2_baselines.py
pytest
```

기본 결과는 `results/problem_1_2_baseline/`에 생성됩니다. `results/`의 CSV/PNG/JSON은 기본적으로 Git에 커밋하지 않습니다.

Qiskit 검증이 필요한 팀원은 아래 명령을 추가로 실행합니다.

```powershell
pip install -e ".[qiskit]"
python scripts/problem_1_qiskit_resource_check.py
```

## Code Map

문제별 실행 파일과 핵심 구현 파일은 아래와 같습니다.

| Problem | Purpose | Entry point | Core implementation |
| --- | --- | --- | --- |
| 1(a) | target ensemble 생성 | `scripts/problem_1a_generate_target_ensemble.py` | `src/quantum_cylinder/problem_1a_target_ensemble.py` |
| 1(b) | fidelity, MMD, Wasserstein metric | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_1b_ensemble_metrics.py` |
| 1(c) | random-unitary diffusion | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_1c_random_unitary_diffusion.py` |
| 2 | Hamiltonian projected diffusion | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/problem_2_hamiltonian_projected_diffusion.py` |
| 1/2 common | baseline curve, CSV, plot 생성 | `scripts/run_problem_1_2_baselines.py` | `src/quantum_cylinder/experiment_curves.py` |
| Qiskit validation | circuit resource proxy | `scripts/problem_1_qiskit_resource_check.py` | Qiskit `QuantumCircuit` |
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
|   |-- 05_hackathon_execution_plan.md
|   |-- 06_paper_triage.md
|   |-- 07_problem_1_2_solution.md
|   |-- 08_test_environment.md
|   |-- 09_qiskit_validation_layer.md
|   `-- 10_llm_development_guide.md
|-- notebooks/                # exploration only; reusable logic belongs in src/
|-- results/                  # generated experiment outputs; ignored by default
|-- scripts/
|   |-- problem_1a_generate_target_ensemble.py
|   |-- problem_1_qiskit_resource_check.py
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
| 한지후 | 핵심 코드 구현, 통합, Problem 3 extension | MVP 해커톤 경험을 일정 관리와 빠른 구현에 활용하고, 양자물리 해석은 팀 검증을 받음 | Problem 1/2 baseline 유지, Problem 3 최소 구현, PR 통합 |
| 김건우 | Qiskit 적용, 회로/resource 검증, 논문 확인 | 양자 관련 코드와 모델 구현 경험을 gate/depth 분석과 문제 조건 검증에 연결 | Qiskit resource 표, NumPy 구현과 회로 관점 차이 정리 |
| 임채진 | 지정문제 해석, 논문 핵심 추출, 발표 흐름 | 문제와 논문을 읽고 팀이 주장할 수 있는 범위를 정리 | 문제 정의, baseline 해석, 보고서/발표 목차 |
| 김승빈 | 개발 환경 복구, 실행 재현, 결과 정리 | 개발 경험을 환경 문제 해결과 반복 실행 로그 관리에 활용 | 로컬 환경 복구, baseline 실행 로그, plot/CSV 확인 |

세부 역할과 리뷰 구조는 `docs/01_team_roles.md`에 정리합니다.

대회 기간 실행 계획과 개인별 작업 브랜치는 `docs/05_hackathon_execution_plan.md`에 정리합니다.

논문 해석 범위를 줄이기 위한 triage 기준은 `docs/06_paper_triage.md`에 정리합니다.

Problem 1/2 baseline 풀이와 구현 선택은 `docs/07_problem_1_2_solution.md`에 정리합니다.

로컬 테스트와 GitHub Actions CI 사용법은 `docs/08_test_environment.md`에 정리합니다.

Qiskit은 필수 구현이 아니라 회로/resource 검증용 선택 레이어로 사용하며, 기준은 `docs/09_qiskit_validation_layer.md`에 정리합니다.

팀원별 LLM 사용 프롬프트와 작업 규칙은 `docs/10_llm_development_guide.md`에 정리합니다.

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
너는 QuantumCylinder 팀의 2026 양자정보경진대회 작업을 돕는 LLM 개발 파트너다.

현재 운영 원칙:
1. 한지후가 핵심 코드 구현과 통합을 담당한다.
2. 김건우는 Qiskit/resource 검증과 논문 확인을 담당한다.
3. 임채진은 지정문제와 논문 해석, 최종 보고서 흐름을 담당한다.
4. 김승빈은 Python 환경 복구, 실행 재현, 결과 파일 확인을 담당한다.
5. Problem 1/2 baseline을 깨지 말고, Problem 3 extension은 baseline과 같은 metric으로 비교한다.
6. 브랜치명에는 개인 이름이나 GitHub username을 넣지 않는다.
7. 코드 변경 후에는 `python -m pytest`를 실행한다.
8. 주장할 때는 개선점과 trade-off를 함께 적는다.
9. 모르는 물리 해석은 단정하지 말고 검증 질문으로 남긴다.
```

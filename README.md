# QuantumCylinder

2026 양자정보경진대회 Technical Challenge, Quantum Machine Learning 지정문제 3번을 위한 팀 저장소입니다.

팀명은 **양자실린더 / QuantumCylinder**입니다. 이 프로젝트의 목표는 명확합니다.

- 1차 목표: **2026 양자정보경진대회 우승**
- 최소 목표: **수상권 진입**
- 구현 목표: Problem 1/2 baseline을 빠르게 재현하고, Problem 3에서 하드웨어 친화적 양자 확산 아이디어를 작지만 정량적으로 검증한다.

이 저장소는 단순 코드 보관소가 아니라, 팀원 모두가 같은 실험 조건과 같은 판단 기준으로 움직이기 위한 대회 운영 레포지토리입니다.

---

## 프로젝트 핵심 전략

올해 문제의 핵심은 거대한 Quantum DDPM 전체를 그대로 구현하는 것이 아니라, 작은 시스템에서 양자 확산의 원리를 재현하고 두 diffusion mechanism의 trade-off를 설득력 있게 비교하는 것입니다.

1. **Problem 1 재현**
   - 2-qubit target ensemble `S0` 생성
   - random-unitary scrambling trajectory 구현
   - fidelity-based MMD와 Wasserstein-type distance 계산

2. **Problem 2 재현**
   - 2-qubit data system + 1 complement qubit 구성
   - fixed Hamiltonian time evolution
   - projected ensemble 기반 diffusion curve 분석

3. **Problem 3 확장**
   - toy reverse/denoising step 제시
   - diffusion setting을 통제된 방식으로 수정
   - baseline 대비 개선점과 희생점을 동시에 정량화

최종 발표의 중심 질문은 다음입니다.

> 양자 확산은 얼마나 적은 control로 충분히 잘 퍼지고, 얼마나 싸게 되돌릴 수 있는가?

---

## 기술 스택

- **Language**: Python 3.11+
- **Core simulation**: NumPy, SciPy state-vector simulation
- **Metrics**: fidelity, MMD, Wasserstein-type distance
- **Visualization**: Matplotlib
- **Testing**: pytest
- **Optional future tools**: Qiskit, PennyLane, IBM Fake Backend

현재 baseline은 외부 양자 SDK 없이 실행 가능하게 유지합니다. Qiskit/PennyLane은 필요성이 명확할 때만 추가합니다.

---

## 빠른 시작

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/run_baselines.py
pytest
```

기본 실행 결과는 `results/baseline/`에 생성됩니다.

생성된 CSV/PNG/JSON 결과물은 재현 가능해야 하지만 기본적으로 Git에 커밋하지 않습니다.

---

## 프로젝트 구조

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── experiment.yml
│   └── pull_request_template.md
│
├── configs/
│   └── baseline.json
│
├── data/
│   ├── raw/                  # 원본/개인정보 포함 가능 파일. Git 커밋 금지
│   └── processed/            # 전처리 산출물
│
├── docs/
│   ├── 00_problem_brief.md
│   ├── 01_team_roles.md
│   ├── 02_roadmap.md
│   ├── 03_experiment_protocol.md
│   ├── 04_extension_ideas.md
│   └── experiments/          # 실험 로그
│
├── notebooks/                # 탐색용 노트북. 핵심 로직은 src로 이동
├── results/                  # 실험 산출물. 기본적으로 Git 커밋 금지
│
├── scripts/
│   └── run_baselines.py
│
├── src/
│   └── quantum_cylinder/
│       ├── states.py         # 상태 생성, gate, normalization
│       ├── metrics.py        # fidelity, MMD, Wasserstein
│       ├── diffusion.py      # random-unitary, Hamiltonian diffusion
│       └── experiments.py    # 실험 curve/resource proxy helper
│
├── tests/
│   └── test_baselines.py
│
├── 1.py                      # 기존 Problem 1-(a) 호환 entry point
├── pyproject.toml
└── requirements.txt
```

---

## 팀 역할

| 팀원 | 주 담당 | 첫 산출물 |
| --- | --- | --- |
| 임채진 | 전체 연구 방향, 물리/정보이론 해석, 발표 논리 | 문제 해석과 final story line |
| 김건우 | 양자 회로 구현, random-unitary/Hamiltonian baseline, resource proxy | Problem 1/2 baseline 검증 |
| 김승빈 | 실험 파이프라인, 로그 관리, 시각화, 발표용 figure | 재현 가능한 실행 스크립트와 plot |
| 한지후 | 수리 모델링, MMD/Wasserstein/loss 분석, Problem 3 extension 설계 | metric 검증과 denoising/loss 후보 비교 |

역할은 책임 영역을 뜻합니다. 모든 PR은 최소 1명의 리뷰 관점을 거칩니다.

---

## Git 운영 규칙

### 기본 브랜치

- `main`
  - 항상 실행 가능한 상태를 유지합니다.
  - 직접 작업하지 않습니다.
  - 모든 변경은 PR을 통해 들어옵니다.

### 브랜치 이름 규칙

브랜치 이름은 반드시 다음 형식을 사용합니다.

```text
<type>/<owner>/<short-topic>
```

허용되는 `type`:

- `feat`: 새 기능, 새 실험 코드
- `fix`: 버그 수정
- `exp`: 실험 실행 또는 실험 설정 추가
- `docs`: 문서 수정
- `refactor`: 동작 변경 없는 구조 정리
- `test`: 테스트 추가 또는 수정
- `chore`: 설정, 템플릿, 기타 관리 작업

`owner`는 작업 주도자를 소문자 영문으로 씁니다.

```text
docs/jihu/readme-conventions
feat/geonwoo/random-unitary-baseline
exp/seungbin/projection-basis-sweep
fix/chaejin/hamiltonian-projection
```

규칙:

- 소문자 영어, 숫자, hyphen만 사용합니다.
- 공백, 한글, underscore는 브랜치명에 쓰지 않습니다.
- 한 브랜치는 하나의 목적만 가집니다.

### PR 규칙

PR 제목은 다음 형식을 사용합니다.

```text
[<type>] <short summary>
```

예시:

```text
[docs] tighten README conventions
[feat] implement random-unitary distance curve
[exp] compare projection basis sweep
```

PR 본문에는 반드시 다음을 적습니다.

- 목적: 왜 필요한 변경인가
- 변경 사항: 무엇이 바뀌었는가
- 검증: 어떤 명령을 실행했는가
- 결과: 실험 PR이면 핵심 수치 또는 결과 파일 경로
- 판단: baseline 대비 좋아진 점과 잃은 점

Conflict가 없고 테스트가 통과하면 PR은 merge합니다. 연구 실험 PR도 실패 결과가 의미 있으면 merge할 수 있지만, 실패 이유와 다음 액션을 문서에 남겨야 합니다.

### 커밋 메시지 규칙

커밋 메시지는 다음 형식을 권장합니다.

```text
<type>: <summary>
```

예시:

```text
docs: tighten project conventions
feat: add fidelity mmd metric
exp: run hamiltonian z basis baseline
fix: normalize projected states
```

---

## 파일 이름 규칙

### 공통 규칙

- 파일명과 디렉터리명은 기본적으로 **소문자 영어 + 숫자 + underscore**를 사용합니다.
- Python 모듈은 `snake_case.py`를 사용합니다.
- 실험 설정은 `configs/<experiment_name>.json`에 둡니다.
- 실험 로그는 `docs/experiments/YYYY-MM-DD_short_name.md` 형식을 사용합니다.
- 결과 디렉터리는 `results/<experiment_name>/` 형식을 사용합니다.
- 개인정보가 들어간 파일은 저장소에 넣지 않습니다.

### 허용 예시

```text
src/quantum_cylinder/random_unitary.py
configs/projection_basis_sweep.json
docs/experiments/2026-06-29_projection_basis_sweep.md
results/projection_basis_sweep/
notebooks/2026-06-29_metric_sanity_check.ipynb
```

### 금지 예시

```text
최종실험.py
new test.py
ExperimentFinalFinal.ipynb
result(1).csv
chaejin_private_application.pdf
```

### Python 코드 네이밍

- 함수/변수: `snake_case`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`
- private helper: `_helper_name`
- 실험 seed, sample size, sigma 등은 config 또는 함수 인자로 노출합니다.

---

## 실험 재현성 규칙

모든 실험은 다음 정보를 남겨야 합니다.

- 실험 목적
- 실행 명령
- config 파일 경로
- seed
- sample size `N`
- `sigma`
- diffusion steps 또는 time grid
- measurement basis
- metric 정의
- 결과 파일 경로
- 해석과 다음 액션

표준 metric:

- `F(psi, phi) = |<psi|phi>|^2`
- fidelity-kernel MMD
- cost `1 - F` 기반 Wasserstein-type distance

표준 resource/control proxy:

- random-unitary: layer 수, random rotation 수, 2-qubit entangler 수
- Hamiltonian diffusion: total evolution time, fixed Hamiltonian term 수, complement qubit 수, measurement basis 수

---

## 데이터 및 개인정보 규칙

- 신청서 원문, 전화번호, 이메일, 서명, 개인정보가 담긴 PDF는 Git에 커밋하지 않습니다.
- 원본 문제 PDF가 필요하면 로컬 `data/raw/`에 둘 수 있지만, Git에는 올리지 않습니다.
- 외부에 공유 가능한 내용만 `docs/`에 정리합니다.
- 결과물에 개인정보가 포함될 가능성이 있으면 PR에 올리기 전에 제거합니다.

---

## 현재 baseline

현재 구현은 다음을 제공합니다.

- 2-qubit target ensemble 생성
- fidelity matrix 계산
- fidelity-based MMD
- infidelity cost 기반 Wasserstein-type distance
- random-unitary forward diffusion trajectory
- 3-qubit Hamiltonian evolution + complement qubit projection diffusion
- baseline metric CSV와 distance curve plot 생성

실행:

```powershell
python scripts/run_baselines.py
```

검증:

```powershell
pytest
```

---

## 참고문헌

- B. Zhang et al., "Generative Quantum Machine Learning via Denoising Diffusion Probabilistic Models", PRL 132, 100602 (2024), arXiv:2310.05866: <https://arxiv.org/abs/2310.05866>
- Q. H. Tran et al., "Learning Quantum Data Distribution via Chaotic Quantum Diffusion Model", arXiv:2602.22061: <https://arxiv.org/abs/2602.22061>

---

## LLM용 개발 가이드

아래 조건을 유지하면서 코드를 작성하거나 수정합니다.

```text
너는 QuantumCylinder 팀의 연구 개발 파트너다.

프로젝트 조건은 다음과 같다.

1. 목표는 2026 양자정보경진대회 우승이며, 최소 목표는 수상이다.
2. Problem 1/2 baseline 재현성과 Problem 3 extension의 정량적 설득력이 가장 중요하다.
3. main 브랜치는 항상 실행 가능해야 하며, 모든 변경은 PR 단위로 관리한다.
4. 브랜치명은 <type>/<owner>/<short-topic> 형식을 따른다.
5. 파일명은 소문자 영어, 숫자, underscore 중심으로 통일한다.
6. Python 모듈은 snake_case.py를 사용한다.
7. 실험 코드는 scripts/에, 재사용 로직은 src/quantum_cylinder/에 둔다.
8. 탐색용 노트북에 핵심 로직을 방치하지 말고 src/로 옮긴다.
9. 실험은 seed, config, metric, 결과 경로가 남아야 한다.
10. 결과 CSV/PNG/JSON과 raw/private 파일은 기본적으로 Git에 커밋하지 않는다.
11. 개인정보가 담긴 신청서, 연락처, 이메일, 서명 파일은 절대 커밋하지 않는다.
12. 새 metric이나 diffusion 변형은 baseline과 같은 조건에서 비교한다.
13. 개선 주장은 반드시 좋아진 점과 희생한 점을 함께 설명한다.
14. 테스트가 가능한 로직은 pytest로 검증한다.
15. 기존 문서와 네이밍 규칙을 우선한다.

이 조건을 항상 유지하면서 작업하라.
```

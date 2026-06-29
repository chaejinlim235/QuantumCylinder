# QuantumCylinder

2026 양자정보경진대회 Technical Challenge, Quantum Machine Learning 지정문제 3번을 위한 팀 저장소입니다.

팀명은 **양자실린더 / QuantumCylinder**이고, 1/2번 baseline을 빠르게 재현한 뒤 3번에서 하드웨어 친화적 양자 확산 엔진을 작게라도 검증하는 것을 목표로 합니다.

## 문제 해석

올해 문제의 핵심은 대형 QuDDPM 전체를 구현하는 것이 아니라 다음 흐름을 설득력 있게 보이는 데 있습니다.

1. Random-unitary scrambling 기반 quantum diffusion을 재현한다.
2. Hamiltonian time evolution + projected ensemble 기반 diffusion을 같은 초기 앙상블에서 비교한다.
3. 두 baseline의 diffusion quality와 resource/control cost trade-off를 근거로, 작은 확장 아이디어를 실험한다.

참고문헌:

- B. Zhang et al., "Generative Quantum Machine Learning via Denoising Diffusion Probabilistic Models", PRL 132, 100602 (2024), arXiv:2310.05866: <https://arxiv.org/abs/2310.05866>
- Q. H. Tran et al., "Learning Quantum Data Distribution via Chaotic Quantum Diffusion Model", arXiv:2602.22061: <https://arxiv.org/abs/2602.22061>

## 빠른 시작

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/run_baselines.py
pytest
```

실험 결과는 기본적으로 `results/baseline/`에 생성됩니다. 생성물은 재현 가능해야 하지만 Git에는 올리지 않는 설정입니다.

## 저장소 구조

```text
.
├── .github/                 # PR/Issue 템플릿
├── configs/                 # 실험 설정
├── data/                    # raw/private 데이터는 Git 제외
├── docs/                    # 문제 해석, 역할, 로드맵, 실험 규약
├── notebooks/               # 탐색용 노트북
├── results/                 # 생성 결과물
├── scripts/                 # 실행 스크립트
├── src/quantum_cylinder/    # 재사용 가능한 실험 코드
└── tests/                   # 최소 검증 테스트
```

## 팀 운영 원칙

- `main`은 항상 실행 가능한 상태로 유지합니다.
- 새 실험은 issue 또는 `docs/03_experiment_protocol.md`의 실험 로그 규칙에 맞춰 시작합니다.
- PR에는 실험 목적, 설정, 결과 파일 경로, 판단을 반드시 적습니다.
- 신청서 원문, 전화번호, 이메일 등 개인정보가 담긴 파일은 저장소에 커밋하지 않습니다.

## 현재 baseline

현재 코드는 외부 양자 SDK 없이 NumPy/SciPy state-vector 시뮬레이션으로 다음을 제공합니다.

- 2-qubit target ensemble 생성
- fidelity-based MMD
- infidelity cost 기반 Wasserstein-type distance
- random unitary forward diffusion trajectory
- 3-qubit Hamiltonian evolution + complement qubit projection diffusion
- 비교 plot/CSV 생성

다음 단계는 `docs/04_extension_ideas.md`에서 하나를 골라 작은 실험으로 3번 답안의 중심축을 만드는 것입니다.

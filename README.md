# QuantumCylinder

QuantumCylinder는 2026 양자정보경진대회 지정문제 3번 풀이를 위해 만든 해커톤
프로젝트입니다. 이 저장소는 최종 제출물, 실험 코드, 결과표, 발표자료, 재현
명령을 보존하기 위한 아카이브입니다.

한 문장으로 말하면, 이 프로젝트는 random-unitary diffusion과 Hamiltonian
projected diffusion을 같은 fidelity 기반 MMD/Wasserstein-type metric으로
비교하고, measurement-induced post-selection을 denoising proxy로 보았을 때
recoverability, post-selection success probability, diversity retention 사이의
trade-off를 분석한 작업입니다.

## Archive Status

- 이 저장소는 해커톤 제출 당시의 연구 흐름과 산출물을 보존하기 위한 저장소입니다.
- 최종 judge-facing 자료는 `submission/usb_package/` 아래에 모았습니다.
- 발표 PDF와 보조 zip 자료는 compact archive 구조에서
  `submission/usb_package_supporting_materials/` 아래에 둘 수 있습니다.
- 실험과 정량 결과는 state-vector simulation을 중심으로 재현되도록 구성했습니다.
- IBM Cloud/QPU 자료는 작은 representative circuit의 hardware-execution
  validation입니다. hardware advantage claim이 아닙니다.
- 이 저장소는 full trainable QuDDPM, quantum advantage, hardware advantage를
  주장하지 않습니다.

## What We Built

### Problem 1: Random-Unitary Scrambling

`|00>` 근처의 2-qubit target ensemble `S0`를 만들고, pure-state fidelity를
기반으로 두 가지 ensemble distance를 계산했습니다.

- fidelity-kernel MMD
- cost `1 - F` 기반 Wasserstein-type distance
- random single-qubit rotations와 entangling operation을 이용한 diffusion
  trajectory
- Haar-random ensemble reference와의 비교

핵심 해석은 random-unitary diffusion이 초기 cluster structure를 빠르게 무너뜨려
strong-scrambling/Haar-like reference level 근처로 이동한다는 것입니다.

### Problem 2: Hamiltonian Projected Diffusion

Problem 1의 2-qubit data system `M`에 complement qubit `F`를 붙여 3-qubit
system을 만들고, 고정 Hamiltonian으로 time evolution을 수행한 뒤 complement
qubit을 projection해 data ensemble을 얻었습니다.

```text
H = sum_j (hx X_j + hy Y_j) + J sum_j X_j X_{j+1}
hx = 0.8090, hy = 0.9045, J = 1.0
```

이 파트의 목적은 random gate-level control을 쓰는 방식과 fixed Hamiltonian,
evolution time, projection choice를 control knob으로 쓰는 방식을 같은 metric
위에서 비교하는 것이었습니다.

### Problem 3: Measurement-Induced Denoising

Problem 3에서는 complement qubit measurement와 post-selection을 denoising
proxy로 사용했습니다. 전체 `M+F` system은 unitary하게 진화하지만, complement
qubit을 측정하고 특정 outcome만 선택하면 data system에는 effective non-unitary
map이 작용합니다.

주요 실험은 다음과 같습니다.

- measurement-induced denoising baseline
- measurement basis sweep을 통한 recovery gain, success probability, diversity
  retention trade-off 분석
- axis-only basis와 continuous basis 비교
- collapse-to-target baseline으로 distance-only metric의 한계 확인
- two-way post-selection candidate
- actor-critic result는 target-aware extension 또는 upper-bound 성격으로만 보조
  해석

핵심 결론은 denoising을 단순히 distance reduction 하나로 평가하면 안 되고,
recoverability, success probability, diversity retention을 함께 보아야 한다는
것입니다.

### IBM Cloud/QPU Validation

IBM Cloud에서는 전체 benchmark를 다시 수행한 것이 아니라, Problem 3-b의
measurement-basis mechanism이 작은 hardware-facing circuit으로 실행 가능한지
확인했습니다.

- backend: `ibm_fez`
- data qubits: `q0`, `q1`
- complement qubit: `q2`
- 측정한 것: basis 변화에 따른 `p(F=0)`와 selected-data entropy
- higher-shot run에서 `p(F=0)`가 basis 변화에 따라 약 `0.89 -> 0.66 -> 0.35`로
  변함

이는 measurement basis가 post-selected projected map을 조절한다는 해석의
hardware-execution validation이며, hardware advantage claim이 아닙니다.

## Main Results

- Haar reference:
  - `D_MMD = 0.869583 +/- 0.024043`
  - `W_{1-F} = 0.724439 +/- 0.021491`
  - Haar는 학습 목표가 아니라 strong-scrambling regime을 해석하기 위한 reference
    level입니다.
- Problem 3-b:
  - continuous measurement-basis post-selection은 MMD와 Wasserstein-type distance를
    줄일 수 있습니다.
  - axis-only 대비 margin은 작으므로 압도적 우월성으로 주장하지 않습니다.
  - 핵심은 distance gain, `p_succ`, `R_div` 사이의 trade-off입니다.
- Problem 3-c:
  - two-way post-selection은 더 큰 distance improvement를 만들 수 있지만 success
    probability를 낮춥니다.
  - 따라서 unconditional win이 아니라 analysis-guided trade-off improvement입니다.

## Team Contributions

이 섹션은 저장소 문서와 팀 메신저 기록을 바탕으로 아카이빙 목적에 맞게 정리한
역할 기록입니다. 메신저에 명시적으로 남아 있지 않은 구현, 실험, 통합 작업은
프로젝트 maintainer 기록에 따라 한지후가 수행한 것으로 정리합니다.

| 팀원 | 주요 기여 | 발표/제출 역할 |
|---|---|---|
| 한지후 (`caffeine-fighter`) | 전체 실험 설계, 핵심 구현, Problem 1/2/3 코드 통합, metric/result gatekeeping, IBM QPU validation, 재현 명령과 최종 패키지 정리 | Problem 2, IBM validation, closing |
| 김건우 (`koi312500`) | 코드와 Qiskit 구현 해석, notebook 설명과 실제 구현의 consistency 검수, 제출 패키지 정리, 발표자료 제작/수정 지원 | opening, Problem 1 |
| 임채진 (`chaejinlim235`) | 코드와 결과 해석, Problem 3(a,b) storyline 정리, 최종 notebook/report와 발표자료 제작 지원 | Problem 3(a), Problem 3(b) |
| 김승빈 (`dreamerghost77`) | 물리적 해석, Problem 3(c) trade-off 해석, measurement-induced denoising/actor-critic 보조 해석, figure/table/repro log 정리 지원 | Problem 3(c) |

대회 직전 5분 발표 흐름은 `Problem 1 -> Problem 2 -> Problem 3(a,b,c) -> IBM
QPU validation` 순서로 정리되었습니다.

## Where To Start

처음 보는 독자는 아래 순서로 보면 됩니다.

1. `submission/usb_package/Summary.md`
   또는 compact archive의 `submission/usb_package/README.md`
2. `submission/usb_package/solution/Problem 1.ipynb`
3. `submission/usb_package/solution/Problem 2.ipynb`
4. `submission/usb_package/solution/Problem 3.ipynb`
5. `submission/usb_package/presentation/QuantumCylinder_presentation.pdf`
   또는 compact archive의
   `submission/usb_package_supporting_materials/presentation/QuantumCylinder_presentation.pdf`
6. 코드 확인은 저장소 루트의 `src/`, `submission/`, `scripts/`, `tests/`를 보거나,
   compact archive의 `submission/usb_package/code/`를 보면 됩니다.

`submission/usb_package/solution/Problem 1.ipynb`, `Problem 2.ipynb`,
`Problem 3.ipynb`가 primary judge-facing notebook입니다.
full USB package layout에
`submission/usb_package/source_code/solution/solution_1.ipynb`가 존재하더라도,
이는 compact source-code reference이며 primary final answer가 아닙니다.

## Repository Map

```text
docs/                         Development notes and handoff documents
scripts/                      Experiment, validation, and packaging scripts
src/quantum_cylinder/         Main reusable implementation modules
submission/                   Lightweight submission-layer scripts
solution/                     Tables, figures, and compact solution notebook
tests/                        Reproducibility and regression tests
submission/usb_package/       Final USB-ready submission package
submission/usb_package_supporting_materials/
                              Presentation PDF and supporting archive zips
```

Inside the full USB package layout:

```text
Summary.md
README_SUBMISSION.md
JUDGING_CRITERIA_ALIGNMENT.md
solution/
  Problem 1.ipynb
  Problem 2.ipynb
  Problem 3.ipynb
  figures/
presentation/
  QuantumCylinder_presentation.pdf
  PRESENTATION_SLIDE_TEXT_EN.md
  PRESENTATION_STORYBOARD_EN.md
  PRESENTATION_15MIN_SPEAKER_SCRIPT_EN.md
  MANUAL_PRESENTATION_EXPORT_GUIDE.md
source_code/
  README_FOR_JUDGES.md
  CODE_MANIFEST.md
  PROBLEM_REQUIREMENT_MAP.md
  REPRODUCIBILITY_COMMANDS.md
  IBM_QPU_README.md
  src/
  scripts/
  tests/
  submission/
  solution/
  results/
```

Inside the compact archive layout:

```text
submission/usb_package/
  README.md
  code/
    pyproject.toml
    requirements.txt
    submission/
    ibm_qpu/
  solution/
    Problem 1.ipynb
    Problem 2.ipynb
    Problem 3.ipynb
    IBM_QPU_Implementation.ipynb
    figures/
submission/usb_package_supporting_materials/
  presentation/QuantumCylinder_presentation.pdf
  archive/
    QuantumCylinder_full_source.zip
    full_source_code_tree.zip
    presentation_supporting_text.zip
    top_level_supporting_reports.zip
```

## Reproduction

From the repository root:

```powershell
python -m pytest
python submission/run_all.py --quick
```

From the USB package source-code folder:

```powershell
cd submission/usb_package/source_code
python -m pytest
python submission/run_all.py --quick
```

For the compact archive layout:

```powershell
cd submission/usb_package/code
python submission/run_all.py --quick
```

Optional validation commands:

```powershell
python scripts/validate_final_csvs_no_pandas.py
python scripts/scan_for_ibm_secrets.py
```

When the full USB package layout is present, more detailed commands are in
`submission/usb_package/source_code/REPRODUCIBILITY_COMMANDS.md`.

## Claim Guardrails

The archive should be read with the following guardrails.

- We do not claim quantum advantage.
- We do not claim hardware advantage.
- We do not claim a full trainable QuDDPM.
- We do not claim Hamiltonian projected diffusion is universally better than
  random-unitary diffusion.
- We do not claim continuous basis is overwhelmingly better than axis-only
  basis.
- IBM Cloud/QPU execution is a tiny representative hardware-execution
  validation, not a full hardware benchmark.
- Main quantitative claims are based on reproducible state-vector simulation.

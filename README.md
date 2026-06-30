# QuantumCylinder Final Submission

## 1. 가장 먼저 열 파일

1. `submission/usb_package/presentation/QuantumCylinder_presentation.pdf`
   - 영어 발표자료.
   - 본선 5분 발표와 결선 15분 발표에 같은 파일을 사용한다.
2. `submission/usb_package/solution/Problem 1.ipynb`
   - Problem 1 최종 풀이.
3. `submission/usb_package/solution/Problem 2.ipynb`
   - Problem 2 최종 풀이.
4. `submission/usb_package/solution/Problem 3.ipynb`
   - Problem 3 최종 풀이.
5. `submission/usb_package/source_code/README_FOR_JUDGES.md`
   - 소스코드 실행 및 검증 안내.

`submission/usb_package/solution/Problem 1.ipynb`,
`Problem 2.ipynb`, `Problem 3.ipynb`가 primary judge-facing
notebook이다. `submission/usb_package/source_code/solution/solution_1.ipynb`가
존재하더라도 이는 compact source-code reference일 뿐이며 primary final answer가
아니다.

## 2. 한 문장 기여

QuantumCylinder는 random-unitary diffusion과 Hamiltonian projected diffusion을
같은 fidelity 기반 MMD/Wasserstein-type metric으로 비교하고,
measurement-induced projected denoising에서 recoverability,
post-selection success probability, diversity retention의 trade-off를 분석하며,
이 3-b mechanism을 IBM Cloud의 tiny M+F circuit으로도 검증한다.

## 3. 문제별 풀이 위치

| 문제 | 요구사항 | 최종 파일 |
|---|---|---|
| 1(a) | \(S_0\) target ensemble 생성 | `submission/usb_package/solution/Problem 1.ipynb` |
| 1(b) | Fidelity, MMD, Wasserstein-type distance | `submission/usb_package/solution/Problem 1.ipynb` |
| 1(c) | Random-unitary diffusion trajectory + Haar reference | `submission/usb_package/solution/Problem 1.ipynb` |
| 2(a) | Fixed Hamiltonian \(H\) | `submission/usb_package/solution/Problem 2.ipynb` |
| 2(b) | Hamiltonian projected ensemble | `submission/usb_package/solution/Problem 2.ipynb` |
| 2(c) | \(S_t^{Ham}\) distance curves and comparison | `submission/usb_package/solution/Problem 2.ipynb` |
| 2(d) | Resource/control-cost proxy | `submission/usb_package/solution/Problem 2.ipynb` |
| 3(a) | Measurement-induced denoising | `submission/usb_package/solution/Problem 3.ipynb` |
| 3(b) | Measurement-basis trade-off analysis | `submission/usb_package/solution/Problem 3.ipynb` |
| 3(c) | Two-way post-selection improvement | `submission/usb_package/solution/Problem 3.ipynb` |

## 4. 핵심 결과

- Haar reference:
  - \(D_{\mathrm{MMD}} = 0.869583 \pm 0.024043\)
  - \(W_{1-F} = 0.724439 \pm 0.021491\)
  - Haar는 학습 목표가 아니라 strong-scrambling regime을 해석하기 위한
    reference level이다.

- Problem 3-b:
  - continuous measurement-basis post-selection은 MMD와 Wasserstein-type
    distance를 줄인다.
  - axis-only 대비 margin은 작으므로 압도적 우월성을 주장하지 않는다.
  - 핵심은 distance gain, \(p_{\mathrm{succ}}\), \(R_{\mathrm{div}}\)
    사이의 trade-off를 분석한다는 점이다.

- Problem 3-c:
  - two-way post-selection은 더 큰 distance improvement를 만들지만 success
    probability를 낮춘다.
  - 따라서 unconditional win이 아니라 analysis-guided trade-off improvement이다.

- IBM Cloud validation:
  - `ibm_fez`에서 Problem 3-b tiny M+F measurement-basis sweep을 실행한다.
  - 두 job이 DONE 상태다.
  - higher-shot run에서 \(p(F=0)\)가 beta에 따라 약
    \(0.89 \to 0.66 \to 0.35\)로 변한다.
  - 이는 hardware-execution validation이며 hardware advantage claim이 아니다.

## 5. 실행 명령

```powershell
cd submission/usb_package/source_code
python -m pytest
python submission/run_all.py --quick
```

Optional inspection commands:

```powershell
python scripts/validate_final_csvs_no_pandas.py
python scripts/scan_for_ibm_secrets.py
```

## 6. 제출 패키지 구조

```text
submission/usb_package/
  presentation/
  solution/
  source_code/
  Summary.md
  README_SUBMISSION.md
  JUDGING_CRITERIA_ALIGNMENT.md
```

## 7. Claim guardrails

- full trainable QuDDPM을 구현했다고 주장하지 않는다.
- quantum advantage를 주장하지 않는다.
- hardware advantage를 주장하지 않는다.
- IBM Cloud 실행은 tiny representative circuit의 hardware-execution validation이다.
- main quantitative benchmark는 state-vector simulation에 기반한다.
- actor-critic 결과가 있으면 target-aware toy candidate로만 취급한다.

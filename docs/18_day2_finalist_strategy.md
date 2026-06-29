# Day 2 Finalist Strategy

이 문서는 Day 2부터 Problem 3를 결선 진출용 결과물로 다듬기 위한 전략 문서다.

## 한 줄 목표

QuantumCylinder는 random-unitary diffusion과 Hamiltonian projected diffusion을 같은 fidelity 기반 metric으로 재현하고, 둘을 섞은 hybrid diffusion toy를 Problem 3의 front-facing extension으로 제안한다. 기존 continuous measurement-basis post-selection 결과는 recoverability, success probability, diversity retention, control/resource cost를 평가하는 안전한 정량 baseline으로 유지한다.

## 왜 이 방향인가

5팀 중 1팀만 결선에 진출한다면, 단순히 "문제를 풀었다"만으로는 부족하다. 심사위원은 모든 코드를 오래 볼 시간이 없으므로, 기술적으로 맞으면서도 30초 안에 차별점이 보여야 한다.

우리의 차별점은 다음 문장으로 고정한다.

> 좋은 diffusion은 단순히 `S0`에서 멀리 퍼지는지만으로 평가할 수 없다. 다시 회복 가능한지, post-selection 성공확률이 충분한지, 다양성을 보존하는지, 제어 비용이 납득 가능한지를 함께 봐야 한다. 우리는 이 평가축 위에서 random-unitary와 Hamiltonian-inspired dynamics를 섞은 2-qubit toy extension까지 테스트했다.

## 현재 메인 결과

현재 Problem 3 seed sweep은 main result로 사용할 수 있는 상태다.

| Metric | Current value |
| --- | --- |
| Seed gate | `20 / 20 use_as_main` |
| Main-candidate rows | `81 / 120 = 0.675` |
| Median MMD improvement | `0.097056` |
| Median Wasserstein improvement | `0.147983` |
| Median axis-only score margin | `0.010000` |
| Median diversity retention | `0.823217` |
| Median success probability | `0.468122` |

단, axis-only 대비 margin은 작다. 따라서 "continuous basis가 압도적으로 좋다"가 아니라 "recoverability-aware benchmark를 만들었고, 그 안에서 continuous post-selection이 재현 가능한 toy denoising proxy로 동작했다"라고 주장해야 한다.

## Day 2 자동화의 역할

자동화는 새 알고리즘을 무작정 늘리는 장치가 아니다. 아래 증거를 반복적으로 만들고 검증하는 장치다.

1. Hybrid random-unitary + Hamiltonian-inspired toy 결과 생성
2. Problem 3(a/b/c) 조건 충족 여부 점검
3. Frozen-parameter holdout으로 selection bias 방어
4. Identity, axis-only, continuous, collapse baseline 비교표 생성
5. Strong-scrambling 또는 angle-scale ablation
6. 최종 보고서/발표에 들어갈 figure, table, claim, limitation 생성
7. 실패한 후보는 main result를 대체하지 않고 appendix/fallback으로 기록

## 실행

overnight 실행은 `docs/19_problem_3_finalist_autopilot.md`의 명령을 사용한다. 08:00 조식은 종료 기준이 아니라 중간 확인 시점으로 두고, 자동화는 stop script를 실행하기 전까지 계속 돌린다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_problem_3_finalist_autopilot.ps1 -CycleMinutes 0 -KeepDisplayOff
```

백그라운드 실행:

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_problem_3_finalist_autopilot.ps1 -CycleMinutes 0 -KeepDisplayOff -Detached
```

상태 확인:

```powershell
cd C:\Coding\Hackathon\2026Quantum
Get-Content results\problem_3_finalist_autopilot\latest_status.md -Wait -Tail 120
```

## 팀원별 역할

| Member | Focus | Output |
| --- | --- | --- |
| 한지후 | 자동화 실행, 통합, 최종 gatekeeping | passing tests, status 확인, merge 판단 |
| 김건우 | 물리 해석 검수 | Hamiltonian/projection/measurement 설명 검증 |
| 임채진 | 문제 해석과 보고서 스토리 | Problem 3(a/b/c) 충족 여부, 발표 문장 |
| 김승빈 | 실행/로그/figure 보조 | seed sweep 확인, figure/table 재현 |

## 하지 말아야 할 주장

- Quantum advantage를 보였다고 말하지 않는다.
- Hardware advantage를 보였다고 말하지 않는다.
- Full trainable QuDDPM reverse process를 구현했다고 말하지 않는다.
- Continuous basis가 axis-only보다 압도적으로 좋다고 말하지 않는다.
- Seed마다 best point를 고른 결과만으로 일반화 성능을 주장하지 않는다.

## 안전한 최종 문장

> 작은 state-vector 실험에서 continuous measurement-basis post-selection은 reproducible post-selected toy denoising proxy로 사용할 수 있다. 20-seed sweep에서 MMD/Wasserstein 개선은 재현되지만 axis-only 대비 margin은 작으므로, hardware advantage나 general quantum advantage가 아니라 recoverability-aware benchmark/probe로 제한해 주장한다.

hybrid extension까지 포함한 발표용 문장:

> 메인 정량 결과는 continuous post-selected denoising benchmark이고, 차별화 포인트는 random-unitary와 Hamiltonian-inspired projected dynamics를 섞은 2-qubit hardware-compatible toy extension이다. 우리는 이를 통해 "잘 퍼지는 diffusion"보다 "회복 가능하고 구현 비용까지 설명 가능한 diffusion"을 평가하는 방향을 제안한다.

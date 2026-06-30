# Problem 3 Finalist Autopilot

이 문서는 Problem 3 자동화의 목적, 전략, 실행 방법을 팀원이 빠르게 이해할 수 있도록 정리한 운영 문서다.

## 목표

우리 팀은 ML과 구현에는 강하지만 양자물리 해석은 약하다. 따라서 Problem 3에서는 복잡한 양자 이론을 과장해서 주장하기보다, 작은 state-vector 실험에서 재현 가능한 benchmark를 만들고 그 결과를 방어 가능하게 설명하는 것이 승률이 높다.

선택한 최종 방향은 **hybrid random-unitary + Hamiltonian-inspired diffusion을 앞에 세우고, 기존 continuous post-selection 결과를 안전한 정량 baseline으로 유지하는 전략**이다.

핵심 메시지는 다음과 같다.

> 좋은 quantum diffusion은 단순히 `S0`에서 멀리 퍼지는지만으로 평가할 수 없다. Recoverability, post-selection success probability, diversity retention, control/resource cost를 함께 봐야 하며, QuantumCylinder는 이 trade-off를 작은 실험으로 정량화했다.

발표에서 기억될 리본은 다음이다.

> random-unitary와 Hamiltonian projected diffusion을 따로 재현하는 데서 멈추지 않고, 둘을 섞은 2-qubit hardware-compatible toy까지 내려가 보았다.

## 문제 3에서 반드시 보여야 하는 것

문제 3은 자유주제처럼 보이지만 실제 요구사항은 세 가지다.

1. Toy reverse 또는 denoising step을 보여야 한다.
2. Diffusion setting을 통제된 방식으로 바꾸고 trade-off를 분석해야 한다.
3. Random-unitary diffusion 또는 Hamiltonian-time-evolution diffusion의 개선안을 제안하고, 작은 예시에서 baseline과 비교해야 한다.

자동화는 매 cycle마다 이 세 조건 중 하나 이상을 더 잘 방어하도록 설계한다.

## 현재 가장 안전한 메인 결과

현재 Problem 3의 주 결과는 continuous measurement-basis post-selection이다.

| Metric | Current value |
| --- | --- |
| Seed gate | `20 / 20 use_as_main` |
| Main-candidate rows | `81 / 120 = 0.675` |
| Median MMD improvement | `0.097056` |
| Median Wasserstein improvement | `0.147983` |
| Median axis-only score margin | `0.010000` |
| Median diversity retention | `0.823217` |
| Median success probability | `0.468122` |

이 결과는 main result로 사용할 수 있지만, axis-only 대비 margin이 작으므로 과장하면 위험하다. 발표에서는 "continuous basis가 압도적으로 좋다"가 아니라 "recoverability-aware benchmark를 만들었다"로 말해야 한다.

## 자동화가 하는 일

새 자동화 스크립트는 다음 루프를 반복한다.

```text
team sync -> pytest -> submission quick -> Hermes evidence improvement
-> pytest -> submission quick -> optional 20-seed sweep -> issue sync -> status/progress 기록
```

Hermes task는 무작정 best score를 더 찾지 않는다. 우선순위는 다음이다.

1. Hybrid random-unitary + Hamiltonian-inspired toy 실행 및 결과 정리
2. Problem 3(a/b/c) 조건 충족 여부 점검
3. Frozen-parameter holdout 추가 또는 보강
4. Identity / axis-only / continuous / collapse baseline table 보강
5. Strong-scrambling, angle-scale, parameter ablation
6. 최종 발표용 figure/table/claim 문장 생성
7. 실패한 후보는 appendix/fallback으로 기록

hybrid toy는 다음 명령으로 단독 실행할 수도 있다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
python scripts\run_problem_3_hybrid_diffusion_toy.py
```

생성 결과:

- `results/problem_3_hybrid_diffusion_toy/hybrid_toy_summary.md`
- `results/problem_3_hybrid_diffusion_toy/hybrid_best_metrics.csv`
- `results/problem_3_hybrid_diffusion_toy/hybrid_toy_metrics.png`

`hybrid_toy_summary.md`는 Problem 3(a)/(b)/(c) requirement coverage와 `front_facing_extension`/`appendix_or_fallback` decision guardrail을 함께 기록한다. 심사위원용 묶음은 `results/problem_3_finalist_package/`에 생성하며, seed sweep을 새로 돌리지 않은 cycle이면 기존 20-seed gate를 재요약한 것인지 명시한다.

seed별 grid-best cherry-picking 질문을 방어하려면 frozen-parameter holdout 요약을 실행한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
python scripts\summarize_problem_3_frozen_holdout.py
```

이 holdout은 train seeds `1..10`에서 하나의 continuous parameter tuple `(tau, theta, phi)`만 고른 뒤 holdout seeds `11..20`에 그대로 적용한다. 결과는 `results/problem_3_frozen_parameter_holdout/frozen_holdout_summary.md`에 남기며, oracle grid-best seed sweep을 대체하지 않고 selection-bias 방어용 보조 근거로만 쓴다.

거리 개선만 보고 collapse된 후보를 고르는 실수를 방어하려면 baseline/collapse table을 생성한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
python scripts\summarize_problem_3_baseline_collapse_table.py
```

이 표는 identity/no-denoising, best exact `Z/X/Y`, continuous post-selection, intentionally collapsed centroid diagnostic을 같은 MMD/Wasserstein/diversity/success probability 형식으로 비교한다. Collapse row는 물리적 제안이 아니라 "거리 개선만으로는 충분하지 않다"는 judge-facing 반례다.

## 실행 명령

### 6/30 새벽 01:00부터 조식 이후까지 쉬지 않고 실행

08:00 조식은 종료 기준이 아니라 중간 확인 시점으로 둔다. 아래 명령은 `Ctrl+C` 또는 stop script를 실행하기 전까지 쉬지 않고 다음 cycle을 시작한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_problem_3_finalist_autopilot.ps1 -CycleMinutes 0 -KeepDisplayOff
```

PowerShell 창을 비워두고 백그라운드로 실행하려면 다음을 사용한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_problem_3_finalist_autopilot.ps1 -CycleMinutes 0 -KeepDisplayOff -Detached
```

08:00에는 새 PowerShell에서 상태만 확인한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
Get-Content results\problem_3_finalist_autopilot\latest_status.md -Wait -Tail 120
```

자동 종료 옵션이 필요할 때만 `-RunHours` 또는 `-StopAt`을 별도로 붙인다. 기본 전략은 조식 이후에도 계속 돌려서 Problem 3 evidence package를 누적하는 것이다.

`-MinRemainingMinutesForNextCycle` 기본값은 `0`이다. 즉, 종료 조건을 직접 걸지 않는 한 08:00이 가까워져도 새 cycle을 막지 않는다.

먼저 1 cycle만 시험 실행한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_problem_3_finalist_autopilot.ps1 -MaxCycles 1 -KeepDisplayOff
```

문제 없으면 상시 실행한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_problem_3_finalist_autopilot.ps1 -CycleMinutes 0 -KeepDisplayOff
```

PowerShell 창을 점유하지 않고 백그라운드로 실행하려면 다음을 사용한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_problem_3_finalist_autopilot.ps1 -CycleMinutes 0 -KeepDisplayOff -Detached
```

`-KeepDisplayOff`는 화면은 꺼질 수 있지만 시스템 sleep은 막도록 설정한다. 즉, 밤새 돌릴 때는 이 옵션을 붙이는 것이 좋다.

`-FullSeedSweepEvery 3`이 기본값이므로 3 cycle마다 20-seed sweep을 다시 수행한다. 더 공격적으로 검증하고 싶으면 `-FullSeedSweepEvery 2`, 실행 시간을 아끼고 싶으면 `-FullSeedSweepEvery 0`으로 비활성화할 수 있다.

## 상태 확인

다른 PowerShell에서 다음 명령으로 진행 상황을 본다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
Get-Content results\problem_3_finalist_autopilot\latest_status.md -Wait -Tail 120
```

백그라운드 실행 자체의 stdout/stderr는 다음 파일에 남는다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
Get-Content logs\problem_3_finalist_autopilot\detached_process.json
```

Hermes watchdog의 최신 상태는 다음으로 본다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
Get-Content logs\problem_3_finalist_autopilot\latest_state.json
```

실제 로그 파일은 `latest_state.json`의 `log` 항목에 기록된다.

## 중지 방법

attached 실행이면 실행 중인 PowerShell에서 `Ctrl+C`를 누른다. 가장 깔끔한 종료 기준은 다음 메시지 직후다.

```text
END: Problem 3 finalist autopilot cycle <n> with status pass
```

detached 실행이면 다음 명령을 사용한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\stop_problem_3_finalist_autopilot.ps1
```

## 팀원별 역할

| Member | Focus | Output |
| --- | --- | --- |
| 한지후 | 자동화 실행, 통합, gatekeeping | status 확인, PR/merge 판단, 최종 claim 고정 |
| 김건우 | 코드/Qiskit consistency 검수 | conditional state, Hamiltonian/projection, resource 설명 검증 |
| 임채진 | 문제 해석과 보고서 스토리 | Problem 3(a/b/c) 충족 여부, 발표 문장 정리 |
| 김승빈 | 물리 해석, 실행 로그, figure/table 패키징 | measurement-induced denoising 해석, seed sweep 확인, figure/table 재현 |

## 하지 말아야 할 주장

- Quantum advantage를 보였다고 말하지 않는다.
- 실제 hardware advantage를 보였다고 말하지 않는다.
- full trainable QuDDPM reverse process를 구현했다고 말하지 않는다.
- continuous basis가 axis-only보다 압도적으로 좋다고 말하지 않는다.
- seed마다 best point를 고른 결과만으로 일반화 성능을 주장하지 않는다.

## 안전한 최종 문장

> 메인 정량 결과는 2-data-qubit setting에서의 continuous measurement-basis post-selection benchmark다. 추가로, random-unitary scrambling과 Hamiltonian-inspired projected dynamics를 섞은 1-data-qubit + 1-auxiliary-qubit hybrid toy를 통해 IBM-style circuit으로 내려갈 수 있는 최소 형태를 실험했다. 두 결과 모두 small-scale state-vector benchmark/probe이며, hardware advantage나 general quantum advantage를 주장하지 않는다.

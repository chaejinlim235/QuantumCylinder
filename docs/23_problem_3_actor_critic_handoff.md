# Problem 3 Actor-Critic Handoff

기준 시각: `2026-06-30 14:31 KST`

## 결론

김승빈의 새 제안은 **진행할 가치가 있다**. 다만 최종 발표에서 "일반적인 unknown-target denoiser"로 말하면 위험하고, **raw target ensemble을 reward로 사용하는 target-aware actor-critic parameter search**로 제한해야 한다.

이 제한을 지키면 Problem 3(c)의 "개선안 제안 및 작은 예제 비교" 요구에 잘 맞는다.

## 새 실험

- 방법: actor-critic policy search
- Action: `K_lambda = diag(1, lambda, lambda, lambda)`의 `lambda` 선택
- Actor: noisy ensemble feature를 보고 action 확률을 업데이트
- Critic: 같은 feature에서 reward baseline을 추정
- Reward: raw target과의 MMD/Wasserstein distance 감소를 보상
- Guardrail: diversity retention과 success probability가 낮은 후보는 penalty 및 선택 제외

## 기본 실행 명령

```powershell
python scripts/run_problem_3_actor_critic_denoising.py
```

생성물:

- `results/problem_3_actor_critic_denoising/actor_critic_summary.md`
- `results/problem_3_actor_critic_denoising/actor_critic_metrics.csv`
- `results/problem_3_actor_critic_denoising/actor_critic_comparison.png`

`results/` 아래 생성물은 Git에 커밋하지 않는다.

## 최신 10-Seed 결과

기본 설정으로 `10`개 seed와 input step `[1, 2, 3]`, 총 `30`개 row를 평가했다.

| Metric | Result |
| --- | --- |
| recommendation | `front_facing_candidate` |
| actor beats 3(a) continuous baseline on MMD | `30 / 30` |
| actor beats 3(a) continuous baseline on Wasserstein | `30 / 30` |
| actor beats both metrics | `30 / 30` |
| median actor MMD improvement | `0.359015` |
| median actor Wasserstein improvement | `0.315669` |
| median actor-vs-continuous MMD margin | `0.271909` |
| median actor-vs-continuous Wasserstein margin | `0.178397` |
| median actor diversity retention | `0.812548` |
| median actor success probability | `0.387360` |

## Notebook 사본

건우가 주석을 단 notebook 형식을 참고해 actor-critic 3(c) 섹션을 추가한 로컬 사본:

```text
C:\Users\sky_m\Downloads\QuantumCylinder_final_submission_report_actor_critic_commented_v1.ipynb
```

검증:

- 전체 notebook 실행 완료
- `30 / 30` row에서 actor-critic이 기존 3(a) continuous baseline보다 MMD와 Wasserstein 모두 낮음
- median diversity retention `0.811962`
- median success probability `0.353912`
- 한글 `??` 깨짐 없음
- mid-noise/re-noise 문구 없음

Notebook 내부 숫자는 repo script의 기본 설정과 sample 수가 조금 다르다. 보고서에 넣을 최종 숫자는 하나로 고정해야 하므로, 제출 직전에는 script 기본 설정 또는 notebook 설정 중 하나를 source of truth로 선택한다.

## 안전한 Claim

> 작은 state-vector 실험에서 raw target ensemble을 reward로 사용하는 actor-critic parameter search가 target-aware non-unitary filter strength를 선택했고, 평가한 여러 seed/input step에서 기존 continuous measurement-basis denoising baseline보다 낮은 MMD/Wasserstein distance를 보였다. 이 결과는 target-aware toy denoising improvement이며, hardware advantage나 일반 quantum advantage 주장은 아니다.

## 남은 일

1. 임채진은 actor-critic 3(c) 섹션을 최종 보고서에 넣을지, 아니면 appendix 후보로 둘지 결정한다.
2. 김건우는 `K_lambda = diag(1, lambda, lambda, lambda)`가 target prior를 쓰는 non-unitary filter라는 설명이 코드와 맞는지 검수한다.
3. 김승빈은 actor-critic을 물리적 denoising claim이 아니라 target-aware policy selection claim으로 제한하는 문장을 검수한다.
4. 한지후는 README, issue, PR, CI 상태를 동기화하고 최종 숫자 source of truth를 하나로 고정한다.

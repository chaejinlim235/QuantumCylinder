# Problem 3 Method Portfolio

기준 시각: `2026-06-30`

## 핵심 판단

Problem 3는 actor-critic 하나로 결론내리면 안 된다. 최종 보고서의 구조는 다음 순서가 되어야 한다.

1. 여러 reverse/denoising 아이디어를 제시한다.
2. 같은 거리 지표와 guardrail로 비교 가능한 것은 한 표에 올린다.
3. 직접 비교가 어려운 후보는 scope와 caveat를 분리해서 적는다.
4. 최종 채택 후보와 부록/기각 후보를 명확히 나눈다.

따라서 actor-critic은 최종 후보 중 하나이며, 전체 방법론을 대체하지 않는다.

## 비교할 후보

| Candidate | 역할 | 보고서에서의 위치 | 주의점 |
| --- | --- | --- | --- |
| identity/no-denoising input | reverse step을 하지 않은 기준점 | baseline | 성능 후보가 아니라 비교 기준 |
| best Z/X/Y axis projection | discrete measurement baseline | 3(b) 대조군 | continuous basis가 꼭 필요한지 확인하는 기준 |
| continuous measurement-basis post-selection | 20-seed gate를 통과한 main quantitative result | 3(a), 3(b) 본문 | axis-only 대비 margin이 작다는 limitation을 함께 적음 |
| diagnostic collapse-to-centroid | 거리 지표만 보는 평가의 실패 예시 | 3(b) 또는 appendix | 물리적 denoiser가 아니며 diversity collapse를 보여주는 방어용 진단 |
| hybrid 1M+1F toy | random-unitary와 Hamiltonian/post-selection을 섞은 hardware-motivated extension | 3(c) 후보 | 1-qubit toy라 main 2-qubit seed sweep과 직접 우열 비교하지 않음 |
| target-aware actor-critic | raw target reward를 쓰는 policy-search 개선 후보 | 3(c) 후보 또는 appendix | unknown-target 일반 denoiser가 아니라 target-aware toy improvement |

## 최종 선택 규칙

- 3(a), 3(b)의 main result는 `continuous measurement-basis post-selection`으로 둔다.
- 3(b)는 `axis-only`와 `continuous basis`의 통제 비교를 보여준다.
- 3(c)는 최소 두 후보를 보여준다.
  - `hybrid 1M+1F toy`: 하드웨어 동기와 보조 큐빗 측정 구조를 설명하는 후보.
  - `target-aware actor-critic`: 성능이 강하지만 target 정보를 쓰는 후보.
- actor-critic 수치가 좋아도 “최종 방법은 actor-critic 하나”라고 쓰지 않는다.
- collapse diagnostic은 성능 후보가 아니라, MMD/Wasserstein만으로는 부족하다는 것을 보이는 방어용 표로 둔다.

## 실행 명령

아래 명령은 이미 생성된 Problem 3 결과물을 읽어 후보 포트폴리오 표와 그림을 만든다.

```powershell
python scripts/summarize_problem_3_method_portfolio.py
```

생성물:

- `results/problem_3_method_portfolio/method_portfolio_summary.md`
- `results/problem_3_method_portfolio/method_portfolio_summary.csv`
- `results/problem_3_method_portfolio/method_portfolio_summary.png`

`results/` 아래 생성물은 기본적으로 Git에 커밋하지 않는다.

## 보고서 문장

최종 보고서의 안전한 서술:

> 우리는 Problem 3에서 하나의 알고리즘만 제안하지 않고, no-denoising baseline, axis-only projection, continuous measurement-basis post-selection, collapse diagnostic, hybrid 1M+1F toy, target-aware actor-critic 후보를 같은 recoverability-aware 관점에서 비교했다. 20-seed robustness gate를 통과한 main result는 continuous post-selection이며, 3(c)의 확장 후보로는 hardware-motivated hybrid toy와 target-aware actor-critic policy search를 제시한다. Actor-critic은 성능상 강한 후보지만 raw target reward를 사용하므로 unknown-target 일반 denoiser로 주장하지 않는다.

## 팀원별 확인 포인트

| Member | 확인할 것 |
| --- | --- |
| 임채진 | 최종 ipynb에서 3(c)가 actor-critic 단독 구조가 아니라 후보 비교 구조인지 확인 |
| 김승빈 | hybrid 1M+1F와 continuous post-selection의 물리적 해석, 보조 큐빗 측정의 필요성 검수 |
| 김건우 | 후보별 코드와 metric 해석이 실제 구현과 맞는지 검수 |
| 한지후 | `summarize_problem_3_method_portfolio.py`, README, issue, notebook 사본 동기화 |

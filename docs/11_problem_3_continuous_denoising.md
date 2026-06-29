# Problem 3 Continuous Projected Denoising

## 선택한 방향

Problem 3의 메인 후보는 **continuous measurement-induced denoising**이다.

기본 `Z/X/Y` measurement basis sweep은 문제 PDF가 직접 예시로 든 방향이므로 다른 팀과 겹칠 가능성이 높다. 그래서 우리는 `Z/X/Y`를 baseline으로만 두고, complement qubit projection basis를 Bloch sphere 위의 연속 basis로 넓혀 탐색한다.

```text
|b(theta, phi)> = cos(theta / 2)|0> + exp(i phi) sin(theta / 2)|1>
```

## 실험 아이디어

1. Problem 1의 `S0`를 만든다.
2. random-unitary diffusion으로 `S_k`를 만든다.
3. `S_k`에 complement qubit `|0>`을 붙인다.
4. Problem 2의 fixed Hamiltonian으로 짧게 evolve한다.
5. complement qubit을 continuous basis로 post-select한다.
6. 이 non-unitary projected map을 toy denoising step으로 본다.
7. `dist(S_k, S0)`와 `dist(D(S_k), S0)`를 같은 MMD/Wasserstein-type metric으로 비교한다.

## 왜 3번 요구와 맞는가

- Problem 3(a): fixed measurement-induced non-unitary map으로 toy reverse/denoising step을 보인다.
- Problem 3(b): projection basis와 denoising time `tau`를 통제된 방식으로 바꾼다.
- Problem 3(c): baseline `S_k`와 axis-only `Z/X/Y` projection 대비 개선 여부를 작은 예제로 검증한다.
- Continuous 후보를 고를 때 exact `Z/X/Y` 축 basis는 제외한다.

## 채택 게이트

성능이 나오지 않으면 main result로 쓰지 않는다.

`main_candidate`가 되려면 다음을 만족해야 한다.

- MMD 또는 Wasserstein-type distance 중 하나가 baseline보다 개선된다.
- continuous basis 후보의 score가 best `Z/X/Y` axis-only 후보보다 충분히 높다.
- diversity retention이 너무 낮지 않다.
- mean post-selection probability가 너무 낮지 않다.

그렇지 않으면 `fallback_candidate` 또는 `do_not_use_as_main`으로 남긴다.

## 실행

```powershell
python scripts/run_problem_3_continuous_denoising.py
```

기본 결과는 `results/problem_3_continuous_denoising/`에 생성된다.

생성 파일:

- `candidate_search_metrics.csv`
- `best_denoising_metrics.csv`
- `denoising_improvement.png`
- `problem_3_settings.json`
- `problem_3_summary.md`

## 해석 기준

좋은 결과는 "거리 감소"만으로 판단하지 않는다.

- MMD 감소: target ensemble과 kernel 평균 구조가 가까워졌는지
- Wasserstein 감소: sample matching 관점에서 가까워졌는지
- diversity retention: ensemble이 한 점으로 collapse하지 않았는지
- success probability: post-selection이 너무 희박한 사건이 아닌지
- axis baseline 비교: 단순 `Z/X/Y` sweep보다 연속 basis 탐색이 의미가 있는지

## 발표 문장 후보

성공 시:

> We use the complement measurement basis as a continuous control knob and show that a post-selected Hamiltonian map can partially denoise a randomly scrambled ensemble while retaining nontrivial diversity.

실패 또는 애매한 경우:

> Continuous projected denoising improves some distance metrics in small cases, but the gain is not strong enough against the best axis-only projection or carries a diversity/success-probability trade-off, so we keep it as a candidate rather than the main result.

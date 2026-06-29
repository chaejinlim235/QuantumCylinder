# 팀 역할

개인정보가 담긴 신청서 원문은 저장소에 두지 않는다. 이 문서는 이름과 역할만 기록한다.

## 핵심 역할

| 팀원 | 주 담당 | 첫 산출물 | 리뷰 파트너 |
| --- | --- | --- | --- |
| 임채진 | 전체 연구 방향, 물리/정보이론 해석, 발표 논리 | 문제 해석 슬라이드 초안, final story line | 한지후 |
| 김건우 | 양자 회로 구현, random-unitary/Hamiltonian baseline, resource proxy | Problem 1/2 baseline 검증, depth/gate count 표 | 김승빈 |
| 김승빈 | 실험 파이프라인, 로그 관리, 시각화, 발표용 figure | 재현 가능한 실험 실행 스크립트, plot style | 김건우 |
| 한지후 | 수리 모델링, MMD/Wasserstein/loss 분석, 3번 extension 설계 | metric 검증, denoising/loss 후보 비교 리포트 | 임채진 |

## 한지후의 시작점

한지후는 다음 세 가지를 먼저 잡으면 팀 전체 속도가 올라간다.

1. MMD와 Wasserstein-type distance의 정의를 팀 표준으로 고정한다.
2. "같은 diffusion strength"를 비교할 기준을 만든다. 예: MMD가 비슷한 지점에서 resource proxy 비교.
3. 3번 extension 후보를 metric 관점으로 평가한다. 예: shallow denoising 후 MMD 회복량 대비 post-selection probability 또는 추가 depth.

## 협업 규칙

- 실험 PR은 반드시 owner와 reviewer를 둔다.
- 한 사람이 만든 figure는 다른 한 사람이 수치와 caption을 확인한다.
- failed experiment도 `docs/experiments/`에 짧게 남긴다. 실패의 이유가 3번 discussion 재료가 될 수 있다.
- 최종 발표에서는 팀원별 구현물을 나열하기보다 하나의 질문으로 묶는다: "양자 확산은 얼마나 적은 control로 충분히 잘 퍼지고, 얼마나 싸게 되돌릴 수 있는가?"

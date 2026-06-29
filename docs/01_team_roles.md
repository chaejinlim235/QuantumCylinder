# 팀 역할

개인정보가 담긴 신청서 원문은 저장소에 두지 않는다. 이 문서는 이름과 역할만 기록한다.

## 핵심 역할

| 팀원 | 주 담당 | 배경과 연결되는 지점 | 첫 산출물 | 리뷰 파트너 |
| --- | --- | --- | --- | --- |
| 임채진 | 연구 방향, 물리적 해석, 발표 구조 | 물리 데이터 해석 및 회귀 모델링 경험을 diffusion behavior 해석에 연결 | 문제 해석 슬라이드 초안, baseline 결과 해석 | 한지후 |
| 김건우 | 양자 회로 구현, resource proxy, hardware-aware 비교 | 양자 터널링 시뮬레이션과 모델 압축 경험을 회로 깊이/게이트 수 분석에 연결 | Problem 1/2 구현 검증, gate/depth proxy 표 | 김승빈 |
| 김승빈 | 실험 파이프라인, 로그 관리, 시각화 | 생성 모델 및 3D reconstruction 파이프라인 경험을 반복 실험 관리와 figure 제작에 활용 | 재현 가능한 실행 스크립트, plot/CSV 관리 | 김건우 |
| 한지후 | metric, loss, 수리 모델링, Problem 3 extension | ML systems, parameter-efficient adaptation, diffusion/loss 분석 경험을 MMD/Wasserstein 및 denoising 설계에 활용 | metric 검증, denoising 및 trade-off 분석 | 임채진 |

## 한지후의 시작점

한지후는 다음 세 가지를 먼저 잡으면 팀 전체 속도가 올라간다.

1. MMD와 Wasserstein-type distance의 정의를 팀 표준으로 고정한다.
2. "같은 diffusion strength"를 비교할 기준을 만든다. 예: MMD가 비슷한 지점에서 resource proxy 비교.
3. 3번 extension 후보를 metric 관점으로 평가한다. 예: shallow denoising 후 MMD 회복량 대비 post-selection probability 또는 추가 depth.

## 협업 규칙

- 실험 PR은 반드시 owner와 reviewer를 둔다.
- 한 사람이 만든 figure는 다른 한 사람이 수치와 caption을 확인한다.
- failed experiment도 `docs/experiments/`에 짧게 남긴다. 실패의 이유가 3번 discussion 재료가 될 수 있다.
- 최종 발표에서는 팀원별 구현물을 나열하기보다 하나의 질문으로 묶는다: "양자 확산 품질과 control/resource cost 사이의 trade-off는 어떻게 달라지는가?"

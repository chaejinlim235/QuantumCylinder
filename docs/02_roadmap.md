# 로드맵

## Day 0: 저장소와 공통 언어

- [x] Git 저장소 초기화
- [x] 문제 브리프 정리
- [x] 역할 분배 정리
- [x] baseline 코드 골격 생성
- [x] 기준 환경에서 `python scripts/run_problem_1_2_baselines.py` 실행 확인

## Day 1: 1/2번 재현

- [x] `N=80`, `sigma=0.10`, seed 고정
- [x] random-unitary trajectory plot 생성
- [x] Hamiltonian projected diffusion time sweep plot 생성
- [x] MMD/Wasserstein 결과 해석용 summary 생성
- [x] resource proxy 표 작성
- [x] comparable diffusion strength 기준 resource match 표 작성

성공 기준:

- baseline plot 2장 이상
- 각 mechanism의 diffusion parameter에 따른 qualitative behavior 설명
- Problem 2(d)의 comparable-strength resource/control 비교
- 코드 실행 방법이 README만 보고 재현 가능

## Day 2: 3번 extension 후보 압축

후보는 최대 2개만 남긴다.

- measurement basis/time schedule sweep
- shallow denoising Kraus map
- noisy channel 추가 후 robustness 비교
- Hamiltonian parameter sweep으로 동일 diffusion strength 비용 비교

성공 기준:

- baseline 하나 이상과 같은 metric으로 비교
- 좋아진 점과 희생한 점이 동시에 보임
- figure caption만 봐도 주장이 읽힘

## Day 3: 최종 실험

- seed 3개 이상 반복
- plot style 통일
- table: MMD, Wasserstein, resource proxy, failure mode
- 발표용 main figure 1개, appendix figure 2-3개 선정

## Day 4: 보고서/발표

- 문제 해석: 1 slide
- baseline 재현: 2 slides
- extension idea: 2 slides
- trade-off and limitations: 1-2 slides
- Q&A 대비: 왜 이 metric인지, 왜 이 resource proxy인지, 왜 small-scale가 의미 있는지

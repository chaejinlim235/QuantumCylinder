# Hermes Agent 연동 가이드

이 문서는 QuantumCylinder 저장소를 Hermes Agent와 함께 쓰기 위한 프로젝트 측 설정을 정리한다.

## 현재 연동 방식

저장소 루트에 `.hermes.md`를 둔다.

Hermes Agent는 이 파일을 프로젝트 context로 읽고 다음 정보를 사용한다.

- 현재 문제 진행도
- 실행 명령
- Problem 3 채택 게이트
- Git/PR 규칙
- 팀 역할
- 개인정보와 결과 파일 commit 규칙

## 설치

Hermes가 이미 설치되어 있지 않다면 Windows PowerShell에서 공식 설치 명령을 사용한다.

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

설치 후 새 터미널을 열고 확인한다.

```powershell
hermes --version
```

## 프로젝트에서 실행

저장소 루트에서 실행한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
hermes
```

Hermes에게 처음 줄 지시는 아래처럼 시작한다.

```text
Read .hermes.md and README.md first.
Use this repository's existing scripts and docs as the source of truth.
Do not commit generated results or private files.
For Problem 3, only treat a result as main if the adoption gate passes.
```

## 권장 작업 요청

Problem 3 seed sweep:

```text
Run the Problem 3 continuous denoising experiment for multiple seeds.
Summarize main_candidate/fallback_candidate counts and keep generated results out of Git.
```

보고서 보강:

```text
Read docs/11_problem_3_continuous_denoising.md and results/problem_3_continuous_denoising/problem_3_summary.md.
Draft concise Korean report paragraphs that describe the method, improvement, trade-off, and limitations.
Do not overclaim beyond the default run.
```

검증:

```text
Run python -m pytest and python scripts/run_problem_3_continuous_denoising.py.
Report the key result numbers and whether the adoption decision is use_as_main.
```

## 주의

- Hermes가 코드를 수정하면 반드시 `python -m pytest`를 실행한다.
- PR 본문은 가능하면 영어/ASCII로 쓴다.
- 한글 문서 파일 자체는 UTF-8로 작성한다.
- `results/` 아래 생성 파일은 기본적으로 commit하지 않는다.
- 신청서, 문제 원본 PDF, 개인정보가 포함된 파일은 commit하지 않는다.

## 현재 핵심 명령

```powershell
python scripts/run_problem_1_2_baselines.py
python scripts/run_problem_3_continuous_denoising.py
python scripts/problem_1_qiskit_resource_check.py
python -m pytest
```

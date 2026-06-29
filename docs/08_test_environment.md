# 테스트 환경

이 저장소는 로컬 테스트와 GitHub Actions CI를 함께 사용한다.

## 로컬 테스트

팀원이 PR을 열기 전 최소한 아래 명령을 실행한다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/problem_1a_generate_target_ensemble.py
python scripts/run_problem_1_2_baselines.py
pytest
```

Linux/macOS에서는 activate 명령만 다르다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/problem_1a_generate_target_ensemble.py
python scripts/run_problem_1_2_baselines.py
pytest
```

## GitHub Actions CI

`.github/workflows/ci.yml`이 다음 상황에서 자동 실행된다.

- `main` push
- `feat/**`, `fix/**`, `exp/**`, `docs/**`, `refactor/**`, `test/**`, `chore/**` 브랜치 push
- 모든 pull request

CI에서 실행하는 항목:

1. Python 3.11 설치
2. `pip install -e ".[dev]"`
3. `python scripts/problem_1a_generate_target_ensemble.py`
4. `python scripts/run_problem_1_2_baselines.py`
5. `pytest`

## 운영 규칙

- PR을 열기 전 로컬에서 `pytest`는 반드시 통과시킨다.
- 실험 코드나 metric을 바꿨다면 baseline smoke test도 실행한다.
- CI가 실패하면 merge하지 않는다.
- 시간상 급한 문서 PR이라도 CI 실패 원인이 코드 변경과 무관한지 확인하고 판단한다.
- 생성된 `results/` 파일은 기본적으로 커밋하지 않는다.

# Problem 3 Support Worker

이 문서는 지후 노트북에서 돌아가는 메인 자동화와 최고의 시너지를 내기 위해, 다른 팀원 노트북에서 무엇을 돌리면 좋은지 정리한 운영 문서다.

## 결론

김승빈 노트북에서는 두 번째 Hermes 자동화를 돌리지 않는다. 대신 `support worker`를 돌린다.

역할 분리는 다음과 같다.

| Machine | Role | Does |
| --- | --- | --- |
| 지후 노트북 | main finalist autopilot | 전략 수정, 코드/문서 반영, 테스트, issue sync, 최종 gatekeeping |
| 승빈 노트북 | support worker | 독립 seed/angle 실험, hybrid toy 재현, seed sweep 보조, 로컬 evidence 생성 |

이렇게 나누는 이유는 간단하다. 두 노트북이 동시에 source file을 고치고 push하면 충돌이 생긴다. 반대로 한 노트북은 코드를 개선하고, 다른 노트북은 같은 코드로 독립 실험 증거를 쌓으면 심사위원에게 보여줄 재현성/강건성 자료가 늘어난다.

## Support Worker가 하는 일

매 cycle마다 다음을 수행한다.

```text
safe git fetch/pull -> pytest -> submission quick
-> hybrid random-unitary + Hamiltonian toy seed/angle grid
-> optional 20-seed continuous sweep
-> pytest -> submission quick -> local status/progress 기록
```

중요한 제한:

- source file을 수정하지 않는다.
- GitHub issue를 수정하지 않는다.
- PR을 만들지 않는다.
- merge하지 않는다.
- 결과는 기본적으로 `results/`와 `logs/` 아래에만 저장되며 Git에 커밋하지 않는다.

## 승빈 노트북 실행 명령

이미 저장소가 있는 경우:

```powershell
cd C:\Coding\Hackathon\2026Quantum
git pull --ff-only origin main
.\scripts\run_problem_3_support_worker.ps1 -WorkerName seungbin -CycleMinutes 0 -KeepDisplayOff
```

가상환경까지 같이 준비하고 시작하고 싶으면:

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\bootstrap_problem_3_support_worker.ps1 -WorkerName seungbin -SetupEnv -KeepDisplayOff
```

PowerShell 창을 비워두고 백그라운드로 돌리고 싶으면 `-Detached`를 붙인다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\bootstrap_problem_3_support_worker.ps1 -WorkerName seungbin -SetupEnv -KeepDisplayOff -Detached
```

## 더 공격적인 7시간 실행 옵션

새벽에 오래 돌릴 때는 hybrid seed와 angle scale을 조금 더 넓힌다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\run_problem_3_support_worker.ps1 `
  -WorkerName seungbin `
  -CycleMinutes 0 `
  -KeepDisplayOff `
  -FullSeedSweepEvery 2 `
  -HybridSeeds 2026,2027,2028 `
  -AngleScales 0.5,1.0,3.141592653589793
```

노트북 성능이 부족하면 기본 명령을 사용한다. 기본 명령도 계속 cycle을 돌며 충분히 유용하다.

## 상태 확인

다른 PowerShell에서 확인한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
Get-Content results\problem_3_support_worker\seungbin\latest_status.md -Wait -Tail 120
```

진행 기록은 다음 파일에 남는다.

```powershell
Get-Content results\problem_3_support_worker\seungbin\progress_log.md -Wait -Tail 120
```

개별 실행 로그는 다음 폴더에 생긴다.

```text
logs/problem_3_support_worker/seungbin/
```

## 종료 방법

attached 실행이면 실행 중인 PowerShell에서 `Ctrl+C`를 누른다.

detached 실행이면 다음을 사용한다.

```powershell
cd C:\Coding\Hackathon\2026Quantum
.\scripts\stop_problem_3_support_worker.ps1 -WorkerName seungbin
```

## 지후에게 공유할 것

승빈 노트북에서 유의미한 결과가 나오면 아래 세 가지만 공유하면 된다.

- `results/problem_3_support_worker/seungbin/latest_status.md`
- 가장 최근 cycle의 `hybrid_toy_summary.md`
- seed sweep을 돌렸다면 `seed_sweep_summary.md`

결과 해석의 기준은 보수적으로 둔다. support worker 결과는 “추가 재현성 evidence” 또는 “appendix 후보”로 사용하고, 메인 claim은 지후 노트북의 finalist autopilot에서 통과한 결과만 사용한다.

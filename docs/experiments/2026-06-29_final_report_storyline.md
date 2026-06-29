# Problem 1/2 final report storyline draft

Owner: 임채진
Reviewer:

## Core question

Problem 1/2의 핵심 질문은 같은 2-qubit target ensemble `S0`와 같은 fidelity 기반 거리 위에서, random-unitary diffusion과 Hamiltonian projected diffusion이 얼마나 다르게 `S0`로부터 멀어지는지와 그 차이가 resource/control cost와 어떻게 연결되는지를 비교하는 것이다.

## Grounded facts from the current baseline design

- Target ensemble은 `|00>` 주변의 작은 2-qubit pure-state cluster로 둔다.
- 표준 설정은 `N=80`, `sigma=0.10`, seed `7`이며 최종 반복은 `7, 11, 23`을 권장한다.
- Random-unitary diffusion은 매 step마다 random single-qubit rotations와 2-qubit entangler를 적용한다.
- Hamiltonian projected diffusion은 2-qubit data system에 1 complement qubit을 붙이고, fixed 3-qubit Hamiltonian evolution 뒤 complement qubit projection으로 2-qubit ensemble을 만든다.
- 두 방식 모두 `F(psi, phi) = |<psi|phi>|^2`에서 정의한 fidelity-kernel MMD와 cost `1 - F` 기반 Wasserstein-type distance로 `S0`와의 거리를 잰다.
- Resource/control proxy는 random-unitary 쪽에서는 layer 수, random rotation 수, 2-qubit entangler 수, random control 수를 보고, Hamiltonian 쪽에서는 total evolution time, fixed Hamiltonian term 수, complement qubit 수, measurement basis 수를 본다.

## Claims to avoid until results are confirmed

- Hamiltonian projected diffusion이 random-unitary diffusion보다 항상 좋다고 말하지 않는다.
- 작은 2-qubit state-vector baseline에서 본 거리 곡선을 hardware-scale 성능으로 일반화하지 않는다.
- MMD나 Wasserstein-type distance 하나만 보고 diffusion quality 전체를 판단하지 않는다.
- Resource/control cost proxy를 실제 하드웨어 실행 시간, fidelity, noise robustness와 동일시하지 않는다.
- Problem 3 extension의 개선 주장은 같은 seed, 같은 target ensemble, 같은 metric으로 baseline과 비교된 뒤에만 쓴다.

## Physical interpretation frame

### Random-unitary diffusion

Random-unitary baseline은 `S0`의 작은 cluster를 각 layer의 random control로 점진적으로 흩뜨리는 방식이다. 해석의 초점은 거리 증가 속도, saturation 양상, 그리고 그 거리를 만들기 위해 필요한 random rotations와 entanglers의 수에 둔다.

### Hamiltonian projected diffusion

Hamiltonian projected baseline은 fixed Hamiltonian evolution과 complement projection을 통해 2-qubit data ensemble의 분포를 바꾸는 방식이다. 해석의 초점은 같은 metric에서 random-unitary와 비슷한 diffusion strength가 나타나는 구간이 있는지, time과 measurement basis에 따라 fluctuation이나 saturation이 생기는지, 그리고 random control을 줄이는 대신 total evolution time과 projection 선택이 비용으로 남는지에 둔다.

### Main comparison sentence

Random-unitary는 많은 layer별 control을 써서 diffusion curve를 직접 밀어붙이는 쪽이고, Hamiltonian projected diffusion은 fixed dynamics와 projection을 써서 control freedom을 줄이는 대신 time schedule과 measurement choice에 민감한 diffusion curve를 얻는 쪽이다.

## Report outline draft

1. Problem setting
   - 2026 QML 지정문제 3번의 목표를 작은 state-vector baseline으로 재현한다고 밝힌다.
   - `S0`, diffusion trajectory, fidelity 기반 metric을 정의한다.
   - 이 보고서의 질문을 "diffusion behavior와 control/resource cost의 공정한 비교"로 좁힌다.

2. Target ensemble and metrics
   - `|00>` 주변 2-qubit target ensemble 생성 방식을 설명한다.
   - Fidelity, MMD, Wasserstein-type distance를 같은 비교 언어로 제시한다.
   - 두 metric이 보는 차이를 짧게 구분한다: kernel 평균 차이와 matching cost 차이.

3. Baseline A: random-unitary diffusion
   - Single-qubit random rotations와 entangler layer 구조를 설명한다.
   - Plot에서는 step `k`에 따른 `dist(S_k, S0)`를 보여준다.
   - 해석은 거리 증가, saturation 여부, layer/control 증가 비용에 묶는다.

4. Baseline B: Hamiltonian projected diffusion
   - 2 data qubits + 1 complement qubit 구조와 fixed Hamiltonian을 설명한다.
   - Complement projection으로 다시 2-qubit ensemble을 얻는 흐름을 그림으로 보여준다.
   - Plot에서는 evolution time `t`에 따른 `dist(S_t^Ham, S0)`를 보여준다.
   - 해석은 fluctuation, saturation, basis sensitivity, fixed-control 장점과 time/projection 비용에 묶는다.

5. Side-by-side comparison
   - 같은 `S0`, 같은 seed, 같은 metric, 같은 sample size로 비교했다는 점을 먼저 둔다.
   - Distance curve 표와 resource/control proxy 표를 나란히 놓는다.
   - 핵심 판단은 "어느 쪽이 더 좋은가"가 아니라 "비슷한 diffusion strength를 얻을 때 무엇을 더 쓰고 무엇을 덜 쓰는가"로 쓴다.

6. Link to Problem 3 extension
   - Problem 3은 위 비교에서 드러난 trade-off 하나를 줄이는 작은 개입으로 소개한다.
   - 후보는 measurement basis sweep, time schedule 조정, shallow denoising map, noise-aware proxy 중 하나로 제한한다.
   - 개선 주장은 baseline 대비 같은 metric에서 확인된 항목만 적고, 악화된 항목도 함께 적는다.

7. Limitations
   - 2-qubit pure-state toy baseline이므로 large-system 또는 hardware result가 아니라고 명시한다.
   - Resource proxy는 실제 transpiled circuit depth나 device noise를 대체하지 않는다고 적는다.
   - Seed 1개 결과는 예비 결과이며, 최종 표에는 seed sweep 결과를 넣는다고 적는다.

8. Conclusion
   - Random-unitary와 Hamiltonian projected diffusion의 물리적 차이를 같은 metric 위에서 비교했다는 점을 요약한다.
   - Resource/control cost 비교가 Problem 3의 개선 방향을 정당화한다고 연결한다.
   - 최종 주장은 "작은 예제에서 확인한 trade-off" 범위 안에 둔다.

## Presentation outline draft

1. Opening slide: One question
   - "같은 target ensemble을 얼마나 다르게 diffuse하고, 그 비용은 무엇인가?"

2. Setup slide
   - `S0`, two diffusion mechanisms, two metrics를 한 장에 배치한다.

3. Random-unitary slide
   - Mechanism diagram, distance curve, resource proxy를 함께 보여준다.
   - 말할 포인트: strong direct control, increasing layer/control cost.

4. Hamiltonian projected slide
   - 2 data qubits + 1 complement qubit, fixed Hamiltonian, projection 흐름을 보여준다.
   - 말할 포인트: reduced random control, sensitivity to time/projection choice.

5. Comparison slide
   - Distance curve와 resource/control table을 나란히 둔다.
   - 말할 포인트: diffusion strength만이 아니라 cost의 종류가 다르다.

6. Extension slide
   - 선택한 작은 개입 하나와 baseline 대비 변화만 보여준다.
   - 말할 포인트: improvement and sacrifice를 동시에 제시한다.

7. Closing slide
   - "Fixed dynamics plus projection can be a controlled alternative to layer-wise random unitaries, but the useful regime must be identified by metric and cost together."

## Evidence slots to fill after baseline execution

| Evidence | Source file | How it supports the story |
| --- | --- | --- |
| Random-unitary MMD/Wasserstein curve | `results/problem_1_2_baseline/random_unitary_metrics.csv` | step별 cluster spreading과 saturation 해석 |
| Hamiltonian MMD/Wasserstein curve | `results/problem_1_2_baseline/hamiltonian_metrics.csv` | time별 fluctuation과 projection-induced diffusion 해석 |
| Resource/control proxy table | `results/problem_1_2_baseline/resource_proxies.csv` | diffusion strength와 control/resource cost 연결 |
| Combined plot | `results/problem_1_2_baseline/distance_curves.png` | 발표용 side-by-side comparison |

## Next

- Baseline 실행 결과가 생성되면 위 evidence slots를 실제 수치와 figure로 채운다.
- 최종 보고서에는 seed `7, 11, 23` 반복 결과가 준비된 범위까지만 주장한다.
- 발표 문장은 "우리가 확인한 작은 예제에서는"이라는 범위를 유지한다.

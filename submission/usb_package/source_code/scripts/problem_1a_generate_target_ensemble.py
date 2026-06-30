"""Compatibility entry point for Problem 1-(a).

The original repository started with this root-level script. Keep it as a
small runnable check, while the reusable implementation lives under src/.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_cylinder.problem_1a_target_ensemble import target_ensemble


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    n_samples = 100
    sigma = 0.10
    s0 = target_ensemble(n_samples=n_samples, sigma=sigma, seed=7)

    print(f"앙상블 S_0 크기: {len(s0)}")
    print(f"첫 번째 샘플의 상태 벡터:\n{s0[0]}")


if __name__ == "__main__":
    main()

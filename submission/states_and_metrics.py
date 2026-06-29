from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import numpy as np

from quantum_cylinder.implementations.qiskit.problem_1a_target_ensemble import target_ensemble
from quantum_cylinder.problem_1b_ensemble_metrics import mmd_fidelity, wasserstein_infidelity


def make_target_ensemble(n_samples: int = 80, sigma: float = 0.10, seed: int = 7) -> np.ndarray:
    """Problem 1(a): states near |00> made by small random single-qubit rotations."""
    return target_ensemble(n_samples=n_samples, sigma=sigma, seed=seed)


def distance_to_target(target: np.ndarray, candidate: np.ndarray) -> dict[str, float]:
    """Use the same two metrics for all three problems."""
    return {
        "mmd": float(mmd_fidelity(target, candidate)),
        "wasserstein": float(wasserstein_infidelity(target, candidate)),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

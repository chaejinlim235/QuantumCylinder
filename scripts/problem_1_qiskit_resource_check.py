from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    from qiskit import QuantumCircuit
except ImportError:
    print('Qiskit is not installed. Run: pip install -e ".[qiskit]"')
    raise SystemExit(0)


def build_problem_1_layer_circuit(n_steps: int = 12, entangler: str = "cz") -> QuantumCircuit:
    if n_steps < 0:
        raise ValueError("n_steps must be non-negative.")
    if entangler not in {"cz", "cx"}:
        raise ValueError("entangler must be either 'cz' or 'cx'.")

    circuit = QuantumCircuit(2, name="problem_1_random_unitary_template")
    for step in range(n_steps):
        for qubit in range(2):
            circuit.rx(0.0, qubit)
            circuit.ry(0.0, qubit)
            circuit.rz(0.0, qubit)
        if entangler == "cz":
            circuit.cz(0, 1)
        else:
            circuit.cx(0, 1)
        if step != n_steps - 1:
            circuit.barrier()
    return circuit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Qiskit resource proxy for Problem 1 random-unitary layers.")
    parser.add_argument("--steps", type=int, default=12)
    parser.add_argument("--entangler", choices=["cz", "cx"], default="cz")
    parser.add_argument("--draw", type=Path, default=None, help="Optional text circuit output path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    circuit = build_problem_1_layer_circuit(args.steps, entangler=args.entangler)
    counts = circuit.count_ops()

    print("Problem 1 Qiskit resource proxy")
    print(f"steps: {args.steps}")
    print(f"entangler: {args.entangler}")
    print(f"depth: {circuit.depth()}")
    print(f"ops: {dict(counts)}")
    print(f"single_qubit_rotations: {args.steps * 2 * 3}")
    print(f"two_qubit_entanglers: {args.steps}")

    if args.draw is not None:
        args.draw.parent.mkdir(parents=True, exist_ok=True)
        args.draw.write_text(str(circuit.draw(output="text")), encoding="utf-8")
        print(f"wrote circuit text drawing to {args.draw}")


if __name__ == "__main__":
    main()

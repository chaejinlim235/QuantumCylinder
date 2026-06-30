"""Optional IBM QPU smoke-test path for tiny representative circuits.

Default behavior is a dry-run. No IBM Quantum job is submitted unless
``--submit`` is passed explicitly.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _backend_name(backend: Any | None) -> str | None:
    if backend is None:
        return None
    name = getattr(backend, "name", None)
    if callable(name):
        return str(name())
    if name is not None:
        return str(name)
    return str(backend)


def _backend_num_qubits(backend: Any | None) -> int | None:
    if backend is None:
        return None
    num_qubits = getattr(backend, "num_qubits", None)
    if isinstance(num_qubits, int):
        return num_qubits
    configuration = getattr(backend, "configuration", None)
    if callable(configuration):
        try:
            return int(configuration().num_qubits)
        except Exception:
            return None
    return None


def _build_representative_circuits(max_circuits: int):
    from qiskit import QuantumCircuit

    circuits = []

    qc1 = QuantumCircuit(2, name="problem1_random_unitary_one_step")
    qc1.ry(0.17, 0)
    qc1.rz(-0.23, 1)
    qc1.cx(0, 1)
    qc1.rx(0.31, 0)
    qc1.ry(-0.19, 1)
    qc1.measure_all()
    circuits.append(qc1)

    qc2 = QuantumCircuit(3, name="hamiltonian_projection_tiny_proxy")
    qc2.ry(0.11, 0)
    qc2.rx(-0.08, 1)
    qc2.h(2)
    qc2.cx(0, 2)
    qc2.rz(0.35, 2)
    qc2.cx(0, 2)
    qc2.cx(1, 2)
    qc2.rz(-0.21, 2)
    qc2.cx(1, 2)
    qc2.ry(0.18, 0)
    qc2.measure_all()
    circuits.append(qc2)

    qc3 = QuantumCircuit(3, name="two_way_postselection_tiny_proxy")
    qc3.ry(0.11, 0)
    qc3.rx(-0.08, 1)
    for angle in (0.22, -0.17):
        qc3.h(2)
        qc3.cx(0, 2)
        qc3.rz(angle, 2)
        qc3.cx(0, 2)
        qc3.cx(1, 2)
        qc3.rz(-angle / 2.0, 2)
        qc3.cx(1, 2)
    qc3.measure_all()
    circuits.append(qc3)

    return circuits[:max_circuits]


def _two_qubit_gate_count(circuit: Any) -> int:
    count = 0
    for item in circuit.data:
        operation = getattr(item, "operation", None)
        if operation is None:
            operation = item[0]
        if getattr(operation, "num_qubits", None) == 2:
            count += 1
    return count


def _transpile_circuits(circuits: list[Any], backend: Any | None) -> tuple[list[Any], str]:
    from qiskit import transpile

    if backend is not None:
        try:
            from qiskit.transpiler.preset_passmanagers import (
                generate_preset_pass_manager,
            )

            pass_manager = generate_preset_pass_manager(
                optimization_level=1,
                backend=backend,
            )
            return [pass_manager.run(circuit) for circuit in circuits], "preset_pass_manager"
        except Exception:
            transpiled = transpile(circuits, backend=backend, optimization_level=1)
            return list(transpiled), "qiskit_transpile_backend"

    transpiled = transpile(circuits, optimization_level=1)
    return list(transpiled), "qiskit_transpile_generic"


def _load_runtime_service() -> tuple[Any | None, str, bool]:
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
    except Exception as exc:
        return None, f"qiskit-ibm-runtime unavailable: {exc}", False

    token = os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")
    instance = os.environ.get("QISKIT_IBM_INSTANCE")
    kwargs: dict[str, str] = {}
    if token:
        kwargs["token"] = token
    if instance:
        kwargs["instance"] = instance

    try:
        service = QiskitRuntimeService(channel="ibm_quantum", **kwargs)
        source = "environment token" if token else "saved Qiskit Runtime account"
        return service, f"loaded from {source}", True
    except TypeError:
        try:
            service = QiskitRuntimeService(**kwargs)
            source = "environment token" if token else "saved Qiskit Runtime account"
            return service, f"loaded from {source}", True
        except Exception as exc:
            return None, f"runtime service unavailable: {exc}", True
    except Exception as exc:
        return None, f"runtime service unavailable: {exc}", True


def _select_backend(service: Any, backend_name: str | None, min_qubits: int) -> tuple[Any | None, str]:
    if service is None:
        return None, "no runtime service"

    if backend_name:
        try:
            return service.backend(backend_name), f"requested backend {backend_name}"
        except Exception as exc:
            return None, f"requested backend unavailable: {exc}"

    try:
        backend = service.least_busy(
            operational=True,
            simulator=False,
            min_num_qubits=min_qubits,
        )
        return backend, "least-busy operational non-simulator backend"
    except Exception as exc:
        return None, f"least-busy backend selection unavailable: {exc}"


def _submit_job(
    primitive: str,
    circuits: list[Any],
    backend: Any,
    shots: int,
) -> tuple[str | None, str | None, str | None]:
    try:
        if primitive == "sampler":
            try:
                from qiskit_ibm_runtime import SamplerV2 as Sampler

                sampler = Sampler(mode=backend)
                job = sampler.run(circuits, shots=shots)
            except ImportError:
                from qiskit_ibm_runtime import Sampler

                sampler = Sampler(backend=backend)
                job = sampler.run(circuits, shots=shots)
        else:
            from qiskit.quantum_info import SparsePauliOp

            observables = [
                SparsePauliOp.from_list([("Z" * circuit.num_qubits, 1.0)])
                for circuit in circuits
            ]
            try:
                from qiskit_ibm_runtime import EstimatorV2 as Estimator

                estimator = Estimator(mode=backend)
                pubs = list(zip(circuits, observables))
                job = estimator.run(pubs)
            except ImportError:
                from qiskit_ibm_runtime import Estimator

                estimator = Estimator(backend=backend)
                job = estimator.run(circuits, observables)

        job_id = job.job_id() if callable(getattr(job, "job_id", None)) else str(job.job_id)
        status = None
        try:
            raw_status = job.status()
            status = str(raw_status)
        except Exception:
            status = "submitted"
        return job_id, status, None
    except Exception as exc:
        return None, None, str(exc)


def _write_outputs(report: dict[str, Any], save_dir: Path) -> None:
    save_dir.mkdir(parents=True, exist_ok=True)
    (save_dir / "ibm_qpu_smoke_test_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# IBM QPU Smoke-Test Summary",
        "",
        f"- generated_at_utc: `{report['generated_at_utc']}`",
        f"- dry_run: `{report['dry_run']}`",
        f"- submitted: `{report['submitted']}`",
        f"- primitive: `{report['primitive']}`",
        f"- shots: `{report['shots']}`",
        f"- backend_selected: `{report['backend_selected']}`",
        f"- runtime_status: {report['runtime_status']}",
        f"- backend_selection_status: {report['backend_selection_status']}",
        "",
        "## Circuits",
        "",
    ]
    for circuit in report["circuits"]:
        lines.extend(
            [
                f"- `{circuit['name']}`: qubits `{circuit['num_qubits']}`, "
                f"depth `{circuit['transpiled_depth']}`, "
                f"two-qubit gates `{circuit['two_qubit_gate_count']}`",
            ]
        )
    if report.get("job_id"):
        lines.append(f"- job_id: `{report['job_id']}`")
    if report.get("job_status"):
        lines.append(f"- job_status: `{report['job_status']}`")
    if report.get("submit_error"):
        lines.append(f"- submit_error: `{report['submit_error']}`")
    lines.extend(
        [
            "",
            "This is optional hardware-execution validation only. It does not replace",
            "the reproducible state-vector benchmark and does not imply hardware advantage.",
            "",
        ]
    )
    (save_dir / "ibm_qpu_smoke_test_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Force no-submit mode.")
    parser.add_argument("--backend", default=None, help="IBM backend name.")
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--max-circuits", type=int, default=3)
    parser.add_argument("--primitive", choices=["sampler", "estimator"], default="sampler")
    parser.add_argument("--submit", action="store_true", help="Submit a real IBM QPU job.")
    parser.add_argument(
        "--save-dir",
        default="results/ibm_qpu_validation",
        help="Output directory for JSON and Markdown reports.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dry_run = True if args.dry_run or not args.submit else False
    max_circuits = max(1, min(args.max_circuits, 3))

    try:
        circuits = _build_representative_circuits(max_circuits)
    except Exception as exc:
        print(f"Qiskit circuit construction failed: {exc}")
        return 1

    min_qubits = max(circuit.num_qubits for circuit in circuits)
    service, runtime_status, runtime_available = _load_runtime_service()
    backend, backend_selection_status = _select_backend(service, args.backend, min_qubits)

    transpiled, transpile_method = _transpile_circuits(circuits, backend)
    circuit_rows = []
    for original, compiled in zip(circuits, transpiled):
        circuit_rows.append(
            {
                "name": original.name,
                "num_qubits": original.num_qubits,
                "original_depth": original.depth(),
                "transpiled_depth": compiled.depth(),
                "two_qubit_gate_count": _two_qubit_gate_count(compiled),
                "operation_counts": dict(compiled.count_ops()),
            }
        )

    job_id = None
    job_status = None
    submit_error = None
    submitted = False
    if not dry_run:
        if backend is None:
            submit_error = "No IBM backend selected; no job submitted."
        elif not runtime_available:
            submit_error = "qiskit-ibm-runtime is unavailable; no job submitted."
        else:
            job_id, job_status, submit_error = _submit_job(
                args.primitive,
                transpiled,
                backend,
                args.shots,
            )
            submitted = job_id is not None

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "submitted": submitted,
        "shots": args.shots,
        "primitive": args.primitive,
        "requested_backend": args.backend,
        "backend_selected": _backend_name(backend),
        "backend_num_qubits": _backend_num_qubits(backend),
        "required_num_qubits": min_qubits,
        "runtime_status": runtime_status,
        "backend_selection_status": backend_selection_status,
        "transpile_method": transpile_method,
        "circuits": circuit_rows,
        "job_id": job_id,
        "job_status": job_status,
        "submit_error": submit_error,
        "counts_or_expectation_values": None,
        "claim_guardrail": (
            "Optional IBM QPU validation only; state-vector benchmark remains "
            "the source of MMD/Wasserstein claims."
        ),
    }

    save_dir = Path(args.save_dir)
    _write_outputs(report, save_dir)

    print(f"IBM QPU smoke test report saved to {save_dir}")
    print(f"dry_run={dry_run} submitted={submitted} backend={report['backend_selected']}")
    print("No token was printed or saved.")
    return 0 if dry_run or submitted else 1


if __name__ == "__main__":
    raise SystemExit(main())

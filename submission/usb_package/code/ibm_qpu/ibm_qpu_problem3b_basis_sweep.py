"""IBM QPU appendix validation for Problem 3-b measurement-basis control.

Default behavior is dry-run/transpilation only. No IBM Quantum job is
submitted unless ``--submit`` is passed explicitly.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HX = 0.8090
HY = 0.9045
J_COUPLING = 1.0
BETAS = [0.0, math.pi / 4.0, math.pi / 2.0, 3.0 * math.pi / 4.0]
TWO_QUBIT_OPS = {"cx", "cz", "ecr", "rxx"}
CLAIM_GUARDRAIL = (
    "This is appendix validation only. The main scientific claims remain "
    "state-vector based. No hardware advantage is claimed."
)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def _status_text(job: Any) -> str:
    try:
        status = job.status()
    except Exception as exc:
        return f"status unavailable: {exc}"
    name = getattr(status, "name", None)
    if name:
        return str(name)
    return str(status)


def _job_id(job: Any) -> str:
    job_id = getattr(job, "job_id", None)
    if callable(job_id):
        return str(job_id())
    return str(job_id)


def _has_credentials() -> tuple[bool, list[str]]:
    missing = []
    if not (os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")):
        missing.append("QISKIT_IBM_TOKEN or IBM_QUANTUM_TOKEN")
    if not os.environ.get("QISKIT_IBM_INSTANCE"):
        missing.append("QISKIT_IBM_INSTANCE")
    return not missing, missing


def _load_runtime(channel: str) -> tuple[Any | None, Any | None, str, str | None]:
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
    except Exception as exc:
        return None, None, f"qiskit-ibm-runtime unavailable: {exc}", "SamplerV2 not checked"

    try:
        from qiskit_ibm_runtime import SamplerV2 as Sampler

        sampler_status = "SamplerV2 available"
    except Exception as exc:
        Sampler = None
        sampler_status = f"SamplerV2 unavailable: {exc}"

    credentials_available, missing = _has_credentials()
    if not credentials_available:
        return (
            None,
            Sampler,
            "missing IBM credentials: " + ", ".join(missing),
            sampler_status,
        )

    kwargs = {
        "token": os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN"),
        "instance": os.environ.get("QISKIT_IBM_INSTANCE"),
    }
    try:
        service = QiskitRuntimeService(channel=channel, **kwargs)
        return service, Sampler, "loaded from environment credentials", sampler_status
    except Exception as exc:
        return None, Sampler, f"runtime service unavailable: {exc}", sampler_status


def _select_backend(service: Any | None, backend_name: str) -> tuple[Any | None, str]:
    if service is None:
        return None, "no runtime service"
    try:
        return service.backend(backend_name), f"requested backend {backend_name}"
    except Exception as exc:
        return None, f"requested backend unavailable: {exc}"


def _build_circuits(repeats: int, trotter_steps: int, dt: float) -> tuple[list[Any], list[dict[str, Any]]]:
    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    from qiskit.circuit.library import RXXGate

    circuits = []
    metadata_rows = []
    index = 0
    for repeat in range(repeats):
        for beta in BETAS:
            qreg = QuantumRegister(3, "q")
            creg = ClassicalRegister(3, "meas")
            beta_over_pi = beta / math.pi
            name = f"p3b_beta_{beta_over_pi:.2f}pi_rep_{repeat}"
            qc = QuantumCircuit(qreg, creg, name=name)

            # Small S0-like preparation near |00> on the data qubits.
            qc.ry(0.045 + 0.010 * repeat, qreg[0])
            qc.rx(-0.035 + 0.006 * repeat, qreg[1])
            qc.rz(0.020 * (repeat + 1), qreg[0])
            qc.ry(-0.015 * (repeat + 1), qreg[1])

            for _ in range(trotter_steps):
                for q in range(3):
                    qc.rx(2.0 * HX * dt, qreg[q])
                    qc.ry(2.0 * HY * dt, qreg[q])
                qc.append(RXXGate(2.0 * J_COUPLING * dt), [qreg[0], qreg[1]])
                qc.append(RXXGate(2.0 * J_COUPLING * dt), [qreg[1], qreg[2]])

            qc.ry(-beta, qreg[2])
            qc.measure(qreg[0], creg[0])
            qc.measure(qreg[1], creg[1])
            qc.measure(qreg[2], creg[2])

            circuits.append(qc)
            metadata_rows.append(
                {
                    "index": index,
                    "circuit_name": name,
                    "beta": beta,
                    "beta_over_pi": beta_over_pi,
                    "repeat": repeat,
                }
            )
            index += 1

    return circuits, metadata_rows


def _two_qubit_gate_count(circuit: Any) -> int:
    counts = circuit.count_ops()
    return int(sum(int(counts.get(op, 0)) for op in TWO_QUBIT_OPS))


def _transpile_circuits(circuits: list[Any], backend: Any | None) -> tuple[list[Any], str, str | None]:
    from qiskit import transpile

    if backend is not None:
        try:
            from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

            pass_manager = generate_preset_pass_manager(
                optimization_level=1,
                backend=backend,
            )
            return [pass_manager.run(circuit) for circuit in circuits], "preset_pass_manager", None
        except Exception as exc:
            try:
                transpiled = transpile(circuits, backend=backend, optimization_level=1)
                return list(transpiled), "qiskit_transpile_backend", str(exc)
            except Exception as fallback_exc:
                return circuits, "transpile_failed_returned_original", str(fallback_exc)

    try:
        transpiled = transpile(circuits, optimization_level=1)
        return list(transpiled), "qiskit_transpile_generic", None
    except Exception as exc:
        return circuits, "generic_transpile_failed_returned_original", str(exc)


def _circuit_rows(
    original_circuits: list[Any],
    transpiled_circuits: list[Any],
    metadata_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for original, compiled, metadata in zip(original_circuits, transpiled_circuits, metadata_rows):
        ops = dict(compiled.count_ops())
        row = {
            **metadata,
            "original_depth": original.depth(),
            "transpiled_depth": compiled.depth(),
            "transpiled_ops": ops,
            "two_qubit_gate_count": _two_qubit_gate_count(compiled),
        }
        rows.append(row)
    return rows


def _normalize_bitstring(key: Any, num_bits: int) -> str | None:
    if isinstance(key, int):
        return format(key, f"0{num_bits}b")
    text = str(key).replace(" ", "")
    if text.startswith("0b"):
        text = text[2:]
    if not text or any(ch not in "01" for ch in text):
        return None
    return text.zfill(num_bits)[-num_bits:]


def _counts_from_bitarray(bitarray: Any, num_bits: int) -> dict[str, int] | None:
    for method_name in ("get_counts", "get_int_counts"):
        method = getattr(bitarray, method_name, None)
        if callable(method):
            try:
                raw_counts = method()
            except TypeError:
                try:
                    raw_counts = method(0)
                except Exception:
                    continue
            except Exception:
                continue
            counts: dict[str, int] = {}
            for key, value in dict(raw_counts).items():
                normalized = _normalize_bitstring(key, num_bits)
                if normalized is not None:
                    counts[normalized] = counts.get(normalized, 0) + int(value)
            if counts:
                return counts

    to_bool_array = getattr(bitarray, "to_bool_array", None)
    if callable(to_bool_array):
        try:
            array = to_bool_array()
            counts = Counter()
            for shot in array.reshape((-1, array.shape[-1])):
                bitstring = "".join("1" if bit else "0" for bit in shot[::-1])
                normalized = _normalize_bitstring(bitstring, num_bits)
                if normalized is not None:
                    counts[normalized] += 1
            if counts:
                return dict(counts)
        except Exception:
            return None

    return None


def _extract_counts(result: Any, num_bits: int = 3) -> list[dict[str, Any]]:
    if result is None:
        return []

    try:
        pub_results = list(result)
    except TypeError:
        pub_results = [result]

    extracted = []
    for pub_index, pub_result in enumerate(pub_results):
        data = getattr(pub_result, "data", None)
        if data is None:
            data = pub_result

        candidates = []
        for name in ("meas", "c"):
            value = getattr(data, name, None)
            if value is not None:
                candidates.append((name, value))

        if not candidates:
            for name in dir(data):
                if name.startswith("_"):
                    continue
                try:
                    value = getattr(data, name)
                except Exception:
                    continue
                if hasattr(value, "get_counts") or hasattr(value, "get_int_counts"):
                    candidates.append((name, value))

        for register, bitarray in candidates:
            counts = _counts_from_bitarray(bitarray, num_bits)
            if counts:
                extracted.append(
                    {
                        "pub_index": pub_index,
                        "register": register,
                        "counts": counts,
                    }
                )
                break

    return extracted


def _entropy(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    value = 0.0
    for count in counts.values():
        if count <= 0:
            continue
        probability = count / total
        value -= probability * math.log2(probability)
    return value


def _analyze_counts(
    counts_entries: list[dict[str, Any]],
    circuit_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_index = {entry["pub_index"]: entry["counts"] for entry in counts_entries}
    analysis_rows = []
    grouped: dict[float, list[dict[str, Any]]] = defaultdict(list)

    for row in circuit_rows:
        index = int(row["index"])
        counts = by_index.get(index)
        if not counts:
            continue
        total_shots = int(sum(int(value) for value in counts.values()))
        selected = Counter()
        success_f0 = 0
        for bitstring, count in counts.items():
            normalized = _normalize_bitstring(bitstring, 3)
            if normalized is None:
                continue
            if normalized[0] == "0":
                success_f0 += int(count)
                selected[normalized[1:]] += int(count)

        success_probability = success_f0 / total_shots if total_shots else 0.0
        entropy = _entropy(dict(selected))
        analysis = {
            "index": index,
            "circuit_name": row["circuit_name"],
            "beta": row["beta"],
            "beta_over_pi": row["beta_over_pi"],
            "repeat": row["repeat"],
            "total_shots": total_shots,
            "success_F0": success_f0,
            "success_probability_F0": success_probability,
            "selected_data_counts_F0": dict(sorted(selected.items())),
            "selected_data_entropy_F0": entropy,
        }
        analysis_rows.append(analysis)
        grouped[float(row["beta"])].append(analysis)

    aggregate_rows = []
    for beta in BETAS:
        rows = grouped.get(beta, [])
        if not rows:
            continue
        success_values = [float(item["success_probability_F0"]) for item in rows]
        entropy_values = [float(item["selected_data_entropy_F0"]) for item in rows]
        aggregate_rows.append(
            {
                "beta": beta,
                "beta_over_pi": beta / math.pi,
                "mean_success_probability_F0": statistics.mean(success_values),
                "std_success_probability_F0": statistics.stdev(success_values)
                if len(success_values) > 1
                else 0.0,
                "mean_selected_data_entropy_F0": statistics.mean(entropy_values),
                "std_selected_data_entropy_F0": statistics.stdev(entropy_values)
                if len(entropy_values) > 1
                else 0.0,
                "num_repeats": len(rows),
            }
        )

    return analysis_rows, aggregate_rows


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            serializable = {
                key: json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else value
                for key, value in row.items()
            }
            writer.writerow({key: serializable.get(key, "") for key in fieldnames})


def _write_summary(report: dict[str, Any], aggregate_rows: list[dict[str, Any]], save_dir: Path) -> None:
    lines = [
        "# IBM QPU Problem 3-b Basis Sweep Summary",
        "",
        "This is a tiny IBM QPU validation of the Problem 3-b measurement-basis trade-off mechanism.",
        "",
        f"- generated_at_utc: `{report['generated_at_utc']}`",
        f"- backend: `{report['backend_selected']}`",
        f"- requested_backend: `{report['backend_requested']}`",
        f"- shots: `{report['shots']}`",
        f"- repeats: `{report['repeats']}`",
        f"- num_circuits: `{report['num_circuits']}`",
        f"- dt: `{report['dt']}`",
        f"- trotter_steps: `{report['trotter_steps']}`",
        f"- submitted: `{report['submitted']}`",
        f"- job_id: `{report.get('job_id')}`",
        f"- job_status: `{report.get('job_status')}`",
        f"- runtime_status: {report['runtime_status']}",
        f"- sampler_status: {report['sampler_status']}",
        "",
        f"Claim guardrail: {CLAIM_GUARDRAIL}",
        "",
    ]

    if aggregate_rows:
        lines.extend(
            [
                "## Aggregate By Basis",
                "",
                "| beta/pi | mean p(F=0) | std p(F=0) | mean selected entropy | std selected entropy | repeats |",
                "| ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in aggregate_rows:
            lines.append(
                "| "
                f"{row['beta_over_pi']:.4f} | "
                f"{row['mean_success_probability_F0']:.6f} | "
                f"{row['std_success_probability_F0']:.6f} | "
                f"{row['mean_selected_data_entropy_F0']:.6f} | "
                f"{row['std_selected_data_entropy_F0']:.6f} | "
                f"{row['num_repeats']} |"
            )
        lines.append("")
    else:
        lines.extend(
            [
                "## Aggregate By Basis",
                "",
                "No shot-count aggregate is available yet. In dry-run mode the script saves",
                "transpilation metadata only. Run with `--submit` or `--retrieve-job` to",
                "extract p(F=0) and selected-data entropy.",
                "",
            ]
        )

    if report.get("submit_error"):
        lines.extend(["## Submit/Retrieve Note", "", str(report["submit_error"]), ""])

    lines.extend(
        [
            "Interpretation: if the aggregate table is present, changes across beta show",
            "that rotating the complement-qubit measurement basis changes the effective",
            "post-selected map through both success probability and the selected data",
            "distribution. This appendix check does not replace the state-vector",
            "MMD/Wasserstein benchmark.",
            "",
        ]
    )

    (save_dir / "problem3b_ibm_basis_sweep_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def _write_outputs(
    report: dict[str, Any],
    circuit_rows: list[dict[str, Any]],
    analysis_rows: list[dict[str, Any]],
    aggregate_rows: list[dict[str, Any]],
    counts_entries: list[dict[str, Any]],
    save_dir: Path,
) -> None:
    save_dir.mkdir(parents=True, exist_ok=True)
    (save_dir / "problem3b_ibm_basis_sweep_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_summary(report, aggregate_rows, save_dir)
    _write_csv(
        save_dir / "problem3b_ibm_basis_sweep_circuits.csv",
        circuit_rows,
        [
            "index",
            "circuit_name",
            "beta",
            "beta_over_pi",
            "repeat",
            "original_depth",
            "transpiled_depth",
            "transpiled_ops",
            "two_qubit_gate_count",
        ],
    )
    _write_csv(
        save_dir / "problem3b_ibm_basis_sweep_aggregate.csv",
        aggregate_rows,
        [
            "beta",
            "beta_over_pi",
            "mean_success_probability_F0",
            "std_success_probability_F0",
            "mean_selected_data_entropy_F0",
            "std_selected_data_entropy_F0",
            "num_repeats",
        ],
    )
    if analysis_rows:
        _write_csv(
            save_dir / "problem3b_ibm_basis_sweep_per_circuit_analysis.csv",
            analysis_rows,
            [
                "index",
                "circuit_name",
                "beta",
                "beta_over_pi",
                "repeat",
                "total_shots",
                "success_F0",
                "success_probability_F0",
                "selected_data_counts_F0",
                "selected_data_entropy_F0",
            ],
        )
    if counts_entries:
        (save_dir / "problem3b_ibm_basis_sweep_counts.json").write_text(
            json.dumps(counts_entries, indent=2, sort_keys=True),
            encoding="utf-8",
        )


def _run_sampler(Sampler: Any, backend: Any, circuits: list[Any], shots: int) -> Any:
    if Sampler is None:
        raise RuntimeError("SamplerV2 is unavailable; cannot submit a SamplerV2 job.")
    sampler = Sampler(mode=backend)
    return sampler.run(circuits, shots=shots)


def _wait_for_job(job: Any, wait_minutes: float) -> str:
    deadline = time.time() + max(0.0, wait_minutes) * 60.0
    status = _status_text(job)
    while wait_minutes > 0.0 and time.time() < deadline:
        if status.upper() in {"DONE", "CANCELLED", "ERROR"}:
            return status
        time.sleep(20)
        status = _status_text(job)
    return status


def _retrieve_result_if_done(job: Any, status: str) -> tuple[Any | None, str | None]:
    if status.upper() != "DONE":
        return None, None
    try:
        return job.result(), None
    except Exception as exc:
        return None, f"result retrieval failed: {exc}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", default="ibm_fez", help="IBM backend name.")
    parser.add_argument("--shots", type=int, default=2048)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--trotter-steps", type=int, default=1)
    parser.add_argument("--dt", type=float, default=0.20)
    parser.add_argument("--submit", action="store_true", help="Submit a real IBM QPU job.")
    parser.add_argument("--wait-minutes", type=float, default=0.0)
    parser.add_argument(
        "--save-dir",
        default="results/ibm_qpu_validation/problem3b_basis_sweep",
        help="Output directory.",
    )
    parser.add_argument("--retrieve-job", default=None, help="Existing IBM Runtime job id.")
    parser.add_argument(
        "--channel",
        default=os.environ.get("QISKIT_IBM_CHANNEL", "ibm_cloud"),
        help="Qiskit Runtime channel.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repeats = max(1, int(args.repeats))
    trotter_steps = max(1, int(args.trotter_steps))
    save_dir = Path(args.save_dir)

    try:
        circuits, metadata_rows = _build_circuits(repeats, trotter_steps, float(args.dt))
    except Exception as exc:
        save_dir.mkdir(parents=True, exist_ok=True)
        failure_report = {
            "generated_at_utc": _timestamp(),
            "error": f"circuit construction failed: {exc}",
            "claim_guardrail": CLAIM_GUARDRAIL,
        }
        (save_dir / "problem3b_ibm_basis_sweep_report.json").write_text(
            json.dumps(failure_report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        print(f"Circuit construction failed; report saved to {save_dir}")
        return 1

    service, Sampler, runtime_status, sampler_status = _load_runtime(args.channel)
    backend, backend_selection_status = _select_backend(service, args.backend)
    transpiled, transpile_method, transpile_warning = _transpile_circuits(circuits, backend)
    circuit_rows = _circuit_rows(circuits, transpiled, metadata_rows)

    submitted = False
    job_id = args.retrieve_job
    job_status = None
    submit_error = None
    retrieve_error = None
    counts_entries: list[dict[str, Any]] = []
    analysis_rows: list[dict[str, Any]] = []
    aggregate_rows: list[dict[str, Any]] = []

    if args.retrieve_job:
        if service is None:
            retrieve_error = "No IBM Runtime service available; cannot retrieve job."
        else:
            try:
                job = service.job(args.retrieve_job)
                job_status = _status_text(job)
                result, retrieve_error = _retrieve_result_if_done(job, job_status)
                counts_entries = _extract_counts(result) if result is not None else []
            except Exception as exc:
                retrieve_error = f"job retrieval failed: {exc}"
    elif args.submit:
        if backend is None:
            submit_error = "No IBM backend selected; no job submitted."
        elif Sampler is None:
            submit_error = sampler_status or "SamplerV2 unavailable; no job submitted."
        else:
            try:
                job = _run_sampler(Sampler, backend, transpiled, args.shots)
                submitted = True
                job_id = _job_id(job)
                job_status = _wait_for_job(job, args.wait_minutes)
                result, retrieve_error = _retrieve_result_if_done(job, job_status)
                counts_entries = _extract_counts(result) if result is not None else []
            except Exception as exc:
                submit_error = f"submission failed: {exc}"
    else:
        submitted = False

    if counts_entries:
        analysis_rows, aggregate_rows = _analyze_counts(counts_entries, circuit_rows)

    report = {
        "generated_at_utc": _timestamp(),
        "backend_requested": args.backend,
        "backend_selected": _backend_name(backend),
        "backend_num_qubits": _backend_num_qubits(backend),
        "backend_selection_status": backend_selection_status,
        "channel": args.channel,
        "credentials_available": _has_credentials()[0],
        "runtime_status": runtime_status,
        "sampler_status": sampler_status,
        "shots": args.shots,
        "repeats": repeats,
        "num_circuits": len(circuits),
        "dt": args.dt,
        "trotter_steps": trotter_steps,
        "hx": HX,
        "hy": HY,
        "J": J_COUPLING,
        "betas": BETAS,
        "transpile_method": transpile_method,
        "transpile_warning": transpile_warning,
        "submitted": submitted,
        "dry_run": not args.submit and not args.retrieve_job,
        "retrieve_job": args.retrieve_job,
        "job_id": job_id,
        "job_status": job_status,
        "submit_error": submit_error,
        "retrieve_error": retrieve_error,
        "counts_extracted": bool(counts_entries),
        "claim_guardrail": CLAIM_GUARDRAIL,
        "circuit_metadata": circuit_rows,
        "analysis_rows": analysis_rows,
        "aggregate_rows": aggregate_rows,
    }

    if submit_error and not report["dry_run"]:
        report["submit_error"] = submit_error
    if retrieve_error:
        report["retrieve_error"] = retrieve_error

    _write_outputs(report, circuit_rows, analysis_rows, aggregate_rows, counts_entries, save_dir)

    print(f"Problem 3-b IBM basis sweep outputs saved to {save_dir}")
    print(f"dry_run={report['dry_run']} submitted={submitted} retrieve_job={args.retrieve_job is not None}")
    print(f"backend={report['backend_selected']} num_circuits={len(circuits)}")
    if job_id:
        print(f"job_id={job_id} job_status={job_status}")
    if submit_error:
        print(f"submit_error={submit_error}")
    if retrieve_error:
        print(f"retrieve_error={retrieve_error}")
    print("No token/API key/CRN was printed or saved.")

    if report["dry_run"]:
        return 0
    if args.retrieve_job:
        return 0 if service is not None else 1
    return 0 if submitted or submit_error is None else 1


if __name__ == "__main__":
    raise SystemExit(main())

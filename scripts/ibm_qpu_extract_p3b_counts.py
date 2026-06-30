"""Extract Problem 3-b IBM QPU basis-sweep counts without pandas.

The script retrieves a completed Qiskit Runtime SamplerV2 job when the runtime
package is available. If a saved counts JSON already exists, it can recompute
the aggregate files from those raw counts using the source report metadata.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CLAIM_GUARDRAIL = (
    "Appendix validation only. Main scientific claims remain state-vector based. "
    "No hardware advantage claim."
)
REGISTER_NAMES = ["c", "meas", "cr", "creg", "alpha", "beta"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--backend", default="ibm_fez")
    parser.add_argument("--source-report", required=True)
    parser.add_argument("--save-dir", required=True)
    parser.add_argument(
        "--channel",
        default=os.environ.get("QISKIT_IBM_CHANNEL", "ibm_cloud"),
    )
    return parser.parse_args()


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _normalize_bitstring(value: Any, num_bits: int = 3) -> str | None:
    if isinstance(value, int):
        return format(value, f"0{num_bits}b")
    text = str(value).replace(" ", "")
    if text.startswith("0b"):
        text = text[2:]
    if not text or any(ch not in "01" for ch in text):
        return None
    return text.zfill(num_bits)[-num_bits:]


def _analyze_counts(counts: dict[str, int]) -> dict[str, Any]:
    normalized_counts: dict[str, int] = {}
    for key, value in counts.items():
        bitstring = _normalize_bitstring(key, 3)
        if bitstring is not None:
            normalized_counts[bitstring] = normalized_counts.get(bitstring, 0) + int(value)

    total = sum(normalized_counts.values())
    success_f0 = 0
    selected_data = Counter()
    for bitstring, count in normalized_counts.items():
        # q0 -> c0, q1 -> c1, q2 -> c2. Qiskit strings are c2 c1 c0.
        if bitstring[0] == "0":
            success_f0 += count
            selected_data[bitstring[1:]] += count

    return {
        "shots_total": total,
        "success_F0": success_f0,
        "success_probability_F0": success_f0 / total if total else None,
        "selected_data_counts_F0": dict(sorted(selected_data.items())),
        "selected_data_entropy_F0": _entropy(dict(selected_data)),
        "all_counts": dict(sorted(normalized_counts.items())),
    }


def _metadata_from_source_report(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = report.get("circuit_metadata") or report.get("circuits") or []
    metadata = []
    for fallback_index, row in enumerate(rows):
        beta = row.get("beta")
        beta_over_pi = row.get("beta_over_pi")
        if beta_over_pi is None and beta is not None:
            beta_over_pi = float(beta) / math.pi
        metadata.append(
            {
                "index": int(row.get("index", fallback_index)),
                "beta": beta,
                "beta_over_pi": beta_over_pi,
                "repeat": row.get("repeat"),
                "circuit_name": row.get("circuit_name") or row.get("name"),
            }
        )

    if metadata:
        return sorted(metadata, key=lambda item: item["index"])

    repeats = int(report.get("repeats", 3))
    betas = report.get("betas") or [0.0, math.pi / 4.0, math.pi / 2.0, 3.0 * math.pi / 4.0]
    rebuilt = []
    index = 0
    # Match scripts/ibm_qpu_problem3b_basis_sweep.py: repeat outer, beta inner.
    for repeat in range(repeats):
        for beta in betas:
            rebuilt.append(
                {
                    "index": index,
                    "beta": float(beta),
                    "beta_over_pi": float(beta) / math.pi,
                    "repeat": repeat,
                    "circuit_name": f"reconstructed_beta_{float(beta):.3f}_rep_{repeat}",
                }
            )
            index += 1
    return rebuilt


def _counts_from_obj(obj: Any) -> dict[str, int] | None:
    if obj is None:
        return None
    if hasattr(obj, "get_counts"):
        try:
            raw = obj.get_counts()
            if isinstance(raw, dict):
                return {str(key): int(value) for key, value in raw.items()}
        except Exception:
            pass
    if hasattr(obj, "get_bitstrings"):
        try:
            bitstrings = obj.get_bitstrings()
            return dict(Counter(str(item) for item in bitstrings))
        except Exception:
            pass
    return None


def _candidate_register_names(data: Any) -> list[str]:
    names = []
    for name in REGISTER_NAMES:
        if hasattr(data, name):
            names.append(name)
    try:
        for name in dir(data):
            if not name.startswith("_") and name not in names:
                names.append(name)
    except Exception:
        pass
    return names


def _extract_counts_from_pub_result(pub_result: Any) -> tuple[dict[str, int] | None, dict[str, Any]]:
    debug: dict[str, Any] = {
        "pub_result_type": type(pub_result).__name__,
        "tried_registers": [],
    }
    data = getattr(pub_result, "data", None)
    debug["data_type"] = type(data).__name__ if data is not None else None

    direct = _counts_from_obj(data)
    if direct:
        debug["counts_source"] = "data_direct"
        return direct, debug

    if data is not None:
        for name in _candidate_register_names(data):
            try:
                candidate = getattr(data, name)
            except Exception as exc:
                debug["tried_registers"].append({"name": name, "error": repr(exc)})
                continue
            debug["tried_registers"].append(
                {
                    "name": name,
                    "type": type(candidate).__name__,
                    "has_get_counts": hasattr(candidate, "get_counts"),
                    "has_get_bitstrings": hasattr(candidate, "get_bitstrings"),
                }
            )
            counts = _counts_from_obj(candidate)
            if counts:
                debug["counts_source"] = f"data.{name}"
                return counts, debug

        join_data = getattr(data, "join_data", None)
        if callable(join_data):
            try:
                joined = join_data()
                counts = _counts_from_obj(joined)
                if counts:
                    debug["counts_source"] = "data.join_data()"
                    return counts, debug
            except Exception as exc:
                debug["join_data_error"] = repr(exc)

    pub_direct = _counts_from_obj(pub_result)
    if pub_direct:
        debug["counts_source"] = "pub_result_direct"
        return pub_direct, debug

    debug["counts_source"] = None
    return None, debug


def _retrieve_runtime_counts(
    job_id: str,
    channel: str,
) -> tuple[list[dict[str, int]] | None, dict[str, Any]]:
    debug: dict[str, Any] = {
        "token_env_set": bool(os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")),
        "instance_env_set": bool(os.environ.get("QISKIT_IBM_INSTANCE")),
    }
    token = os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")
    instance = os.environ.get("QISKIT_IBM_INSTANCE")
    if not token or not instance:
        debug["status"] = "missing_token_or_instance"
        return None, debug

    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
    except Exception as exc:
        debug["status"] = "qiskit_ibm_runtime_import_failed"
        debug["error"] = repr(exc)
        return None, debug

    service = QiskitRuntimeService(channel=channel, token=token, instance=instance)
    job = service.job(job_id)
    debug["job_status"] = str(job.status())
    result = job.result()
    debug["result_type"] = type(result).__name__
    debug["result_repr_preview"] = repr(result)[:2000]

    counts_rows = []
    extract_debug = []
    for index, pub_result in enumerate(list(result)):
        counts, row_debug = _extract_counts_from_pub_result(pub_result)
        row_debug["index"] = index
        extract_debug.append(row_debug)
        counts_rows.append(counts or {})

    debug["status"] = "retrieved_from_runtime"
    debug["num_pub_results"] = len(counts_rows)
    debug["extract_debug"] = extract_debug
    return counts_rows, debug


def _load_saved_counts(save_dir: Path) -> tuple[list[dict[str, int]] | None, dict[str, Any]]:
    counts_path = save_dir / "problem3b_ibm_basis_sweep_counts.json"
    if not counts_path.exists():
        return None, {"status": "no_saved_counts_json"}
    raw_rows = _load_json(counts_path)
    counts_rows = []
    for row in sorted(raw_rows, key=lambda item: int(item.get("index", 0))):
        counts_rows.append({str(key): int(value) for key, value in (row.get("all_counts") or {}).items()})
    return counts_rows, {
        "status": "recomputed_from_saved_counts_without_runtime",
        "saved_counts_path": str(counts_path),
        "num_saved_count_rows": len(counts_rows),
    }


def _format_beta(beta_over_pi: Any) -> str:
    try:
        return f"{float(beta_over_pi):.4f}pi"
    except Exception:
        return str(beta_over_pi)


def _build_rows(
    metadata: list[dict[str, Any]],
    counts_rows: list[dict[str, int]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    per_circuit = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for index, counts in enumerate(counts_rows):
        meta = metadata[index] if index < len(metadata) else {"index": index}
        analysis = _analyze_counts(counts)
        row = {
            "index": int(meta.get("index", index)),
            "beta": meta.get("beta"),
            "beta_over_pi": meta.get("beta_over_pi"),
            "beta_label": _format_beta(meta.get("beta_over_pi")),
            "repeat": meta.get("repeat"),
            "circuit_name": meta.get("circuit_name"),
            "counts_found": bool(counts),
            **analysis,
        }
        per_circuit.append(row)
        if row["success_probability_F0"] is not None:
            grouped[row["beta_label"]].append(row)

    aggregate = []
    for beta_label in sorted(grouped.keys()):
        rows = grouped[beta_label]
        success = [float(row["success_probability_F0"]) for row in rows]
        entropy = [float(row["selected_data_entropy_F0"]) for row in rows]
        aggregate.append(
            {
                "beta": beta_label,
                "mean_success_probability_F0": statistics.mean(success),
                "std_success_probability_F0": statistics.stdev(success) if len(success) >= 2 else 0.0,
                "mean_selected_data_entropy_F0": statistics.mean(entropy),
                "std_selected_data_entropy_F0": statistics.stdev(entropy) if len(entropy) >= 2 else 0.0,
                "num_repeats": len(rows),
            }
        )
    return per_circuit, aggregate


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            serializable = {
                key: json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else value
                for key, value in row.items()
            }
            writer.writerow({key: serializable.get(key, "") for key in fieldnames})


def _write_outputs(
    save_dir: Path,
    report: dict[str, Any],
    per_circuit: list[dict[str, Any]],
    aggregate: list[dict[str, Any]],
) -> None:
    save_dir.mkdir(parents=True, exist_ok=True)
    (save_dir / "problem3b_ibm_counts_extract_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_csv(
        save_dir / "problem3b_ibm_basis_sweep_aggregate.csv",
        aggregate,
        [
            "beta",
            "mean_success_probability_F0",
            "std_success_probability_F0",
            "mean_selected_data_entropy_F0",
            "std_selected_data_entropy_F0",
            "num_repeats",
        ],
    )
    _write_csv(
        save_dir / "problem3b_ibm_basis_sweep_circuits.csv",
        per_circuit,
        [
            "index",
            "beta",
            "beta_over_pi",
            "beta_label",
            "repeat",
            "circuit_name",
            "counts_found",
            "shots_total",
            "success_F0",
            "success_probability_F0",
            "selected_data_entropy_F0",
            "selected_data_counts_F0",
            "all_counts",
        ],
    )
    counts_json = [
        {
            "index": row["index"],
            "beta": row.get("beta"),
            "beta_over_pi": row.get("beta_over_pi"),
            "beta_label": row.get("beta_label"),
            "repeat": row.get("repeat"),
            "all_counts": row.get("all_counts"),
            "selected_data_counts_F0": row.get("selected_data_counts_F0"),
        }
        for row in per_circuit
    ]
    (save_dir / "problem3b_ibm_basis_sweep_counts.json").write_text(
        json.dumps(counts_json, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# IBM QPU Problem 3-b Counts Extraction Summary",
        "",
        f"- generated_at_utc: `{report['generated_at_utc']}`",
        f"- backend: `{report['backend']}`",
        f"- job_id: `{report['job_id']}`",
        f"- job_status: `{report.get('job_status')}`",
        f"- counts_source_status: `{report.get('counts_source_status')}`",
        f"- aggregate_rows: `{len(aggregate)}`",
        "",
        f"Claim guardrail: {CLAIM_GUARDRAIL}",
        "",
        "## Aggregate by measurement basis",
        "",
    ]
    if aggregate:
        lines.extend(
            [
                "| beta | mean p(F=0) | std p(F=0) | mean selected entropy | std selected entropy | repeats |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for row in aggregate:
            lines.append(
                f"| {row['beta']} | {row['mean_success_probability_F0']:.6f} | "
                f"{row['std_success_probability_F0']:.6f} | "
                f"{row['mean_selected_data_entropy_F0']:.6f} | "
                f"{row['std_selected_data_entropy_F0']:.6f} | "
                f"{row['num_repeats']} |"
            )
    else:
        lines.append("No aggregate could be extracted. See `extract_debug` in the JSON report.")
    lines.extend(
        [
            "",
            "Interpretation: changing the complement-qubit measurement basis changes",
            "post-selection statistics and selected data distribution, supporting the",
            "Problem 3-b effective-map interpretation. This does not replace the",
            "state-vector benchmark.",
            "",
        ]
    )
    (save_dir / "problem3b_ibm_basis_sweep_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    save_dir = Path(args.save_dir)
    source_report = Path(args.source_report)
    source = _load_json(source_report)
    metadata = _metadata_from_source_report(source)

    runtime_counts, runtime_debug = _retrieve_runtime_counts(args.job_id, args.channel)
    counts_source_status = runtime_debug.get("status")
    counts_rows = runtime_counts
    if counts_rows is None:
        counts_rows, saved_debug = _load_saved_counts(save_dir)
        counts_source_status = saved_debug.get("status")
    else:
        saved_debug = {"status": "not_needed"}

    if counts_rows is None:
        per_circuit: list[dict[str, Any]] = []
        aggregate: list[dict[str, Any]] = []
    else:
        per_circuit, aggregate = _build_rows(metadata, counts_rows)

    report = {
        "generated_at_utc": _timestamp(),
        "job_id": args.job_id,
        "backend": args.backend,
        "channel": args.channel,
        "source_report": str(source_report),
        "token_env_set": bool(os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")),
        "instance_env_set": bool(os.environ.get("QISKIT_IBM_INSTANCE")),
        "job_status": runtime_debug.get("job_status") or source.get("job_status"),
        "counts_source_status": counts_source_status,
        "runtime_debug": runtime_debug,
        "saved_counts_debug": saved_debug,
        "metadata_rows": len(metadata),
        "per_circuit_analysis": per_circuit,
        "aggregate_by_beta": aggregate,
        "claim_guardrail": CLAIM_GUARDRAIL,
    }

    _write_outputs(save_dir, report, per_circuit, aggregate)
    print(f"Counts extraction saved to {save_dir}")
    print(f"job_id={args.job_id} status={report.get('job_status')} aggregate_rows={len(aggregate)}")
    print("No token/API key/CRN was printed or saved.")
    return 0 if aggregate else 1


if __name__ == "__main__":
    raise SystemExit(main())

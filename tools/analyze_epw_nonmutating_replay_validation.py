"""Terminal analyzer for the one-shot non-mutating serial EPW replay.

The analyzer consumes preserved evidence only. It never launches QE or mutates
replay state. Filesystem integrity and EPW completion are independent mandatory
gates; diagnostic success cannot override either failure.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.design_epw_replay_output_boundary import (
    FileRecord,
    compare_replay_tree,
    evaluate_completion,
)


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _records(path: Path) -> list[FileRecord]:
    payload = _load_json(path)
    files = payload.get("files")
    if not isinstance(files, list):
        raise ValueError(f"manifest has no files list: {path}")
    return [FileRecord(**record) for record in files]


def analyze(
    *,
    execution_contract: Path,
    boundary_contract: Path,
    seed_manifest: Path,
    post_manifest: Path,
    replay_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    exit_code: int,
) -> dict[str, Any]:
    execution = _load_json(execution_contract)
    boundary = _load_json(boundary_contract)
    if execution["stage"] != "B0_epw_nonmutating_replay_validation":
        raise ValueError("unexpected execution contract stage")
    if execution["issue"] != 371 or execution["phase"] != "one_pinned_execution":
        raise ValueError("unexpected execution contract identity")
    if boundary["stage"] != "B0_epw_replay_output_boundary_design":
        raise ValueError("unexpected boundary contract stage")
    if boundary["issue"] != 355 or boundary["phase"] != "design_only":
        raise ValueError("unexpected boundary design identity")

    seed = _records(seed_manifest)
    post = _records(post_manifest)
    filesystem = compare_replay_tree(seed, post, boundary)

    post_paths = {record.relative_path for record in post}
    output_files: dict[str, bytes] = {}
    for relative in filesystem["created_declared_outputs"]:
        if relative not in post_paths:
            raise ValueError(f"declared output missing from post manifest: {relative}")
        output_files[relative] = (replay_dir / relative).read_bytes()

    stdout = stdout_path.read_text(encoding="utf-8", errors="replace")
    stderr = stderr_path.read_text(encoding="utf-8", errors="replace")
    completion = evaluate_completion(
        stdout=stdout,
        stderr=stderr,
        exit_code=exit_code,
        output_files=output_files,
        contract=boundary,
    )

    if exit_code != 0 or any(completion["forbidden_markers_present"].values()):
        classification = "STOP_REPLAY_RUNTIME"
    elif filesystem["deleted_immutable_paths"] or filesystem["mutated_immutable_paths"]:
        classification = "STOP_STATE_MUTATION"
    elif (
        filesystem["forbidden_created_paths"]
        or filesystem["forbidden_existing_paths"]
        or filesystem["unknown_created_paths"]
        or filesystem["declared_outputs_present_in_seed"]
    ):
        classification = "STOP_FORBIDDEN_OUTPUT"
    elif not completion["passed"]:
        classification = "STOP_COMPLETION_EVIDENCE"
    elif not filesystem["passed"]:
        classification = "STOP_HARNESS"
    else:
        classification = execution["pass_classification"]

    passed = classification == execution["pass_classification"]
    return {
        "schema_version": "1.0",
        "stage": "B0_epw_nonmutating_replay_validation_result",
        "program": "R02",
        "issue": 371,
        "status": "pass" if passed else "stop",
        "classification": classification,
        "replay_exit_code": exit_code,
        "filesystem_integrity": filesystem,
        "completion_evidence": completion,
        "created_declared_output_count": len(
            filesystem["created_declared_outputs"]
        ),
        "immutable_seed_file_count": len(seed),
        "post_replay_file_count": len(post),
        "exporter_enabled": False,
        "material_calculation_count": 0,
        "historical_issue_350_result_changed": False,
        "automatic_successor_authorized": False,
        "claim_boundary": execution["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution-contract", type=Path, required=True)
    parser.add_argument("--boundary-contract", type=Path, required=True)
    parser.add_argument("--seed-manifest", type=Path, required=True)
    parser.add_argument("--post-manifest", type=Path, required=True)
    parser.add_argument("--replay-dir", type=Path, required=True)
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--stderr", type=Path, required=True)
    parser.add_argument("--exit-code", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = analyze(
        execution_contract=args.execution_contract,
        boundary_contract=args.boundary_contract,
        seed_manifest=args.seed_manifest,
        post_manifest=args.post_manifest,
        replay_dir=args.replay_dir,
        stdout_path=args.stdout,
        stderr_path=args.stderr,
        exit_code=args.exit_code,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if result["status"] == "pass" else 3


if __name__ == "__main__":
    raise SystemExit(main())

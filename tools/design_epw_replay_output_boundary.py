"""Design-only EPW replay boundary and completion-evidence helpers.

This module never launches external processes. It classifies a prepared tree,
constructs an immutable replay seed, checks post-replay filesystem evidence,
and evaluates prospective EPW 6.1 completion observables.
"""
from __future__ import annotations

from dataclasses import dataclass
import fnmatch
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
from typing import Any, Mapping, Sequence


class ReplayBoundaryError(ValueError):
    """Raised when replay state or completion evidence is ambiguous."""


@dataclass(frozen=True)
class FileRecord:
    relative_path: str
    file_type: str
    mode: int
    size_bytes: int
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "relative_path": self.relative_path,
            "file_type": self.file_type,
            "mode": self.mode,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
        }


def load_contract(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ReplayBoundaryError(f"expected JSON object: {path}")
    return value


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_tree_manifest(root: Path) -> list[FileRecord]:
    base = root.resolve()
    if not base.is_dir():
        raise ReplayBoundaryError(f"tree root is not a directory: {base}")
    records: list[FileRecord] = []
    for path in sorted(base.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(base).as_posix()
        if path.is_symlink():
            raise ReplayBoundaryError(f"symlink is prohibited: {relative}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ReplayBoundaryError(f"special file is prohibited: {relative}")
        stat = path.stat()
        records.append(
            FileRecord(
                relative_path=relative,
                file_type="regular",
                mode=stat.st_mode & 0o7777,
                size_bytes=stat.st_size,
                sha256=_sha256_file(path),
            )
        )
    if not records:
        raise ReplayBoundaryError("tree manifest cannot be empty")
    return records


def manifest_payload(records: Sequence[FileRecord]) -> dict[str, Any]:
    files = [record.as_dict() for record in records]
    canonical = json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    return {
        "schema_version": "1.0",
        "file_count": len(files),
        "files": files,
        "manifest_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def _patterns(contract: Mapping[str, Any], class_name: str) -> list[str]:
    return list(contract["path_classes"][class_name].get("patterns", []))


def _matches(path: str, patterns: Sequence[str]) -> bool:
    name = PurePosixPath(path).name
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def path_matches(contract: Mapping[str, Any], relative_path: str) -> list[str]:
    """Return every explicit class matched by a path.

    Unknown regular files intentionally have no explicit match and become part
    of the immutable seed.
    """

    matches: list[str] = []
    required = set(
        contract["path_classes"]["consumed_immutable_state"]["required_exact_paths"]
    )
    if relative_path in required:
        matches.append("consumed_immutable_state")
    for class_name in (
        "replay_declared_outputs",
        "transient_runtime_files",
        "forbidden_unknown_files",
    ):
        if _matches(relative_path, _patterns(contract, class_name)):
            matches.append(class_name)
    return matches


def classify_path(contract: Mapping[str, Any], relative_path: str) -> str:
    matches = path_matches(contract, relative_path)
    if len(matches) > 1:
        raise ReplayBoundaryError(
            f"path belongs to multiple replay classes: {relative_path}: {matches}"
        )
    if matches:
        return matches[0]
    return "consumed_immutable_state"


def validate_contract(contract: Mapping[str, Any]) -> None:
    if contract.get("stage") != "B0_epw_replay_output_boundary_design":
        raise ReplayBoundaryError("unexpected replay-boundary stage")
    if contract.get("issue") != 355 or contract.get("phase") != "design_only":
        raise ReplayBoundaryError("replay boundary must remain design-only")
    if contract.get("historical_issue_350_result_unchanged") is not True:
        raise ReplayBoundaryError("historical issue-350 stop must remain unchanged")

    authorization = contract["authorization"]
    for field in (
        "configure_or_build",
        "patch_application",
        "preparation_execution",
        "epw_replay_execution",
        "exporter_enabled_execution",
        "automatic_retry",
        "marker_or_threshold_fitting",
        "mpi_execution",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "automatic_executable_successor",
    ):
        if authorization[field] is not False:
            raise ReplayBoundaryError(f"execution authorization must be false: {field}")

    replay = contract["replay_input"]
    controls = replay["explicit_restart_controls"]
    expected = {
        "epbwrite": False,
        "epbread": False,
        "epwwrite": False,
        "epwread": True,
        "wannierize": False,
        "elecselfen": True,
        "nest_fn": False,
    }
    if controls != expected:
        raise ReplayBoundaryError("unexpected replay-control state")
    if replay["output_control_change_only"] is not True:
        raise ReplayBoundaryError("epbwrite delta must remain output-only")
    if replay["physical_parameter_change"] is not False:
        raise ReplayBoundaryError("physical parameters may not change")

    required = contract["path_classes"]["consumed_immutable_state"][
        "required_exact_paths"
    ]
    if len(required) != len(set(required)) or not required:
        raise ReplayBoundaryError("required immutable paths are duplicate or empty")
    for path in required:
        matches = path_matches(contract, path)
        if matches != ["consumed_immutable_state"]:
            raise ReplayBoundaryError(f"required path has class collision: {path}")

    for class_name in (
        "replay_declared_outputs",
        "transient_runtime_files",
        "forbidden_unknown_files",
    ):
        patterns = _patterns(contract, class_name)
        if not patterns or len(patterns) != len(set(patterns)):
            raise ReplayBoundaryError(f"invalid patterns for {class_name}")

    completion = contract["completion_observables"]
    if completion["post_hoc_marker_substitution_allowed"] is not False:
        raise ReplayBoundaryError("post-hoc marker substitution must be prohibited")
    if completion["exit_code_alone_is_sufficient"] is not False:
        raise ReplayBoundaryError("exit code alone cannot establish completion")
    if completion["stdout_marker_alone_is_sufficient"] is not False:
        raise ReplayBoundaryError("one stdout marker cannot establish completion")
    re.compile(completion["necessary"]["selfen_timer_name"])
    re.compile(completion["timer_regex"])


def project_immutable_seed(
    preparation: Sequence[FileRecord], contract: Mapping[str, Any]
) -> dict[str, Any]:
    """Project a complete preparation tree into a clean immutable seed."""

    validate_contract(contract)
    indexed = {record.relative_path: record for record in preparation}
    if len(indexed) != len(preparation):
        raise ReplayBoundaryError("duplicate preparation path")
    required = set(
        contract["path_classes"]["consumed_immutable_state"]["required_exact_paths"]
    )
    missing = sorted(required - set(indexed))
    if missing:
        raise ReplayBoundaryError(f"missing source-audited consumed paths: {missing}")

    seed: list[FileRecord] = []
    removed: dict[str, list[str]] = {
        "replay_declared_outputs": [],
        "transient_runtime_files": [],
        "forbidden_unknown_files": [],
    }
    for record in preparation:
        class_name = classify_path(contract, record.relative_path)
        if class_name == "consumed_immutable_state":
            seed.append(record)
        else:
            removed[class_name].append(record.relative_path)

    seed_paths = {record.relative_path for record in seed}
    if not required <= seed_paths:
        raise ReplayBoundaryError("seed projection removed a required consumed path")
    if any(classify_path(contract, path) != "consumed_immutable_state" for path in seed_paths):
        raise ReplayBoundaryError("non-immutable path leaked into replay seed")
    return {
        "seed": sorted(seed, key=lambda record: record.relative_path),
        "removed": {key: sorted(value) for key, value in removed.items()},
    }


def compare_replay_tree(
    seed: Sequence[FileRecord],
    post: Sequence[FileRecord],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate immutable input bytes and classify every post-replay file."""

    before = {record.relative_path: record for record in seed}
    after = {record.relative_path: record for record in post}
    if len(before) != len(seed) or len(after) != len(post):
        raise ReplayBoundaryError("duplicate path in replay manifest")

    deleted = sorted(set(before) - set(after))
    mutated = sorted(
        path
        for path in set(before) & set(after)
        if before[path].as_dict() != after[path].as_dict()
    )
    created_outputs: list[str] = []
    transient: list[str] = []
    forbidden: list[str] = []
    unknown: list[str] = []
    for path in sorted(set(after) - set(before)):
        class_name = classify_path(contract, path)
        if class_name == "replay_declared_outputs":
            created_outputs.append(path)
        elif class_name == "transient_runtime_files":
            transient.append(path)
        elif class_name == "forbidden_unknown_files":
            forbidden.append(path)
        else:
            unknown.append(path)

    forbidden_existing = sorted(
        path
        for path in after
        if classify_path(contract, path) == "forbidden_unknown_files"
    )
    output_existing_in_seed = sorted(
        path
        for path in before
        if classify_path(contract, path) == "replay_declared_outputs"
    )
    passed = not (
        deleted
        or mutated
        or forbidden
        or forbidden_existing
        or unknown
        or output_existing_in_seed
    )
    return {
        "passed": passed,
        "deleted_immutable_paths": deleted,
        "mutated_immutable_paths": mutated,
        "created_declared_outputs": created_outputs,
        "created_transient_files": transient,
        "forbidden_created_paths": forbidden,
        "forbidden_existing_paths": forbidden_existing,
        "unknown_created_paths": unknown,
        "declared_outputs_present_in_seed": output_existing_in_seed,
    }


_FORTRAN_FLOAT = re.compile(
    r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?$"
)


def count_numeric_rows(content: bytes) -> int:
    text = content.decode("utf-8", errors="replace")
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "!")):
            continue
        tokens = stripped.replace(",", " ").split()
        numeric = []
        for token in tokens:
            if _FORTRAN_FLOAT.match(token):
                value = float(token.replace("D", "E").replace("d", "e"))
                if math.isfinite(value):
                    numeric.append(value)
        if len(numeric) >= 3:
            count += 1
    return count


def evaluate_completion(
    *,
    stdout: str,
    stderr: str,
    exit_code: int,
    output_files: Mapping[str, bytes],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Evaluate source-grounded EPW completion without post-hoc marker fitting."""

    validate_contract(contract)
    completion = contract["completion_observables"]
    necessary = completion["necessary"]
    combined = stdout + "\n" + stderr
    forbidden = {
        marker: marker in combined for marker in completion["forbidden_markers"]
    }
    timer_matches = list(
        re.finditer(completion["timer_regex"], stdout, flags=re.IGNORECASE)
    )
    timer_calls = [int(match.group("calls")) for match in timer_matches]
    positive_timer = any(calls > 0 for calls in timer_calls)
    total_present = necessary["total_program_execution_marker"] in stdout

    result_pattern = necessary["electron_self_energy_result_pattern"]
    result_files = {
        path: content
        for path, content in output_files.items()
        if fnmatch.fnmatch(PurePosixPath(path).name, result_pattern)
    }
    result_evidence = {
        path: {
            "size_bytes": len(content),
            "numeric_row_count": count_numeric_rows(content),
        }
        for path, content in sorted(result_files.items())
    }
    result_files_pass = (
        len(result_files) >= necessary["result_file_count_minimum"]
        and all(len(content) > 0 for content in result_files.values())
        and all(
            evidence["numeric_row_count"]
            >= necessary["result_file_numeric_row_minimum"]
            for evidence in result_evidence.values()
        )
    )
    passed = (
        exit_code == 0
        and not any(forbidden.values())
        and total_present
        and positive_timer
        and result_files_pass
    )
    return {
        "passed": passed,
        "classification": (
            "EPW_COMPLETION_EVIDENCE_PASS" if passed else "EPW_COMPLETION_EVIDENCE_STOP"
        ),
        "exit_code_zero": exit_code == 0,
        "forbidden_markers_present": forbidden,
        "total_program_execution_present": total_present,
        "selfen_timer_match_count": len(timer_matches),
        "selfen_timer_calls": timer_calls,
        "selfen_timer_positive_call_count": positive_timer,
        "result_files": result_evidence,
        "result_files_pass": result_files_pass,
        "historical_issue_350_result_changed": False,
    }


def build_dry_run_manifest(
    contract: Mapping[str, Any],
    *,
    preparation_tree_label: str,
    replay_seed_label: str,
    replay_input: Path,
    executable_label: str,
) -> dict[str, Any]:
    validate_contract(contract)
    if _sha256_file(replay_input) != contract["replay_input"]["sha256"]:
        raise ReplayBoundaryError("non-mutating replay input SHA-256 mismatch")
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "stage": "B0_epw_replay_output_boundary_dry_run",
        "issue": contract["issue"],
        "execution_authorized": False,
        "preparation_tree_label": preparation_tree_label,
        "replay_seed_label": replay_seed_label,
        "replay_input": str(replay_input.resolve()),
        "replay_input_sha256": contract["replay_input"]["sha256"],
        "executable_label": executable_label,
        "seed_projection": contract["state_projection"],
        "path_classes": contract["path_classes"],
        "completion_observables": contract["completion_observables"],
        "claim_boundary": contract["claim_boundary"],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["manifest_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def write_json(value: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

"""Design-only helpers for same-state EPW exporter attribution.

The module performs hashing, manifest comparison, mutation checks, and synthetic
attribution logic. It never launches a process or executes Quantum ESPRESSO.
"""
from __future__ import annotations

from dataclasses import dataclass
import fnmatch
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping, Sequence


class SameStateDesignError(ValueError):
    """Raised when the prepared-state or attribution design is ambiguous."""


@dataclass(frozen=True)
class TreeEntry:
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
        raise SameStateDesignError(f"expected JSON object: {path}")
    return value


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_contract(contract: Mapping[str, Any]) -> None:
    if contract.get("stage") != "B0_epw_same_state_attribution_design":
        raise SameStateDesignError("unexpected same-state contract stage")
    if contract.get("issue") != 318 or contract.get("phase") != "design_only":
        raise SameStateDesignError("same-state attribution must remain design-only")

    authorization = contract["authorization"]
    for field in (
        "configure_or_build",
        "preparation_execution",
        "epw_replay_execution",
        "automatic_retry",
        "threshold_fitting",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "automatic_phase_transition",
    ):
        if authorization[field] is not False:
            raise SameStateDesignError(f"execution authorization must be false: {field}")

    state = contract["prepared_state"]
    if state["symlinks_allowed"] is not False:
        raise SameStateDesignError("prepared-state symlinks must be prohibited")
    if state["special_files_allowed"] is not False:
        raise SameStateDesignError("prepared-state special files must be prohibited")
    if state["three_byte_identical_clones_required"] is not True:
        raise SameStateDesignError("three byte-identical clones are required")
    if state["clone_ids"] != ["disabled_a", "disabled_b", "enabled"]:
        raise SameStateDesignError("unexpected replay clone identities")

    replays = contract["replays"]
    if replays["count"] != 3 or replays["order"] != state["clone_ids"]:
        raise SameStateDesignError("replay order differs from prepared-state clones")
    for field in ("pw_x_allowed", "ph_x_allowed", "pp_py_allowed", "wannierization_allowed"):
        if replays[field] is not False:
            raise SameStateDesignError(f"upstream regeneration must be false: {field}")

    rule = contract["attribution_rule"]
    if rule["historical_issue_313_result_unchanged"] is not True:
        raise SameStateDesignError("historical issue-313 result must remain unchanged")
    if rule["retrospective_floor_or_threshold_change_allowed"] is not False:
        raise SameStateDesignError("retrospective threshold changes must be prohibited")
    if rule["baseline_pass_required_before_enabled_evaluation"] is not True:
        raise SameStateDesignError("baseline reproducibility must gate enabled attribution")
    if rule["all_components_must_pass"] is not True:
        raise SameStateDesignError("all components must pass")


def build_tree_manifest(root: Path) -> list[TreeEntry]:
    """Hash every regular file in a prepared state and reject ambiguous nodes."""

    base = root.resolve()
    if not base.is_dir():
        raise SameStateDesignError(f"prepared-state root is not a directory: {base}")

    entries: list[TreeEntry] = []
    for path in sorted(base.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(base).as_posix()
        if path.is_symlink():
            raise SameStateDesignError(f"symlink is not allowed: {relative}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise SameStateDesignError(f"special file is not allowed: {relative}")
        stat = path.stat()
        entries.append(
            TreeEntry(
                relative_path=relative,
                file_type="regular",
                mode=stat.st_mode & 0o7777,
                size_bytes=stat.st_size,
                sha256=_sha256_file(path),
            )
        )
    if not entries:
        raise SameStateDesignError("prepared-state manifest cannot be empty")
    return entries


def manifest_payload(entries: Sequence[TreeEntry]) -> dict[str, Any]:
    records = [entry.as_dict() for entry in entries]
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return {
        "schema_version": "1.0",
        "file_count": len(records),
        "files": records,
        "manifest_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def require_paths(entries: Sequence[TreeEntry], required_paths: Sequence[str]) -> None:
    observed = {entry.relative_path for entry in entries}
    missing = sorted(set(required_paths) - observed)
    if missing:
        raise SameStateDesignError(f"missing required prepared-state paths: {missing}")


def assert_identical_manifests(
    manifests: Mapping[str, Sequence[TreeEntry]], clone_ids: Sequence[str]
) -> None:
    if set(manifests) != set(clone_ids):
        raise SameStateDesignError("manifest identities do not match required clones")
    reference = [entry.as_dict() for entry in manifests[clone_ids[0]]]
    for clone_id in clone_ids[1:]:
        candidate = [entry.as_dict() for entry in manifests[clone_id]]
        if candidate != reference:
            raise SameStateDesignError(f"prepared-state clone differs: {clone_id}")


def _entry_map(entries: Sequence[TreeEntry]) -> dict[str, TreeEntry]:
    mapped = {entry.relative_path: entry for entry in entries}
    if len(mapped) != len(entries):
        raise SameStateDesignError("duplicate manifest path")
    return mapped


def compare_pre_post_manifests(
    pre: Sequence[TreeEntry],
    post: Sequence[TreeEntry],
    allowed_new_patterns: Sequence[str],
) -> dict[str, Any]:
    """Reject mutation/deletion and permit only declared new output patterns."""

    before = _entry_map(pre)
    after = _entry_map(post)
    deleted = sorted(set(before) - set(after))
    mutated = sorted(
        path
        for path in set(before) & set(after)
        if before[path].as_dict() != after[path].as_dict()
    )
    new_paths = sorted(set(after) - set(before))
    unauthorized_new = sorted(
        path
        for path in new_paths
        if not any(fnmatch.fnmatch(Path(path).name, pattern) for pattern in allowed_new_patterns)
    )
    return {
        "passed": not deleted and not mutated and not unauthorized_new,
        "deleted": deleted,
        "mutated": mutated,
        "new_paths": new_paths,
        "unauthorized_new": unauthorized_new,
    }


def _coerce_metric(values: Sequence[float], name: str) -> list[float]:
    numeric = [float(value) for value in values]
    if not numeric:
        raise SameStateDesignError(f"metric cannot be empty: {name}")
    if any(not (value == value and abs(value) != float("inf")) for value in numeric):
        raise SameStateDesignError(f"metric contains nonfinite value: {name}")
    return numeric


def evaluate_attribution(
    disabled_a: Mapping[str, Sequence[float]],
    disabled_b: Mapping[str, Sequence[float]],
    enabled: Mapping[str, Sequence[float]],
    *,
    floors: Mapping[str, float],
    baseline_ceilings: Mapping[str, float],
) -> dict[str, Any]:
    """Evaluate a prospective deterministic disabled-replay envelope."""

    metrics = set(disabled_a)
    if metrics != set(disabled_b) or metrics != set(enabled):
        raise SameStateDesignError("metric names differ across replays")
    if metrics != set(floors) or metrics != set(baseline_ceilings):
        raise SameStateDesignError("metric thresholds are incomplete")

    results: dict[str, Any] = {}
    all_passed = True
    for metric in sorted(metrics):
        a = _coerce_metric(disabled_a[metric], metric)
        b = _coerce_metric(disabled_b[metric], metric)
        e = _coerce_metric(enabled[metric], metric)
        if not (len(a) == len(b) == len(e)):
            raise SameStateDesignError(f"metric lengths differ: {metric}")
        floor = float(floors[metric])
        ceiling = float(baseline_ceilings[metric])
        if floor < 0.0 or ceiling < 0.0:
            raise SameStateDesignError(f"negative threshold: {metric}")

        baseline = [abs(left - right) for left, right in zip(a, b, strict=True)]
        baseline_max = max(baseline)
        baseline_passed = baseline_max <= ceiling
        envelope_violations = [
            max(0.0, min(left, right) - floor - treatment, treatment - max(left, right) - floor)
            for left, right, treatment in zip(a, b, e, strict=True)
        ]
        envelope_max = max(envelope_violations)
        enabled_passed = envelope_max <= 0.0
        metric_passed = baseline_passed and enabled_passed
        all_passed = all_passed and metric_passed
        results[metric] = {
            "component_count": len(a),
            "floor": floor,
            "baseline_ceiling": ceiling,
            "baseline_max_abs_difference": baseline_max,
            "baseline_passed": baseline_passed,
            "enabled_envelope_max_violation": envelope_max,
            "enabled_envelope_passed": enabled_passed,
            "passed": metric_passed,
        }

    return {
        "schema_version": "1.0",
        "rule": "disabled_replay_interval_with_fixed_floor",
        "passed": all_passed,
        "classification": (
            "ATTRIBUTION_NONINTERFERENCE_PASS" if all_passed else "ATTRIBUTION_STOP"
        ),
        "metrics": results,
        "statistical_population_claim_allowed": False,
        "historical_issue_313_result_changed": False,
    }


def build_dry_run_manifest(
    contract: Mapping[str, Any],
    *,
    prepared_state_dir: Path,
    replay_root: Path,
    replay_input: Path,
    executable_label: str,
) -> dict[str, Any]:
    """Create an inert preparation/replay plan without process execution."""

    validate_contract(contract)
    prepared = prepared_state_dir.resolve()
    root = replay_root.resolve()
    input_path = replay_input.resolve()
    if prepared == root or prepared in root.parents:
        raise SameStateDesignError("replay root cannot contain the prepared state")
    if _sha256_file(input_path) != contract["replay_input"]["sha256"]:
        raise SameStateDesignError("replay input SHA-256 mismatch")

    clone_ids = contract["prepared_state"]["clone_ids"]
    replays = []
    for clone_id in clone_ids:
        clone = root / clone_id
        replays.append(
            {
                "id": clone_id,
                "prepared_state_source": str(prepared),
                "clone_destination": str(clone),
                "pre_manifest": str(root / "manifests" / f"{clone_id}.pre.json"),
                "post_manifest": str(root / "manifests" / f"{clone_id}.post.json"),
                "executable_label": executable_label,
                "input": str(input_path),
                "stdout": str(root / "evidence" / f"{clone_id}.stdout.txt"),
                "stderr": str(root / "evidence" / f"{clone_id}.stderr.txt"),
                "raw_vertex": (
                    str(root / "evidence" / "enabled.raw-vertex.txt")
                    if clone_id == "enabled"
                    else None
                ),
                "export_enabled": clone_id == "enabled",
            }
        )
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "stage": "B0_epw_same_state_attribution_dry_run",
        "issue": contract["issue"],
        "execution_authorized": False,
        "prepared_state_dir": str(prepared),
        "replay_root": str(root),
        "replay_input_sha256": contract["replay_input"]["sha256"],
        "replays": replays,
        "attribution_rule": contract["attribution_rule"],
        "claim_boundary": contract["claim_boundary"],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["manifest_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def write_json(value: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

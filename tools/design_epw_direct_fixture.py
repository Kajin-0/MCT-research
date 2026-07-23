"""Build a design-only EPW command manifest without executing processes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shlex
from typing import Any, Mapping


class DirectFixtureDesignError(ValueError):
    """Raised when the design contract or dry-run filesystem is ambiguous."""


def load_contract(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise DirectFixtureDesignError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_contract(contract: Mapping[str, Any]) -> None:
    if contract.get("stage") != "B0_epw_direct_fixture_design":
        raise DirectFixtureDesignError("unexpected direct-fixture contract stage")
    if contract.get("issue") != 309 or contract.get("phase") != "design_only":
        raise DirectFixtureDesignError("direct fixture must remain design-only")

    authorization = contract["authorization"]
    forbidden = (
        "configure_or_build",
        "pw_x_execution",
        "ph_x_execution",
        "epw_x_execution",
        "pp_py_execution",
        "fixture_execution",
        "automatic_retry",
        "parameter_sweep",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "automatic_phase_transition",
    )
    for field in forbidden:
        if authorization[field] is not False:
            raise DirectFixtureDesignError(f"execution authorization must be false: {field}")

    commands = contract["command_sequence"]
    expected_ids = ["pw_scf", "ph", "pp", "pw_scf_epw", "pw_nscf_epw", "epw"]
    expected_branches = [1, 2, 2, 1, 1, 3]
    if [item["id"] for item in commands] != expected_ids:
        raise DirectFixtureDesignError("command ordering differs from upstream sequence")
    if [item["upstream_run_epw_branch"] for item in commands] != expected_branches:
        raise DirectFixtureDesignError("run-epw branch mapping is incorrect")

    outputs = [item[key] for item in commands for key in ("stdout", "stderr")]
    if len(outputs) != len(set(outputs)):
        raise DirectFixtureDesignError("stdout/stderr destinations are not unique")
    if not all(path.startswith("evidence/commands/") for path in outputs):
        raise DirectFixtureDesignError("outputs must live under evidence/commands")


def verify_fixture_inputs(
    contract: Mapping[str, Any], fixture_dir: Path
) -> dict[str, str]:
    observed: dict[str, str] = {}
    for name, specification in contract["source"]["fixture_files"].items():
        if name == "C_3.98148.UPF":
            continue
        path = fixture_dir / name
        if not path.is_file():
            raise DirectFixtureDesignError(f"missing fixture input: {path}")
        digest = sha256_file(path)
        if digest != specification["sha256"]:
            raise DirectFixtureDesignError(f"fixture input hash mismatch: {name}")
        observed[name] = digest
    return observed


def build_manifest(
    contract: Mapping[str, Any],
    *,
    fixture_dir: Path,
    evidence_dir: Path,
    executable_labels: Mapping[str, str],
    epw_bin_dir: Path,
    verify_inputs: bool = True,
) -> dict[str, Any]:
    """Return a deterministic inert manifest; no process is invoked."""

    validate_contract(contract)
    fixture = fixture_dir.resolve()
    evidence = evidence_dir.resolve()
    epw_bin = epw_bin_dir.resolve()
    if fixture == evidence or fixture in evidence.parents:
        raise DirectFixtureDesignError("evidence cannot be inside the fixture tree")

    symbols = {item["executable_symbol"] for item in contract["command_sequence"]}
    if set(executable_labels) != symbols:
        raise DirectFixtureDesignError(f"executable labels must be exactly {sorted(symbols)}")

    input_hashes = verify_fixture_inputs(contract, fixture) if verify_inputs else {}
    commands: list[dict[str, Any]] = []
    destinations: set[str] = set()
    for sequence, item in enumerate(contract["command_sequence"], 1):
        argv = [str(value) for value in item["argv"]]
        argv = [
            str(epw_bin / value.removeprefix("EPW_BIN/"))
            if value.startswith("EPW_BIN/")
            else value
            for value in argv
        ]
        stdin = str((fixture / item["stdin"]).resolve()) if item["stdin"] else None
        stdout = str((evidence / Path(item["stdout"]).relative_to("evidence")).resolve())
        stderr = str((evidence / Path(item["stderr"]).relative_to("evidence")).resolve())
        for destination in (stdout, stderr):
            if destination in destinations:
                raise DirectFixtureDesignError(f"duplicate output destination: {destination}")
            destinations.add(destination)
            if str(fixture) in Path(destination).parents:
                raise DirectFixtureDesignError("output overlaps fixture cleanup scope")
        quoted_words = [executable_labels[item["executable_symbol"]], *argv]
        commands.append(
            {
                "sequence": sequence,
                "id": item["id"],
                "cwd": str(fixture),
                "executable_symbol": item["executable_symbol"],
                "executable_label": executable_labels[item["executable_symbol"]],
                "argv": argv,
                "stdin": stdin,
                "stdout": stdout,
                "stderr": stderr,
                "quoted_command_text": shlex.join(quoted_words),
                "upstream_run_epw_branch": item["upstream_run_epw_branch"],
            }
        )

    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "stage": "B0_epw_direct_fixture_dry_run_manifest",
        "program": contract["program"],
        "issue": contract["issue"],
        "execution_authorized": False,
        "fixture_dir": str(fixture),
        "evidence_dir": str(evidence),
        "epw_bin_dir": str(epw_bin),
        "source_commit": contract["source"]["commit_sha"],
        "run_epw_git_blob_sha": contract["source"]["run_epw_git_blob_sha"],
        "fixture_input_sha256": input_hashes,
        "commands": commands,
        "preservation": contract["preservation"],
        "claim_boundary": contract["claim_boundary"],
    }
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    manifest["manifest_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return manifest


def write_manifest(manifest: Mapping[str, Any], output_path: Path) -> None:
    """Write the inert JSON manifest and nothing executable."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

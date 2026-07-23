from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from tools.design_epw_direct_fixture import (
    DirectFixtureDesignError,
    build_manifest,
    load_contract,
    validate_contract,
    verify_fixture_inputs,
    write_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "first_principles/b0/r02_epw_direct_fixture_design_contract.json"
TOOL_PATH = ROOT / "tools/design_epw_direct_fixture.py"


def _contract() -> dict:
    return load_contract(CONTRACT_PATH)


def _labels() -> dict[str, str]:
    return {
        "PW_X": "/opt/qe build/bin/pw.x",
        "PH_X": "/opt/qe build/bin/ph.x",
        "EPW_X": "/opt/qe build/bin/epw.x",
        "PYTHON": "/usr/bin/python3",
    }


def _manifest(tmp_path: Path) -> dict:
    fixture = tmp_path / "fixture with spaces"
    fixture.mkdir()
    evidence = tmp_path / "immutable evidence"
    return build_manifest(
        _contract(),
        fixture_dir=fixture,
        evidence_dir=evidence,
        executable_labels=_labels(),
        epw_bin_dir=tmp_path / "qe source" / "EPW" / "bin",
        verify_inputs=False,
    )


def test_contract_is_design_only_and_execution_closed() -> None:
    contract = _contract()
    validate_contract(contract)
    assert contract["issue"] == 309
    assert contract["phase"] == "design_only"
    assert contract["source"]["run_epw_git_blob_sha"] == (
        "8f6a915fb656e424f8e4c03b3e5ea301d83953ae"
    )
    authorization = contract["authorization"]
    for field in (
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
    ):
        assert authorization[field] is False


def test_command_sequence_matches_upstream_branches() -> None:
    commands = _contract()["command_sequence"]
    assert [item["id"] for item in commands] == [
        "pw_scf",
        "ph",
        "pp",
        "pw_scf_epw",
        "pw_nscf_epw",
        "epw",
    ]
    assert [item["upstream_run_epw_branch"] for item in commands] == [
        1,
        2,
        2,
        1,
        1,
        3,
    ]
    assert commands[2]["stdin"] == "pp.in"
    assert commands[2]["argv"] == ["EPW_BIN/pp.py"]


def test_manifest_is_inert_and_has_explicit_unique_outputs(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    assert manifest["stage"] == "B0_epw_direct_fixture_dry_run_manifest"
    assert manifest["execution_authorized"] is False
    assert len(manifest["commands"]) == 6
    outputs = [
        command[key]
        for command in manifest["commands"]
        for key in ("stdout", "stderr")
    ]
    assert len(outputs) == 12
    assert len(set(outputs)) == 12
    assert all("immutable evidence/commands/" in output for output in outputs)
    assert all(
        command["cwd"] == manifest["fixture_dir"]
        for command in manifest["commands"]
    )
    assert len(manifest["manifest_payload_sha256"]) == 64


def test_shell_quoting_is_preserved_as_inert_text(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    first = manifest["commands"][0]
    assert first["quoted_command_text"].startswith("'/opt/qe build/bin/pw.x'")
    pp = manifest["commands"][2]
    assert "'/tmp/" in pp["quoted_command_text"]
    assert "qe source/EPW/bin/pp.py'" in pp["quoted_command_text"]
    assert "subprocess" not in TOOL_PATH.read_text(encoding="utf-8")
    assert "os.system" not in TOOL_PATH.read_text(encoding="utf-8")


def test_evidence_inside_fixture_tree_fails_closed(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    with pytest.raises(DirectFixtureDesignError, match="evidence cannot be inside"):
        build_manifest(
            _contract(),
            fixture_dir=fixture,
            evidence_dir=fixture / "evidence",
            executable_labels=_labels(),
            epw_bin_dir=tmp_path / "EPW" / "bin",
            verify_inputs=False,
        )


def test_duplicate_output_contract_fails_closed() -> None:
    contract = deepcopy(_contract())
    contract["command_sequence"][1]["stdout"] = contract["command_sequence"][0][
        "stdout"
    ]
    with pytest.raises(DirectFixtureDesignError, match="not unique"):
        validate_contract(contract)


def test_execution_authorization_fails_closed() -> None:
    contract = deepcopy(_contract())
    contract["authorization"]["epw_x_execution"] = True
    with pytest.raises(DirectFixtureDesignError, match="must be false"):
        validate_contract(contract)


def test_fixture_hash_verification_accepts_exact_pp_input(tmp_path: Path) -> None:
    contract = deepcopy(_contract())
    pp_specification = contract["source"]["fixture_files"]["pp.in"]
    contract["source"]["fixture_files"] = {"pp.in": pp_specification}
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    (fixture / "pp.in").write_bytes(b"diam\n")
    observed = verify_fixture_inputs(contract, fixture)
    assert observed == {
        "pp.in": "f052c801085cf37855fbab544b5cbe46c864e54c37a163a2bc6eab51c2a34e47"
    }


def test_fixture_hash_mismatch_and_missing_input_fail_closed(tmp_path: Path) -> None:
    contract = deepcopy(_contract())
    pp_specification = contract["source"]["fixture_files"]["pp.in"]
    contract["source"]["fixture_files"] = {"pp.in": pp_specification}
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    with pytest.raises(DirectFixtureDesignError, match="missing fixture input"):
        verify_fixture_inputs(contract, fixture)
    (fixture / "pp.in").write_text("wrong\n", encoding="utf-8")
    with pytest.raises(DirectFixtureDesignError, match="hash mismatch"):
        verify_fixture_inputs(contract, fixture)


def test_manifest_write_is_deterministic_json_only(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    output = tmp_path / "design" / "manifest.json"
    write_manifest(manifest, output)
    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded == manifest
    assert output.read_bytes().endswith(b"\n")
    first_digest = hashlib.sha256(output.read_bytes()).hexdigest()
    write_manifest(manifest, output)
    assert hashlib.sha256(output.read_bytes()).hexdigest() == first_digest

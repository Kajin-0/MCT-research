from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.render_cdte_static_kane_inputs import OUTPUT_NAMES, render

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "first_principles/a0/cdte_static_kane_method_smoke.json"
COMMITTED = ROOT / "first_principles/a0/cdte_static_kane_smoke_inputs"
EXPECTED_SHA256 = {
    "cdte_kane.scf.in": "4f2dfd8f007b3893f8fb5ca09fb95f41e5ca20aa9c361b1a763bc427e8bcea01",
    "cdte_kane.nscf.in": "e1e4f97c3460fa27ddecaf3734f9dda09a82207023465ffddca694a17c3f7e8f",
    "cdte_kane.win": "969d1e2be2689749819a210583a2c0f9c48a5cbd49baa69dc9a0f5ba03cb4270",
    "cdte_kane.pw2wan.in": "7cabfca312f3040f040e7f69580a1c47d30320b4af247a8d776498ad5b6c77a7",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_renderer_reproduces_committed_inputs_byte_for_byte(tmp_path: Path) -> None:
    manifest = render(SPEC, tmp_path)

    assert tuple(EXPECTED_SHA256) == OUTPUT_NAMES
    assert manifest["status"] == "rendered_planning_inputs_not_execution_evidence"
    assert manifest["rendered_file_sha256"] == EXPECTED_SHA256
    assert manifest["calculation_executed"] is False
    assert manifest["scientific_result_available"] is False

    for name, expected_hash in EXPECTED_SHA256.items():
        generated = (tmp_path / name).read_bytes()
        committed = (COMMITTED / name).read_bytes()
        assert generated == committed
        assert _sha256(generated) == expected_hash


def test_rendered_stencil_and_readiness_remain_fail_closed() -> None:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    nscf = (COMMITTED / "cdte_kane.nscf.in").read_text(encoding="utf-8")
    win = (COMMITTED / "cdte_kane.win").read_text(encoding="utf-8")

    assert spec["rendered_inputs"]["file_sha256"] == EXPECTED_SHA256
    assert spec["readiness"]["rendered_inputs_committed"] is True
    assert spec["readiness"]["runtime_available"] is False
    assert spec["readiness"]["ready_for_execution"] is False
    assert spec["authorization"]["phonons"] is False
    assert spec["authorization"]["electron_phonon_self_energy"] is False

    assert "K_POINTS crystal\n  13\n" in nscf
    assert nscf.count(" 1.0 ! ") == 13
    nnkpts = win.split("begin nnkpts\n", 1)[1].split("end nnkpts", 1)[0]
    assert len([line for line in nnkpts.splitlines() if line.strip()]) == 13

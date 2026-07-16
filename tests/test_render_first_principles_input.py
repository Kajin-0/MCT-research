from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.render_first_principles_input import render, render_text


def test_render_text_requires_exact_parameter_set() -> None:
    template = "ecutwfc=@ECUT@\nnk=@NK@\n"
    assert render_text(template, {"ECUT": 102, "NK": 8}) == "ecutwfc=102\nnk=8\n"
    with pytest.raises(ValueError, match="missing template parameters: NK"):
        render_text(template, {"ECUT": 102})
    with pytest.raises(ValueError, match="unused template parameters: EXTRA"):
        render_text(template, {"ECUT": 102, "NK": 8, "EXTRA": 1})


def test_render_writes_hash_manifest_and_external_inputs(tmp_path: Path) -> None:
    template = tmp_path / "template.in"
    parameters = tmp_path / "parameters.json"
    output = tmp_path / "rendered.in"
    manifest_path = tmp_path / "manifest.json"
    pseudo = tmp_path / "Cd.upf"

    template.write_text("prefix='@PREFIX@'\necutwfc=@ECUT@\n", encoding="utf-8")
    parameters.write_text(
        json.dumps({"PREFIX": "cdte", "ECUT": 102}), encoding="utf-8"
    )
    pseudo.write_bytes(b"synthetic pseudo bytes\n")

    manifest = render(
        template,
        output,
        parameters,
        manifest_path,
        input_files=[f"Cd_UPF={pseudo}"],
    )

    assert output.read_text(encoding="utf-8") == "prefix='cdte'\necutwfc=102\n"
    assert manifest["execution_performed"] is False
    assert manifest["syntax_check_performed"] is False
    assert manifest["rendered_input"]["sha256"] == hashlib.sha256(
        output.read_bytes()
    ).hexdigest()
    assert manifest["external_inputs"]["Cd_UPF"]["sha256"] == hashlib.sha256(
        pseudo.read_bytes()
    ).hexdigest()
    assert json.loads(manifest_path.read_text(encoding="utf-8")) == manifest


def test_render_rejects_missing_external_file(tmp_path: Path) -> None:
    template = tmp_path / "template.in"
    parameters = tmp_path / "parameters.json"
    template.write_text("@VALUE@\n", encoding="utf-8")
    parameters.write_text('{"VALUE": 1}', encoding="utf-8")
    with pytest.raises(FileNotFoundError):
        render(
            template,
            tmp_path / "rendered.in",
            parameters,
            tmp_path / "manifest.json",
            input_files=[f"missing={tmp_path / 'missing.upf'}"],
        )

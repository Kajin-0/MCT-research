from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from tools.render_cdte_a0_runtime_inputs import (
    derive_settings,
    pseudo_records,
)
from tools.validate_qe_ph_input_against_source import (
    input_keys,
    source_variables,
    validate,
)


ROOT = Path(__file__).resolve().parents[1]
RUN_SPEC = ROOT / "first_principles" / "a0" / "cdte_a0_run_spec.json"
SELECTION = ROOT / "first_principles" / "a0" / "cdte_pseudopotential_selection.json"
TEMPLATES = ROOT / "first_principles" / "a0" / "templates"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_first_a0_runtime_point_matches_declared_sequence() -> None:
    settings = derive_settings(_load(RUN_SPEC))

    assert settings["reference_lattice_angstrom"] == pytest.approx(
        6.476035479332049
    )
    assert settings["ecutwfc_ry"] == 114.0
    assert settings["ecutrho_ry"] == 456.0
    assert settings["ecut_ha"] == 57.0
    assert settings["kgrid"] == 4
    assert settings["nbnd"] == 40
    assert settings["scf_conv_thr_ry"] == 1e-8
    assert settings["ph_tr2"] == 1e-10
    assert settings["volume_grid"]["execution_authorized"] is True


def test_runtime_pseudopotential_schema_and_hash_checks(tmp_path: Path) -> None:
    selection = copy.deepcopy(_load(SELECTION))
    payloads = {
        "Cd-sp_r.upf": b"Cd UPF test bytes\n",
        "Cd-sp_r.psp8": b"Cd PSP8 test bytes\n",
        "Te-d_r.upf": b"Te UPF test bytes\n",
        "Te-d_r.psp8": b"Te PSP8 test bytes\n",
    }
    for filename, payload in payloads.items():
        (tmp_path / filename).write_bytes(payload)

    for element in ("Cd", "Te"):
        entry = selection["elements"][element]
        for kind, path_key, hash_key in (
            ("upf", "upf_path", "upf_sha256"),
            ("psp8", "psp8_path", "psp8_sha256"),
        ):
            filename = Path(entry[path_key]).name
            entry[hash_key] = hashlib.sha256(payloads[filename]).hexdigest()

    records = pseudo_records(selection, tmp_path)
    assert set(records) == {"Cd_upf", "Cd_psp8", "Te_upf", "Te_psp8"}
    assert records["Cd_upf"]["upstream_path"] == selection["elements"]["Cd"][
        "upf_path"
    ]

    (tmp_path / "Cd-sp_r.upf").write_bytes(b"corrupted")
    with pytest.raises(ValueError, match="Cd upf hash mismatch"):
        pseudo_records(selection, tmp_path)


def test_qe_ph_source_validator_accepts_only_declared_keys(tmp_path: Path) -> None:
    rendered = tmp_path / "ph.in"
    definition = tmp_path / "INPUT_PH.def"
    output = tmp_path / "validation.json"
    rendered.write_text(
        """&INPUTPH
prefix='cdte'
outdir='./tmp'
fildyn='cdte.dyn'
tr2_ph=1.0d-10
niter_ph=0
trans=.true.
epsil=.true.
ldisp=.false.
/
0 0 0
""",
        encoding="utf-8",
    )
    definition.write_text(
        "\n".join(
            f"var {name} -type CHARACTER" if name in {"prefix", "outdir", "fildyn"}
            else f"var {name} -type LOGICAL"
            for name in (
                "prefix",
                "outdir",
                "fildyn",
                "tr2_ph",
                "niter_ph",
                "trans",
                "epsil",
                "ldisp",
            )
        ),
        encoding="utf-8",
    )

    result = validate(rendered, definition)
    assert result["passed"] is True
    assert result["missing_from_pinned_source"] == []
    assert input_keys(rendered.read_text(encoding="utf-8")) == [
        "epsil",
        "fildyn",
        "ldisp",
        "niter_ph",
        "outdir",
        "prefix",
        "tr2_ph",
        "trans",
    ]
    assert "epsil" in source_variables(definition.read_text(encoding="utf-8"))

    rendered.write_text(
        rendered.read_text(encoding="utf-8").replace(
            "epsil=.true.", "epsil=.true.\nnot_a_qe_variable=1"
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="not_a_qe_variable"):
        validate(rendered, definition)


def test_runtime_templates_preserve_no_science_boundary() -> None:
    qe = (TEMPLATES / "cdte_qe_scf_dry.in.template").read_text(encoding="utf-8")
    ph = (TEMPLATES / "cdte_qe_ph_gamma.in.template").read_text(encoding="utf-8")
    abinit = (TEMPLATES / "cdte_abinit_dry.abi.template").read_text(encoding="utf-8")

    assert "nstep = 0" in qe
    assert "niter_ph = @NITER_PH@" in ph
    assert "nspinor 2" in abinit
    assert "so_psp 1 1" in abinit
    assert max(len(line) for line in abinit.splitlines()) <= 132
    assert "@LATTICE_ANGSTROM@" in qe
    assert "@LATTICE_ANGSTROM@" in abinit

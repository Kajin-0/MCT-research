from __future__ import annotations

import json
import re
from pathlib import Path

RUN_SPEC_PATH = Path("first_principles/a0/cdte_a0_run_spec.json")
SELECTION_PATH = Path("first_principles/a0/cdte_pseudopotential_selection.json")
REFERENCE_PATH = Path(
    "first_principles/a0/cdte_a0_runtime_readiness_reference.json"
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_runtime_reference_is_a_no_science_pass_record() -> None:
    reference = _load(REFERENCE_PATH)

    assert reference["status"] == (
        "runtime_and_rendered_inputs_validated_no_scientific_run"
    )
    assert reference["verification"]["runtime_workflow_run_id"] == 29623698323
    assert reference["verification"]["artifact_id"] == 8423244947
    assert reference["verification"]["artifact_digest"] == (
        "sha256:7835dddd59f042997daba935f15719030a31840f07516e3bc9b07c0150b14b9e"
    )
    assert reference["validation"]["runtime_hashes_verified"] is True
    assert reference["validation"]["release_specific_syntax_checked"] is True
    assert reference["validation"]["calculation_executed"] is False
    assert reference["validation"]["scientific_result_available"] is False
    assert all(
        reference["rendered_inputs"][name]["passed"] is True
        for name in ("qe_scf", "qe_ph", "abinit")
    )


def test_run_spec_matches_runtime_reference_exactly() -> None:
    specification = _load(RUN_SPEC_PATH)
    reference = _load(REFERENCE_PATH)

    qe = specification["source_code"]["quantum_espresso"]
    abinit = specification["source_code"]["abinit"]
    assert qe["executable_sha256"] == {
        name: reference["executables"][name]["sha256"]
        for name in ("pw.x", "ph.x")
    }
    assert abinit["executable_sha256"] == {
        "abinit": reference["executables"]["abinit"]["sha256"]
    }

    runtime = specification["runtime_inputs"]
    assert runtime["runtime_readiness_reference"] == str(REFERENCE_PATH)
    assert runtime["verification_workflow_run_id"] == (
        reference["verification"]["runtime_workflow_run_id"]
    )
    assert runtime["verification_artifact_id"] == (
        reference["verification"]["artifact_id"]
    )
    assert runtime["verification_artifact_digest"] == (
        reference["verification"]["artifact_digest"]
    )

    first = reference["selected_first_a0_point"]
    assert first["reference_lattice_angstrom"] == (
        specification["structure"]["execution_lattice_constant_angstrom"]
    )
    assert first["ecutwfc_ry"] == max(
        specification["convergence_ladders"]["ecutwfc_ry"]
    )
    assert first["ecutrho_ry"] == min(
        specification["convergence_ladders"]["ecutrho_ry"]
    )
    assert first["k_grid"] == [
        min(specification["convergence_ladders"]["k_grid_n"])
    ] * 3
    assert first["nbnd"] == min(specification["convergence_ladders"]["nbnd"])


def test_selection_runtime_hashes_match_reference() -> None:
    selection = _load(SELECTION_PATH)
    reference = _load(REFERENCE_PATH)

    mapping = {
        "Cd_upf": ("Cd", "upf_sha256"),
        "Te_upf": ("Te", "upf_sha256"),
        "Cd_psp8": ("Cd", "psp8_sha256"),
        "Te_psp8": ("Te", "psp8_sha256"),
    }
    for runtime_name, (element, field) in mapping.items():
        expected = selection["elements"][element][field]
        actual = reference["runtime_pseudopotentials"][runtime_name]["sha256"]
        assert actual == expected
        assert SHA256.fullmatch(actual)

    state = selection["verification_state"]
    assert state["runtime_file_hash_verified"] is True
    assert state["qe_syntax_checked"] is True
    assert state["abinit_syntax_checked"] is True
    assert state["static_calculation_run"] is False
    assert state["phonon_calculation_run"] is False


def test_all_promoted_runtime_hashes_are_well_formed() -> None:
    reference = _load(REFERENCE_PATH)

    hashes = [
        *(entry["sha256"] for entry in reference["executables"].values()),
        *(
            entry["sha256"]
            for entry in reference["runtime_pseudopotentials"].values()
        ),
        *(
            entry["rendered_sha256"]
            for entry in reference["rendered_inputs"].values()
        ),
    ]
    assert all(SHA256.fullmatch(value) for value in hashes)

    limitations = " ".join(reference["known_limitations"]).lower()
    assert "parallel netcdf-io" in limitations
    assert "build metadata" in limitations

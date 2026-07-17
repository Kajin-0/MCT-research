from __future__ import annotations

import copy
import json
from pathlib import Path

from tools.check_cdte_a0_readiness import evaluate_readiness

RUN_SPEC_PATH = Path("first_principles/a0/cdte_a0_run_spec.json")
SELECTION_PATH = Path("first_principles/a0/cdte_pseudopotential_selection.json")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _complete_specification() -> tuple[dict, dict]:
    specification = _load(RUN_SPEC_PATH)
    selection = _load(SELECTION_PATH)

    specification["source_code"]["quantum_espresso"].update(
        {
            "installed_version_output": "Quantum ESPRESSO v.7.4.1",
            "executable_sha256": {"pw.x": "1" * 64, "ph.x": "2" * 64},
            "release_specific_syntax_checked": True,
        }
    )
    specification["source_code"]["abinit"].update(
        {
            "installed_version_output": "ABINIT 10.6.5",
            "executable_sha256": {"abinit": "3" * 64},
            "release_specific_syntax_checked": True,
        }
    )
    specification["structure"]["execution_lattice_constant_angstrom"] = 6.482
    specification["structure"]["execution_lattice_constant_source"] = {
        "source_type": "primary_experimental",
        "citation": "Synthetic primary-source record for validator testing",
        "source_sha256": "4" * 64,
        "measurement_temperature_k": 0,
        "reported_lattice_constant_angstrom": 6.482,
        "reported_standard_uncertainty_angstrom": 0.0001,
        "observable_definition": (
            "cubic zincblende lattice parameter from X-ray diffraction"
        ),
        "reference_volume_temperature_k": 0,
    }
    specification["runtime_inputs"].update(
        {
            "runtime_hash_manifest": "runs/cdte_a0/runtime-hashes.json",
            "runtime_hashes_verified": True,
            "rendered_qe_scf_manifest": "runs/cdte_a0/qe-scf.manifest.json",
            "rendered_qe_phonon_manifest": "runs/cdte_a0/qe-ph.manifest.json",
            "rendered_abinit_manifest": "runs/cdte_a0/abinit.manifest.json",
        }
    )
    return specification, selection


def test_repository_a0_specification_fails_closed_on_unresolved_runtime() -> None:
    report = evaluate_readiness(_load(RUN_SPEC_PATH), _load(SELECTION_PATH))

    assert report["ready_for_execution"] is False
    assert {
        "quantum_espresso_installed_binary_recorded",
        "quantum_espresso_release_syntax_checked",
        "abinit_installed_binary_recorded",
        "abinit_release_syntax_checked",
        "runtime_pseudopotential_hashes_verified",
        "render_manifests_recorded",
    }.issubset(report["blocking_checks"])
    assert {
        "execution_lattice_constant_provenance",
        "ecutrho_ladder_declared",
        "k_grid_ladder_declared",
        "band_count_ladder_declared",
    }.isdisjoint(report["blocking_checks"])


def test_source_release_tags_and_commits_are_immutable_pins() -> None:
    specification = _load(RUN_SPEC_PATH)

    assert specification["source_code"]["quantum_espresso"] == {
        "repository": "QEF/q-e",
        "tag": "qe-7.4.1",
        "commit": "500de340b820e1cb8c05f2d8bb8fced102f377c1",
        "executables": ["pw.x", "ph.x"],
        "installed_version_output": None,
        "executable_sha256": {},
        "release_specific_syntax_checked": False,
    }
    assert specification["source_code"]["abinit"] == {
        "repository": "abinit/abinit",
        "tag": "10.6.5",
        "commit": "d50172aacfc501b46cd33ae58fda139e674d40e3",
        "executables": ["abinit"],
        "installed_version_output": None,
        "executable_sha256": {},
        "release_specific_syntax_checked": False,
    }


def test_synthetic_complete_a0_record_passes() -> None:
    specification, selection = _complete_specification()

    report = evaluate_readiness(specification, selection)

    assert report["ready_for_execution"] is True
    assert report["blocking_checks"] == []
    assert report["passed_checks"] == report["total_checks"]


def test_scope_escalation_and_missing_runtime_hashes_fail() -> None:
    specification, selection = _complete_specification()
    specification = copy.deepcopy(specification)
    specification["authorization"]["production_ahc"] = True
    specification["runtime_inputs"]["runtime_hashes_verified"] = False

    report = evaluate_readiness(specification, selection)

    assert report["ready_for_execution"] is False
    assert "a0_scope_authorized" in report["blocking_checks"]
    assert "runtime_pseudopotential_hashes_verified" in report["blocking_checks"]


def test_direct_lattice_source_requires_real_sha256_and_uncertainty() -> None:
    specification, selection = _complete_specification()
    source = specification["structure"]["execution_lattice_constant_source"]
    source["source_sha256"] = "not-a-hash".ljust(64, "x")
    source["reported_standard_uncertainty_angstrom"] = None

    report = evaluate_readiness(specification, selection)

    assert report["ready_for_execution"] is False
    assert "execution_lattice_constant_provenance" in report["blocking_checks"]


def test_temperature_transformation_requires_verified_expansion_manifest() -> None:
    specification, selection = _complete_specification()
    source = specification["structure"]["execution_lattice_constant_source"]
    source["measurement_temperature_k"] = 300
    source["reference_volume_temperature_k"] = 0

    report = evaluate_readiness(specification, selection)
    assert "execution_lattice_constant_provenance" in report["blocking_checks"]

    source["transformation_to_reference"] = {
        "method": "integrate measured linear thermal expansion",
        "thermal_expansion_citation": "Synthetic primary expansion source",
        "thermal_expansion_source_sha256": "5" * 64,
        "thermal_expansion_status": "primary_measurement_acquired_verified",
        "integration_temperature_bounds_k": [0, 300],
        "uncertainty_propagation": "runs/cdte_a0/lattice-uncertainty.json",
        "derivation_manifest": "runs/cdte_a0/lattice-transform.json",
    }

    report = evaluate_readiness(specification, selection)
    assert report["ready_for_execution"] is True


def test_repository_bounded_lattice_path_passes_when_runtime_is_complete() -> None:
    specification, selection = _complete_specification()
    repository_specification = _load(RUN_SPEC_PATH)
    specification["structure"] = copy.deepcopy(repository_specification["structure"])

    report = evaluate_readiness(specification, selection)

    assert report["ready_for_execution"] is True
    assert report["blocking_checks"] == []


def test_bounded_lattice_path_rejects_missing_or_mislabeled_bound() -> None:
    specification, selection = _complete_specification()
    repository_specification = _load(RUN_SPEC_PATH)
    specification["structure"] = copy.deepcopy(repository_specification["structure"])
    source = specification["structure"]["execution_lattice_constant_source"]
    source["execution_uncertainty"]["type"] = "standard_uncertainty"
    source["execution_uncertainty"]["volume_sensitivity_gate_passed"] = False

    report = evaluate_readiness(specification, selection)

    assert report["ready_for_execution"] is False
    assert "execution_lattice_constant_provenance" in report["blocking_checks"]

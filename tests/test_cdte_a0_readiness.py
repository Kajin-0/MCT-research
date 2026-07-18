from __future__ import annotations

import copy
import json
from pathlib import Path

from tools.check_cdte_a0_readiness import evaluate_readiness

RUN_SPEC_PATH = Path("first_principles/a0/cdte_a0_run_spec.json")
SELECTION_PATH = Path("first_principles/a0/cdte_pseudopotential_selection.json")
RUNTIME_REFERENCE_PATH = Path(
    "first_principles/a0/cdte_a0_runtime_readiness_reference.json"
)


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


def test_repository_a0_specification_is_ready_without_result_claim() -> None:
    specification = _load(RUN_SPEC_PATH)
    report = evaluate_readiness(specification, _load(SELECTION_PATH))

    assert report["ready_for_execution"] is True
    assert report["blocking_checks"] == []
    assert report["passed_checks"] == report["total_checks"]
    assert specification["readiness_claim"] == {
        "calculation_executed": False,
        "scientific_result_available": False,
        "ready_for_execution": True,
        "scope": "first declared A0 convergence point only",
        "authorized_next_action": (
            "execute the smallest A0 point and record raw observables; "
            "do not infer convergence from one point"
        ),
        "a1_or_production_authorized": False,
    }


def test_source_release_pins_and_validated_build_hashes_are_recorded() -> None:
    specification = _load(RUN_SPEC_PATH)
    reference = _load(RUNTIME_REFERENCE_PATH)

    qe = specification["source_code"]["quantum_espresso"]
    assert qe["repository"] == "QEF/q-e"
    assert qe["tag"] == "qe-7.4.1"
    assert qe["commit"] == "500de340b820e1cb8c05f2d8bb8fced102f377c1"
    assert qe["executable_sha256"] == {
        "pw.x": "79338a906d5d2e4211dcf3cb5d71706a5bd7bd0dc7e685025485fd5317c609e3",
        "ph.x": "57b99c18169f38ef9691387d56e7d3765be7226ff155bfbd1727ab81c1c396e4",
    }
    assert qe["release_specific_syntax_checked"] is True

    abinit = specification["source_code"]["abinit"]
    assert abinit["repository"] == "abinit/abinit"
    assert abinit["tag"] == "10.6.5"
    assert abinit["commit"] == "d50172aacfc501b46cd33ae58fda139e674d40e3"
    assert abinit["executable_sha256"] == {
        "abinit": "b10a0fa2a0259b2d4525a0bbf1a7bf93e3056414ed90ffe5f12c6113584bb062"
    }
    assert abinit["release_specific_syntax_checked"] is True

    assert reference["verification"]["runtime_workflow_run_id"] == 29623698323
    assert reference["verification"]["artifact_id"] == 8423244947
    assert reference["validation"]["calculation_executed"] is False
    assert reference["validation"]["scientific_result_available"] is False


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

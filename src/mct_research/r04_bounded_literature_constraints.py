"""Validation helpers for the bounded R04 literature constraint package."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping


SCHEMA_VERSION = "r04_bounded_literature_constraints_v1"
DECISION = "BOUNDED_CONSTRAINT_PACKAGE_READY"
SEMANTIC_ROLES = {
    "DESIGN_TARGET",
    "DRIFT_STRESS_CASE",
    "KERNEL_METHOD_BENCHMARK",
    "STM_ARTIFACT_ENVELOPE",
}
REQUIRED_DOIS = {
    "10.1103/physrevmaterials.9.054602",
    "10.1016/j.jcrysgro.2005.01.051",
    "10.1107/s1600577520013211",
    "10.1063/1.4756938",
}


class BoundedConstraintValidationError(ValueError):
    """Raised when the bounded literature package violates a frozen boundary."""


def load_constraint_package(path: str | Path) -> dict[str, Any]:
    """Load a constraint package from JSON."""

    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise BoundedConstraintValidationError(message)


def _constraint_map(record: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    constraints = record.get("constraints")
    _require(isinstance(constraints, list) and constraints, "constraints must be a non-empty list")
    result: dict[str, Mapping[str, Any]] = {}
    for item in constraints:
        _require(isinstance(item, Mapping), "every constraint must be an object")
        constraint_id = item.get("id")
        _require(isinstance(constraint_id, str) and constraint_id, "constraint id is required")
        _require(constraint_id not in result, f"duplicate constraint id: {constraint_id}")
        result[constraint_id] = item
    return result


def validate_constraint_package(record: Mapping[str, Any]) -> None:
    """Validate semantic roles, provenance, derived values, and stop boundaries."""

    _require(record.get("schema_version") == SCHEMA_VERSION, "unexpected schema version")
    _require(record.get("issue") == 403, "constraint package must remain tied to issue #403")
    _require(record.get("decision") == DECISION, "unexpected package decision")
    _require(record.get("outreach_authorized") is False, "outreach must remain disabled")
    _require(
        record.get("cross_paper_specimen_synthesis") is False,
        "cross-paper specimen synthesis is prohibited",
    )
    _require(
        record.get("default_probability_distributions_assigned") is False,
        "unsupported default probability distributions are prohibited",
    )
    _require(record.get("data_ingestion_authorized") is False, "matched-data ingestion remains blocked")
    _require(record.get("new_simulation_authorized") is False, "new simulation remains unauthorized")
    _require(record.get("r05_material_activation") == "BLOCKED", "R05 must remain blocked")
    _require(set(record.get("semantic_roles", [])) == SEMANTIC_ROLES, "semantic role vocabulary changed")

    constraints = _constraint_map(record)
    seen_dois: set[str] = set()
    seen_roles: set[str] = set()
    for constraint in constraints.values():
        _validate_constraint(constraint)
        seen_dois.add(str(constraint["source_doi"]).lower())
        seen_roles.add(str(constraint["semantic_role"]))

    _require(seen_dois == REQUIRED_DOIS, "constraint package DOI coverage changed")
    _require(seen_roles == SEMANTIC_ROLES, "every semantic role must be instantiated")

    _validate_derived_values(constraints)
    _validate_role_specific_boundaries(constraints)

    unsupported = set(record.get("unsupported_quantities", []))
    for phrase in (
        "local random-mass variance",
        "lateral correlation length",
        "measured STS energy-resolution kernel",
        "same-specimen covariance-to-DOS linkage",
        "probability distribution for local composition or mass",
    ):
        _require(phrase in unsupported, f"missing unsupported quantity: {phrase}")

    stop_text = " ".join(record.get("stop_rules", [])).lower()
    for phrase in (
        "different papers",
        "probability distribution",
        "wafer-scale sigma",
        "depth-response kernel",
        "apparent gaps",
        "reactivate r05",
    ):
        _require(phrase in stop_text, f"missing stop-rule safeguard: {phrase}")


def _validate_constraint(constraint: Mapping[str, Any]) -> None:
    required = {
        "id",
        "semantic_role",
        "source_doi",
        "quantity",
        "value",
        "unit",
        "distribution",
        "allowed_use",
        "prohibited_use",
    }
    missing = required.difference(constraint)
    _require(not missing, f"constraint missing fields: {sorted(missing)}")
    _require(constraint["semantic_role"] in SEMANTIC_ROLES, "unknown semantic role")
    _require(str(constraint["source_doi"]).lower() in REQUIRED_DOIS, "unknown source DOI")
    _require(constraint["distribution"] is None, "literature constraints may not assign a distribution")
    _require(bool(constraint["allowed_use"]), "allowed-use list is required")
    _require(bool(constraint["prohibited_use"]), "prohibited-use list is required")

    value = constraint["value"]
    if isinstance(value, list):
        _require(value and all(isinstance(v, (int, float)) for v in value), "numeric list value required")
    else:
        _require(isinstance(value, (int, float)), "numeric value required")


def _validate_derived_values(constraints: Mapping[str, Mapping[str, Any]]) -> None:
    full_sigma = float(constraints["chang_cdte_si_full_sigma_x"]["value"])
    center_sigma = float(constraints["chang_cdte_si_center_sigma_x"]["value"])
    ratio = float(constraints["chang_full_to_center_sigma_ratio"]["value"])
    _require(math.isclose(ratio, full_sigma / center_sigma, rel_tol=1e-12), "Chang sigma ratio mismatch")

    kernel = constraints["biquard_micro_laue_depth_kernel"]
    width_ratio = float(constraints["biquard_measured_to_nominal_width_ratio"]["value"])
    expected_width_ratio = float(kernel["value"]) / float(kernel["nominal_beam_diameter_nm"])
    _require(math.isclose(width_ratio, expected_width_ratio, rel_tol=1e-12), "Biquard width ratio mismatch")

    artifact = constraints["zha_flat_region_apparent_gap_excess"]
    excess = float(artifact["observed_plateau_eV"]) - float(artifact["reported_bulk_gap_eV"])
    _require(math.isclose(float(artifact["value"]), excess, rel_tol=1e-12), "Zha gap excess mismatch")

    gap_ratio = float(constraints["zha_flat_region_apparent_to_bulk_gap_ratio"]["value"])
    expected_gap_ratio = float(artifact["observed_plateau_eV"]) / float(artifact["reported_bulk_gap_eV"])
    _require(math.isclose(gap_ratio, expected_gap_ratio, rel_tol=1e-9), "Zha gap ratio mismatch")


def _validate_role_specific_boundaries(constraints: Mapping[str, Mapping[str, Any]]) -> None:
    boundary_x = constraints["bovkun_qw_boundary_composition"]
    _require(boundary_x["semantic_role"] == "DESIGN_TARGET", "Bovkun boundary must remain a design target")
    _require(boundary_x.get("is_probability_interval") is False, "Bovkun range is not a probability interval")
    _require(boundary_x.get("is_measured_local_variance") is False, "Bovkun range is not local variance")

    broadening = constraints["bovkun_kp_broadening_convention"]
    _require(broadening.get("is_measured_energy_kernel") is False, "model broadening is not a measured kernel")

    for constraint_id in (
        "chang_cdznte_whole_map_sigma_x",
        "chang_cdte_si_center_sigma_x",
        "chang_cdte_si_full_sigma_x",
    ):
        constraint = constraints[constraint_id]
        _require(constraint["semantic_role"] == "DRIFT_STRESS_CASE", "Chang sigma must remain a drift stress case")
        _require(constraint.get("stationary_local_variance") is False, "Chang sigma is not stationary local variance")

    kernel = constraints["biquard_micro_laue_depth_kernel"]
    _require(kernel["semantic_role"] == "KERNEL_METHOD_BENCHMARK", "Biquard response must remain a kernel benchmark")
    _require(kernel.get("geometry") == "cross-sectional depth profiling", "Biquard geometry changed")
    _require(kernel.get("is_target_material_correlation_length") is False, "Biquard response is not a correlation length")

    gap = constraints["zha_flat_region_apparent_gap_excess"]
    _require(gap["semantic_role"] == "STM_ARTIFACT_ENVELOPE", "Zha gap must remain an artifact envelope")
    _require(gap.get("is_measured_energy_kernel") is False, "Zha gap excess is not an energy kernel")
    _require(gap.get("is_direct_local_dos") is False, "Zha plateau is not direct local DOS")

    pit = constraints["zha_bias_dependent_apparent_pit_depth"]
    _require(pit.get("is_geometric_depth_change") is False, "Zha bias contrast is not geometric depth")


def validate_constraint_package_file(path: str | Path) -> None:
    """Load and validate a constraint package from disk."""

    validate_constraint_package(load_constraint_package(path))

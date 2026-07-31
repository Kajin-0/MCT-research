from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


SCHEMA_VERSION = "r04_r05_matched_evidence_v1"

EVIDENCE_CLASSES = {
    "measured_raw",
    "measured_derived",
    "source_established",
    "empirical_model",
    "exploratory_assumption",
    "unresolved",
}

MATERIAL_GATE_EVIDENCE_CLASSES = {
    "measured_raw",
    "measured_derived",
    "source_established",
    "empirical_model",
}

REQUIRED_GATES = (
    "local_variance_gate",
    "correlation_length_gate",
    "same_population_gate",
    "near_critical_gate",
    "resolution_gate",
    "matched_null_gate",
    "robustness_gate",
    "decision_changing_gate",
)

GATE_STATUSES = {"PASS", "FAIL", "UNRESOLVED", "NOT_APPLICABLE"}

DECISIONS = {
    "UNRESOLVED",
    "PUBLIC_DATA_FEASIBLE",
    "PARTNER_DATA_REQUIRED",
    "EXTERNAL_DATA_BLOCKED",
    "EVIDENCE_GATE_FAILED",
    "R05_REACTIVATION_RECOMMENDED",
    "R05_REACTIVATION_NOT_RECOMMENDED",
}


@dataclass(frozen=True)
class EvidenceValidationResult:
    """Validation result for one R04/R05 evidence record."""

    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors

    def require_valid(self) -> None:
        if self.errors:
            joined = "\n- ".join(self.errors)
            raise ValueError(f"Invalid R04/R05 evidence record:\n- {joined}")


def _mapping(value: Any, path: str, errors: list[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        errors.append(f"{path} must be an object")
        return {}
    return value


def _sequence(value: Any, path: str, errors: list[str]) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        errors.append(f"{path} must be an array")
        return ()
    return value


def _require_keys(
    value: Mapping[str, Any],
    required: Sequence[str],
    path: str,
    errors: list[str],
) -> None:
    for key in required:
        if key not in value:
            errors.append(f"{path}.{key} is required")


def _check_evidence_class(value: Any, path: str, errors: list[str]) -> None:
    if value not in EVIDENCE_CLASSES:
        errors.append(f"{path} must be one of {sorted(EVIDENCE_CLASSES)}")


def _check_estimate(value: Any, path: str, errors: list[str]) -> None:
    estimate = _mapping(value, path, errors)
    _require_keys(
        estimate,
        ("value", "units", "interval", "evidence_class", "method"),
        path,
        errors,
    )
    if "evidence_class" in estimate:
        _check_evidence_class(estimate["evidence_class"], f"{path}.evidence_class", errors)
    interval = estimate.get("interval")
    if interval is not None:
        values = _sequence(interval, f"{path}.interval", errors)
        if len(values) != 2:
            errors.append(f"{path}.interval must contain exactly two bounds")
        elif all(isinstance(item, (int, float)) for item in values):
            if values[0] > values[1]:
                errors.append(f"{path}.interval lower bound exceeds upper bound")
        else:
            errors.append(f"{path}.interval bounds must be numeric")


def validate_evidence_record(record: Mapping[str, Any]) -> EvidenceValidationResult:
    """Validate scientific invariants not captured by structural JSON parsing.

    The function intentionally avoids a runtime dependency on ``jsonschema``. The
    normative JSON Schema remains in ``data/schemas``; this validator enforces the
    cross-field claim and reopening rules required by issue #395.
    """

    errors: list[str] = []
    root = _mapping(record, "record", errors)
    _require_keys(
        root,
        (
            "schema_version",
            "record_id",
            "record_state",
            "specimen",
            "spatial_measurement",
            "spectroscopy_measurement",
            "joint_inference",
            "gates",
            "decision",
            "claim_boundary",
            "provenance",
        ),
        "record",
        errors,
    )

    if root.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"record.schema_version must equal {SCHEMA_VERSION}")

    if root.get("record_state") not in {"template", "candidate", "complete"}:
        errors.append("record.record_state must be template, candidate, or complete")

    decision = root.get("decision")
    if decision not in DECISIONS:
        errors.append(f"record.decision must be one of {sorted(DECISIONS)}")

    specimen = _mapping(root.get("specimen"), "record.specimen", errors)
    _require_keys(
        specimen,
        (
            "specimen_id",
            "material",
            "region_relationship",
            "exchangeability_evidence",
            "evidence_class",
        ),
        "record.specimen",
        errors,
    )
    if specimen.get("material") != "Hg1-xCdxTe":
        errors.append("record.specimen.material must equal Hg1-xCdxTe")
    if "evidence_class" in specimen:
        _check_evidence_class(
            specimen["evidence_class"], "record.specimen.evidence_class", errors
        )
    relationship = specimen.get("region_relationship")
    allowed_relationships = {
        "same_region",
        "same_specimen_different_region",
        "adjacent_lamella",
        "same_growth_run",
        "unlinked",
    }
    if relationship not in allowed_relationships:
        errors.append(
            "record.specimen.region_relationship must use the declared relationship vocabulary"
        )
    if relationship not in {None, "same_region", "unlinked"} and not specimen.get(
        "exchangeability_evidence"
    ):
        errors.append(
            "record.specimen.exchangeability_evidence is required when regions are not identical"
        )

    spatial = _mapping(
        root.get("spatial_measurement"), "record.spatial_measurement", errors
    )
    _require_keys(
        spatial,
        (
            "latent_quantity",
            "point_spread_function",
            "depth_kernel",
            "local_variance",
            "correlation_length",
            "covariance_families",
            "wafer_tolerance_used_as_local_sigma",
            "evidence_class",
        ),
        "record.spatial_measurement",
        errors,
    )
    if spatial.get("wafer_tolerance_used_as_local_sigma") is not False:
        errors.append(
            "record.spatial_measurement.wafer_tolerance_used_as_local_sigma must be false"
        )
    if "evidence_class" in spatial:
        _check_evidence_class(
            spatial["evidence_class"],
            "record.spatial_measurement.evidence_class",
            errors,
        )
    _check_estimate(
        spatial.get("local_variance"),
        "record.spatial_measurement.local_variance",
        errors,
    )
    _check_estimate(
        spatial.get("correlation_length"),
        "record.spatial_measurement.correlation_length",
        errors,
    )
    psf = _mapping(
        spatial.get("point_spread_function"),
        "record.spatial_measurement.point_spread_function",
        errors,
    )
    _require_keys(
        psf,
        ("kind", "parameters", "calibration_uri", "evidence_class"),
        "record.spatial_measurement.point_spread_function",
        errors,
    )
    if "evidence_class" in psf:
        _check_evidence_class(
            psf["evidence_class"],
            "record.spatial_measurement.point_spread_function.evidence_class",
            errors,
        )
    families = _sequence(
        spatial.get("covariance_families"),
        "record.spatial_measurement.covariance_families",
        errors,
    )
    if "gaussian" not in families:
        errors.append(
            "record.spatial_measurement.covariance_families must include gaussian"
        )
    if not any(str(item).startswith("matern_") for item in families):
        errors.append(
            "record.spatial_measurement.covariance_families must include at least one Matérn family"
        )

    spectroscopy = _mapping(
        root.get("spectroscopy_measurement"),
        "record.spectroscopy_measurement",
        errors,
    )
    _require_keys(
        spectroscopy,
        (
            "energy_resolution_kernel",
            "band_bending_assessment",
            "surface_state_assessment",
            "evidence_class",
        ),
        "record.spectroscopy_measurement",
        errors,
    )
    if "evidence_class" in spectroscopy:
        _check_evidence_class(
            spectroscopy["evidence_class"],
            "record.spectroscopy_measurement.evidence_class",
            errors,
        )
    energy_kernel = _mapping(
        spectroscopy.get("energy_resolution_kernel"),
        "record.spectroscopy_measurement.energy_resolution_kernel",
        errors,
    )
    _require_keys(
        energy_kernel,
        (
            "kind",
            "parameters",
            "calibration_uri",
            "fwhm_meV",
            "evidence_class",
            "universal_requirement_claimed",
        ),
        "record.spectroscopy_measurement.energy_resolution_kernel",
        errors,
    )
    if energy_kernel.get("universal_requirement_claimed") is not False:
        errors.append(
            "record.spectroscopy_measurement.energy_resolution_kernel.universal_requirement_claimed must be false"
        )
    if "evidence_class" in energy_kernel:
        _check_evidence_class(
            energy_kernel["evidence_class"],
            "record.spectroscopy_measurement.energy_resolution_kernel.evidence_class",
            errors,
        )

    inference = _mapping(
        root.get("joint_inference"), "record.joint_inference", errors
    )
    _require_keys(
        inference,
        (
            "gap_to_mass_convention",
            "m_max",
            "m_max_frozen_before_final_comparison",
            "g_threshold_lower",
            "g_threshold_upper",
            "shared_one_point_distribution",
            "shared_measurement_kernel",
            "evidence_class",
        ),
        "record.joint_inference",
        errors,
    )
    if inference.get("gap_to_mass_convention") != "M=Eg/2":
        errors.append("record.joint_inference.gap_to_mass_convention must equal M=Eg/2")
    if inference.get("g_threshold_lower") != 0.25:
        errors.append("record.joint_inference.g_threshold_lower must equal 0.25")
    if inference.get("g_threshold_upper") != 0.3:
        errors.append("record.joint_inference.g_threshold_upper must equal 0.3")
    if inference.get("shared_one_point_distribution") is not True:
        errors.append(
            "record.joint_inference.shared_one_point_distribution must be true"
        )
    if inference.get("shared_measurement_kernel") is not True:
        errors.append("record.joint_inference.shared_measurement_kernel must be true")
    if "evidence_class" in inference:
        _check_evidence_class(
            inference["evidence_class"],
            "record.joint_inference.evidence_class",
            errors,
        )

    gates = _mapping(root.get("gates"), "record.gates", errors)
    _require_keys(gates, REQUIRED_GATES, "record.gates", errors)
    gate_statuses: dict[str, Any] = {}
    for gate_name in REQUIRED_GATES:
        gate = _mapping(gates.get(gate_name), f"record.gates.{gate_name}", errors)
        _require_keys(gate, ("status", "reason"), f"record.gates.{gate_name}", errors)
        status = gate.get("status")
        gate_statuses[gate_name] = status
        if status not in GATE_STATUSES:
            errors.append(
                f"record.gates.{gate_name}.status must be one of {sorted(GATE_STATUSES)}"
            )
        reason = gate.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"record.gates.{gate_name}.reason must be nonempty")

    if decision == "R05_REACTIVATION_RECOMMENDED":
        failed = [name for name, status in gate_statuses.items() if status != "PASS"]
        if failed:
            errors.append(
                "R05_REACTIVATION_RECOMMENDED requires every gate to PASS; "
                f"nonpassing gates: {failed}"
            )
        if inference.get("m_max_frozen_before_final_comparison") is not True:
            errors.append(
                "R05_REACTIVATION_RECOMMENDED requires m_max to be frozen before final comparison"
            )
        if relationship == "unlinked":
            errors.append(
                "R05_REACTIVATION_RECOMMENDED cannot use unlinked spatial and spectroscopy specimens"
            )
        reopening_classes = {
            "specimen": specimen.get("evidence_class"),
            "spatial_measurement": spatial.get("evidence_class"),
            "local_variance": _mapping(
                spatial.get("local_variance"),
                "record.spatial_measurement.local_variance",
                errors,
            ).get("evidence_class"),
            "correlation_length": _mapping(
                spatial.get("correlation_length"),
                "record.spatial_measurement.correlation_length",
                errors,
            ).get("evidence_class"),
            "spatial_psf": psf.get("evidence_class"),
            "spectroscopy_measurement": spectroscopy.get("evidence_class"),
            "energy_resolution_kernel": energy_kernel.get("evidence_class"),
            "joint_inference": inference.get("evidence_class"),
        }
        weak = {
            name: evidence_class
            for name, evidence_class in reopening_classes.items()
            if evidence_class not in MATERIAL_GATE_EVIDENCE_CLASSES
        }
        if weak:
            errors.append(
                "R05_REACTIVATION_RECOMMENDED cannot rely on exploratory or unresolved evidence: "
                f"{weak}"
            )

    claim_boundary = _sequence(
        root.get("claim_boundary"), "record.claim_boundary", errors
    )
    joined_boundaries = " ".join(str(item) for item in claim_boundary).lower()
    for required_phrase in (
        "not universal",
        "synthetic recovery",
        "topology",
    ):
        if required_phrase not in joined_boundaries:
            errors.append(
                f"record.claim_boundary must preserve a boundary containing '{required_phrase}'"
            )

    return EvidenceValidationResult(tuple(errors))

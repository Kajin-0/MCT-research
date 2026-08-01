"""Validation helpers for the R04/R05 open-literature recovery tranche."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


ALLOWED_DECISIONS = {
    "LITERATURE_CONSTRAINTS_ONLY",
    "PARTIAL_REANALYSIS_FEASIBLE",
    "QUALIFYING_PUBLISHED_DATA_FOUND",
}

ALLOWED_GATE_STATES = {"PASS", "PARTIAL", "FAIL", "NOT_APPLICABLE"}

REQUIRED_GATES = {
    "local_variance",
    "correlation_length",
    "same_population",
    "near_critical",
    "resolution",
    "matched_null",
    "robustness",
    "decision_changing",
}


class OpenLiteratureRecoveryValidationError(ValueError):
    """Raised when an open-literature record violates a frozen boundary."""


def load_open_literature_recovery(path: str | Path) -> dict[str, Any]:
    """Load an open-literature recovery JSON record."""

    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise OpenLiteratureRecoveryValidationError(message)


def validate_open_literature_recovery(record: Mapping[str, Any]) -> None:
    """Validate source access, scientific boundaries, and gate consistency."""

    _require(
        record.get("schema_version") == "r04_r05_open_literature_recovery_v1",
        "unexpected open-literature schema version",
    )
    _require(record.get("issue") == 400, "recovery record must remain tied to issue #400")
    _require(record.get("predecessor_pr") == 401, "predecessor PR must remain #401")
    _require(
        record.get("source_mode") == "PUBLIC_OPEN_ACCESS_AND_AUTHOR_POSTED_LITERATURE",
        "unexpected source mode",
    )
    _require(record.get("outreach_authorized") is False, "outreach must remain disabled")
    _require(
        record.get("cross_paper_specimen_synthesis") is False,
        "cross-paper specimen synthesis is prohibited",
    )
    _require(record.get("overall_decision") in ALLOWED_DECISIONS, "unknown overall decision")
    _require(
        record.get("r05_material_activation") == "BLOCKED",
        "R05 material activation must remain blocked",
    )
    _require(
        record.get("data_ingestion_authorized") is False,
        "literature constraints do not authorize matched-data ingestion",
    )
    _require(
        set(record.get("evidence_gates", [])) == REQUIRED_GATES,
        "the frozen eight-gate vocabulary changed",
    )

    sources = record.get("sources")
    _require(isinstance(sources, list) and len(sources) == 3, "exactly three recovery routes are required")

    seen_dois: set[str] = set()
    qualifying = 0
    for source in sources:
        _validate_source(source)
        doi = source["doi"].lower()
        _require(doi not in seen_dois, f"duplicate DOI: {doi}")
        seen_dois.add(doi)
        if all(value == "PASS" for value in source["gate_status"].values()):
            qualifying += 1

    aggregate = record.get("aggregate_findings", {})
    _require(
        aggregate.get("qualifying_single_source_found") is (qualifying > 0),
        "qualifying-source flag disagrees with source gates",
    )
    _require(
        aggregate.get("qualifying_cross_source_combination_allowed") is False,
        "unrelated literature sources may not be combined into a specimen",
    )
    _require(
        aggregate.get("matched_lateral_covariance_and_local_dos_found") is False,
        "the recovery did not find matched covariance and local DOS",
    )

    if record.get("overall_decision") == "QUALIFYING_PUBLISHED_DATA_FOUND":
        _require(qualifying > 0, "qualifying decision requires one independently qualifying source")

    _require(
        record.get("next_state") == "LITERATURE_RECOVERY_EXHAUSTED_UNLESS_NEW_USER_PAPERS_APPEAR",
        "the bounded literature stop state changed",
    )

    stop_text = " ".join(record.get("stop_rules", [])).lower()
    for phrase in (
        "do not combine",
        "measured energy-resolution kernel",
        "580 nm depth kernel",
        "lateral correlation length",
        "do not reactivate r05",
    ):
        _require(phrase in stop_text, f"missing stop-rule safeguard: {phrase}")


def _validate_source(source: Mapping[str, Any]) -> None:
    required = {
        "source_id",
        "citation",
        "title",
        "doi",
        "access_status",
        "access_route",
        "copyrighted_pdf_committed",
        "source_class",
        "official_sources",
        "gate_status",
        "source_decision",
    }
    missing = required.difference(source)
    _require(not missing, f"source missing fields: {sorted(missing)}")
    _require(source["copyrighted_pdf_committed"] is False, "PDFs must not be committed")
    _require(bool(source["official_sources"]), "source must retain public provenance")
    _require(set(source["gate_status"]) == REQUIRED_GATES, "source gate map is incomplete")
    _require(
        set(source["gate_status"].values()).issubset(ALLOWED_GATE_STATES),
        "source uses an unknown gate state",
    )
    _require(source["source_decision"] in ALLOWED_DECISIONS, "unknown source decision")

    source_id = source["source_id"]
    if source_id == "bovkun_2025_phase_diagram":
        _validate_bovkun(source)
    elif source_id == "biquard_2021_micro_laue":
        _validate_biquard(source)
    elif source_id == "wang_zha_2012_etched_sts":
        _validate_wang_zha(source)
    else:
        raise OpenLiteratureRecoveryValidationError(f"unknown recovery source: {source_id}")


def _validate_bovkun(source: Mapping[str, Any]) -> None:
    _require(source["license"] == "CC_BY_4_0", "Bovkun access license changed")
    samples = source["specimen_series"]["samples"]
    _require([sample["x"] for sample in samples] == [0.04, 0.047, 0.049, 0.052, 0.054, 0.061], "Bovkun sample grid changed")
    _require(
        source["specimen_series"]["thin_qw_xrd_limitation"],
        "thin-well composition-calibration limitation must remain explicit",
    )
    _require(
        source["model_and_resolution"]["broadening_is_measured_instrument_kernel"] is False,
        "model broadening must not be promoted to a measured energy kernel",
    )
    _require(
        source["gate_status"]["near_critical"] == "PASS",
        "Bovkun must retain its near-critical specimen-class contribution",
    )
    _require(source["gate_status"]["local_variance"] == "FAIL", "Bovkun has no local variance map")


def _validate_biquard(source: Mapping[str, Any]) -> None:
    kernel = source["measured_kernel"]
    _require(kernel["measured_fwhm_nm"] == 580, "Biquard measured FWHM changed")
    _require(kernel["composition_profiles_convolved_with_measured_beam"] is True, "kernel-matched comparison must remain explicit")
    _require(
        source["limitations_for_r04_r05"]["geometry"].startswith("cross-sectional"),
        "Biquard geometry must remain cross-sectional",
    )
    _require(source["gate_status"]["correlation_length"] == "FAIL", "depth kernel is not lateral correlation length")
    _require(source["gate_status"]["resolution"] == "PARTIAL", "Biquard supplies only a spatial-kernel contribution")


def _validate_wang_zha(source: Mapping[str, Any]) -> None:
    _require(
        source["access_status"] == "AUTHOR_POSTED_COPY_IDENTIFIED_BUT_NOT_RELIABLY_RETRIEVED",
        "unretrieved STS full text must not be recorded as ingested",
    )
    _require(
        source["incremental_value_after_pr401"] == "LOW_AND_NON_DECISIVE",
        "abstract-only source must remain non-decisive",
    )
    _require(source["gate_status"]["resolution"] == "FAIL", "abstract does not provide a measured energy kernel")


def validate_open_literature_recovery_file(path: str | Path) -> None:
    """Load and validate one recovery record from disk."""

    validate_open_literature_recovery(load_open_literature_recovery(path))

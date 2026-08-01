"""Validation helpers for user-supplied R04/R05 literature batches."""

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


class LiteratureBatchValidationError(ValueError):
    """Raised when a literature-batch record violates a frozen boundary."""


def load_literature_batch(path: str | Path) -> dict[str, Any]:
    """Load a literature-batch JSON record."""

    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise LiteratureBatchValidationError(message)


def validate_literature_batch(record: Mapping[str, Any]) -> None:
    """Validate provenance, gate states, and claim boundaries.

    A literature batch may constrain priors or nuisance models. It may not
    create same-specimen linkage across unrelated papers or authorize R05
    activation unless one source independently passes all eight evidence gates.
    """

    _require(
        record.get("schema_version") == "r04_r05_literature_batch_v1",
        "unexpected literature-batch schema version",
    )
    _require(record.get("issue") == 400, "literature batch must remain tied to issue #400")
    _require(
        record.get("source_mode") == "USER_SUPPLIED_PUBLISHED_PAPERS_ONLY",
        "source mode must remain user-supplied published papers only",
    )
    _require(record.get("outreach_authorized") is False, "outreach must remain disabled")
    _require(
        record.get("overall_decision") in ALLOWED_DECISIONS,
        "unknown overall literature decision",
    )
    _require(
        record.get("r05_material_activation") == "BLOCKED",
        "R05 material activation must remain blocked for this batch",
    )
    _require(
        record.get("data_ingestion_authorized") is False,
        "figure-level literature constraints cannot authorize PR3 data ingestion",
    )
    _require(
        record.get("cross_paper_specimen_synthesis") is False,
        "cross-paper specimen synthesis is prohibited",
    )

    listed_gates = set(record.get("evidence_gates", []))
    _require(listed_gates == REQUIRED_GATES, "the frozen eight-gate vocabulary changed")

    sources = record.get("sources")
    _require(isinstance(sources, list) and sources, "at least one source is required")

    qualifying_sources = 0
    seen_dois: set[str] = set()
    for source in sources:
        _validate_source(source)
        doi = source["doi"].lower()
        _require(doi not in seen_dois, f"duplicate DOI in batch: {doi}")
        seen_dois.add(doi)
        if all(value == "PASS" for value in source["gate_status"].values()):
            qualifying_sources += 1

    aggregate = record.get("aggregate_findings", {})
    _require(
        aggregate.get("qualifying_cross_source_combination_allowed") is False,
        "unrelated papers may not be combined into a qualifying dataset",
    )
    _require(
        aggregate.get("qualifying_single_source_found") is (qualifying_sources > 0),
        "qualifying-source flag disagrees with per-source gates",
    )

    if record.get("overall_decision") == "QUALIFYING_PUBLISHED_DATA_FOUND":
        _require(
            qualifying_sources > 0,
            "qualifying decision requires one source to pass all eight gates independently",
        )

    if record.get("overall_decision") == "PARTIAL_REANALYSIS_FEASIBLE":
        _require(
            any(source.get("figure_reanalysis", {}).get("status") == "FIGURE_DERIVED_ONLY" for source in sources),
            "partial reanalysis requires an explicitly figure-derived path",
        )

    stop_rules = " ".join(record.get("stop_rules", [])).lower()
    for phrase in (
        "do not combine",
        "100 um aperture",
        "stm topography",
        "energy-resolution",
        "reactivate r05",
    ):
        _require(phrase in stop_rules, f"missing stop-rule safeguard: {phrase}")


def _validate_source(source: Mapping[str, Any]) -> None:
    required = {
        "source_id",
        "citation",
        "title",
        "doi",
        "supplied_filename",
        "sha256",
        "page_count",
        "copyrighted_pdf_committed",
        "source_class",
        "scientific_constraints",
        "figure_reanalysis",
        "gate_status",
        "source_decision",
    }
    missing = required.difference(source)
    _require(not missing, f"source missing fields: {sorted(missing)}")

    _require(source["copyrighted_pdf_committed"] is False, "copyrighted PDF must not be committed")
    _require(len(source["sha256"]) == 64, "source SHA-256 must contain 64 hexadecimal characters")
    try:
        int(source["sha256"], 16)
    except ValueError as exc:
        raise LiteratureBatchValidationError("source SHA-256 is not hexadecimal") from exc

    gate_status = source["gate_status"]
    _require(set(gate_status) == REQUIRED_GATES, "source gate map is incomplete")
    _require(
        set(gate_status.values()).issubset(ALLOWED_GATE_STATES),
        "source uses an unknown gate state",
    )
    _require(source["source_decision"] in ALLOWED_DECISIONS, "unknown source decision")

    reanalysis = source["figure_reanalysis"]
    _require(
        reanalysis.get("status") == "FIGURE_DERIVED_ONLY",
        "this batch contains no raw published data archive",
    )
    _require(bool(reanalysis.get("prohibited_outputs")), "figure-derived limits must be explicit")

    source_text = json.dumps(source, sort_keys=True).lower()
    if "chang_2005" in source["source_id"]:
        _require("100.0" in source_text, "Chang record must retain the 100 um aperture")
        _require(
            source["measurement"]["measured_spatial_psf_reported"] is False,
            "Chang aperture must not be promoted to a measured PSF",
        )
        _require(
            source["gate_status"]["correlation_length"] == "FAIL",
            "Chang figures cannot identify the required correlation length",
        )
    if "zha_2012" in source["source_id"]:
        _require(
            source["surface_and_instrument"]["measured_energy_kernel_reported"] is False,
            "Zha paper does not report a measured energy kernel",
        )
        _require(
            source["specimen"]["stm_measurement_temperature"] == "NOT_REPORTED",
            "unreported STM temperature must not be inferred",
        )
        prohibited = " ".join(reanalysis["prohibited_outputs"]).lower()
        _require("geometric pit-depth" in prohibited, "single-bias topography safeguard is missing")


def validate_literature_batch_file(path: str | Path) -> None:
    """Load and validate a literature-batch record from disk."""

    validate_literature_batch(load_literature_batch(path))

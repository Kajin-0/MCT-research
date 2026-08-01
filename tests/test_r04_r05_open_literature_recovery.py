from __future__ import annotations

import copy
from pathlib import Path

import pytest

from mct_research.r04_r05_open_literature_recovery import (
    OpenLiteratureRecoveryValidationError,
    load_open_literature_recovery,
    validate_open_literature_recovery,
)


RECORD_PATH = Path("data/validation/r04_r05_open_literature_recovery_002.json")


def _record() -> dict:
    return load_open_literature_recovery(RECORD_PATH)


def _source(record: dict, source_id: str) -> dict:
    return next(source for source in record["sources"] if source["source_id"] == source_id)


def test_recovery_record_validates() -> None:
    validate_open_literature_recovery(_record())


def test_outreach_remains_disabled() -> None:
    record = _record()
    record["outreach_authorized"] = True
    with pytest.raises(OpenLiteratureRecoveryValidationError, match="outreach"):
        validate_open_literature_recovery(record)


def test_bovkun_model_broadening_is_not_measurement_kernel() -> None:
    record = _record()
    source = _source(record, "bovkun_2025_phase_diagram")
    source["model_and_resolution"]["broadening_is_measured_instrument_kernel"] = True
    with pytest.raises(OpenLiteratureRecoveryValidationError, match="model broadening"):
        validate_open_literature_recovery(record)


def test_bovkun_near_critical_pass_does_not_create_local_variance() -> None:
    record = _record()
    source = _source(record, "bovkun_2025_phase_diagram")
    assert source["gate_status"]["near_critical"] == "PASS"
    assert source["gate_status"]["local_variance"] == "FAIL"
    assert source["gate_status"]["correlation_length"] == "FAIL"


def test_biquard_depth_kernel_is_not_lateral_correlation_length() -> None:
    record = _record()
    source = _source(record, "biquard_2021_micro_laue")
    assert source["measured_kernel"]["measured_fwhm_nm"] == 580
    assert source["gate_status"]["resolution"] == "PARTIAL"
    assert source["gate_status"]["correlation_length"] == "FAIL"

    corrupted = copy.deepcopy(record)
    _source(corrupted, "biquard_2021_micro_laue")["gate_status"]["correlation_length"] = "PASS"
    with pytest.raises(OpenLiteratureRecoveryValidationError, match="depth kernel"):
        validate_open_literature_recovery(corrupted)


def test_unretrieved_sts_copy_cannot_be_recorded_as_ingested() -> None:
    record = _record()
    source = _source(record, "wang_zha_2012_etched_sts")
    source["access_status"] = "FULL_TEXT_RECOVERED"
    with pytest.raises(OpenLiteratureRecoveryValidationError, match="unretrieved STS"):
        validate_open_literature_recovery(record)


def test_cross_paper_specimen_synthesis_is_rejected() -> None:
    record = _record()
    record["cross_paper_specimen_synthesis"] = True
    with pytest.raises(OpenLiteratureRecoveryValidationError, match="cross-paper"):
        validate_open_literature_recovery(record)


def test_r05_activation_remains_blocked() -> None:
    record = _record()
    record["r05_material_activation"] = "ACTIVE"
    with pytest.raises(OpenLiteratureRecoveryValidationError, match="R05 material activation"):
        validate_open_literature_recovery(record)


def test_qualifying_decision_requires_one_independent_source() -> None:
    record = _record()
    record["overall_decision"] = "QUALIFYING_PUBLISHED_DATA_FOUND"
    with pytest.raises(OpenLiteratureRecoveryValidationError, match="independently qualifying"):
        validate_open_literature_recovery(record)


def test_bounded_stop_state_is_frozen() -> None:
    record = _record()
    record["next_state"] = "KEEP_SEARCHING_INDEFINITELY"
    with pytest.raises(OpenLiteratureRecoveryValidationError, match="stop state"):
        validate_open_literature_recovery(record)

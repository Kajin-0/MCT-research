from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.audit_herrmann_model_readiness import audit  # noqa: E402

INPUT = ROOT / "data/evidence/hgcdte_herrmann_readiness.json"


def load_payload() -> dict[str, object]:
    return json.loads(INPUT.read_text(encoding="utf-8"))


def write_payload(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "herrmann.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_exact_table_and_reconstructability_decision() -> None:
    result = audit(INPUT)
    assert result["source_count"] == 2
    assert result["table_i_row_count"] == 8
    assert result["explicit_component_count"] == 4
    assert result["missing_dependency_count"] == 6
    assert result["decision"] == {
        "complete_model_reconstructable": False,
        "exact_transition_table_diagnostics_authorized": True,
        "hybrid_substitution_authorized": False,
        "implementation_authorized": False,
        "universal_gap_fit_authorized": False,
    }


def test_published_transition_discrepancies_are_deterministic() -> None:
    result = audit(INPUT)
    assert result["transition_offset_signed_mean_error_meV"] == pytest.approx(-1.825)
    assert result["transition_offset_mean_absolute_error_meV"] == pytest.approx(2.35)
    assert result["transition_offset_median_absolute_error_meV"] == pytest.approx(1.0)
    assert result["transition_offset_maximum_absolute_error_meV"] == pytest.approx(8.4)
    assert result[
        "transition_absorption_median_calculated_to_measured_ratio"
    ] == pytest.approx(0.8902093596059113)
    assert result[
        "transition_absorption_geometric_mean_calculated_to_measured_ratio"
    ] == pytest.approx(0.8289560553696742)
    assert result["transition_absorption_maximum_factor_error"] == pytest.approx(
        2.865329512893983
    )


def test_table_is_secondary_validation_not_gap_fit_evidence() -> None:
    payload = load_payload()
    semantics = payload["table_i_semantics"]
    assert semantics["status"] == "exact_secondary_model_validation_table"
    assert semantics["independent_specimen_gap_evidence"] is False
    assert semantics["universal_gap_fit_authorized"] is False
    assert audit(INPUT)["copyrighted_source_files_committed"] is False


def test_missing_dependency_inventory_is_fail_closed(tmp_path: Path) -> None:
    payload = load_payload()
    payload["missing_dependencies"] = payload["missing_dependencies"][:-1]
    with pytest.raises(ValueError, match="missing-dependency inventory"):
        audit(write_payload(tmp_path, payload))


def test_model_cannot_be_promoted_without_new_sources(tmp_path: Path) -> None:
    payload = load_payload()
    payload["decision"]["implementation_authorized"] = True
    with pytest.raises(ValueError, match="implementation_authorized"):
        audit(write_payload(tmp_path, payload))


def test_hybrid_substitution_cannot_be_enabled(tmp_path: Path) -> None:
    payload = load_payload()
    payload["decision"]["hybrid_substitution_authorized"] = True
    with pytest.raises(ValueError, match="hybrid_substitution_authorized"):
        audit(write_payload(tmp_path, payload))


def test_exact_table_transcription_is_fail_closed(tmp_path: Path) -> None:
    payload = load_payload()
    payload["table_i_rows"][4][4] = 10.3
    with pytest.raises(ValueError, match="Table I row 5 column 5"):
        audit(write_payload(tmp_path, payload))


def test_recovered_companion_asset_is_hash_bound(tmp_path: Path) -> None:
    payload = load_payload()
    payload["sources"][1]["input_asset_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="asset hash"):
        audit(write_payload(tmp_path, payload))

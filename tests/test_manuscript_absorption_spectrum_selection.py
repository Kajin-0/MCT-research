from __future__ import annotations

import csv
from pathlib import Path

from tools.audit_manuscript_absorption_spectrum_selection import audit

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "data/manuscript/absorption_spectrum_selection.csv"
ACQUISITION = ROOT / "data/manuscript/absorption_source_acquisition_status.csv"


def test_selected_spectra_close_the_coverage_gate() -> None:
    result = audit(SELECTION)
    assert result["spectrum_count"] == 3
    assert result["source_count"] == 2
    assert result["composition_values"] == [0.21, 0.22, 0.31]
    assert result["temperature_range_k"] == [80.0, 300.0]
    assert result["selection_gate_passed"] is True


def test_selection_does_not_authorize_analysis() -> None:
    result = audit(SELECTION)
    assert result["digitization_ready_spectrum_count"] == 0
    assert result["machine_readable_spectrum_count"] == 0
    assert result["analysis_authorized_now"] is False


def test_acquisition_status_matches_selected_spectra_and_remains_fail_closed() -> None:
    with SELECTION.open(newline="", encoding="utf-8") as stream:
        selected = {row["spectrum_id"] for row in csv.DictReader(stream)}
    with ACQUISITION.open(newline="", encoding="utf-8") as stream:
        acquisition_rows = list(csv.DictReader(stream))

    assert {row["spectrum_id"] for row in acquisition_rows} == selected
    assert all(row["primary_full_text_resolved"] == "true" for row in acquisition_rows)
    assert all(row["figure_caption_verified"] == "true" for row in acquisition_rows)
    assert all(row["local_raster_available"] == "false" for row in acquisition_rows)
    assert all(row["axis_calibration_available"] == "false" for row in acquisition_rows)
    assert all(row["machine_readable_points_available"] == "false" for row in acquisition_rows)
    assert {
        row["acquisition_status"] for row in acquisition_rows
    } == {"primary_source_resolved_raster_blocked"}

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
    assert result["composition_values"] == [0.21, 0.226, 0.31]
    assert result["temperature_range_k"] == [80.0, 300.0]
    assert result["selection_gate_passed"] is True


def test_two_moazzami_spectra_authorize_real_spectrum_analysis() -> None:
    result = audit(SELECTION)
    assert result["digitization_ready_spectrum_count"] == 2
    assert result["machine_readable_spectrum_count"] == 2
    assert result["analysis_authorized_now"] is True


def test_acquisition_status_preserves_one_blocked_and_two_complete_records() -> None:
    with SELECTION.open(newline="", encoding="utf-8") as stream:
        selected = {row["spectrum_id"] for row in csv.DictReader(stream)}
    with ACQUISITION.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    assert {row["spectrum_id"] for row in rows} == selected
    by_id = {row["spectrum_id"]: row for row in rows}
    chang = by_id["chang2006_x021_80k"]
    assert chang["local_raster_available"] == "true"
    assert chang["axis_calibration_available"] == "false"
    assert chang["machine_readable_points_available"] == "false"
    assert chang["acquisition_status"] == "primary_figure_recovered_point_separation_blocked"

    for spectrum_id in ("moazzami2005_x022_300k", "moazzami2005_x031_300k"):
        row = by_id[spectrum_id]
        assert row["local_raster_available"] == "true"
        assert row["axis_calibration_available"] == "true"
        assert row["machine_readable_points_available"] == "true"
        assert row["acquisition_status"] == "contract_complete_digitized_primary_figure"

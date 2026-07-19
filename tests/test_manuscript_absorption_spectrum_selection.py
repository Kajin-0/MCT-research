from pathlib import Path

from tools.audit_manuscript_absorption_spectrum_selection import audit

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "data/manuscript/absorption_spectrum_selection.csv"


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

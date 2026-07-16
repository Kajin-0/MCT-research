from pathlib import Path

import pytest

from tools.analyze_laurenti1990_figure2_cd_rich import analyze

DATA = Path("data/experimental/laurenti1990_figure2_cd_rich_digitized.csv")


def test_source_ledger_has_three_anchors_and_eighteen_direct_markers() -> None:
    summary = analyze(DATA)
    assert summary["specimen_count"] == 3
    assert summary["digitized_marker_count"] == 18
    assert summary["source_pdf_sha256"] == (
        "1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea"
    )


def test_observed_room_temperature_shifts_cluster_near_minus_seventy_mev() -> None:
    endpoint = analyze(DATA)["observed_near_300k_shift_mev"]
    assert endpoint["mean"] == pytest.approx(-71.52637218433334)
    assert endpoint["range"] == pytest.approx(3.2152537420000016)
    assert endpoint["population_standard_deviation"] == pytest.approx(
        1.450248531580785
    )


def test_laurenti_reproduces_its_cd_rich_fitting_data_at_digitization_scale() -> None:
    summary = analyze(DATA)
    metrics = summary["model_results"]["Laurenti_1990_equation_7"][
        "nominal_composition_pooled_metrics"
    ]
    assert metrics["rms_mev"] == pytest.approx(3.8922304952058115)
    assert metrics["maximum_absolute_mev"] == pytest.approx(7.7550067252555515)


def test_hansen_cd_rich_temperature_extrapolation_fails_strongly() -> None:
    summary = analyze(DATA)
    nominal = summary["model_results"][
        "Hansen_1982_linear_temperature_extrapolation"
    ]["nominal_composition_pooled_metrics"]
    bounded = summary["model_results"][
        "Hansen_1982_linear_temperature_extrapolation"
    ]["bounded_composition_pooled_metrics"]

    assert nominal["rms_mev"] == pytest.approx(51.15553764397286)
    assert nominal["maximum_absolute_mev"] == pytest.approx(80.68916205792432)
    assert bounded["rms_mev"] == pytest.approx(50.13015270606819)
    assert summary["rms_ratio_hansen_to_laurenti"] == pytest.approx(
        13.142987730809576
    )

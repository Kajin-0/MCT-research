from __future__ import annotations

import math
from pathlib import Path

from tools.analyze_chu_1991_turning_point_series import analyze

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "data/evidence/hgcdte_chu_1991_turning_point_series.json"


def result() -> dict[str, object]:
    return analyze(SERIES)


def test_chu_series_preserves_measurement_and_value_classes() -> None:
    data = result()
    assert data["measurement_class"] == "absorption_turning_point_edge"
    assert data["value_status"] == "printed_figure_labels"
    assert data["temperature_series"]["row_count"] == 7
    assert data["composition_series_300K"]["row_count"] == 8


def test_same_specimen_observed_thermal_increment_is_61_mev() -> None:
    data = result()
    assert data["temperature_series"]["reference_temperature_K"] == 6.0
    assert math.isclose(
        data["decision"]["observed_6_to_300_increment_meV"],
        61.0,
        abs_tol=1e-12,
    )


def test_pade_transfers_worse_than_hansen_at_nominal_composition() -> None:
    comparisons = result()["temperature_series"]["model_comparisons"]
    pade = comparisons["provisional_hansen_pade"]["anchored_increment"]["mae_meV"]
    hansen = comparisons["hansen_1982"]["anchored_increment"]["mae_meV"]
    assert 11.72 < pade < 11.73
    assert 7.21 < hansen < 7.22
    assert 4.50 < pade - hansen < 4.52


def test_pade_hansen_difference_survives_composition_interval() -> None:
    data = result()
    comparisons = data["temperature_series"]["model_comparisons"]
    pade_min = comparisons["provisional_hansen_pade"]["composition_envelope"][
        "anchored_mae_meV_min"
    ]
    hansen_max = comparisons["hansen_1982"]["composition_envelope"][
        "anchored_mae_meV_max"
    ]
    assert pade_min > 10.82
    assert hansen_max < 8.02
    assert pade_min - hansen_max > 2.81
    assert data["decision"][
        "provisional_pade_preferred_for_chu_turning_point_transfer"
    ] is False
    assert data["decision"]["provisional_pade_cross_source_support_weakened"] is True


def test_pade_is_last_in_anchored_increment_screen() -> None:
    rank = result()["temperature_series"]["anchored_mae_rank"]
    assert rank[0] == "laurenti_reconstructed"
    assert rank[-1] == "provisional_hansen_pade"


def test_chu_absolute_fit_is_not_independent_validation() -> None:
    data = result()
    rank = data["composition_series_300K"]["absolute_mae_rank"]
    assert rank[0] == "chu_1983"
    assert data["decision"]["chu_absolute_ranking_independent"] is False


def test_turning_point_transfer_does_not_select_a_material_law_or_refit() -> None:
    decision = result()["decision"]
    assert decision["hansen_over_pade_material_law_selection_authorized"] is False
    assert decision["strict_cross_method_material_law_ranking_authorized"] is False
    assert decision["new_universal_gap_refit_authorized"] is False

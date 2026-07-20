from __future__ import annotations

import math
from pathlib import Path

from tools.analyze_chu_1991_composition_shape import analyze

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "data/evidence/hgcdte_chu_1991_turning_point_series.json"


def result() -> dict[str, object]:
    return analyze(SERIES)


def test_composition_series_inventory_and_provenance() -> None:
    data = result()
    assert data["row_count"] == 8
    assert data["temperature_K"] == 300.0
    assert data["measurement_class"] == "absorption_turning_point_edge"
    assert data["value_status"] == "printed_figure_labels"


def test_raw_absolute_ranking_differs_from_offset_transfer_ranking() -> None:
    data = result()
    assert data["independent_raw_absolute_mae_rank"][0] == "schmit_stelzer_1969"
    assert data["independent_leave_one_out_offset_mae_rank"][0] == "seiler_1990"
    assert data["decision"]["ranking_changes_after_observation_offset"] is True


def test_nominal_leave_one_out_offset_transfer_values() -> None:
    comparisons = result()["model_comparisons"]
    assert math.isclose(
        comparisons["seiler_1990"]["leave_one_specimen_out_offset_transfer"][
            "mae_meV"
        ],
        4.186483084499717,
        abs_tol=1e-10,
    )
    assert math.isclose(
        comparisons["hansen_1982"]["leave_one_specimen_out_offset_transfer"][
            "mae_meV"
        ],
        4.277150356571433,
        abs_tol=1e-10,
    )
    assert math.isclose(
        comparisons["provisional_hansen_pade"][
            "leave_one_specimen_out_offset_transfer"
        ]["mae_meV"],
        7.478883632989254,
        abs_tol=1e-10,
    )


def test_hansen_pade_shape_separation_survives_shared_composition_shift() -> None:
    data = result()
    comparisons = data["model_comparisons"]
    hansen_max = comparisons["hansen_1982"]["shared_composition_shift_envelope"][
        "loo_mae_meV_max"
    ]
    pade_min = comparisons["provisional_hansen_pade"][
        "shared_composition_shift_envelope"
    ]["loo_mae_meV_min"]
    assert hansen_max < 4.320
    assert pade_min > 7.424
    assert pade_min - hansen_max > 3.10
    assert data["decision"]["pade_min_minus_hansen_max_shared_shift_meV"] > 3.10


def test_seiler_hansen_sub_tenth_mev_ordering_is_not_selected() -> None:
    decision = result()["decision"]
    assert abs(decision["seiler_minus_hansen_loo_mae_meV"]) < 0.1
    assert decision["seiler_over_hansen_material_law_selection_authorized"] is False


def test_source_specific_offset_does_not_authorize_universal_correction_or_refit() -> None:
    decision = result()["decision"]
    assert decision["chu_1983_independent_validation_authorized"] is False
    assert decision["universal_observation_offset_authorized"] is False
    assert decision["new_universal_gap_refit_authorized"] is False

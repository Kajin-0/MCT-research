from __future__ import annotations

import numpy as np
import pytest

from mct_research.gap_models import hansen_gap_ev, laurenti_gap_ev
from tools.run_hansen_table1_source_adjustment_diagnostic import (
    hansen_dx,
    laurenti_dx,
    load_table1,
    run_study,
)


def _metric_lookup(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    return {(str(row["model"]), str(row["adjustment"])): row for row in rows}


def test_analytical_composition_derivatives_match_finite_difference() -> None:
    for model, derivative in (
        (hansen_gap_ev, hansen_dx),
        (laurenti_gap_ev, laurenti_dx),
    ):
        for x in (0.199, 0.205, 0.216, 0.5, 0.97):
            temperature_k = 80.0
            step = 1.0e-6
            numerical = (
                float(model(x + step, temperature_k))
                - float(model(x - step, temperature_k))
            ) / (2.0 * step)
            assert derivative(x, temperature_k) == pytest.approx(
                numerical, rel=0.0, abs=2.0e-10
            )


def test_source_energy_and_composition_adjustments_are_numerically_equivalent() -> None:
    observations = load_table1()
    assert len(observations) == 16

    metric_rows, identifiability_rows = run_study()
    lookup = _metric_lookup(metric_rows)

    assert float(lookup[("Hansen", "none")]["mae_mev"]) == pytest.approx(
        2.158015174, abs=1.0e-9
    )
    assert float(lookup[("Laurenti", "none")]["mae_mev"]) == pytest.approx(
        2.961546845, abs=1.0e-9
    )

    for model in ("Hansen", "Laurenti"):
        energy_rmse = float(
            lookup[(model, "source_energy_offsets")]["rmse_mev"]
        )
        composition_rmse = float(
            lookup[(model, "source_composition_shifts")]["rmse_mev"]
        )
        assert abs(energy_rmse - composition_rmse) < 0.002

    hansen_adjusted = float(
        lookup[("Hansen", "source_composition_shifts")]["mae_mev"]
    )
    laurenti_adjusted = float(
        lookup[("Laurenti", "source_composition_shifts")]["mae_mev"]
    )
    assert abs(hansen_adjusted - laurenti_adjusted) < 0.06

    assert len(identifiability_rows) == 4
    for row in identifiability_rows:
        assert float(row["condition_number_scaled"]) > 1300.0
        assert abs(float(row["covariance_correlation_b_dx"])) > 0.999998
        assert float(row["derivative_relative_span"]) < 0.0062


def test_equivalent_offsets_follow_local_gap_sensitivity() -> None:
    metric_rows, _ = run_study()
    lookup = _metric_lookup(metric_rows)

    expected = {
        "Hansen": {"Tobin": 1.62, "Rawe": 1.61},
        "Laurenti": {"Tobin": 1.74, "Rawe": 1.74},
    }
    for model in ("Hansen", "Laurenti"):
        energy = lookup[(model, "source_energy_offsets")]
        composition = lookup[(model, "source_composition_shifts")]
        for source, prefix in (("Tobin", "tobin"), ("Rawe", "rawe")):
            offset_ev = 1.0e-3 * float(energy[f"{prefix}_energy_offset_mev"])
            delta_x = float(composition[f"{prefix}_delta_x"])
            ratio = offset_ev / delta_x
            assert np.isfinite(ratio)
            assert ratio == pytest.approx(expected[model][source], abs=0.02)

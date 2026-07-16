from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_laurenti1990_debye_waller_endpoint import analyze

INPUT = Path("data/theory/laurenti1990_debye_waller_endpoint_inputs.csv")


def test_empirical_endpoint_shifts_reproduce_printed_varshni_parameters() -> None:
    summary = analyze(INPUT)
    materials = summary["materials"]

    assert materials["CdTe"]["empirical_endpoint_gap_shift_mev"] == pytest.approx(
        -77.23791919725376
    )
    assert materials["HgTe"]["empirical_endpoint_gap_shift_mev"] == pytest.approx(
        182.31511254019296
    )


def test_reported_edge_motion_reproduces_debye_waller_gap_shifts() -> None:
    summary = analyze(INPUT)
    materials = summary["materials"]

    assert materials["CdTe"]["debye_waller_gap_shift_mev"] == pytest.approx(
        -191.0
    )
    assert materials["HgTe"]["debye_waller_gap_shift_mev"] == pytest.approx(
        -141.0
    )
    assert materials["CdTe"]["absolute_magnitude_ratio"] == pytest.approx(
        2.4728786324786327
    )


def test_hgte_sign_failure_is_robust_to_printed_rounding() -> None:
    summary = analyze(INPUT)
    hgte = summary["materials"]["HgTe"]

    assert hgte["same_sign"] is False
    assert hgte["printed_rounding_empirical_interval_mev"] == pytest.approx(
        [180.57784911717494, 184.05797101449275]
    )
    assert hgte["printed_rounding_debye_waller_interval_mev"] == pytest.approx(
        [-142.0, -140.0]
    )
    assert hgte["printed_rounding_residual_interval_mev"] == pytest.approx(
        [-326.05797101449275, -320.57784911717494]
    )


def test_endpoint_sign_topology_falsifies_complete_debye_waller_model() -> None:
    summary = analyze(INPUT)
    topology = summary["endpoint_topology"]

    assert topology["empirical_endpoint_sign_reversal"] is True
    assert topology["debye_waller_endpoint_sign_reversal"] is False
    assert summary["materials"]["CdTe"]["same_sign"] is True
    assert summary["materials"]["HgTe"]["same_sign"] is False

from __future__ import annotations

import numpy as np
import pytest

from mct_research.historical_gap_models import (
    SEILER_1990_A_K3,
    SEILER_1990_B_K2,
    SEILER_1990_SOURCE_DOI,
    seiler_1990_gap_ev,
)


def test_seiler_1990_published_constants_and_reference_values() -> None:
    assert SEILER_1990_A_K3 == -1822.0
    assert SEILER_1990_B_K2 == 255.2
    assert SEILER_1990_SOURCE_DOI == "10.1116/1.576952"
    assert seiler_1990_gap_ev(0.155, 77.0) == pytest.approx(
        0.007930824007761694,
        abs=1.0e-15,
    )
    assert seiler_1990_gap_ev(0.259, 75.0) == pytest.approx(
        0.17641052401665683,
        abs=1.0e-15,
    )


def test_seiler_1990_is_not_zero_anchored() -> None:
    assert seiler_1990_gap_ev(0.0, 0.0) == pytest.approx(
        -0.305819631661442,
        abs=1.0e-15,
    )
    assert seiler_1990_gap_ev(1.0, 0.0) == pytest.approx(
        1.653819631661442,
        abs=1.0e-15,
    )


def test_seiler_1990_broadcasting_and_validation() -> None:
    values = seiler_1990_gap_ev(np.array([0.226, 0.310]), 300.0)
    np.testing.assert_allclose(
        values,
        [0.19011175067821742, 0.3040585564043113],
        rtol=0.0,
        atol=1.0e-15,
    )
    with pytest.raises(ValueError, match="mole fraction"):
        seiler_1990_gap_ev(-0.01, 77.0)
    with pytest.raises(ValueError, match="non-negative"):
        seiler_1990_gap_ev(0.2, -1.0)

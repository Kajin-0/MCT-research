from __future__ import annotations

import numpy as np
import pytest

from mct_research.gap_models import (
    bracketed_root,
    critical_composition,
    critical_temperature_k,
    hansen_gap_ev,
    laurenti_gap_ev,
)


def test_hansen_reference_values() -> None:
    assert hansen_gap_ev(0.155, 77.0) == pytest.approx(0.009212564, abs=1.0e-12)
    assert critical_temperature_k(hansen_gap_ev, 0.155) == pytest.approx(
        52.0427, abs=1.0e-4
    )


def test_laurenti_reproduces_teppe_transition() -> None:
    assert laurenti_gap_ev(0.155, 77.0) == pytest.approx(
        -4.78120358e-5, abs=1.0e-12
    )
    assert critical_temperature_k(laurenti_gap_ev, 0.155) == pytest.approx(
        77.124121892, abs=1.0e-8
    )
    assert critical_composition(laurenti_gap_ev, 77.0) == pytest.approx(
        0.1550278120, abs=1.0e-9
    )


def test_laurenti_endpoint_and_low_temperature_values() -> None:
    assert laurenti_gap_ev(0.0, 0.0) == pytest.approx(-0.303)
    assert laurenti_gap_ev(1.0, 0.0) == pytest.approx(1.606)
    assert laurenti_gap_ev(0.175, 2.0) == pytest.approx(0.012078255408)
    assert laurenti_gap_ev(0.155, 2.0) == pytest.approx(-0.024324840477)


def test_laurenti_has_zero_linear_temperature_slope_at_zero() -> None:
    x = 0.155
    step = 1.0e-4
    numerical_slope = (laurenti_gap_ev(x, step) - laurenti_gap_ev(x, 0.0)) / step
    assert numerical_slope == pytest.approx(0.0, abs=1.0e-8)


def test_array_broadcasting() -> None:
    values = laurenti_gap_ev(np.array([0.155, 0.175]), 77.0)
    assert isinstance(values, np.ndarray)
    np.testing.assert_allclose(values, [-4.78120358e-5, 0.03442801849])


def test_input_validation() -> None:
    with pytest.raises(ValueError, match="mole fraction"):
        hansen_gap_ev(-0.01, 77.0)
    with pytest.raises(ValueError, match="mole fraction"):
        laurenti_gap_ev(1.01, 77.0)
    with pytest.raises(ValueError, match="non-negative"):
        laurenti_gap_ev(0.2, -1.0)


def test_bracketed_root_rejects_unbracketed_interval() -> None:
    with pytest.raises(ValueError, match="not bracketed"):
        bracketed_root(lambda value: value**2 + 1.0, -1.0, 1.0)

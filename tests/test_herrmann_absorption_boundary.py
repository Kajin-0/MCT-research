from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from mct_research.herrmann_absorption import (
    BOLTZMANN_EV_PER_K,
    HERRMANN_1992_PRECURSOR_DOI,
    HERRMANN_1993_SOURCE_DOI,
    herrmann_equilibrium_band_filling_factor,
    herrmann_urbach_tail_alpha_cm1,
    herrmann_urbach_width_ev,
)
from tools.audit_herrmann_absorption_boundary import audit

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "data/evidence/hgcdte_herrmann_1993_operator_boundary.json"


def test_source_identifiers_are_explicit() -> None:
    assert HERRMANN_1993_SOURCE_DOI == "10.1063/1.352954"
    assert HERRMANN_1992_PRECURSOR_DOI == "10.1016/0022-0248(92)90851-9"


def test_urbach_width_matches_explicit_temperature_law() -> None:
    assert math.isclose(
        herrmann_urbach_width_ev(0.0, 0.005, 1.0),
        0.005,
        abs_tol=1e-15,
    )
    expected = 0.005 + BOLTZMANN_EV_PER_K * 300.0
    assert math.isclose(
        herrmann_urbach_width_ev(300.0, 0.005, 1.0),
        expected,
        abs_tol=1e-15,
    )


def test_urbach_tail_is_anchored_and_has_declared_log_slope() -> None:
    transition = 0.200
    alpha0 = 1000.0
    width = 0.005
    assert math.isclose(
        herrmann_urbach_tail_alpha_cm1(transition, transition, alpha0, width),
        alpha0,
        abs_tol=1e-12,
    )
    value = herrmann_urbach_tail_alpha_cm1(transition - 0.010, transition, alpha0, width)
    assert math.isclose(value, alpha0 * math.exp(-2.0), rel_tol=1e-14)


def test_urbach_tail_vectorizes_and_remains_monotone() -> None:
    energy = np.array([0.180, 0.185, 0.190, 0.195, 0.200])
    absorption = herrmann_urbach_tail_alpha_cm1(energy, 0.200, 800.0, 0.006)
    assert isinstance(absorption, np.ndarray)
    assert np.all(np.diff(absorption) > 0.0)
    assert math.isclose(float(absorption[-1]), 800.0, abs_tol=1e-12)


def test_urbach_primitive_fails_closed_above_transition() -> None:
    with pytest.raises(ValueError, match="restricted"):
        herrmann_urbach_tail_alpha_cm1(0.201, 0.200, 1000.0, 0.005)


def test_equilibrium_band_filling_limit_has_expected_symmetry() -> None:
    split = 0.150
    temperature = 80.0
    delta = 0.010
    center = herrmann_equilibrium_band_filling_factor(split, split, temperature)
    below = herrmann_equilibrium_band_filling_factor(split - delta, split, temperature)
    above = herrmann_equilibrium_band_filling_factor(split + delta, split, temperature)
    assert math.isclose(center, 0.0, abs_tol=1e-15)
    assert math.isclose(below, -above, rel_tol=1e-14, abs_tol=1e-14)
    with pytest.raises(ValueError, match="positive"):
        herrmann_equilibrium_band_filling_factor(0.2, 0.1, 0.0)


def test_boundary_audit_blocks_full_operator_and_edge_envelope_update() -> None:
    result = audit(BOUNDARY)
    assert result["recoverable_primitive_count"] == 3
    assert result["blocked_component_count"] == 4
    assert result["source_asset_bound"] is True
    assert result["precursor_full_text_recovered"] is False
    assert result["full_operator_authorized"] is False
    assert result["existing_edge_envelope_update_authorized"] is False

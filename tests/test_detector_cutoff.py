from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.detector_cutoff import (
    absorption_for_target_response_cm_inverse,
    chang_2006_cutoff_jacobian,
    chang_2006_response_cutoff,
    cutoff_wavelength_um,
    single_pass_absorptance,
    urbach_tail_cutoff_energy_ev,
    urbach_thickness_shift_ev,
)

EDGE_EV = 0.100
WIDTH_EV = 0.012
B_EV = 0.100
AMPLITUDE_CM1 = 50000.0


def test_single_pass_response_inverse() -> None:
    target_alpha = absorption_for_target_response_cm_inverse(10.0, 0.5)
    assert target_alpha == pytest.approx(693.1471805599453)
    response = single_pass_absorptance(np.asarray([target_alpha]), 10.0)
    assert response[0] == pytest.approx(0.5, abs=1.0e-15)


def test_cutoff_wavelength_conversion() -> None:
    assert cutoff_wavelength_um(0.1) == pytest.approx(12.398419843320026)


def test_tail_cutoff_matches_full_chang_operator() -> None:
    numerical = chang_2006_response_cutoff(
        edge_ev=EDGE_EV,
        urbach_width_ev=WIDTH_EV,
        hyperbola_b_ev=B_EV,
        amplitude_cm_inverse=AMPLITUDE_CM1,
        effective_thickness_um=5.0,
        target_response=0.5,
    )
    analytical = urbach_tail_cutoff_energy_ev(
        join_energy_ev=numerical.join_energy_ev,
        tail_energy_ev=WIDTH_EV,
        join_absorption_cm_inverse=numerical.join_absorption_cm_inverse,
        effective_thickness_um=5.0,
        target_response=0.5,
    )

    assert numerical.branch == "tail"
    assert numerical.energy_ev == pytest.approx(0.0996292713225439, abs=2.0e-12)
    assert analytical == pytest.approx(numerical.energy_ev, abs=2.0e-12)


def test_tail_cutoff_has_logarithmic_thickness_shift() -> None:
    thin = chang_2006_response_cutoff(
        edge_ev=EDGE_EV,
        urbach_width_ev=WIDTH_EV,
        hyperbola_b_ev=B_EV,
        amplitude_cm_inverse=AMPLITUDE_CM1,
        effective_thickness_um=5.0,
        target_response=0.5,
    )
    thick = chang_2006_response_cutoff(
        edge_ev=EDGE_EV,
        urbach_width_ev=WIDTH_EV,
        hyperbola_b_ev=B_EV,
        amplitude_cm_inverse=AMPLITUDE_CM1,
        effective_thickness_um=20.0,
        target_response=0.5,
    )

    expected_shift = urbach_thickness_shift_ev(WIDTH_EV, 4.0)
    assert thin.branch == thick.branch == "tail"
    assert thick.energy_ev - thin.energy_ev == pytest.approx(
        expected_shift,
        abs=3.0e-12,
    )
    assert expected_shift == pytest.approx(-0.01663553233343869)
    assert thin.wavelength_um == pytest.approx(12.444541657, rel=2.0e-8)
    assert thick.wavelength_um == pytest.approx(14.93901613, rel=2.0e-8)


def test_source_domain_rejects_too_thick_tail_crossing() -> None:
    with pytest.raises(ValueError, match="below the authorized"):
        chang_2006_response_cutoff(
            edge_ev=EDGE_EV,
            urbach_width_ev=WIDTH_EV,
            hyperbola_b_ev=B_EV,
            amplitude_cm_inverse=AMPLITUDE_CM1,
            effective_thickness_um=50.0,
            target_response=0.5,
        )


def test_thin_detector_crossing_enters_intrinsic_branch() -> None:
    result = chang_2006_response_cutoff(
        edge_ev=EDGE_EV,
        urbach_width_ev=WIDTH_EV,
        hyperbola_b_ev=B_EV,
        amplitude_cm_inverse=AMPLITUDE_CM1,
        effective_thickness_um=1.0,
        target_response=0.5,
    )
    assert result.branch == "intrinsic"
    assert result.energy_ev == pytest.approx(0.14726943525940045, abs=2.0e-12)


def test_all_tail_cutoffs_have_rank_two() -> None:
    designs = [
        (1.0, 0.10),
        (2.0, 0.10),
        (2.0, 0.25),
        (5.0, 0.25),
        (5.0, 0.50),
        (10.0, 0.50),
        (20.0, 0.50),
        (10.0, 0.75),
        (20.0, 0.75),
    ]
    diagnostics = chang_2006_cutoff_jacobian(
        edge_ev=EDGE_EV,
        urbach_width_ev=WIDTH_EV,
        hyperbola_b_ev=B_EV,
        amplitude_cm_inverse=AMPLITUDE_CM1,
        designs=designs,
    )

    assert set(diagnostics.branches) == {"tail"}
    assert diagnostics.numerical_rank == 2
    assert diagnostics.relative_singular_values[2] < 1.0e-9
    assert diagnostics.relative_singular_values[3] < 1.0e-9


def test_mixed_tail_intrinsic_design_restores_rank_but_is_ill_conditioned() -> None:
    designs = [
        (1.0, 0.25),
        (1.0, 0.50),
        (2.0, 0.50),
        (1.0, 0.75),
        (2.0, 0.75),
        (5.0, 0.75),
        (2.0, 0.90),
        (5.0, 0.90),
        (10.0, 0.90),
        (20.0, 0.90),
    ]
    diagnostics = chang_2006_cutoff_jacobian(
        edge_ev=EDGE_EV,
        urbach_width_ev=WIDTH_EV,
        hyperbola_b_ev=B_EV,
        amplitude_cm_inverse=AMPLITUDE_CM1,
        designs=designs,
    )

    assert set(diagnostics.branches) == {"tail", "intrinsic"}
    assert diagnostics.numerical_rank == 4
    assert diagnostics.condition_number == pytest.approx(199.81, rel=0.02)
    assert diagnostics.relative_singular_values[-1] == pytest.approx(
        0.00500,
        rel=0.03,
    )


def test_cutoff_input_validation() -> None:
    with pytest.raises(ValueError, match="strictly between"):
        absorption_for_target_response_cm_inverse(10.0, 1.0)
    with pytest.raises(ValueError, match="non-negative"):
        single_pass_absorptance(np.asarray([-1.0]), 10.0)
    with pytest.raises(ValueError, match="above the Urbach"):
        urbach_tail_cutoff_energy_ev(
            join_energy_ev=0.1,
            tail_energy_ev=0.01,
            join_absorption_cm_inverse=100.0,
            effective_thickness_um=1.0,
            target_response=0.9,
        )
    with pytest.raises(ValueError, match="must not be empty"):
        chang_2006_cutoff_jacobian(
            edge_ev=EDGE_EV,
            urbach_width_ev=WIDTH_EV,
            hyperbola_b_ev=B_EV,
            amplitude_cm_inverse=AMPLITUDE_CM1,
            designs=[],
        )

from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.carrier_filling import (
    HBAR2_OVER_2M0_EV_A2,
    carrier_edge_density_series_jacobian,
    carrier_filled_optical_edge_ev,
    density_scaled_bandgap_renormalization_ev,
    fermi_wavevector_inverse_angstrom,
    kane_nonparabolic_energy_ev_from_parabolic,
    parabolic_kinetic_energy_ev,
)


def test_fermi_wavevector_reference() -> None:
    wavevector = fermi_wavevector_inverse_angstrom(7.0e17)
    assert wavevector == pytest.approx(0.02746879954226066, rel=1.0e-13)
    assert HBAR2_OVER_2M0_EV_A2 == pytest.approx(3.80998211615486)


def test_parabolic_and_nonparabolic_limits() -> None:
    wavevector = fermi_wavevector_inverse_angstrom(7.0e17)
    parabolic = parabolic_kinetic_energy_ev(wavevector, 0.01)
    assert parabolic == pytest.approx(0.28747646590097786, rel=1.0e-12)
    assert kane_nonparabolic_energy_ev_from_parabolic(parabolic, 0.0) == parabolic

    alpha = 7.5
    nonparabolic = kane_nonparabolic_energy_ev_from_parabolic(parabolic, alpha)
    assert nonparabolic == pytest.approx(0.14015364156709495, rel=1.0e-12)
    assert nonparabolic * (1.0 + alpha * nonparabolic) == pytest.approx(
        parabolic,
        rel=1.0e-13,
    )


def test_low_density_recovers_parabolic_limit() -> None:
    wavevector = fermi_wavevector_inverse_angstrom(1.0e14)
    parabolic = parabolic_kinetic_energy_ev(wavevector, 0.01)
    nonparabolic = kane_nonparabolic_energy_ev_from_parabolic(parabolic, 7.5)
    assert parabolic == pytest.approx(7.856038513359774e-4, rel=1.0e-12)
    assert nonparabolic == pytest.approx(7.810288063632089e-4, rel=1.0e-12)
    assert (parabolic - nonparabolic) < 5.0e-6


def test_dingrong_density_sensitivity_reference() -> None:
    density = 7.0e17
    bgr = density_scaled_bandgap_renormalization_ev(density, 0.020)
    result = carrier_filled_optical_edge_ev(
        zero_density_gap_ev=0.100,
        electron_density_cm3=density,
        conduction_edge_mass_ratio=0.010,
        nonparabolicity_ev_inverse=7.5,
        valence_mass_ratio=0.35,
        bandgap_renormalization_ev=bgr,
    )

    assert result.fermi_wavevector_inverse_angstrom == pytest.approx(
        0.02746879954226066,
        rel=1.0e-13,
    )
    assert result.parabolic_conduction_energy_ev == pytest.approx(
        0.28747646590097786,
        rel=1.0e-12,
    )
    assert result.nonparabolic_conduction_energy_ev == pytest.approx(
        0.14015364156709495,
        rel=1.0e-12,
    )
    assert result.valence_recoil_energy_ev == pytest.approx(
        0.008213613311456511,
        rel=1.0e-12,
    )
    assert result.burstein_moss_shift_ev == pytest.approx(
        0.14836725487855146,
        rel=1.0e-12,
    )
    assert result.bandgap_renormalization_ev == pytest.approx(
        -0.017758080034852013,
        rel=1.0e-12,
    )
    assert result.optical_edge_ev == pytest.approx(
        0.23060917484369944,
        rel=1.0e-12,
    )
    assert result.parabolic_overestimate_ev == pytest.approx(
        0.1473228243338829,
        rel=1.0e-12,
    )
    assert result.nonparabolicity_parameter == pytest.approx(
        2.156073494257334,
        rel=1.0e-12,
    )


def test_parabolic_overestimate_grows_with_density() -> None:
    densities = [1.0e14, 1.0e15, 1.0e16, 1.0e17, 7.0e17]
    overestimates = []
    for density in densities:
        result = carrier_filled_optical_edge_ev(
            zero_density_gap_ev=0.100,
            electron_density_cm3=density,
            conduction_edge_mass_ratio=0.010,
            nonparabolicity_ev_inverse=7.5,
            valence_mass_ratio=0.35,
        )
        overestimates.append(result.parabolic_overestimate_ev)

    assert np.all(np.diff(overestimates) > 0.0)
    np.testing.assert_allclose(
        np.asarray(overestimates) * 1000.0,
        [0.004575045, 0.094616417, 1.731411784, 23.08302836, 147.32282433],
        rtol=2.0e-8,
    )


def test_one_edge_has_rank_one() -> None:
    diagnostics = carrier_edge_density_series_jacobian(
        electron_densities_cm3=[7.0e17],
        zero_density_gap_ev=0.100,
        conduction_edge_mass_ratio=0.010,
        nonparabolicity_ev_inverse=7.5,
        valence_mass_ratio=0.35,
        bgr_coefficient_ev_at_1e18_cm3=0.020,
    )
    assert diagnostics.numerical_rank == 1
    assert diagnostics.singular_values.size == 1
    assert math.isinf(diagnostics.condition_number)


def test_five_density_series_is_full_rank_but_ill_conditioned() -> None:
    diagnostics = carrier_edge_density_series_jacobian(
        electron_densities_cm3=[1.0e16, 3.0e16, 1.0e17, 3.0e17, 7.0e17],
        zero_density_gap_ev=0.100,
        conduction_edge_mass_ratio=0.010,
        nonparabolicity_ev_inverse=7.5,
        valence_mass_ratio=0.35,
        bgr_coefficient_ev_at_1e18_cm3=0.020,
    )

    assert diagnostics.numerical_rank == 5
    assert diagnostics.condition_number == pytest.approx(11034.75, rel=2.0e-4)
    np.testing.assert_allclose(
        diagnostics.relative_singular_values,
        [1.0, 0.259838534, 0.0181695971, 0.0007118022, 0.0000906228],
        rtol=3.0e-5,
    )
    np.testing.assert_allclose(
        diagnostics.optical_edges_ev,
        [0.1113686214, 0.1237207269, 0.1484387615, 0.1865788246, 0.2306091748],
        rtol=2.0e-9,
    )


def test_carrier_filling_input_validation() -> None:
    with pytest.raises(ValueError, match="electron_density_cm3"):
        fermi_wavevector_inverse_angstrom(0.0)
    with pytest.raises(ValueError, match="effective_mass_ratio"):
        parabolic_kinetic_energy_ev(0.01, 0.0)
    with pytest.raises(ValueError, match="non-negative"):
        kane_nonparabolic_energy_ev_from_parabolic(0.1, -1.0)
    with pytest.raises(ValueError, match="must not be empty"):
        carrier_edge_density_series_jacobian(
            electron_densities_cm3=[],
            zero_density_gap_ev=0.100,
            conduction_edge_mass_ratio=0.010,
            nonparabolicity_ev_inverse=7.5,
            valence_mass_ratio=0.35,
            bgr_coefficient_ev_at_1e18_cm3=0.020,
        )
    with pytest.raises(ValueError, match="must be unique"):
        carrier_edge_density_series_jacobian(
            electron_densities_cm3=[1.0e17, 1.0e17],
            zero_density_gap_ev=0.100,
            conduction_edge_mass_ratio=0.010,
            nonparabolicity_ev_inverse=7.5,
            valence_mass_ratio=0.35,
            bgr_coefficient_ev_at_1e18_cm3=0.020,
        )

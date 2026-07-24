from dataclasses import replace

import numpy as np
import pytest

from mct_research.transport_noise.statistics_interface import (
    BipolarStatisticsState,
    CarrierStatisticsClosure,
    ParabolicFermiClosure,
    evaluate_parabolic_bipolar_statistics,
    evaluate_parabolic_carrier_statistics,
    thermodynamic_identity_relative_error,
)
from mct_research.transport_noise.statistics_prototype import BOLTZMANN_EV_PER_K


def test_rejects_invalid_input_domain():
    with pytest.raises(ValueError):
        evaluate_parabolic_carrier_statistics(
            eta=0.0,
            temperature_k=0.0,
            density_scale_cm3=1.0e16,
        )
    with pytest.raises(ValueError):
        evaluate_parabolic_carrier_statistics(
            eta=np.inf,
            temperature_k=77.0,
            density_scale_cm3=1.0e16,
        )
    with pytest.raises(ValueError):
        ParabolicFermiClosure(density_scale_cm3=-1.0)


def test_generalized_einstein_identity_is_exact_by_construction():
    state = evaluate_parabolic_carrier_statistics(
        eta=0.7,
        temperature_k=77.0,
        density_scale_cm3=2.5e16,
    )
    assert thermodynamic_identity_relative_error(state) < 1.0e-14
    assert state.thermodynamic_einstein_ratio == pytest.approx(
        state.generalized_einstein_factor,
        rel=1.0e-14,
    )


def test_compressibility_matches_density_finite_difference():
    eta = -0.4
    temperature = 120.0
    scale = 7.0e15
    step = 2.0e-5
    center = evaluate_parabolic_carrier_statistics(
        eta=eta,
        temperature_k=temperature,
        density_scale_cm3=scale,
    )
    plus = evaluate_parabolic_carrier_statistics(
        eta=eta + step,
        temperature_k=temperature,
        density_scale_cm3=scale,
    )
    minus = evaluate_parabolic_carrier_statistics(
        eta=eta - step,
        temperature_k=temperature,
        density_scale_cm3=scale,
    )
    derivative_with_respect_to_eta = (
        plus.density_cm3 - minus.density_cm3
    ) / (2.0 * step)
    expected = (
        BOLTZMANN_EV_PER_K
        * temperature
        * center.compressibility_cm3_per_ev
    )
    assert derivative_with_respect_to_eta == pytest.approx(expected, rel=2.0e-8)


def test_boltzmann_limit_recovers_unit_einstein_factor():
    state = evaluate_parabolic_carrier_statistics(
        eta=-12.0,
        temperature_k=77.0,
        density_scale_cm3=1.0e16,
    )
    assert state.normalized_density == pytest.approx(np.exp(-12.0), rel=3.0e-6)
    assert state.generalized_einstein_factor == pytest.approx(1.0, rel=3.0e-6)


def test_degenerate_statistics_increase_einstein_factor():
    state = evaluate_parabolic_carrier_statistics(
        eta=3.0,
        temperature_k=77.0,
        density_scale_cm3=1.0e16,
    )
    assert state.generalized_einstein_factor > 1.0


def test_density_is_monotone_in_reduced_chemical_potential():
    closure = ParabolicFermiClosure(density_scale_cm3=1.0e16)
    values = [
        closure.evaluate(eta=eta, temperature_k=77.0).density_cm3
        for eta in (-6.0, -2.0, 0.0, 2.0)
    ]
    assert np.all(np.diff(values) > 0.0)


def test_parabolic_closure_satisfies_runtime_protocol():
    closure = ParabolicFermiClosure(density_scale_cm3=1.0e16)
    assert isinstance(closure, CarrierStatisticsClosure)


def test_bipolar_state_uses_one_temperature_and_sums_susceptibilities():
    state = evaluate_parabolic_bipolar_statistics(
        electron_eta=-1.2,
        hole_eta=-0.7,
        temperature_k=90.0,
        electron_density_scale_cm3=2.0e16,
        hole_density_scale_cm3=3.0e16,
    )
    assert state.net_charge_number_density_cm3 == pytest.approx(
        state.hole.density_cm3 - state.electron.density_cm3
    )
    assert state.charge_compressibility_cm3_per_ev == pytest.approx(
        state.electron.compressibility_cm3_per_ev
        + state.hole.compressibility_cm3_per_ev
    )
    assert state.charge_compressibility_cm3_per_ev > 0.0


def test_bipolar_state_rejects_temperature_mismatch():
    electron = evaluate_parabolic_carrier_statistics(
        eta=-1.0,
        temperature_k=77.0,
        density_scale_cm3=1.0e16,
    )
    hole = replace(electron, temperature_k=78.0)
    with pytest.raises(ValueError):
        BipolarStatisticsState(electron=electron, hole=hole)


def test_density_scale_is_explicit_and_linear():
    first = evaluate_parabolic_carrier_statistics(
        eta=0.2,
        temperature_k=77.0,
        density_scale_cm3=1.0e15,
    )
    second = evaluate_parabolic_carrier_statistics(
        eta=0.2,
        temperature_k=77.0,
        density_scale_cm3=4.0e15,
    )
    assert second.density_cm3 == pytest.approx(4.0 * first.density_cm3)
    assert second.compressibility_cm3_per_ev == pytest.approx(
        4.0 * first.compressibility_cm3_per_ev
    )
    assert second.generalized_einstein_factor == pytest.approx(
        first.generalized_einstein_factor
    )

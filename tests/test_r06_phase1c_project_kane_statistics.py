import json
from pathlib import Path

import numpy as np
import pytest

from mct_research.transport_noise.project_kane_statistics import (
    MODEL_IDENTITY,
    KaneQuadratureOptions,
    ProjectDefinedKaneClosure,
    evaluate_simplified_kane_statistics,
    simplified_kane_dos_shape,
    simplified_kane_normalized_integrals,
)
from mct_research.transport_noise.statistics_interface import (
    CarrierStatisticsClosure,
    evaluate_parabolic_carrier_statistics,
    thermodynamic_identity_relative_error,
)
from mct_research.transport_noise.statistics_prototype import BOLTZMANN_EV_PER_K


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_PATH = (
    ROOT / "configs" / "transport_noise" / "project_kane_reference_points.json"
)


def test_rejects_invalid_domain_and_quadrature_controls():
    with pytest.raises(ValueError):
        KaneQuadratureOptions(quadrature_order=16)
    with pytest.raises(ValueError):
        ProjectDefinedKaneClosure(
            parabolic_density_scale_cm3=1.0e16,
            nonparabolicity_ev_inverse=-1.0,
        )
    with pytest.raises(ValueError):
        evaluate_simplified_kane_statistics(
            eta=0.0,
            temperature_k=0.0,
            parabolic_density_scale_cm3=1.0e16,
            nonparabolicity_ev_inverse=1.0,
        )
    with pytest.raises(ValueError):
        simplified_kane_dos_shape([-0.1, 0.0], 0.2)


def test_dos_shape_is_positive_and_recovers_parabolic_limit():
    energy = np.linspace(0.0, 20.0, 101)
    parabolic = simplified_kane_dos_shape(energy, 0.0)
    nonparabolic = simplified_kane_dos_shape(energy, 0.4)
    np.testing.assert_allclose(parabolic, 1.0, rtol=0.0, atol=0.0)
    assert np.all(nonparabolic >= 1.0)
    assert np.all(np.diff(nonparabolic) >= 0.0)


@pytest.mark.parametrize("eta", [-6.0, -1.0, 0.0, 2.5])
def test_zero_nonparabolicity_reduces_to_merged_parabolic_closure(eta):
    temperature = 90.0
    scale = 2.5e16
    kane = evaluate_simplified_kane_statistics(
        eta=eta,
        temperature_k=temperature,
        parabolic_density_scale_cm3=scale,
        nonparabolicity_ev_inverse=0.0,
    ).carrier
    parabolic = evaluate_parabolic_carrier_statistics(
        eta=eta,
        temperature_k=temperature,
        density_scale_cm3=scale,
    )
    assert kane.density_cm3 == pytest.approx(parabolic.density_cm3, rel=5.0e-9)
    assert kane.compressibility_cm3_per_ev == pytest.approx(
        parabolic.compressibility_cm3_per_ev,
        rel=5.0e-9,
    )
    assert kane.generalized_einstein_factor == pytest.approx(
        parabolic.generalized_einstein_factor,
        rel=5.0e-9,
    )


def test_analytical_compressibility_matches_centered_density_derivative():
    eta = 0.4
    temperature = 120.0
    alpha = 18.0
    scale = 4.0e15
    step = 2.0e-5
    center = evaluate_simplified_kane_statistics(
        eta=eta,
        temperature_k=temperature,
        parabolic_density_scale_cm3=scale,
        nonparabolicity_ev_inverse=alpha,
    ).carrier
    plus = evaluate_simplified_kane_statistics(
        eta=eta + step,
        temperature_k=temperature,
        parabolic_density_scale_cm3=scale,
        nonparabolicity_ev_inverse=alpha,
    ).carrier
    minus = evaluate_simplified_kane_statistics(
        eta=eta - step,
        temperature_k=temperature,
        parabolic_density_scale_cm3=scale,
        nonparabolicity_ev_inverse=alpha,
    ).carrier
    derivative_eta = (plus.density_cm3 - minus.density_cm3) / (2.0 * step)
    expected = (
        BOLTZMANN_EV_PER_K
        * temperature
        * center.compressibility_cm3_per_ev
    )
    assert derivative_eta == pytest.approx(expected, rel=1.0e-7)
    assert thermodynamic_identity_relative_error(center) < 1.0e-14


def test_positive_nonparabolicity_increases_density_and_compressibility():
    parabolic = evaluate_simplified_kane_statistics(
        eta=0.3,
        temperature_k=100.0,
        parabolic_density_scale_cm3=1.0e16,
        nonparabolicity_ev_inverse=0.0,
    )
    kane = evaluate_simplified_kane_statistics(
        eta=0.3,
        temperature_k=100.0,
        parabolic_density_scale_cm3=1.0e16,
        nonparabolicity_ev_inverse=25.0,
    )
    assert kane.carrier.density_cm3 > parabolic.carrier.density_cm3
    assert (
        kane.carrier.compressibility_cm3_per_ev
        > parabolic.carrier.compressibility_cm3_per_ev
    )
    assert kane.density_enhancement_over_parabolic > 1.0
    assert kane.compressibility_enhancement_over_parabolic > 1.0


def test_density_is_monotone_in_reduced_chemical_potential():
    closure = ProjectDefinedKaneClosure(
        parabolic_density_scale_cm3=1.0e16,
        nonparabolicity_ev_inverse=20.0,
    )
    values = [
        closure.evaluate(eta=eta, temperature_k=77.0).density_cm3
        for eta in (-6.0, -2.0, 0.0, 2.0)
    ]
    assert np.all(np.diff(values) > 0.0)


def test_boltzmann_limit_recovers_unit_generalized_einstein_factor():
    state = evaluate_simplified_kane_statistics(
        eta=-12.0,
        temperature_k=150.0,
        parabolic_density_scale_cm3=1.0e16,
        nonparabolicity_ev_inverse=40.0,
    ).carrier
    assert state.generalized_einstein_factor == pytest.approx(1.0, rel=4.0e-6)


def test_density_scale_is_linear_and_einstein_factor_is_scale_independent():
    first = evaluate_simplified_kane_statistics(
        eta=0.5,
        temperature_k=77.0,
        parabolic_density_scale_cm3=1.0e15,
        nonparabolicity_ev_inverse=30.0,
    ).carrier
    second = evaluate_simplified_kane_statistics(
        eta=0.5,
        temperature_k=77.0,
        parabolic_density_scale_cm3=5.0e15,
        nonparabolicity_ev_inverse=30.0,
    ).carrier
    assert second.density_cm3 == pytest.approx(5.0 * first.density_cm3)
    assert second.compressibility_cm3_per_ev == pytest.approx(
        5.0 * first.compressibility_cm3_per_ev
    )
    assert second.generalized_einstein_factor == pytest.approx(
        first.generalized_einstein_factor
    )


def test_quadrature_refinement_is_stable():
    coarse = simplified_kane_normalized_integrals(
        eta=2.0,
        reduced_nonparabolicity=0.4,
        quadrature=KaneQuadratureOptions(quadrature_order=160),
    )
    fine = simplified_kane_normalized_integrals(
        eta=2.0,
        reduced_nonparabolicity=0.4,
        quadrature=KaneQuadratureOptions(quadrature_order=360),
    )
    np.testing.assert_allclose(coarse, fine, rtol=2.0e-11, atol=0.0)


def test_frozen_dimensionless_reference_points():
    payload = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    assert payload["model_identity"] == MODEL_IDENTITY
    assert payload["scientific_boundary"]["material_validation"] is False
    options = KaneQuadratureOptions(quadrature_order=480, tail_margin=48.0)
    for point in payload["reference_points"]:
        density, compressibility = simplified_kane_normalized_integrals(
            eta=point["eta"],
            reduced_nonparabolicity=point["beta"],
            quadrature=options,
        )
        assert density == pytest.approx(point["normalized_density"], rel=2.0e-12)
        assert compressibility == pytest.approx(
            point["normalized_compressibility"],
            rel=2.0e-12,
        )
        assert density / compressibility == pytest.approx(
            point["generalized_einstein_factor"],
            rel=2.0e-12,
        )


def test_reduced_nonparabolicity_is_alpha_kbt():
    alpha = 24.0
    temperature = 80.0
    result = evaluate_simplified_kane_statistics(
        eta=0.0,
        temperature_k=temperature,
        parabolic_density_scale_cm3=1.0e16,
        nonparabolicity_ev_inverse=alpha,
    )
    assert result.reduced_nonparabolicity == pytest.approx(
        alpha * BOLTZMANN_EV_PER_K * temperature
    )


def test_closure_satisfies_merged_runtime_protocol_and_fixed_identity():
    closure = ProjectDefinedKaneClosure(
        parabolic_density_scale_cm3=1.0e16,
        nonparabolicity_ev_inverse=10.0,
    )
    assert isinstance(closure, CarrierStatisticsClosure)
    detailed = closure.evaluate_detailed(eta=0.0, temperature_k=77.0)
    assert detailed.model_identity == MODEL_IDENTITY
    assert "madarasz" not in detailed.model_identity
    assert "lowney" not in detailed.model_identity

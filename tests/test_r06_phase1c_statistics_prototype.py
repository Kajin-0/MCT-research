from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from mct_research.transport_noise.statistics_prototype import (
    BOLTZMANN_EV_PER_K,
    hansen_schmit_intrinsic_density_cm3,
    normalized_fermi_dirac,
    parabolic_fermi_statistics,
)


@pytest.mark.parametrize(
    ("eta", "fermi_half", "fermi_minus_half", "theta"),
    [
        (-8.0, 0.000335422847973596, 0.000335383075306765, 1.000118588771346),
        (-5.0, 0.006721954314505913, 0.006706019989268209, 1.002376122538138),
        (-4.0, 0.018198203508367109, 0.018081922991399386, 1.006430760545935),
        (-3.0, 0.048933705696495779, 0.048102635332204083, 1.017277023567466),
        (-2.0, 0.129298513320075591, 0.123665621801209943, 1.045549372871956),
        (-1.0, 0.327795159260711548, 0.294027617611451220, 1.114844795613326),
        (0.0, 0.765147024625407945, 0.604898643421630370, 1.264917739437019),
        (2.0, 2.82372127740158413, 1.46429458908762912, 1.928383331089808),
        (5.0, 8.84420889524295389, 2.47298762248294402, 3.576325580781976),
    ],
)
def test_normalized_fermi_integral_reference_values(
    eta: float,
    fermi_half: float,
    fermi_minus_half: float,
    theta: float,
) -> None:
    assert normalized_fermi_dirac(0.5, eta) == pytest.approx(fermi_half, rel=3e-13)
    assert normalized_fermi_dirac(-0.5, eta) == pytest.approx(
        fermi_minus_half,
        rel=3e-13,
    )
    assert parabolic_fermi_statistics(eta).generalized_einstein_factor == pytest.approx(
        theta,
        rel=5e-13,
    )


def test_vectorized_integral_matches_scalar_calls() -> None:
    eta = np.array([-5.0, -3.0, 0.0, 2.0])
    vector = normalized_fermi_dirac(0.5, eta)
    scalar = np.array([normalized_fermi_dirac(0.5, value) for value in eta])
    np.testing.assert_allclose(vector, scalar, rtol=2e-14, atol=0.0)


def test_derivative_identity_for_half_order() -> None:
    step = 2.0e-5
    for eta in (-5.0, -3.0, -1.0, 0.0, 2.0):
        numerical = (
            normalized_fermi_dirac(0.5, eta + step)
            - normalized_fermi_dirac(0.5, eta - step)
        ) / (2.0 * step)
        expected = normalized_fermi_dirac(-0.5, eta)
        assert numerical == pytest.approx(expected, rel=2e-9)


def test_boltzmann_reduction_errors_match_phase1c_table() -> None:
    expected_corrections = {
        -1.0: 0.1089603751,
        -2.0: 0.0446060316,
        -3.0: 0.0171402474,
        -4.0: 0.0064117545,
        -5.0: 0.0023735248,
    }
    previous = math.inf
    for eta, expected in expected_corrections.items():
        result = parabolic_fermi_statistics(eta)
        assert result.fermi_correction_relative_to_boltzmann == pytest.approx(
            expected,
            abs=5e-10,
        )
        assert result.fermi_correction_relative_to_boltzmann < previous
        assert result.generalized_einstein_factor > 1.0
        previous = result.fermi_correction_relative_to_boltzmann


def test_hansen_schmit_fit_matches_direct_expression() -> None:
    x = 0.21
    temperature = 77.0
    gap = 0.10
    expected = (
        1.0e14
        * (
            5.585
            - 3.820 * x
            + 1.753e-3 * temperature
            - 1.364e-3 * x * temperature
        )
        * gap**0.75
        * temperature**1.5
        * math.exp(-gap / (2.0 * BOLTZMANN_EV_PER_K * temperature))
    )
    assert hansen_schmit_intrinsic_density_cm3(
        composition=x,
        temperature_k=temperature,
        gap_ev=gap,
    ) == pytest.approx(expected, rel=2e-15)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"composition": -0.1, "temperature_k": 77.0, "gap_ev": 0.1},
        {"composition": 0.2, "temperature_k": 0.0, "gap_ev": 0.1},
        {"composition": 0.2, "temperature_k": 77.0, "gap_ev": 0.0},
        {"composition": 0.2, "temperature_k": 50.0, "gap_ev": 0.1},
        {"composition": 0.7, "temperature_k": 77.0, "gap_ev": 0.1},
    ],
)
def test_hansen_schmit_fit_rejects_invalid_or_out_of_domain_inputs(
    kwargs: dict[str, float],
) -> None:
    with pytest.raises(ValueError):
        hansen_schmit_intrinsic_density_cm3(**kwargs)


@pytest.mark.parametrize("order", [-1.5, 0.0, 1.5])
def test_unsupported_fermi_order_is_rejected(order: float) -> None:
    with pytest.raises(ValueError):
        normalized_fermi_dirac(order, 0.0)


def test_machine_readable_reference_matches_integrals() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "validation"
        / "r06_phase1c_parabolic_fermi_reference.json"
    )
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["schema_version"] == 1
    for point in record["points"]:
        eta = float(point["eta"])
        assert normalized_fermi_dirac(0.5, eta) == pytest.approx(
            point["F_half"],
            rel=3e-13,
        )
        assert normalized_fermi_dirac(-0.5, eta) == pytest.approx(
            point["F_minus_half"],
            rel=3e-13,
        )

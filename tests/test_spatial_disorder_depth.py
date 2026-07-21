from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder import GaussianCovariance
from mct_research.spatial_disorder_depth import (
    ExponentialCovariance1D,
    ExponentialDepthKernel,
    finite_slab_depth_effective_variance,
    finite_slab_exponential_depth_ratio,
    semi_infinite_exponential_depth_ratio,
    semi_infinite_gaussian_depth_ratio,
)


def _integrated_kernel_weight(
    kernel: ExponentialDepthKernel,
    order: int = 96,
) -> float:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    depth = 0.5 * kernel.thickness * (nodes + 1.0)
    integration_weights = 0.5 * kernel.thickness * weights
    return float(integration_weights @ np.asarray(kernel.weight(depth)))


@pytest.mark.parametrize("side", ["front", "back"])
def test_depth_kernel_is_normalized(side: str) -> None:
    kernel = ExponentialDepthKernel(attenuation_coefficient=2.3, thickness=4.7, side=side)  # type: ignore[arg-type]
    assert _integrated_kernel_weight(kernel) == pytest.approx(1.0, rel=2.0e-14)


def test_front_and_back_weights_are_reflections() -> None:
    front = ExponentialDepthKernel(1.7, 3.2, "front")
    back = ExponentialDepthKernel(1.7, 3.2, "back")
    depth = np.linspace(0.0, 3.2, 41)
    assert np.asarray(front.weight(depth)) == pytest.approx(
        np.asarray(back.weight(3.2 - depth)),
        rel=1.0e-14,
    )


def test_exponential_covariance_convention() -> None:
    covariance = ExponentialCovariance1D(variance=0.04, correlation_length=2.0)
    assert covariance.dimension == 1
    assert covariance.covariance(0.0) == pytest.approx(0.04)
    assert covariance.covariance(2.0) == pytest.approx(0.04 / math.e)
    assert covariance.covariance(-2.0) == pytest.approx(0.04 / math.e)


@pytest.mark.parametrize(
    ("product", "expected"),
    [
        (0.1, 0.09090909090909091),
        (1.0, 0.5),
        (2.0, 2.0 / 3.0),
        (10.0, 10.0 / 11.0),
    ],
)
def test_exponential_semi_infinite_reference_values(
    product: float,
    expected: float,
) -> None:
    assert semi_infinite_exponential_depth_ratio(product, 1.0) == pytest.approx(
        expected,
        rel=1.0e-15,
    )


@pytest.mark.parametrize(
    ("product", "expected"),
    [
        (0.1, 0.11592623996187362),
        (1.0, 0.6556795424187986),
        (2.0, 0.8427384585761093),
        (20.0, 0.9975185196367710),
        (100.0, 0.9999000299850106),
    ],
)
def test_gaussian_semi_infinite_reference_values(
    product: float,
    expected: float,
) -> None:
    assert semi_infinite_gaussian_depth_ratio(product, 1.0) == pytest.approx(
        expected,
        rel=2.0e-14,
    )


def test_small_product_asymptotes() -> None:
    product = 1.0e-8
    exponential = semi_infinite_exponential_depth_ratio(product, 1.0)
    gaussian = semi_infinite_gaussian_depth_ratio(product, 1.0)
    assert exponential / product == pytest.approx(1.0, rel=1.0e-8)
    assert gaussian / (math.sqrt(math.pi / 2.0) * product) == pytest.approx(
        1.0,
        rel=1.0e-8,
    )


def test_large_product_asymptotes() -> None:
    product = 1.0e6
    exponential = semi_infinite_exponential_depth_ratio(product, 1.0)
    gaussian = semi_infinite_gaussian_depth_ratio(product, 1.0)
    assert (1.0 - exponential) * product == pytest.approx(1.0, rel=2.0e-6)
    assert (1.0 - gaussian) * product**2 == pytest.approx(1.0, rel=2.0e-4)


def test_exact_finite_exponential_ratio_matches_quadrature() -> None:
    attenuation = 2.0
    correlation = 1.0
    thickness = 3.0
    exact_ratio = finite_slab_exponential_depth_ratio(
        attenuation,
        correlation,
        thickness,
    )
    covariance = ExponentialCovariance1D(1.0, correlation)
    kernel = ExponentialDepthKernel(attenuation, thickness)
    numerical_ratio = finite_slab_depth_effective_variance(
        covariance,
        kernel,
        quadrature_order=1024,
    )
    assert exact_ratio == pytest.approx(0.6696656179288729, rel=2.0e-15)
    assert numerical_ratio == pytest.approx(exact_ratio, rel=2.0e-6)


def test_removable_case_attenuation_equals_inverse_correlation() -> None:
    attenuation = 0.5
    correlation = 2.0
    thickness = 5.0
    exact_ratio = finite_slab_exponential_depth_ratio(
        attenuation,
        correlation,
        thickness,
    )
    numerical_ratio = finite_slab_depth_effective_variance(
        ExponentialCovariance1D(1.0, correlation),
        ExponentialDepthKernel(attenuation, thickness),
        quadrature_order=1024,
    )
    assert exact_ratio == pytest.approx(numerical_ratio, rel=2.0e-6)


def test_thin_slab_limit_approaches_point_variance() -> None:
    ratio = finite_slab_exponential_depth_ratio(
        attenuation_coefficient=3.0,
        correlation_length=2.0,
        thickness=1.0e-8,
    )
    assert ratio == pytest.approx(1.0 - 1.0e-8 / 6.0, rel=1.0e-15)


def test_thick_slab_exponential_limit_matches_semi_infinite() -> None:
    attenuation = 2.0
    correlation = 1.0
    finite = finite_slab_exponential_depth_ratio(
        attenuation,
        correlation,
        thickness=40.0,
    )
    semi_infinite = semi_infinite_exponential_depth_ratio(
        attenuation,
        correlation,
    )
    assert finite == pytest.approx(semi_infinite, rel=1.0e-14)


def test_thick_slab_gaussian_quadrature_matches_semi_infinite() -> None:
    attenuation = 2.0
    correlation = 1.0
    covariance = GaussianCovariance.isotropic(1.0, correlation, 1)
    kernel = ExponentialDepthKernel(attenuation, thickness=10.0)
    finite = finite_slab_depth_effective_variance(
        covariance,
        kernel,
        quadrature_order=128,
    )
    semi_infinite = semi_infinite_gaussian_depth_ratio(
        attenuation,
        correlation,
    )
    assert finite == pytest.approx(semi_infinite, rel=5.0e-9)


@pytest.mark.parametrize(
    "covariance",
    [
        ExponentialCovariance1D(0.03, 0.8),
        GaussianCovariance.isotropic(0.03, 0.8, 1),
    ],
)
def test_front_back_variance_symmetry(
    covariance: ExponentialCovariance1D | GaussianCovariance,
) -> None:
    front = finite_slab_depth_effective_variance(
        covariance,
        ExponentialDepthKernel(1.4, 3.7, "front"),
        quadrature_order=160,
    )
    back = finite_slab_depth_effective_variance(
        covariance,
        ExponentialDepthKernel(1.4, 3.7, "back"),
        quadrature_order=160,
    )
    assert front == pytest.approx(back, rel=2.0e-14)


@pytest.mark.parametrize(
    ("attenuation", "correlation", "thickness"),
    [
        (0.05, 0.2, 0.4),
        (0.5, 4.0, 0.1),
        (2.0, 1.0, 3.0),
        (100.0, 0.01, 1.0),
    ],
)
def test_exact_finite_exponential_ratio_stays_physical(
    attenuation: float,
    correlation: float,
    thickness: float,
) -> None:
    ratio = finite_slab_exponential_depth_ratio(
        attenuation,
        correlation,
        thickness,
    )
    assert 0.0 < ratio <= 1.0


def test_depth_result_is_invariant_under_consistent_length_rescaling() -> None:
    reference = finite_slab_exponential_depth_ratio(2.0, 0.7, 3.0)
    scale = 1.0e-6
    scaled = finite_slab_exponential_depth_ratio(
        2.0 / scale,
        0.7 * scale,
        3.0 * scale,
    )
    assert scaled == pytest.approx(reference, rel=2.0e-14)


def test_quadrature_converges_for_gaussian_covariance() -> None:
    covariance = GaussianCovariance.isotropic(0.02, 0.9, 1)
    kernel = ExponentialDepthKernel(1.8, 2.5)
    order_32 = finite_slab_depth_effective_variance(
        covariance,
        kernel,
        quadrature_order=32,
    )
    order_64 = finite_slab_depth_effective_variance(
        covariance,
        kernel,
        quadrature_order=64,
    )
    order_128 = finite_slab_depth_effective_variance(
        covariance,
        kernel,
        quadrature_order=128,
    )
    assert order_64 == pytest.approx(order_128, rel=1.0e-13)
    assert order_32 == pytest.approx(order_128, rel=1.0e-12)


def test_invalid_scalar_and_side_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="variance"):
        ExponentialCovariance1D(0.0, 1.0)
    with pytest.raises(ValueError, match="correlation_length"):
        ExponentialCovariance1D(1.0, -1.0)
    with pytest.raises(ValueError, match="attenuation_coefficient"):
        ExponentialDepthKernel(0.0, 1.0)
    with pytest.raises(ValueError, match="thickness"):
        ExponentialDepthKernel(1.0, math.inf)
    with pytest.raises(ValueError, match="side"):
        ExponentialDepthKernel(1.0, 1.0, "left")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="correlation_length"):
        semi_infinite_gaussian_depth_ratio(1.0, 0.0)
    with pytest.raises(ValueError, match="thickness"):
        finite_slab_exponential_depth_ratio(1.0, 1.0, -1.0)


def test_depth_and_displacement_validation() -> None:
    kernel = ExponentialDepthKernel(1.0, 2.0)
    with pytest.raises(ValueError, match="finite slab"):
        kernel.weight(-0.1)
    with pytest.raises(ValueError, match="finite"):
        kernel.weight([0.0, math.nan])
    covariance = ExponentialCovariance1D(1.0, 1.0)
    with pytest.raises(ValueError, match="finite"):
        covariance.covariance(math.inf)


def test_invalid_covariance_and_quadrature_inputs_are_rejected() -> None:
    kernel = ExponentialDepthKernel(1.0, 2.0)
    with pytest.raises(ValueError, match="one-dimensional"):
        finite_slab_depth_effective_variance(
            GaussianCovariance.isotropic(1.0, 1.0, 2),
            kernel,
        )
    with pytest.raises(TypeError, match="covariance"):
        finite_slab_depth_effective_variance(object(), kernel)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="kernel"):
        finite_slab_depth_effective_variance(
            ExponentialCovariance1D(1.0, 1.0),
            object(),  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="quadrature_order"):
        finite_slab_depth_effective_variance(
            ExponentialCovariance1D(1.0, 1.0),
            kernel,
            quadrature_order=1,
        )
    with pytest.raises(ValueError, match="quadrature_order"):
        finite_slab_depth_effective_variance(
            ExponentialCovariance1D(1.0, 1.0),
            kernel,
            quadrature_order=True,
        )

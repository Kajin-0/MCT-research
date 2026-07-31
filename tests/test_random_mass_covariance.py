from __future__ import annotations

import numpy as np

from mct_research.random_mass_covariance import (
    SUPPORTED_COVARIANCE_FAMILIES,
    covariance_power_spectrum,
    generate_random_mass_field,
    periodic_target_correlation,
)


def test_supported_covariance_spectra_are_nonnegative_and_normalized() -> None:
    for family in SUPPORTED_COVARIANCE_FAMILIES:
        power = covariance_power_spectrum(64, 16.0, 1.0, family)
        assert np.all(power >= 0.0)
        assert abs(np.mean(power) - 1.0) < 1.0e-14
        correlation = periodic_target_correlation(64, 16.0, 1.0, family)
        assert abs(correlation[0] - 1.0) < 1.0e-14
        assert np.all(np.isfinite(correlation))


def test_random_mass_field_is_deterministic_and_preserves_declared_mean() -> None:
    first = generate_random_mass_field(64, 16.0, 0.3, 0.5, 1.0, seed=123)
    second = generate_random_mass_field(64, 16.0, 0.3, 0.5, 1.0, seed=123)
    assert np.array_equal(first.mass, second.mass)
    assert abs(np.mean(first.mass) - 0.3) < 1.0e-14
    assert abs(first.realized_fluctuation_mean) < 1.0e-14


def test_gaussian_field_ensemble_recovers_target_variance_and_covariance() -> None:
    fields = np.asarray(
        [
            generate_random_mass_field(
                64,
                16.0,
                0.0,
                1.0,
                1.0,
                seed=seed,
            ).fluctuation
            for seed in np.random.SeedSequence(9227).spawn(256)
        ]
    )
    empirical_power = np.mean(np.abs(np.fft.fft(fields, axis=1)) ** 2, axis=0) / 64
    empirical_correlation = np.fft.ifft(empirical_power).real
    empirical_correlation /= empirical_correlation[0]
    target = periodic_target_correlation(64, 16.0, 1.0)
    assert abs(np.mean(fields**2) - 1.0) < 0.08
    assert np.max(np.abs(empirical_correlation[:8] - target[:8])) < 0.08
# Exact spatial-disorder theorem extensions

This layer complements the Gaussian covariance core, depth-kernel benchmarks, and multiscale Fisher diagnostics.

```python
from mct_research.spatial_disorder_theorems import (
    cutoff_standard_deviation_um,
    probe_averaged_gap_moments,
    recover_isotropic_gaussian_two_scales,
    single_scale_point_variance_family,
    top_hat_exponential_effective_variance_1d,
    top_hat_gaussian_effective_variance_1d,
    two_scale_log_parameter_condition_number,
)
```

## One-scale non-identifiability

```python
point_variance = single_scale_point_variance_family(
    effective_variance=measured_variance,
    correlation_length=declared_xi,
    probe_sigma=probe_sigma,
    dimension=2,
)
```

For every positive declared correlation length, this returns a point variance that produces the same one-scale observation.

## Arbitrary-dimensional exact inverse

```python
result = recover_isotropic_gaussian_two_scales(
    effective_variance_1=v1,
    effective_variance_2=v2,
    probe_sigma_1=s1,
    probe_sigma_2=s2,
    dimension=3,
)
```

The result includes point variance, correlation length, exact reconstruction residual, and the closed two-scale log-parameter condition number.

## Exact top-hat formulas

```python
variance_gaussian = top_hat_gaussian_effective_variance_1d(
    point_variance,
    correlation_length,
    window_length,
)

variance_exponential = top_hat_exponential_effective_variance_1d(
    point_variance,
    correlation_length,
    window_length,
)
```

The formulas are independently verified against direct covariance quadrature.

## HgCdTe propagation

```python
moments = probe_averaged_gap_moments(
    gap_model,
    mean_composition=xbar,
    temperature_k=77.0,
    point_composition_variance=sigma_x**2,
    correlation_length=xi,
    probe_sigma=probe_sigma,
    dimension=2,
)
```

The returned variance is exact for a quadratic gap law with Gaussian probe-averaged composition. Small gap spreads can be converted to first-order cutoff spread with `cutoff_standard_deviation_um`.

## Boundaries

These functions do not validate the covariance family, infer a specimen correlation length from historical spectra, or equate point composition variance with Urbach energy, PL linewidth, or detector-cutoff spread.

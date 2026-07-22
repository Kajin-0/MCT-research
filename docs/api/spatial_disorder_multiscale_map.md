# Cross-scale correlated-raster API

This module computes the exact covariance of ordinary map-variance estimators measured at several Gaussian probe scales on the same spatial realization.

```python
from mct_research.spatial_disorder_multiscale_map import (
    gaussian_multiscale_map_covariance_blocks,
    gaussian_multiscale_map_fisher_comparison,
    gaussian_multiscale_map_variance_statistics,
)
```

## Common-raster covariance blocks

```python
blocks = gaussian_multiscale_map_covariance_blocks(
    covariance,
    positions,
    probe_sigmas,
)
```

The returned shape is

```text
(scale_count, scale_count, pixel_count, pixel_count).
```

Each block uses the merged Gaussian filtered-map cross-covariance theorem. Probe kernels are isotropic Gaussian kernels; the material covariance may be anisotropic.

## Cross-scale map-variance statistics

```python
statistics = gaussian_multiscale_map_variance_statistics(
    blocks,
    probe_sigmas,
)
```

For ordinary map variances

```text
q_i = y_i.T @ P @ y_i/(n-1),
P   = I - 11.T/n,
```

the exact Gaussian quadratic-form moments are

```text
E[q_i] = tr(P C_ii)/(n-1)
Cov(q_i,q_j) = 2 tr(P C_ij P C_ji)/(n-1)^2.
```

The result reports:

```text
marginal_filtered_variances
expected_naive_variances
deterministic_bias_factors
raw_variance_estimator_covariance
bias_corrected_estimator_covariance
delta_log_variance_covariance
delta_log_variance_standard_deviations
delta_log_variance_correlation
moment_matched_effective_degrees_of_freedom
```

`delta_log_variance_covariance` is the first-order delta-method covariance

```text
Cov(q_i,q_j)/(E[q_i] E[q_j]).
```

It is not an exact claim that correlated quadratic forms are jointly log-normal.

## Fisher comparison

```python
comparison = gaussian_multiscale_map_fisher_comparison(
    point_variance,
    correlation_length,
    probe_sigmas,
    statistics.delta_log_variance_covariance,
    nominal_pixel_count=statistics.nominal_pixel_count,
)
```

The full calculation uses the same-raster cross-scale covariance. The nominal comparison assumes every pixel is independent at every scale and uses

```text
2 I/(n-1).
```

The result reports parameter covariance, standard-deviation inflation, determinant inflation, and parameter correlation for `(log A, log xi)`.

## Interpretation boundary

- deterministic map-variance bias correction does not increase independent information;
- nominal pixel count is not an independent-repeat count;
- multiple resolutions of one raster are not independent scale observations;
- full block covariance or independent specimen regions are required for defensible precision;
- the module does not infer a specimen covariance or authorize a manuscript.

# Spatial-disorder covariance-family diagnostics

This additive API tests the Gaussian covariance/Gaussian probe family before a recovered correlation length is interpreted physically.

## Half-integer Matérn filtering

```python
from mct_research.spatial_disorder_covariance_families import (
    matern_gaussian_probe_variance_2d,
)

variances = matern_gaussian_probe_variance_2d(
    point_variance=2.5e-5,
    correlation_length=5.0,
    probe_sigmas=[0.5, 5.0, 10.0],
    smoothness=1.5,
)
```

Supported smoothness values are:

```text
0.5   exponential covariance
1.5   Matérn 3/2
2.5   Matérn 5/2
```

The standard parameterization is

```text
z = sqrt(2 nu) r / ell.
```

The implementation uses exact half-integer closed forms at small arguments and an equivalent Gauss--Laguerre representation where direct evaluation would suffer cancellation.

## Exact three-scale Gaussian test

For the two-dimensional Gaussian benchmark,

```text
V(s)=A/(1+2s^2/xi^2),
```

`1/V` must be affine in `s^2`.

```python
from mct_research.spatial_disorder_covariance_families import (
    gaussian_three_scale_falsification,
)

result = gaussian_three_scale_falsification(
    probe_sigmas=[0.5, 5.0, 10.0],
    variances=variances,
    variance_standard_deviations=0.03 * variances,
)
```

Returned diagnostics include:

```text
reciprocal_second_divided_difference
reciprocal_middle_residual
endpoint_predicted_middle_variance
middle_relative_prediction_error
residual_standard_deviation
standardized_reciprocal_residual
endpoint_fitted_point_variance
endpoint_fitted_correlation_length
```

The endpoint scales determine the two Gaussian parameters. The middle scale is a family test.

## Multi-scale weighted reciprocal fit

```python
from mct_research.spatial_disorder_covariance_families import (
    gaussian_reciprocal_linearity_fit,
)

fit = gaussian_reciprocal_linearity_fit(
    probe_sigmas=[0.25, 0.5, 1.5, 5.0, 10.0],
    variances=measured_variances,
    variance_standard_deviations=measured_standard_deviations,
)
```

The fit reports:

```text
intercept and slope in reciprocal space
fitted point variance and correlation length
fitted variances
reciprocal and relative residuals
maximum absolute relative residual
chi-square and reduced chi-square
coefficient covariance
```

With no uncertainty array, the fit remains deterministic but chi-square is not assigned a probabilistic interpretation.

## Interpretation

- Two admissible scales can always fit a two-parameter Gaussian family exactly.
- Three scales provide the first exact reciprocal-curvature check.
- A nonzero residual falsifies the declared Gaussian covariance/probe family.
- A small residual does not prove Gaussian covariance; the alternative may be unresolved at the available scales and uncertainty.
- Very large probes are weak family discriminators because the supported standard Matérn families share the same leading inverse-area attenuation.

## Scientific boundary

The API does not identify a specimen covariance family. It assumes the reported input values are apparent variances evaluated under a consistent operation order and calibrated probe definition. Connecting those values to spectra, photoluminescence linewidths, or detector cutoffs requires the corresponding observation operator.

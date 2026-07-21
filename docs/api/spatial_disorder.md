# Gaussian spatial-disorder API

The first Stage 1 implementation is intentionally narrow. It provides exact analytical filtering for a stationary Gaussian covariance field observed through a normalized Gaussian spatial kernel.

```python
from mct_research.spatial_disorder import (
    GaussianCovariance,
    GaussianKernel,
    gaussian_gaussian_effective_variance,
    isotropic_gaussian_effective_variance,
    two_scale_gaussian_inversion,
)
```

## Covariance convention

```python
covariance = GaussianCovariance.isotropic(
    variance=0.001**2,
    correlation_length=2.0e-6,
    dimension=2,
)
```

The local covariance is

```text
C(h) = variance * exp[-0.5 h^T Lambda^-1 h].
```

For an isotropic model, `Lambda = xi^2 I`. Therefore `xi` is the principal-axis displacement at which the covariance falls to `exp(-1/2)` of its point value. It is not the `1/e` radius.

## Gaussian measurement kernel

```python
kernel = GaussianKernel.isotropic(
    probe_sigma=5.0e-6,
    dimension=2,
)
```

`probe_sigma` is the specimen-plane Gaussian standard deviation. A zero covariance matrix represents the point-probe limit.

## Exact effective variance

```python
variance_eff = gaussian_gaussian_effective_variance(covariance, kernel)
```

The implementation evaluates

```text
Var[x_w]
  = sigma_x^2 sqrt(det(Lambda)/det(Lambda + 2 Sigma_w))
```

through a stable log-determinant calculation.

The isotropic convenience function is

```python
variance_eff = isotropic_gaussian_effective_variance(
    point_variance=0.001**2,
    correlation_length=2.0e-6,
    probe_sigma=5.0e-6,
    dimension=2,
)
```

which returns

```text
sigma_x^2 (1 + 2 s^2/xi^2)^(-d/2).
```

## Two-scale inversion

For the isotropic two-dimensional benchmark,

```python
result = two_scale_gaussian_inversion(
    variance_at_s1=v1,
    variance_at_s2=v2,
    probe_sigma_1=s1,
    probe_sigma_2=s2,
)

sigma_x_squared = result.point_variance
xi = result.correlation_length
```

The inversion rejects:

- equal probe sizes;
- equal effective variances;
- variance increasing with probe size;
- data implying a non-positive point variance or correlation length.

Two scales identify the two parameters only under the assumed isotropic Gaussian covariance family. They do not test that family. Three or more scales are required for model checking.

## Boundaries

This module does not:

- infer composition from an optical edge;
- model exponential or Matérn covariance;
- model depth sensitivity;
- generate random fields;
- fit noisy multiscale data;
- couple disorder to absorption, detector cutoff, PL, or Kane physics.

Those capabilities require separate issues and validation gates.
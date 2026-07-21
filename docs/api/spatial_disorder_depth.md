# Depth-kernel spatial-disorder API

This module implements the second Stage 1 benchmark layer: one-dimensional stationary covariance filtered by a normalized exponential depth sensitivity in a finite slab.

```python
from mct_research.spatial_disorder import GaussianCovariance
from mct_research.spatial_disorder_depth import (
    ExponentialCovariance1D,
    ExponentialDepthKernel,
    finite_slab_depth_effective_variance,
    finite_slab_exponential_depth_ratio,
    semi_infinite_exponential_depth_ratio,
    semi_infinite_gaussian_depth_ratio,
)
```

## Exponential depth kernel

```python
kernel = ExponentialDepthKernel(
    attenuation_coefficient=1.0 / penetration_depth,
    thickness=absorber_thickness,
    side="front",
)
```

For front incidence,

```text
w(z) = a exp(-a z)/(1-exp(-a d)),  0 <= z <= d.
```

The back-incidence kernel is reflected about the slab midplane. The kernel is analytically normalized.

## Exact semi-infinite ratios

For exponential covariance

```text
C(dz) = sigma_x^2 exp(-|dz|/xi),
```

use

```python
ratio = semi_infinite_exponential_depth_ratio(a, xi)
```

which returns

```text
a xi/(1+a xi).
```

For Gaussian covariance

```text
C(dz) = sigma_x^2 exp[-dz^2/(2 xi^2)],
```

use

```python
ratio = semi_infinite_gaussian_depth_ratio(a, xi)
```

which returns

```text
sqrt(pi/2) a xi exp[(a xi)^2/2] erfc(a xi/sqrt(2)).
```

The implementation switches to an asymptotic expansion for large `a xi` so the finite ratio can approach one without intermediate overflow.

## Exact finite-slab exponential result

```python
ratio = finite_slab_exponential_depth_ratio(
    attenuation_coefficient=a,
    correlation_length=xi,
    thickness=d,
)
```

This is the exact normalized variance ratio for exponential covariance and the finite exponential depth kernel. It handles the removable case `a = 1/xi` and uses a thin-slab series when direct subtraction would lose precision.

## Reference quadrature

```python
covariance = ExponentialCovariance1D(
    variance=sigma_x**2,
    correlation_length=xi,
)

variance_eff = finite_slab_depth_effective_variance(
    covariance,
    kernel,
    quadrature_order=128,
)
```

A one-dimensional Gaussian covariance can be supplied through

```python
covariance = GaussianCovariance.isotropic(
    variance=sigma_x**2,
    correlation_length=xi,
    dimension=1,
)
```

The reference integrator uses deterministic Gauss–Legendre nodes and evaluates the covariance quadratic form. Exponential covariance has a cusp at zero lag, so its tensor-product quadrature converges algebraically and may require a larger order for high-precision comparison. Gaussian covariance is smooth and converges rapidly.

## Front/back symmetry boundary

For a stationary covariance in a homogeneous slab, front and back kernels are reflections and produce the same filtered variance. This symmetry does not imply that measured optical spectra must be identical. Depth-dependent composition means, defects, carriers, interfaces, nonlinear Beer–Lambert propagation, and collection physics can break the symmetry in later observation operators.

## Non-goals

This module does not:

- calculate absorption or transmission;
- extract a band edge or detector cutoff;
- model a nonstationary depth profile;
- infer a correlation length from data;
- combine lateral and depth kernels;
- perform PL, Kane, SCBA, or topological calculations.
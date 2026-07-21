# Multiscale spatial-disorder recoverability API

This module diagnoses whether an isotropic two-dimensional Gaussian probe design can separate point composition variance from correlation length.

```python
from mct_research.spatial_disorder_inference import (
    gaussian_multiscale_variance,
    gaussian_multiscale_log_jacobian,
    gaussian_multiscale_fisher_information,
)
```

## Model

```text
V(s; A, xi) = A/(1 + 2 s^2/xi^2),
```

where `A = sigma_x^2` is the point variance and `xi` is the Gaussian `exp(-1/2)` correlation scale used by the lateral benchmark.

The diagnostic parameterization is

```text
theta = (log A, log xi).
```

This avoids mixing the numerical units of variance and length in the Fisher matrix.

## Prediction and Jacobian

```python
predicted = gaussian_multiscale_variance(
    point_variance=A,
    correlation_length=xi,
    probe_sigmas=scales,
)

jacobian = gaussian_multiscale_log_jacobian(
    point_variance=A,
    correlation_length=xi,
    probe_sigmas=scales,
)
```

The exact columns are

```text
dV/dlogA  = V

dV/dlogxi = V * 4 s^2/(xi^2 + 2 s^2).
```

## Fisher diagnostics

For independent relative uncertainty,

```python
diagnostics = gaussian_multiscale_fisher_information(
    point_variance=A,
    correlation_length=xi,
    probe_sigmas=scales,
    relative_standard_deviation=0.05,
)
```

Independent absolute standard deviations can be supplied with

```python
observation_standard_deviations=sigma_y
```

and a full correlated covariance with

```python
observation_covariance=Sigma_y.
```

Exactly one uncertainty representation is required.

The function Cholesky-whitens the analytical Jacobian and returns:

- predicted variances;
- probe ratios `s/xi`;
- log-parameter Jacobian;
- observation covariance;
- Fisher matrix;
- singular values;
- numerical rank and absolute rank threshold;
- condition number;
- log-parameter covariance and correlation when full rank;
- a normalized null direction when rank deficient;
- a scale-regime classification.

## Regime interpretation

```text
small_probe          max(s/xi) <= 0.1
large_probe          min(s/xi) >= 10
spanning_transition  min(s/xi) < 1 < max(s/xi)
intermediate_one_sided otherwise
```

### Small-probe regime

```text
s << xi  => V(s) ~= A.
```

The correlation-length derivative vanishes. More precision at the same small scales does not create meaningful length information.

### Large-probe regime

```text
s >> xi  => V(s) ~= A xi^2/(2s^2).
```

Only the product `A xi^2` is identifiable. In log parameters the Jacobian columns approach the ratio

```text
dV/dlogxi = 2 dV/dlogA.
```

### Transition-spanning regime

Scales on both sides of `s/xi ~ 1` can separate amplitude and length under finite noise. Full rank alone is insufficient; the condition number and parameter correlation must also be reported.

## Example

```python
diagnostics = gaussian_multiscale_fisher_information(
    point_variance=1.0e-6,
    correlation_length=2.0e-6,
    probe_sigmas=[0.0, 0.4e-6, 2.0e-6, 10.0e-6],
    relative_standard_deviation=0.05,
)

assert diagnostics.rank == 2
print(diagnostics.condition_number)
print(diagnostics.parameter_correlation)
```

Under independent relative noise, Fisher conditioning is invariant to a common rescaling of `A`. It is also invariant when every probe scale and `xi` are expressed in a different but consistent length unit.

## Boundaries

This module does not:

- estimate parameters from noisy data;
- provide confidence intervals beyond the local Fisher approximation;
- perform profile likelihood or covariance-family selection;
- infer a physical point-spread function;
- ingest HgCdTe maps;
- couple to absorption, detector cutoff, PL, or Kane physics.

A rank-two result is model-conditioned evidence that the declared design contains local information. It is not proof that the Gaussian covariance family is correct.
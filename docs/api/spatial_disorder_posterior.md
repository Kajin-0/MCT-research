# Nonlinear common-scale posterior propagation

This additive API propagates a common multiplicative probe-scale calibration through the full nonlinear spatial-disorder posterior.

## Relative-scale posterior

```python
from mct_research.spatial_disorder_posterior import (
    relative_scale_posterior_grid,
)

posterior = relative_scale_posterior_grid(
    observed_variances=observed,
    probe_sigmas=scales,
    log_point_variance_grid=u_grid,
    log_relative_correlation_grid=lambda_grid,
    likelihood="log_gaussian",
    relative_standard_deviation=0.05,
)
```

The inferred coordinates are

```text
u      = log(point variance)
lambda = log(correlation length) - common log-scale error
```

The result contains normalized probability mass, mean, covariance, the marginal relative-length distribution, boundary mass, and the discrete log normalizer.

Supported likelihoods are:

```text
log_gaussian
gaussian
```

Exactly one matching observation-uncertainty interface must be supplied.

## Calibration prior

```python
from mct_research.spatial_disorder_posterior import (
    discrete_distribution,
    gaussian_grid_distribution,
)

calibration = gaussian_grid_distribution(
    grid=delta_grid,
    mean=0.0,
    standard_deviation=0.08,
)
```

`discrete_distribution` accepts an arbitrary normalized or unnormalized non-negative mass array on a uniform grid and reports its first four cumulants.

## Exact common-scale convolution

```python
from mct_research.spatial_disorder_posterior import (
    combine_common_scale_calibration,
)

absolute = combine_common_scale_calibration(
    relative_posterior=posterior,
    calibration_prior=calibration,
)
```

Under the declared factorization conditions,

```text
log xi_absolute = log xi_relative + delta.
```

The returned result contains:

```text
absolute log-correlation distribution
mean and covariance of (log A, log xi_absolute)
covariance increment
first four log-correlation cumulants
variance-addition residual
cross-covariance residual
```

The relative posterior and calibration prior must use the same grid spacing for direct discrete convolution.

## Direct bounded-prior verification

```python
from mct_research.spatial_disorder_posterior import (
    direct_bounded_common_scale_posterior,
)

direct = direct_bounded_common_scale_posterior(
    observed_variances=observed,
    probe_sigmas=scales,
    log_point_variance_grid=u_grid,
    log_absolute_correlation_grid=v_grid,
    calibration_prior=calibration,
    likelihood="log_gaussian",
    relative_standard_deviation=0.08,
)
```

This routine evaluates the direct posterior in

```text
(log A, log xi_absolute, delta)
```

using a finite uniform prior over the supplied absolute log-length grid. It reports:

```text
absolute-length boundary mass
posterior calibration total variation
calibration mean and variance shifts
Cov(log xi_relative, delta)
variance-addition residual
cross-covariance residual
```

The direct path verifies factorization for broad support and quantifies its failure when a finite absolute-length prior becomes active.

## Exact theorem

When the likelihood depends on scale only through `s*exp(delta)/xi`, the calibration prior is independent, and the absolute log-length prior is translation invariant over posterior support,

```text
p(u, lambda, delta | data)
=
p(u, lambda | data) p_delta(delta).
```

Therefore

```text
kappa_n(log xi_absolute)
=
kappa_n(log xi_relative) + kappa_n(delta)
```

for every existing cumulant. In particular,

```text
Var(log xi_absolute)
=
Var(log xi_relative) + Var(delta)
```

and

```text
Cov(log A, log xi_absolute)
=
Cov(log A, log xi_relative).
```

## Scientific boundary

This API does not:

- infer a specimen correlation length;
- validate a Gaussian covariance family;
- provide a general-purpose Bayesian framework;
- make the factorization exact under informative or active bounded priors on absolute correlation length;
- replace explicit treatment of independent scale errors, kernel-shape errors, thickness, or modality-specific observation operators.

The grid posterior is deterministic and model conditioned. Boundary mass must be checked before applying the exact convolution identity to a finite-prior calculation.

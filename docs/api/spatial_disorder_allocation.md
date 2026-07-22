# Spatial-disorder probe-allocation API

This module allocates a fixed repeat budget across multiscale Gaussian-probe measurements. It reuses the R04 Gaussian Fisher, common scale-calibration, Matérn covariance, and three-scale falsification APIs.

```python
from mct_research.spatial_disorder_allocation import (
    endpoint_d_optimal_allocation,
    endpoint_integer_d_efficiency,
    gaussian_allocation_diagnostics,
    gaussian_log_correlation_sensitivity,
    optimize_three_scale_allocation,
)
```

## Sensitivity

```python
g = gaussian_log_correlation_sensitivity(
    probe_sigmas=[0.1, 1.0, 2.0],
    correlation_length=1.0,
)
```

For the two-dimensional Gaussian benchmark,

```text
g(s/xi) = 4(s/xi)^2/[1+2(s/xi)^2].
```

## Endpoint D-optimal allocation

```python
counts = endpoint_d_optimal_allocation(total_repeats=31)
# [15, 16]
```

The continuous optimum places equal weight at the feasible minimum and maximum probe scales. Integer rounding changes the counts by at most one.

```python
efficiency = endpoint_integer_d_efficiency(31)
```

## Allocation diagnostics

```python
diagnostic = gaussian_allocation_diagnostics(
    point_variance=0.01,
    correlation_length=1.0,
    probe_sigmas=[0.1, 1.0, 2.0],
    repeats=[11, 7, 12],
    single_repeat_relative_standard_deviation=0.03,
    common_log_scale_standard_deviation=0.02,
)
```

The returned object includes:

```text
Fisher matrix and determinant
D-efficiency relative to balanced endpoints
relative-scale parameter covariance
absolute-scale parameter covariance
relative and absolute log-xi standard deviations
parameter correlation and condition number
```

The common absolute-scale calibration contribution is kept separate and must obey

```text
Var(log xi_absolute) = Var(log xi_relative) + tau_scale^2.
```

## Three-scale precision/falsification compromise

```python
result = optimize_three_scale_allocation(
    point_variance=0.01,
    correlation_length=1.0,
    probe_sigmas=[0.1, 1.0, 2.0],
    total_repeats=30,
    single_repeat_relative_standard_deviation=0.03,
    minimum_middle_repeats=1,
    minimum_d_efficiency=0.8,
    common_log_scale_standard_deviation=0.02,
)
```

The optimizer enumerates positive integer allocations. Among designs satisfying the D-efficiency floor, it maximizes the minimum absolute standardized reciprocal-linearity residual over the established Matérn alternatives `nu=1/2, 3/2, 5/2`.

The result contains:

```text
recommended allocation
complete Pareto front
all enumerated designs
Gaussian parameter precision
Matérn standardized residuals
```

## Boundaries

- The design is local in the declared `s/xi` ratios.
- Physical probe sizes require a design value or range for `xi`.
- The Gaussian family must still be tested with the third scale.
- Repeat allocation cannot remove common absolute scale-calibration uncertainty.
- The result is not a specimen covariance estimate, instrument prescription, or manuscript authorization.

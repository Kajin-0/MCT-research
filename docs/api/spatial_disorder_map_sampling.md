# Correlated spatial-map sampling API

This module computes exact covariance and finite-map statistics for Gaussian-correlated material measured through Gaussian spatial kernels.

```python
from mct_research.spatial_disorder_map_sampling import (
    gaussian_filtered_cross_covariance,
    gaussian_map_covariance_matrix,
    gaussian_map_sampling_diagnostics,
    gaussian_regular_grid_sampling_diagnostics,
    regular_grid_positions,
)
```

## Cross covariance

```python
cov_ij = gaussian_filtered_cross_covariance(
    covariance,
    kernel_i,
    kernel_j,
    displacement=r_i - r_j,
)
```

For material covariance matrix `Lambda` and kernel covariance matrices `Sigma_i`, `Sigma_j`, the result is

```text
A sqrt(det(Lambda)/det(Lambda + Sigma_i + Sigma_j))
  exp[-0.5 delta.T @ inv(Lambda + Sigma_i + Sigma_j) @ delta].
```

Equal kernels at zero displacement recover the established filtered-variance theorem.

## Map covariance matrix

```python
C = gaussian_map_covariance_matrix(
    covariance,
    positions,
    common_kernel,
)
```

A sequence containing one kernel per position may be supplied for mixed-resolution maps.

## Regular grids

```python
positions = regular_grid_positions(
    shape=(10, 10),
    spacing=(0.5, 0.5),
)
```

All lengths in one call must use consistent units.

## Finite-map statistics

```python
result = gaussian_map_sampling_diagnostics(C)
```

The result reports:

```text
nominal_sample_count
average_marginal_variance
map_mean_variance
map_mean_effective_sample_count
naive_sample_variance_expectation
naive_sample_variance_relative_bias
naive_sample_variance_variance
naive_sample_variance_relative_standard_deviation
variance_effective_degrees_of_freedom
covariance_condition_number
```

For a zero-mean Gaussian map vector and centering matrix `P`, the sample-variance moments are exact:

```text
E[s_naive^2]   = tr(P C)/(n-1)
Var(s_naive^2) = 2 tr[(P C)^2]/(n-1)^2.
```

`variance_effective_degrees_of_freedom` is a moment-matched scaled-chi-square summary. It is not an exact distributional identity for arbitrary correlated maps.

## Regular-grid convenience call

```python
C, result = gaussian_regular_grid_sampling_diagnostics(
    covariance,
    kernel,
    shape=(10, 10),
    spacing=0.5,
)
```

## Interpretation boundary

Nominal raster pixels are not independent repeats unless their covariance supports that approximation. Use independent maps, sufficiently separated regions, or the full covariance matrix in inference. Effective counts are diagnostics and should not replace the full covariance when accurate likelihoods or Fisher information are required.

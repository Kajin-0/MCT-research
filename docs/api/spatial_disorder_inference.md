# Spatial-disorder inference API

The inference layer extends the exact covariance/kernel core without replacing it.

```python
from mct_research.spatial_disorder_inference import (
    cutoff_standard_deviation_um,
    probe_averaged_gap_moments,
    recover_isotropic_gaussian_two_scales,
    single_scale_point_variance_family,
    top_hat_exponential_effective_variance_1d,
    top_hat_gaussian_effective_variance_1d,
    two_scale_log_parameter_condition_number,
)
```

## One-scale non-identifiability family

```python
point_variance = single_scale_point_variance_family(
    effective_variance=measured_variance,
    correlation_length=declared_xi,
    probe_sigma=probe_sigma,
    dimension=2,
)
```

For every positive declared correlation length, the function returns a point variance that reproduces the same one-scale observation. A single measured width cannot identify both quantities.

## Arbitrary-dimensional two-scale inverse

```python
result = recover_isotropic_gaussian_two_scales(
    effective_variance_1=v1,
    effective_variance_2=v2,
    probe_sigma_1=s1,
    probe_sigma_2=s2,
    dimension=3,
)
```

The result includes:

```text
point_variance
point_standard_deviation
correlation_length
powered_variance_ratio
log_parameter_condition_number
relative_reconstruction_residual
```

The inverse assumes an isotropic Gaussian covariance and Gaussian probes. It identifies model parameters; it does not validate the model family.

## Conditioning diagnostic

```python
condition_number = two_scale_log_parameter_condition_number(
    correlation_length=xi,
    probe_sigma_1=s1,
    probe_sigma_2=s2,
    dimension=2,
)
```

The diagnostic uses logarithmic parameters `(ln point_variance, ln correlation_length)`. Equal scales are singular. Two scales much smaller than the correlation length or two scales much larger than it are also poorly conditioned.

## Top-hat kernels

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

These are exact one-dimensional formulas. Their difference provides a direct covariance-family sensitivity test.

## Gap propagation

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

The function returns second-order mean and variance propagation. The variance is exact for a quadratic gap law and Gaussian probe-averaged composition.

For a small gap spread around a nonzero cutoff energy,

```python
sigma_lambda_um = cutoff_standard_deviation_um(
    gap_standard_deviation_ev=sigma_gap,
    cutoff_wavelength_um=lambda_c,
    cutoff_energy_ev=energy_c,
)
```

## Boundaries

The module does not infer a specimen covariance from Herrmann, Chang, Dingrong, or Ivanov-Omskii data. It does not equate composition variance with Urbach energy, PL linewidth, or detector-cutoff spread. Those links require explicit observation operators and independent validation.

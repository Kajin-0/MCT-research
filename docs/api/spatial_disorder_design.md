# Multiscale spatial-disorder measurement design API

This module composes the validated Stage 1 analytical layers into one controlled forward prediction:

```text
point composition variance and correlation length
    -> probe-filtered composition variance
    -> first-order gap width
    -> operation-order-correct response cutoff.
```

```python
from mct_research.spatial_disorder_design import (
    multiscale_gaussian_gap_width,
    multiscale_gaussian_gap_cutoff_prediction,
)
```

## First-order composition-to-gap closure

For an isotropic two-dimensional Gaussian covariance,

```text
V_x(s) = sigma_x^2/(1 + 2 s^2/xi^2).
```

A declared local gap slope gives

```text
sigma_G(s) = |dE_g/dx| sqrt(V_x(s)).
```

Use

```python
width = multiscale_gaussian_gap_width(
    point_composition_variance=sigma_x**2,
    correlation_length=xi,
    gap_slope_ev_per_fraction=dEg_dx,
    probe_sigmas=scales,
)
```

The returned read-only arrays are:

- `probe_sigmas`;
- `probe_scale_ratios`;
- `effective_composition_variance`;
- `effective_composition_standard_deviation`;
- `effective_gap_standard_deviation_ev`.

The input scale order is preserved. A scalar scale produces zero-dimensional read-only arrays; a one-dimensional input produces arrays of the same shape.

The gap slope may be positive or negative. Only its magnitude enters the first-order width. A zero slope is a valid deterministic-gap limit.

## Exact scale limits

### Point probe

```text
s=0

V_x=sigma_x^2

sigma_G=|dE_g/dx| sigma_x.
```

### Large probe

In two dimensions,

```text
V_x(s) ~ sigma_x^2 xi^2/(2s^2)

sigma_G(s) ~ |dE_g/dx| sigma_x xi/(sqrt(2)s).
```

Consistently rescaling `s` and `xi` into another length unit leaves the prediction unchanged.

## End-to-end cutoff prediction

```python
prediction = multiscale_gaussian_gap_cutoff_prediction(
    point_composition_variance=sigma_x**2,
    correlation_length=xi,
    gap_slope_ev_per_fraction=dEg_dx,
    probe_sigmas=scales,
    mean_gap_ev=mean_gap,
    thickness_cm=thickness,
    lower_energy_ev=lower,
    upper_energy_ev=upper,
    target_response=0.5,
    exponent=0.5,
    amplitude_cm_inverse_ev_power=amplitude,
)
```

For every filtered gap width, the function calls the validated operation-order cutoff solver. It reports read-only arrays for:

- transmission-averaged cutoff energy and wavelength;
- scalar mean-absorption-closure cutoff energy and wavelength;
- energy and wavelength differences between the two operation orders;
- response residuals;
- bisection iteration counts.

The nested `gap_width` result retains the probe-filtering quantities and the declared first-order closure metadata.

## Falsifiable scale prediction

The exact universal prediction at this model level is the decrease of filtered composition variance and linearized gap width with increasing Gaussian probe scale.

As `s/xi` becomes large,

```text
sigma_G -> 0,
```

so both cutoff calculations converge to the deterministic local-gap result.

A monotone cutoff shift is not imposed as a universal theorem. In the controlled `p=0` step-edge model, however, both cutoff energies are Gaussian quantiles and their difference is proportional to `sigma_G`. The operation-order cutoff shift therefore decreases in direct proportion to the filtered gap width for that declared benchmark.

## Measurement-design interpretation

A practical multiscale experiment should use specimen-plane Gaussian-equivalent probe widths spanning `s/xi = O(1)`. Measurements entirely in either asymptotic regime remain poorly conditioned:

```text
s << xi: the width is nearly the point width;

s >> xi: the width depends mainly on sigma_x xi/s.
```

The cutoff prediction does not replace the recoverability diagnostics in `spatial_disorder_inference.py`. It supplies the forward observable that a later source-bounded design can combine with an uncertainty model.

## Scientific boundary

This module does not:

- evaluate `E_g(x,T)` or its curvature;
- establish that composition is the dominant broadening field;
- infer composition from an optical edge;
- model a measured point-spread function;
- combine lateral and depth kernels;
- distribute thickness, amplitude, carrier density, defects, or strain;
- apply the Chang 2006 absorption parameterization;
- fit an experimental correlation length;
- perform PL, SCBA, Kane, or topological calculations.

The composition-to-gap step is explicitly first order. Any application near a strongly curved gap-composition regime must first pass a curvature and bounded-quadrature audit.
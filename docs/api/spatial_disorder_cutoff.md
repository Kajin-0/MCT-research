# Spatial-disorder detector-cutoff API

This module quantifies a second operation-order effect after lateral transmission averaging.

```python
from mct_research.spatial_disorder_cutoff import (
    lateral_gaussian_gap_response_curves,
    lateral_gaussian_gap_response_cutoff,
)
```

## Competing response curves

For local columns

```text
alpha(E|G) = A max(E-G,0)^p
```

with uniform thickness `d`, the operation-order-correct response is

```text
R_true(E) = 1 - E_G[exp(-d alpha(E|G))].
```

The scalar mean-absorption closure is

```text
R_mean(E) = 1 - exp[-d E_G(alpha(E|G))].
```

Use

```python
curves = lateral_gaussian_gap_response_curves(
    photon_energy_ev=energy,
    mean_gap_ev=mean_gap,
    gap_sigma_ev=gap_sigma,
    thickness_cm=thickness,
    exponent=0.5,
    amplitude_cm_inverse_ev_power=amplitude,
)
```

The result contains read-only arrays:

- `transmission_averaged_response`;
- `mean_absorption_closure_response`;
- `closure_response_excess`.

Jensen's inequality gives

```text
R_true(E) <= R_mean(E).
```

The closure therefore predicts at least as much response as the heterogeneous-column model at the same photon energy.

## Fixed-response cutoff comparison

```python
cutoff = lateral_gaussian_gap_response_cutoff(
    mean_gap_ev=mean_gap,
    gap_sigma_ev=gap_sigma,
    thickness_cm=thickness,
    lower_energy_ev=lower,
    upper_energy_ev=upper,
    target_response=0.5,
    exponent=0.5,
    amplitude_cm_inverse_ev_power=amplitude,
)
```

Both response curves must bracket the target in the explicit positive-energy interval. Deterministic bisection is applied separately to each curve.

For monotone response curves,

```text
E_cut,true >= E_cut,mean
```

and because wavelength is inversely proportional to energy,

```text
lambda_cut,true <= lambda_cut,mean.
```

The result reports:

- both cutoff energies;
- both cutoff wavelengths;
- `energy_shift_ev = E_cut,true-E_cut,mean`;
- `wavelength_shift_um = lambda_cut,true-lambda_cut,mean`;
- response values and residuals at both cutoffs;
- iteration counts;
- target response, bracket, and tolerances.

## Exact step-edge benchmark

For `p=0`, the local absorption is either zero or `A`. At `E=mean_gap`, the Gaussian active fraction is one half, so

```text
R_true(mean_gap) = 0.5 [1-exp(-A d)].
```

Choosing this value as the target returns the operation-order-correct cutoff at `mean_gap`. For nonzero gap width and finite optical thickness, the scalar mean-absorption closure reaches the same response at a lower energy.

## Thin-sample limit

For small `d`,

```text
R_true(E) = d E[alpha] - d^2 E[alpha^2]/2 + O(d^3)

R_mean(E) = d E[alpha] - d^2 E[alpha]^2/2 + O(d^3).
```

Their difference is

```text
R_mean-R_true = d^2 Var(alpha)/2 + O(d^3).
```

The cutoff shift therefore tends to zero with optical thickness when the response target remains bracketed.

## Scientific boundary

This benchmark assumes:

- one local gap per lateral column;
- a common uniform thickness;
- a monotone controlled local edge;
- single-pass absorptance;
- no reflection, interference, scattering, or diffuse transport;
- no variation in carrier collection or electronic transport.

It does not apply the Chang 2006 absorption parameterization, distribute multiple local parameters, or predict a production detector cutoff. Those steps require separate source-domain and identifiability audits.
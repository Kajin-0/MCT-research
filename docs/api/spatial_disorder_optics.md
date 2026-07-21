# Lateral transmission-averaging API

This module quantifies the first nonlinear observation-order effect in the Stage 1 spatial-disorder program.

```python
from mct_research.spatial_disorder_optics import (
    gaussian_gap_averaged_log_transmission,
    lateral_gaussian_gap_transmission_observation,
)
```

## Controlled column model

Each lateral column has one local gap `G`, one uniform thickness `d`, and the controlled local edge

```text
alpha(E | G) = A max(E-G, 0)^p.
```

The column gaps follow the same symmetrically truncated and renormalized Gaussian convention used by the repository's scalar spectral-convolution benchmark.

Two operations are compared:

```text
mean_alpha(E) = E_G[alpha(E | G)]

T_bar(E) = E_G[exp(-d alpha(E | G))]

alpha_T(E) = -log(T_bar(E))/d.
```

In general,

```text
alpha_T(E) != mean_alpha(E).
```

Jensen's inequality gives the exact ordering

```text
alpha_T(E) <= mean_alpha(E)
```

or

```text
T_bar(E) >= exp[-d mean_alpha(E)].
```

The heterogeneous specimen is therefore more transmitting than a homogeneous Beer–Lambert model built from the arithmetic mean absorption.

## Stable averaged log transmission

```python
log_transmission = gaussian_gap_averaged_log_transmission(
    photon_energy_ev=energy,
    mean_gap_ev=mean_gap,
    gap_sigma_ev=gap_sigma,
    thickness_cm=thickness,
    exponent=0.5,
    amplitude_cm_inverse_ev_power=amplitude,
)
```

The function returns

```text
log E_G[exp(-d alpha(E | G))].
```

The absorbing interval is integrated only where `G <= E`. The transparent probability is added analytically, and the two contributions are combined with log-sum-exp arithmetic. This keeps the log transmission meaningful even when the ordinary transmission underflows to zero.

For `p=0`, the active and transparent probabilities are both analytical. At `E=mean_gap`, symmetry gives

```text
mean_alpha = A/2

T_bar = 0.5 [1 + exp(-A d)].
```

## Operation-order observation

```python
observation = lateral_gaussian_gap_transmission_observation(
    photon_energy_ev=energy,
    mean_gap_ev=mean_gap,
    gap_sigma_ev=gap_sigma,
    thickness_cm=thickness,
    exponent=0.5,
    amplitude_cm_inverse_ev_power=amplitude,
)
```

The result contains read-only arrays:

- `mean_absorption_cm_inverse`;
- `log_averaged_transmission`;
- `averaged_transmission`;
- `transmission_effective_absorption_cm_inverse`;
- `jensen_gap_cm_inverse`;
- `relative_closure_error`.

The closure metrics are

```text
Jensen gap = mean_alpha - alpha_T

relative closure error = (mean_alpha-alpha_T)/mean_alpha
```

where the mean absorption is positive. The relative error is defined as zero where both absorptions vanish.

## Limiting behavior

### Deterministic local gap

```text
sigma_G = 0 => alpha_T = mean_alpha.
```

### Zero optical amplitude

```text
A = 0 => T_bar = 1 and both absorptions vanish.
```

### Thin sample

Expanding the exponential gives

```text
alpha_T = mean_alpha - d Var(alpha)/2 + O(d^2).
```

Thus the scalar mean-absorption closure becomes accurate as optical thickness tends to zero.

### Optically thick heterogeneous sample

The lowest-absorption columns dominate the averaged transmission. The arithmetic mean absorption can substantially overestimate the transmission-derived effective absorption.

## Scientific boundary

This is a lateral mixture of independent uniform columns. It does not model:

- composition changing continuously along an optical ray;
- a lateral point-spread function or finite numerical aperture;
- coherent thin-film interference;
- scattering or diffuse transport;
- depth-dependent defects, carriers, strain, or mean composition;
- detector collection efficiency or cutoff extraction;
- a complete Kane or empirical HgCdTe absorption law.

The result isolates one exact operation-order error. It should be composed with spatial kernels and more complete local physics only in later, separately validated stages.
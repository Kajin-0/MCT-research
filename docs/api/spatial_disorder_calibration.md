# Probe-scale calibration diagnostics

This additive API quantifies how uncertainty in Gaussian probe scale affects local recovery of microscopic point variance and correlation length.

The physical benchmark is

```text
V(s)=A/(1+2s^2/xi^2).
```

Calibration errors are represented in log space:

```text
delta_log_s = B @ eta.
```

`B` is a declared basis and `eta` contains nuisance calibration coordinates.

## Common calibration

```python
from mct_research.spatial_disorder_calibration import (
    common_probe_scale_calibration_information,
)

result = common_probe_scale_calibration_information(
    point_variance=0.03,
    correlation_length=1.4,
    probe_sigmas=[0.2, 0.7, 2.0, 6.0],
    calibration_log_standard_deviation=0.08,
    relative_standard_deviation=0.04,
)
```

A common multiplicative scale error is exactly confounded with absolute correlation length because

```text
dV/dlog(s_i) = -dV/dlog(xi).
```

Set `calibration_log_standard_deviation=None` to represent an uncalibrated common scale. The marginalized physical information then has rank one and `log xi` is unidentifiable.

For a finite common calibration prior with log-standard deviation `tau_s`, the exact local covariance identity is

```text
Cov(log A, log xi)_calibrated
=
Cov(log A, log xi)_exact_scale
+ [[0, 0], [0, tau_s**2]].
```

## Independent per-scale calibration

```python
from mct_research.spatial_disorder_calibration import (
    independent_probe_scale_calibration_information,
)

result = independent_probe_scale_calibration_information(
    point_variance=0.02,
    correlation_length=1.5,
    probe_sigmas=[0.15, 0.5, 1.5, 4.5, 12.0],
    calibration_log_standard_deviations=[0.02] * 5,
    relative_standard_deviation=0.03,
)
```

Independent errors perturb relative scale spacing and can inflate uncertainty in both `log A` and `log xi`.

## Arbitrary correlated calibration basis

```python
import numpy as np

from mct_research.spatial_disorder_calibration import (
    gaussian_probe_scale_calibration_information,
)

scales = np.array([0.25, 0.6, 1.4, 3.2, 7.0])
basis = np.column_stack(
    (
        np.ones(scales.size),
        np.linspace(-1.0, 1.0, scales.size),
    )
)

result = gaussian_probe_scale_calibration_information(
    point_variance=0.04,
    correlation_length=1.6,
    probe_sigmas=scales,
    calibration_basis=basis,
    calibration_prior_covariance=[
        [0.04**2, 0.25 * 0.04 * 0.02],
        [0.25 * 0.04 * 0.02, 0.02**2],
    ],
    relative_standard_deviation=0.03,
    calibration_mode="common_plus_tilt",
)
```

The nuisance coordinates are marginalized using a Schur complement. A prior may be supplied as:

- `calibration_prior_standard_deviations`;
- `calibration_prior_covariance`;
- `calibration_prior_precision`;
- no prior, representing unconstrained nuisance coordinates.

## Returned diagnostics

`ProbeScaleCalibrationDiagnostics` contains:

```text
base_diagnostics
calibration_basis
probe_log_jacobian
nuisance_jacobian
nuisance_prior_precision
joint_fisher_matrix
nuisance_fisher_matrix
marginalized_fisher_matrix
singular_values
rank
rank_tolerance
condition_number
parameter_covariance
parameter_correlation
standard_deviation_inflation
null_direction
nuisance_dimension
calibration_mode
```

All numerical arrays are read-only.

## Scientific boundary

This API is a local linear-Gaussian information calculation. It does not:

- calibrate an instrument;
- validate the Gaussian covariance family;
- infer a specimen correlation length;
- model large nonlinear calibration errors automatically;
- identify optical tail energy, PL linewidth, or cutoff spread with microscopic composition variance.

The exact common-mode identity relies on the declared observation depending on scale through `s/xi`. Additional independently calibrated absolute-length dependencies can break that identity.

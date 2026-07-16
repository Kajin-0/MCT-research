# First-order composition uncertainty in HgCdTe gap benchmarks

## Scope

This benchmark layer addresses a narrow but important failure mode: a residual of
a few meV can be produced by uncertainty in Cd mole fraction rather than by a
missing temperature-dependent physical term.

For a reported composition `x_hat` with Gaussian uncertainty `sigma_x`, linearize
one declared analytical model about the reported value:

```text
E(x, T) ~= E(x_hat, T) + (dE/dx) delta_x.
```

The corresponding first-order marginal variance for one independent observation
is

```text
sigma_eff^2 = sigma_E^2 + [(dE/dx) sigma_x]^2.
```

For example, when

```text
|dE/dx| = 1.7 eV per mole fraction
sigma_x = 0.003,
```

the composition contribution is

```text
5.1 meV.
```

A 5 meV residual in that regime is therefore not automatically evidence for a
new thermal term.

## Shared specimen covariance

Repeated temperatures from one specimen do not have independent composition
errors. With one shared specimen perturbation `delta_x,g`, observations `i` and
`j` in group `g` acquire covariance

```text
C_ij^(x) = (dE_i/dx)(dE_j/dx) sigma_x,g^2.
```

The implemented `shared_group` mode adds this rank-one block to the diagonal
energy-measurement covariance. It requires every member of a group to carry the
same reported composition and composition uncertainty. This prevents a single
specimen uncertainty from being counted repeatedly as independent information.

The `independent` mode is available only when each record genuinely has an
independent composition determination or when the analyst explicitly accepts a
diagonal approximation.

## Iterative generalized least squares

The derivative depends on the fitted coefficients, so the covariance is also
parameter-dependent. The fitter therefore uses a fixed-point generalized least
squares iteration:

1. fit using the reported energy covariance;
2. calculate the analytic `dE/dx`;
3. build the independent or shared-group composition covariance;
4. refit with the updated covariance;
5. stop only when the covariance change meets the declared tolerance.

Nonzero `sigma_x` requires an explicit uncertainty specification. The code does
not silently choose independent or shared-specimen semantics.

## Measurement and source separation

Each observation carries:

- a specimen or leakage-safe `group`;
- a `source` label;
- a `measurement_class` label.

Mixed measurement classes are rejected by default. They can be pooled only with
an explicit override. No source offset and no free composition shift is fitted.
A leave-one-source-out benchmark is provided to expose source-transfer failure
without absorbing it into nuisance parameters.

In shared-group cross-validation, a holdout may not split one specimen across
training and test sets. Doing so would leak the same latent composition error
into both sides of the comparison.

## Interpretation limits

This is a first-order Gaussian linearization, not a complete errors-in-variables
posterior. In particular, it does not include:

- curvature-induced mean shifts from `d^2E/dx^2`;
- non-Gaussian or asymmetric composition uncertainty;
- composition gradients within a specimen;
- covariance between composition and measured gap;
- source-dependent calibration offsets;
- a free latent composition inferred from the gap data;
- an exact parameter covariance for the parameter-dependent weighting problem.

The reported coefficient covariance is a conditional working-weight covariance.
It must not be described as an exact EIV posterior.

If the first-order composition scale is comparable to the model distinction, the
correct conclusion is that the available data do not identify that distinction.
The remedy is stronger specimen-level composition evidence, not another free
oscillator or source offset.

## Minimal usage

```python
from mct_research import (
    CompositionAwareGapData,
    CompositionUncertaintySpec,
    OscillatorBasisSpec,
    fit_composition_aware_gap_model,
)

data = CompositionAwareGapData.from_arrays(
    x,
    temperature_k,
    gap_ev,
    sigma_ev=sigma_gap_ev,
    sigma_x=sigma_composition,
    group=specimen_id,
    source=source_id,
    measurement_class=measurement_class,
)

fit = fit_composition_aware_gap_model(
    data,
    OscillatorBasisSpec(
        static_degree=3,
        amplitude_degree=1,
        oscillator_temperatures_k=(150.0,),
    ),
    composition_uncertainty=CompositionUncertaintySpec(
        mode="shared_group"
    ),
)
```

Synthetic recovery or a reduced weighted residual does not establish experimental
superiority. Real model ranking still requires specimen-level composition data,
measurement-class separation, leakage-safe holdouts, and a complete uncertainty
ledger.

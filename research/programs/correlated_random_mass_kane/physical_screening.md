# R05 Phase 0 physical screening

**Controlling issue:** #390  
**Evidence date:** 2026-07-31  
**Numerical input:** PR 2 minimal one-dimensional oracle  
**Physical-screening result:** no source-supported HgCdTe activation region identified

## 1. Screening question

The numerical oracle establishes a finite-range correlated-versus-scalar DOS distinction in a controlled one-dimensional model. PR 3 asks whether that result maps to a defensible HgCdTe parameter regime and an experimentally resolvable observable.

The control parameters are

\[
m=\frac{\overline M\xi}{\hbar v_K},
\qquad
g=\frac{\sigma_M\xi}{\hbar v_K}.
\]

The source-ranked nominal energy-length scale is

```text
hbar v_K = 0.7042868 eV nm.
```

## 2. Dimensionless physical-screening sweep

The PR 2 numerical settings were retained:

```text
L/xi = 32
a/xi = 0.125
grid points = 256
numerical broadening = 0.08
experimental convolution width = 0.25
32 periodic/antiperiodic boundary-averaged realizations per point
```

### 2.1 Near-massless mean

| `m` | `g` | `Delta_1` | batch SE | threshold result |
|---:|---:|---:|---:|---|
| `0` | `0.10` | `0.02183` | `0.00100` | fail |
| `0` | `0.20` | `0.07138` | `0.00300` | fail |
| `0` | `0.25` | `0.09874` | `0.00274` | immediately below threshold |
| `0` | `0.30` | `0.13723` | `0.00385` | pass |
| `0` | `0.40` | `0.17757` | `0.00409` | pass |

For the declared finite box and resolution, the 10% synthetic threshold is bracketed by

```text
0.25 < g_threshold < 0.30.
```

This is not a universal critical coupling. It depends on dimension, observable, numerical regularization, energy window, mass marginal, covariance family, and measurement convolution.

### 2.2 Mean-mass detuning

| `m` | `g` | `Delta_1` | batch SE | result |
|---:|---:|---:|---:|---|
| `0.5` | `0.3` | `0.07899` | `0.00577` | fail |
| `0.5` | `0.6` | `0.21675` | `0.00645` | pass |
| `1.0` | `0.3` | `0.08178` | `0.01678` | fail |
| `1.0` | `0.6` | `0.10083` | `0.03041` | statistically unresolved |
| `1.0` | `1.0` | `0.35856` | `0.01970` | pass |

The effect is easiest to obtain close to the mean-massless point. Detuning requires stronger dimensionless disorder and produces greater realization-to-realization uncertainty.

Deeply gapped regimes were not used for activation because a relative effect statistic can become misleading when the reference spectral weight in the selected energy window is extremely small.

## 3. Exploratory HgCdTe mapping

At `77 K`, the repository Hansen law gives

```text
x_c = 0.1494464216
dEg/dx at x_c = 1.661253 eV per Cd fraction.
```

Under the local linearization

\[
\sigma_M
\simeq
\frac12\left|\frac{\partial E_g}{\partial x}\right|\sigma_x,
\]

the threshold bracket maps as follows.

| exploratory `sigma_x` | `sigma_M` | `xi` for `g=0.25` | `xi` for `g=0.30` |
|---:|---:|---:|---:|
| `0.0005` | `0.415 meV` | `424 nm` | `509 nm` |
| `0.0010` | `0.831 meV` | `212 nm` | `254 nm` |
| `0.0020` | `1.661 meV` | `106 nm` | `127 nm` |
| `0.0050` | `4.153 meV` | `42.4 nm` | `50.9 nm` |
| `0.0100` | `8.306 meV` | `21.2 nm` | `25.4 nm` |

These rows are mathematical mappings of exploratory values. They are not a measured HgCdTe parameter envelope.

The reported historical sample-homogeneity statement of approximately `+/-0.002` in composition is not a local standard deviation, is from a different composition domain, and contains no spatial covariance definition. It cannot validate the `sigma_x=0.002` row.

No qualifying near-critical HgCdTe source was identified for the continuum electronic-mass correlation length `xi`.

## 4. Energy-resolution mapping

The decision convolution corresponds to

\[
\delta E_{\rm decision}
=0.25\frac{\hbar v_K}{\xi}.
\]

At fixed `g`, this can also be written

\[
\delta E_{\rm decision}
=\frac{0.25}{g}\sigma_M.
\]

For the threshold bracket:

| exploratory `sigma_x` | resolution for `g=0.25` | resolution for `g=0.30` |
|---:|---:|---:|
| `0.0005` | `0.415 meV` | `0.346 meV` |
| `0.0010` | `0.831 meV` | `0.692 meV` |
| `0.0020` | `1.661 meV` | `1.384 meV` |
| `0.0050` | `4.153 meV` | `3.461 meV` |
| `0.0100` | `8.306 meV` | `6.922 meV` |

A tunneling experiment whose thermal width is approximated by `3.5 k_B T` would require, before allowing for modulation, contact, lifetime, and background broadening:

| exploratory `sigma_x` | maximum `T` for `g=0.25` | maximum `T` for `g=0.30` |
|---:|---:|---:|
| `0.0005` | `1.38 K` | `1.15 K` |
| `0.0010` | `2.75 K` | `2.30 K` |
| `0.0020` | `5.51 K` | `4.59 K` |
| `0.0050` | `13.8 K` | `11.5 K` |
| `0.0100` | `27.5 K` | `23.0 K` |

These are upper thermal ceilings, not feasibility claims. Real experiments require a smaller thermal contribution because several independent broadening mechanisms consume the resolution budget.

## 5. Experimental observable assessment

### 5.1 Tunneling DOS

The scalar null predicts a smooth linear low-energy DOS for a continuous mass marginal, whereas the 1D correlated oracle produces excess near-zero spectral weight. This makes tunneling DOS the cleanest conceptual discriminator.

The gate still fails because no identified near-critical HgCdTe specimen has all of:

```text
independently measured local mass distribution
source-qualified xi
controlled surface and contact electrostatics
sub-meV-to-few-meV resolution matched to the same specimen
bulk-representative tunneling response
```

A zero-bias conductance alone would not distinguish correlated mass from surface accumulation, band bending, charged-disorder puddles, contact-barrier distributions, lifetime broadening, or surface states.

### 5.2 Magneto-optics

Massless-Kane magneto-optics is experimentally established, but the present oracle cannot predict a discriminating line shape. A valid calculation would require:

```text
multiband Kane Landau levels
heavy-hole participation
optical matrix elements
carrier filling
magnetic-field-dependent disorder treatment
matched scalar mixture of homogeneous transition spectra
instrument and lifetime convolution
```

Because no source-supported material overlap exists, this full-Kane calculation is not currently decision changing.

### 5.3 Spatial spectroscopy

A direct spatial map would be scientifically strongest, but it requires an independently calibrated composition or mass proxy, lateral point-spread width below approximately `xi/2`, a field of view spanning many correlation lengths, and full finite-kernel covariance inference. No qualifying public dataset was identified.

## 6. Full-Kane necessity after screening

Full Kane structure is necessary for a quantitative optical or magneto-optical prediction because of the heavy-hole sector, multiband matrix elements, asymmetry, degeneracy, and magnetic response.

It is not currently justified because:

1. the local mass variance is not source qualified;
2. the mass correlation length is not source qualified;
3. no experiment-specific matched null is available;
4. the additional calculation cannot presently change the final activation decision.

Decision:

```text
DEFER_NOT_DECISION_CHANGING_WITHOUT_MATERIAL_OVERLAP
```

## 7. Activation-gate result

| Required activation gate | Result |
|---|---|
| claim-level distinction from prior work | pass, narrowly framed |
| source-supported HgCdTe parameter regime | fail |
| correlated model differs from matched scalar mixture | pass in 1D synthetic model |
| effect exceeds frozen threshold | pass near `m=0`, `g=0.3` |
| numerical convergence | pass |
| covariance-family robustness | pass |
| survives source-grounded experimental convolution | fail |
| experiment can distinguish models | fail |
| next calculation is decision changing | fail |
| full-Kane status explicit | pass; deferred |

## 8. Physical-screening conclusion

The numerical distinction is real within the declared model, but the chain from model to HgCdTe is incomplete at the two decisive links:

```text
source-qualified (sigma_M, xi)
experiment-specific matched resolution and null model
```

The work should be retained as a reusable correlated-versus-scalar method benchmark and threshold calculator. It does not support activation of an HgCdTe physics claim.
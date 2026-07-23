# CdSeTe real-map R04 demonstration result

## Decision

```text
RESTRICTED_REAL_DATA_DEMONSTRATION_COMPLETE
```

This is a restricted demonstration on a source-data-derived CdSeTe PL
peak-wavelength map. It is not HgCdTe validation and does not identify a
native physical correlation length because the sample-plane instrument
kernel is unmeasured.

## Primary added-kernel sweep

```text
sigma pixels       [0.0, 0.5, 1.0, 2.0, 4.0]
variance nm^2      [13.73732519293478, 11.374408090901321, 7.829969631751158, 4.3497792689765, 1.5443547243068794]
fraction raw       [1.0, 0.8279929266544024, 0.5699777447052193, 0.3166394627691879, 0.11242033675530617]
```

## Descriptive family fits

- Gaussian: train log-RMS `0.0330701`, held-out relative error `+13.518143%`, descriptive scale `2.02659 px`.
- Matern_nu_1_over_2: train log-RMS `0.0838957`, held-out relative error `-6.478097%`, descriptive scale `2.20293 px`.
- Matern_nu_3_over_2: train log-RMS `0.00998593`, held-out relative error `+4.824086%`, descriptive scale `2.09712 px`.
- Matern_nu_5_over_2: train log-RMS `0.0112856`, held-out relative error `+8.017865%`, descriptive scale `2.07239 px`.

These are closure diagnostics on deterministic transforms of one
raster, not independent model validation or a universal-family result.

## Same-raster dependence

```text
bias factors                 [0.9625876449009557, 0.9582025140885805, 0.9453816543879127, 0.8980918474831142, 0.7487851555512602]
effective variance dof        [49.18804762532587, 44.15270274253692, 33.95061872019799, 18.27214526384906, 7.548144417414276]
parameter SD inflation        [4.524956168633019, 0.9064386724870949]
covariance determinant ratio  16.9812
```

The covariance is exact only conditional on the fitted descriptive
Gaussian field model. It is not empirical repeat covariance.

## Sensitivity

```text
max wrap/reflect difference       72.626205%
max nearest/reflect difference    37.714925%
max crop/full difference          72.744460%
max detrended/primary difference  19.809705%
```

## Claim boundary

No HgCdTe validation, composition assignment, native-kernel
deconvolution, independent-scale claim, R05 activation, or manuscript
authorization follows from this result.

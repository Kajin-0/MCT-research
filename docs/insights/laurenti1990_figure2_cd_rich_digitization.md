# Laurenti 1990 Figure 2: calibrated Cd-rich series

## Question

What do the directly plotted high-Cd experimental series imply for the temperature dependence of the HgCdTe gap, and can the Hansen 1982 linear temperature term be extrapolated into this composition range?

## Source and calibration

The directly uploaded Laurenti PDF has SHA256:

```text
1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea
```

Page 3 is a native 300 dpi bilevel image. Figure 2 was calibrated from its printed ticks:

- temperature ticks: 0 to 400 K in 50 K increments;
- energy ticks: -0.4 to 1.7 eV in 0.1 eV increments;
- marker centers: compact-component centroids after a 3x3 binary opening;
- direct marker-center uncertainty: 1.5 pixels, corresponding to 0.726 K and 2.704 meV.

The paper separately states that the interband edges extracted from excitonic spectral fits are accurate to better than 3 meV.

## Specimens

The Camassel-to-Laurenti crosswalk supplies the 2 K anchors:

| Composition | Specimen | Growth | 2 K gap |
|---:|---|---|---:|
| 0.970 | MCT 83 | LPE | 1.5405 eV |
| 0.955 | bulk reference | THM | 1.5079 eV |
| 0.925 | MCT 51 | LPE | 1.4498 eV |

The present ledger contains six directly digitized Figure 2 markers per specimen, plus the three table anchors.

## Observed thermal shifts

At the highest digitized temperatures, approximately 300.6 K, the measured shifts from the 2 K anchors are:

| Composition | Shift |
|---:|---:|
| 0.970 | -69.483 meV |
| 0.955 | -72.398 meV |
| 0.925 | -72.698 meV |

The mean is -71.526 meV and the full range is only 3.215 meV across `Delta x = 0.045` and across both LPE and THM growth.

This similarity is descriptive, not a growth-method conclusion: there is only one THM reference specimen.

## Shape comparison

Every specimen is anchored to its own 2 K value, so the comparison tests temperature shape rather than absolute gap offset.

### Laurenti equation 7

Nominal-composition pooled residuals over all 18 markers:

| Metric | Value |
|---|---:|
| RMSE | 3.892 meV |
| MAE | 3.293 meV |
| maximum absolute residual | 7.755 meV |

This agreement is an internal reproduction, not independent validation, because these Cd-rich data contributed to the Laurenti global fit.

### Hansen 1982 temperature term extrapolated to high Cd

Nominal-composition pooled residuals:

| Metric | Value |
|---|---:|
| RMSE | 51.156 meV |
| MAE | 47.746 meV |
| maximum absolute residual | 80.689 meV |

The Hansen RMSE is 13.143 times the Laurenti RMSE.

Allowing each composition to move anywhere within its full reported `+/-0.005` uncertainty changes the Hansen pooled RMSE only to 50.130 meV. Composition uncertainty cannot rescue the extrapolation.

Near 300 K, Hansen predicts shifts of approximately -136 to -150 meV, about twice the observed magnitude.

## Decision

```text
The directly plotted Cd-rich data reject extrapolation of Hansen's linear
HgCdTe temperature term to x = 0.925-0.970.
```

The result does **not** challenge Hansen within the mercury-rich detector compositions for which it is normally used. It establishes a domain boundary: a temperature law that works near detector-grade HgCdTe does not transfer across the full alloy range.

Laurenti's nonlinear Varshni-like composition dependence reproduces the high-Cd series, but this dataset cannot independently validate the equation that was fitted to it or identify a microscopic phonon mechanism.

## Observable boundary

The reported gaps are obtained by fitting derivative-absorption spectra with three-dimensional direct-allowed exciton theory. They are experimental, model-corrected interband edges-not raw quasiparticle gaps, detector cutoffs, or magneto-optical gaps.

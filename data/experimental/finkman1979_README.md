# Finkman and Nemirovsky 1979 optical-absorption source audit

## Primary source

```text
E. Finkman and Y. Nemirovsky
Infrared optical absorption of Hg1-xCdxTe
Journal of Applied Physics 50, 4356-4361 (1979)
DOI: 10.1063/1.326421
File Library asset: finkman1979.pdf
```

The PDF is available in the user File Library but is not materialized as repository binary content. Its SHA256 is unavailable and is not fabricated.

Canonical source files are:

```text
data/experimental/finkman1979_source_metadata.csv
data/experimental/finkman1979_parameter_ledger.csv
data/experimental/finkman1979_README.md
```

## Source scope

The primary experiment covers

```text
0.205 <= x <= 0.220
80 K <= T <= 300 K
20 cm^-1 <= alpha <= 1000 cm^-1 for the fitted exponential tail
alpha <= approximately 2000 cm^-1 for the presented inversion range
```

The material was n type, with electron concentration approximately `(1-2)e15 cm^-3` and mobility approximately `1e5 cm^2 V^-1 s^-1` at 77 K.

The primary paper reports composition measured by electron-beam microprobe to approximately `+/-0.003`. Hansen 1982 later describes the compositions entering its source graph as vendor Cominco values, with Cominco calibration based on optical cutoff tied to destructive chemistry. These two provenance statements are retained in parallel. This audit does not silently decide that they are identical measurements.

## Specimen and apparatus record

The optical specimens were initially approximately `80 um` thick with thickness uniformity around `+/-2 um` and were progressively thinned to approximately `15 um`. Approximately `10 um` was removed by a final `20%` bromine-methanol etch to remove surface damage.

Thickness was determined by micrometer measurement, calibrated cleavage photographs, and interference fringes. Absorption coefficients obtained from repeated thicknesses of the same original specimen agreed within the source's experimental resolution.

The source used a Beckman model 4250 infrared spectrophotometer and an Air Products Helitran model 110 cryostat with ZnSe windows. Temperature uniformity was checked with silicon diodes and reported as better than `1 K`.

The paper explicitly detected source heating through anomalous absorption-edge shifts. Source power was reduced or attenuators were inserted until further power reduction no longer shifted the measured absorption.

## Transmission inversion is the observation operator

The stored measurement class is

```text
transmission_inverted_optical_absorption_coefficient
```

The source did not directly measure an intrinsic gap. It measured transmission, estimated refractive index from interference fringes and reflectivity, and inverted the average transmission while retaining reflection and multiple-reflection terms.

The source reports approximately:

```text
absolute refractive-index uncertainty: +/-3%
fringe-position accuracy: +/-4 cm^-1
relative refractive-index change accuracy: +/-0.5%
reflection-approximation error: less than 0.5% in the declared region
absorption error from refractive-index extrapolation: approximately 2%
```

These are article-level estimates. They are not converted into independent pointwise Gaussian errors or a diagonal covariance matrix.

## Modified-Urbach law

For `20 <= alpha <= 1000 cm^-1`, the source fits

```text
alpha = alpha0 * exp[sigma*(E-E0)/(T+T0)]
```

with `E` and `E0` in `cm^-1` and

```text
sigma = 5.65 +/- 0.07 K per cm^-1
T0 = 80.5 +/- 2 K
E0 = -3109 + 16450*x        cm^-1
ln(alpha0) = -20.44 + 51.70*x
```

The summary prints the rounded values `sigma=5.646` and `T0=80.51`.

`E0` is an intercept parameter of the fitted exponential law. It is not stored as a signed `Gamma6-Gamma8` interaction gap, an excitonic gap, or an independently observed slope-change energy.

## Fixed-alpha relation and OCR correction

The source-derived energy relation is

```text
E(alpha=const)_eV = -0.349
                  + 1.77e-3*ln(alpha_cm_inverse)
                  + 2.20e-5*T_k*[ln(alpha_cm_inverse)+20.44-51.70*x]
                  + 1.95*x
```

and

```text
dE/dT|alpha = 2.20e-5*ln(alpha_cm_inverse)
              + 4.49e-4
              - 1.13e-3*x       eV/K.
```

Some extracted text renders the Equation (10) temperature coefficient as `2.20e-7`. That transcription is inconsistent with the source's Equation (11) and with dimensional closure:

```text
1.23984e-4 eV per cm^-1 / 5.646 K per cm^-1
    = 2.196e-5 eV/K.
```

The repository therefore records `2.20e-5`.

## Gap-proxy boundary

The source states that information about the actual gap position lies where the absorption changes slope and begins to rise slowly, generally above `1000 cm^-1`. Because the thinnest available specimens were approximately `15 um`, that region could not be reached reliably.

At higher temperatures the authors concluded that

```text
E(alpha=1000 cm^-1)
```

was a reasonable estimate of the band gap. The repository records this as

```text
fixed_absorption_optical_edge_alpha_1000_cm_inverse_proxy
```

with

```text
signed_gap_eligible = false
intrinsic_gap_eligible_without_observation_operator = false
```

It is a source-defined proxy created because the intended slope-change region was unavailable, not a direct signed-gap measurement.

## Measured-range and extrapolation boundary

The fitted specimens occupy only `0.205 <= x <= 0.220`. The paper compares its parameter trends with HgTe and CdTe endpoint information and argues that portions of the parameterization can be useful over a broader composition range. It also states that the composition dependence of `T0` remains to be studied.

Accordingly:

- the narrow-range parameter fit is source data analysis;
- endpoint agreement is a cross-source consistency argument;
- whole-range use is an extrapolation claim;
- whole-range validation is not directly measured by this experiment.

## Hansen lineage

```text
hansen_graph_id = HSC_R03
role_in_hansen = fitted_data
independent_validation_of_hansen = false
```

The source may be reconstructed to understand Hansen's optical-input lineage. It cannot be described as an independent validation of Hansen.

## R03 boundary

Existing R03 work determined that Figures 3-6 do not provide a model-independent curvature validation dataset without an external latent-window or above-gap anchor. This R01 audit preserves that decision.

This tranche contains:

```text
no Figure 3-6 marker ledger
no manual curvature digitization
no Gaussian-disorder parameter
no reinterpretation of sigma, T0, or E0 as a latent gap distribution
no R03 file modification
```

## Repository-state integrity

During this audit, the canonical R01 state ledger was found to have been replaced by a one-line placeholder in earlier stacked history. The complete known-good ledger was restored before the Finkman section was added.

`tests/test_r01_state_integrity.py` now enforces:

```text
canonical title and R01 identity
minimum byte and line counts
presence of every major historical source section
manuscript and production-equation claim boundaries
explicit rejection of the placeholder value
```

The focused workflow runs this guard alongside the Finkman source tests. Future source tranches may extend the ledger, but a truncated or placeholder state can no longer pass the complete test suite silently.

## Claim boundary

This source audit supports the experiment, optical inversion, modified-Urbach fit, fixed-alpha proxy, provenance conflict, and extrapolation limits stated above.

It does not establish intrinsic signed gaps, validate logarithmic curvature, identify a disorder mechanism, refit a gap law, rank Hansen or another equation, authorize a production relation, or authorize a manuscript.

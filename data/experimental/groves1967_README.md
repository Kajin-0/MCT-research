# Groves 1967 signed HgTe magnetoreflection endpoint

## Source

```text
S. H. Groves, R. N. Brown, and C. R. Pidgeon
Interband Magnetoreflection and Band Structure of HgTe
Physical Review 161, 779-792 (1967)
DOI: 10.1103/PhysRev.161.779
File Library asset: groves1967.pdf
```

The source PDF is available in the user File Library but is not materialized as repository binary content. Its SHA256 is therefore unavailable and is not fabricated.

Canonical audit files are:

```text
data/experimental/groves1967_source_metadata.csv
data/experimental/groves1967_band_parameter_ledger.csv
data/experimental/groves1967_README.md
```

## What the source measures

Groves, Brown, and Pidgeon measured interband magnetoreflection in HgTe. They observed a high-energy transition family assigned to `Gamma6 -> Gamma8` and a lower-energy family assigned to `Gamma8 -> Gamma8` transitions.

The high-energy transition energies were compared with a coupled `Gamma6-Gamma7-Gamma8` Kane/Luttinger magnetic-field calculation. The paper reports that the observed transitions fit the inverted gray-tin ordering of HgTe.

The stored measurement class is

```text
interband_magnetoreflection
```

and the stored signed observable is

```text
signed_Gamma6_minus_Gamma8_interaction_gap
```

with convention

```text
E_g = E(Gamma6) - E(Gamma8)
E_g < 0 means inverted ordering.
```

This negative interaction gap is not the same object as the thermal-energy gap at the cubic `Gamma8` degeneracy. The source describes the latter as zero while retaining a finite negative `Gamma6-Gamma8` separation.

## Published fitted values

The abstract reports

```text
E_g = -0.283 +/- 0.001 eV
E_p = 18 +/- 1 eV
```

where the reported errors reflect uncertainty in the higher-band parameters. They are not independent pointwise measurement standard deviations and are not a reported covariance matrix.

For the representative full parameter set used in the source comparison, the paper gives

```text
E_g = -0.2833 eV
E_p = 18.13 eV
Delta = 1.0 eV
H1 = -5.0
G = -1.0
L_prime = -2.0
A_prime = 0
M = -5.0
L_minus_M_minus_N = 7.0
```

The detailed set is a conditional model parameterization. It is not an independently measured universal modern eight-band parameter vector. Translation to another Kane convention requires an explicit basis, sign, normalization, and remote-band mapping.

## Temperature ledger

The source contains two distinct temperature statements that must not be merged.

### Main paper fit

The note added in proof states that the paper's `0.283 eV` value was estimated to have been determined at approximately

```text
30 K.
```

The repository therefore records

```text
main_fit_temperature_k = 30
main_fit_temperature_status = source_note_estimate_not_directly_logged_setpoint
```

This is not relabeled as 4.2 K or 5.5 K.

### Continued low-temperature measurement

The same note reports that comparison of magnetoreflection with the sample immersed in superfluid helium and on the helium-Dewar cold finger gave

```text
|E_g| near 0.30 eV at 1.5 K.
```

Only the magnitude is printed in that sentence. The source interpretation remains inverted, but the repository does not silently replace the printed magnitude with a newly reported signed number.

The two source statements do not identify a temperature law. No slope, interpolation, or nonlinear thermal model is fitted from them.

## Sample and experiment

The magnetoreflection material was slowly grown by the Bridgman method in an Hg-rich environment at approximately

```text
0.25 cm/day.
```

The source describes the material as high purity but polycrystalline. Reflected light therefore sampled several orientations. This limits orientation- and polarization-specific interpretation.

The sample was mounted on the cold finger of a helium Dewar. Attempts to resolve the oscillations near `77 K` were unsuccessful.

A reflective surface was prepared with a `5-10%` bromine-in-methanol etch followed by a methanol rinse.

Measurements were made at fixed photon energy while sweeping magnetic field. The maximum of each magnetoreflection oscillation was used as the resonance field, and increasing- and decreasing-field results were averaged to reduce response-time errors.

One run used a thermocouple detector. A later run used a Cu-doped Ge detector operating at `4.2 K`. The detector operating temperature is not the sample temperature and is retained in a separate field.

## Model dependence

The source fit is not a direct model-free readout of `E_g` and `E_p`.

The paper varied the higher-band assumptions and performed a two-parameter least-squares fit for `E_g` and `E_p` conditional on those assumptions. It also warns that omitting higher-band terms or using an infinite-spin-orbit approximation can cause serious errors for a `Gamma8` conduction band.

Accordingly:

- the rounded uncertainties are stored as higher-band-parameter sensitivity;
- no pointwise transition-energy covariance is assigned;
- no modern parameter covariance matrix is inferred;
- the detailed source parameter set is not promoted to production defaults;
- no `P` value is derived from `E_p` in this tranche because that conversion depends on the declared convention and constants.

## Figure boundary

Figures 4 and 5 contain experimental transition energies and fitted theoretical curves. This tranche contains no calibrated marker coordinates.

It does not:

- sample the fitted curves and present them as observations;
- infer marker coordinates from flattened text;
- assign a point count from visual inspection without a calibrated ledger;
- reconstruct Figure 6 or Figure 7 transport data;
- refit the transition data.

A future digitization requires rendered source pages, calibrated axes, marker centers, transition-family labels, detector/run identity, magnetic-field uncertainty, photon-energy uncertainty, and separation of experimental points from theoretical curves.

## Hansen and alloy-law boundary

Groves 1967 is not one of the reconstructed Hansen 22 fitted alloy studies. It is a primary endpoint and sign source used by later HgCdTe literature.

It can support:

- the inverted sign of the HgTe `Gamma6-Gamma8` separation;
- a historical endpoint constraint with explicit measurement and model class;
- comparison of sign semantics with Blue 1964;
- later audits of endpoint values and Kane parameter conventions.

It cannot by itself support:

- alloy bowing or composition curvature;
- a complete `E_g(x,T)` relation;
- validation or rejection of Hansen, Laurenti, Seiler, or Hansen-Pade;
- a universal eight-band parameter set;
- a production equation;
- manuscript or submission authorization.

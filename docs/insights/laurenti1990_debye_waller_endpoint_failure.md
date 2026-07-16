# Laurenti 1990 Debye-Waller endpoint falsification

## Question

Can the temperature-dependent empirical-pseudopotential form-factor treatment examined by Laurenti et al. reproduce the signed 0-300 K gap shifts of both CdTe and HgTe?

This is an internal reproduction of a historical model failure. It is not experimental validation of a modern first-principles Fan-plus-Debye-Waller implementation.

## Quantities reported by the primary paper

Laurenti et al. fit the endpoint temperature dependence with

```text
Eg(T) = Eg(0) + a T^2 / (b + T).
```

The printed endpoint parameters are:

| Material | `a` | `b` |
|---|---:|---:|
| CdTe | `-3.25 x 10^-4 eV/K` | `78.7 K` |
| HgTe | `+6.3 x 10^-4 eV/K` | `11 K` |

The opposite signs encode the key endpoint topology:

- the CdTe signed gap decreases with temperature;
- the negative HgTe gap becomes less negative, so its signed gap change is positive.

The paper separately evaluates temperature-dependent empirical pseudopotential form factors using mean-square atomic displacements. It reports the following 0-300 K edge motions:

| Material | Lowest conduction edge | Highest valence edge |
|---|---:|---:|
| CdTe | `-16 meV` | `+175 meV` |
| HgTe | `+49 meV` | `+190 meV` |

The signed gap convention is

```text
Delta Eg = Delta Ec - Delta Ev.
```

## Empirical endpoint shifts

At 300 K, the endpoint fits give

```text
CdTe: Delta Eg = -77.2379 meV
HgTe: Delta Eg = +182.3151 meV
```

Thus the measured-fit endpoint shifts reverse sign between CdTe and HgTe.

## Debye-Waller form-factor result

The reported edge motions imply

```text
CdTe: Delta Eg_DW = -16 - 175 = -191 meV
HgTe: Delta Eg_DW = +49 - 190 = -141 meV.
```

| Material | Empirical endpoint shift | Debye-Waller shift | Residual, DW minus empirical |
|---|---:|---:|---:|
| CdTe | `-77.24 meV` | `-191 meV` | `-113.76 meV` |
| HgTe | `+182.32 meV` | `-141 meV` | `-323.32 meV` |

For CdTe, the historical model has the correct sign but predicts 2.473 times the empirical magnitude.

For HgTe, the model predicts the wrong sign. It makes the inverted gap more negative, while the empirical endpoint fit makes it less negative.

## Rounding robustness

Assuming half-unit rounding in every printed coefficient and edge shift gives:

| Quantity | Interval |
|---|---:|
| CdTe empirical shift | `[-77.367, -77.109] meV` |
| CdTe Debye-Waller shift | `[-192, -190] meV` |
| HgTe empirical shift | `[+180.578, +184.058] meV` |
| HgTe Debye-Waller shift | `[-142, -140] meV` |

The HgTe sign failure is therefore not a printed-rounding ambiguity. Its residual remains between approximately `-326.1` and `-320.6 meV` under this conservative arithmetic bound.

## Scientific decision

```text
The temperature-dependent-form-factor Debye-Waller treatment is
falsified as an endpoint-complete thermal-gap model.
```

It fails in two distinct ways:

1. it substantially overpredicts the CdTe magnitude;
2. it cannot reproduce the CdTe/HgTe endpoint sign reversal.

The important lesson is not merely that one historical calculation was inaccurate. The pseudopotential form factors were selected to reproduce composition-dependent static band structure, yet their Debye-Waller thermal transfer failed at the inverted endpoint. Static composition accuracy therefore does not establish thermal transferability.

## Consequence for the current computation program

This result reinforces the existing CdTe-first workflow while sharpening the eventual HgTe stress test.

A future microscopic workflow must:

- retain both Fan-like and Debye-Waller-like contributions;
- preserve the signed gap convention at inverted HgTe;
- validate individual edge motion as well as the total gap;
- demonstrate the opposite endpoint signs before attempting alloy interpolation;
- avoid treating a static scissors or fitted form-factor correction as sufficient thermal validation.

A successful CdTe calculation alone cannot establish the HgTe endpoint physics. CdTe provides the implementation check; HgTe remains the qualitative sign stress test after the CdTe numerical gates pass.

## Claim boundary

This analysis does not establish:

- a modern separation of Fan and Debye-Waller self-energies;
- a complete Allen-Heine-Cardona calculation;
- a matrix-valued self-energy;
- the correct microscopic origin of the HgTe sign;
- any alloy interpolation between the two endpoints;
- experimental validation of the repository's future calculations.

The source calculation changes empirical pseudopotential form factors using mean-square atomic displacement. It should not be relabeled as a complete modern Debye-Waller implementation without qualification.

## Falsification criteria

The numerical reconstruction should be revised if primary-source inspection changes any of the four reported edge shifts or the endpoint coefficients.

The computational conclusion would be weakened only if another historical contribution, omitted from the quoted comparison, closes the endpoint signs and magnitudes. A future modern calculation passes this test only when its total signed endpoint shifts and edge-resolved motions agree with declared experimental references within a complete uncertainty budget.

## Reproduction

```bash
python tools/analyze_laurenti1990_debye_waller_endpoint.py \
  --summary-json /tmp/laurenti1990_debye_waller_endpoint.json
```

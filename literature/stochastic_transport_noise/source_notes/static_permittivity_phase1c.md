# R06 Phase 1C static-permittivity source audit

**Program:** R06 — stochastic transport and finite-size noise  
**Controlling issue:** #346  
**Decision:** `STATIC_PERMITTIVITY_BENCHMARK_BRACKET_ACCEPTED_PRIMARY_ALLOY_FIT_LINEAGE_UNRESOLVED`

## 1. Quantity required by the transport model

The Poisson and electrostatic-screening equations require the low-frequency bulk relative permittivity

```text
epsilon_s
```

including lattice polarization.

This is distinct from:

- `epsilon_infinity`, the high-frequency bulk dielectric constant above the optical-phonon response;
- the optical dielectric function at interband energies;
- the dielectric constant of native oxide, anodic oxide, passivation, or encapsulation layers.

Those quantities are not interchangeable.

## 2. Primary evidence recovered

Baars and Sorger measured reststrahlen reflection spectra of `CdxHg1-xTe` single crystals over

```text
0 <= x <= 0.54
T = 77 K and 300 K
```

and analyzed the spectra by Kramers-Kronig integration. The mixed crystals exhibited two transverse optical modes with composition-dependent frequencies.

This source provides primary phonon and reststrahlen evidence suitable for Lyddane-Sachs-Teller consistency checks. It does not, in the recovered record, print the later quadratic alloy-permittivity polynomial.

## 3. Data-review lineage

Tong and Ravindra's 1993 optical-properties review plots the composition dependence of low- and high-frequency dielectric constants and states that these curves are average values for 77 and 300 K. Their reference for those composition data is:

> J. Brice and P. Capper, *Properties of Mercury Cadmium Telluride*, EMIS Datareviews Series No. 3, INSPEC, London (1987).

Tong and Ravindra separately compare the HgTe and CdTe dielectric ratios with Baars-Sorger optical-phonon frequencies through the Lyddane-Sachs-Teller relation.

The lineage is therefore:

```text
primary reststrahlen / phonon evidence
    -> compiled EMIS property data
    -> later review curves and device-model polynomials
```

The relevant Brice-Capper data-review page has not been recovered in equation-quality form.

## 4. Static polynomial variants

Two nearly identical static relations are widely reproduced:

```text
epsilon_s = 20.5 - 15.5*x + 5.7*x^2
```

and

```text
epsilon_s = 20.5 - 15.6*x + 5.7*x^2.
```

R06 does not choose one as source exact. For dimensionless and architecture-level electrostatic benchmarks, the accepted bracket is

```text
20.5 - 15.6*x + 5.7*x^2
    <= epsilon_s <=
20.5 - 15.5*x + 5.7*x^2
```

with midpoint

```text
epsilon_s,nominal = 20.5 - 15.55*x + 5.7*x^2.
```

The half-width is

```text
delta epsilon_s = 0.05*x.
```

This bracket represents coefficient-transcription and source-lineage ambiguity only. It is not a physical confidence interval.

At detector-relevant compositions:

| x | lower | nominal | upper |
|---:|---:|---:|---:|
| 0.17 | 18.01273 | 18.02123 | 18.02973 |
| 0.20 | 17.60800 | 17.61800 | 17.62800 |
| 0.21 | 17.47537 | 17.48587 | 17.49637 |
| 0.30 | 16.33300 | 16.34800 | 16.36300 |

## 5. High-frequency warning

The commonly reproduced high-frequency relation is

```text
epsilon_infinity = 15.2 - 15.6*x + 8.2*x^2.
```

At least one later secondary chapter prints `-5.6*x` instead. That is inconsistent with other later tables and with the expected CdTe endpoint.

R06 records this as a secondary-source typographical warning. The high-frequency relation is not used in the electrostatic closure and the `-5.6*x` form is not accepted.

## 6. Temperature boundary

Later sources state that no temperature dependence was observed within experimental resolution, but the underlying measurement uncertainty and source page have not been recovered.

R06 therefore does not authorize a general temperature-independent material law. The benchmark bracket may be used only at the explicitly supported 77 K and 300 K reference temperatures, with no interpolated or extrapolated temperature model.

## 7. Authorization

Authorized:

- the static polynomial bracket as a Tier B electrostatic benchmark;
- Poisson and screening sensitivity calculations within that bracket;
- Baars-Sorger primary phonon data for future LST reconstruction;
- source-lineage work on the Brice-Capper data review.

Not authorized:

- a source-exact static-permittivity relation;
- a physical uncertainty interval based only on the coefficient discrepancy;
- use of `epsilon_infinity` in Poisson's equation;
- use of oxide permittivity as bulk HgCdTe permittivity;
- predictive detector claims.

## 8. Next source work

1. Inspect the Brice-Capper pages underlying the composition curves.
2. Recover their primary references and tabulated values.
3. Reconstruct `epsilon_s` from primary reststrahlen data where possible.
4. Quantify real composition and temperature uncertainty.
5. propagate the accepted uncertainty through Debye screening and Poisson sensitivity.

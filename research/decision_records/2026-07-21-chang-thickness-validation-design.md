# Decision record: Chang thickness-pair validation design

**Date:** 2026-07-21  
**Issue:** #186  
**Status:** candidate controlling decision pending PR validation

## Decision

Predeclare the Chang external-validation experiment as a paired effective-thickness test of the exponential-tail cutoff law.

For two same-state tail cutoffs,

```text
Delta_E = -W ln(d2/d1)
W_hat   = -Delta_E / ln(d2/d1)
```

The validation must retain cutoff covariance, effective-thickness uncertainty, and any covariance between the cutoff difference and logarithmic thickness ratio.

## Selected synthetic design

Use the existing source-bounded sensitivity case:

```text
W   = 12 meV
d1  = 5 um
d2  = 20 um
r   = 4
```

The pair gives:

```text
Delta_E = -16.6355 meV
W_hat   = 12.0000 meV
```

and remains:

```text
2.99374 meV
```

above the lower source-energy bound.

## Source-domain result

For baseline cutoff `E1`, minimum authorized energy `E_min`, energy margin `m`, and tail width `W`, the maximum ratio is:

```text
r_max = exp[(E1-E_min-m)/W]
```

For the declared baseline:

```text
absolute r_max                5.13342
r_max with 2 meV margin       4.34535
r_max with 3 meV margin       3.99791
```

The ratio-4 pair uses:

```text
77.9% of the absolute maximum
92.1% of the 2 meV-margin maximum
```

Therefore the existing 5-to-20 um pair is retained as the recommended synthetic validation design. It is near the largest informative ratio that preserves a practical source-boundary margin.

## Precision decision

For equal independent cutoff uncertainties and exact thickness ratio, ratio 4 requires:

```text
target W precision   per-cutoff sigma
5%                   0.588 meV
10%                  1.176 meV
20%                  2.353 meV
```

With independent 2% effective-thickness uncertainties:

```text
target W precision   per-cutoff sigma
5%                   0.537 meV
10%                  1.152 meV
20%                  2.340 meV
```

The route acceptance target is initially set at:

```text
relative W uncertainty <= 10%
```

which requires approximately `1.15 meV` or better independent per-cutoff uncertainty when both effective thicknesses have 2% uncertainty.

## Covariance decision

Do not assume cutoff errors are independent.

At ratio 4 with 1 meV uncertainty per cutoff:

```text
rho_E = 0.0   relative W uncertainty  8.50%
rho_E = 0.8   relative W uncertainty  3.80%
```

A common energy calibration can cancel substantially in the paired difference. The source intake must preserve or estimate the cutoff covariance.

## Data-contract decision

Future source data must conform to:

```text
data/templates/chang_thickness_validation_dataset.schema.json
```

The contract keeps separate:

- effective optical thickness;
- physical thickness;
- cutoff energy and covariance;
- response criterion;
- branch classification;
- composition, temperature, and carrier state;
- source calibration and digitization provenance;
- same-specimen ownership of `W`, `b`, and amplitude.

The schema fixes:

```text
external_material_validation_authorized = false
```

until a route-specific source audit and validation PR explicitly change that state.

## Acceptance gates

A source pair is accepted for quantitative validation only when:

1. both measurements share one specimen state or a documented common material state;
2. the same response criterion applies;
3. effective thickness and uncertainty are available;
4. cutoff covariance is available or audibly estimated;
5. both crossings are on the exponential tail;
6. both energies lie inside the source-authorized interval with a declared margin;
7. composition, temperature, carrier state, and processing are preserved;
8. no parameter is silently transferred between specimens.

## Rejection gates

Reject the paired-tail validation when:

- only physical thickness is available without an effective-thickness model;
- branch classification is unknown;
- one crossing is intrinsic and the tail formula is still applied;
- the source-energy boundary is violated;
- covariance is discarded despite common calibration;
- `W`, `b`, or amplitude belong to another specimen;
- cutoff uncertainty cannot meet the declared precision target and no weaker claim is predeclared.

## Claim boundary

This decision does not:

- fit Chang Figure 2;
- identify a universal optimum thickness ratio;
- equate physical and effective thickness;
- establish external material validation;
- or authorize a source-specific parameter transfer.

## Next decision after merge

When the Chang papers or source data are obtained:

1. populate the future-data contract;
2. execute the source and specimen-ownership audit;
3. classify both crossings;
4. evaluate the paired estimator and covariance;
5. accept, weaken, or reject the validation claim under the predeclared gates.

# Camassel composition-accuracy envelope at 2 K

## Question

Can the discrepancy between published HgCdTe gap relations and Camassel et al. Table I be removed by the source-reported composition accuracy alone?

The calculation is deliberately not a fit. Each published model is evaluated over

```text
x_true in [x_reported - 0.005, x_reported + 0.005],
```

clipped to the physical interval `[0,1]`.

The `0.005` value is used as a deterministic source-accuracy sensitivity envelope. It is not interpreted as a Gaussian standard deviation, probability distribution, likelihood, or confidence interval.

## Source and observable

Camassel et al., *Physical Review B* **38**, 3948–3959 (1988), DOI `10.1103/PhysRevB.38.3948`, report exciton-conditioned gap observations at approximately 2 K.

Two measurement classes remain separate:

- reflectivity exciton-polariton gaps;
- absorption/derivative-absorption excitonic gaps.

No pointwise energy covariance is reported.

## Models evaluated

No coefficient is fitted.

1. Hansen 1982.
2. Laurenti 1990.
3. The provisional Hansen-Pade relation as a diagnostic.

The provisional relation changes only the temperature term and inherits Hansen's zero-temperature composition polynomial.

## Hansen domain boundary

Hansen's fitted composition evidence was approximately

```text
0 <= x <= 0.6
```

plus the CdTe endpoint. The source described the behavior above approximately `x=0.6` as conjectural.

The primary external within-domain Camassel checks are therefore the absorption-derived excitonic gaps at:

```text
x = 0.50
x = 0.55
```

The `x=0.62` row is treated as a boundary extrapolation diagnostic. Higher-composition rows are retained for descriptive comparison but are not presented as fair within-domain validation of Hansen.

## Within-domain result

| Reported x | Camassel gap | Hansen nominal residual | Hansen minimum absolute residual over x envelope |
|---:|---:|---:|---:|
| 0.50 | 0.6280 eV | +63.500 meV | 54.779646 meV |
| 0.55 | 0.7010 eV | +48.208 meV | 39.234326 meV |

Positive residual means

```text
Camassel observed gap - model prediction > 0.
```

Neither Hansen residual can reach zero anywhere inside the declared composition envelope.

The result is therefore not a nominal-composition artifact. Under the Camassel excitonic-gap definition, Hansen underpredicts both external within-domain observations by tens of meV even after the complete source-reported composition allowance is used.

## Provisional Hansen-Pade diagnostic

| Reported x | Minimum absolute residual over x envelope |
|---:|---:|
| 0.50 | 54.769089 meV |
| 0.55 | 39.118204 meV |

At 2 K, the provisional nonlinear thermal term is negligible. It does not repair the inherited static composition discrepancy.

This does not invalidate the low-temperature shape result from Seiler. It identifies the zero-temperature composition law as the controlling limitation when the model is transferred to the Camassel Cd-rich observations.

## Laurenti interpretation

Laurenti is descriptively closer:

```text
all-observation nominal MAE: 10.469 meV
Hansen nominal MAE:          39.578 meV
```

The comparison is not held out for Laurenti. Camassel belongs to the experimental lineage used to construct the later Laurenti Cd-rich relation.

The admissible statement is:

```text
Laurenti is descriptively consistent with its source lineage at the declared composition scale.
```

The inadmissible statement is:

```text
Camassel independently validates Laurenti over Hansen.
```

## Measurement-class dependence

Two specimens contain both optical modalities:

| Specimen | x | Reflectivity minus absorption gap |
|---|---:|---:|
| MCT49 | 0.88 | +2.0 meV |
| MCT47 | 0.78 | -17.5 meV |

The 17.5 meV same-specimen difference is larger than many proposed refinements to analytical gap equations. Reflectivity and absorption observations cannot be pooled as interchangeable independent gap measurements without an explicit observation model.

## Descriptive full-source metrics

These values are diagnostics, not weighted statistical rankings because the source reports no pointwise energy covariance and the two modalities are not independent for dual-modality specimens.

| Model | All-row MAE | Reflectivity MAE | Absorption MAE | Zero reachable within x envelope |
|---|---:|---:|---:|---:|
| Hansen 1982 | 39.578 meV | 22.221 meV | 54.455 meV | 1 / 13 observations |
| Laurenti 1990 | 10.469 meV | 9.428 meV | 11.361 meV | 6 / 13 observations |
| provisional Hansen-Pade | 39.430 meV | 22.341 meV | 54.078 meV | 1 / 13 observations |

The row count is not the number of independent specimens. MCT49 and MCT47 each contribute two correlated modality observations.

## Scientific decision

The bounded forward calculation supports the following narrow result:

```text
For the Camassel absorption-derived excitonic-gap observable at 2 K,
Hansen 1982 is incompatible with the independently microprobe-calibrated
x=0.50 and x=0.55 specimens across the complete source-reported
x +/- 0.005 composition-accuracy envelope.
```

It also shows that changing only the low-temperature thermal shape cannot resolve the discrepancy.

## Not established

This analysis does not establish:

- universal rejection of Hansen for every operational gap definition;
- independent validation of Laurenti;
- Gaussian significance, a p-value, or chi-square;
- that composition is the only uncertainty in Camassel Table I;
- an optimal replacement static composition law;
- production-equation status;
- manuscript or submission authorization.

## Reproduction

```bash
python tools/analyze_camassel1988_composition_envelope.py \
  --output-json /tmp/camassel-envelope.json \
  --output-csv /tmp/camassel-envelope.csv
```

The immutable compact decision record is

```text
validation/camassel1988_composition_envelope_reference.json
```

and all 39 observation-model evaluations are in

```text
validation/camassel1988_composition_envelope_records.csv
```

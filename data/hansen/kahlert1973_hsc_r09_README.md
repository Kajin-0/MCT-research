# Kahlert and Bauer 1973 HSC_R09 primary-source audit

## Source

H. Kahlert and G. Bauer, "Magnetophonon Effect in n-Type Hg1-xCdxTe (x = 0.212)," Physical Review Letters 30, 1211-1214 (1973), DOI 10.1103/PhysRevLett.30.1211.

The repository owner supplied the complete four-page article as `kahlert1973.pdf`. The observed binary SHA256 is:

```text
3052179e8d216de4d7ba015ef61e1ce73d193127602418075cf3c096fa09275a
```

The copyrighted PDF is not committed.

## Corrected measurement classification

Hansen 1982 groups HSC_R09 with magneto-optical gap evidence. The primary source is a magnetotransport study, not an optical absorption-edge experiment. It combines:

- low-temperature longitudinal Shubnikov-de Haas oscillations;
- longitudinal magnetoresistance versus magnetic field;
- temperature-dependent magnetophonon-resonance extrema from 50 to 130 K;
- a Kane nonparabolic-band model used to convert resonance positions into a temperature-dependent gap parameter.

The direct observations are magnetic-field positions of resistance extrema. The reported `Eg(T)` law is model-conditioned.

## Material and carrier state

The source describes n-type Cominco Hg1-xCdxTe with nominal `x=0.212`. It reports at 4.2 K:

```text
mobility              85,600 cm^2 V^-1 s^-1
carrier concentration 1.6e15 cm^-3
```

The carrier concentration was deduced from Hall and SdH measurements. The source says "samples" but provides no specimen identifiers or exact count. The audit therefore records one source-level sample population and does not invent a specimen. No composition uncertainty or independent composition method is reported in the article.

## Low-temperature SdH outputs

From SdH amplitude and extremum analysis the source reports:

```text
m*(0)/m0 = 0.005 +/- 0.0003
g*(0)    = -172 +/- 10
```

The Figure 1 calculation uses `Eg=0.093 eV`, spin-orbit splitting `Delta=0.96 eV`, and `EF=0.009065 eV`. These fixed calculation inputs are not assigned unreported covariance.

## Magnetophonon assignment

Figure 3 compares experimental resonance positions with two phonon branches:

```text
HgTe-like LO phonon  17.1 meV  accepted assignment
CdTe-like LO phonon  19.6 meV  unsuccessful fit
```

The experimental markers and theoretical curves remain distinct evidence layers. No dense curve or marker digitization is performed.

## Temperature-dependent gap model

The source assumes:

```text
Eg(T) = Eg0(1 + alpha T)
m*(T) = m*(0)(1 + alpha T)
Eg0   = 0.09 eV
alpha = 8.5e-3 K^-1
```

The best fit to the Figure 3 resonance positions gives the printed rounded result:

```text
dEg/dT = 7.6e-4 eV/K
```

The product of the separately printed parameters is `alpha*Eg0 = 7.65e-4 eV/K`. The audit preserves both the exact product and the rounded reported coefficient rather than forcing them to be numerically identical.

The paper compares this fitted value with a directly measured `3.5e-4 eV/K` coefficient in similar-composition alloys from its Ref. 18. That comparison is secondary-source context, not an additional observation from Kahlert and Bauer.

## Hansen ingestion boundary

The printed Kahlert relation yields at 80 K:

```text
Eg(80 K) from Eg0 and alpha       0.1512 eV
Eg(80 K) from rounded dEg/dT      0.1508 eV
```

Hansen does not expose source-labeled HSC_R09 markers and does not state whether it ingested the printed relation, a rounded 80 K conversion, selected Figure 3 points, or another transcription. Plot proximity is insufficient.

```text
controlling decision
primary_source_recovered_temperature_relation_reconstructed_hansen_marker_mapping_unresolved
```

Kahlert is part of Hansen's fitted lineage and cannot independently validate Hansen.

## Files

- `kahlert1973_hsc_r09_source_metadata.csv` - source and measurement identity.
- `kahlert1973_sample_population.csv` - source-level sample population without invented specimen IDs.
- `kahlert1973_model_parameters.csv` - source-reported fit outputs, inputs, and context.
- `kahlert1973_temperature_relation.csv` - exact printed model relation and uncertainty boundary.
- `kahlert1973_hansen_ingestion_candidates.csv` - plausible, unproven Hansen conversion conventions.
- `../validation/kahlert1973_hsc_r09_audit.json` - canonical deterministic audit.

## Prohibited interpretations

This audit does not support:

- direct optical-edge classification;
- pointwise gap measurements from the Figure 3 dots;
- pointwise statistical covariance;
- a known physical specimen count;
- exact Hansen per-marker assignment;
- independent validation of Hansen;
- a universal or production gap equation;
- a manuscript claim.

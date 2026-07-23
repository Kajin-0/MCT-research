# Elliott et al. 1972 HSC_R08 primary-source audit

## Source identity

```text
C. T. Elliott, John Melngailis, T. C. Harman,
J. A. Kafalas, and W. C. Kernan

Pressure Dependence of the Carrier Concentrations in p-Type
Alloys of Hg1-xCdxTe at 4.2 and 77 K

Physical Review B 5, 2985-2997 (1972)
DOI 10.1103/PhysRevB.5.2985
```

The repository owner supplied a 13-page PDF under the working filename `elliott1972.pdf`.

```text
SHA256
509bbcfd3c4b72312ab49ee2460e56561a9324e4e96af56dd29e8612b0b2b328
```

The copyrighted PDF is not committed.

## Corrected measurement class

Hansen 1982 grouped HSC_R08 with magneto-optical gap evidence. The primary article is instead a hydrostatic-pressure magnetotransport study of p-type Hg1-xCdxTe near the semimetal-semiconductor transition.

Measured quantities include:

- zero-field resistivity and low-field Hall coefficient versus pressure;
- Hall coefficient and transverse magnetoconductivity versus magnetic field;
- longitudinal magnetoconductivity and Shubnikov-de Haas oscillations;
- electron and hole concentrations and mobilities inferred from Hall and conductivity limits.

The gap values in Table II are not direct optical edges. They are signed zero-pressure gap parameters inferred from pressure-dependent electron concentrations using Kane k.p theory.

## Material and composition provenance

The three named sample identities are:

```text
7B    x = 0.149 +/- 0.005    annealed four days at 400 C in Hg vapor
7B1   x = 0.149 +/- 0.005    unannealed
8B    x = 0.138 +/- 0.005    unannealed
```

Composition was measured by electron microprobe. The reported `+/-0.005` is retained as the source accuracy statement and is not converted into pointwise Gaussian covariance.

The source describes crystal growth as a technique believed to involve mass-transport-induced growth and simultaneous temperature-gradient annealing in a vertical ampoule.

Figure 8 states that the 7B pressure series contains results from two physical specimens under one shared sample identity. Therefore the article contains three named identities but at least four physical specimens. The two 7B specimens are not separately named and are not invented in the ledger.

## Pressure and field protocol

Hydrostatic helium pressure covered approximately 0-9 kbar. At 4.2 K the helium solidified. The authors discuss a possible pressure decrease during cooling and explicitly choose to treat the bomb pressure as the externally maintained pressure. They do not provide a pointwise pressure uncertainty, so none is manufactured here.

The article reports 77 K and 4.2 K carrier measurements, with longitudinal magnetoconductivity examples at 1.3 and 4.0 K. Figures extend to magnetic fields as high as 70 kG, but a single global maximum-field specification is not stated for every specimen and protocol.

## Direct source summaries

### Table I

`elliott1972_table1_carriers.csv` transcribes the exact carrier concentrations and mobilities printed in Table I. The 7B hole values at 77 K are explicitly footnoted as high-pressure limiting values for `P > 5 kbar`, despite the table's atmospheric-pressure heading. They are not relabeled as zero-pressure hole observations.

### Table II

`elliott1972_table2_gap_candidates.csv` transcribes the exact source-model outputs:

```text
sample   T (K)   x                 EF (meV)   E0 (meV)
7B       4.2     0.149 +/- 0.005    9         -16
7B1      4.2     0.149 +/- 0.005   16         -10
8B       4.2     0.138 +/- 0.005   20         -33
7B       77      0.149 +/- 0.005   23          -8   for mh*=0.3 m0
7B       77      0.149 +/- 0.005   31          +2   for mh*=0.7 m0
```

The 77 K values are a sensitivity pair, not two independent observations.

## Source-reported model parameters

```text
dEg/dP                    7.0e-6 eV/bar
                           7.0e-3 eV/kbar
Kane matrix element PK    8.4e-8 eV cm
heavy-hole mass range     0.3-0.7 m0
deformation potential     3.3 eV
```

The Kane matrix element is inherited from earlier magnetoreflection work and held fixed. The source does not report a modern fit covariance for the inferred gap parameters.

## Source interpretation boundary

The authors report pressure-independent Fermi-level positions at 4.2 K and propose an acceptor/impurity-band model. The approximately 9 meV acceptor level in 7B and approximately 20 meV impurity-band energy in the as-grown samples are source interpretations, not independent direct observations.

Magnetic freeze-out is attributed to the lowest-energy, spin-split, zero-order Landau level passing through the Fermi energy. Non-Ohmic behavior during freeze-out is reported but not fully explained.

## Hansen ingestion boundary

The source-native numerical candidates are reconstructed exactly from Table II. For the same named 7B sample, two 4.2-to-77 K pairings are possible because the 77 K result depends on the assumed heavy-hole mass:

```text
mh*=0.3 m0   slope = 1.0989011e-4 eV/K
mh*=0.7 m0   slope = 2.4725275e-4 eV/K
```

Hansen does not expose per-marker source labels or identify which 77 K sensitivity value was ingested. Plot proximity is not used to force an assignment.

```text
controlling decision
primary_source_recovered_source_native_gap_candidates_reconstructed_hansen_marker_mapping_unresolved
```

Elliott is part of Hansen's fitted lineage and cannot independently validate Hansen.

## Claim boundary

Supported:

- exact source identity, page range, and source hash;
- corrected pressure-magnetotransport measurement class;
- exact named sample, composition, anneal, Table I, and Table II records;
- exact source-reported pressure coefficient and model assumptions;
- explicit source-native Hansen candidates and pairing ambiguity.

Not supported:

- pointwise pressure covariance;
- unreported specimen identifiers for the two 7B physical specimens;
- digitization of fitted curves or dense figure traces;
- replacement of source analysis with regression on rounded plot coordinates;
- exact HSC_R08 per-marker mapping;
- independent Hansen validation;
- a universal or production gap relation;
- a manuscript claim.

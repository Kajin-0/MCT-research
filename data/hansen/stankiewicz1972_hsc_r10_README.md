# Stankiewicz and Giriat 1972 HSC_R10 primary-source audit

## Source

J. Stankiewicz and W. Giriat, "Pressure and Temperature Dependence of the Energy Gap in CdxHg1-xTe," *physica status solidi (b)* **49**, 387-393 (1972), DOI `10.1002/pssb.2220490136`.

The repository owner supplied the complete seven-page article as `stankiewicz1972.pdf`. The observed binary SHA256 is:

```text
d48d5312fbd3de5e90a95eab695c7cf1e0b86a9e528f7c1035978abc4993245e
```

The copyrighted PDF is not committed.

## Corrected measurement classification

Hansen 1982 groups HSC_R10 with magneto-optical evidence. The primary source is not an optical experiment. It reports Hall-coefficient measurements under hydrostatic pressure and temperature, followed by a model inversion for the signed zero-pressure gap.

Direct observations are:

- Hall coefficient versus temperature;
- Hall coefficient versus hydrostatic pressure at fixed temperatures;
- measurements at 300 Oe;
- temperatures from 77 to 295 K;
- pressures up to 10,000 atm.

The Table 1 gaps and coefficients are outputs of a numerical fit to a simplified Kane/Groves-Paul carrier model. They are model-conditioned, not direct optical edges.

## Material and specimen provenance

Four specimens are explicitly reported, identified in the paper only by composition:

```text
x = 0.070 +/- 0.005
x = 0.095 +/- 0.005
x = 0.130 +/- 0.005
x = 0.180 +/- 0.005
```

The crystals were prepared from HgTe and CdTe by a modified vertical melted-zone technique. Composition was determined by density measurements. Homogeneity was checked by measuring Hall coefficient along each sample and by electron microprobe analysis.

Repository record IDs are audit surrogates. They are not source-native specimen names.

## Source model

The source calculates intrinsic carrier concentration using a simplified Kane nonparabolic conduction-band model and a Boltzmann hole expression. For the inverted regime it substitutes `Eg -> |E0|`.

Fixed assumptions are:

```text
Kane matrix element Ep       18 eV
hole effective mass          0.55 m0
overlap energy Delta epsilon 0
samples                      treated as intrinsic
```

The fixed quantities were taken as pressure- and temperature-independent. The authors explicitly warn that the samples were not perfectly intrinsic and showed hole influence, especially at low temperature and high pressure. They also state that model assumptions can add error beyond the reported measurement errors.

## Table 1 reconstruction

Table 1 gives signed zero-pressure gap values and fitted coefficients for four specimens:

```text
x       E0(77 K)       E0(280 K)      dE0/dp               dE0/dT
        eV             eV             eV/atm                eV/K
0.070  -0.122 +/- .006 -0.035 +/- .006  9.5e-6 +/- 0.5e-6   4.4e-4 +/- 0.5e-4
0.095  -0.096 +/- .006 -0.008 +/- .006 10.5e-6 +/- 0.5e-6   4.3e-4 +/- 0.5e-4
0.130  -0.035 +/- .006  0.049 +/- .006  9.6e-6 +/- 0.5e-6   4.0e-4 +/- 0.5e-4
0.180   0.042 +/- .006  0.117 +/- .006  8.5e-6 +/- 0.5e-6   3.8e-4 +/- 0.5e-4
```

The source says shifting a fitted gap by `+/-6 meV` produced a noticeably poorer fit. No pointwise fit covariance or cross-specimen covariance is reported.

## Source empirical relation

For `x < 0.2`, the paper prints Equation 4:

```text
E0(x,T) = -0.303 + 1.91 x + 5.25e-4 (1-2x) T  eV
```

The relation is a source empirical synthesis using the small-x linearity assumption and an HgTe endpoint. It is separate from the four Table 1 specimen records. The paper states that the `x=0.18` result is an exception to the agreement shown in Figure 6.

## Evidence layers retained separately

1. Direct Hall-coefficient curves in Figures 1-5.
2. Model-conditioned Table 1 gaps and coefficients.
3. The source-level empirical Equation 4.
4. Hansen's later global empirical equation.

No Hall curves or Figure 6 markers are digitized. No covariance is inferred from graphical scatter.

## Hansen ingestion boundary

The source exposes eight tabulated gap values and a complete empirical relation. Hansen does not expose source-labeled HSC_R10 markers or state whether it ingested:

- all or a subset of the Table 1 values;
- values generated from Equation 4;
- Figure 6 markers;
- another transcription.

The candidate ledger preserves the eight exact Table 1 values and the existence of the Equation 4 family without assigning any candidate to a Hansen marker.

```text
controlling decision
primary_source_recovered_table1_and_equation4_reconstructed_hansen_marker_mapping_unresolved
```

Stankiewicz and Giriat belong to Hansen's fitted lineage and cannot independently validate Hansen.

## Claim boundary

Supported:

- exact source identity, page range, DOI, and supplied-file hash;
- corrected hydrostatic-pressure Hall-transport classification;
- four composition-defined specimen records and source preparation/provenance;
- exact Table 1 gaps, pressure coefficients, temperature coefficients, and reported half-widths;
- exact Equation 4 relation and stated domain;
- explicit source limitations and unresolved Hansen ingestion mapping.

Not supported:

- direct optical-gap classification;
- pointwise Hall-curve reconstruction;
- modern fit covariance;
- exact Hansen marker assignment;
- independent validation of Hansen;
- a production gap relation;
- a manuscript claim.

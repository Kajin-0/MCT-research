# R01 state addendum: Antcliffe 1970 HSC_R07 primary-source audit

**Date:** 2026-07-23  
**Program:** R01 - empirical bandgap reconstruction  
**Issue:** #301  
**Hansen graph identity:** HSC_R07

## Precedence

This addendum supersedes the earlier fail-closed Antcliffe acquisition statement in this same branch. It modifies only the Antcliffe HSC_R07 source state and does not replace any other R01 source history, model result, uncertainty contract, or roadmap decision.

## Source recovery

```text
primary full text             recovered from user upload
article pages                 345-351
working filename              antcliffe1970.pdf
PDF pages                     7
source PDF SHA256
43743f5f12598b0f7987be6fa1df2199f52b845b3c163189ac93d8d811901240
copyrighted binary committed  false
```

## Correct source classification

```text
primary technique
Shubnikov-de Haas oscillatory magnetoresistance

primary gap observable
Kane two-band interaction gap inferred from
effective-mass nonparabolicity

separate optical observable
50% relative photoconductive response threshold
```

Hansen's generic magneto-optical classification is too coarse for the primary paper. The source combines a magnetotransport-derived interaction-gap parameter with separate photoconductive threshold information.

## Material and specimen state

```text
material                       n-type single-crystal Hg0.796Cd0.204Te
growth                         solid-state recrystallization
nominal x                      0.204
reported spatial x variation  +/-0.003 over 10 mm
transport temperatures        1.5-4.2 K
optical threshold states      4.2 K and 77 K
maximum magnetic field        20 kG
Table I specimens             6
additional named figures      2
complete sample count         not reported
```

The composition half-width is a spatial source-ingot variation, not a Gaussian absolute-composition sigma.

## Numerical evidence

The six exact Table I rows preserve periodicity, carrier concentration, effective mass, Fermi energy, observed splitting ratio, and `g`.

Source-reported fit:

```text
m0*/m0   = 5.60 +/- 0.25 e-3
Ep       = 17 +/- 1.4 eV
Eg       = 0.0635 +/- 0.008 eV
g0       = 164 +/- 16
```

Optical threshold evidence:

```text
77 K wavelength                      13.7 +/- 0.5 um
77 K derived central cutoff energy   0.0904994 eV
4.2 K source gap proxy               0.0665 +/- 0.002 eV
```

## Reproduction boundary

An ordinary least-squares reconstruction from the rounded six Table I summaries under the source's small-mass A4 approximation gives approximately:

```text
m0*/m0   = 0.00509808
Ep       = 15.1277 eV
Eg       = 0.05168 eV
```

It does not exactly reproduce the source-reported fit. The source values remain authoritative because the approximately fifteen underlying mass determinations per specimen, weighting, and covariance are not printed. The repository preserves both layers and does not silently substitute one for the other.

## Hansen mapping

Two source-supported low/high-temperature pairings remain plausible:

```text
4.2 K photoconductive proxy -> 77 K photoconductive threshold
slope = 3.29662e-4 eV/K

4.2 K SdH interaction gap -> 77 K photoconductive threshold
slope = 3.70871e-4 eV/K
```

Hansen does not label source-specific plot markers, so exact HSC_R07 ingestion remains unresolved.

Antcliffe is part of Hansen's fitted lineage and is not independent validation.

## Controlling decision

```text
primary_source_recovered_hansen_ingestion_mapping_unresolved
```

## Authorization state

```text
primary identity and source hash                    validated
method and material provenance                      validated
six-row Table I transport ledger                    validated
source-reported band parameters                     validated
photoconductive threshold ledger                    validated
rounded-table deterministic audit                   validated
HSC_R07 primary measurement classification          corrected
exact Hansen source-specific marker mapping         unresolved
independent Hansen validation                       not authorized
pointwise covariance                                unavailable
new equation or manuscript claim                    not authorized
```

## Roadmap consequence

Issue #301 is complete as a primary-source audit once this branch is merged. Reopening the HSC_R07 ingestion question requires a source-native Hansen fitting ledger, explicitly source-labeled Hansen markers, or another traceable record of the value pairing used for Antcliffe. Plot proximity alone is insufficient.

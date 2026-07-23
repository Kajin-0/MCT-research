# Antcliffe 1970 HSC_R07 primary-source audit

## Exact source identity

```text
G. A. Antcliffe
Effective Mass and Spin Splitting in Hg1-xCdxTe
Physical Review B 2, 345-351 (1970)
Published 15 July 1970
DOI 10.1103/PhysRevB.2.345
```

The user supplied a seven-page primary PDF. The copyrighted binary is not committed.

```text
working filename
antcliffe1970.pdf

source PDF SHA256
43743f5f12598b0f7987be6fa1df2199f52b845b3c163189ac93d8d811901240
```

## Correct measurement classification

Hansen 1982 lists Antcliffe among its magneto-optical sources. The primary paper itself is a low-temperature **Shubnikov-de Haas magnetotransport** study, not a magnetoreflectance or magnetoabsorption experiment.

The central transport observable is the temperature dependence and magnetic-field periodicity of oscillatory magnetoresistance. Antcliffe uses those measurements with a Kane two-band model to infer an interaction-gap parameter from conduction-band nonparabolicity.

The paper separately reports photoconductive 50% relative-response threshold information. These optical detector-response values are not the same observable as the Shubnikov-de Haas interaction-gap fit.

## Material and experimental contract

```text
material                         n-type single-crystal Hg0.796Cd0.204Te
growth                           solid-state recrystallization
doping                           random unknown trace impurities
nominal x                        0.204
reported x variation             +/-0.003 over 10 mm
composition methods              relative spectral response
                                 Cd-115 radioactive tracer analyses
sample dimensions                approximately 10 x 2 x 0.5 mm
contacts                         indium solder after bromine-methanol etch
carrier concentration            2e15 to 1e16 cm^-3
mobility, low concentration      greater than 2e5 cm^2/V s
mobility near 1e16 cm^-3         greater than 1e5 cm^2/V s
transport temperature range      1.5 to 4.2 K
reported optical threshold T     4.2 and 77 K
maximum magnetic field           20 kG
usual geometry                   H perpendicular to current
```

The `+/-0.003` composition statement is a spatial variation over the source ingot. It is not encoded as a Gaussian one-sigma absolute-composition error.

The source reports less than 10% carrier-concentration variation over 0.5 mm in the best samples, residual microinhomogeneity below 10 mil in low-density material, and a Fermi surface spherical to approximately `+/-2%`.

## Specimen registry

The complete number of specimens examined is not reported.

The numerically tabulated Table I set contains six specimens:

```text
Q228-9
Q270-22
Q190-15
Q269-11
Q269-30
Q193-19
```

Two additional named figure examples are preserved without promoting them into the Table I fit:

```text
Q224-25   Figure 1 inhomogeneity example
Q115-15   Figures 2-3 spin-splitting example
```

For Q224-25, region B is explicitly rejected as unreliable because of inhomogeneity. Q115-15 carries exact figure labels of `n=3.3e15 cm^-3` and `Delta(1/H)=1.43e-4 Oe^-1`, but it is not one of the six tabulated fit rows.

## Table I reconstruction

The exact six-row table is stored in `antcliffe1970_specimens.csv`.

| Sample | Delta(1/H), 1e-4 Oe^-1 | n, 1e15 cm^-3 | m*/m0, 1e-3 | EF, meV | delta_expt | g |
|---|---:|---:|---:|---:|---:|---:|
| Q228-9 | 1.80 | 2.32 | 7.02 | 8.0 | 0.48 | 137 |
| Q270-22 | 1.50 | 3.10 | 7.55 | 11.0 | 0.45 | 119 |
| Q190-15 | 0.98 | 5.90 | 8.30 | 15.2 | 0.48 | 115 |
| Q269-11 | 0.90 | 6.60 | 9.10 | 19.7 | 0.45 | 99 |
| Q269-30 | 0.81 | 8.00 | 9.20 | 20.4 | 0.47 | 100 |
| Q193-19 | 0.645 | 9.66 | 9.66 | 23.0 | 0.44 | 93 |

The paper states that about fifteen effective-mass determinations were averaged to obtain each reported mass summary. Those underlying measurements are not printed.

## Source-reported band parameters

The Figure 5 fit and text report:

```text
band-edge mass ratio m0* / m0       5.60 +/- 0.25 e-3
interband matrix element Ep         17 +/- 1.4 eV
Kane interaction gap Eg             0.0635 +/- 0.008 eV
band-edge electron g factor         164 +/- 16
preferred N=1 delta_expt            0.46 +/- 0.02
Fermi-shift corrected delta         0.44
spin-orbit splitting Delta          0.75 eV
```

The fit-parameter covariance is not reported. The mass, `Ep`, and `Eg` values are therefore not treated as independent measurements.

Figure 5 states that all experimental mass-ratio error bars are `+/-5%`.

## Rounded-table reproduction boundary

The repository independently applies the source's small-mass approximation to the rounded Table I values:

```text
fit ordinate                    (m*/m0)^2
fit abscissa                    [Delta(1/H)]^-1
source A4 coefficient           6.90e-8 / Ep
```

This produces approximately:

```text
band-edge mass ratio            0.00509808
Ep                              15.1277 eV
interaction gap                 0.05168 eV
```

These values do **not** exactly reproduce the source-reported `0.00560`, `17 eV`, and `0.0635 eV`.

This discrepancy does not authorize replacement of the source values. Table I contains rounded averages, while the paper does not expose the underlying mass determinations, fit weighting, regression covariance, or complete fitting record. The source-reported parameters and the rounded-table reproduction are retained as separate evidence layers.

Figure 5 is not digitized because its six plotted observations duplicate Table I and its curve is a source fit.

## Photoconductive threshold observations

At `77 K`, the paper reports:

```text
50% relative spectral-response wavelength
lambda = 13.7 +/- 0.5 um
```

The quoted range includes data from many ingots. It is not identified as a Gaussian standard deviation.

Using `hc = 1.2398419843320026 eV um`, the repository-derived central cutoff energy is:

```text
E50(77 K) = 0.0904994 eV
deterministic wavelength interval = [0.0873128, 0.0939274] eV
```

At `4.2 K`, the source states that the threshold wavelength increases by a factor of `1.37` and reports:

```text
Eg^p = 0.0665 +/- 0.002 eV
```

The wavelength ratio independently implies `0.0660580 eV`, which lies within the source-reported interval.

Antcliffe states that the true gap should differ from this photoconductive proxy by no more than the approximately `4 meV` Fermi energy of the low-concentration photoconductive samples. This is a source-level physical bound, not a pointwise covariance model.

## Hansen lineage and unresolved ingestion mapping

Hansen 1982 classifies Antcliffe as fitted magneto-optical evidence, but does not label individual Figure 1 or Figure 2 markers by source.

Antcliffe exposes three relevant low- and high-temperature quantities:

```text
77 K photoconductive threshold energy       0.0904994 eV, repository-derived
4.2 K photoconductive gap proxy             0.0665 +/- 0.002 eV
low-temperature SdH Kane interaction gap     0.0635 +/- 0.008 eV
```

Two plausible source-pairing reconstructions are therefore retained:

```text
photoconductive pair slope
(0.0904994 - 0.0665)/(77 - 4.2)
= 3.29662e-4 eV/K

SdH-to-photoconductive pair slope
(0.0904994 - 0.0635)/(77 - 4.2)
= 3.70871e-4 eV/K
```

Both normalize to approximately `0.0915-0.0916 eV` at `80 K`. Hansen's equation gives `0.0904120 eV` at `x=0.204`, `80 K`.

The exact Antcliffe value or pairing ingested by Hansen cannot be proven because Hansen does not provide per-marker source labels or an observation ledger. The repository therefore records:

```text
Hansen exact source-specific ingestion mapping = unresolved
```

No Hansen point is reverse-engineered from plot proximity.

## Descriptive Hansen comparison

At `x=0.204`, Hansen 1982 gives:

```text
T = 4.2 K     0.0664047 eV
T = 77 K      0.0894619 eV
T = 80 K      0.0904120 eV
```

These values are numerically close to Antcliffe's reported and reconstructed quantities. This is descriptive only. Antcliffe is part of Hansen's fitted source lineage and cannot independently validate Hansen.

## Artifact controls

The source identifies two experimental artifacts explicitly:

1. **Carrier/composition inhomogeneity.** It can introduce a second oscillatory component, broaden Landau levels, and create spurious splitting.
2. **Electron heating from dc bias.** At fields near `20 mV/cm`, the inferred mass increased with magnetic field because the electron temperature exceeded the lattice temperature. Reducing the bias removed the effect.

These controls are retained as source evidence, not generalized into new numerical corrections.

## Direct observations versus curves

```text
Table I rows                         directly transcribed
Figure 2/3 exact labels              retained as figure metadata
Figure 1 region quality              retained qualitatively
Figure 4 traces                      not digitized
Figure 5 six points                  not digitized; duplicate Table I
Figure 5 least-squares curve         not sampled
underlying approximately 15 masses   unavailable
pointwise covariance                 unavailable
```

## Controlling decision

```text
primary_source_recovered_hansen_ingestion_mapping_unresolved
```

Supported:

- exact primary-source identity and SHA256;
- source method, specimens, composition provenance, temperature and field protocol;
- six Table I transport summaries;
- source-reported band parameters and stated error semantics;
- photoconductive threshold observations;
- deterministic rounded-table and wavelength checks;
- correction of HSC_R07 from unspecified magneto-optical evidence to Shubnikov-de Haas magnetotransport;
- explicit Hansen-lineage ambiguity.

Not supported:

- an exact source-by-source Hansen marker assignment;
- replacement of source fit values with the rounded-table regression;
- pointwise Gaussian covariance;
- digitization of duplicate or fitted curves;
- independent validation of Hansen;
- a universal gap equation;
- a production relation or manuscript claim.

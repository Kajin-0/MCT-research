# R06 Phase 1C — HgCdTe Kane material-evidence recovery

**Date:** 2026-07-25  
**Controlling issue:** #346  
**Gate:** PR #385 external material-evidence contract  
**Result:** candidate sources recovered; no material point accepted

## 1. Purpose

PR #385 requires at least three positive uncertainty-bearing HgCdTe points from
at least two provenance groups, spanning at least two temperatures, with:

- one absolute scale observable (`density_cm3` or
  `compressibility_cm3_per_ev`);
- one scale-free or matched shape observable (`generalized_einstein_factor`, or
  density and compressibility at one condition);
- independently known reduced chemical potential `eta`, or a separately
  validated neutrality model.

This recovery pass searched for evidence that could satisfy those requirements.
It did not fit `N_*` or `alpha` and did not authorize material prediction.

## 2. Recovery methods

The pass used:

- the existing repository source ledger and R06 source notes;
- DOI and exact-title searches;
- official NIST publication pages and the open 1991 NIST proceedings PDF;
- institutional publication records from Technion;
- the open Nature Communications 2016 HgCdTe magneto-optical article;
- targeted searches for HgCdTe intrinsic density, Hall carrier concentration,
  chemical compressibility, thermodynamic density of states, quantum
  capacitance, and generalized Einstein measurements.

A source was not promoted from a model curve to an experimental point, and an
abstract formula was not treated as a point-level uncertainty-bearing dataset.

## 3. Direct intrinsic-density evidence

### 3.1 Nemirovsky and Finkman 1979

**Citation:** Y. Nemirovsky and E. Finkman, *Journal of Applied Physics* **50**,
8107–8111 (1979), DOI `10.1063/1.325950`.

The institutional abstract reports that intrinsic carrier concentration was
measured for:

```text
0.205 <= x <= 0.22,
x = 0.29,
approximately 150 K to 320 K.
```

The measurements were based on Hall data from uncompensated, characterized
samples. Photoconductive response and infrared transmittance were also used to
check composition and sample uniformity.

This is the strongest direct density source recovered in the pass. It is not yet
countable under PR #385 because the following were not recovered at point level:

- sample-by-sample density values;
- standard uncertainties;
- composition uncertainties;
- compensation and Hall-inversion details;
- a chemical-potential value or an independently validated neutrality mapping
  compatible with the R06 closure.

The abstract-reported analytic expression remains a historical fit. It must not
be converted silently into point uncertainties or into project-defined
simplified-Kane parameters.

### 3.2 Finkman 1983

**Citation:** E. Finkman, *Journal of Applied Physics* **54**, 1883–1886
(1983), DOI `10.1063/1.332241`.

The abstract reports temperature-dependent carrier concentration derived from
Hall coefficient measurements in the near-intrinsic region. A Kane-model fit was
used to infer:

- the band-gap relation;
- Kane's interband coupling;
- the heavy-hole effective-mass ratio;
- modified intrinsic carrier concentrations.

This is primary experimental parameter-inversion evidence, but it is not yet a
usable PR #385 observation set. The full sample grid, Hall points, point
uncertainties, compensation assumptions, fitted equations, and covariance have
not been recovered. The fitted historical Kane parameters also cannot be mapped
directly onto the independent project parameter `alpha` without a new derivation.

## 4. Primary calculated intrinsic-density sources

### 4.1 Hansen and Schmit 1983

**Citation:** G. L. Hansen and J. L. Schmit, *Journal of Applied Physics* **54**,
1639–1640 (1983), DOI `10.1063/1.332153`.

The source reports a Kane nonparabolic calculation using measured heavy-hole
mass and band gap, followed by the analytic fit already implemented as the
bounded R06 benchmark. The abstract-reported domain is:

```text
Eg > 0,
50 K < T < 300 K,
x < 0.7.
```

The fit is reported within 1% of the underlying calculation and within 15% of
experimental Hall-derived intrinsic density.

This source remains a useful model benchmark. It is not an independent set of
uncertainty-bearing experimental points and supplies neither chemical
compressibility nor generalized Einstein measurements.

### 4.2 Seiler, Lowney, Littler, and Yoon 1991

**Citation:** D. G. Seiler, J. R. Lowney, C. L. Littler, and I. T. Yoon,
*Materials Research Society Symposium Proceedings* **216**, 59–63 (1991),
DOI `10.1557/PROC-216-59`; official NIST publication 22086.

The open NIST paper reports calculations over:

```text
0.17 <= x <= 0.30,
4 K <= T <= 300 K.
```

The calculation uses:

- a three-band Kane conduction model;
- full Fermi–Dirac conduction statistics;
- a nondegenerate heavy-hole band;
- Newton iteration for intrinsic neutrality;
- split-off energy `Delta = 1 eV`;
- momentum matrix element `P = 8.49e-8 eV cm`;
- heavy-hole mass `m_hh = 0.55 m0`.

The paper also reports magneto-absorption band-gap checks at compositions near
`x = 0.201` and `x = 0.229`. Intrinsic-density curves are shown for `x = 0.17`
and `x = 0.22`.

The intrinsic-density curves are model outputs, not independent density
measurements. They are not tabulated, do not carry point uncertainty, and do not
report the solved Fermi energy at each point. Equations (2)–(4) remain corrupted
in the PDF text layer and require visual symbol-level transcription before any
replication claim.

Digitized curves may later serve as historical model-regression targets. They
must not count as independent material observations.

### 4.3 Lowney, Seiler, Littler, and Yoon 1992

**Citation:** J. R. Lowney, D. G. Seiler, C. L. Littler, and I. T. Yoon,
*Journal of Applied Physics* **71**, 1253–1258 (1992), DOI
`10.1063/1.351371`.

The journal article is the final nonlinear-gap intrinsic-density calculation.
The required fitted coefficients and point-level numerical references were not
recovered in this pass. It shares the NIST calculation lineage with the 1991
precursor and therefore cannot be counted as a second independent experimental
provenance group.

## 5. Independent band-structure adequacy evidence

### Teppe et al. 2016

**Citation:** F. Teppe et al., *Nature Communications* **7**, 12576 (2016),
DOI `10.1038/ncomms12576`.

The open primary paper reports far-infrared magneto-spectroscopy on bulk-like
HgCdTe layers with approximately:

```text
x = 0.155 and x = 0.175,
2 K to 120 K.
```

A simplified Kane analysis gives a velocity of

```text
(1.07 +/- 0.05) x 10^6 m/s
```

across the studied range and reports a band gap of approximately `5 +/- 2 meV`
for one sample at 2 K.

This is uncertainty-bearing, independent HgCdTe band-structure evidence. It is
not a PR #385 density, compressibility, or generalized-Einstein observation. It
is therefore retained only for the later decision between a restricted
simplified dispersion and a full three-band model.

No direct mapping from the reported velocity and rest mass to the project inputs
`N_*` and `alpha` is authorized without a source-grounded derivation and a
consistent neutrality model.

## 6. Missing observation classes

This pass recovered no direct HgCdTe measurements of:

- chemical compressibility `dn/dmu`;
- thermodynamic density of states suitable as `dn/dmu`;
- generalized Einstein factor;
- a matched density/compressibility pair at one material condition.

This is a recovery result, not a claim that such measurements do not exist.
Targeted searches should continue using terms such as quantum capacitance,
thermodynamic density of states, magnetocapacitance, electrochemical potential,
and generalized Einstein relation in HgCdTe.

## 7. Evidence-contract assessment

The candidate pool fails the PR #385 gate because:

1. zero point-level density or compressibility observations have both recovered
   values and positive standard uncertainties;
2. no shape observable has been recovered;
3. no candidate density point has independently known `eta`;
4. no separately validated heavy-hole/split-off-band neutrality model is
   available;
5. model curves cannot be mixed with experimental Hall data as independent
   observations;
6. the open band-structure evidence is indirect with respect to `N_*` and
   `alpha`.

The machine-readable status therefore remains:

```text
blocked_no_accepted_hgcdte_reference_set
```

## 8. Priority recovery sequence

1. Obtain the full primary Nemirovsky–Finkman 1979 article and transcribe the
   Hall-derived intrinsic-density points, sample metadata, and uncertainty
   information.
2. Obtain the full primary Finkman 1983 article and transcribe the measured Hall
   data, fitted band parameters, assumptions, and covariance or error estimates.
3. Visually transcribe Seiler et al. 1991 equations (2)–(4); digitize its curves
   only as historical model benchmarks.
4. Search specifically for direct compressibility or generalized-Einstein
   evidence.
5. Derive, from primary Kane theory, whether the Teppe velocity/gap measurements
   constrain the simplified project parameterization or instead demonstrate the
   necessity of a fuller band model.
6. Keep parameter fitting, screening, detector coupling, and predictive noise
   blocked until the evidence contract passes.

# R06 intrinsic-density equation recovery audit - 2026-07-24

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Gate type:** primary-source provenance before material-model implementation

## 1. Decision summary

The source search narrows the intrinsic-density gap but does not close it.

Recovered with primary or official support:

- the official NIST distribution and complete prose context for the 1991 Seiler-Lowney-Littler-Yoon precursor;
- the exact nonlinear gap relation used by that precursor;
- the Kane three-band architecture, parameter choices, neutrality solve, integration-by-parts strategy, and final density-evaluation sequence;
- the bibliographic identity of the earlier Madarasz-Szmulowicz-McBath Kane calculation;
- the relationship between that earlier calculation, the later Fermi-Dirac extension, and the Lowney nonlinear-gap work.

Not recovered at symbol-exact quality:

- a reliable transcription of the 1991 precursor Eqs. (2)-(4);
- the printed equations of the 1985 Fermi-Dirac paper;
- the final fitted intrinsic-density coefficients reported in the 1992 Lowney journal paper;
- numerical reference tables sufficient to validate a source-exact implementation.

Therefore a material-accurate HgCdTe intrinsic-density implementation remains unauthorized.

## 2. Source lineage

### 2.1 Madarasz, Szmulowicz, and McBath (1985)

**Title:** Intrinsic carrier concentrations and effective masses in Hg1-xCdxTe  
**Authors:** F. L. Madarasz, F. Szmulowicz, J. R. McBath  
**Journal:** Journal of Applied Physics 58, 361-365  
**DOI:** `10.1063/1.335685`

This paper is the earlier Kane calculation referred to by the later Fermi-Dirac extension. Available primary metadata and abstract-level records establish that it:

- calculates intrinsic carrier concentration and effective masses;
- retains the Kane band structure without further analytical band approximations;
- compares against Hansen-Schmit;
- reports increasing disagreement at larger alloy composition.

The equation set itself has not been recovered at implementation quality.

### 2.2 Madarasz and Szmulowicz (1985)

**Title:** Intrinsic carrier concentrations in Hg1-xCdxTe with the use of Fermi-Dirac statistics  
**Journal:** Journal of Applied Physics 58, 2770-2772  
**DOI:** `10.1063/1.335868`

This paper extends the earlier calculation to full Fermi-Dirac statistics. Its abstract establishes:

- Fermi-Dirac statistics are required for the narrow-gap `x<0.20` regime;
- Boltzmann and Fermi-Dirac results agree well for `x>=0.20`;
- the Kane momentum matrix element is composition and temperature dependent;
- no extra band-structure approximation is introduced beyond the Kane theory.

No source-exact transcription is authorized from the abstract alone.

### 2.3 Seiler, Lowney, Littler, and Yoon (1991)

**Title:** Intrinsic Carrier Concentrations in Long Wavelength HgCdTe Based on the New, Nonlinear Temperature Dependence of Eg(x,T)  
**Proceedings:** Materials Research Society Symposium Proceedings 216, 59-63  
**DOI:** `10.1557/PROC-216-59`  
**Official distribution:** NIST publication `22086`

The official NIST PDF states that its calculation follows the general outline of Madarasz and Szmulowicz. It supplies the following model facts:

- Kane three-band `k.p` conduction-band model;
- full Fermi-Dirac conduction-band statistics;
- nondegenerate heavy-hole statistics;
- split-off energy `Delta = 1 eV`;
- momentum matrix element `P = 8.49e-8 eV cm`;
- heavy-hole mass `m_hh = 0.55 m0`;
- reduced Fermi energy found by Newton iteration;
- integration by parts used to remove the derivative of the inverted Kane function from the electron integral;
- final intrinsic density evaluated from either carrier population after neutrality is solved.

The exact nonlinear gap relation is

```text
Eg(x,T) = -0.302
          + 1.93*x
          - 0.810*x^2
          + 0.832*x^3
          + 5.35e-4*(1-2*x)*((-1822+T^3)/(255.2+T^2))
```

with `Eg` in eV and `T` in kelvin.

The PDF text layer corrupts the mathematical typography of Eqs. (2)-(4). The surrounding prose is usable; the extracted equation fragments are not.

### 2.4 Lowney, Seiler, Littler, and Yoon (1992)

**Title:** Intrinsic carrier concentration of narrow-gap mercury cadmium telluride based on the nonlinear temperature dependence of the band gap  
**Journal:** Journal of Applied Physics 71, 1253-1258  
**DOI:** `10.1063/1.351371`

Official NIST metadata and the journal abstract establish:

- composition range approximately `0.17<=x<=0.30`;
- temperature range approximately `0<=T<=300 K`;
- Kane nonparabolicity;
- the nonlinear magnetoabsorption-constrained gap;
- a nonlinear least-squares fit to the calculated intrinsic density.

The 1991 precursor recovers the architecture and gap relation, but not the final 1992 fit coefficients.

## 3. What can be implemented now

Authorized:

- retain the existing Hansen-Schmit abstract formula as a benchmark;
- retain parabolic Fermi-integral tests and generalized-Einstein architecture tests;
- implement source-independent numerical machinery for a generic Kane secular equation only when it is explicitly labeled a mathematical prototype;
- use the 1991 source to define transcription tests and unit-conversion checks.

Not authorized:

- label any reconstructed formula as the Madarasz-Szmulowicz equation set;
- publish a Lowney 1992 fit without verified coefficients;
- infer missing degeneracy factors, atomic-unit normalization, or integration prefactors from corrupted text extraction;
- treat a later review or detector-model formula as an independent recovery of the original equations.

## 4. Required closure evidence

The source-exact gate closes only after all of the following are available:

1. visual transcription of every symbol in the inherited neutrality and density equations;
2. an independent dimensional audit from atomic units/Ry to SI or eV-cm units;
3. verification of spin and band degeneracy factors;
4. an independently derived Kane secular-equation inversion consistent with the printed definitions;
5. at least three numerical reference points from a primary table, figure digitization with uncertainty, or author-supplied calculation;
6. the final 1992 fit coefficients if the Lowney fit is included.

## 5. Phase 1C consequence

The statistics architecture remains scientifically plausible and source-linked, but not source-exact. The correct next action is parallel work on mobility and static permittivity provenance while equation-quality copies are pursued. Production material coupling remains blocked.
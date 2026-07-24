# R06 Phase 1C intrinsic-density source audit

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Status:** official open primary precursor recovered; architecture and nonlinear gap relation verified; source-exact implementation remains blocked on symbol-level transcription

## 1. Scope

This audit separates five kinds of evidence:

1. an abstract-reported fitted intrinsic-density expression;
2. a Fermi-Dirac/Kane model whose architecture is now recovered from an open primary precursor;
3. a Hall-constrained parameter-extraction paper;
4. a nonlinear-gap Kane calculation whose final journal fit remains unavailable;
5. symbol-level equations that remain unverified because machine extraction corrupts their mathematical typography.

No missing equation is reconstructed from a later review and attributed silently to an older paper.

## 2. Hansen and Schmit (1983)

**Source:** G. L. Hansen and J. L. Schmit, "Calculation of intrinsic carrier concentration in Hg1-xCdxTe," *Journal of Applied Physics* **54**, 1639-1640 (1983).  
**DOI:** `10.1063/1.332153`  
**Verification:** bibliographic identity and abstract equation verified; full text still required for the underlying numerical integration.

The abstract reports the fitted expression

```text
ni = 1e14 * [5.585 - 3.820*x + 1.753e-3*T - 1.364e-3*x*T]
     * Eg^(3/4) * T^(3/2) * exp[-Eg/(2*kB*T)]
```

with `ni` in `cm^-3`, `Eg` in eV, and `T` in kelvin.

The abstract reports:

- fit error below 1% relative to its calculation for `Eg>0`, `50<T<300 K`, and `x<0.7`;
- agreement within 15% of experimental Hall-derived intrinsic density.

### R06 use

The fitted expression is implemented only as a historical reduction benchmark. It is not the selected reference statistics closure because it does not expose carrier susceptibility and cannot by itself provide generalized Einstein or contact-FDT coefficients.

## 3. Madarasz and Szmulowicz (1985)

**Source:** F. L. Madarasz and F. Szmulowicz, "Intrinsic carrier concentrations in Hg1-xCdxTe with the use of Fermi-Dirac statistics," *Journal of Applied Physics* **58**, 2770-2772 (1985).  
**DOI:** `10.1063/1.335868`  
**Verification:** bibliographic identity and primary abstract verified; exact printed equations remain pending.

The abstract establishes that:

- the model uses Fermi-Dirac rather than Boltzmann statistics;
- it uses a composition- and temperature-dependent Kane momentum matrix element;
- it makes no additional band-structure approximation beyond the selected Kane theory;
- Boltzmann statistics are described as inappropriate for `x<0.20`;
- Fermi-Dirac and Boltzmann results agree well for `x>=0.20`;
- comparison with Hansen-Schmit is reported over approximately `0.15<=x<=0.40`.

### Equation-lineage recovery

The official open 1991 Seiler-Lowney-Littler-Yoon proceedings paper explicitly states that its calculation follows the general outline of Madarasz and Szmulowicz. It identifies its charge-neutrality relation as Eq. (1) of the Madarasz paper and its final intrinsic-density relation as Eq. (2) of that paper.

This recovers the equation lineage and most of the model architecture, but not a symbol-perfect transcription of the Madarasz equations themselves.

### R06 use

Madarasz remains the reference architecture source. A source-exact implementation is not authorized until its equation typography, degeneracy factors, normalization, and units are independently verified.

## 4. Seiler, Lowney, Littler, and Yoon (1991) - open primary precursor

**Source:** D. G. Seiler, J. R. Lowney, C. L. Littler, and I. T. Yoon, "Intrinsic Carrier Concentrations in Long Wavelength HgCdTe Based on the New, Nonlinear Temperature Dependence of Eg(x,T)," *Materials Research Society Symposium Proceedings* **216**, 59-63 (1991).  
**DOI:** `10.1557/PROC-216-59`  
**Official distribution:** NIST publication `22086`.  
**Verification:** official open primary PDF and model architecture recovered; Eqs. (2)-(4) require visual symbol-level transcription.

The source reports calculations over approximately

```text
0.17 <= x <= 0.30
4 K <= T <= 300 K
```

It uses:

- Kane's three-band `k.p` conduction-band model;
- full Fermi-Dirac statistics for the conduction band;
- nondegenerate statistics for the valence band;
- interactions with light-hole and split-off valence bands;
- a separately treated heavy-hole band;
- split-off energy `Delta = 1 eV`;
- momentum matrix element `P = 8.49e-8 eV cm`;
- heavy-hole mass `m_hh = 0.55 m0`;
- Newton iteration for the reduced Fermi energy;
- integration by parts to remove the derivative from the electron-density integrand;
- direct solution of Kane's cubic secular equation for `gamma = k^2`.

The exact printed nonlinear gap relation is

```text
Eg = -0.302
     + 1.93*x
     - 0.810*x^2
     + 0.832*x^3
     + 5.35e-4*(1-2*x)*((-1822+T^3)/(255.2+T^2))
```

with `Eg` in eV and `T` in kelvin.

### Transcription boundary

The official PDF prints the charge-neutrality, integration-by-parts, and final intrinsic-density relations as Eqs. (2)-(4). Machine text extraction corrupts their mathematical typography. R06 therefore records their roles and surrounding definitions but does not convert the extracted fragments into executable equations.

## 5. Finkman (1983) - ledger correction

**Source:** E. Finkman, "Determination of band-gap parameters of Hg1-xCdxTe based on high-temperature carrier concentration," *Journal of Applied Physics* **54**, 1883-1886 (1983).  
**DOI:** `10.1063/1.332241`  
**Verification:** title, author, DOI, abstract, and reported PDF availability verified; full equation audit pending.

The prior ledger incorrectly described this DOI as a Finkman-Schacham intrinsic-density/effective-mass paper. The source is by **E. Finkman alone**.

The abstract says that high-temperature Hall-derived carrier concentrations are fitted with a Kane electron-concentration calculation to extract:

- the band gap and its composition/temperature dependence;
- Kane's interband-coupling matrix element;
- heavy-hole effective mass;
- modified intrinsic-carrier-density values.

### R06 use

This is a parameter-extraction and model-form source, not an independent direct intrinsic-density formula to mix freely with Hansen or Lowney. Measured Hall observables and fitted band parameters must remain separated.

## 6. Lowney, Seiler, Littler, and Yoon (1992)

**Source:** J. R. Lowney, D. G. Seiler, C. L. Littler, and I. T. Yoon, "Intrinsic carrier concentration of narrow-gap mercury cadmium telluride based on the nonlinear temperature dependence of the band gap," *Journal of Applied Physics* **71**, 1253-1258 (1992).  
**DOI:** `10.1063/1.351371`  
**Verification:** official NIST metadata verified; open primary precursor recovered; final journal fit coefficients and full equation set remain pending.

The official record reports calculations over approximately

```text
0.17 <= x <= 0.30
0 K <= T <= 300 K
```

using:

- a nonlinear temperature-dependent gap constrained by magnetoabsorption;
- Kane `k.p` conduction-band nonparabolicity;
- a nonlinear least-squares fit to the computed intrinsic density.

The open 1991 precursor recovers the calculation architecture and the exact nonlinear gap relation. It does not recover the final 1992 fit coefficients.

### R06 use

This remains the preferred low-temperature model-comparison source once the final fit and symbol-exact density equations are acquired. Until then, R06 may implement neither a presumed Lowney fit nor an inferred version reconstructed from figures.

## 7. Tangential open equation source

An open 2017 carrier-concentration article prints a one-parameter nonparabolic electron-density integral. It provides a useful independent coding check but is not treated as the exact Madarasz, Hansen-Schmit, Finkman, or Lowney equation set.

## 8. Executable scope

Authorized and implemented:

- normalized complete parabolic Fermi integrals `F_1/2` and `F_-1/2`;
- generalized-Einstein factor `Theta = F_1/2/F_-1/2`;
- Boltzmann-reduction errors;
- the abstract-reported Hansen-Schmit fitted intrinsic density;
- immutable reference values and tests.

Recovered but not executable:

- Lowney/Madarasz model architecture;
- exact nonlinear Lowney gap Eq. (1);
- reported `Delta`, `P`, and `m_hh`;
- neutrality and integration strategy.

Not implemented:

- a source-exact HgCdTe Kane density of states;
- Madarasz-Szmulowicz intrinsic density;
- Lowney 1992 fitted intrinsic density;
- Finkman parameter fits;
- dopant ionization;
- source-exact charge neutrality.

## 9. Decision

The source gap is narrowed from architecture recovery to symbol-exact transcription and numerical-reference recovery.

The reference HgCdTe statistics implementation remains blocked until:

1. Eqs. (2)-(4) are transcribed visually and independently checked;
2. Ry/atomic-unit normalization is audited;
3. numerical reference points are committed;
4. the 1992 fit coefficients are verified if that fit is to be used.

The code must retain the words `prototype` and `benchmark` in its module and API until this gate closes.

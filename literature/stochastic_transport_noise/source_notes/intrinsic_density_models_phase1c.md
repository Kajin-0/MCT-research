# R06 Phase 1C intrinsic-density source audit

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Status:** primary-record and abstract audit; only the Hansen-Schmit fitted expression is executable in this increment

## 1. Scope

This audit corrects the source ledger and separates four different kinds of evidence:

1. an abstract-reported fitted intrinsic-density expression;
2. a Fermi-Dirac/Kane model whose exact equations remain unavailable;
3. a Hall-constrained parameter-extraction paper;
4. a nonlinear-gap Kane calculation whose full fit and density-of-states equations remain unavailable.

No missing equation is reconstructed from a later review and attributed silently to an older paper.

## 2. Hansen and Schmit (1983)

**Source:** G. L. Hansen and J. L. Schmit, “Calculation of intrinsic carrier concentration in Hg1-xCdxTe,” *Journal of Applied Physics* **54**, 1639–1640 (1983).  
**DOI:** `10.1063/1.332153`  
**Verification:** bibliographic identity and abstract equation verified; full text still required for the underlying numerical integration.

The abstract states that the calculation uses the Kane nonparabolic approximation, recent heavy-hole-mass measurements, and the energy-gap relation. It reports the fitted expression

\[
n_i =
10^{14}
\left[
5.585-3.820x+1.753\times10^{-3}T
-1.364\times10^{-3}xT
\right]
E_g^{3/4}T^{3/2}
\exp\left(-\frac{E_g}{2k_BT}\right)
\]

with `n_i` in `cm^-3`, `E_g` in eV, and `T` in kelvin.

The abstract reports:

- fit error below 1% relative to its calculation for `E_g>0`, `50<T<300 K`, and `x<0.7`;
- agreement within 15% of experimental Hall-derived intrinsic density.

### R06 use

The fitted expression is implemented only as a historical reduction benchmark. It is not the selected reference statistics closure because it does not expose carrier susceptibility and cannot by itself provide generalized Einstein or contact-FDT coefficients.

## 3. Madarasz and Szmulowicz (1985)

**Source:** F. L. Madarasz and F. Szmulowicz, “Intrinsic carrier concentrations in Hg1-xCdxTe with the use of Fermi-Dirac statistics,” *Journal of Applied Physics* **58**, 2770–2772 (1985).  
**DOI:** `10.1063/1.335868`  
**Verification:** primary abstract verified; equation-level audit pending.

The abstract establishes that:

- the model uses Fermi-Dirac rather than Boltzmann statistics;
- it uses a composition- and temperature-dependent Kane momentum matrix element;
- it makes no additional band-structure approximation beyond the selected Kane theory;
- Boltzmann statistics are described as inappropriate for `x<0.20`;
- Fermi-Dirac and Boltzmann results agree well for `x>=0.20`;
- comparison with Hansen-Schmit is reported over approximately `0.15<=x<=0.40`.

### R06 use

This paper is the highest-priority exact-equation source for the reference statistics model. Its abstract supports the architecture decision but does not provide enough information to implement its model faithfully. Required full-text fields include:

- the exact Kane dispersion;
- density-of-states and degeneracy conventions;
- momentum-matrix-element relation;
- heavy- and light-hole treatment;
- charge-neutrality definition;
- numerical quadrature and fitted output.

## 4. Finkman (1983) — ledger correction

**Source:** E. Finkman, “Determination of band-gap parameters of Hg1-xCdxTe based on high-temperature carrier concentration,” *Journal of Applied Physics* **54**, 1883–1886 (1983).  
**DOI:** `10.1063/1.332241`  
**Verification:** title, author, DOI, abstract, and reported PDF availability verified; full equation audit pending.

The prior ledger incorrectly described this DOI as a Finkman-Schacham intrinsic-density/effective-mass paper. The source is by **E. Finkman alone**.

The abstract says that high-temperature Hall-derived carrier concentrations are fitted with a Kane electron-concentration calculation to extract:

- the band gap and its composition/temperature dependence;
- Kane’s interband-coupling matrix element;
- heavy-hole effective mass;
- modified intrinsic-carrier-density values.

### R06 use

This is a parameter-extraction and model-form source, not an independent direct intrinsic-density formula to mix freely with Hansen or Lowney. Measured Hall observables and fitted band parameters must remain separated.

## 5. Lowney, Seiler, Littler, and Yoon (1992) — author correction

**Source:** J. R. Lowney, D. G. Seiler, C. L. Littler, and I. T. Yoon, “Intrinsic carrier concentration of narrow-gap mercury cadmium telluride based on the nonlinear temperature dependence of the band gap,” *Journal of Applied Physics* **71**, 1253–1258 (1992).  
**DOI:** `10.1063/1.351371`  
**Verification:** official NIST record and primary abstract verified; full equations pending.

The prior ledger author list was incorrect. The official record lists Lowney, Seiler, Littler, and Yoon.

The source reports calculations over approximately

\[
0.17\le x\le0.30,
\qquad
0\le T\le300\ {\rm K},
\]

using:

- a nonlinear temperature-dependent gap constrained by magnetoabsorption;
- Kane `k.p` conduction-band nonparabolicity;
- a nonlinear least-squares fit to the computed intrinsic density.

The abstract reports large low-temperature percentage differences relative to earlier intrinsic-density relations.

### R06 use

This is the preferred low-temperature model-comparison source once its full equations are acquired. Until then, R06 may cite its range and architectural choices but may not reconstruct or fit a Lowney relation from figures or secondary tables.

## 6. Tangential open equation source

An open 2017 carrier-concentration article prints a nonparabolic electron-density integral of the form

\[
n \propto
\int_0^\infty
\frac{
X^{1/2}(1+\beta X)^{1/2}(1+2\beta X)
}{
1+\exp(X-\eta)
}\,dX.
\]

This provides a useful independent coding check for a one-parameter nonparabolic band. It is not treated as the exact Madarasz, Hansen-Schmit, Finkman, or Lowney equation set.

## 7. Executable scope in this increment

Authorized and implemented:

- normalized complete parabolic Fermi integrals `F_{1/2}` and `F_{-1/2}`;
- generalized-Einstein factor `Theta=F_{1/2}/F_{-1/2}`;
- Boltzmann-reduction errors;
- the abstract-reported Hansen-Schmit fitted intrinsic density;
- immutable reference values and tests.

Not implemented:

- a final HgCdTe Kane density of states;
- Madarasz-Szmulowicz intrinsic density;
- Lowney intrinsic density;
- Finkman parameter fits;
- dopant ionization;
- charge neutrality;
- any drift-diffusion or noise solver.

## 8. Decision

The statistics-only prototype may proceed as a verification kernel, but the reference HgCdTe model remains blocked on the exact Madarasz/Lowney equation audit. The code must keep the words `prototype` and `benchmark` in its module and API until that gate closes.

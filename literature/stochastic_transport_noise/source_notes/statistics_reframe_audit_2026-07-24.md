# R06 source-exact statistics reframe audit - 2026-07-24

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision class:** proceed / reframe / terminate

## 1. Search result

The source-exact historic replication objective remains blocked.

The audit searched:

- the repository source ledger and prior intrinsic-density gate;
- files uploaded in the current conversation and the user's File Library;
- exact titles and DOI strings for the 1985 Madarasz papers and the 1992 Lowney paper;
- the official NIST distribution of the 1991 Seiler-Lowney-Littler-Yoon precursor;
- candidate alternative closed-form HgCdTe intrinsic-density papers.

No implementation-quality full text was located for:

- Madarasz, Szmulowicz, and McBath, DOI `10.1063/1.335685`;
- Madarasz and Szmulowicz, DOI `10.1063/1.335868`;
- the fitted coefficients in Lowney et al., DOI `10.1063/1.351371`.

The official NIST precursor remains the strongest open primary source:

- Seiler, Lowney, Littler, and Yoon, DOI `10.1557/PROC-216-59`;
- NIST publication `22086`;
- official PDF distributed by NIST.

## 2. What the NIST precursor establishes

The source explicitly states:

- Kane three-band `k.p` conduction-band model;
- full Fermi-Dirac conduction-band statistics;
- nondegenerate heavy-hole statistics;
- split-off energy `Delta=1 eV`;
- momentum matrix element `P=8.49e-8 eV cm`;
- heavy-hole mass `m_hh=0.55 m0`;
- energy in Rydbergs and length in atomic units in the inherited neutrality equation;
- direct inversion of the cubic Kane secular equation;
- Newton iteration for the reduced Fermi energy;
- integration by parts to remove the derivative of the inverted Kane function;
- final intrinsic density evaluated from either electron or hole density after neutrality.

It also gives the nonlinear gap relation

```text
Eg(x,T) = -0.302
          + 1.93*x
          - 0.810*x^2
          + 0.832*x^3
          + 5.35e-4*(1-2*x)*((-1822+T^3)/(255.2+T^2))
```

with `Eg` in eV and `T` in kelvin.

The source text layer does not preserve Eqs. (2)-(4) at symbol-exact quality. The remaining ambiguity includes integral prefactors, reduced-variable typography, degeneracy factors, and atomic-unit normalization. Those quantities must not be reconstructed by pattern matching to later formulas.

## 3. Candidate alternatives

### Hansen-Schmit 1983

The published fitted expression is already implemented as a benchmark. It is source-exact at the formula level within its declared domain, but it supplies intrinsic density only. It does not supply the chemical-potential-dependent density and susceptibility needed by the nonlinear transport and fluctuation operators.

### Schmit 1970

Search results expose an abstract-level fitted expression and the use of a Kane calculation. A primary equation-quality copy was not recovered in this audit. It is not promoted above the existing Hansen-Schmit benchmark.

### Yadava 1994

The paper claims a closed expression accurate to approximately one percent for `x>=0.17`, but the accessible abstract does not preserve the fitted functions and coefficients. It is therefore another candidate source, not a recovered closure.

### Project-defined Kane closure

An independently derived three-band Kane closure is scientifically permissible if it is labeled as a project model rather than a reconstruction of Madarasz or Lowney. It would still require primary Kane theory, source-grounded HgCdTe parameters, dimensional and degeneracy audits, numerical reference points, and an uncertainty declaration.

## 4. Decision

**REFRAME.**

Do not terminate R06, because the deterministic transport, contact, trap, optical, and thermodynamic architecture can continue without pretending that the historic material closure is available.

Do not proceed with a material-accurate HgCdTe statistics claim, because the source-exact equation and validation gates remain open.

The project objective is reframed from

> reproduce the Madarasz/Lowney intrinsic-density implementation

to

> require every statistics closure to return density and susceptibility from one thermodynamically consistent evaluation, while preserving explicit provenance and model identity.

## 5. Authorized consequence

Authorized:

- a closure-independent density/compressibility interface;
- generalized Einstein identity tests;
- parabolic Fermi-Dirac reduction benchmarks;
- Hansen-Schmit intrinsic density as a bounded benchmark;
- the NIST nonlinear gap as a sensitivity input;
- an independently derived project-defined Kane prototype with an explicit non-reproduction label.

Still blocked:

- predictive HgCdTe equilibrium density or susceptibility;
- direct production coupling to detector observables;
- claiming the Lowney fit or Madarasz equations have been recovered;
- stochastic PSD or detectivity calculations using an unvalidated material closure.

## 6. Closure criterion

A material closure becomes eligible only after either:

1. source-exact recovery with symbol transcription, unit and degeneracy audits, and at least three primary numerical points; or
2. an independent project-defined Kane derivation validated against at least three independent numerical points and accompanied by a declared parameter-uncertainty domain.

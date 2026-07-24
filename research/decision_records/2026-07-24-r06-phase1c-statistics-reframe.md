# R06 Phase 1C statistics decision: reframe

**Date:** 2026-07-24  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision:** REFRAME AND PROCEED UNDER A MATERIAL-PREDICTION BLOCK

## Question

Should R06 continue to require a source-exact reproduction of the Madarasz/Lowney intrinsic-density calculations before any carrier-statistics architecture can advance?

## Evidence

The repository and renewed source audit establish:

- the physical lineage from Kane theory through Madarasz and Lowney;
- the official NIST 1991 precursor and its verified nonlinear gap relation;
- the model architecture, selected parameters, neutrality iteration, and integration-by-parts strategy;
- a source-exact Hansen-Schmit fitted intrinsic-density benchmark;
- no symbol-exact 1985 Madarasz equation set;
- no verified 1992 Lowney fitted coefficients;
- no primary numerical table sufficient for direct implementation validation.

The missing elements are not cosmetic. They affect dimensional prefactors, degeneracy, reduced-variable definitions, and validation authority.

## Options considered

### Proceed as though the historic equations were recovered

Rejected. This would convert inference from corrupted typography and later summaries into false source attribution.

### Terminate R06

Rejected. The finite-volume, nonlinear, contact, trap, optical, and thermodynamic structures remain useful and testable independently of the final material closure.

### Reframe

Accepted. Separate the software and thermodynamic contract from the identity of the eventual HgCdTe statistics model.

## Accepted architecture

Every future carrier-statistics closure must return, from one internally consistent evaluation:

1. carrier density;
2. positive chemical compressibility magnitude;
3. generalized Einstein factor;
4. temperature and reduced chemical potential;
5. the explicit normalization or density scale;
6. a declared model identity and validity domain.

The electrostatic and stochastic operators may consume this contract without knowing whether the closure is parabolic, Kane, tabulated, or fitted.

## Current implementations

### Parabolic Fermi-Dirac closure

Accepted only as a mathematical and reduction benchmark. It validates density, susceptibility, degeneracy, and generalized Einstein assembly.

### Hansen-Schmit 1983 fit

Accepted as a source-exact intrinsic-density benchmark within the published domain. It is not a chemical-potential-dependent susceptibility closure.

### Seiler-Lowney 1991 nonlinear gap

Accepted as a verified gap relation and sensitivity control. It is not, by itself, a complete intrinsic-density closure.

## Future material closure paths

A material closure may enter only through one of two paths.

### Path A - source-exact recovery

Required evidence:

- visual symbol-level transcription;
- independent unit and degeneracy audit;
- secular-equation consistency;
- at least three primary numerical reference points;
- verified fit coefficients for any fitted result.

### Path B - independent project-defined Kane closure

Required evidence:

- derivation from primary Kane theory;
- source-grounded HgCdTe parameters;
- explicit statement that the model is not a reconstruction of Madarasz or Lowney;
- dimensional and degeneracy audits;
- at least three independent numerical validation points;
- parameter and domain uncertainty declaration.

## Authorization

Authorized now:

- merge the closure-independent statistics interface;
- connect density and susceptibility to deterministic screening architecture at the interface level;
- test thermodynamic identities and reduction limits;
- continue source recovery and numerical-reference acquisition.

Not authorized:

- predictive HgCdTe density or susceptibility;
- material-grounded screening lengths;
- production transport or stochastic PSD coupling;
- predictive responsivity, gain, noise, or detectivity;
- claims that the Madarasz or Lowney equations have been reproduced.

## Phase consequence

R06 proceeds, but the Phase 1 material claim remains blocked. The next scientific gate is not more deterministic contact machinery. It is either acquisition of validation-quality intrinsic-density evidence or an independently derived project-defined Kane closure with explicit provenance and numerical validation.

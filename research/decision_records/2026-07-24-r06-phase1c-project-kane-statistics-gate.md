# R06 Phase 1C project-defined simplified Kane statistics gate

**Date:** 2026-07-24  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision:** authorize a simplified nonparabolic benchmark; retain the material-prediction block

## Objective

Implement the first executable closure under the project-defined path authorized by PR #381 without claiming that the unresolved Madarasz or Lowney equation sets have been recovered.

## Model

The accepted prototype dispersion is

\[
E(1+\alpha E)=\frac{\hbar^2k^2}{2m^*}.
\]

The model uses:

- explicit nonparabolicity `alpha` in `eV^-1`;
- explicit parabolic density scale `N_*` in `cm^-3`;
- full Fermi-Dirac occupation;
- density and chemical compressibility from one quadrature;
- generalized Einstein factor from the thermodynamic ratio;
- no composition, temperature, gap, or effective-mass parameter formula.

## Why this model is admissible

The simplified relation is a recognizable project-defined Kane model with an explicit derivation and model identity. It provides the correct architecture for testing nonparabolic density, susceptibility, degeneracy, and the generalized Einstein relation.

It is not represented as:

- the complete three-band Kane secular equation;
- the NIST precursor equation set;
- a Madarasz or Lowney replication;
- an HgCdTe material closure.

## Numerical evidence required

The prototype must pass:

- exact parabolic reduction;
- density-of-states positivity;
- finite-difference susceptibility agreement;
- thermodynamic identity closure;
- Boltzmann-limit recovery;
- monotonicity;
- scale separation;
- quadrature refinement;
- three frozen high-precision dimensionless reference points;
- runtime protocol compliance.

The frozen points are numerical regression evidence only. They do not satisfy the independent material-validation requirement declared by PR #381.

## Decision

Authorize the simplified Kane prototype as a **nonparabolic mathematical benchmark**.

Do not authorize material coupling. The following remain unresolved:

1. the full three-band HgCdTe secular equation and band accounting;
2. source-grounded `alpha(x,T)` or an equivalent parameterization;
3. source-grounded density scale or effective mass;
4. heavy-hole neutrality and split-off-band treatment;
5. independent HgCdTe numerical reference points;
6. parameter uncertainty and validity domain.

## Next gate

After numerical CI validation, the next scientific gate is a parameter and validation design—not immediate detector coupling. It must specify what primary measurements or calculations can identify:

- the density scale;
- nonparabolicity;
- intrinsic neutrality;
- chemical compressibility;
- the intended composition-temperature domain.

A source-grounded comparison against Hansen-Schmit intrinsic density may be used as a diagnostic, but it cannot validate susceptibility by itself.

## Authorization boundary

Passing this gate authorizes:

- nonparabolic architecture tests;
- reduced-model comparisons;
- sensitivity to explicit `alpha` and `N_*`;
- future substitution behind the merged statistics protocol.

It does not authorize:

- HgCdTe density or susceptibility prediction;
- screening-length prediction;
- production deterministic transport;
- stochastic PSD, gain, responsivity, or detectivity calculations;
- historic-source reproduction claims.

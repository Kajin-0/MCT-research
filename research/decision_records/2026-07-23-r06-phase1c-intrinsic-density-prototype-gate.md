# R06 Phase 1C intrinsic-density prototype gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision:** authorize a parabolic Fermi-integral verification prototype and Hansen-Schmit benchmark; do not authorize a final Kane/HgCdTe statistics implementation

## Source findings

1. Hansen-Schmit 1983 exposes an abstract-level fitted intrinsic-density equation and validity range.
2. Madarasz-Szmulowicz 1985 establishes that Fermi-Dirac statistics matter for narrow-gap `x<0.20` material, but its exact equations are not yet available.
3. DOI `10.1063/1.332241` was misidentified in the prior ledger. It is E. Finkman’s Hall-constrained high-temperature band-parameter paper.
4. The 1992 nonlinear-gap paper is by J. R. Lowney, D. G. Seiler, C. L. Littler, and I. T. Yoon; the prior author list was wrong.
5. No uploaded copy of the four intrinsic-density papers is currently available.

## Implemented prototype

The authorized kernel evaluates the normalized complete Fermi-Dirac integrals

\[
\mathcal F_j(\eta)
=
\Gamma(j+1)^{-1}
\int_0^\infty
\frac{t^j}{1+\exp(t-\eta)}dt
\]

for `j=-1/2` and `j=1/2`, together with

\[
\Theta=\frac{\mathcal F_{1/2}}{\mathcal F_{-1/2}}.
\]

It also implements the abstract-reported Hansen-Schmit fit as a historical benchmark.

## Validation

Local isolated validation completed:

- 22 tests passed;
- reference points from `eta=-8` through `eta=5`;
- derivative identity `dF_{1/2}/deta=F_{-1/2}`;
- vector/scalar consistency;
- monotonic Boltzmann-limit convergence;
- Hansen-Schmit equation reproduction;
- invalid-domain rejection;
- immutable machine-readable reference consistency.

This validation was run outside GitHub Actions. Current-head CI remains the repository-level authority after commit.

## Claim boundary

Supported:

- numerical Fermi-integral and generalized-Einstein verification;
- reproduction of the Hansen-Schmit abstract formula;
- preliminary Boltzmann-reduction thresholds.

Not supported:

- identification of the exact HgCdTe Kane model;
- reproduction of Madarasz, Lowney, or Finkman calculations;
- predictive intrinsic density;
- parameter uncertainty;
- transport, contact, or noise predictions.

## Next gate

Acquire or independently verify the full Madarasz-Szmulowicz and Lowney equations. If unavailable, Phase 2 must begin with dimensionless statistics and the parabolic/nonparabolic verification family rather than a claimed material-accurate HgCdTe carrier model.

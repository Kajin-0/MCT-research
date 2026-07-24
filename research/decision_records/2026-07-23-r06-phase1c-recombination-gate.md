# R06 Phase 1C equilibrium-consistent pair-recombination gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision:** provisionally accept one dimensionless mass-action pair source pending current-head CI

## Accepted source

The restricted net electron-hole pair annihilation rate is

\[
U=\kappa\left(NP-K_{\mathrm{eq}}\right),
\]

with

\[
\kappa\geq0,
\qquad
K_{\mathrm{eq}}>0.
\]

Positive `U` denotes net pair annihilation. Negative `U` denotes the reverse
thermal-generation direction. The source vanishes when

\[
NP=K_{\mathrm{eq}}.
\]

This is accepted only as a dimensionless detailed-balance architecture model.
The coefficient is not identified with an HgCdTe lifetime, radiative
coefficient, Auger coefficient, capture coefficient, or measured material
parameter.

## Continuity signs

The previously accepted conventional currents are

\[
j_n=d_n(N'-N\psi'),
\]

\[
j_p=-d_p(P'+P\psi').
\]

The source-augmented steady residuals are

\[
R_n=\frac{d j_n}{dx}-U,
\]

\[
R_p=\frac{d j_p}{dx}+U.
\]

The opposite signs are required by the electron and hole charge conventions.
Using the same residual sign in both equations would violate total-current
conservation.

The accepted sum identity is

\[
R_n+R_p
=
\frac{d}{dx}(j_n+j_p).
\]

Thus pair annihilation redistributes the separate electron and hole currents
without introducing a net conventional-current source.

## Analytical Jacobian contribution

With logarithmic carrier unknowns,

\[
\frac{\partial U}{\partial\log N}
=
\frac{\partial U}{\partial\log P}
=
\kappa NP.
\]

The source Jacobian additions are therefore

\[
\Delta J_{n,n}=\Delta J_{n,p}=-\kappa NP,
\]

\[
\Delta J_{p,n}=\Delta J_{p,p}=+\kappa NP.
\]

The restricted source has no direct potential derivative.

## Global conservation diagnostics

The independent diagnostic evaluates

\[
j_{n,R}-j_{n,L}-h\sum_iU_i,
\]

\[
j_{p,R}-j_{p,L}+h\sum_iU_i,
\]

and the spatial variation of

\[
j_n+j_p.
\]

These quantities are reconstructed from face currents and local pair rates,
not inferred only from the nonlinear residual norm.

At a converged state, the separate carrier balances must close and the total
conventional current must remain spatially constant.

## Local verification evidence

A focused isolated test run reports **10 passed tests**.

Verified locally:

- the rate has the declared annihilation, generation, and detailed-balance signs;
- a constant charged equilibrium with `NP = K_eq` has zero full residual;
- the equilibrium nonlinear solve terminates without iteration;
- `kappa = 0` reduces bitwise to the accepted source-free bipolar residual and
  Jacobian;
- the local pair source cancels exactly from the sum of continuity blocks;
- the analytical source-augmented Jacobian agrees with centered finite
  differences;
- arbitrary-state terminal/source mismatches equal the integrated discrete
  residuals;
- a symmetric contact-supplied recombination benchmark converges;
- that benchmark preserves `N = P`, `psi = 0`, positive net annihilation, and
  constant total current;
- invalid parameters and carrier arrays are rejected.

GitHub Actions remains the repository-level authority for the committed head.

## Scientific interpretation

This gate fixes the first deterministic source signs and conservation
architecture. It does not establish which physical recombination mechanism
dominates an HgCdTe photoconductor or determine a quantitative lifetime.

The mass-action form is intentionally minimal because it provides an exact
reverse process and a transparent equilibrium product. A one-way sink such as
`-N/tau` is rejected for this gate because it does not preserve dark thermal
equilibrium without an explicitly paired generation process.

## Authorization after green CI

Authorize next:

1. merge this source-sign and detailed-balance gate;
2. decide whether the next source model is direct band-to-band or an explicit
   dynamic trap state;
3. require any successor source to reduce to this pair-balance structure;
4. connect `K_eq` to the accepted carrier-statistics interface only after the
   exact Kane/intrinsic-density audit is complete;
5. continue mobility and static-permittivity provenance;
6. prepare the final Phase 1 proceed/reframe/terminate decision.

Still unauthorized:

- assigning `kappa` to an HgCdTe material lifetime;
- predictive recombination, responsivity, detectivity, or noise calculations;
- phenomenological single-lifetime fitting presented as mechanism identification;
- dynamic traps without explicit occupancy and reverse rates;
- optical generation before dark equilibrium remains verified;
- stochastic source covariance or PSD production;
- broad material sweeps;
- manuscript or novelty claims.

## Failure and rollback conditions

Revise or reject this source if current-head CI shows that:

- the source signs conflict with the accepted conventional-current definitions;
- the source fails to cancel from the summed continuity equation;
- detailed-balance equilibrium is not exact;
- the analytical Jacobian fails independent finite differences;
- terminal pair balances fail after nonlinear convergence;
- total current is not conserved;
- the new package breaks previously merged unipolar or bipolar tests.

## Final gate condition

This provisional decision becomes accepted only after all current-head
repository workflows complete successfully. Until then, the branch remains a
draft and no dynamic-trap or material-lifetime implementation is authorized.

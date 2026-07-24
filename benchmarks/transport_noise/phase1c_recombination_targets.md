# R06 Phase 1C equilibrium-consistent pair-recombination targets

**Status:** executable deterministic-source gate  
**Scope:** one dimensionless mass-action pair source in the verified bipolar model  
**Controlling issue:** #346

## Purpose

This gate establishes the source signs, detailed-balance condition, analytical
Jacobian contribution, nonlinear behavior, and global conservation identities
for the first deterministic electron-hole source term.

It is a numerical architecture test. It is not an HgCdTe lifetime law and does
not represent a validated SRH, radiative, Auger, trap-assisted, or optical model.

## Net pair rate

Define

\[
U=\kappa\left(NP-K_{\mathrm{eq}}\right),
\]

where

- `kappa >= 0` is a dimensionless rate coefficient;
- `K_eq > 0` is the equilibrium carrier-product constant;
- `U > 0` denotes net electron-hole pair annihilation;
- `U < 0` denotes the reverse thermal-generation direction.

Detailed balance requires

\[
NP=K_{\mathrm{eq}}
\quad\Longrightarrow\quad
U=0.
\]

## Continuity-source signs

The accepted conventional currents are

\[
j_n=d_n(N'-N\psi'),
\]

\[
j_p=-d_p(P'+P\psi').
\]

The steady continuity residuals with positive net annihilation are

\[
R_n=\frac{d j_n}{dx}-U,
\]

\[
R_p=\frac{d j_p}{dx}+U.
\]

The source therefore enters the electron and hole residuals with opposite
signs. This is required by the opposite charge signs in the two conventional
current continuity equations.

Adding the two equations gives

\[
\frac{d}{dx}(j_n+j_p)=0,
\]

so the total conventional current remains source-free.

## R0 — detailed-balance equilibrium

Choose constant positive densities `N0`, `P0` satisfying

\[
N_0P_0=K_{\mathrm{eq}},
\]

and fixed charge

\[
C=N_0-P_0.
\]

With constant potential and matching reservoir values, the full Poisson,
electron-continuity, and hole-continuity residual must vanish to roundoff.

Acceptance:

- local pair rate is zero;
- full residual is zero to roundoff;
- Newton terminates without an iteration;
- total current is spatially constant.

## R1 — rate direction

For positive `kappa`:

- `NP > K_eq` must produce `U > 0`;
- `NP < K_eq` must produce `U < 0`;
- `NP = K_eq` must produce `U = 0`.

This verifies the declared net-annihilation convention.

## R2 — exact source-free reduction

At `kappa = 0`, the recombining residual and Jacobian must be bitwise identical
to the previously accepted source-free bipolar residual and Jacobian.

No hidden source-dependent scaling or regularization is permitted.

## R3 — local charge cancellation

At every interior node,

\[
\Delta R_n+\Delta R_p=0,
\]

where `Delta` denotes the contribution from the pair source.

The source may redistribute electron and hole conventional currents, but it may
not create a net charge-current source.

## R4 — analytical source Jacobian

For logarithmic carrier variables,

\[
\frac{\partial U}{\partial\log N}
=
\frac{\partial U}{\partial\log P}
=
\kappa NP.
\]

Therefore the local Jacobian additions are

\[
\frac{\partial R_n}{\partial\log N}
=
\frac{\partial R_n}{\partial\log P}
=-\kappa NP,
\]

\[
\frac{\partial R_p}{\partial\log N}
=
\frac{\partial R_p}{\partial\log P}
=+\kappa NP.
\]

There is no direct source derivative with respect to potential in this
restricted model.

Acceptance: the complete analytical Jacobian agrees with centered finite
differences over a nonuniform finite state.

## R5 — global pair balance

At a converged steady state,

\[
j_{n,R}-j_{n,L}=h\sum_i U_i,
\]

\[
j_{p,R}-j_{p,L}=-h\sum_i U_i.
\]

The independent diagnostic must evaluate both identities from reconstructed
face currents and sampled pair rates rather than from the nonlinear residual
norm alone.

Acceptance: relative mismatch below `1e-10` for each carrier.

## R6 — total-current conservation

Because the pair source cancels between the two continuity equations,

\[
(j_n+j_p)_R-(j_n+j_p)_L=0.
\]

For a converged source-driven state, the total face current must be spatially
constant within the nonlinear tolerance.

## R7 — contact-supplied recombination case

Use equal electron and hole reservoir densities greater than the equilibrium
density, zero applied voltage, equal diffusion ratios, and zero fixed charge.

The nonlinear solution must satisfy:

- `N = P` by symmetry;
- `psi = 0` to numerical tolerance;
- the interior density is below the reservoir density;
- integrated pair annihilation is positive;
- electron and hole terminal balances close independently;
- total conventional current remains spatially constant.

This is a dimensionless benchmark, not a physical surface-recombination or
contact-injection model.

## R8 — nonlinear solver behavior

The source-augmented system must use the existing residual-decreasing damped
Newton policy and report explicit termination reasons.

Acceptance:

- exact equilibrium terminates immediately;
- the contact-supplied recombination case converges;
- all accepted states remain finite and carrier-positive;
- final residual does not exceed the declared target.

## R9 — rejection paths

Reject explicitly:

- negative or non-finite rate coefficients;
- non-positive or non-finite equilibrium products;
- unequal electron and hole input shapes;
- non-finite carrier densities;
- non-positive carrier densities;
- incompatible nonlinear state dimensions.

## R10 — scientific boundary

Passing R0–R9 authorizes only the next deterministic-source decision.

It does not authorize:

- assigning the dimensionless coefficient to an HgCdTe lifetime;
- claiming SRH, radiative, or Auger fidelity;
- adding dynamic trap occupancy without a separate detailed-balance gate;
- optical generation;
- material-accurate simulations or broad parameter sweeps;
- stochastic source covariance or PSD calculations;
- responsivity, detectivity, or terminal-noise predictions;
- manuscript or novelty claims.

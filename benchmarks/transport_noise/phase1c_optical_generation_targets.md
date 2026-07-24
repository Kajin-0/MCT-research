# R06 Phase 1C uniform optical-generation benchmark targets

**Status:** executable deterministic architecture gate  
**Scope:** spatially uniform, state-independent mobile-pair generation  
**Controlling issue:** #346

## O0 — generation-domain validation

The dimensionless pair-generation rate `G` must be finite and non-negative. Invalid rates must be rejected explicitly.

## O1 — dark residual reduction

At `G = 0`, the illuminated residual must reduce bitwise to the accepted reversible trap residual.

## O2 — dark Jacobian reduction

At `G = 0`, the illuminated Jacobian must reduce bitwise to the accepted reversible trap Jacobian.

## O3 — source signs

Uniform generation must enter only the mobile-carrier continuity rows:

```text
R_n = div(j_n) - A + G
R_p = div(j_p) + B - G
R_f = A - B.
```

It must not act directly on Poisson or trap occupancy.

## O4 — local charge cancellation

The generation increments must cancel cell by cell:

```text
(+G) + (-G) + 0 = 0.
```

## O5 — exact uniform illuminated balance

For a symmetric reversible trap and compatible fixed reservoirs, a uniform state satisfying `A = B = G` must have zero Poisson, electron, hole, and trap residuals.

## O6 — exact nonlinear termination

The exact uniform illuminated state supplied as the initial condition must terminate without a Newton step.

## O7 — analytical Jacobian

Because `G` is state independent, the illuminated analytical Jacobian must equal the trap Jacobian and agree with a centered finite-difference Jacobian.

## O8 — global generation-recombination balances

For an arbitrary state,

```text
j_n,R - j_n,L - [h sum(A) - h sum(G)] = h sum(R_n)

j_p,R - j_p,L - [h sum(G) - h sum(B)] = h sum(R_p)

h sum(A - B) = h sum(R_f).
```

The sum of the three kinetic residual blocks must telescope to the terminal difference of total conventional current.

## O9 — contact-extracted photogeneration

With equilibrium-density contacts and positive uniform generation, the nonlinear solve must converge with

- positive integrated generation;
- independently closed electron, hole, and trap balances;
- spatially constant total conventional current.

## O10 — controlled failure

Invalid state shape or non-finite state values must be rejected. Nonlinear failure must return an explicit termination reason rather than NaNs or false convergence.

## Acceptance boundary

Passing O0–O10 validates deterministic pair-generation signs, dark reduction, illuminated balance, and nonlinear architecture only. It does not validate absorption, quantum efficiency, spectral response, responsivity, optical gain, or HgCdTe detector performance.

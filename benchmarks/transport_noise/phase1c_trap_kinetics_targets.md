# R06 Phase 1C reversible trap-kinetics benchmark targets

**Status:** executable deterministic architecture gate  
**Scope:** one bounded occupancy field with four reversible channels  
**Controlling issue:** #346

## T0 — occupancy bounds

The logit representation must reconstruct `0 < f < 1` for every finite numerical state. Invalid direct occupancy inputs must be rejected.

## T1 — electron detailed balance

At `(N_eq, f_eq)`, electron capture and electron emission must agree to floating-point precision.

## T2 — hole detailed balance

At `(P_eq, f_eq)`, hole capture and hole emission must agree to floating-point precision.

## T3 — charged equilibrium

For compatible fixed charge

```text
C = N_eq + N_t f_eq - P_eq,
```

a spatially uniform equilibrium must have zero Poisson, electron, hole, and trap residuals.

## T4 — source-free reduction

At `N_t = 0`, the first three residual blocks must reduce exactly to the accepted source-free bipolar residual, and the trap residual must vanish.

The resulting four-block Jacobian is singular because occupancy becomes physically absent. This case is a reduction identity, not a nonlinear-solver benchmark.

## T5 — local charge conservation

The electron, hole, and trap source increments must satisfy

```text
Delta R_n + Delta R_p + R_f = 0
```

cell by cell.

## T6 — steady occupancy

The analytical `f_ss(N,P)` must make net electron capture and net hole capture equal locally.

## T7 — reduced pair rate

The eliminated rate must satisfy

```text
U_ss = kappa_eff(N,P) (N P - K_eq)
```

with `kappa_eff > 0` for positive parameters and densities.

The benchmark must explicitly reject the claim that a single constant coefficient is globally exact.

## T8 — analytical Jacobian

The complete four-block analytical Jacobian must agree with a centered finite-difference Jacobian over a nonuniform state.

## T9 — global balance identities

For an arbitrary state,

```text
j_n,R - j_n,L - h sum(A) = h sum(R_n)

j_p,R - j_p,L + h sum(B) = h sum(R_p)

h sum(A - B) = h sum(R_f).
```

The sum of the three kinetic residual blocks must telescope to the terminal difference of total conventional current.

## T10 — equilibrium nonlinear termination

An exact equilibrium supplied as the initial state must terminate without a Newton step.

## T11 — contact-supplied trap recombination

A symmetric nonequilibrium contact benchmark must converge with

- positive integrated net electron capture;
- matched integrated electron and hole capture;
- negligible trap-balance residual;
- spatially constant total conventional current.

## T12 — controlled failure and validation

Invalid trap density, capture coefficients, equilibrium occupancy, state shape, or occupancy inputs must be rejected explicitly. Nonlinear failures must return a declared termination reason rather than NaNs or false convergence.

## Acceptance boundary

Passing T0–T12 validates reversible trap signs, bounded occupancy, detailed balance, charge conservation, Jacobian assembly, and steady nonlinear architecture only. It does not validate HgCdTe trap parameters, SRH lifetime, optical response, or noise predictions.

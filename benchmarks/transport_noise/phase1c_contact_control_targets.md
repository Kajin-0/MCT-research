# R06 Phase 1C finite-contact control targets

These targets validate a restricted dimensionless deterministic contact architecture. They do not validate a material-specific HgCdTe contact.

## F0 — input domain

Reject nonpositive equilibrium density, negative Biot number, nonfinite potential, nonpositive diffusion ratio, and incompatible state shape.

## F1 — exact zero-field finite-contact state

For zero screening and equal boundary potentials, the analytical linear-density state must satisfy the complete residual to numerical precision.

## F2 — exact series-current law

The computed current must equal

\[
j_n=\frac{D_n}{L}\frac{N_R^{eq}-N_L^{eq}}
{1+\mathrm{Bi}_L^{-1}+\mathrm{Bi}_R^{-1}}.
\]

## F3 — conservative bulk current

All Scharfetter-Gummel face currents must agree for the exact source-free state.

## F4 — independent contact balances

The left and right exchange currents must independently agree with the adjacent bulk face current using the declared outward-normal signs.

## F5 — fast-reservoir asymptote

As both Biot numbers increase, boundary densities and current must approach the fixed-density ideal-reservoir solution.

## F6 — two-sided blocking limit

At `Bi_L=Bi_R=0`, particle current must vanish. With zero screening, uniform-density states must expose one conserved-population Jacobian null mode.

## F7 — one-sided blocking limit

If either contact is exactly blocking in the source-free steady benchmark, the terminal particle current must vanish.

## F8 — analytical Jacobian

The complete Poisson/continuity/contact Jacobian must agree with centered finite differences for a nonuniform state.

## F9 — nonlinear recovery

Damped Newton must recover the exact finite-contact benchmark from a perturbed potential and log-density state.

## F10 — asymmetric contact dominance

For strongly unequal Biot numbers, the lower-Biot contact must dominate the exact series-resistance partition.

## F11 — terminal-load separation

The independent series-load number `Lambda_Z=R_s/R_device` must recover ideal voltage bias at zero and the high-load current suppression `1/(1+Lambda_Z)`.

## F12 — positivity

All contact-adjacent and interior densities must remain positive through the all-node logarithmic representation.

## Acceptance boundary

Passing F0-F12 authorizes the classical finite-exchange boundary only as a dimensionless deterministic architecture and reduction benchmark. It does not authorize:

- HgCdTe contact velocities;
- Schottky barriers or Richardson constants;
- tunneling or thermionic-emission closure;
- dynamic interface charge;
- pair surface recombination;
- contact-noise covariance;
- predictive detector or terminal claims.

# R06 Phase 1C bipolar-contact control targets

These targets validate a restricted dimensionless deterministic contact architecture. They do not validate a material-specific HgCdTe contact.

## G0 — input domain

Reject invalid diffusion ratios, negative screening, nonfinite fixed charge, nonpositive equilibrium densities, negative Biot numbers, and incompatible state shape.

## G1 — exact zero-field bipolar state

For zero screening and equal boundary potentials, the analytical electron and hole profiles must satisfy the complete Poisson/continuity/contact residual.

## G2 — electron contact signs

The left and right electron rows must recover

`j_n,L = +S_n,L (N_L-N_L_eq)`

`j_n,R = -S_n,R (N_R-N_R_eq)`.

## G3 — hole contact signs

The left and right hole rows must recover

`j_p,L = -S_p,L (P_L-P_L_eq)`

`j_p,R = +S_p,R (P_R-P_R_eq)`.

## G4 — exact carrier currents

Each carrier current must equal its exact series-resistance expression with independent contact Biot numbers.

## G5 — neutral screened equilibrium

A constant state satisfying `N-P-C=0`, identical left/right equilibrium densities, and zero field must give exactly zero residual for nonzero screening.

## G6 — fast-reservoir reduction

As all four Biot numbers increase, both carrier boundary densities and currents must approach the ideal-reservoir bipolar solution.

## G7 — selective electron blocking

If either electron contact is blocking, source-free electron current must vanish while hole current may remain finite.

## G8 — selective hole blocking

If either hole contact is blocking, source-free hole current must vanish while electron current may remain finite.

## G9 — two-species blocking null modes

With both carriers blocked at both contacts and zero screening, the Jacobian must expose two independent population null modes.

## G10 — electron-hole symmetry

For equal diffusion ratios, equal Biot controls, and reversed electron/hole reservoir gradients, electron and hole currents must agree and their density profiles must map by spatial reflection.

## G11 — analytical Jacobian

The full Poisson/electron/hole/four-contact Jacobian must agree with centered finite differences for a nonuniform state.

## G12 — nonlinear recovery

Damped Newton must recover the exact finite-contact state from perturbed potential and both log-density blocks.

## G13 — carrier and total-current diagnostics

Electron current, hole current, all four boundary exchange currents, and total conventional current must be independently conserved for the exact source-free state.

## Acceptance boundary

Passing G0-G13 authorizes the bipolar classical finite-exchange block only as a deterministic architecture and limiting-regime benchmark. It does not authorize material contact parameters, interface-state dynamics, surface-pair recombination, contact noise, or predictive detector claims.

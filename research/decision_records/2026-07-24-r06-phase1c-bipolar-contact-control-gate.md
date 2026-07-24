# R06 Phase 1C bipolar contact-control gate

**Date:** 2026-07-24  
**Controlling issue:** #346  
**Decision:** provisionally accept the separate electron/hole finite-exchange architecture subject to current-head CI; retain all quantitative HgCdTe contact claims as blocked

## Added architecture

- fixed electrostatic potential at both terminals;
- all-node positive electron and hole densities through logarithmic variables;
- conservative Scharfetter-Gummel electron and hole currents;
- independent left/right electron exchange;
- independent left/right hole exchange;
- four contact Biot numbers;
- Poisson, electron continuity, hole continuity, and four contact residual rows;
- complete analytical Jacobian;
- exact zero-field electron and hole profiles;
- selective blocking and fast-reservoir reductions;
- carrier-resolved and total-current diagnostics;
- damped Newton solve.

## Accepted contact signs

Electron conventional current:

`j_n,L = +S_n,L (N_L-N_L_eq)`

`j_n,R = -S_n,R (N_R-N_R_eq)`

Hole conventional current:

`j_p,L = -S_p,L (P_L-P_L_eq)`

`j_p,R = +S_p,R (P_R-P_R_eq)`

The difference follows from the opposite charge signs relating conventional current to particle flux.

## Exact zero-field result

`j_n = (D_n/L)(N_R_eq-N_L_eq)/(1+1/Bi_n,L+1/Bi_n,R)`

`j_p = (D_p/L)(P_L_eq-P_R_eq)/(1+1/Bi_p,L+1/Bi_p,R)`

## Selective-contact result

The deterministic architecture permits one carrier to be blocking while the other remains transmissive. This is a structural control, not a claim that a specific metal/HgCdTe contact realizes those Biot values.

## Blocking result

With both carriers blocked at both terminals and zero screening, separate total electron and hole populations are conserved. The Jacobian therefore has two null modes. No artificial pinning is added.

## Authorized use

- sign and conservation verification;
- carrier-selective contact benchmarks;
- contact-limited versus bulk-limited dimensionless sensitivity;
- ideal-reservoir and blocking reductions;
- preparation for later source/recombination coupling.

## Not authorized

- HgCdTe electron or hole transfer velocities;
- barrier heights, Richardson constants, tunneling, or thermionic emission;
- surface recombination velocities interpreted as metal-contact exchange;
- dynamic interface charge or interface-trap occupancy;
- contact-noise covariance or contact FDT claims;
- predictive terminal resistance, gain, responsivity, noise, or detectivity.

## Next gate

After this deterministic block passes CI, the next scientific decision should be whether to couple the finite contacts to the already verified bulk pair/trap source or to stop contact expansion and return to the source-exact statistics closure. No nonlinear electrochemical-potential exchange law should be added without an explicit source audit.

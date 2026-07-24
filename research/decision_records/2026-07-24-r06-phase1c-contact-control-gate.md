# R06 Phase 1C contact-control gate

**Date:** 2026-07-24  
**Controlling issue:** #346  
**Decision:** accept the restricted classical finite-exchange contact prototype as a deterministic architecture benchmark; retain all quantitative HgCdTe contact claims as blocked

## Accepted implementation

The branch adds a one-dimensional unipolar finite-contact system with:

- fixed electrostatic potentials;
- all-node logarithmic carrier density;
- conservative Scharfetter-Gummel bulk current;
- independent left and right classical density-Robin exchange laws;
- contact Biot controls `Bi=S L/D`;
- exact zero-field finite-contact current and state;
- exact blocking and fast-reservoir reductions;
- analytical Poisson/continuity/contact Jacobian;
- residual-decreasing damped Newton solve;
- independent bulk and boundary balance diagnostics;
- separate scalar terminal series-load control.

## Verified sign convention

For electron conventional current,

`j_left = S_left * (N_left - N_left_eq)`

`j_right = -S_right * (N_right - N_right_eq)`.

The sign difference follows from the opposite outward normals.

## Exact structural result

For the zero-field source-free benchmark,

`j/j_ideal = 1 / (1 + 1/Bi_left + 1/Bi_right)`.

This gives an exact partition between bulk, left-contact, and right-contact resistance for the declared reduced model.

## Blocking-contact result

At two exactly blocking contacts with zero screening, total carrier population is conserved and the Jacobian has one null mode. The implementation records this explicitly rather than regularizing it silently.

## Authorized use

- deterministic sign and conservation tests;
- ideal-reservoir and blocking reduction tests;
- contact-limited versus bulk-limited sensitivity studies in dimensionless variables;
- asymmetric-contact numerical benchmarks;
- separation of contact control from terminal series loading;
- preparation for a later bipolar finite-contact extension.

## Not authorized

- a universal HgCdTe surface-transfer velocity;
- barrier-height, Richardson-constant, tunneling, or thermionic-emission predictions;
- quantitative metal/HgCdTe contact resistance;
- interface-state storage or pair surface recombination;
- stochastic contact covariance or terminal FDT claims;
- responsivity, gain, noise, or detectivity predictions.

## Next gate

The next contact increment should extend the verified signs and controls to the bipolar residual with separate electron and hole exchange, then test exact equilibrium and fast/blocking reductions. A nonlinear electrochemical-potential exchange law or dynamic interface state should not be added until its source and parameter requirements are explicit.

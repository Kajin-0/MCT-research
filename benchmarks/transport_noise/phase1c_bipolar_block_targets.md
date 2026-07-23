# R06 Phase 1C bipolar deterministic benchmark targets

**Status:** executable architecture gate  
**Scope:** steady dimensionless source-free bipolar finite volume  
**Controlling issue:** #346

## B0 — configuration validation

Reject:

- non-finite boundary values;
- zero or negative carrier reservoir densities;
- negative screening strength;
- zero or negative electron or hole diffusion ratios;
- state vectors with incorrect size or non-finite entries.

## B1 — positivity representation

Reconstruct

\[
N_i=\exp(\nu_i),
\qquad
P_i=\exp(\pi_i)
\]

and verify strictly positive interior densities for every finite state.

## B2 — uniform neutral equilibrium

For

\[
\psi=\text{constant},
\qquad
N=P+C,
\]

require:

- Poisson residual at roundoff;
- electron and hole continuity residuals at roundoff;
- zero electron and hole face currents.

Target absolute residual: `< 5e-12`.

## B3 — exact biased neutral resistor

For constant `N`, constant `P`, `C=N-P`, and affine `psi`, require

\[
j_n=-d_nN\Delta\psi/L,
\qquad
j_p=-d_pP\Delta\psi/L.
\]

Requirements:

- all residual blocks `< 5e-11` absolute;
- each face-current variation `< 1e-12` relative;
- current value agreement `< 1e-12` relative.

## B4 — zero-field diffusion signs

At constant potential and increasing density,

\[
j_n>0,
\qquad
j_p<0.
\]

The numerical currents must reproduce the exact linear-profile values.

## B5 — independent conservation identities

For arbitrary finite positive states, verify

\[
h\sum_iR_{n,i}=j_{n,R}-j_{n,L},
\]

\[
h\sum_iR_{p,i}=j_{p,R}-j_{p,L}.
\]

Target discrepancy: `< 5e-12` absolute.

## B6 — analytical Jacobian

Compare the complete analytical Jacobian against centered finite differences for nonuniform potential and both carrier densities.

Targets:

- maximum absolute discrepancy `< 5e-7`;
- maximum relative discrepancy `< 5e-7` away from numerically zero entries.

## B7 — block sparsity semantics

For the source-free independent-carrier model,

\[
J_{np}=0,
\qquad
J_{pn}=0.
\]

Poisson must retain both `J_psi,n` and `J_psi,p` diagonal blocks with opposite signs.

## B8 — electron-hole symmetry

Apply

\[
\psi\to-\psi,
\quad
N\leftrightarrow P,
\quad
C\to-C,
\quad
d_n\leftrightarrow d_p.
\]

Require

\[
R_\psi'=-R_\psi,
\qquad
R_n'=-R_p,
\qquad
R_p'=-R_n.
\]

Target discrepancy: `< 5e-12` absolute.

## B9 — unipolar reduction

Hold `P=P_0` constant and choose

\[
C=N_B-P_0.
\]

The bipolar Poisson and electron-continuity blocks must match the merged unipolar residual for the same potential, electron density, screening strength, and electron diffusion ratio.

Target discrepancy: `< 5e-12` absolute.

## B10 — boundary-profile constructor

The linear reservoir constructor must:

- reproduce both potential endpoint values;
- interpolate potential linearly;
- interpolate each log density linearly;
- preserve positive densities.

## B11 — regression boundary

No benchmark in this file authorizes:

- material-specific HgCdTe prediction;
- recombination or trap terms;
- optical generation;
- finite-rate contacts;
- external circuit state;
- stochastic covariance or PSD calculation.

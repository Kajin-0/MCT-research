# R06 finite-exchange contact controls

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Scope:** dimensionless steady unipolar verification

## 1. Orientation and current sign

The device occupies `0 <= x <= L`. The dimensionless electron conventional current is

\[
j_n=d_n\left(\partial_x N-N\partial_x\psi\right).
\]

Electron particle flux has the opposite sign. With outward normals `nu_L=-1` and `nu_R=+1`, the classical outward particle-exchange law is

\[
\nu\Gamma_n=S_c(N-N_c^{eq}).
\]

Therefore the conventional-current boundary equations are

\[
j_n(0)=S_L\left[N(0)-N_L^{eq}\right],
\]

\[
j_n(L)=-S_R\left[N(L)-N_R^{eq}\right].
\]

The opposite signs are geometric. They are not separate physical conventions.

## 2. Dimensionless contact control

Define the contact Biot number

\[
\mathrm{Bi}_c=\frac{S_cL}{D_n}.
\]

It compares boundary exchange to bulk diffusion across the device length.

- `Bi -> 0`: blocking particle exchange;
- `Bi ~ 1`: comparable bulk and contact resistance;
- `Bi -> infinity`: ideal-reservoir asymptote.

`Bi` does not determine contact noise, barrier physics, interface storage, or material validity.

## 3. Exact zero-field benchmark

For equal boundary potentials, zero screening, and source-free steady transport,

\[
j_n=D_n\frac{N_R-N_L}{L}.
\]

The contact laws give

\[
N_L=N_L^{eq}+\frac{j_n}{S_L},
\qquad
N_R=N_R^{eq}-\frac{j_n}{S_R}.
\]

Eliminating the boundary densities yields

\[
j_n=
\frac{D_n}{L}
\frac{N_R^{eq}-N_L^{eq}}
{1+\mathrm{Bi}_L^{-1}+\mathrm{Bi}_R^{-1}}.
\]

Thus the current relative to the ideal-reservoir value is

\[
\frac{j_n}{j_{ideal}}=
\frac{1}{1+\mathrm{Bi}_L^{-1}+\mathrm{Bi}_R^{-1}}.
\]

The corresponding exact series-resistance fractions are

\[
f_{bulk}=\frac{1}{\mathcal D},
\qquad
f_L=\frac{\mathrm{Bi}_L^{-1}}{\mathcal D},
\qquad
f_R=\frac{\mathrm{Bi}_R^{-1}}{\mathcal D},
\]

with

\[
\mathcal D=1+\mathrm{Bi}_L^{-1}+\mathrm{Bi}_R^{-1}.
\]

## 4. Blocking null mode

When both contacts are exactly blocking and screening is absent, the steady equations conserve total carrier population. Any uniform positive density gives zero current and zero residual. The Jacobian therefore has one population null mode.

This is a physical consequence of the selected ensemble, not a numerical defect. A unique blocking-contact solve requires an additional population constraint, nonzero screening/background coupling, generation-recombination, or a finite exchange rate.

## 5. External series-load control

For the separate linear terminal benchmark, define

\[
\Lambda_Z=\frac{R_s}{R_{device}}.
\]

The current relative to ideal voltage bias is

\[
\frac{I}{I_{V-bias}}=\frac{1}{1+\Lambda_Z}.
\]

This scalar check keeps terminal loading distinct from the contact Biot numbers. It is not yet a coupled circuit solve.

## 6. Accepted boundary

The implemented density-Robin law is a classical deterministic reduction. It does not establish an HgCdTe metal-contact surface velocity or barrier. The source hierarchy still requires electrochemical-potential-based nonlinear exchange, interface-state storage, and stochastic forward/reverse event covariance before quantitative contact claims are authorized.

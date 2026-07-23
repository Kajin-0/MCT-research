# R06 bipolar deterministic finite-volume block

**Date:** 2026-07-23  
**Scope:** dimensionless steady one-dimensional verification model  
**Status:** Phase 1C numerical architecture only

## 1. State and sign convention

The device occupies `0 <= x <= L`. The dimensionless electrostatic potential is `psi`. The positive carrier densities are represented by logarithmic unknowns,

\[
N_i=\exp(\nu_i),
\qquad
P_i=\exp(\pi_i).
\]

The interior state ordering is

\[
u=(\psi_1,\ldots,\psi_m,\nu_1,\ldots,\nu_m,\pi_1,\ldots,\pi_m)^T.
\]

The conventional dimensionless electron and hole currents are

\[
j_n=d_n\left(\partial_xN-N\partial_x\psi\right),
\]

\[
j_p=-d_p\left(\partial_xP+P\partial_x\psi\right).
\]

These definitions preserve the existing R06 electron-current convention. At zero field,

\[
j_n=d_n\partial_xN,
\qquad
j_p=-d_p\partial_xP.
\]

For constant densities in a positive potential gradient, both conventional currents are negative.

## 2. Poisson equation

Let `C` denote the normalized fixed charge density, positive for net ionized donors and negative for net ionized acceptors. The mobile charge density is proportional to `P-N`, so the dimensionless Poisson equation is written

\[
\partial_x^2\psi
-
\Lambda^2(N-P-C)
=0.
\]

Uniform charge neutrality is therefore

\[
N=P+C.
\]

The unipolar equation is recovered by holding `P=P_0` constant and defining

\[
C=N_B-P_0,
\]

which gives

\[
N-P-C=N-N_B.
\]

## 3. Fitted face currents

For face `i+1/2`, define

\[
\Delta\psi_i=\psi_{i+1}-\psi_i,
\qquad
B(z)=\frac{z}{\exp(z)-1}.
\]

The accepted electron face current remains

\[
j_{n,i+1/2}
=
\frac{d_n}{h}
\left[
B(\Delta\psi_i)N_{i+1}
-
B(-\Delta\psi_i)N_i
\right].
\]

Solving the local constant-current hole equation exactly under piecewise-linear potential gives

\[
j_{p,i+1/2}
=
\frac{d_p}{h}
\left[
B(\Delta\psi_i)P_i
-
B(-\Delta\psi_i)P_{i+1}
\right].
\]

The reversed density ordering in the hole expression is required by the hole diffusion sign.

## 4. Conservative residual

For each interior node,

\[
R_{\psi,i}
=
\frac{\psi_{i+1}-2\psi_i+\psi_{i-1}}{h^2}
-
\Lambda^2(N_i-P_i-C),
\]

\[
R_{n,i}
=
\frac{j_{n,i+1/2}-j_{n,i-1/2}}{h},
\]

\[
R_{p,i}
=
\frac{j_{p,i+1/2}-j_{p,i-1/2}}{h}.
\]

The residual ordering is

\[
R=(R_\psi,R_n,R_p)^T.
\]

With no volumetric source terms, each continuity block telescopes independently:

\[
h\sum_iR_{n,i}=j_{n,R}-j_{n,L},
\]

\[
h\sum_iR_{p,i}=j_{p,R}-j_{p,L}.
\]

## 5. Jacobian block structure

The dense verification Jacobian has the structure

\[
J=
\begin{pmatrix}
J_{\psi\psi} & J_{\psi n} & J_{\psi p}\\
J_{n\psi} & J_{nn} & 0\\
J_{p\psi} & 0 & J_{pp}
\end{pmatrix}.
\]

For the present source-free independent-carrier model, electron continuity has no direct derivative with respect to hole density, and hole continuity has no direct derivative with respect to electron density. Coupling occurs through Poisson and the shared potential.

The Poisson density derivatives are

\[
\frac{\partial R_{\psi,i}}{\partial\nu_i}
=-\Lambda^2N_i,
\qquad
\frac{\partial R_{\psi,i}}{\partial\pi_i}
=+\Lambda^2P_i.
\]

All face-current derivatives are assembled into adjacent control-volume rows with opposite signs.

## 6. Electron-hole symmetry

Under

\[
\psi\mapsto-\psi,
\qquad
N\leftrightarrow P,
\qquad
C\mapsto-C,
\qquad
d_n\leftrightarrow d_p,
\]

the residual transforms as

\[
R_\psi\mapsto-R_\psi,
\qquad
R_n\mapsto-R_p,
\qquad
R_p\mapsto-R_n.
\]

Zeros of the residual are therefore preserved. This is an explicit sign-consistency benchmark.

## 7. Exact neutral-resistor solution

For constant `N`, constant `P`, constant `C=N-P`, and affine potential,

\[
\psi(x)=\psi_L+\frac{x}{L}(\psi_R-\psi_L),
\]

Poisson and both continuity residuals vanish exactly. The currents are

\[
j_n=-d_nN\frac{\psi_R-\psi_L}{L},
\]

\[
j_p=-d_pP\frac{\psi_R-\psi_L}{L}.
\]

This provides a mesh-independent bipolar conduction benchmark.

## 8. Claim boundary

This block validates sign, conservation, positivity, symmetry, and Jacobian architecture only. It does not establish quantitative HgCdTe behavior and includes no recombination, traps, illumination, finite-rate contacts, external circuit equation, stochastic source, or terminal PSD.

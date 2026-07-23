# R06 conservative finite-volume residual and Jacobian

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Status:** Phase 1C deterministic prototype specification; no material-accurate HgCdTe calculation

## 1. Scope

This increment defines the smallest executable drift-diffusion-Poisson kernel needed to test conservation, sign conventions, fitted face fluxes, positivity, and Jacobian assembly.

Included:

- one-dimensional uniform mesh;
- dimensionless electrostatic potential;
- one mobile electron population;
- fixed positive background charge;
- ideal fixed-potential, fixed-density reservoirs;
- steady Poisson and electron-continuity residuals;
- Scharfetter-Gummel fitted face current;
- logarithmic density unknowns;
- analytical Jacobian;
- independent current-conservation diagnostics.

Excluded:

- holes;
- traps and recombination;
- optical generation;
- dynamic or stochastic contacts;
- terminal circuit unknowns;
- time dependence;
- stochastic covariance;
- source-controlled HgCdTe material coefficients;
- production nonlinear continuation.

## 2. Dimensionless variables

Let the normalized coordinate be `x` over a domain of length `ell`. The prototype uses

\[
\psi=\frac{q\phi}{k_BT},
\qquad
N=\frac{n}{n_r}.
\]

The electric field convention remains

\[
E=-\frac{\partial\phi}{\partial x}.
\]

The dimensionless electron current is

\[
j_n=d_n\left(\frac{\partial N}{\partial x}-N\frac{\partial\psi}{\partial x}\right),
\]

where `d_n>0` is the electron diffusion coefficient normalized by the selected reference value.

For one mobile electron population with normalized fixed positive background `N_B`, Poisson is

\[
\frac{\partial^2\psi}{\partial x^2}
=
\Lambda^2(N-N_B).
\]

The steady source-free continuity equation is

\[
\frac{\partial j_n}{\partial x}=0.
\]

## 3. Unknowns and positivity

At interior node `i`, the unknowns are

\[
\psi_i,
\qquad
u_i=\ln N_i.
\]

Density is reconstructed as

\[
N_i=e^{\nu_i}>0.
\]

The logarithmic representation prevents Newton iterations from proposing negative carrier density. It does not by itself guarantee global nonlinear convergence.

Boundary values are fixed independently:

\[
\psi_0=\psi_L,
\qquad
\psi_M=\psi_R,
\]

\[
N_0=N_L>0,
\qquad
N_M=N_R>0.
\]

These are ideal-reservoir benchmark conditions, not a complete physical contact model.

## 4. Bernoulli function

Define

\[
B(z)=\frac{z}{e^z-1}.
\]

The implementation uses series expansions near zero and asymptotic branches for large positive and negative arguments. Required identities include

\[
B(-z)=B(z)+z,
\]

and

\[
B(0)=1,
\qquad
B'(0)=-\frac12.
\]

## 5. Fitted electron face current

For face `i+1/2`, let

\[
\Delta\psi_i=\psi_{i+1}-\psi_i.
\]

Assuming piecewise-linear potential and constant current over the interval, exact integration gives

\[
\boxed{
 j_{i+1/2}
 =
 \frac{d_n}{h}
 \left[
 B(\Delta\psi_i)N_{i+1}
 -B(-\Delta\psi_i)N_i
 \right]
 }.
\]

Properties:

1. At zero field,

\[
j_{i+1/2}
=\frac{d_n}{h}(N_{i+1}-N_i).
\]

2. For constant density and linear potential,

\[
j_n=-d_n\frac{\partial\psi}{\partial x},
\]

and the discrete expression is exact on every mesh interval.

3. The same face current is used by adjacent control volumes with opposite signs, so internal fluxes cancel exactly in global balances.

## 6. Residual blocks

For each interior node `i=1,...,M-1`, the Poisson residual is

\[
R_{\psi,i}
=
\frac{\psi_{i+1}-2\psi_i+\psi_{i-1}}{h^2}
-
\Lambda^2(N_i-N_B).
\]

The conservative continuity residual is

\[
R_{n,i}
=
\frac{j_{i+1/2}-j_{i-1/2}}{h}.
\]

The global residual is ordered as

\[
R=
\begin{bmatrix}
R_\psi\\
R_n
\end{bmatrix},
\qquad
u=
\begin{bmatrix}
\psi_{interior}\\
\ln N_{interior}
\end{bmatrix}.
\]

The source-free continuity block obeys the exact telescoping identity

\[
h\sum_{i=1}^{M-1}R_{n,i}
=
j_{M-1/2}-j_{1/2}.
\]

This identity is a structural conservation check independent of nonlinear convergence.

## 7. Analytical Jacobian

The Poisson block is tridiagonal in potential:

\[
\frac{\partial R_{\psi,i}}{\partial\psi_{i-1}}
=\frac1{h^2},
\qquad
\frac{\partial R_{\psi,i}}{\partial\psi_i}
=-\frac2{h^2},
\qquad
\frac{\partial R_{\psi,i}}{\partial\psi_{i+1}}
=\frac1{h^2}.
\]

Because `N_i=e^{\nu_i}`,

\[
\frac{\partial R_{\psi,i}}{\partial\nu_i}
=-\Lambda^2N_i.
\]

For a face with left and right density `N_L,N_R` and potential drop `z`,

\[
\frac{\partial j}{\partial N_L}
=-\frac{d_n}{h}B(-z),
\qquad
\frac{\partial j}{\partial N_R}
=\frac{d_n}{h}B(z),
\]

\[
\frac{\partial j}{\partial z}
=
\frac{d_n}{h}
\left[B'(z)N_R+B'(-z)N_L\right].
\]

Potential derivatives follow from

\[
z=\psi_R-\psi_L,
\]

and log-density derivatives multiply the density derivative by the local density.

The prototype assembles a dense Jacobian for transparent verification. A production implementation should preserve the same block derivatives in sparse form.

## 8. Independent diagnostics

Current conservation is not inferred only from the continuity residual. The converged or candidate state is reconstructed and every face current is recomputed independently.

Define

\[
\epsilon_I
=
\frac{\max(j)-\min(j)}
{\max(1,\max|j|)}.
\]

For the exact uniform-resistor benchmark, the target is machine-level variation. For later nonlinear cases, the Phase 1 target remains

\[
\epsilon_I<10^{-8}
\]

after convergence and mesh verification.

## 9. Exact benchmark states

### 9.1 Thermal equilibrium

For

\[
\psi=0,
\qquad
N=N_B=1,
\]

both residual blocks vanish exactly up to floating-point roundoff.

### 9.2 Uniform resistor

For fixed boundary density

\[
N_L=N_R=N_B=1
\]

and linear potential

\[
\psi(x)=-Ux/\ell,
\]

Poisson and continuity residuals vanish and

\[
j_n=d_n\frac{U}{\ell}
\]

at every face under the project voltage orientation.

This is the first biased deterministic benchmark. It does not require an HgCdTe material parameter set.

## 10. Validation completed locally

The combined statistics and finite-volume prototypes pass 46 focused local tests. New finite-volume tests cover:

- Bernoulli symmetry and derivative;
- log-density positivity;
- exact uniform equilibrium;
- exact uniform-resistor current;
- zero-field diffusion limit;
- analytical Jacobian against centered finite differences;
- telescoping continuity balance;
- invalid configuration rejection.

GitHub Actions remains the repository-level authority after commit.

## 11. Next extensions

The next deterministic extensions, in order, are:

1. sparse Jacobian representation without changing derivatives;
2. a damped Newton solve for the exact uniform benchmarks;
3. nonuniform fixed background and mesh-refinement checks;
4. bipolar electron-hole residuals;
5. equilibrium charge neutrality through the selected statistics interface;
6. finite circuit unknowns;
7. reaction and trap residuals;
8. stochastic linearization only after deterministic conservation gates pass.

No material-accurate HgCdTe prediction is authorized by this prototype.
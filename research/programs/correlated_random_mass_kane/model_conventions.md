# R05 minimal model and convention specification

**Controlling issue:** #390  
**Status:** conventions frozen for the PR 2 oracle unless amended before implementation

## 1. Repository-to-minimal-model mapping

The repository homogeneous Kane implementation uses:

```text
basis: Gamma6(+/-1/2), Gamma8(+3/2,+1/2,-1/2,-3/2), Gamma7(+/-1/2)
k: inverse angstrom
energy: eV
Kane coupling: eV angstrom
signed gap: Eg = E_Gamma6 - E_Gamma8
```

The first R05 oracle is not an 8-band spatial Hamiltonian. It is a symmetric two-component Dirac benchmark:

\[
H=-i\hbar v_K\sigma_x\partial_x+M(x)\sigma_z.
\]

The mapping is

\[
M=E_g/2.
\]

Thus positive `M` is the normal ordering and negative `M` is the inverted ordering under the repository signed-gap convention.

## 2. Matrix representation

Use

\[
\alpha=\sigma_x,
\qquad
\beta=\sigma_z.
\]

The chiral/spectral-symmetry operator is

\[
\Gamma=\sigma_y,
\qquad
\{H,\Gamma\}=0.
\]

For every eigenvalue `E`, the declared model therefore has a partner `-E`, up to numerical tolerance and zero-mode handling.

This symmetry is a property of the minimal model. Electron-hole asymmetry and the heavy-hole sector are deliberately absent.

## 3. Physical and dimensionless variables

Physical variables:

```text
x_coordinate: nm
M, Mbar, sigma_M, E: eV
v_K: m/s
hbar v_K: eV nm
xi, L, a: nm
DOS: states / (eV nm) per two-component species
```

Dimensionless variables:

\[
u=x/\xi,
\qquad
\varepsilon=E\xi/(\hbar v_K),
\qquad
m=\overline M\xi/(\hbar v_K),
\qquad
g=\sigma_M\xi/(\hbar v_K).
\]

In dimensionless form,

\[
\mathcal H=H\xi/(\hbar v_K)
=-i\sigma_x\partial_u+[m+g\eta(u)]\sigma_z,
\]

where `eta` has zero mean and unit point variance.

## 4. Spatial dimension and interpretation

The mandatory first oracle is 1D.

It is used to:

- test the matched scalar null;
- verify limiting cases;
- identify coherent sign-change mechanisms;
- determine numerical requirements;
- estimate the parameter scale required for a measurable distinction.

It is not a quantitative bulk HgCdTe prediction. A 2D or 3D interpretation requires a separate gate.

## 5. Domain and boundary conditions

Primary domain:

```text
x in [0,L)
periodic boundary condition
```

Mandatory boundary cross-check:

```text
antiperiodic boundary condition
```

Boundary-condition averaging is required near zero energy because a periodic massless homogeneous system contains a `k=0` level while the antiperiodic system does not.

## 6. Ultraviolet regularization

Primary regularization: Fourier pseudospectral derivative.

For `N` equally spaced points,

```text
a = L/N
k_max = pi/a
```

The derivative is diagonal in the discrete Fourier basis. The kinetic operator is transformed to real space or applied matrix-free.

Reasons for this choice:

- exact derivative for represented Fourier modes;
- explicit ultraviolet cutoff;
- no hidden naive-central-difference fermion doubler;
- simple exact homogeneous reference spectrum.

A Wilson or staggered local discretization may be added only as an independent regularization comparison.

## 7. Homogeneous spectrum

For constant `M`,

\[
E_\pm(k)=\pm\sqrt{(\hbar v_K k)^2+M^2}.
\]

Periodic momenta:

\[
k_n=2\pi n/L.
\]

Antiperiodic momenta:

\[
k_n=2\pi(n+1/2)/L.
\]

These finite-box eigenvalues are the primary exact reference.

## 8. Disorder marginal

Primary marginal:

\[
M(x)\sim\mathcal N(\overline M,\sigma_M^2).
\]

The scalar null and correlated model must use the same declared marginal.

A bounded or non-Gaussian marginal is a robustness test, not the primary result.

## 9. Covariance conventions

Primary Gaussian covariance:

\[
C_G(r)=\exp[-r^2/(2\xi^2)].
\]

Here `xi` is the coordinate standard-deviation parameter of the covariance and `C_G(0)=1`.

Robustness families:

```text
Matern nu = 1/2
Matern nu = 3/2
Matern nu = 5/2
```

The Matérn length convention must match `spatial_disorder_covariance_families.py`.

## 10. Field-generation conventions

A periodic Gaussian field is generated from the discrete nonnegative power spectrum.

Required metadata:

```text
seed
N
L
a
xi
Mbar
sigma_M
covariance family
power-spectrum convention
mean-removal choice
variance-renormalization choice
realized mean
realized variance
realized covariance diagnostic
```

Two ensembles must be distinguishable:

1. raw finite-periodic Gaussian field;
2. per-realization mean-removed and/or variance-normalized field.

Per-realization normalization is not silently applied because it suppresses ensemble fluctuations and alters low-wave-number statistics.

## 11. Density-of-states convention

For eigenvalues `E_j`, the numerical DOS is

\[
\rho_\eta(E)=\frac{1}{L}\sum_j K_{\eta_{\rm num}}(E-E_j),
\]

where `K` is a normalized kernel.

Primary numerical kernel: Gaussian.

\[
K_\eta(E)=\frac{1}{\sqrt{2\pi}\eta}
\exp[-E^2/(2\eta^2)].
\]

The DOS is per unit length and per two-component species.

## 12. Scalar null convention

Infinite-volume homogeneous DOS:

\[
\rho_{\rm hom}(E;M)=
\frac{|E|}{\pi\hbar v_K\sqrt{E^2-M^2}}
\Theta(|E|-|M|).
\]

Matched scalar mixture:

\[
\rho_{\rm scalar}(E)=
\int dM\,P(M)\rho_{\rm hom}(E;M).
\]

Two implementations are mandatory:

- analytic/adaptive quadrature followed by numerical broadening;
- finite-box homogeneous Monte Carlo using the same mass samples and spectral kernel as the correlated calculation.

The null implementations must agree before any correlated-minus-null effect is accepted.

## 13. Broadening and experimental convolution

Keep separate:

```text
eta_num: numerical estimator width
delta_E_exp: experimental resolution width
```

Workflow:

```text
raw converged model DOS
-> residual eta_num convergence
-> experimental convolution
-> effect-size statistic
```

Experimental resolution must not be used to stabilize an unconverged numerical spectrum.

## 14. Degeneracy convention

The minimal result includes no multiplicative physical degeneracy.

Any mapping to HgCdTe must derive:

- spin/Kramers counting;
- cone or valley counting;
- heavy-hole contribution;
- optical matrix-element weights.

No degeneracy multiplier may be chosen merely to match a measured amplitude.

## 15. Input validation

Implementation must reject:

- nonfinite parameters;
- `v_K <= 0`;
- `xi <= 0`;
- `L <= 0`;
- `N < 4` or incompatible grid sizes;
- `sigma_M < 0`;
- negative numerical broadening;
- covariance spectra with materially negative eigenvalues;
- energy windows beyond the validated ultraviolet fraction.

No silent clipping or absolute-value correction is permitted.

## 16. Validated regime warning

Every solver result must report

```text
a/xi
L/xi
eta_num xi/(hbar v_K)
max_abs_E / (hbar v_K k_max)
```

and warn or fail when outside the predeclared convergence regime.

## 17. Full-Kane boundary

The minimal model omits:

- heavy-hole flat-band DOS;
- split-off band;
- electron-hole asymmetry;
- anisotropic/multiple velocities;
- spatial variation of Kane coupling or band offsets;
- magnetic field and optical matrix elements.

These omissions are acceptable for the first matched-null mechanism test, but not automatically for experimental HgCdTe prediction.
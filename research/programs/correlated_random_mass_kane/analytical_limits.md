# R05 Phase 0 analytical limits and mechanism tests

**Controlling issue:** #390  
**Model:** one-dimensional two-component random-mass Dirac benchmark  
**Evidence class:** exact model consequences and predeclared numerical validation targets; not HgCdTe material validation

## 1. Declared Hamiltonian and symmetry

The minimal oracle is

\[
H=-i\hbar v_K\sigma_x\partial_x+M(x)\sigma_z.
\]

With

\[
\Gamma=\sigma_y,
\]

both Pauli terms anticommute with `Gamma`, so

\[
\{H,\Gamma\}=0.
\]

Therefore every nonzero eigenvalue has a partner of opposite sign:

\[
H\psi=E\psi
\quad\Longrightarrow\quad
H(\Gamma\psi)=-E(\Gamma\psi).
\]

### Numerical test

For every realization, require

```text
Hermiticity residual < 1e-12 relative Frobenius norm
maximum paired-spectrum residual < 1e-10 in dimensionless energy
```

for exact diagonalization sizes. A sparse estimator must reproduce the same symmetry statistically and on overlapping exact-reference sizes.

## 2. Homogeneous limit

For constant mass `M`, plane waves give

\[
E_\pm(k)=\pm\sqrt{(\hbar v_K k)^2+M^2}.
\]

For a periodic interval `L`,

\[
k_n=\frac{2\pi n}{L};
\]

for antiperiodic boundaries,

\[
k_n=\frac{2\pi(n+1/2)}{L}.
\]

The infinite-volume DOS per unit length and per two-component Dirac species is

\[
\rho_{\rm hom}(E;M)=
\frac{|E|}{\pi\hbar v_K\sqrt{E^2-M^2}}
\Theta(|E|-|M|).
\]

For `M=0`,

\[
\rho_{\rm hom}(E;0)=\frac{1}{\pi\hbar v_K}
\]

away from the finite-box zero-mode convention.

### Required tests

1. `sigma_M=0` reproduces the exact finite-box eigenvalues.
2. Broadened finite-box DOS converges to the analytic DOS as `L` increases and numerical broadening decreases in a coordinated sequence.
3. Integrated spectral weight equals the represented Hilbert-space state count to the kernel-quadrature tolerance.

## 3. Matched scalar-mixture null

For mass marginal `P(M)`,

\[
\rho_{\rm scalar}(E)
=\int_{-|E|}^{|E|}dM\,
P(M)
\frac{|E|}{\pi\hbar v_K\sqrt{E^2-M^2}}.
\]

With `M=|E| sin(theta)`, this becomes the nonsingular reference integral

\[
\rho_{\rm scalar}(E)
=\frac{|E|}{\pi\hbar v_K}
\int_{-\pi/2}^{\pi/2}
P\!\left(|E|\sin\theta\right)d\theta.
\]

This form should be used for quadrature near the homogeneous band-edge singularity.

### 3.1 Universal small-energy scalar-null behavior

If `P(M)` is continuous at zero with finite `P(0)`,

\[
\rho_{\rm scalar}(E)
=\frac{|E|P(0)}{\hbar v_K}+O(|E|^3).
\]

Thus a smooth scalar local-gap mixture vanishes linearly at zero energy even when it contains both signs of mass.

For a Gaussian marginal,

\[
P(0)=
\frac{1}{\sqrt{2\pi}\sigma_M}
\exp\left[-\frac{\overline M^2}{2\sigma_M^2}\right].
\]

This linear low-energy law is a strong null-model diagnostic. A correlated model that produces stable excess zero-energy spectral weight must still pass finite-size, boundary, broadening, and measurement-convolution tests before it is interpreted physically.

### 3.2 Exact zero-mean Gaussian scalar null

For `Mbar=0`, define

\[
q=\frac{E^2}{4\sigma_M^2}.
\]

The scalar mixture reduces to

\[
\rho_{\rm scalar}(E)
=
\frac{|E|}{\hbar v_K\sqrt{2\pi}\sigma_M}
\exp(-q)I_0(q),
\]

where `I_0` is the modified Bessel function. This gives an independent exact reference for the numerical quadrature.

### Required tests

```text
adaptive theta-quadrature vs exact zero-mean Gaussian formula: relative error < 1e-10
finite-box homogeneous Monte Carlo vs broadened quadrature: discrepancy below combined finite-size and sampling uncertainty
small-E slope vs P(0)/(hbar v_K): relative error < 1% in a predeclared asymptotic window
```

## 4. Long-correlation or semiclassical limit

When the mass varies slowly relative to the local propagation scale,

\[
\xi\gg \ell_E,
\qquad
\ell_E=\frac{\hbar v_K}{\max(|E|,\eta_{\rm num})},
\]

the leading local-density approximation is

\[
\rho_{\rm LDA}(E)
=\frac{1}{L}\int_0^L dx\,\rho_{\rm hom}(E;M(x)).
\]

Ensemble averaging a stationary field gives

\[
\langle\rho_{\rm LDA}(E)\rangle
=\int dM\,P(M)\rho_{\rm hom}(E;M)
=\rho_{\rm scalar}(E).
\]

Therefore finite correlation length is not sufficient by itself to generate a non-scalar effect. The distinction must arise from spatial gradients, coherent propagation across sign-changing regions, interface-state hybridization, or another nonlocal mechanism omitted by LDA.

No universal coefficient for the gradient correction is asserted here. The numerical oracle must establish its scaling and covariance dependence.

### Falsification test

At fixed marginal distribution and increasing `xi/L_E`, the correlated DOS must approach the scalar mixture outside an explicitly identified interface-dominated low-energy window. Failure to approach the null at energies well away from interfaces indicates finite-size, cutoff, field-generation, or estimator error.

## 5. Short-correlation limit

For one-dimensional Gaussian covariance

\[
\langle\delta M(0)\delta M(r)\rangle
=\sigma_M^2\exp[-r^2/(2\xi^2)],
\]

the integrated disorder strength is

\[
W
=\int_{-\infty}^{\infty}dr\,
\langle\delta M(0)\delta M(r)\rangle
=\sqrt{2\pi}\,\sigma_M^2\xi.
\]

Two inequivalent limits must be tested.

### 5.1 Fixed point variance

If `sigma_M` is fixed while `xi -> 0`,

\[
W\rightarrow0.
\]

The disorder becomes weak in integrated strength and the model should converge toward the homogeneous mean-mass system, subject to ultraviolet resolution.

### 5.2 Fixed integrated disorder

If `W` is fixed while `xi -> 0`,

\[
\sigma_M^2=\frac{W}{\sqrt{2\pi}\xi}
\rightarrow\infty.
\]

This is the white-noise scaling limit. The point variance diverges, and the grid must satisfy `a/xi << 1` before the limit is extrapolated.

Under this scaling,

\[
g=\frac{\sigma_M\xi}{\hbar v_K}
=\frac{1}{\hbar v_K}
\sqrt{\frac{W\xi}{\sqrt{2\pi}}}
\rightarrow0,
\]

so `g` alone is not a complete classifier of the fixed-`W` white-noise limit. The dimensionless integrated coupling

\[
w=\frac{W}{(\hbar v_K)^2}
\]

must also be reported.

### Falsification test

A claimed `xi -> 0` result is invalid unless it states whether `sigma_M` or `W` is held fixed and demonstrates independent convergence in `a/xi` and ultraviolet cutoff.

## 6. Large mean-mass limit

For a Gaussian marginal, the probability that a local mass has the sign opposite to the mean is

\[
p_{\rm opp}
=\frac12\operatorname{erfc}
\left(
\frac{|\overline M|}{\sqrt2\sigma_M}
\right).
\]

For

\[
|\overline M|/\sigma_M\gg1,
\]

sign-changing intervals are exponentially suppressed. In this regime the correlated and scalar models should agree after matched broadening except for perturbative gradient corrections.

### Required sweep

Include at least

```text
|Mbar|/sigma_M = 0, 0.5, 1, 2, 3, 5
```

and verify that the non-scalar low-energy effect decreases consistently with the loss of sign-changing structure. A persistent large effect at `|Mbar|/sigma_M = 5` requires an identified non-interface mechanism.

## 7. Mean-massless limit

At

\[
\overline M=0,
\]

the ensemble is symmetric under `M -> -M` for a symmetric marginal. This does not add a new single-realization symmetry beyond the spectral symmetry already present.

Near zero energy, the calculation is especially sensitive to:

- periodic zero modes;
- paired domain-wall states;
- finite-box domain count;
- numerical broadening;
- rare realization weighting;
- arithmetic underflow in DOS ratios.

### Required controls

```text
periodic and antiperiodic boundaries
median and mean across realizations
independent seed batches
raw low-energy integrated state count
broadening ladder
system-length ladder at fixed L/xi
```

A mean-only DOS curve is insufficient because rare realizations can dominate the average.

## 8. Isolated sign-changing wall

Use the deterministic profile

\[
M(x)=M_0\tanh(x/w),
\qquad M_0>0.
\]

At zero energy,

\[
\left[
-i\hbar v_K\sigma_x\partial_x
+M(x)\sigma_z
\right]\psi=0.
\]

Multiplying by `sigma_x` gives

\[
\hbar v_K\partial_x\psi+M(x)\sigma_y\psi=0.
\]

For `sigma_y chi_+=chi_+`,

\[
\psi_0(x)
\propto
\exp\left[-\frac{1}{\hbar v_K}
\int_0^xM(x')dx'\right]\chi_+
\]

and therefore

\[
\psi_0(x)
\propto
\left[\cosh(x/w)\right]^{-M_0w/(\hbar v_K)}\chi_+.
\]

This is normalizable because the mass changes sign. The characteristic asymptotic localization length is

\[
\ell_{\rm wall}=\frac{\hbar v_K}{M_0}.
\]

### Numerical test

For a sufficiently isolated wall pair in a periodic box:

- recover two near-zero states whose splitting decreases exponentially with wall separation;
- recover the analytical envelope away from the partner wall;
- verify spectral symmetry and normalization;
- demonstrate that a same-sign mass profile does not produce the corresponding zero mode.

This is a mechanism benchmark only. It does not establish a topological invariant, percolating network, or measurable HgCdTe domain-wall transport.

## 9. Interface-density screening estimate

For a differentiable stationary zero-mean Gaussian mass fluctuation with covariance `R(r)`, Rice's formula gives the expected crossing density of the level `-Mbar` as

\[
\nu_0
=\frac{1}{\pi}
\sqrt{-\frac{R''(0)}{R(0)}}
\exp\left[-\frac{\overline M^2}{2\sigma_M^2}\right].
\]

For the declared Gaussian covariance,

\[
R(r)=\sigma_M^2e^{-r^2/(2\xi^2)},
\qquad
-R''(0)/R(0)=1/\xi^2,
\]

so

\[
\nu_0
=\frac{1}{\pi\xi}
\exp\left[-\frac{\overline M^2}{2\sigma_M^2}\right].
\]

This provides a pre-simulation check on the number of sign changes in a finite box. It is not itself a DOS prediction. Matérn `nu=1/2` is not differentiable, so this crossing formula does not apply without regularization.

## 10. Numerical sum and scale checks

Every saved reference must report:

```text
trace(H) and expected trace
Hermiticity residual
paired-spectrum residual
integrated DOS spectral weight
realized mass mean and variance
realized zero-crossing count
Rice crossing-density expectation where applicable
a/xi
L/xi
eta_num xi/(hbar v_K)
max_abs_E/(hbar v_K k_max)
```

## 11. Predeclared mechanism decision

A non-scalar DOS effect is mechanism-supported only if all are true:

1. the scalar-null exact references pass;
2. the homogeneous and LDA limits pass;
3. the effect tracks sign-changing or gradient structure in a controlled way;
4. it is stable under boundary, size, spacing, broadening, seed, and covariance checks;
5. it remains after plausible experimental convolution;
6. it is not explained by unmatched marginals or per-realization normalization.

Otherwise the apparent effect is classified as a numerical artifact, null-model defect, or model-conditioned curiosity rather than an R05 physical result.
# Program state: measurement-kernel-aware spatial disorder

**Portfolio contribution:** R04  
**State:** active-result and candidate work; manuscript gate not yet passed

## Objective

Determine how a spatially correlated HgCdTe composition field combines with finite lateral and depth measurement kernels to control apparent composition variance, gap width, optical response, and detector cutoff.

## Controlling issues

- #196 — scale-dependent spatial-disorder theorem and replacement scientific core;
- #215 — probe-scale calibration limits in multiscale disorder inference;
- #218 — three-scale covariance-family falsification;
- #220 — exact nonlinear common-scale posterior propagation;
- #224 — Gaussian-surrogate bias and pairwise drift under covariance misspecification;
- #228 — composite optical, pixel, and finite-depth instrument kernel.

## Completed foundations

Merged or current implementation tranches include:

- PR #199 — Gaussian covariance and Gaussian-kernel core;
- PR #202 — finite-depth kernels and slab limits;
- PR #204 — multiscale Fisher and recoverability diagnostics;
- PR #207 — lateral transmission operation-order benchmark;
- PR #210 — detector-cutoff operation-order benchmark;
- PR #212 — end-to-end multiscale disorder-to-cutoff design;
- PR #216 — probe-scale calibration theorem and nuisance marginalization;
- PR #219 — reciprocal-linearity family test and half-integer Matérn alternatives;
- PR #221 — exact nonlinear posterior factorization and bounded-prior failure;
- PR #227 — pairwise Gaussian-parameter drift and global-surrogate bias extension;
- PR #229 — composite optical-PSF, pixel, and absorption-depth kernel.

Representative modules:

```text
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_depth.py
src/mct_research/spatial_disorder_inference.py
src/mct_research/spatial_disorder_theorems.py
src/mct_research/spatial_disorder_optics.py
src/mct_research/spatial_disorder_cutoff.py
src/mct_research/spatial_disorder_design.py
src/mct_research/spatial_disorder_calibration.py
src/mct_research/spatial_disorder_covariance_families.py
src/mct_research/spatial_disorder_covariance_bias.py
src/mct_research/spatial_disorder_instrument.py
src/mct_research/spatial_disorder_posterior.py
```

Established within declared models:

- exact covariance filtering by normalized kernels;
- one-scale non-identifiability of point variance and correlation length;
- exact two-scale inversion and conditioning diagnostics;
- finite-depth analytical benchmarks;
- Jensen-consistent transmission and cutoff operation ordering;
- controlled forward prediction from probe scale to filtered gap width and cutoff;
- exact confounding of common multiplicative probe calibration with correlation length;
- analytical marginalization of arbitrary Gaussian log-probe calibration modes;
- exact reciprocal-linearity condition for the Gaussian covariance/probe family;
- stable Gaussian-probe filtering for Matérn `nu=1/2, 3/2, 5/2` alternatives;
- pairwise scale-selection drift and fitting-convention-dependent Gaussian-surrogate bias under covariance misspecification;
- exact lateral filtering for an axis-aligned elliptical Gaussian PSF convolved with rectangular pixel integration;
- separable composition of lateral and finite-depth instrument factors;
- first-order propagation of PSF, pixel, absorption, and thickness calibration covariance;
- exact nonlinear convolution of the relative correlation-length posterior with an independent common-scale calibration prior.

## Probe-scale calibration result

For the Gaussian benchmark

$$
V(s)=\frac{A}{1+2s^2/\xi^2},
$$

$$
\frac{\partial V}{\partial\log s}
=-\frac{\partial V}{\partial\log\xi}.
$$

A common multiplicative probe-scale error is indistinguishable from the opposite change in correlation length. If the common log-scale calibration prior has variance $\tau_s^2$, the local covariance of $(\log A,\log\xi)$ gains exactly

$$
\begin{pmatrix}
0&0\\
0&\tau_s^2
\end{pmatrix}.
$$

Independent or shape-changing probe errors can degrade both recovered parameters.

## Exact nonlinear posterior result

Define

$$
u=\log A,
\qquad
v=\log\xi,
\qquad
\lambda=v-\delta,
$$

where $\delta$ is a common log-scale calibration error. Any likelihood whose scale dependence enters only through $s_i e^\delta/\xi$ depends on $(u,\lambda)$ rather than on $v$ and $\delta$ separately.

With an independent calibration prior and translation-invariant absolute log-length support,

$$
\boxed{
p(u,\lambda,\delta\mid y)
=
p(u,\lambda\mid y)p_\delta(\delta).
}
$$

Therefore

$$
\boxed{
\kappa_n(v)=\kappa_n(\lambda)+\kappa_n(\delta)
}
$$

for every existing cumulant. In particular,

$$
\operatorname{Var}(v)
=
\operatorname{Var}(\lambda)+\operatorname{Var}(\delta),
$$

and

$$
\operatorname{Cov}(u,v)
=
\operatorname{Cov}(u,\lambda).
$$

This promotes the common-scale calibration floor from a local Fisher statement to an exact nonlinear posterior result under explicit assumptions.

For the declared synthetic log-Gaussian design, the relative Frobenius error between nonlinear posterior covariance and local Fisher covariance is:

```text
relative observation uncertainty     covariance error
1%                                   1.98e-5
5%                                   4.95e-4
15%                                  4.40e-3
30%                                  1.66e-2
```

The Fisher approximation remains accurate to 1.66% even at 30% relative uncertainty for this specific scale layout and likelihood.

A broad direct three-dimensional calculation closes the variance-addition identity to `1.73e-18`. A narrow absolute log-length prior with `14.08%` boundary mass creates:

```text
posterior calibration total variation    0.06954
Cov(lambda,delta)                        -8.41e-4
variance-addition residual               -4.576e-3
cross-covariance residual                 9.04e-4
```

Thus the exact identity must not be applied when an informative or bounded absolute-length prior is active near its support boundary.

## Covariance-family result

The Gaussian benchmark obeys

$$
\boxed{
\frac{1}{V(s)}
=\frac{1}{A}+\frac{2}{A\xi^2}s^2.
}
$$

Thus two admissible scales recover two Gaussian parameters but cannot test the covariance family. A third scale must lie on the same reciprocal line. For ordered scales,

$$
\boxed{
\frac{V_3^{-1}-V_2^{-1}}{s_3^2-s_2^2}
-
\frac{V_2^{-1}-V_1^{-1}}{s_2^2-s_1^2}
=0.
}
$$

For the dimensionless design

```text
s/ell = [0.1, 1, 2]
relative variance uncertainty = 3%
```

forcing the Gaussian family through the endpoint scales gives:

```text
true family       middle prediction error      standardized residual
Matern nu=1/2          17.482%                         4.120
Matern nu=3/2           8.086%                         2.012
Matern nu=5/2           5.207%                         1.319
```

The rough family is distinguishable at this uncertainty; the smoothest family is not. Failure to reject Gaussian covariance does not establish Gaussian covariance.

## Covariance-family bias extension

The family test above answers whether Gaussian covariance can be rejected. PR #227 separately quantifies what is reported when a Gaussian inverse is still imposed.

For each scale pair $(i,j)$, the exact Gaussian two-scale theorem returns $(A_{ij},\xi_{ij})$. Exact Gaussian data give one common pair. Under misspecification, the values drift with scale selection.

For the broad controlled design

```text
A = 0.01
ell = 2
s = [0, 0.5, 2, 8, 20]
```

the diagnostics are:

```text
true family       pairwise A spread    pairwise xi spread    A_fit/A    xi_fit/ell    RMS log error
Gaussian               1.000                 1.000             1.0000       1.0000        <3e-13
Matern nu=1/2          2.820                 3.418             0.8351       1.0406         0.1388
Matern nu=3/2          1.630                 1.734             0.9441       1.0084         0.0516
Matern nu=5/2          1.381                 1.417             0.9678       1.0035         0.0317
```

For the exponential covariance, different scale pairs therefore report Gaussian correlation lengths spanning a factor of approximately `3.42`, while the equal-weight log-variance surrogate underestimates point variance by approximately `16.5%`.

This extension does not duplicate the reciprocal-linearity test. It adds scale-selection and fitting-convention sensitivity after family misspecification is present. Pairwise spreads are diagnostics, not confidence intervals, and the global bias depends on the declared fitting loss and weights.

## Composite instrument-kernel result

PR #229 replaces one nominal Gaussian width with the declared separable kernel

```text
elliptical Gaussian optical PSF
convolved with rectangular pixel or scan-bin integration
multiplied by finite-slab exponential depth weighting
```

For one lateral axis with Gaussian correlation length $\xi$, PSF width $\sigma$, pixel width $p$, and

$$
L^2=\xi^2+2\sigma^2,
$$

the exact attenuation is

$$
\boxed{
F(\xi,\sigma,p)
=
\frac{\xi}{L}
\frac{2}{p^2}
\left[
 pL\sqrt{\frac{\pi}{2}}
 \operatorname{erf}\left(\frac{p}{\sqrt{2}L}\right)
 +L^2\operatorname{expm1}\left(-\frac{p^2}{2L^2}\right)
\right].
}
$$

For axis-aligned separable Gaussian covariance,

$$
\frac{\operatorname{Var}(X_w)}{A}=F_xF_yF_z,
$$

where $F_z$ is evaluated by the established finite-slab depth quadrature.

For the controlled reference case

```text
xi = [2, 2, 2]
PSF sigma = [2, 2]
pixel width = [5, 5]
alpha = 0.5
thickness = 10
```

```text
exact measured / point variance       0.16258
equivalent-Gaussian relative error    1.116%
instrument calibration relative SD    5.35%
```

A declared 42-case dimensionless stress grid has 18 cases above 1% equivalent-Gaussian error and a maximum error of `9.045%` in a pixel-dominated regime. A separate pixel-dominated reference gives `8.876%` error.

The exact model therefore survives the termination criterion as more than a purely formal correction. However, the synthetic calibration budget is larger than the shape-reduction error in the reference case, so actual PSF and depth calibration remain necessary.

This result is restricted to axis-aligned separable Gaussian covariance and lateral kernels. It does not establish a rotated or nonseparable kernel theorem, a universal PSF, or a specimen parameter.

## Unresolved scientific questions

- whether available HgCdTe data contain enough multi-resolution information to estimate a correlation length;
- whether experimentally achievable uncertainty resolves Gaussian versus smooth Matérn covariance;
- how rotated, aberrated, or otherwise nonseparable lateral kernels change the declared benchmark;
- whether a real instrument PSF, pixel geometry, absorption coefficient, and thickness can be calibrated tightly enough for inversion;
- whether the predicted scale effect survives thickness, carrier, defect, calibration, covariance-family, fitting-convention, and operation-order nuisance variables jointly;
- whether distinct measurement modalities can be predicted from one latent spatial field;
- whether the full contribution is sufficiently distinct from existing finite-aperture mapping and random-field literature.

## Manuscript status

No manuscript is currently authorized. A candidate paper becomes writeable only after:

1. full-text prior-art audit;
2. one public-data or experimentally specified validation path;
3. an experimentally specified instrument kernel and calibrated scale range;
4. combined calibration, covariance-family, thickness, and observation-operator stress testing;
5. a concise theorem-centered figure and claim plan.

The local-to-nonlinear common-calibration gate, covariance-family stress-test gate, and controlled representative-instrument-kernel gate are completed. The experimental kernel-calibration and joint-nuisance gates remain open.

## Authorized next gates

- complete full-text audits for the highest-priority finite-aperture sources;
- obtain or declare one experimentally specified PSF, pixel geometry, thickness, and absorption-depth model;
- combine instrument calibration, covariance-family, fitting-convention, and observation-operator uncertainty in one design calculation;
- test whether distinct modalities can be predicted from one latent field;
- identify one public-data or experimentally specified validation path.

## Unsupported claims

This program does not currently support:

- a specimen-specific correlation length;
- a universal Gaussian or Matérn covariance law;
- a universal Gaussian optical PSF or rectangular-pixel model;
- replacing a measured point-spread function with nominal pixel pitch;
- interpreting a low reciprocal-linearity residual as proof of Gaussian covariance;
- interpreting pairwise parameter spread as a statistical confidence interval;
- reporting a misspecified Gaussian parameter without declaring the fitting loss and scale design;
- treating a moment-matched Gaussian as exact outside a verified regime;
- applying the exact common-scale convolution when an active bounded absolute-length prior couples $\lambda$ and $\delta$;
- identifying optical tail energy with microscopic composition variance;
- treating controlled cutoff shifts as measured detector behavior;
- treating every local Fisher covariance as globally accurate outside the tested design;
- a topological or random-mass Kane conclusion;
- manuscript submission readiness.

## Shared dependencies

This program uses empirical gap slopes, distributional absorption and cutoff operators, literature records, and validation infrastructure shared with other works.

The covariance-family, bias, instrument, and posterior modules are additive shared infrastructure. They reuse existing Gaussian prediction, recovery, depth filtering, family filtering, and calibration definitions without changing their numerical behavior.

## Stage-2 boundary

Correlated random-mass Kane physics is a separate program. It is not automatically activated by progress in this workstream.

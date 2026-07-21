# Three-scale closure for covariance-family misspecification

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issues:** #196, #224  
**Status:** exact model-closure theorem plus controlled synthetic stress test

## 1. Purpose

The Gaussian covariance/Gaussian-probe model has two unknown parameters:

- point variance $A$;
- correlation length $\xi$.

Two scale-dependent variance measurements can determine two parameters, but that does not test whether the Gaussian covariance family is correct. This note derives the first exact family-closure test and quantifies the bias produced when a Gaussian inverse is applied to equal-area exponential and Matérn covariance fields.

The result is model-conditioned. It does not identify a covariance family for HgCdTe.

## 2. Filtered variance under a Gaussian probe

Let $x(\mathbf r)$ be a zero-mean stationary isotropic field with covariance

$$
C(r)=A\,c(r/\xi),
$$

where $A=C(0)$ and $c(0)=1$.

For a normalized two-dimensional Gaussian probe,

$$
w_s(\mathbf r)
=
\frac{1}{2\pi s^2}
\exp\!\left(-\frac{|\mathbf r|^2}{2s^2}\right),
$$

the filtered observable is

$$
X_s=\int w_s(\mathbf r)x(\mathbf r)\,d^2r.
$$

Its variance is

$$
V(s)
=
\iint
w_s(\mathbf r)w_s(\mathbf r')
C(|\mathbf r-\mathbf r'|)
\,d^2r\,d^2r'.
$$

The displacement of two independent draws from $w_s$ is Gaussian with covariance $2s^2I$. Its radial magnitude has density

$$
p_s(r)=\frac{r}{2s^2}\exp\!\left(-\frac{r^2}{4s^2}\right).
$$

Therefore

$$
\frac{V(s)}{A}
=
\int_0^\infty
\frac{r}{2s^2}
\exp\!\left(-\frac{r^2}{4s^2}\right)
c(r/\xi)\,dr.
$$

With $r=2sy$,

$$
\boxed{
\frac{V(s)}{A}
=
\int_0^\infty
2y e^{-y^2}
c\!\left(2\frac{s}{\xi}y\right)dy
}
$$

so the attenuation depends only on the ratio $s/\xi$.

## 3. Equal-area covariance convention

The controlled families are normalized to the same point variance and the same two-dimensional integral correlation area:

$$
\int_{\mathbb R^2}\frac{C(r)}{C(0)}\,d^2r
=
2\pi\xi^2.
$$

The dimensionless radial forms are

$$
c_G(\rho)=e^{-\rho^2/2},
$$

$$
c_E(\rho)=e^{-\rho},
$$

$$
c_{3/2}(\rho)
=
(1+\sqrt{3}\rho)e^{-\sqrt{3}\rho},
$$

and

$$
c_{5/2}(\rho)
=
\left(
1+\sqrt{5}\rho+\frac{5\rho^2}{3}
\right)e^{-\sqrt{5}\rho}.
$$

For each family,

$$
2\pi\int_0^\infty \rho c(\rho)\,d\rho=2\pi.
$$

This convention compares shape at fixed point variance and fixed integral correlation area. It is not a claim that these are the only physically meaningful matching conditions.

## 4. Exact Gaussian attenuation

For

$$
c_G(r/\xi)
=
\exp\!\left(-\frac{r^2}{2\xi^2}\right),
$$

the radial integral gives

$$
\boxed{
V_G(s)
=
\frac{A}{1+2s^2/\xi^2}
}.
$$

Taking the reciprocal,

$$
\boxed{
\frac{1}{V_G(s)}
=
\frac{1}{A}
+
\frac{2}{A\xi^2}s^2
}.
$$

Thus $1/V_G$ is exactly affine in $s^2$.

## 5. Three-scale closure theorem

Let three distinct probe scales satisfy

$$
0\le s_1<s_2<s_3,
$$

and define

$$
x_i=s_i^2,
\qquad
y_i=\frac{1}{V(s_i)}.
$$

If the Gaussian covariance/Gaussian-probe model is exact, then the middle reciprocal variance must equal the affine interpolation of the endpoints:

$$
\boxed{
y_2
=
y_1
+
\frac{x_2-x_1}{x_3-x_1}
(y_3-y_1)
}.
$$

Define the signed closure residual

$$
R_{123}
=
y_2-y_1
-
\frac{x_2-x_1}{x_3-x_1}(y_3-y_1).
$$

Then

$$
R_{123}=0
$$

for every exact Gaussian-family triple.

A dimensionless form is

$$
\widehat R_{123}
=
\frac{R_{123}}
{\max(|y_1|,|y_2|,|y_3|)}.
$$

A nonzero $\widehat R_{123}$ falsifies the Gaussian family only under the declared assumptions of stationarity, isotropy, a Gaussian probe, and correctly known probe scales.

## 6. Why two scales cannot test family shape

A physically admissible two-scale pair gives two equations for the two Gaussian parameters. Writing

$$
\frac{1}{V(s)}=b+ms^2,
$$

the pair determines

$$
b=\frac{1}{A},
\qquad
m=\frac{2}{A\xi^2}.
$$

Consequently, two-scale recovery can be internally exact even when the true covariance is non-Gaussian. The first overdetermined family test requires a third scale.

With more than three scales, every scale pair produces an inferred $(A,\xi)$. Exact Gaussian data give identical pairwise parameters. Family misspecification produces scale-pair dependence.

## 7. Exact exponential benchmark

For the exponential covariance,

$$
c_E(r/\xi)=e^{-r/\xi},
$$

the radial integral is

$$
\frac{V_E(s)}{A}
=
\int_0^\infty
\frac{r}{2s^2}
\exp\!\left(
-\frac{r^2}{4s^2}-\frac{r}{\xi}
\right)dr.
$$

With $u=s/\xi$,

$$
\boxed{
\frac{V_E(s)}{A}
=
1-\sqrt{\pi}\,u\,e^{u^2}\operatorname{erfc}(u)
}.
$$

For large $u$, direct evaluation suffers cancellation. The implementation evaluates the positive asymptotic remainder,

$$
\frac{V_E}{A}
\sim
\frac{1}{2u^2}
-\frac{3}{4u^4}
+\frac{15}{8u^6}
-\cdots.
$$

This exact branch independently validates the numerical radial quadrature.

## 8. Numerical Matérn evaluation

For the Matérn families, the transformed integral

$$
\frac{V(s)}{A}
=
\int_0^\infty
2y e^{-y^2}
c(2uy)\,dy
$$

is evaluated on $y\in[0,10]$ with Gauss-Legendre quadrature.

The omitted Gaussian tail is bounded by

$$
\int_{10}^\infty 2y e^{-y^2}dy=e^{-100},
$$

before the additional covariance attenuation is applied.

Gauss-Legendre is used after the $r=2sy$ transformation because the integrand is smooth at $y=0$. Direct Gauss-Laguerre quadrature in $t=y^2$ leaves non-Gaussian terms proportional to $\sqrt t$, which converge substantially more slowly.

## 9. Best Gaussian surrogate

For $N\ge3$ synthetic observations $V_i$, the best Gaussian surrogate is defined by weighted log-variance least squares:

$$
\chi^2(\log A,\log\xi)
=
\sum_i w_i
\left[
\log A
-
\log\!\left(1+\frac{2s_i^2}{\xi^2}\right)
-
\log V_i
\right]^2,
$$

with

$$
w_i>0,
\qquad
\sum_iw_i=1.
$$

For fixed $\xi$, the optimal $\log A$ is analytical:

$$
\log A_*(\xi)
=
\sum_iw_i
\left[
\log V_i
+
\log\!\left(1+\frac{2s_i^2}{\xi^2}\right)
\right].
$$

This reduces the fit to one dimension. The implementation:

1. nondimensionalizes length by the geometric mean of positive probe scales;
2. centers the log variances to remove amplitude-scale dependence;
3. evaluates the analytical derivative of the profiled objective;
4. solves for the stationary point by bracketed bisection.

The fitted bias ratios are

$$
B_A=\frac{A_{\rm fit}}{A_{\rm true}},
\qquad
B_\xi=\frac{\xi_{\rm fit}}{\xi_{\rm true}}.
$$

## 10. Controlled results

Two designs are recorded:

- three-scale transition design: $s=(0.25,1,4)$ with $A=0.01$, $\xi=2$;
- five-scale broad design: $s=(0,0.5,2,8,20)$ with the same $A$ and $\xi$.

### Three-scale design

| True family | $|\widehat R|$ | $A_{\rm fit}/A$ | $\xi_{\rm fit}/\xi$ | maximum relative surrogate error |
|---|---:|---:|---:|---:|
| Gaussian | 0 | 1.0000 | 1.0000 | $<3\times10^{-13}$ |
| Exponential | 0.03904 | 0.7595 | 1.0401 | 0.1432 |
| Matérn $3/2$ | 0.01756 | 0.9241 | 0.9972 | 0.0682 |
| Matérn $5/2$ | 0.01107 | 0.9567 | 0.9954 | 0.0432 |

### Five-scale design

| True family | maximum $|\widehat R|$ | pairwise $\xi$ spread | $A_{\rm fit}/A$ | RMS log error |
|---|---:|---:|---:|---:|
| Gaussian | 0 | 1.000 | 1.0000 | $<3\times10^{-13}$ |
| Exponential | 0.07812 | 3.418 | 0.8351 | 0.1388 |
| Matérn $3/2$ | 0.02334 | 1.734 | 0.9441 | 0.0516 |
| Matérn $5/2$ | 0.01253 | 1.417 | 0.9678 | 0.0317 |

Under these declared designs, the roughest tested covariance produces the strongest Gaussian-family closure failure. Increasing Matérn smoothness reduces but does not eliminate the mismatch.

This ordering is a controlled result for the selected scales and equal-area convention, not a universal theorem over every design.

## 11. Measurement-design consequence

A two-scale experiment can recover Gaussian parameters but cannot validate Gaussian covariance shape.

A defensible covariance-family test requires:

1. at least three independently characterized probe scales;
2. scales spanning the attenuation transition rather than one asymptotic regime;
3. uncertainty propagation for variance and probe-scale calibration;
4. examination of reciprocal-affinity residuals and pairwise parameter drift;
5. comparison against multiple covariance families or a nonparametric alternative.

The third scale is therefore not merely redundant precision. It changes the logical status of the experiment from parameter recovery to model testing.

## 12. Claim restrictions

This result does not establish:

- that HgCdTe composition disorder follows a Gaussian, exponential, or Matérn covariance;
- a specimen-specific $A$ or $\xi$;
- that equal integral area is the unique comparison convention;
- that a nonzero closure residual must arise from covariance shape rather than probe, calibration, depth, or nonstationarity errors;
- that two-scale agreement validates a covariance family;
- manuscript readiness or novelty relative to established spatial-statistics literature.

The next steps remain full-text prior-art review, kernel-shape uncertainty, nonlinear posterior recovery, and one public-data or experimentally specified validation path.

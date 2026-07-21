# Derivation 012: a three-scale covariance-family test

## 1. Scope

This derivation belongs to the measurement-kernel-aware spatial-disorder program, contribution R04.

The existing exact inverse assumes an isotropic two-dimensional Gaussian material covariance and a Gaussian lateral measurement kernel. Two scales determine the two Gaussian parameters, but parameter recovery does not test whether the Gaussian covariance family is correct.

The present result separates:

1. **parameter identifiability within the Gaussian family**;
2. **family falsification using a third scale**;
3. **practical detectability under measurement uncertainty**;
4. **bias when a non-Gaussian family is forced into the Gaussian inverse**.

No specimen covariance family is selected here.

## 2. Exact Gaussian reciprocal-linearity theorem

For point variance `A`, Gaussian correlation length `xi`, and Gaussian probe standard deviation `s`,

$$
V_G(s)=\frac{A}{1+2s^2/\xi^2}.
$$

Taking the reciprocal gives

$$
\boxed{
\frac{1}{V_G(s)}
=\frac{1}{A}+\frac{2}{A\xi^2}s^2.
}
$$

Define

$$
x=s^2,
\qquad
y=\frac{1}{V}.
$$

Every exact Gaussian dataset lies on the affine line

$$
y=\alpha+\beta x,
$$

with

$$
A=\frac{1}{\alpha},
\qquad
\xi=\sqrt{\frac{2\alpha}{\beta}}.
$$

### 2.1 Why two scales cannot test the family

Any two distinct points define one line. If the resulting intercept and slope are positive, the pair defines an admissible Gaussian `A` and `xi` and is reproduced exactly.

Thus two noiseless scales can estimate Gaussian parameters but cannot test Gaussian covariance.

### 2.2 Three-scale invariant

For ordered scales

$$
s_1<s_2<s_3,
$$

define

$$
y_i=\frac{1}{V_i},
\qquad
x_i=s_i^2.
$$

The Gaussian family requires

$$
\boxed{
\mathcal K_{123}
=
\frac{y_3-y_2}{x_3-x_2}
-
\frac{y_2-y_1}{x_2-x_1}
=0.
}
$$

Equivalently, the endpoint scales predict the middle reciprocal variance:

$$
\widehat y_2
=
(1-t)y_1+ty_3,
\qquad
 t=\frac{x_2-x_1}{x_3-x_1},
$$

and therefore

$$
\boxed{
\widehat V_2
=
\left[(1-t)V_1^{-1}+tV_3^{-1}\right]^{-1}.
}
$$

A nonzero middle residual is an exact lack-of-fit result for the declared Gaussian covariance/probe family.

## 3. Uncertainty of the three-scale residual

Let the three measured variances be independent with standard deviations `sigma_i`. To first order,

$$
\sigma_{y_i}=\frac{\sigma_i}{V_i^2}.
$$

For

$$
r_2=y_2-[(1-t)y_1+ty_3],
$$

the residual variance is

$$
\boxed{
\sigma_{r_2}^2
=
\sigma_{y_2}^2
+(1-t)^2\sigma_{y_1}^2
+t^2\sigma_{y_3}^2.
}
$$

The local standardized lack of fit is

$$
z_{123}=\frac{r_2}{\sigma_{r_2}}.
$$

This is a design statistic under the declared independent Gaussian uncertainty. It is not a global posterior probability or a universal significance threshold.

## 4. More than three scales

For `N >= 3`, fit

$$
y_i=\alpha+\beta s_i^2+\epsilon_i.
$$

If variance standard deviations are known, use

$$
\sigma_{y_i}\simeq\frac{\sigma_{V_i}}{V_i^2}
$$

and weighted least squares. The lack-of-fit statistic is

$$
\chi^2
=
\sum_i
\frac{(y_i-\widehat y_i)^2}{\sigma_{y_i}^2},
$$

with

$$
\nu_{\rm dof}=N-2.
$$

The fitted Gaussian parameters are valid only when

$$
\alpha>0,
\qquad
\beta>0.
$$

A low residual does not prove Gaussian covariance; it only shows that the available scales and uncertainties do not resolve a departure from reciprocal linearity.

## 5. Half-integer Matern alternatives

Use the standard isotropic Matern correlation

$$
\rho_\nu(r)
=
\frac{2^{1-\nu}}{\Gamma(\nu)}
 z^\nu K_\nu(z),
\qquad
z=\frac{\sqrt{2\nu}r}{\ell}.
$$

The supported half-integer cases are

$$
\rho_{1/2}(r)=e^{-z},
$$

$$
\rho_{3/2}(r)=(1+z)e^{-z},
$$

and

$$
\rho_{5/2}(r)=\left(1+z+\frac{z^2}{3}\right)e^{-z}.
$$

Let the normalized two-dimensional Gaussian probe have coordinate standard deviation `s`. The separation `R` between two independently sampled probe coordinates has density

$$
p_R(r)
=
\frac{r}{2s^2}
\exp\left(-\frac{r^2}{4s^2}\right).
$$

Therefore the apparent variance is

$$
\boxed{
V_\nu(s)
=A\int_0^\infty
\rho_\nu(r)
\frac{r}{2s^2}
\exp\left(-\frac{r^2}{4s^2}\right)dr.
}
$$

Define

$$
\varrho=\frac{\sqrt{2\nu}s}{\ell},
\qquad
H(\varrho)=\sqrt\pi e^{\varrho^2}\operatorname{erfc}(\varrho).
$$

Direct integration gives the exact attenuation factors

$$
\boxed{
F_{1/2}
=1-\varrho H(\varrho),
}
$$

$$
\boxed{
F_{3/2}
=1-2\varrho^2+2\varrho^3H(\varrho),
}
$$

and

$$
\boxed{
F_{5/2}
=1-\frac{2}{3}\varrho^2
+\frac{4}{3}\varrho^4
-\frac{4}{3}\varrho^5H(\varrho).
}
$$

The implementation uses these forms before cancellation becomes important and switches to the equivalent Gauss--Laguerre representation

$$
F_\nu
=
\frac{1}{2\varrho^2}
\int_0^\infty
zP_\nu(z)e^{-z}
\exp\left(-\frac{z^2}{4\varrho^2}\right)dz
$$

at larger `varrho`.

## 6. Limiting behavior

### 6.1 Point-probe limit

For every supported family,

$$
\lim_{s/\ell\to0}F_\nu=1.
$$

The finite probe approaches the microscopic point variance.

### 6.2 Large-probe limit

For the standard `sqrt(2 nu)/ell` parameterization,

$$
\boxed{
F_\nu(s/\ell)
\sim
\frac{1}{2(s/\ell)^2}
\qquad
s/\ell\to\infty
}
$$

for all three supported smoothness values.

Thus very large probes share the same leading inverse-area law and carry little covariance-family information. Family discrimination requires scales in or below the transition around `s/ell = O(1)`.

## 7. Three-scale reference design

Declare

$$
\frac{s}{\ell}=(0.1,1,2)
$$

and use the first and third scales to fit the Gaussian endpoint model. The middle-scale result is then a pure family check.

| True covariance | True middle attenuation | Gaussian endpoint prediction | Relative prediction error | Standardized residual at 3% independent relative uncertainty |
|---|---:|---:|---:|---:|
| Matern `nu=1/2` | 0.242128 | 0.284456 | 17.482% | 4.120 |
| Matern `nu=3/2` | 0.292792 | 0.316468 | 8.086% | 2.012 |
| Matern `nu=5/2` | 0.307162 | 0.323154 | 5.207% | 1.319 |

Consequences:

1. the rough exponential family is distinguishable at this uncertainty level;
2. `nu=3/2` is marginally distinguishable;
3. `nu=5/2` is unresolved by this three-scale design at 3% uncertainty;
4. failure to reject Gaussian covariance does not establish Gaussian covariance.

The endpoint-fitted Gaussian parameters are biased even though both endpoint measurements are reproduced exactly:

| True covariance | Fitted `A/A_true` | Fitted `xi/ell` |
|---|---:|---:|
| Matern `nu=1/2` | 0.85807 | 0.99589 |
| Matern `nu=3/2` | 0.97519 | 0.98023 |
| Matern `nu=5/2` | 0.98892 | 0.98528 |

## 8. Six-scale reference

For

$$
s/\ell=(0.05,0.1,0.3,1,2,5)
$$

with 3% independent relative uncertainty, the best weighted Gaussian reciprocal line gives:

| True covariance | Reduced chi-square | Maximum absolute variance residual |
|---|---:|---:|
| Matern `nu=1/2` | 18.795 | 18.089% |
| Matern `nu=3/2` | 3.519 | 7.526% |
| Matern `nu=5/2` | 1.363 | 4.752% |

The smoother alternative remains difficult to separate without lower noise or a more informative scale design.

## 9. Experimental consequence

A multiscale experiment should not proceed directly from two-scale inversion to a reported HgCdTe correlation length. The minimum sequence is:

1. measure at least three distinct effective probe scales;
2. test reciprocal linearity before accepting the Gaussian covariance family;
3. include scales near and below the expected correlation length;
4. propagate probe-scale calibration uncertainty;
5. report family-conditioned parameters and lack of fit separately.

The test operates on apparent variance. Connecting it to spectra, PL linewidth, or cutoff distributions still requires the corresponding observation operator.

## 10. Claim boundary

The affine reciprocal identity is elementary algebra for the declared Gaussian benchmark. Matern covariance, Gaussian convolution, and weighted linear regression are established mathematics.

The candidate R04 contribution is the combined HgCdTe measurement consequence:

- two scales estimate but cannot test the Gaussian family;
- three scales provide an exact family invariant;
- family misspecification can bias recovered point variance and correlation length while fitting two scales perfectly;
- practical family resolution depends strongly on probe placement and uncertainty.

This result does not establish a covariance family for any specimen and does not authorize manuscript writing.

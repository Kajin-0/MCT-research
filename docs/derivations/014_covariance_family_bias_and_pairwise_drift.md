# Derivation 014: covariance-family bias and pairwise parameter drift

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issues:** #196, #218, #224  
**Status:** controlled synthetic extension of the three-scale family test

## 1. Scope

Derivation 012 established the reciprocal-linearity theorem for the two-dimensional Gaussian covariance/Gaussian-probe model:

$$
V_G(s)=\frac{A}{1+2s^2/\xi^2},
$$

$$
\frac{1}{V_G(s)}=\frac{1}{A}+\frac{2}{A\xi^2}s^2.
$$

It also established that:

1. two admissible scales can determine two Gaussian parameters but cannot test the family;
2. a third scale supplies the first exact lack-of-fit test;
3. uncertainty-aware reciprocal residuals determine whether the departure is practically resolvable.

The present extension asks a different question:

> When the true covariance is non-Gaussian but a Gaussian inverse is nevertheless reported, how strongly do the inferred parameters depend on the selected probe scales and fitting convention?

No covariance family is selected for HgCdTe, and no specimen parameter is inferred.

## 2. Pairwise Gaussian recovery

Let measured or synthetic filtered variances be

$$
V_i=V(s_i),
$$

at distinct scales $s_i$.

For each pair $(i,j)$, force the Gaussian model through the two values. In two dimensions,

$$
R_{ij}=\frac{V_i}{V_j}.
$$

The Gaussian correlation length inferred from that pair is

$$
\boxed{
\xi_{ij}^2
=
2\frac{s_j^2-R_{ij}s_i^2}{R_{ij}-1}
}
$$

when the pair implies positive Gaussian parameters. The inferred point variance is

$$
\boxed{
A_{ij}
=
V_i\left(1+\frac{2s_i^2}{\xi_{ij}^2}\right).
}
$$

For exact Gaussian-family data,

$$
A_{ij}=A,
\qquad
\xi_{ij}=\xi
$$

for every pair.

Under covariance-family misspecification, each pair can still be reproduced exactly, but the inferred parameters generally drift with scale selection.

Define the pairwise spread ratios

$$
S_A
=
\frac{\max_{i<j}A_{ij}}{\min_{i<j}A_{ij}},
$$

$$
S_\xi
=
\frac{\max_{i<j}\xi_{ij}}{\min_{i<j}\xi_{ij}}.
$$

Exact Gaussian data satisfy

$$
S_A=S_\xi=1.
$$

Values above unity measure scale-pair dependence of the reported Gaussian parameters. They are diagnostics of family-conditioned instability, not statistical confidence intervals.

## 3. Best global Gaussian surrogate

A multi-scale dataset may still be summarized by one Gaussian surrogate even after reciprocal linearity fails. The fitted values then depend on the declared loss function.

This extension uses weighted log-variance loss:

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

For fixed $\xi$, the optimal amplitude is analytical:

$$
\boxed{
\log A_*(\xi)
=
\sum_iw_i
\left[
\log V_i
+
\log\!\left(1+\frac{2s_i^2}{\xi^2}\right)
\right].
}
$$

The fit therefore reduces to one dimension.

To preserve unit invariance, define a reference length from the geometric mean of positive probe scales,

$$
s_{\rm ref}
=
\exp\left[
\frac{1}{N_+}
\sum_{s_i>0}\log s_i
\right],
$$

and optimize the dimensionless variable

$$
r=\log(\xi/s_{\rm ref}).
$$

The implementation also centers the observed log variances before evaluating the profile. Consequently:

- multiplying every $V_i$ by a constant changes only fitted $A$;
- multiplying every $s_i$ and the true correlation length by one length-unit factor changes only fitted $\xi$ by that factor;
- the bias ratios and residual diagnostics are invariant.

## 4. Reported bias quantities

For controlled synthetic truth with point variance $A_{\rm true}$ and correlation parameter $\xi_{\rm true}$, define

$$
B_A
=
\frac{A_{\rm fit}}{A_{\rm true}},
$$

$$
B_\xi
=
\frac{\xi_{\rm fit}}{\xi_{\rm true}}.
$$

The global surrogate also reports

$$
\epsilon_{\log}
=
\left[
\sum_iw_i
\left(\log V_{G,i}^{\rm fit}-\log V_i\right)^2
\right]^{1/2},
$$

and

$$
\epsilon_{\max}
=
\max_i
\left|
\frac{V_{G,i}^{\rm fit}}{V_i}-1
\right|.
$$

These quantities answer different questions from the uncertainty-aware chi-square in Derivation 012:

- reciprocal chi-square asks whether Gaussian covariance can be rejected under declared measurement uncertainty;
- $S_A$ and $S_\xi$ measure dependence on selected scale pairs;
- $B_A$ and $B_\xi$ measure bias of one declared global surrogate;
- $\epsilon_{\log}$ and $\epsilon_{\max}$ measure deterministic approximation error.

## 5. Controlled covariance families

The extension reuses the family definitions and filtering implementation established in `spatial_disorder_covariance_families.py`:

- Matérn $\nu=1/2$ (exponential);
- Matérn $\nu=3/2$;
- Matérn $\nu=5/2$.

Under the standard parameterization

$$
z=\sqrt{2\nu}\,r/\ell,
$$

all three supported families share the same point value and the same leading large-probe inverse-area coefficient. The comparison therefore isolates covariance shape over the transition region rather than trivial point-amplitude or integral-area differences.

## 6. Three-scale transition design

Use

$$
A=0.01,
\qquad
\ell=2,
\qquad
s=(0.25,1,4).
$$

The equal-weight log-variance Gaussian surrogates give:

| True family | $S_A$ | $S_\xi$ | $B_A$ | $B_\xi$ | $\epsilon_{\max}$ |
|---|---:|---:|---:|---:|---:|
| Gaussian | 1.000 | 1.000 | 1.0000 | 1.0000 | $<3\times10^{-13}$ |
| Matérn $1/2$ | 1.398 | 1.603 | 0.7595 | 1.0401 | 0.1432 |
| Matérn $3/2$ | 1.186 | 1.272 | 0.9241 | 0.9972 | 0.0682 |
| Matérn $5/2$ | 1.116 | 1.171 | 0.9567 | 0.9954 | 0.0432 |

Even with only three scales, the rough exponential truth permits materially different Gaussian parameter reports depending on which pair or fitting convention is used.

## 7. Five-scale broad design

Use

$$
A=0.01,
\qquad
\ell=2,
\qquad
s=(0,0.5,2,8,20).
$$

The broad scale range gives:

| True family | $S_A$ | $S_\xi$ | $B_A$ | $B_\xi$ | RMS log error |
|---|---:|---:|---:|---:|---:|
| Gaussian | 1.000 | 1.000 | 1.0000 | 1.0000 | $<3\times10^{-13}$ |
| Matérn $1/2$ | 2.820 | 3.418 | 0.8351 | 1.0406 | 0.1388 |
| Matérn $3/2$ | 1.630 | 1.734 | 0.9441 | 1.0084 | 0.0516 |
| Matérn $5/2$ | 1.381 | 1.417 | 0.9678 | 1.0035 | 0.0317 |

For the exponential truth, the reported Gaussian correlation length varies by a factor of approximately $3.42$ across scale pairs, while the equal-weight global surrogate underestimates point variance by approximately $16.5\%$.

For these declared designs, increasing Matérn smoothness reduces pairwise drift and global surrogate error. This ordering is design-conditioned, not a universal theorem over all probe layouts.

## 8. Dependence on fitting convention

A global surrogate is not unique until the loss and weights are declared. Increasing the weight of the point-probe datum drives the fitted point variance toward the microscopic value and changes the fitted correlation length.

Therefore a reported Gaussian $(A,\xi)$ from non-Gaussian data is not only covariance-family-conditioned; it is also fitting-convention-conditioned.

A defensible report should state:

1. probe scales and their calibration;
2. covariance family;
3. fitting domain, such as variance, reciprocal variance, or log variance;
4. uncertainty model and weights;
5. family lack-of-fit statistic;
6. pairwise parameter drift or another sensitivity measure.

## 9. Experimental consequence

The minimum logical sequence for a multiscale experiment is now:

1. use at least three independently characterized scales;
2. test reciprocal linearity before accepting Gaussian covariance;
3. quantify detectability under measurement and scale uncertainty;
4. inspect pairwise parameter drift;
5. compare global surrogate results across justified fitting conventions;
6. report family-conditioned parameters only after these checks.

A single two-scale estimate or one unqualified global fit can conceal substantial scale-selection bias.

## 10. Claim restrictions

This extension does not establish:

- that HgCdTe follows any tested covariance family;
- a specimen-specific point variance or correlation length;
- that log-variance loss is uniquely correct;
- that pairwise spread is a confidence interval;
- that a low pairwise spread proves Gaussian covariance;
- that covariance-family error is the only source of scale dependence;
- manuscript readiness or novelty relative to established spatial-statistics literature.

The remaining R04 gates are representative instrument kernels, combined calibration/family/operator uncertainty, full-text prior-art review, and one public-data or experimentally specified validation path.

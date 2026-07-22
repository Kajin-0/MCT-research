# Derivation 018: correlated map sampling and effective degrees of freedom

## 1. Measurement centers are not independent realizations

Let the local composition fluctuation be a stationary zero-mean Gaussian field

\[
\delta x(\mathbf r)
\]

with covariance

\[
C_x(\mathbf h)
=
A\exp\left(-\frac12\mathbf h^T\Lambda^{-1}\mathbf h\right).
\]

Measurement \(i\), centered at \(\mathbf r_i\), uses a normalized Gaussian kernel
with covariance \(\Sigma_i\):

\[
X_i
=
\int w_i(\mathbf u)\,
\delta x(\mathbf r_i+\mathbf u)\,d\mathbf u.
\]

Two nearby map pixels generally sample overlapping material correlation volumes.
The nominal pixel count is therefore not the number of independent observations.

## 2. Exact cross-covariance theorem

Let

\[
\mathbf U_i\sim\mathcal N(0,\Sigma_i),
\qquad
\mathbf U_j\sim\mathcal N(0,\Sigma_j)
\]

be independent coordinates drawn from the two kernels. Then

\[
\operatorname{Cov}(X_i,X_j)
=
\mathbb E\left[
C_x(\mathbf r_i-\mathbf r_j+\mathbf U_i-\mathbf U_j)
\right].
\]

Define

\[
\Delta\mathbf r=\mathbf r_i-\mathbf r_j,
\qquad
\mathbf Z=\mathbf U_i-\mathbf U_j.
\]

Because the kernels are Gaussian,

\[
\mathbf Z\sim
\mathcal N(0,\Sigma_i+\Sigma_j).
\]

The Gaussian quadratic expectation

\[
\mathbb E\left[
\exp\left(-\frac12(\Delta\mathbf r+\mathbf Z)^T
\Lambda^{-1}(\Delta\mathbf r+\mathbf Z)\right)
\right]
\]

can be completed analytically. The result is

\[
\boxed{
\operatorname{Cov}(X_i,X_j)
=
A
\sqrt{
\frac{\det\Lambda}
{\det(\Lambda+\Sigma_i+\Sigma_j)}
}
\exp\left[
-\frac12\Delta\mathbf r^T
(\Lambda+\Sigma_i+\Sigma_j)^{-1}
\Delta\mathbf r
\right].
}
\]

This formula applies to anisotropic material covariance, anisotropic Gaussian
kernels, unequal kernels, and arbitrary sample-center displacement.

### Equal-kernel zero-lag limit

When

\[
\Sigma_i=\Sigma_j=\Sigma_w,
\qquad
\Delta\mathbf r=0,
\]

then

\[
\boxed{
\operatorname{Var}(X_i)
=
A\sqrt{
\frac{\det\Lambda}{\det(\Lambda+2\Sigma_w)}
},
}
\]

which is the existing Gaussian filtering theorem.

### Isotropic equal-kernel map

For

\[
\Lambda=\ell^2I,
\qquad
\Sigma_w=s^2I,
\]

in \(D\) dimensions,

\[
\operatorname{Cov}(X_i,X_j)
=
A\left(1+\frac{2s^2}{\ell^2}\right)^{-D/2}
\exp\left[
-\frac{|\Delta\mathbf r|^2}{2(\ell^2+2s^2)}
\right].
\]

The finite probe lowers the marginal variance but increases the correlation scale
of the measured map from \(\ell\) to

\[
\sqrt{\ell^2+2s^2}.
\]

A smoother-looking map can therefore contain fewer independent spatial samples
than the pixel count suggests.

## 3. Exact map-mean uncertainty

Collect \(n\) map values into

\[
\mathbf y\sim\mathcal N(0,C),
\]

where \(C\) is built from the cross-covariance theorem. The map mean is

\[
\bar y=\frac1n\mathbf 1^T\mathbf y.
\]

Therefore

\[
\boxed{
\operatorname{Var}(\bar y)
=
\frac{\mathbf 1^TC\mathbf 1}{n^2}.
}
\]

For a homogeneous map with common marginal variance \(V_w\), define

\[
\boxed{
n_{\rm eff,mean}
=
\frac{V_w}{\operatorname{Var}(\bar y)}.
}
\]

Independent samples give \(n_{\rm eff,mean}=n\). Positively correlated raster
samples give a smaller value, approaching one when the entire map spans much less
than one measured correlation area.

## 4. Exact moments of the usual sample variance

The estimator normally called the unbiased sample variance is

\[
s^2_{\rm naive}
=
\frac1{n-1}
\sum_{i=1}^n(y_i-\bar y)^2.
\]

Define the centering projector

\[
P=I-\frac1n\mathbf 1\mathbf 1^T.
\]

Then

\[
s^2_{\rm naive}
=
\frac{\mathbf y^TP\mathbf y}{n-1}.
\]

For a zero-mean Gaussian vector and symmetric quadratic form \(B\),

\[
\mathbb E[\mathbf y^TB\mathbf y]=\operatorname{tr}(BC),
\]

and

\[
\operatorname{Var}(\mathbf y^TB\mathbf y)
=2\operatorname{tr}[(BC)^2].
\]

Using \(B=P/(n-1)\),

\[
\boxed{
\mathbb E[s^2_{\rm naive}]
=
\frac{\operatorname{tr}(PC)}{n-1},
}
\]

and

\[
\boxed{
\operatorname{Var}(s^2_{\rm naive})
=
\frac{2\operatorname{tr}[(PC)^2]}{(n-1)^2}.
}
\]

The estimator is unbiased only under the independence structure for which it was
derived.

### Bias written through the map-mean effective count

For equal marginal variance \(V_w\),

\[
\operatorname{tr}(PC)
=
nV_w-\frac1n\mathbf 1^TC\mathbf 1
=
nV_w-n\operatorname{Var}(\bar y).
\]

Thus

\[
\boxed{
\frac{\mathbb E[s^2_{\rm naive}]}{V_w}
=
\frac{n}{n-1}
\left(1-\frac1{n_{\rm eff,mean}}\right).
}
\]

A low effective count causes the ordinary map variance to underestimate the
marginal filtered variance, even with perfect instrumentation and no fitting
error.

## 5. Moment-matched variance-estimator degrees of freedom

A correlated Gaussian quadratic form is generally a weighted sum of independent
\(\chi_1^2\) variables, not one exact scaled chi-square variable. A useful
moment-matched degree of freedom is

\[
\boxed{
\nu_{\rm eff,var}
=
\frac{[\operatorname{tr}(PC)]^2}
{\operatorname{tr}[(PC)^2]}.
}
\]

It satisfies

\[
\frac{\sqrt{\operatorname{Var}(s^2_{\rm naive})}}
{\mathbb E[s^2_{\rm naive}]}
=
\sqrt{\frac2{\nu_{\rm eff,var}}}.
\]

For independent samples, \(\nu_{\rm eff,var}=n-1\). For correlated maps it can be
orders of magnitude smaller.

This is a moment-equivalent summary, not an exact distributional identity unless
the relevant projected covariance eigenvalues are equal.

## 6. Controlled 10 by 10 raster

Declare

\[
A=(0.005)^2,
\qquad
\ell=2\ \mu\mathrm m,
\qquad
s=1\ \mu\mathrm m,
\]

and a \(10\times10\) raster. The filtered marginal variance is

\[
V_w
=A\frac{\ell^2}{\ell^2+2s^2}
=1.66667\times10^{-5}.
\]

Exact finite-map results are:

| Pixel spacing | Nominal pixels | \(n_{\rm eff,mean}\) | \(E[s^2_{\rm naive}]/V_w\) | \(\nu_{\rm eff,var}\) |
|---:|---:|---:|---:|---:|
| 0.25 µm | 100 | 1.1760 | 0.1512 | 2.3729 |
| 0.5 µm | 100 | 1.7377 | 0.4288 | 3.4783 |
| 1 µm | 100 | 4.0701 | 0.7619 | 7.7019 |
| 2 µm | 100 | 12.8720 | 0.9316 | 24.2730 |
| 4 µm | 100 | 45.5178 | 0.9879 | 78.6247 |
| 8 µm | 100 | 98.2843 | 0.99982 | 98.9919 |

At 0.5 µm spacing, one hundred pixels provide only approximately 1.74 independent
samples for the map mean. The ordinary sample variance averages only 42.9% of the
marginal filtered variance and has approximately 3.48 moment-equivalent degrees of
freedom.

At 8 µm spacing the same pixel count is nearly independent under the declared
model.

## 7. Fixed-field-of-view oversampling theorem consequence

Compare approximately the same field of view:

```text
10 by 10 pixels at 0.5 um spacing
20 by 20 pixels at 0.25 um spacing
```

The nominal count increases from 100 to 400, but

```text
n_eff,mean: 1.73771 -> 1.74276
```

an increase of only 0.29%. The expected naive-variance ratio changes from

```text
0.42882 -> 0.42727.
```

Finer sampling resolves the same correlated realization more densely; it does not
create new material realizations.

## 8. Connection to multiscale allocation

The repeat counts in the optimal-allocation theorem are counts of independent
realizations, or observations treated with their full covariance. A raster with
\(n\) pixels must not enter the allocation model as \(n\) independent repeats.

Acceptable routes are:

1. use independent maps or sufficiently separated sampling regions;
2. use the full map covariance in the likelihood or Fisher calculation;
3. use effective-count diagnostics only as declared summaries, not as substitutes
   for the full covariance when precision matters.

Increasing raster density at fixed field of view does not overcome the common
absolute probe-scale calibration floor and does not guarantee increased
covariance-family discrimination.

## 9. Claim boundary

Established mathematics used here includes Gaussian convolution, Gaussian-process
covariance propagation, and moments of Gaussian quadratic forms.

The R04 contribution is the explicit finite-resolution HgCdTe map consequence and
its integration with the multiscale inference, calibration, covariance-family, and
allocation hierarchy.

The controlled calculations do not identify a specimen correlation length,
prescribe a universal scan pitch, or authorize a manuscript.

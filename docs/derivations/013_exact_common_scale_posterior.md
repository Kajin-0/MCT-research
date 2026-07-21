# Derivation 013: exact nonlinear posterior under common probe-scale calibration

## 1. Scope

This derivation belongs to the measurement-kernel-aware spatial-disorder program, contribution R04.

The local calibration result previously used Fisher information. The present result asks whether the common absolute probe-scale uncertainty floor survives the full nonlinear likelihood.

For the isotropic two-dimensional Gaussian covariance/Gaussian probe benchmark,

$$
V_i(A,\xi,\delta)
=
\frac{A}{1+2(s_i e^\delta)^2/\xi^2},
$$

where

- $A>0$ is point variance;
- $\xi>0$ is absolute correlation length;
- $s_i$ is the nominal probe standard deviation;
- $\delta$ is a common multiplicative calibration error in log scale.

No specimen inference or covariance-family validation is attempted.

## 2. Exact reparameterization

Define

$$
u=\log A,
\qquad
v=\log\xi,
\qquad
\lambda=v-\delta.
$$

Then

$$
\frac{s_i e^\delta}{\xi}
=s_i e^{-\lambda},
$$

and therefore

$$
V_i
=
\frac{e^u}{1+2s_i^2e^{-2\lambda}}.
$$

Any observation likelihood whose scale dependence enters only through $s_i e^\delta/\xi$ has the form

$$
p(y\mid u,v,\delta)
=
L(y\mid u,v-\delta)
=
L(y\mid u,\lambda).
$$

The transformation $(u,v,\delta)\mapsto(u,\lambda,\delta)$ has unit Jacobian because $v=\lambda+\delta$.

## 3. Exact posterior factorization theorem

Assume:

1. the calibration prior $p_\delta(\delta)$ is independent of $(u,v)$;
2. the prior on $v$ is translation invariant over the posterior support, or its finite support is sufficiently broad that boundary effects are negligible;
3. the prior on $u$ is independent of $\delta$;
4. the likelihood depends on scale only through $v-\delta$.

Then

$$
p(u,\lambda,\delta\mid y)
\propto
L(y\mid u,\lambda)
p_u(u)p_v(\lambda+\delta)p_\delta(\delta).
$$

With translation-invariant $p_v$,

$$
p_v(\lambda+\delta)=\text{constant},
$$

so normalization gives

$$
\boxed{
p(u,\lambda,\delta\mid y)
=
p(u,\lambda\mid y)p_\delta(\delta).
}
$$

Thus the relative correlation-length coordinate inferred from the data is statistically independent of the absolute-scale calibration coordinate.

## 4. Exact convolution and cumulant addition

Because

$$
v=\lambda+\delta
$$

with independent posterior variables $\lambda$ and $\delta$, the absolute log-correlation posterior is the convolution

$$
\boxed{
p_v(v)
=
\int p_\lambda(v-\delta)p_\delta(\delta)\,d\delta.
}
$$

The cumulant-generating function is additive:

$$
K_v(t)
=
\log\mathbb E[e^{tv}]
=
K_\lambda(t)+K_\delta(t).
$$

Therefore, for every existing cumulant,

$$
\boxed{
\kappa_n(v)
=
\kappa_n(\lambda)+\kappa_n(\delta).
}
$$

The first four consequences are

$$
\mathbb E[v]
=
\mathbb E[\lambda]+\mathbb E[\delta],
$$

$$
\boxed{
\operatorname{Var}(v)
=
\operatorname{Var}(\lambda)+\operatorname{Var}(\delta),
}
$$

$$
\mu_3(v)
=
\mu_3(\lambda)+\mu_3(\delta),
$$

and

$$
\kappa_4(v)
=
\kappa_4(\lambda)+\kappa_4(\delta).
$$

No Gaussian approximation is required.

Since $u$ is independent of $\delta$ conditional on the factorized posterior,

$$
\boxed{
\operatorname{Cov}(u,v)
=
\operatorname{Cov}(u,\lambda).
}
$$

Consequently, the exact covariance increment is

$$
\boxed{
\operatorname{Cov}(u,v)
-
\operatorname{Cov}(u,\lambda)
=
\begin{pmatrix}
0&0\\
0&\operatorname{Var}(\delta)
\end{pmatrix}.
}
$$

The local Fisher identity is therefore the second-cumulant projection of a stronger global result.

## 5. Deterministic posterior calculation

The implementation evaluates a normalized posterior mass on uniform grids in

$$
(u,\lambda).
$$

Two likelihoods are supported:

1. Gaussian errors in variance;
2. Gaussian errors in log variance.

For the log-Gaussian case,

$$
\log y_i
\sim
N(\log V_i,\sigma_{\log,i}^2).
$$

The grid posterior is normalized by a log-sum-exp calculation. A separate discrete calibration distribution is convolved with the $\lambda$ marginal. The first four cumulants and the full two-parameter covariance are calculated directly from normalized probability mass.

An independent direct calculation uses a three-dimensional grid in

$$
(u,v,\delta)
$$

with a finite uniform prior on $v$. This path verifies factorization when the $v$ bounds are broad and exposes its failure when posterior mass reaches those bounds.

## 6. Synthetic reference design

Declare

$$
A=0.03,
\qquad
\xi=1.4,
$$

and

$$
s=(0.2,0.7,2.0,6.0).
$$

The exact apparent variances are

$$
V=
(0.0288235294,
0.0200000000,
0.00590361446,
0.000795024337).
$$

Use exact synthetic observations under a log-Gaussian likelihood.

## 7. Fisher comparison

The relative Frobenius error between the nonlinear posterior covariance and the local Fisher covariance is

| Relative observation uncertainty | Covariance error |
|---:|---:|
| 1% | $1.9846\times10^{-5}$ |
| 5% | $4.9537\times10^{-4}$ |
| 15% | $4.3978\times10^{-3}$ |
| 30% | $1.6642\times10^{-2}$ |

The error increases with uncertainty, as expected, but remains only 1.66% at 30% for this design and likelihood. Therefore the local Fisher result is unusually robust here. This is not guaranteed for other likelihoods, scale layouts, priors, or observation operators.

## 8. Exact calibration-floor references

At 15% relative observation uncertainty, the relative-scale posterior covariance is

$$
C_{u\lambda}
=
\begin{pmatrix}
0.0173321179 & -0.0109384855\\
-0.0109384855 & 0.0101750396
\end{pmatrix}.
$$

### 8.1 Two-percent common log-scale calibration

The discretized calibration variance is

$$
\operatorname{Var}(\delta)
=0.0003999986503.
$$

The absolute posterior covariance is

$$
C_{uv}
=
\begin{pmatrix}
0.0173321179 & -0.0109384855\\
-0.0109384855 & 0.0105750383
\end{pmatrix}.
$$

The variance-addition residual is

$$
1.73\times10^{-17}.
$$

### 8.2 Ten-percent common log-scale calibration

The discretized calibration variance is

$$
0.00999988429,
$$

and

$$
C_{uv}
=
\begin{pmatrix}
0.0173321179 & -0.0109384855\\
-0.0109384855 & 0.0201749239
\end{pmatrix}.
$$

The variance-addition residual is

$$
3.82\times10^{-17}.
$$

The amplitude variance and amplitude--length covariance remain unchanged in both cases.

## 9. Non-Gaussian calibration prior

An asymmetric discrete calibration prior was used to test higher cumulants. Its properties are

$$
\mathbb E[\delta]=-0.0192891,
$$

$$
\operatorname{Var}(\delta)=0.00847723,
$$

$$
\kappa_3(\delta)=-1.36398\times10^{-4},
$$

and

$$
\kappa_4(\delta)=-1.64248\times10^{-5}.
$$

After convolution, all four cumulant-addition identities close at numerical precision. The variance residual is

$$
3.47\times10^{-17}.
$$

Thus the exact theorem is not restricted to Gaussian calibration priors.

## 10. Bounded-prior failure

A finite prior on absolute $v$ introduces the factor

$$
p_v(\lambda+\delta),
$$

which couples $\lambda$ and $\delta$. The factorization becomes

$$
p(u,\lambda,\delta\mid y)
\propto
p(u,\lambda\mid y)p_\delta(\delta)p_v(\lambda+\delta),
$$

and is no longer separable.

### 10.1 Broad support

For the broad reference grid:

```text
absolute-v boundary mass              4.59e-134
calibration posterior total variation 4.41e-16
Cov(lambda,delta)                      4.02e-20
variance-addition residual            -1.73e-18
```

The direct three-dimensional integration and convolution theorem agree.

### 10.2 Narrow support

For a narrow grid with 14.08% posterior boundary mass:

```text
calibration posterior total variation 0.06954
Cov(lambda,delta)                     -8.41e-4
variance-addition residual            -4.576e-3
cross-covariance residual              9.04e-4
```

The absolute-length prior has become scientifically active. Reporting the simple calibration-floor identity in this regime would be incorrect.

## 11. Interpretation for HgCdTe measurement design

The exact result separates two quantities:

1. **relative correlation length**, measured in units of the effective probe calibration;
2. **absolute correlation length**, which inherits the full common calibration distribution.

No amount of repeated data under the same uncalibrated absolute scale can remove that distinction. Additional measurements help only if they introduce independently calibrated absolute-length information or a different observation operator that is not reducible to $s/\xi$.

The practical reporting rule is:

- report the relative-scale posterior from the data;
- report the calibration prior independently;
- obtain the absolute log-length posterior by convolution;
- declare any informative absolute-length prior and monitor boundary mass;
- do not present a local Fisher calibration floor as globally exact when support boundaries are active.

## 12. Claim boundary

Posterior reparameterization, convolution, and cumulant addition are established probability theory. The R04-specific contribution is the exact measurement consequence, deterministic verification, and bounded-prior failure diagnostic integrated with the HgCdTe multiscale observation model.

The result does not establish a specimen correlation length, validate Gaussian covariance, or authorize manuscript writing.

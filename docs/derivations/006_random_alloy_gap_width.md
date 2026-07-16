# Derivation 006: ideal random-alloy composition width and local gap-sign probability

## Scope

This derivation gives a low-cost statistical diagnostic for deciding when a mean alloy gap may be smaller than local composition-induced variation.

It is **not** a substitute for SQS, CPA, SCBA, localization, optical-tail, or transport calculations. It assumes independent cation occupations and linearizes the gap about the mean composition.

## 1. Local composition statistics

Consider a coarse-graining region containing $N$ cation sites. Let each site be Cd with probability $x$ and Hg with probability $1-x$.

The local Cd fraction is

$$
\hat x_N=\frac{1}{N}\sum_{i=1}^{N}X_i,
\qquad
X_i\in\{0,1\}.
$$

For an ideal uncorrelated random alloy,

$$
\mathbb E[\hat x_N]=x,
$$

and

$$
\boxed{
\sigma_x(N)=
\sqrt{\frac{x(1-x)}{N}}
}.
$$

A real alloy may have clustering, anticorrelation, gradients, ordering, or a nontrivial correlation length. Those effects replace the ideal binomial variance with an empirically or atomistically determined variance.

## 2. Propagation into signed-gap width

Let the mean signed gap law be $\bar E_g(x,T)$. Linearizing around the mean composition,

$$
E_g(\hat x_N,T)
\approx
\bar E_g(x,T)
+
\frac{\partial \bar E_g}{\partial x}
(\hat x_N-x).
$$

Therefore the ideal composition-induced standard deviation is

$$
\boxed{
\sigma_{E,x}(x,T;N)
\approx
\left|
\frac{\partial \bar E_g}{\partial x}
\right|
\sqrt{\frac{x(1-x)}{N}}
}.
$$

This width is a distribution of local gap values under a declared coarse-graining scale. It is not automatically equal to a quasiparticle linewidth or optical Urbach energy.

## 3. Opposite-sign local fraction

Under the Gaussian approximation,

$$
E_g^{\mathrm{local}}
\sim
\mathcal N(\bar E_g,\sigma_E^2).
$$

The fraction of local regions with the opposite sign from the mean is

$$
\boxed{
p_{\mathrm{opp}}
=
\frac{1}{2}
\operatorname{erfc}
\left(
\frac{|\bar E_g|}{\sqrt{2}\sigma_E}
\right)
}.
$$

Useful reference values are:

| $|\bar E_g|/\sigma_E$ | opposite-sign fraction |
|---:|---:|
| 1 | 15.87% |
| 2 | 2.28% |
| 3 | 0.135% |

Thus a positive disorder-averaged signed gap does not imply that every local region is normal, and a negative mean gap does not imply that every local region is inverted.

This probability is a local-sign statistic, not a bulk topological invariant.

## 4. Minimum averaging volume for a resolved sign

Demand that the mean signed gap exceed $z$ ideal composition standard deviations:

$$
|\bar E_g|
\ge
z\sigma_{E,x}.
$$

Solving for $N$ gives

$$
\boxed{
N_{\min}
=
x(1-x)
\left(
\frac{z|\partial_x\bar E_g|}
{|\bar E_g|}
\right)^2
}.
$$

This equation exposes the divergence near inversion:

$$
N_{\min}\propto |\bar E_g|^{-2}.
$$

No finite fixed coarse-graining volume can make an exactly zero mean gap sign-definite in an ideal random alloy.

## 5. Numerical HgCdTe example

Using the Laurenti law at

$$
x=0.17,\qquad T=77\ \mathrm K,
$$

one obtains

$$
\frac{\partial E_g}{\partial x}
\approx1.726\ \mathrm{eV}.
$$

For a zincblende lattice parameter $a\approx0.646$ nm, there are four cation sites per conventional cubic cell. An equivalent cubic length is estimated from

$$
L_N
=\left(\frac{Na^3}{4}\right)^{1/3}.
$$

| Mean-gap magnitude | $N_{\min}$ at $1\sigma$ | cube length | $N_{\min}$ at $3\sigma$ | cube length |
|---:|---:|---:|---:|---:|
| 2 meV | 105,102 | 19.2 nm | 945,922 | 39.9 nm |
| 5 meV | 16,816 | 10.4 nm | 151,348 | 21.7 nm |
| 10 meV | 4,204 | 6.57 nm | 37,837 | 13.7 nm |
| 20 meV | 1,051 | 4.14 nm | 9,459 | 8.61 nm |
| 50 meV | 168 | 2.25 nm | 1,513 | 4.67 nm |

These values are not predictions of the physical coherence volume. They show how strongly a near-zero mean gap depends on the spatial scale over which composition is averaged.

## 6. Correlated-alloy generalization

For correlated occupation variables,

$$
\operatorname{Var}(\hat x_N)
=
\frac{1}{N^2}
\sum_{i,j}
\operatorname{Cov}(X_i,X_j).
$$

Define an effective number of independent sites $N_{\mathrm{eff}}$ through

$$
\operatorname{Var}(\hat x_N)
\equiv
\frac{x(1-x)}{N_{\mathrm{eff}}}.
$$

Then all equations above remain valid after replacing $N$ with $N_{\mathrm{eff}}$.

Clustering gives

$$
N_{\mathrm{eff}}<N,
$$

and therefore broader local-gap statistics than the binomial estimate. Anticorrelation or short-range ordering can give the opposite trend.

## 7. Required reporting standard

A disorder-aware analytical model near inversion should report at minimum:

1. the mean signed gap $\bar E_g$;
2. the width definition $\sigma_E$ or $\Gamma_E$;
3. the spatial or spectral coarse-graining scale;
4. the assumed correlation model;
5. the implied opposite-sign fraction when meaningful;
6. whether the reported gap is spectral, optical, transport, mobility, or effective-medium.

A single number called “the bandgap” is incomplete when its magnitude is comparable to the relevant width.

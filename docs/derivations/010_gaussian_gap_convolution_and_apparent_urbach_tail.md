# Derivation 010: Gaussian local-gap convolution and an apparent Urbach tail

## 1. Objective

This derivation asks whether a spatial or ensemble distribution of local band gaps can produce an absorption spectrum that looks exponential below the mean gap, and whether the resulting fitted tail energy uniquely identifies the underlying gap width.

The answer is:

1. yes, a Gaussian gap distribution can look highly exponential over a finite dynamic range;
2. no, the apparent tail is not exactly exponential;
3. the fitted tail energy depends on the fit window and intrinsic-edge model;
4. therefore the inverse problem is not unique without additional information.

The result is an observation-model statement. It does not identify the microscopic origin of the gap distribution.

## 2. Controlled local absorption edge

Let the local gap be $G$. Consider the intrinsic-edge family

$$
\alpha(E\mid G)=A(E-G)_+^p,
$$

with

$$
(y)_+=\max(y,0),
\qquad p\ge0.
$$

Important cases are:

- $p=0$: ideal step edge;
- $p=1/2$: parabolic square-root edge;
- $p=1$: linear edge;
- $p=2$: a steeper effective edge.

This family is an analytically controlled sensitivity basis. It does not replace the full Kane or Anderson-Herrmann expression.

## 3. Gaussian local-gap distribution

Write

$$
G\sim\mathcal N(\mu_G,\sigma_G^2).
$$

The averaged absorption is

$$
\bar\alpha(E)
=
A\int_{-\infty}^{E}
(E-G)^p
\frac{1}{\sqrt{2\pi}\sigma_G}
\exp\left[-\frac{(G-\mu_G)^2}{2\sigma_G^2}\right]
\,dG.
$$

Introduce the standardized energy

$$
z=\frac{E-\mu_G}{\sigma_G}
$$

and the variable

$$
u=\frac{G-\mu_G}{\sigma_G}.
$$

Then

$$
\boxed{
\bar\alpha(E)
=A\sigma_G^p F_p(z)
}
$$

where

$$
F_p(z)
=
\int_{-\infty}^{z}
(z-u)^p\phi(u)\,du
$$

and

$$
\phi(u)=\frac{e^{-u^2/2}}{\sqrt{2\pi}}.
$$

The spectral shape is therefore scale invariant. Changing $\sigma_G$ stretches the energy axis and rescales the amplitude by $\sigma_G^p$.

## 4. Closed forms for integer exponents

Let

$$
\Phi(z)=\int_{-\infty}^{z}\phi(u)\,du.
$$

### Step edge, $p=0$

$$
F_0(z)=\Phi(z).
$$

### Linear edge, $p=1$

$$
\boxed{
F_1(z)=z\Phi(z)+\phi(z)
}
$$

so

$$
\bar\alpha(E)
=A\left[(E-\mu_G)\Phi(z)+\sigma_G\phi(z)\right].
$$

### Quadratic edge, $p=2$

$$
\boxed{
F_2(z)
=(z^2+1)\Phi(z)+z\phi(z)
}
$$

and

$$
\bar\alpha(E)
=A\left[
((E-\mu_G)^2+\sigma_G^2)\Phi(z)
+(E-\mu_G)\sigma_G\phi(z)
\right].
$$

These expressions provide exact regression tests for the numerical quadrature.

## 5. Why the tail looks exponential

For $z\ll0$, the dominant contribution comes from local gaps near the photon energy. Set

$$
y=z-u\ge0.
$$

Then

$$
F_p(z)
=
\int_0^\infty y^p\phi(z-y)\,dy.
$$

Using

$$
\phi(z-y)
=
\phi(z)\exp\left(zy-\frac{y^2}{2}\right)
$$

and expanding for large negative $z$, the leading term is

$$
\boxed{
F_p(z)
\sim
\frac{\Gamma(p+1)}{\sqrt{2\pi}}
\frac{e^{-z^2/2}}{(-z)^{p+1}}
}
\qquad(z\to-\infty).
$$

Thus

$$
\ln\bar\alpha(E)
\approx
C
-\frac{z^2}{2}
-(p+1)\ln(-z).
$$

Over a limited $z$ interval this curved function can be fitted extremely well by a straight line.

## 6. The local apparent Urbach energy is not constant

Define the local log-slope

$$
S(E)=\frac{d\ln\bar\alpha}{dE}.
$$

An exact exponential would have

$$
S(E)=\frac{1}{W}
$$

with constant $W$.

From the asymptotic form,

$$
S(E)
\approx
\frac{1}{\sigma_G}
\left[
-z-\frac{p+1}{z}
\right].
$$

Therefore the local effective tail energy is

$$
\boxed{
W_{\mathrm{eff}}(E)
\approx
\frac{\sigma_G}
{-z-(p+1)/z}
}
$$

and varies with photon energy. The Gaussian convolution is not an Urbach law even when a finite-range log-linear fit has $R^2$ close to one.

## 7. Herrmann source convention

Herrmann et al. (1992) use

$$
P(G)=
\frac{1}{2s\sqrt{\pi}}
\exp\left[-\frac{(G-\bar G)^2}{4s^2}\right].
$$

Comparison with the standard Gaussian gives

$$
\boxed{
\sigma_G=\sqrt{2}\,s
}.
$$

The paper reports that convolution with its intrinsic branch gives a nearly exponential tail in the `1-100 cm^-1` range with

$$
W\approx\frac{s}{2}.
$$

## 8. Controlled reproduction

The repository normalizes the distributed absorption to

$$
\bar\alpha(\mu_G)=1000\ \mathrm{cm^{-1}}
$$

and fits

$$
\ln\bar\alpha(E)=a+\frac{E}{W_{\mathrm{fit}}}
$$

for

$$
1\le\bar\alpha\le100\ \mathrm{cm^{-1}}.
$$

For $p=1/2$,

$$
\boxed{
\frac{W_{\mathrm{fit}}}{s}=0.50474
}
$$

with

$$
R^2=0.99566.
$$

This independently reproduces the reported approximately-$s/2$ scale.

## 9. Fit-window non-uniqueness

For the same $p=1/2$ spectrum:

| fit window ($\mathrm{cm^{-1}}$) | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---|---:|---:|
| 0.1-100 | 0.46075 | 0.99307 |
| 1-100 | 0.50474 | 0.99566 |
| 10-100 | 0.56808 | 0.99828 |
| 10-500 | 0.66850 | 0.99188 |
| 100-500 | 0.80860 | 0.99734 |

The source window and upper window differ by

$$
\frac{0.80860}{0.50474}-1
=0.602.
$$

Therefore a `60.2%` change in the inferred tail energy can be produced solely by changing the fit window, even though both fits have $R^2>0.995$.

## 10. Intrinsic-edge non-uniqueness

Using the same source window:

| $p$ | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---:|---:|---:|
| 0.5 | 0.50474 | 0.99566 |
| 1.0 | 0.50014 | 0.99620 |
| 2.0 | 0.48375 | 0.99712 |

Substantially different intrinsic edges produce nearly indistinguishable exponential-looking tails. The total spread in $W_{\mathrm{fit}}/s$ is only about `4.2%` of the maximum value.

Thus the tail fit alone weakly constrains $p$.

## 11. Inverse problem

Suppose an experiment reports

$$
W_{\mathrm{fit}}=4\ \mathrm{meV}.
$$

Within only the declared exponent and fit-window family,

$$
0.31594
\le
\frac{W_{\mathrm{fit}}}{\sigma_G}
\le
0.57177.
$$

Therefore

$$
\boxed{
6.996\ \mathrm{meV}
\le
\sigma_G
\le
12.661\ \mathrm{meV}
}
$$

and

$$
\boxed{
4.947\ \mathrm{meV}
\le
s
\le
8.952\ \mathrm{meV}
}.
$$

The inferred width spans a factor of

$$
1.81.
$$

This is before including uncertainties from carrier filling, temperature-dependent phonon broadening, shallow levels, excitons, optical inversion, or instrument response.

## 12. Identifiability statement

A measured exponential tail supplies a slope over a selected range. The latent model contains at least:

- gap-distribution width;
- intrinsic-edge exponent or band structure;
- amplitude normalization;
- fit range;
- carrier state;
- temperature-dependent broadening;
- defect and shallow-level contributions;
- instrument and thickness response.

One scalar fitted tail energy cannot identify all of these quantities.

The valid statement is therefore:

> A Gaussian gap distribution can be consistent with an Urbach-like tail, but an Urbach-like tail does not uniquely identify a Gaussian gap distribution or its width.

## 13. Falsification and escalation tests

The controlled operator should be rejected or extended if:

1. calibrated data show systematic curvature incompatible with every declared $p$;
2. the fitted $W$ is stable under broad fit-window changes but the Gaussian model predicts strong variation;
3. independently constrained above-gap dispersion cannot reproduce the below-gap spectrum for any $\sigma_G$;
4. carrier-density variation changes the tail in a way requiring explicit band filling;
5. temperature dependence cannot be decomposed into permanent and dynamic components;
6. shallow-level or excitonic features are spectrally resolved.

Only after one of these tests identifies a decision-changing deficiency should the program activate the complete Anderson/Herrmann or atomistic disorder branch.

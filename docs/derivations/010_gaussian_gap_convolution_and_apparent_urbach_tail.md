# Derivation 010: Gaussian local-gap convolution and an apparent Urbach tail

## 1. Objective

This derivation asks whether a distribution of local HgCdTe gaps can produce an absorption spectrum that appears exponential below the mean gap, and whether the fitted tail energy uniquely identifies the latent gap width.

The result is:

1. a Gaussian gap distribution can look strongly exponential over a finite dynamic range;
2. the convolved spectrum is not an exact exponential;
3. the fitted tail energy depends on the absorption window and intrinsic edge;
4. one fitted tail slope does not uniquely identify the latent gap width.

This is an observation-model statement. It does not identify the microscopic origin of the distribution.

## 2. Controlled local edge

Let the local gap be $G$. Use the declared intrinsic-edge family

$$
\alpha(E\mid G)=A(E-G)_+^p,
$$

where

$$
(y)_+=\max(y,0),
\qquad p\ge0.
$$

Useful controlled cases are:

- $p=0$: ideal step edge;
- $p=1/2$: parabolic square-root edge;
- $p=1$: linear edge;
- $p=2$: steeper effective edge.

This family is an analytical sensitivity basis, not the complete Kane or Anderson-Herrmann absorption model.

## 3. Gaussian gap distribution

Assume

$$
G\sim\mathcal N(\mu_G,\sigma_G^2).
$$

The ensemble absorption is

$$
\bar\alpha(E)
=
A\int_{-\infty}^{E}
(E-G)^p
\frac{1}{\sqrt{2\pi}\sigma_G}
\exp\left[-\frac{(G-\mu_G)^2}{2\sigma_G^2}\right]
\,dG.
$$

Define

$$
z=\frac{E-\mu_G}{\sigma_G},
\qquad
u=\frac{G-\mu_G}{\sigma_G}.
$$

Then

$$
\boxed{
\bar\alpha(E)=A\sigma_G^p F_p(z)
}
$$

with

$$
F_p(z)=
\int_{-\infty}^{z}(z-u)^p\phi(u)\,du,
$$

and

$$
\phi(u)=\frac{e^{-u^2/2}}{\sqrt{2\pi}}.
$$

The shape is scale invariant: changing $\sigma_G$ stretches the energy axis and changes the amplitude by $\sigma_G^p$.

## 4. Closed forms

Let

$$
\Phi(z)=\int_{-\infty}^{z}\phi(u)\,du.
$$

For $p=0$,

$$
F_0(z)=\Phi(z).
$$

For $p=1$,

$$
\boxed{F_1(z)=z\Phi(z)+\phi(z)},
$$

so

$$
\bar\alpha(E)=A\left[(E-\mu_G)\Phi(z)+\sigma_G\phi(z)\right].
$$

For $p=2$,

$$
\boxed{F_2(z)=(z^2+1)\Phi(z)+z\phi(z)},
$$

and

$$
\bar\alpha(E)=A\left[
((E-\mu_G)^2+\sigma_G^2)\Phi(z)
+(E-\mu_G)\sigma_G\phi(z)
\right].
$$

These expressions are used as exact regression tests for the numerical operator.

## 5. Why a Gaussian convolution looks exponential

For $z\ll0$, set $y=z-u\ge0$. Then

$$
F_p(z)=\int_0^\infty y^p\phi(z-y)\,dy.
$$

Since

$$
\phi(z-y)=\phi(z)\exp\left(zy-\frac{y^2}{2}\right),
$$

the leading large-negative-$z$ behavior is

$$
\boxed{
F_p(z)
\sim
\frac{\Gamma(p+1)}{\sqrt{2\pi}}
\frac{e^{-z^2/2}}{(-z)^{p+1}}
}
\qquad(z\rightarrow-\infty).
$$

Therefore

$$
\ln\bar\alpha(E)
\approx
C-rac{z^2}{2}-(p+1)\ln(-z).
$$

This function is curved, but over a restricted interval it can be approximated very well by a straight line.

## 6. The effective tail energy varies with energy

Define the local logarithmic slope

$$
S(E)=\frac{d\ln\bar\alpha}{dE}.
$$

An exact Urbach law would have constant

$$
S(E)=\frac{1}{W}.
$$

From the asymptotic form,

$$
S(E)
\approx
\frac{1}{\sigma_G}
\left[-z-\frac{p+1}{z}\right].
$$

Hence

$$
\boxed{
W_{\mathrm{eff}}(E)
\approx
\frac{\sigma_G}{-z-(p+1)/z}
}.
$$

The apparent local tail energy changes with photon energy. A finite-window $R^2$ near one is not evidence that the underlying spectrum has a constant Urbach slope.

## 7. Herrmann convention

Herrmann et al. 1992 write their Eq. (8) as

$$
P(G)=
\frac{1}{2s\sqrt{\pi}}
\exp\left[-\frac{(G-\bar G)^2}{4s^2}\right].
$$

Comparison with the standard Gaussian gives

$$
\boxed{\sigma_G=\sqrt{2}\,s}.
$$

They state that convolution with their intrinsic branch gives a nearly exponential tail over `1-100 cm^-1`, with

$$
W\approx\frac{s}{2}.
$$

## 8. Numerical method

The thresholded local edge has a moving nonanalytic point at $G=E$. Integrating the thresholded function on one fixed global node grid gives slow and irregular convergence in the deep tail.

The implemented operator instead evaluates

$$
\bar\alpha(E)
=A\int_{G_{\min}}^{\min(E,G_{\max})}
(E-G)^p P(G)\,dG
$$

and maps Gauss-Legendre nodes separately for every photon energy. The integrand is smooth on each mapped interval.

For the tested square-root tail:

```text
maximum relative change, order 256 -> 512 = 5.78e-7
```

The $p=1$ and $p=2$ branches agree with their closed forms at approximately `1e-10` and `1e-9` relative tolerance, respectively.

## 9. Source-aligned reproduction

Declare

$$
\bar\alpha(\mu_G)=1000\ \mathrm{cm^{-1}}
$$

and fit

$$
\ln\bar\alpha(E)=a+\frac{E}{W_{\mathrm{fit}}}
$$

only where

$$
1\le\bar\alpha\le100\ \mathrm{cm^{-1}}.
$$

For $p=1/2$,

$$
\boxed{\frac{W_{\mathrm{fit}}}{s}=0.50504},
$$

with

$$
R^2=0.99570.
$$

Thus the controlled square-root calculation independently reproduces the source scale $W\approx s/2$.

For `s=8 meV`,

$$
W_{\mathrm{fit}}=4.040\ \mathrm{meV}.
$$

## 10. Fit-window dependence

For the same square-root spectrum:

| fit window ($\mathrm{cm^{-1}}$) | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---|---:|---:|
| 0.1-100 | 0.46096 | 0.99307 |
| 1-100 | 0.50504 | 0.99570 |
| 10-100 | 0.56806 | 0.99836 |
| 10-500 | 0.66828 | 0.99190 |
| 100-500 | 0.80871 | 0.99738 |

Moving from `1-100` to `100-500 cm^-1` changes the fitted energy by

$$
\frac{0.80871}{0.50504}-1=0.601.
$$

Thus the inferred tail energy rises by `60.1%` solely because the observation window changes, even though both fits have $R^2>0.995$.

## 11. Intrinsic-edge dependence

Over `1-100 cm^-1`:

| exponent $p$ | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---:|---:|---:|
| 0.5 | 0.50504 | 0.99570 |
| 1.0 | 0.50000 | 0.99620 |
| 2.0 | 0.48375 | 0.99712 |

Substantially different intrinsic edges produce similarly strong exponential-looking tails. The source-window slope changes by only approximately `4.2%` of the largest ratio.

## 12. Inverse problem

Suppose an experiment reports

$$
W_{\mathrm{fit}}=4\ \mathrm{meV}.
$$

Within the declared exponent and fit-window family,

$$
0.31594
\le
\frac{W_{\mathrm{fit}}}{\sigma_G}
\le
0.57184.
$$

Therefore

$$
\boxed{
6.995\ \mathrm{meV}
\le\sigma_G\le
12.661\ \mathrm{meV}
}
$$

and

$$
\boxed{
4.946\ \mathrm{meV}
\le s\le
8.952\ \mathrm{meV}
}.
$$

The inferred width spans a factor of `1.81` before adding carrier filling, phonons, shallow levels, excitons, optical inversion, or instrumental response.

## 13. Identifiability conclusion

A fitted tail supplies one slope over one declared range. The latent observation model contains at least:

- gap-distribution width;
- intrinsic-edge structure;
- normalization;
- fit window;
- carrier state;
- temperature-dependent broadening;
- shallow-level and defect contributions;
- optical and instrumental transfer.

One fitted scalar cannot identify all of these quantities.

The controlling statement is:

> A Gaussian gap distribution can be consistent with an Urbach-like tail, but an Urbach-like tail does not uniquely identify a Gaussian gap distribution or its width.

## 14. Falsification and escalation gates

The controlled operator should be rejected or extended if:

1. calibrated data show curvature incompatible with every declared $p$;
2. measured $W$ remains stable under broad fit-window changes when the Gaussian model predicts substantial variation;
3. independently constrained above-gap dispersion cannot reproduce the tail for any $\sigma_G$;
4. carrier-density variation requires explicit band filling;
5. temperature dependence cannot be separated into permanent and dynamic components;
6. shallow-level or excitonic features are spectrally resolved.

Only a decision-changing failure justifies activation of the complete Anderson-Herrmann, carrier-filled, or atomistic-disorder branch.

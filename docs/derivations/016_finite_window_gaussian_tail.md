# Derivation 016: differential structure of Gaussian-distributed absorption tails

## Scope

This derivation belongs to the distributional band-edge observables program, contribution R03 and Issue #225.

It analyzes the controlled observation model

$$
\alpha_p(E)
=
A\,\mathbb E[(E-G)_+^p],
\qquad
G\sim\mathcal N(\mu_G,\sigma_G^2),
\qquad p\ge0.
$$

The model represents a sharp local power-law edge averaged over a Gaussian distribution of local gaps. It is not a complete HgCdTe absorption theory and does not establish the microscopic origin of a measured tail.

Herrmann et al. 1992 already state that a Gaussian gap distribution can produce a nearly exponential HgCdTe tail over the finite `1-100 cm^-1` range. That qualitative finite-window observation is prior art. The result derived here is narrower: the exact differential identities, log-curvature sign, monotonic local tail energy, and deep-tail asymptotic of the declared Gaussian-power operator.

## Dimensionless reduction

Define

$$
z=\frac{E-\mu_G}{\sigma_G}
$$

and

$$
t=\frac{E-G}{\sigma_G}.
$$

Then

$$
\boxed{
\alpha_p(E)=A\sigma_G^p F_p(z)
}
$$

with

$$
F_p(z)
=
\int_0^\infty t^p\phi(z-t)\,dt,
$$

where

$$
\phi(y)=\frac{1}{\sqrt{2\pi}}e^{-y^2/2}.
$$

All differential lineshape information depends only on $z$ and $p$. The amplitude $A$ cancels from logarithmic derivatives, while $\sigma_G$ supplies the energy scale.

## Exact derivative identities

Differentiate the Gaussian kernel rather than the thresholded power:

$$
\frac{\partial}{\partial z}\phi(z-t)
=-(z-t)\phi(z-t)
=(t-z)\phi(z-t).
$$

Therefore

$$
\begin{aligned}
F_p'(z)
&=\int_0^\infty t^p(t-z)\phi(z-t)\,dt\\
&=F_{p+1}(z)-zF_p(z),
\end{aligned}
$$

so

$$
\boxed{F_p'=F_{p+1}-zF_p}.
$$

Differentiate once more:

$$
\begin{aligned}
F_p''
&=F_{p+1}'-F_p-zF_p'\\
&=F_{p+2}-zF_{p+1}-F_p-z(F_{p+1}-zF_p),
\end{aligned}
$$

which gives

$$
\boxed{
F_p''
=F_{p+2}-2zF_{p+1}+(z^2-1)F_p
}.
$$

These identities evaluate the differential tail using three nonnegative Gaussian moments. No finite difference of $\log\alpha$ is required.

## Local apparent tail energy

Let

$$
L(E)=\log\alpha_p(E).
$$

Then

$$
\frac{dL}{dE}
=\frac{1}{\sigma_G}\frac{F_p'}{F_p}.
$$

Define

$$
W_{\rm loc}(E)
=\left(\frac{dL}{dE}\right)^{-1}.
$$

Hence

$$
\boxed{
\frac{W_{\rm loc}}{\sigma_G}
=\frac{F_p}{F_p'}
}.
$$

A true Urbach exponential

$$
\alpha_U(E)=\alpha_0\exp(E/W_U)
$$

has constant $W_{\rm loc}=W_U$.

## Log-concavity theorem

The Gaussian density is log-concave. The one-sided power function

$$
h_p(y)=y_+^p
$$

is log-concave for every $p\ge0$: for $p>0$, $\log h_p=p\log y$ is concave on its convex support $y>0$; for $p=0$, $h_0$ is the indicator of a half-line.

The absorption is the convolution

$$
\alpha_p(E)=A(h_p*f_G)(E).
$$

The convolution of log-concave functions is log-concave by the established Prékopa-Leindler result. Therefore

$$
\boxed{
\frac{d^2\log\alpha_p}{dE^2}\le0
}.
$$

Since $d\log\alpha_p/dE>0$ in the subgap tail,

$$
\frac{dW_{\rm loc}}{dE}
=-
\frac{d^2\log\alpha_p/dE^2}
{(d\log\alpha_p/dE)^2}
\ge0.
$$

Thus

$$
\boxed{
W_{\rm loc}(E)\text{ is nondecreasing with photon energy.}
}
$$

The distributed-gap spectrum can resemble an exponential over a finite interval, but its local exponential energy cannot remain constant over the complete tail.

## Deep-subgap asymptotic

Set

$$
z=-a,
\qquad a>0.
$$

Then

$$
F_p(-a)
=\int_0^\infty t^p\phi(a+t)\,dt
=\phi(a)\int_0^\infty t^p e^{-at-t^2/2}\,dt.
$$

Use $y=at$:

$$
F_p(-a)
=\phi(a)a^{-(p+1)}
\int_0^\infty y^p e^{-y}e^{-y^2/(2a^2)}\,dy.
$$

As $a\to\infty$, dominated convergence gives

$$
\boxed{
F_p(z)
\sim
\Gamma(p+1)\phi(z)(-z)^{-(p+1)},
\qquad z\to-\infty.
}
$$

Expanding the last exponential gives

$$
F_p(-a)
=
\Gamma(p+1)\phi(a)a^{-(p+1)}
\left[
1-
\frac{(p+1)(p+2)}{2a^2}
+O(a^{-4})
\right].
$$

Therefore

$$
\log F_p(z)
=-\frac{z^2}{2}
-(p+1)\log(-z)
+\text{constant}
+O(z^{-2}).
$$

Differentiation gives

$$
\boxed{
\frac{d\log F_p}{dz}
=-z-\frac{p+1}{z}+O((-z)^{-3})
}
$$

and

$$
\boxed{
\frac{d^2\log F_p}{dz^2}
=-1+\frac{p+1}{z^2}+O((-z)^{-4}).
}
$$

In physical units,

$$
\boxed{
\frac{d^2\log\alpha_p}{dE^2}
\longrightarrow
-\frac{1}{\sigma_G^2}
}
$$

and

$$
\boxed{
\frac{W_{\rm loc}}{\sigma_G}
\sim
\left[-z-\frac{p+1}{z}\right]^{-1}.
}
$$

A true exponential has zero log curvature. The Gaussian-distributed power-edge tail instead approaches curvature $-1/\sigma_G^2$. Its deepest subgap behavior is Gaussian with an algebraic prefactor, not exponential.

## Gaussian square-root benchmark

For $p=1/2$, the dimensionless local tail energy changes substantially across the subgap domain:

```text
z       W_local / sigma_G     sigma_G^2 d2 log(alpha)/dE2
-8      0.12223768            -0.97895032
-6      0.16038506            -0.96519098
-4      0.23088740            -0.93409938
-2      0.39483481            -0.84918406
 0      0.95597762            -0.59421979
```

Between $z=-6$ and $z=0$, the local apparent tail energy increases by a factor of approximately `5.96`.

The corrected source-normalized finite-window calculations are:

```text
fit window        W_fit / sigma_G     R^2
1-100 cm^-1       0.35712             0.99570
100-500 cm^-1     0.57184             0.99738
```

The apparent width increases by `60.1%` when only the fit window changes. Herrmann's printed source parameter satisfies `s=sigma_G`; therefore the simplified power-edge result does not reproduce the source-reported approximate `W=s/2` coefficient. That historical mapping belongs to the full source-native intrinsic branch, not to the differential theorem proved here.

## Published-spectrum interpretation

The theorem supplies a falsification diagnostic, not a mechanism identification:

- constant local tail energy is compatible with a true exponential over the resolved interval;
- systematic increase of local tail energy is expected from the Gaussian distributed-gap power-edge model;
- positive log curvature cannot be produced by this log-concave family;
- finite spectral range, digitization, noise, baseline error, and instrumental convolution can obscure curvature;
- observing the predicted curvature does not prove composition disorder because other mechanisms may produce similar behavior.

Chang 2006 and 2007 use a piecewise model with an exact exponential below the joining energy and enforce continuity of the absorption and first derivative. Their formulation does not impose or test second-derivative continuity. The published figures mainly cover absorption coefficients of approximately `10^2-10^4 cm^-1`, so they are more suitable for testing the join than the deep-tail asymptote.

A practical paper-only comparison should fit several nonoverlapping windows or estimate a regularized derivative of $\log\alpha$, then propagate digitization and baseline uncertainty. No new laboratory measurement is required.

## Claim boundary

Established prior art includes:

- the Urbach exponential description of HgCdTe tails;
- Gaussian gap-distribution convolution as an inhomogeneous-broadening model;
- the observation that this convolution can look nearly exponential over a finite absorption interval;
- joining an empirical exponential tail to a Kane-type intrinsic branch;
- fitting the first derivative of the absorption edge.

The candidate project result is restricted to:

- exact derivative identities for the declared Gaussian-power operator;
- its log-concavity consequence;
- monotonic local apparent tail energy;
- the deep-tail curvature limit;
- a finite-range observation diagnostic based on those results.

This derivation does not identify:

- a specimen gap distribution;
- a composition variance;
- a spatial correlation length;
- an Urbach microscopic mechanism;
- a PL or quasiparticle linewidth;
- a complete Kane, excitonic, phonon, defect, or free-carrier absorption law.
